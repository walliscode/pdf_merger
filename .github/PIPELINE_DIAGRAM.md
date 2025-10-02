# CI/CD Pipeline Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         TRIGGER EVENT                                │
│  • Push to main branch                                               │
│  • Pull Request to main                                              │
│  • Manual workflow dispatch                                          │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────────┐
        │          PARALLEL EXECUTION                │
        │                                            │
        │    ┌──────────┐        ┌──────────┐      │
        │    │   TEST   │        │   LINT   │      │
        │    └──────────┘        └──────────┘      │
        │         │                    │            │
        │    • Python 3.12        • flake8         │
        │    • Install deps       • pylint         │
        │    • Run tests          • Check style    │
        │    • pandoc/LaTeX       • Report issues  │
        │         │                    │            │
        └─────────┼────────────────────┼────────────┘
                  │                    │
                  └─────────┬──────────┘
                            │
                     ✓ Tests Pass
                     ✓ Lint Pass
                            │
                            ▼
        ┌────────────────────────────────────────────┐
        │       PARALLEL BUILD JOBS                  │
        │                                            │
        │  ┌──────────────┐  ┌──────────────┐      │
        │  │   PACKAGE    │  │ EXECUTABLE   │      │
        │  └──────────────┘  └──────────────┘      │
        │        │                  │               │
        │  • setup.py         • PyInstaller         │
        │  • Build wheel      • Linux build         │
        │  • Build source     • Windows build       │
        │  • Upload           • macOS build         │
        │                     • Upload              │
        │                                           │
        │  ┌──────────────────────────────┐        │
        │  │         DOCKER               │        │
        │  └──────────────────────────────┘        │
        │              │                            │
        │        • Build image                      │
        │        • Tag (latest, SHA, branch)        │
        │        • Push to Docker Hub (main only)   │
        │        • Save artifact (PR only)          │
        │                                           │
        └────────────────────────────────────────────┘
                            │
                            ▼
        ┌────────────────────────────────────────────┐
        │            ARTIFACTS AVAILABLE             │
        │                                            │
        │  📦 Python Package                         │
        │     • pdf_merger-1.0.0-py3-none-any.whl   │
        │     • pdf_merger-1.0.0.tar.gz             │
        │                                            │
        │  🔨 Executables                            │
        │     • pdf-merger (Linux)                   │
        │     • pdf-merger.exe (Windows)             │
        │     • pdf-merger (macOS)                   │
        │                                            │
        │  🐳 Docker Image                           │
        │     • username/pdf-merger:latest           │
        │     • username/pdf-merger:SHA              │
        │     • username/pdf-merger:branch           │
        │                                            │
        └────────────────────────────────────────────┘
                            │
                            ▼
        ┌────────────────────────────────────────────┐
        │         DISTRIBUTION CHANNELS              │
        │                                            │
        │  • GitHub Actions Artifacts (30 days)      │
        │  • Docker Hub (persistent)                 │
        │  • GitHub Releases (when tagged)           │
        │                                            │
        └────────────────────────────────────────────┘
```

## Job Dependencies

```
Trigger
  │
  ├─→ [Test] ────────┐
  │                  │
  └─→ [Lint] ────────┤
                     │
                     └─→ Tests & Lint Pass
                            │
                            ├─→ [Build Package]
                            │
                            ├─→ [Build Executable]
                            │     ├─→ Linux
                            │     ├─→ Windows
                            │     └─→ macOS
                            │
                            └─→ [Build Docker]
```

## Workflow Stages

### Stage 1: Quality Checks (Parallel)
- **Duration**: ~2-5 minutes
- **Jobs**: Test, Lint
- **Purpose**: Ensure code quality and correctness

### Stage 2: Build Artifacts (Parallel, after Stage 1)
- **Duration**: ~5-10 minutes per job
- **Jobs**: Package, Executable (3x), Docker
- **Purpose**: Create distributable artifacts

### Stage 3: Distribution
- **Duration**: Immediate (artifacts) or ~1-2 minutes (Docker push)
- **Actions**: Upload artifacts, push Docker images
- **Purpose**: Make builds available to users

## Artifact Lifecycle

### Python Package
```
Build → Upload to GitHub Actions → Download manually or via releases
```

### Executables
```
Build (Linux/Windows/macOS) → Upload to GitHub Actions → Download per platform
```

### Docker Image
```
Build → Tag → Push to Docker Hub → Pull with docker pull
                     ↓
              (or save as artifact for PRs)
```

## Conditional Behavior

### On Pull Request
- ✅ Run tests
- ✅ Run linting
- ✅ Build all artifacts
- ✅ Save Docker image as artifact
- ❌ Don't push to Docker Hub

### On Main Branch Push
- ✅ Run tests
- ✅ Run linting  
- ✅ Build all artifacts
- ✅ Push Docker image to Docker Hub
- ✅ Tag as `latest`, SHA, branch name

### On Manual Trigger
- ✅ Run tests
- ✅ Run linting
- ✅ Build all artifacts
- Behavior depends on branch (same as above)

## Resource Usage

| Job | Runner | Duration | Artifacts |
|-----|--------|----------|-----------|
| Test | ubuntu-latest | ~3 min | Logs |
| Lint | ubuntu-latest | ~2 min | Logs |
| Package | ubuntu-latest | ~2 min | 2 files (~17KB each) |
| Executable (Linux) | ubuntu-latest | ~5 min | 1 file (~8MB) |
| Executable (Windows) | windows-latest | ~5 min | 1 file (~8MB) |
| Executable (macOS) | macos-latest | ~5 min | 1 file (~8MB) |
| Docker | ubuntu-latest | ~3 min | Image or artifact |

**Total parallel execution time**: ~10 minutes (with job dependencies)

## Security Considerations

1. **Docker Hub Credentials**: Stored as GitHub secrets
2. **Non-root Docker User**: Container runs as `pdfuser`
3. **No Secrets in Code**: All sensitive data in environment variables
4. **Minimal Dependencies**: Only required packages installed
5. **Verified Base Images**: Official Python images from Docker Hub

## Monitoring & Debugging

### Check Build Status
- GitHub Actions tab shows all runs
- README badge shows current status
- Email notifications for failures (if configured)

### View Logs
- Click on any job to see detailed logs
- Download logs for offline analysis
- Check specific step failures

### Download Artifacts
- Available from workflow run summary
- 30-day retention for packages and executables
- Docker images persist on Docker Hub

### Troubleshooting
- Review job logs for errors
- Check dependencies and versions
- Verify secrets are configured
- Test locally with `build.sh`

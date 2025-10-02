# Using PDF Merger Releases

This guide explains how to download and use the different distribution formats of PDF Merger.

## Available Formats

PDF Merger is distributed in three formats:

1. **Python Package** - For Python users
2. **Standalone Executables** - No Python installation required
3. **Docker Image** - Containerized deployment

## Python Package

### Installation from Package

Download the `.whl` file from [GitHub Releases](https://github.com/walliscode/pdf_merger/releases) and install:

```bash
pip install pdf_merger-1.0.0-py3-none-any.whl
```

### Usage

After installation, two commands are available:

```bash
# CLI version
pdf-merger /path/to/pdfs "*.pdf" "merged.pdf"

# GUI version
pdf-merger-gui
```

### Uninstallation

```bash
pip uninstall pdf-merger
```

## Standalone Executables

Standalone executables include everything needed to run PDF Merger without Python installed.

### Download

Download the executable for your platform from [GitHub Actions Artifacts](https://github.com/walliscode/pdf_merger/actions):

- **Linux**: `pdf-merger-linux`
- **Windows**: `pdf-merger-windows` 
- **macOS**: `pdf-merger-macos`

Or download from [GitHub Releases](https://github.com/walliscode/pdf_merger/releases) (when available).

### Linux

```bash
# Make executable
chmod +x pdf-merger

# Run
./pdf-merger /path/to/pdfs "*.pdf" "merged.pdf"

# Optional: Move to PATH
sudo mv pdf-merger /usr/local/bin/
```

### Windows

```powershell
# Run from PowerShell or Command Prompt
.\pdf-merger.exe C:\path\to\pdfs "*.pdf" "merged.pdf"
```

Or double-click `pdf-merger.exe` to see usage help.

### macOS

```bash
# Make executable
chmod +x pdf-merger

# Run (may need to allow in Security settings first time)
./pdf-merger /path/to/pdfs "*.pdf" "merged.pdf"

# Optional: Move to PATH
sudo mv pdf-merger /usr/local/bin/
```

**Note**: On first run, macOS may block the executable. Go to System Preferences → Security & Privacy and click "Open Anyway".

## Docker Image

### Pull Image

```bash
docker pull <dockerhub-username>/pdf-merger:latest
```

### Quick Start

```bash
# Show help
docker run --rm <dockerhub-username>/pdf-merger

# Merge PDFs
docker run --rm -v $(pwd)/mypdfs:/data <dockerhub-username>/pdf-merger /data "*.pdf" "merged.pdf"

# Preview mode
docker run --rm -v $(pwd)/mypdfs:/data <dockerhub-username>/pdf-merger --preview /data "*.pdf" "merged.pdf"
```

For detailed Docker usage, see [DOCKER.md](DOCKER.md).

## Common Usage Examples

### Example 1: Merge All PDFs

Merge all PDF files in subdirectories:

```bash
# Python package
pdf-merger /path/to/main/dir "*.pdf" "{directory}_merged.pdf"

# Executable
./pdf-merger /path/to/main/dir "*.pdf" "{directory}_merged.pdf"

# Docker
docker run --rm -v /path/to/main/dir:/data <dockerhub-username>/pdf-merger /data "*.pdf" "{directory}_merged.pdf"
```

### Example 2: Preview Before Merging

See what will be merged without actually merging:

```bash
# Python package
pdf-merger --preview /path/to/main/dir "*.pdf" "{directory}_merged.pdf"

# Executable
./pdf-merger --preview /path/to/main/dir "*.pdf" "{directory}_merged.pdf"

# Docker
docker run --rm -v /path/to/main/dir:/data <dockerhub-username>/pdf-merger --preview /data "*.pdf" "{directory}_merged.pdf"
```

### Example 3: Specific File Pattern

Merge only files matching a pattern:

```bash
# Python package
pdf-merger /path/to/main/dir "report*.pdf" "report_combined.pdf"

# Executable
./pdf-merger /path/to/main/dir "report*.pdf" "report_combined.pdf"

# Docker
docker run --rm -v /path/to/main/dir:/data <dockerhub-username>/pdf-merger /data "report*.pdf" "report_combined.pdf"
```

### Example 4: Merge Configuration Mode

Configure specific files that must be present:

```bash
# Set configuration
pdf-merger --set-merge-config /path/to/main/dir "intro,body,conclusion"

# Merge using configuration
pdf-merger --merge-config /path/to/main/dir "*.pdf" "{directory}_complete.pdf"
```

### Example 5: Verbose Output

Get detailed progress information:

```bash
pdf-merger --verbose /path/to/main/dir "*.pdf" "{directory}_merged.pdf"
```

## Comparison of Formats

| Feature | Python Package | Executable | Docker |
|---------|---------------|------------|---------|
| Python Required | ✅ Yes | ❌ No | ❌ No |
| Size | Small (~17KB) | Large (~8MB) | Medium (~100MB) |
| Startup Speed | Fast | Fast | Medium |
| Easy Updates | ✅ pip | Manual | ✅ docker pull |
| Cross-platform | ✅ Yes | Platform-specific | ✅ Yes |
| Isolation | ❌ No | ✅ Yes | ✅ Yes |
| Best For | Python devs | End users | Servers/Containers |

## Getting Help

For more information:

- **General Usage**: See [README.md](README.md)
- **Docker Usage**: See [DOCKER.md](DOCKER.md)
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)
- **CI/CD Setup**: See [CICD_SETUP.md](CICD_SETUP.md)

For issues or questions, visit the [GitHub Issues](https://github.com/walliscode/pdf_merger/issues) page.

## Version Information

Check your version:

```bash
# Python package
pdf-merger --help | head -1

# Executable
./pdf-merger --help | head -1
```

Current stable version: **1.0.0**

## Support

- **Bug Reports**: [GitHub Issues](https://github.com/walliscode/pdf_merger/issues)
- **Feature Requests**: [GitHub Issues](https://github.com/walliscode/pdf_merger/issues)
- **Discussions**: [GitHub Discussions](https://github.com/walliscode/pdf_merger/discussions)

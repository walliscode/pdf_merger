# Release v1.0.0

## 📦 Distribution Formats

This release includes multiple distribution formats to suit different use cases:

### Python Package
- **Wheel**: `pdf_merger-1.0.0-py3-none-any.whl`
- **Source**: `pdf_merger-1.0.0.tar.gz`
- Install: `pip install pdf_merger-1.0.0-py3-none-any.whl`

### Standalone Executables
- **Linux**: Download from [GitHub Actions Artifacts](../../actions)
- **Windows**: Download from [GitHub Actions Artifacts](../../actions)
- **macOS**: Download from [GitHub Actions Artifacts](../../actions)
- No Python installation required

### Docker Image
```bash
docker pull <dockerhub-username>/pdf-merger:latest
docker pull <dockerhub-username>/pdf-merger:1.0.0
```

## ✨ What's New

### Features
- 🎯 GUI Interface with tkinter
- 🖥️ Full-featured CLI for automation
- 📋 Merge Configuration Mode
- 🔍 Preview Mode
- 📝 Flexible file patterns
- 🏷️ Customizable output naming
- 🔒 Non-destructive operations

### CI/CD Pipeline
- ✅ Automated testing on every commit
- 🔍 Code quality checks with flake8 and pylint
- 📦 Automatic package builds
- 🔨 Cross-platform executable generation
- 🐳 Docker image builds and publishing
- 🚀 Multi-platform support (Linux, Windows, macOS)

## 📚 Documentation

- [README.md](README.md) - General usage and features
- [CICD_SETUP.md](CICD_SETUP.md) - CI/CD pipeline setup
- [DOCKER.md](DOCKER.md) - Docker usage guide
- [RELEASES.md](RELEASES.md) - Distribution formats guide
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contributing guidelines

## 🚀 Quick Start

### Python Package
```bash
pip install pdf_merger-1.0.0-py3-none-any.whl
pdf-merger /path/to/pdfs "*.pdf" "merged.pdf"
```

### Executable
```bash
chmod +x pdf-merger  # Linux/macOS only
./pdf-merger /path/to/pdfs "*.pdf" "merged.pdf"
```

### Docker
```bash
docker run --rm -v $(pwd)/pdfs:/data <dockerhub-username>/pdf-merger /data "*.pdf" "merged.pdf"
```

## 🔧 Requirements

### Python Package
- Python 3.6+
- PyPDF2 3.0.1
- tkinter (for GUI mode)

### Executables
- No dependencies required

### Docker
- Docker Engine

## 🐛 Bug Fixes

List any bug fixes here...

## ⚠️ Breaking Changes

List any breaking changes here...

## 📝 Notes

- Original files are never modified
- Files are sorted naturally
- Configuration files stored in user home directory
- Cross-platform compatible

## 🙏 Contributors

Thanks to everyone who contributed to this release!

## 📄 License

GNU General Public License v3.0 - see [LICENSE](LICENSE) for details.

---

For issues or questions, please visit our [Issues page](../../issues).

# Contributing to PDF Merger

Thank you for your interest in contributing to PDF Merger! This document provides guidelines and instructions for contributing.

## Development Setup

### Prerequisites

- Python 3.6 or higher
- Git
- Docker (optional, for testing Docker builds)

### Setting Up Your Development Environment

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/walliscode/pdf_merger.git
   cd pdf_merger
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install development dependencies:**
   ```bash
   pip install flake8 pylint pyinstaller wheel
   ```

4. **Install system dependencies for testing (Ubuntu/Debian):**
   ```bash
   sudo apt-get install pandoc poppler-utils texlive-latex-base texlive-fonts-recommended texlive-latex-extra
   ```

## Making Changes

### Before You Start

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes in logical, small commits

3. Follow the existing code style and conventions

### Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise
- Maximum line length: 127 characters

### Testing

**Run all tests before submitting:**
```bash
python3 test_pdf_merger.py
```

**The tests require:**
- pandoc (for markdown to PDF conversion)
- pdftotext (for PDF text extraction)
- LaTeX (texlive packages for PDF generation)

### Linting

**Run linters to check code quality:**

```bash
# Check for critical errors
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# Check for style issues
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# Run pylint
pylint *.py
```

## Building

### Build All Artifacts

Use the provided build script:
```bash
./build.sh
```

### Build Python Package Only

```bash
python setup.py sdist bdist_wheel
```

### Build Executable Only

```bash
pyinstaller pdf-merger.spec
```

### Build Docker Image

```bash
docker build -t pdf-merger:dev .
```

## Submitting Changes

### Pull Request Process

1. **Update documentation** if you've changed functionality

2. **Run tests and linters** to ensure code quality:
   ```bash
   python3 test_pdf_merger.py
   flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
   ```

3. **Commit your changes** with clear, descriptive messages:
   ```bash
   git add .
   git commit -m "Add feature: description of what you added"
   ```

4. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request** on GitHub:
   - Provide a clear description of the changes
   - Reference any related issues
   - Ensure all CI/CD checks pass

### Pull Request Guidelines

- **One feature per PR**: Keep pull requests focused on a single feature or bugfix
- **Clear description**: Explain what changes you made and why
- **Pass all checks**: Ensure tests pass and linters report no critical errors
- **Update documentation**: Include documentation updates for new features
- **Reference issues**: Link to related GitHub issues if applicable

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:

- **Tests**: Run automatically on every push and PR
- **Linting**: Code quality checks run on every push and PR
- **Package Build**: Python packages built on successful tests
- **Executable Build**: Cross-platform executables built for Linux, Windows, and macOS
- **Docker Build**: Docker images built and pushed to Docker Hub

For more details, see [CICD_SETUP.md](CICD_SETUP.md).

## Reporting Issues

### Bug Reports

When reporting bugs, please include:

1. **Description**: Clear description of the issue
2. **Steps to reproduce**: Detailed steps to reproduce the problem
3. **Expected behavior**: What you expected to happen
4. **Actual behavior**: What actually happened
5. **Environment**: 
   - OS and version
   - Python version
   - PDF Merger version
6. **Logs**: Any relevant error messages or logs

### Feature Requests

When requesting features, please include:

1. **Description**: Clear description of the feature
2. **Use case**: Explain why this feature would be useful
3. **Examples**: Provide examples of how the feature would work
4. **Alternatives**: Describe any alternative solutions you've considered

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers and beginners
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment or discriminatory language
- Personal attacks or trolling
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

## Questions?

If you have questions about contributing, feel free to:

- Open an issue with the "question" label
- Check existing issues and discussions
- Review the documentation in [README.md](README.md)

## License

By contributing to PDF Merger, you agree that your contributions will be licensed under the GNU General Public License v3.0.

---

Thank you for contributing to PDF Merger! 🎉

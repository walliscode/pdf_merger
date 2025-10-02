# CI/CD Pipeline Setup Guide

This document explains how to set up and use the CI/CD pipeline for the PDF Merger project.

## Overview

The CI/CD pipeline automatically:
1. Runs tests on every push and pull request
2. Checks code quality with linters
3. Builds Python packages (wheel and source distribution)
4. Creates standalone executables for Linux, Windows, and macOS
5. Builds and pushes Docker images to Docker Hub

## Prerequisites

### For Docker Image Publishing

To enable Docker image publishing, you need to set up Docker Hub secrets in your GitHub repository:

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Add the following repository secrets:
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub access token or password

### Getting a Docker Hub Access Token

1. Log in to [Docker Hub](https://hub.docker.com/)
2. Go to **Account Settings** → **Security**
3. Click **New Access Token**
4. Give it a descriptive name (e.g., "GitHub Actions")
5. Copy the token and save it as the `DOCKER_PASSWORD` secret

## Workflow Jobs

### Test Job
- **Trigger**: Every push and pull request
- **Environment**: Ubuntu Latest
- **Dependencies**: Python 3.12, pandoc, poppler-utils, LaTeX
- **Actions**: Runs `test_pdf_merger.py`

### Lint Job
- **Trigger**: Every push and pull request
- **Tools**: flake8, pylint
- **Actions**: 
  - Critical syntax errors will fail the build
  - Style warnings are reported but don't fail the build

### Build Package Job
- **Trigger**: After test and lint pass
- **Output**: 
  - Source distribution (.tar.gz)
  - Wheel distribution (.whl)
- **Artifacts**: Available for download from GitHub Actions for 30 days

### Build Executable Job
- **Trigger**: After test and lint pass
- **Platforms**: Ubuntu, Windows, macOS
- **Tool**: PyInstaller
- **Output**: Standalone executables for each platform
- **Artifacts**: Available for download from GitHub Actions for 30 days

### Build Docker Job
- **Trigger**: After test and lint pass
- **On PRs**: Builds image and saves as artifact (doesn't push)
- **On main branch**: Builds and pushes to Docker Hub with tags:
  - `latest` (for main branch)
  - Commit SHA
  - Branch name

## Using the Pipeline

### Automatic Triggers

The pipeline automatically runs when you:
- Push commits to the `main` branch
- Create or update a pull request targeting `main`

### Manual Trigger

You can manually trigger the pipeline:
1. Go to your repository on GitHub
2. Click **Actions** tab
3. Select **CI/CD Pipeline** workflow
4. Click **Run workflow** button
5. Select the branch and click **Run workflow**

## Downloading Artifacts

After a workflow run completes:
1. Go to the **Actions** tab
2. Click on the workflow run
3. Scroll down to the **Artifacts** section
4. Download the desired artifacts:
   - `python-package`: Python distributions
   - `pdf-merger-linux`: Linux executable
   - `pdf-merger-windows`: Windows executable  
   - `pdf-merger-macos`: macOS executable
   - `docker-image`: Docker image (PR only)

## Using the Docker Image

### Pull from Docker Hub

```bash
docker pull <your-docker-username>/pdf-merger:latest
```

### Run the Container

```bash
docker run --rm -v $(pwd)/mypdfs:/data <your-docker-username>/pdf-merger /data "*.pdf" "merged.pdf"
```

For more Docker usage examples, see [DOCKER.md](DOCKER.md).

## Local Development

### Build Locally

Use the provided build script:

```bash
./build.sh
```

This will:
- Clean previous builds
- Build Python package
- Build executable with PyInstaller

### Test Locally

```bash
# Install test dependencies (Ubuntu/Debian)
sudo apt-get install pandoc poppler-utils texlive-latex-base texlive-fonts-recommended texlive-latex-extra

# Install Python dependencies
pip install -r requirements.txt

# Run tests
python3 test_pdf_merger.py
```

### Lint Locally

```bash
# Install linters
pip install flake8 pylint

# Run flake8
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# Run pylint
pylint *.py
```

## Troubleshooting

### Docker Push Fails

**Problem**: Docker push fails with authentication error

**Solution**: 
- Verify `DOCKER_USERNAME` and `DOCKER_PASSWORD` secrets are set correctly
- Ensure the Docker Hub token has push permissions
- Check that the Docker Hub repository exists

### Tests Fail

**Problem**: Tests fail due to missing dependencies

**Solution**: 
- Ensure all system dependencies are installed (pandoc, poppler-utils, LaTeX)
- Check that Python dependencies from requirements.txt are installed

### Executable Build Fails

**Problem**: PyInstaller build fails

**Solution**:
- Ensure PyInstaller is installed: `pip install pyinstaller`
- Check that all Python modules can be imported
- Review the `pdf-merger.spec` file for missing dependencies

## Customization

### Changing Python Version

Edit `.github/workflows/ci-cd.yml`:

```yaml
env:
  PYTHON_VERSION: '3.11'  # Change to desired version
```

### Adding More Platforms

To build executables for additional platforms, edit the matrix in the `build-executable` job:

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest, ubuntu-20.04]
```

### Modifying Docker Image Name

Edit `.github/workflows/ci-cd.yml`:

```yaml
env:
  DOCKER_IMAGE_NAME: my-custom-name
```

## Best Practices

1. **Test Locally First**: Always test your changes locally before pushing
2. **Keep Secrets Secure**: Never commit secrets to the repository
3. **Review Artifacts**: Check the generated artifacts to ensure they work correctly
4. **Monitor Workflow Runs**: Check the Actions tab regularly for any failures
5. **Update Dependencies**: Keep Python packages and system dependencies up to date

## Support

For issues with the CI/CD pipeline, check:
- GitHub Actions logs for detailed error messages
- The workflow configuration in `.github/workflows/ci-cd.yml`
- This documentation for common troubleshooting steps

#!/bin/bash
# Build script for PDF Merger
# This script builds the Python package and executable

set -e

echo "==================================="
echo "Building PDF Merger"
echo "==================================="

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist *.egg-info

# Build Python package
echo ""
echo "Building Python package..."
python setup.py sdist bdist_wheel
echo "✓ Python package built successfully"

# Build executable with PyInstaller
echo ""
echo "Building executable with PyInstaller..."
pyinstaller pdf-merger.spec
echo "✓ Executable built successfully"

echo ""
echo "==================================="
echo "Build complete!"
echo "==================================="
echo "Package files:"
ls -lh dist/*.tar.gz dist/*.whl 2>/dev/null || true
echo ""
echo "Executable:"
ls -lh dist/pdf-merger 2>/dev/null || true
echo ""

# PDF Merger

[![CI/CD Pipeline](https://github.com/walliscode/pdf_merger/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/walliscode/pdf_merger/actions/workflows/ci-cd.yml)

A Python application for merging PDF files in subdirectories based on user-defined specifications.

## Features

- **GUI Interface**: User-friendly tkinter-based graphical interface
- **Command-line Interface**: Full-featured CLI for automation and scripting
- **Merge Configuration**: Configure specific filenames (without .pdf) that must be present for all subdirectories of a root directory
- **Flexible File Patterns**: Support for glob patterns to specify which files to merge
- **Customizable Output Names**: Template-based output naming with date/time placeholders
- **Preview Mode**: See what will be merged before performing the operation
- **Non-destructive**: Original files are never modified
- **Natural Sorting**: Files are sorted naturally (handles numbers correctly)
- **Smart Validation**: Only merges when all required components are present

## Installation

1. Clone the repository:
```bash
git clone https://github.com/walliscode/pdf_merger.git
cd pdf_merger
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Install tkinter if not available:
```bash
sudo apt-get install python3-tk  # Ubuntu/Debian
```

## Usage

### GUI Mode

Run the graphical interface:
```bash
python3 main.py
```

The GUI provides:
- Directory selection browser
- File pattern specification with help
- Output format customization
- Component mode with configuration dialog
- Preview functionality
- Progress tracking and logging

#### Merge Configuration Mode (GUI)

1. Select your main directory
2. Check "Use Merge Configuration Mode"
3. Click "Configure Merge Order"
4. Enter filenames (without .pdf) separated by commas (e.g., `intro, body, conclusion`)
5. Click "Save"
6. Use Preview or Merge PDFs - subdirectories without all required files will be skipped

### Command-line Mode

```bash
# Basic usage
python3 cli.py /path/to/main/directory

# Preview what will be merged
python3 cli.py /path/to/main/directory --preview

# Use specific file pattern
python3 cli.py /path/to/main/directory --pattern "report*.pdf"

# Custom output format
python3 cli.py /path/to/main/directory --output "merged_{directory}_{datetime}.pdf"

# Verbose output with statistics
python3 cli.py /path/to/main/directory --verbose --stats
```

#### Merge Configuration Mode (CLI)

```bash
# Configure merge order for a root directory (without .pdf extension)
python3 cli.py --set-merge-config /path/to/main/directory "intro,body,conclusion"

# List all saved configurations
python3 cli.py --list-configs

# Preview with merge configuration mode
python3 cli.py /path/to/main/directory --merge-config --preview --verbose

# Merge with merge configuration mode (configuration is mandatory)
python3 cli.py /path/to/main/directory --merge-config --verbose
```

Merge configuration mode will:
- Apply the same merge order to ALL subdirectories under the root directory
- Only merge subdirectories where ALL configured filenames are found
- Merge files in the order specified by configuration
- Skip subdirectories with missing files (with clear messages)
- Continue processing remaining subdirectories even if one fails
- Configuration must be set before using this mode

### File Patterns

Use glob patterns to specify which files to include:
- `*.pdf` - All PDF files (default)
- `report*.pdf` - Files starting with 'report'
- `*_final.pdf` - Files ending with '_final'
- `[0-9][0-9]*.pdf` - Files starting with two digits
- `chapter?.pdf` - Files like chapter1.pdf, chapter2.pdf

### Output Format Templates

Customize output filenames using placeholders:
- `{directory}` - Name of the subdirectory
- `{date}` - Current date (YYYY-MM-DD)
- `{time}` - Current time (HHMMSS)
- `{datetime}` - Current date and time (YYYY-MM-DD_HHMMSS)

Examples:
- `{directory}_{date}.pdf` → `Reports_2024-01-15.pdf`
- `merged_{directory}.pdf` → `merged_Reports.pdf`
- `{directory}_combined_{datetime}.pdf` → `Reports_combined_2024-01-15_143022.pdf`

### Merge Configuration Mode

Merge configuration mode allows you to define a specific merge order for a root directory. All subdirectories under that root will use the same merge order. This ensures consistent document organization across all subdirectories.

#### How It Works

1. **Configure Merge Order**: For a root directory, define the required filenames in merge order
   - Example: `intro, body, conclusion` (these are filenames without .pdf)
   - Files are matched case-insensitively as exact filenames (e.g., "intro" matches "intro.pdf" or "INTRO.pdf")
   - The configuration applies to ALL subdirectories under the root directory

2. **Mandatory Configuration**: The merge configuration must be set before using this mode
   - Without a configuration, the tool will refuse to run
   - This ensures you always know exactly what order files will be merged

3. **Validation**: Before merging, the tool checks if ALL configured filenames are present in each subdirectory
   - If any file is missing, a clear message is displayed
   - The subdirectory is skipped (no partial merge)

4. **Ordered Merging**: Files are merged in the order you specify
   - Files are merged in the exact order of the configuration

5. **Continuous Processing**: The tool continues to the next subdirectory even if previous ones had missing files

#### Example

```
Main Directory/           (Config: intro, body, conclusion - applies to all subdirectories)
├── Reports/
│   ├── intro.pdf       ✓
│   ├── body.pdf        ✓
│   └── conclusion.pdf  ✓
│   → Will merge in order
│
├── Invoices/
│   ├── intro.pdf       ✓
│   └── conclusion.pdf  ✓
│   → Skipped - missing "body"
│
└── Manuals/
    ├── intro.pdf       ✓
    ├── body.pdf        ✓
    └── conclusion.pdf  ✓
    → Will merge in order
```

## How It Works

The application supports two modes:

### Pattern Mode (Default)
1. **Directory Structure**: The application expects a main directory containing subdirectories
2. **File Discovery**: In each subdirectory, it finds files matching your specified pattern
3. **Sorting**: Files are sorted naturally (numbers are handled correctly)
4. **Merging**: PDFs are combined into a single file in the same subdirectory
5. **Naming**: Output file uses your specified template with date/time information

### Merge Configuration Mode
1. **Configuration**: Define required merge order for a root directory (e.g., "beginning, middle, end")
2. **Universal Application**: The same merge order applies to all subdirectories
3. **Mandatory Setup**: Configuration must be set before using this mode
4. **Validation**: Check that ALL configured files are present before merging each subdirectory
5. **Ordered Discovery**: Find files matching each configured filename
6. **Sequential Merging**: Merge files in the order specified by configuration
7. **Smart Skipping**: Skip subdirectories with missing files, continue with others

Example directory structure:
```
Main Directory/
├── Reports/
│   ├── 01_summary.pdf
│   ├── 02_details.pdf
│   ├── 03_conclusion.pdf
│   └── Reports_2024-01-15.pdf  ← Created by merger
├── Invoices/
│   ├── invoice_001.pdf
│   ├── invoice_002.pdf
│   └── Invoices_2024-01-15.pdf  ← Created by merger
└── Manuals/
    ├── chapter1.pdf
    ├── chapter2.pdf
    └── Manuals_2024-01-15.pdf  ← Created by merger
```

## Requirements

- Python 3.6+
- PyPDF2
- tkinter (for GUI mode)

## CI/CD Pipeline

This project includes a comprehensive CI/CD pipeline using GitHub Actions that:

### Testing & Quality
- **Automated Tests**: Runs all tests on every push and pull request
- **Code Linting**: Checks code quality with flake8 and pylint
- **Multi-Platform Support**: Tests run on Ubuntu with required dependencies (pandoc, poppler-utils)

### Distribution

#### Python Package
- Builds a distributable Python package (wheel and source)
- Available as GitHub Actions artifacts
- Ready for PyPI publication

#### Executables
- **Cross-Platform Builds**: Creates standalone executables for:
  - Linux (Ubuntu)
  - Windows
  - macOS
- **No Dependencies Required**: Users can run the application without Python installed
- **Download**: Executables available as artifacts from GitHub Actions runs

#### Docker Image
- **Automated Build**: Docker images built and pushed on every main branch commit
- **Multi-Tag Support**: Images tagged with branch name, commit SHA, and `latest`
- **Lightweight**: Based on Python 3.12 slim image
- **Secure**: Runs as non-root user

### Using the Docker Image

For detailed Docker usage instructions, see [DOCKER.md](DOCKER.md).

Quick example:
```bash
docker run --rm -v $(pwd)/mypdfs:/data <dockerhub-username>/pdf-merger /data "*.pdf" "merged.pdf"
```

### Workflow Triggers
- Push to `main` branch
- Pull requests to `main` branch
- Manual workflow dispatch

## Documentation

- **[CICD_SETUP.md](CICD_SETUP.md)** - Comprehensive CI/CD pipeline setup guide
- **[DOCKER.md](DOCKER.md)** - Docker usage and examples
- **[RELEASES.md](RELEASES.md)** - Guide to using different distribution formats
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contributing guidelines for developers

## License

GNU General Public License v3.0 - see LICENSE file for details.

# PDF Merger

A Python application for merging PDF files in subdirectories based on user-defined specifications.

## Features

- **GUI Interface**: User-friendly tkinter-based graphical interface
- **Command-line Interface**: Full-featured CLI for automation and scripting
- **Flexible File Patterns**: Support for glob patterns to specify which files to merge
- **Customizable Output Names**: Template-based output naming with date/time placeholders
- **Preview Mode**: See what will be merged before performing the operation
- **Non-destructive**: Original files are never modified
- **Natural Sorting**: Files are sorted naturally (handles numbers correctly)

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
- Preview functionality
- Progress tracking and logging

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

## How It Works

1. **Directory Structure**: The application expects a main directory containing subdirectories
2. **File Discovery**: In each subdirectory, it finds files matching your specified pattern
3. **Sorting**: Files are sorted naturally (numbers are handled correctly)
4. **Merging**: PDFs are combined into a single file in the same subdirectory
5. **Naming**: Output file uses your specified template with date/time information

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

## License

GNU General Public License v3.0 - see LICENSE file for details.

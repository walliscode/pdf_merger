# PDF Merger

A Python application for merging PDF files in subdirectories based on user-defined specifications.

## Features

- **GUI Interface**: User-friendly tkinter-based graphical interface
- **Command-line Interface**: Full-featured CLI for automation and scripting
- **Filename-Based Merging**: Configure specific filenames (without .pdf) that must be present for each directory
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

#### Component Mode (GUI)

1. Select your main directory
2. Check "Use Component Mode"
3. Click "Configure Components"
4. For each subdirectory, enter filenames (without .pdf) separated by commas (e.g., `intro, body, conclusion`)
5. Click "Save"
6. Use Preview or Merge PDFs - directories without all required files will be skipped

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

#### Component Mode (CLI)

```bash
# Configure filenames for directories (without .pdf extension)
python3 cli.py --set-components "Reports:intro,body,conclusion"
python3 cli.py --set-components "Invoices:invoice_intro,invoice_body,invoice_summary"

# List all saved configurations
python3 cli.py --list-configs

# Preview with component mode
python3 cli.py /path/to/main/directory --component-mode --preview --verbose

# Merge with component mode
python3 cli.py /path/to/main/directory --component-mode --verbose
```

Component mode will:
- Only merge directories where ALL configured filenames are found
- Merge files in the order specified by configuration
- Skip directories with missing files (with clear messages)
- Continue processing remaining directories even if one fails

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

### Component Mode

Component mode allows you to define specific filenames (without .pdf extension) that must be present in each directory before merging. This ensures complete document sets are merged together.

#### How It Works

1. **Configure Filenames**: For each top-level directory (by name), define required filenames
   - Example: `intro, body, conclusion` (these are filenames without .pdf)
   - Files are matched case-insensitively as exact filenames (e.g., "intro" matches "intro.pdf" or "INTRO.pdf")

2. **Validation**: Before merging, the tool checks if ALL configured filenames are present
   - If any file is missing, a clear message is displayed
   - The directory is skipped (no partial merge)

3. **Ordered Merging**: Files are merged in the order you specify
   - Files are merged in the exact order of the configuration

4. **Continuous Processing**: The tool continues to the next directory even if previous ones had missing files

#### Example

```
Main Directory/
├── Reports/              (Config: intro, body, conclusion)
│   ├── intro.pdf       ✓
│   ├── body.pdf        ✓
│   └── conclusion.pdf  ✓
│   → Will merge in order
│
├── Invoices/             (Config: intro, body, conclusion)
│   ├── intro.pdf       ✓
│   └── conclusion.pdf  ✓
│   → Skipped - missing "body"
│
└── Manuals/              (Config: intro, body, conclusion)
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

### Component Mode
1. **Configuration**: Define required components for each directory (e.g., "beginning, middle, end")
2. **Validation**: Check that ALL configured components are present before merging
3. **Ordered Discovery**: Find files matching each component pattern
4. **Sequential Merging**: Merge files in the order specified by components
5. **Smart Skipping**: Skip directories with missing components, continue with others

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

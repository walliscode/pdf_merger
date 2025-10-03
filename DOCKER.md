# Docker Usage Guide

## Building the Docker Image

```bash
docker build -t pdf-merger .
```

## Running the Container

### Basic Usage

Show help:
```bash
docker run --rm pdf-merger
```

### Merge PDFs in a Directory

Mount your directory with PDF files:
```bash
docker run --rm -v /path/to/your/pdfs:/data pdf-merger /data "*.pdf" "{directory}_merged.pdf"
```

### Preview Mode

Preview what would be merged without actually merging:
```bash
docker run --rm -v /path/to/your/pdfs:/data pdf-merger --preview /data "*.pdf" "{directory}_merged.pdf"
```

### Using Merge Configuration Mode

Set merge configuration:
```bash
docker run --rm -v /path/to/your/pdfs:/data pdf-merger \
  --set-merge-config /data "intro,body,conclusion" \
  /data "*.pdf" "{directory}_merged.pdf"
```

Merge using configuration:
```bash
docker run --rm -v /path/to/your/pdfs:/data pdf-merger \
  --merge-config /data "*.pdf" "{directory}_merged.pdf"
```

### Verbose Mode

Get detailed output:
```bash
docker run --rm -v /path/to/your/pdfs:/data pdf-merger \
  --verbose /data "*.pdf" "{directory}_merged.pdf"
```

## Environment Variables

- `DISPLAY`: Set for GUI support (default: `:0`)

## Volume Mounts

The container expects a volume mount at `/data` where your PDF files are located.

## Examples

### Example 1: Simple Merge

```bash
# Directory structure:
# mypdfs/
# ├── project1/
# │   ├── file1.pdf
# │   └── file2.pdf
# └── project2/
#     ├── file3.pdf
#     └── file4.pdf

docker run --rm -v $(pwd)/mypdfs:/data pdf-merger /data "*.pdf" "merged.pdf"
```

### Example 2: Merge with Date Stamp

```bash
docker run --rm -v $(pwd)/mypdfs:/data pdf-merger /data "*.pdf" "{directory}_{date}.pdf"
```

### Example 3: Specific File Pattern

```bash
docker run --rm -v $(pwd)/mypdfs:/data pdf-merger /data "report*.pdf" "report_combined.pdf"
```

## Notes

- The container runs as a non-root user (`pdfuser`) for security
- Merged PDFs are created in the same directories as the source files
- Original files are never modified
- Configuration files are stored in the container's home directory

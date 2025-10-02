# Use Python slim image for smaller size
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies (for GUI support if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY *.py .
COPY README.md .
COPY LICENSE .

# Create a non-root user for security
RUN useradd -m -u 1000 pdfuser && \
    chown -R pdfuser:pdfuser /app

# Switch to non-root user
USER pdfuser

# Set environment variable to disable GUI warnings
ENV DISPLAY=:0

# Create volume mount point for PDF files
VOLUME ["/data"]

# Set default working directory for PDF operations
WORKDIR /data

# Default command runs CLI help
ENTRYPOINT ["python3", "/app/cli.py"]
CMD ["--help"]

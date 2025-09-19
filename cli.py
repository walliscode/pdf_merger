#!/usr/bin/env python3
"""
Command-line version of the PDF Merger application

Provides a CLI interface for merging PDF files in subdirectories.
"""

import argparse
import os
import sys
from pdf_merger import PDFMerger

def main():
    """Main command-line interface"""
    parser = argparse.ArgumentParser(
        description="Merge PDF files in subdirectories based on specifications",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/main/directory
  %(prog)s /path/to/main/directory --pattern "report*.pdf"
  %(prog)s /path/to/main/directory --output "{directory}_merged_{date}.pdf"
  %(prog)s /path/to/main/directory --preview
  
File Patterns:
  *.pdf          - All PDF files (default)
  report*.pdf    - Files starting with 'report'
  *_final.pdf    - Files ending with '_final'
  [0-9][0-9]*.pdf - Files starting with two digits
  
Output Formats:
  {directory}    - Name of the subdirectory
  {date}         - Current date (YYYY-MM-DD)
  {time}         - Current time (HHMMSS)
  {datetime}     - Current date and time (YYYY-MM-DD_HHMMSS)
        """
    )
    
    parser.add_argument(
        "directory",
        help="Main directory containing subdirectories with PDF files"
    )
    
    parser.add_argument(
        "--pattern", "-p",
        default="*.pdf",
        help="File pattern to match (default: *.pdf)"
    )
    
    parser.add_argument(
        "--output", "-o",
        default="{directory}_{date}.pdf",
        help="Output filename format (default: {directory}_{date}.pdf)"
    )
    
    parser.add_argument(
        "--preview", "-n",
        action="store_true",
        help="Preview what will be merged without actually merging"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    parser.add_argument(
        "--stats", "-s",
        action="store_true",
        help="Show directory statistics"
    )
    
    args = parser.parse_args()
    
    # Validate directory
    if not os.path.exists(args.directory):
        print(f"Error: Directory '{args.directory}' does not exist.", file=sys.stderr)
        sys.exit(1)
    
    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' is not a directory.", file=sys.stderr)
        sys.exit(1)
    
    # Initialize PDF merger
    merger = PDFMerger()
    
    try:
        # Validate directory
        valid, message = merger.validate_directory(args.directory)
        if not valid:
            print(f"Error: {message}", file=sys.stderr)
            sys.exit(1)
        
        if args.verbose:
            print(f"Processing directory: {args.directory}")
            print(f"File pattern: {args.pattern}")
            print(f"Output format: {args.output}")
        
        # Show statistics if requested
        if args.stats:
            stats = merger.get_directory_stats(args.directory, args.pattern)
            print("\nDirectory Statistics:")
            print(f"  Total subdirectories: {stats['total_subdirs']}")
            print(f"  Subdirectories with matching files: {stats['subdirs_with_pdfs']}")
            print(f"  Total matching files: {stats['total_pdf_files']}")
            
            if args.verbose and stats['subdirs_info']:
                print("\nSubdirectory Details:")
                for subdir_info in stats['subdirs_info']:
                    if subdir_info['file_count'] > 0:
                        print(f"  {subdir_info['name']}: {subdir_info['file_count']} files")
                        if args.verbose:
                            for file in subdir_info['files']:
                                print(f"    - {file}")
            print()
        
        # Preview or merge
        if args.preview:
            print("Preview Mode - Showing what would be merged:")
            preview_data = merger.preview_merge(args.directory, args.pattern, args.output)
            
            if not preview_data:
                print("No subdirectories with matching PDF files found.")
                sys.exit(0)
            
            print(f"\nFound {len(preview_data)} subdirectories to process:")
            total_files = 0
            for subdir, files, output_file in preview_data:
                subdir_name = os.path.basename(subdir)
                output_name = os.path.basename(output_file)
                print(f"  {subdir_name}: {len(files)} files -> {output_name}")
                total_files += len(files)
                
                if args.verbose:
                    for file in files:
                        print(f"    - {os.path.basename(file)}")
            
            print(f"\nTotal files to merge: {total_files}")
            
        else:
            # Actual merge
            print("Merging PDFs...")
            
            def progress_callback(message):
                if args.verbose:
                    print(f"  {message}")
            
            results = merger.merge_pdfs(
                args.directory,
                args.pattern,
                args.output,
                progress_callback=progress_callback if args.verbose else None
            )
            
            if results:
                print(f"\nSuccessfully merged {len(results)} directories:")
                for result in results:
                    print(f"  Created: {result}")
            else:
                print("No PDFs were merged.")
                sys.exit(1)
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
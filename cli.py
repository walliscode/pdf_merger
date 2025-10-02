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
  
  # Merge configuration mode examples
  %(prog)s --set-merge-config /path/to/main/directory beginning,middle,end
  %(prog)s --list-configs
  %(prog)s /path/to/main/directory --merge-config --preview
  %(prog)s /path/to/main/directory --merge-config
  
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

Merge Configuration Mode:
  Configure specific file order for a root directory.
  All subdirectories follow the same merge order.
  Only merges when ALL configured files are present.
  Merges files in the order specified by configuration.
        """
    )
    
    parser.add_argument(
        "directory",
        nargs='?',
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
    
    parser.add_argument(
        "--merge-config", "-m",
        action="store_true",
        help="Use merge configuration mode (requires configuration to be set)"
    )
    
    parser.add_argument(
        "--set-merge-config",
        nargs=2,
        metavar=("ROOT_DIR", "FILE1,FILE2,..."),
        action="append",
        help="Set merge configuration for a root directory (e.g., /path/to/dir \"beginning,middle,end\")"
    )
    
    parser.add_argument(
        "--list-configs",
        action="store_true",
        help="List all saved merge configurations"
    )
    
    args = parser.parse_args()
    
    # Validate directory (if provided)
    if args.directory:
        if not os.path.exists(args.directory):
            print(f"Error: Directory '{args.directory}' does not exist.", file=sys.stderr)
            sys.exit(1)
        
        if not os.path.isdir(args.directory):
            print(f"Error: '{args.directory}' is not a directory.", file=sys.stderr)
            sys.exit(1)
    
    # Initialize PDF merger
    merger = PDFMerger()
    
    # Handle merge configuration commands
    if args.set_merge_config:
        for root_dir, merge_order_str in args.set_merge_config:
            merge_order = [f.strip() for f in merge_order_str.split(',') if f.strip()]
            if merge_order:
                merger.set_merge_config(root_dir, merge_order)
                print(f"Set merge configuration for '{root_dir}': {merge_order}")
            else:
                print(f"Warning: No valid files specified for '{root_dir}'", file=sys.stderr)
    
    if args.list_configs:
        configs = merger.get_all_configs()
        if configs:
            print("Merge Configurations:")
            for root_dir, merge_order in configs.items():
                print(f"  {root_dir}: {', '.join(merge_order)}")
        else:
            print("No merge configurations found.")
        
        # If only listing configs, exit
        if not args.directory:
            sys.exit(0)
    
    try:
        # Validate directory (only if provided)
        if not args.directory:
            print("Error: Directory argument is required for merge/preview operations.", file=sys.stderr)
            sys.exit(1)
            
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
            mode_text = "merge configuration mode" if args.merge_config else "pattern mode"
            print(f"Preview Mode - Showing what would be merged ({mode_text}):")
            preview_data = merger.preview_merge(args.directory, args.pattern, args.output, 
                                               use_merge_config=args.merge_config)
            
            if not preview_data:
                print("No subdirectories with matching PDF files found.")
                sys.exit(0)
            
            print(f"\nFound {len(preview_data)} subdirectories:")
            total_files = 0
            ready_count = 0
            missing_count = 0
            
            for subdir, files, output_file, status_info in preview_data:
                subdir_name = os.path.basename(subdir)
                output_name = os.path.basename(output_file)
                
                if status_info['status'] == 'missing':
                    missing_count += 1
                    print(f"  {subdir_name}: MISSING FILES - {', '.join(status_info['missing_files'])}")
                elif status_info['status'] == 'ready':
                    ready_count += 1
                    if status_info['mode'] == 'merge_config':
                        print(f"  {subdir_name}: READY ({len(files)} files in order: {', '.join(status_info['merge_order'])}) -> {output_name}")
                        if args.verbose:
                            for filename in status_info['merge_order']:
                                merge_files = status_info['merge_files'].get(filename, [])
                                for f in merge_files:
                                    print(f"    [{filename}] {os.path.basename(f)}")
                    else:
                        print(f"  {subdir_name}: {len(files)} files -> {output_name}")
                        if args.verbose:
                            for file in files:
                                print(f"    - {os.path.basename(file)}")
                    total_files += len(files)
            
            print(f"\nTotal files to merge: {total_files}")
            if args.merge_config:
                print(f"Ready to merge: {ready_count}, Missing files: {missing_count}")
            
        else:
            # Actual merge
            mode_text = "merge configuration mode" if args.merge_config else "pattern mode"
            print(f"Merging PDFs ({mode_text})...")
            
            def progress_callback(message):
                if args.verbose:
                    print(f"  {message}")
            
            results = merger.merge_pdfs(
                args.directory,
                args.pattern,
                args.output,
                progress_callback=progress_callback if args.verbose else None,
                use_merge_config=args.merge_config
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
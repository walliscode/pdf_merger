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
  
  # Component mode examples
  %(prog)s --set-components "Reports:beginning,middle,end"
  %(prog)s --list-configs
  %(prog)s /path/to/main/directory --component-mode --preview
  %(prog)s /path/to/main/directory --component-mode
  
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

Component Mode:
  Configure specific component patterns for each directory.
  Only merges when ALL components are present.
  Merges files in the order specified by components.
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
        "--component-mode", "-c",
        action="store_true",
        help="Use component-based merging with saved configurations"
    )
    
    parser.add_argument(
        "--set-components",
        metavar="DIR:COMP1,COMP2,...",
        action="append",
        help="Set component configuration for a directory (e.g., Reports:beginning,middle,end)"
    )
    
    parser.add_argument(
        "--list-configs",
        action="store_true",
        help="List all saved component configurations"
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
    
    # Handle component configuration commands
    if args.set_components:
        for config_str in args.set_components:
            try:
                dir_name, components_str = config_str.split(':', 1)
                components = [c.strip() for c in components_str.split(',') if c.strip()]
                if components:
                    merger.set_directory_config(dir_name, components)
                    print(f"Set components for '{dir_name}': {components}")
                else:
                    print(f"Warning: No valid components specified for '{dir_name}'", file=sys.stderr)
            except ValueError:
                print(f"Error: Invalid format '{config_str}'. Use DIR:COMP1,COMP2,...", file=sys.stderr)
                sys.exit(1)
    
    if args.list_configs:
        configs = merger.get_all_configs()
        if configs:
            print("Component Configurations:")
            for dir_name, components in configs.items():
                print(f"  {dir_name}: {', '.join(components)}")
        else:
            print("No component configurations found.")
        
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
            mode_text = "component mode" if args.component_mode else "pattern mode"
            print(f"Preview Mode - Showing what would be merged ({mode_text}):")
            preview_data = merger.preview_merge(args.directory, args.pattern, args.output, 
                                               use_component_mode=args.component_mode)
            
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
                    print(f"  {subdir_name}: MISSING COMPONENTS - {', '.join(status_info['missing_components'])}")
                elif status_info['status'] == 'ready':
                    ready_count += 1
                    if status_info['mode'] == 'component':
                        print(f"  {subdir_name}: READY ({len(files)} files in order: {', '.join(status_info['components'])}) -> {output_name}")
                        if args.verbose:
                            for component in status_info['components']:
                                comp_files = status_info['component_files'].get(component, [])
                                for f in comp_files:
                                    print(f"    [{component}] {os.path.basename(f)}")
                    else:
                        print(f"  {subdir_name}: {len(files)} files -> {output_name}")
                        if args.verbose:
                            for file in files:
                                print(f"    - {os.path.basename(file)}")
                    total_files += len(files)
            
            print(f"\nTotal files to merge: {total_files}")
            if args.component_mode:
                print(f"Ready to merge: {ready_count}, Missing components: {missing_count}")
            
        else:
            # Actual merge
            mode_text = "component mode" if args.component_mode else "pattern mode"
            print(f"Merging PDFs ({mode_text})...")
            
            def progress_callback(message):
                if args.verbose:
                    print(f"  {message}")
            
            results = merger.merge_pdfs(
                args.directory,
                args.pattern,
                args.output,
                progress_callback=progress_callback if args.verbose else None,
                use_component_mode=args.component_mode
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
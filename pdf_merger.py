"""
PDF Merger Core Functionality

Handles the actual PDF merging operations.
"""

import os
import glob
from datetime import datetime
import re
import json
from PyPDF2 import PdfWriter, PdfReader

class PDFMerger:
    def __init__(self):
        self.config_file = os.path.join(os.path.expanduser("~"), ".pdf_merger_config.json")
        self.configs = self.load_configs()
    
    def load_configs(self):
        """Load filename configurations from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}
    
    def save_configs(self):
        """Save filename configurations to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.configs, f, indent=2)
        except Exception as e:
            raise Exception(f"Error saving configurations: {e}")
    
    def set_directory_config(self, directory_name, components):
        """Set filename configuration for a directory
        
        Args:
            directory_name: Name of the directory (not full path)
            components: List of filenames (without .pdf) in merge order, e.g. ["intro", "body", "conclusion"]
        """
        self.configs[directory_name] = components
        self.save_configs()
    
    def get_directory_config(self, directory_name):
        """Get filename configuration for a directory
        
        Args:
            directory_name: Name of the directory
            
        Returns:
            List of filenames (without .pdf) or None if not configured
        """
        return self.configs.get(directory_name)
    
    def delete_directory_config(self, directory_name):
        """Delete filename configuration for a directory"""
        if directory_name in self.configs:
            del self.configs[directory_name]
            self.save_configs()
    
    def get_all_configs(self):
        """Get all filename configurations"""
        return self.configs.copy()
    
    def get_subdirectories(self, main_directory):
        """Get all subdirectories in the main directory"""
        subdirs = []
        try:
            for item in os.listdir(main_directory):
                item_path = os.path.join(main_directory, item)
                if os.path.isdir(item_path):
                    subdirs.append(item_path)
        except OSError as e:
            raise Exception(f"Error reading directory {main_directory}: {e}")
        return subdirs
    
    def get_matching_files(self, directory, pattern):
        """Get files matching the pattern in the directory"""
        try:
            pattern_path = os.path.join(directory, pattern)
            files = glob.glob(pattern_path)
            # Sort files naturally (handle numbers correctly)
            files.sort(key=self.natural_sort_key)
            return [f for f in files if os.path.isfile(f)]
        except Exception as e:
            raise Exception(f"Error finding files in {directory}: {e}")
    
    def find_component_files(self, directory, components):
        """Find files matching the specified filenames (without .pdf extension)
        
        Args:
            directory: Directory to search in
            components: List of filenames without .pdf extension (e.g., ["intro", "body", "conclusion"])
            
        Returns:
            Tuple of (all_found, component_files_dict, missing_components)
            - all_found: Boolean indicating if all files were found
            - component_files_dict: Dict mapping filename to matching file path
            - missing_components: List of filenames that weren't found
        """
        component_files = {}
        missing_components = []
        
        # Get all files in directory (not just .pdf to catch .PDF, .Pdf, etc.)
        try:
            all_files = [os.path.join(directory, f) for f in os.listdir(directory) 
                        if os.path.isfile(os.path.join(directory, f)) and f.lower().endswith('.pdf')]
        except OSError:
            all_files = []
        
        for component in components:
            component_lower = component.lower()
            
            # Look for exact match of filename (without .pdf extension, case-insensitive)
            matching_file = None
            for file_path in all_files:
                basename = os.path.basename(file_path)
                # Remove .pdf extension (case-insensitive)
                if basename.lower().endswith('.pdf'):
                    filename_without_ext = basename[:-4]
                    if filename_without_ext.lower() == component_lower:
                        matching_file = file_path
                        break
            
            if matching_file:
                component_files[component] = [matching_file]
            else:
                missing_components.append(component)
        
        all_found = len(missing_components) == 0
        return all_found, component_files, missing_components
    
    def get_ordered_component_files(self, component_files_dict, components):
        """Get files in the order specified by components
        
        Args:
            component_files_dict: Dict mapping component to list of files
            components: List of components in desired order
            
        Returns:
            List of files in the specified order
        """
        ordered_files = []
        for component in components:
            if component in component_files_dict:
                ordered_files.extend(component_files_dict[component])
        return ordered_files
    
    def natural_sort_key(self, text):
        """Natural sorting key that handles numbers correctly"""
        def convert(text):
            return int(text) if text.isdigit() else text.lower()
        return [convert(c) for c in re.split('([0-9]+)', text)]
    
    def format_output_filename(self, template, directory_name):
        """Format the output filename using the template"""
        now = datetime.now()
        replacements = {
            'directory': os.path.basename(directory_name),
            'date': now.strftime('%Y-%m-%d'),
            'time': now.strftime('%H%M%S'),
            'datetime': now.strftime('%Y-%m-%d_%H%M%S')
        }
        
        filename = template
        for key, value in replacements.items():
            filename = filename.replace(f'{{{key}}}', value)
        
        # Ensure .pdf extension
        if not filename.lower().endswith('.pdf'):
            filename += '.pdf'
            
        return filename
    
    def preview_merge(self, main_directory, file_pattern, output_format, use_component_mode=False):
        """Preview what will be merged without actually merging
        
        Args:
            main_directory: Main directory containing subdirectories
            file_pattern: File pattern to match (only used when not in component mode)
            output_format: Output filename template
            use_component_mode: If True, use component-based merging with configs
            
        Returns:
            List of tuples (subdir, matching_files, output_path, status_info)
        """
        preview_data = []
        
        if not os.path.exists(main_directory):
            raise Exception(f"Directory does not exist: {main_directory}")
        
        subdirs = self.get_subdirectories(main_directory)
        
        for subdir in subdirs:
            subdir_name = os.path.basename(subdir)
            status_info = {}
            
            if use_component_mode:
                components = self.get_directory_config(subdir_name)
                
                if components:
                    status_info['mode'] = 'component'
                    status_info['components'] = components
                    all_found, component_files, missing = self.find_component_files(subdir, components)
                    
                    if all_found:
                        matching_files = self.get_ordered_component_files(component_files, components)
                        status_info['status'] = 'ready'
                        status_info['component_files'] = component_files
                    else:
                        matching_files = []
                        status_info['status'] = 'missing'
                        status_info['missing_components'] = missing
                else:
                    status_info['mode'] = 'pattern'
                    matching_files = self.get_matching_files(subdir, file_pattern)
                    status_info['status'] = 'ready' if matching_files else 'no_files'
            else:
                status_info['mode'] = 'pattern'
                matching_files = self.get_matching_files(subdir, file_pattern)
                status_info['status'] = 'ready' if matching_files else 'no_files'
            
            if matching_files or (use_component_mode and status_info.get('status') == 'missing'):
                output_filename = self.format_output_filename(output_format, subdir)
                output_path = os.path.join(subdir, output_filename)
                preview_data.append((subdir, matching_files, output_path, status_info))
        
        return preview_data
    
    def merge_pdf_files(self, file_list, output_path):
        """Merge a list of PDF files into a single PDF"""
        if not file_list:
            raise Exception("No files to merge")
        
        writer = PdfWriter()
        
        try:
            for pdf_file in file_list:
                try:
                    reader = PdfReader(pdf_file)
                    for page in reader.pages:
                        writer.add_page(page)
                except Exception as e:
                    raise Exception(f"Error reading {pdf_file}: {e}")
            
            # Write the merged PDF
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
                
        except Exception as e:
            raise Exception(f"Error writing merged PDF to {output_path}: {e}")
    
    def merge_pdfs(self, main_directory, file_pattern, output_format, progress_callback=None, use_component_mode=False):
        """Merge PDFs in all subdirectories
        
        Args:
            main_directory: Main directory containing subdirectories
            file_pattern: File pattern to match (only used when not in component mode)
            output_format: Output filename template
            progress_callback: Optional callback for progress messages
            use_component_mode: If True, use component-based merging with configs
        """
        if not os.path.exists(main_directory):
            raise Exception(f"Directory does not exist: {main_directory}")
        
        results = []
        subdirs = self.get_subdirectories(main_directory)
        
        if progress_callback:
            progress_callback(f"Found {len(subdirs)} subdirectories to process")
        
        for i, subdir in enumerate(subdirs, 1):
            subdir_name = os.path.basename(subdir)
            
            if progress_callback:
                progress_callback(f"Processing {i}/{len(subdirs)}: {subdir_name}")
            
            # Check if component mode is enabled
            if use_component_mode:
                components = self.get_directory_config(subdir_name)
                
                if components:
                    # Component-based merging
                    if progress_callback:
                        progress_callback(f"  Using component configuration: {components}")
                    
                    all_found, component_files, missing = self.find_component_files(subdir, components)
                    
                    if not all_found:
                        if progress_callback:
                            progress_callback(f"  Missing components: {', '.join(missing)}")
                            progress_callback(f"  Skipping {subdir_name} - not all components present")
                        continue
                    
                    if progress_callback:
                        progress_callback(f"  All components found!")
                        for component in components:
                            files = component_files[component]
                            progress_callback(f"    {component}: {len(files)} file(s)")
                    
                    # Get files in order specified by components
                    matching_files = self.get_ordered_component_files(component_files, components)
                else:
                    # No config for this directory, use pattern-based matching
                    if progress_callback:
                        progress_callback(f"  No component configuration for {subdir_name}, using pattern")
                    matching_files = self.get_matching_files(subdir, file_pattern)
            else:
                # Pattern-based merging (original behavior)
                matching_files = self.get_matching_files(subdir, file_pattern)
            
            if not matching_files:
                if progress_callback:
                    progress_callback(f"  No matching files found in {subdir_name}")
                continue
            
            if progress_callback and not use_component_mode:
                progress_callback(f"  Found {len(matching_files)} matching files")
            
            try:
                output_filename = self.format_output_filename(output_format, subdir)
                output_path = os.path.join(subdir, output_filename)
                
                # Check if output file already exists
                if os.path.exists(output_path):
                    if progress_callback:
                        progress_callback(f"  Warning: {output_filename} already exists, will overwrite")
                
                self.merge_pdf_files(matching_files, output_path)
                results.append(output_path)
                
                if progress_callback:
                    progress_callback(f"  Successfully created: {output_filename}")
                    
            except Exception as e:
                if progress_callback:
                    progress_callback(f"  Error processing {subdir_name}: {e}")
                # Continue with other directories instead of stopping
                continue
        
        return results
    
    def validate_directory(self, directory):
        """Validate that the directory exists and is readable"""
        if not directory:
            return False, "No directory specified"
        
        if not os.path.exists(directory):
            return False, f"Directory does not exist: {directory}"
        
        if not os.path.isdir(directory):
            return False, f"Path is not a directory: {directory}"
        
        try:
            os.listdir(directory)
        except PermissionError:
            return False, f"Permission denied accessing directory: {directory}"
        except OSError as e:
            return False, f"Error accessing directory: {e}"
        
        return True, "Directory is valid"
    
    def get_directory_stats(self, main_directory, file_pattern):
        """Get statistics about directories and files"""
        stats = {
            'total_subdirs': 0,
            'subdirs_with_pdfs': 0,
            'total_pdf_files': 0,
            'subdirs_info': []
        }
        
        try:
            subdirs = self.get_subdirectories(main_directory)
            stats['total_subdirs'] = len(subdirs)
            
            for subdir in subdirs:
                matching_files = self.get_matching_files(subdir, file_pattern)
                file_count = len(matching_files)
                
                if file_count > 0:
                    stats['subdirs_with_pdfs'] += 1
                    stats['total_pdf_files'] += file_count
                
                stats['subdirs_info'].append({
                    'name': os.path.basename(subdir),
                    'path': subdir,
                    'file_count': file_count,
                    'files': [os.path.basename(f) for f in matching_files]
                })
                
        except Exception as e:
            raise Exception(f"Error getting directory statistics: {e}")
        
        return stats
"""
PDF Merger Core Functionality

Handles the actual PDF merging operations.
"""

import os
import glob
from datetime import datetime
import re
from PyPDF2 import PdfWriter, PdfReader

class PDFMerger:
    def __init__(self):
        pass
    
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
    
    def preview_merge(self, main_directory, file_pattern, output_format):
        """Preview what will be merged without actually merging"""
        preview_data = []
        
        if not os.path.exists(main_directory):
            raise Exception(f"Directory does not exist: {main_directory}")
        
        subdirs = self.get_subdirectories(main_directory)
        
        for subdir in subdirs:
            matching_files = self.get_matching_files(subdir, file_pattern)
            
            if matching_files:
                output_filename = self.format_output_filename(output_format, subdir)
                output_path = os.path.join(subdir, output_filename)
                preview_data.append((subdir, matching_files, output_path))
        
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
    
    def merge_pdfs(self, main_directory, file_pattern, output_format, progress_callback=None):
        """Merge PDFs in all subdirectories"""
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
            
            matching_files = self.get_matching_files(subdir, file_pattern)
            
            if not matching_files:
                if progress_callback:
                    progress_callback(f"  No matching files found in {subdir_name}")
                continue
            
            if progress_callback:
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
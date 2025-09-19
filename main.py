"""
PDF Merger Application

A tkinter GUI application for merging PDF files in subdirectories based on user-defined specifications.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
from datetime import datetime
import logging
from pdf_merger import PDFMerger

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PDFMergerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        self.root.geometry("800x600")
        
        # Initialize variables
        self.selected_directory = tk.StringVar()
        self.file_pattern = tk.StringVar(value="*.pdf")
        self.output_format = tk.StringVar(value="{directory}_{date}.pdf")
        
        # Initialize PDF merger
        self.pdf_merger = PDFMerger()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        # Directory selection
        ttk.Label(main_frame, text="Main Directory:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        dir_frame = ttk.Frame(main_frame)
        dir_frame.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        dir_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(dir_frame, textvariable=self.selected_directory, state="readonly").grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(dir_frame, text="Browse", command=self.browse_directory).grid(row=0, column=1)
        
        # File pattern specification
        ttk.Label(main_frame, text="File Pattern:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        pattern_frame = ttk.Frame(main_frame)
        pattern_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        pattern_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(pattern_frame, textvariable=self.file_pattern).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(pattern_frame, text="?", width=3, command=self.show_pattern_help).grid(row=0, column=1)
        
        # Output format specification
        ttk.Label(main_frame, text="Output Format:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        output_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(output_frame, textvariable=self.output_format).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(output_frame, text="?", width=3, command=self.show_output_help).grid(row=0, column=1)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(button_frame, text="Preview", command=self.preview_merge).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Merge PDFs", command=self.merge_pdfs).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Clear Log", command=self.clear_log).pack(side=tk.LEFT)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Log area
        ttk.Label(main_frame, text="Log:").grid(row=5, column=0, sticky=(tk.W, tk.N), pady=(10, 0))
        self.log_text = scrolledtext.ScrolledText(main_frame, height=15, width=70)
        self.log_text.grid(row=5, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
    def browse_directory(self):
        """Open directory selection dialog"""
        directory = filedialog.askdirectory(title="Select Main Directory")
        if directory:
            self.selected_directory.set(directory)
            self.log(f"Selected directory: {directory}")
            
    def show_pattern_help(self):
        """Show help for file pattern"""
        help_text = """File Pattern Help:

Use glob patterns to specify which files to include:
• *.pdf - All PDF files
• report*.pdf - PDFs starting with 'report'
• *_final.pdf - PDFs ending with '_final'
• page[0-9].pdf - PDFs like page1.pdf, page2.pdf, etc.

Examples:
• *.pdf (default) - Include all PDF files
• chapter*.pdf - Include files like chapter1.pdf, chapter2.pdf
• [0-9][0-9]_*.pdf - Include files like 01_intro.pdf, 02_methods.pdf
"""
        messagebox.showinfo("File Pattern Help", help_text)
        
    def show_output_help(self):
        """Show help for output format"""
        help_text = """Output Format Help:

Use placeholders in the output filename:
• {directory} - Name of the subdirectory
• {date} - Current date (YYYY-MM-DD)
• {time} - Current time (HHMMSS)
• {datetime} - Current date and time (YYYY-MM-DD_HHMMSS)

Examples:
• {directory}_{date}.pdf (default) - Reports_2024-01-15.pdf
• merged_{directory}.pdf - merged_Reports.pdf
• {directory}_combined_{datetime}.pdf - Reports_combined_2024-01-15_143022.pdf
"""
        messagebox.showinfo("Output Format Help", help_text)
        
    def log(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def clear_log(self):
        """Clear the log area"""
        self.log_text.delete(1.0, tk.END)
        
    def preview_merge(self):
        """Preview what will be merged without actually merging"""
        if not self.selected_directory.get():
            messagebox.showerror("Error", "Please select a main directory first.")
            return
            
        try:
            self.log("Previewing merge operation...")
            preview_data = self.pdf_merger.preview_merge(
                self.selected_directory.get(),
                self.file_pattern.get(),
                self.output_format.get()
            )
            
            if not preview_data:
                self.log("No subdirectories with matching PDF files found.")
                return
                
            self.log(f"Found {len(preview_data)} subdirectories to process:")
            for subdir, files, output_file in preview_data:
                self.log(f"  {subdir}: {len(files)} files -> {output_file}")
                for file in files[:3]:  # Show first 3 files
                    self.log(f"    - {file}")
                if len(files) > 3:
                    self.log(f"    ... and {len(files) - 3} more files")
                    
        except Exception as e:
            self.log(f"Preview error: {str(e)}")
            messagebox.showerror("Preview Error", str(e))
            
    def merge_pdfs(self):
        """Perform the actual PDF merging"""
        if not self.selected_directory.get():
            messagebox.showerror("Error", "Please select a main directory first.")
            return
            
        # Confirm action
        if not messagebox.askyesno("Confirm", "This will create merged PDF files. Continue?"):
            return
            
        try:
            self.progress.start()
            self.log("Starting PDF merge operation...")
            
            results = self.pdf_merger.merge_pdfs(
                self.selected_directory.get(),
                self.file_pattern.get(),
                self.output_format.get(),
                progress_callback=self.log
            )
            
            self.progress.stop()
            
            if results:
                self.log(f"Successfully merged {len(results)} directories:")
                for output_file in results:
                    self.log(f"  Created: {output_file}")
                messagebox.showinfo("Success", f"Successfully merged PDFs in {len(results)} directories.")
            else:
                self.log("No PDFs were merged.")
                messagebox.showwarning("Warning", "No PDFs were found to merge.")
                
        except Exception as e:
            self.progress.stop()
            self.log(f"Merge error: {str(e)}")
            messagebox.showerror("Merge Error", str(e))

def main():
    """Main application entry point"""
    try:
        root = tk.Tk()
        app = PDFMergerGUI(root)
        root.mainloop()
    except Exception as e:
        logging.error(f"Application error: {e}")
        messagebox.showerror("Application Error", f"An error occurred: {e}")

if __name__ == "__main__":
    main()
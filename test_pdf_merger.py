#!/usr/bin/env python3
"""
Tests for PDF Merger with markdown->PDF->merge->markdown verification
"""

import os
import sys
import tempfile
import shutil
import subprocess
from pdf_merger import PDFMerger


def run_command(cmd, cwd=None):
    """Run a shell command and return the output"""
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"Command failed: {cmd}")
        print(f"stderr: {result.stderr}")
        print(f"stdout: {result.stdout}")
    return result.returncode, result.stdout, result.stderr


def create_markdown_file(path, content):
    """Create a markdown file with given content"""
    with open(path, 'w') as f:
        f.write(content)


def markdown_to_pdf(md_path, pdf_path):
    """Convert markdown to PDF using pandoc"""
    cmd = f'pandoc "{md_path}" -o "{pdf_path}"'
    returncode, stdout, stderr = run_command(cmd)
    if returncode != 0:
        raise Exception(f"Failed to convert markdown to PDF: {stderr}")
    return pdf_path


def pdf_to_text(pdf_path):
    """Extract text from PDF using pdftotext"""
    cmd = f'pdftotext "{pdf_path}" -'
    returncode, stdout, stderr = run_command(cmd)
    if returncode != 0:
        raise Exception(f"Failed to extract text from PDF: {stderr}")
    return stdout


def normalize_markdown_text(text):
    """Normalize markdown text for comparison"""
    # Remove extra whitespace, normalize line endings
    lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
    return '\n'.join(lines)


def test_merge_configuration_basic():
    """Test basic merge configuration with markdown->PDF->merge->markdown"""
    print("\n=== Test: Basic Merge Configuration ===")
    
    # Create temporary directory structure
    with tempfile.TemporaryDirectory() as tmpdir:
        root_dir = os.path.join(tmpdir, "test_root")
        os.makedirs(root_dir)
        
        # Create two subdirectories
        subdir1 = os.path.join(root_dir, "project1")
        subdir2 = os.path.join(root_dir, "project2")
        os.makedirs(subdir1)
        os.makedirs(subdir2)
        
        # Define markdown content
        intro_content = "# Introduction\n\nThis is the introduction section.\n"
        body_content = "# Body\n\nThis is the main body content.\n"
        conclusion_content = "# Conclusion\n\nThis is the conclusion section.\n"
        
        # Create markdown files for project1
        md_intro1 = os.path.join(subdir1, "intro.md")
        md_body1 = os.path.join(subdir1, "body.md")
        md_conclusion1 = os.path.join(subdir1, "conclusion.md")
        
        create_markdown_file(md_intro1, intro_content)
        create_markdown_file(md_body1, body_content)
        create_markdown_file(md_conclusion1, conclusion_content)
        
        # Convert to PDFs
        pdf_intro1 = os.path.join(subdir1, "intro.pdf")
        pdf_body1 = os.path.join(subdir1, "body.pdf")
        pdf_conclusion1 = os.path.join(subdir1, "conclusion.pdf")
        
        markdown_to_pdf(md_intro1, pdf_intro1)
        markdown_to_pdf(md_body1, pdf_body1)
        markdown_to_pdf(md_conclusion1, pdf_conclusion1)
        
        # Create markdown files for project2
        md_intro2 = os.path.join(subdir2, "intro.md")
        md_body2 = os.path.join(subdir2, "body.md")
        md_conclusion2 = os.path.join(subdir2, "conclusion.md")
        
        create_markdown_file(md_intro2, intro_content + "\nProject 2 specific content.")
        create_markdown_file(md_body2, body_content + "\nMore details for project 2.")
        create_markdown_file(md_conclusion2, conclusion_content + "\nProject 2 concludes here.")
        
        # Convert to PDFs
        pdf_intro2 = os.path.join(subdir2, "intro.pdf")
        pdf_body2 = os.path.join(subdir2, "body.pdf")
        pdf_conclusion2 = os.path.join(subdir2, "conclusion.pdf")
        
        markdown_to_pdf(md_intro2, pdf_intro2)
        markdown_to_pdf(md_body2, pdf_body2)
        markdown_to_pdf(md_conclusion2, pdf_conclusion2)
        
        # Initialize merger and set configuration
        merger = PDFMerger()
        merge_order = ["intro", "body", "conclusion"]
        merger.set_merge_config(root_dir, merge_order)
        
        # Verify configuration was set
        config = merger.get_merge_config(root_dir)
        assert config == merge_order, f"Expected {merge_order}, got {config}"
        print(f"✓ Configuration set correctly: {config}")
        
        # Merge PDFs
        results = merger.merge_pdfs(
            root_dir,
            "*.pdf",
            "{directory}_merged.pdf",
            use_merge_config=True
        )
        
        assert len(results) == 2, f"Expected 2 merged PDFs, got {len(results)}"
        print(f"✓ Successfully merged {len(results)} directories")
        
        # Check that merged PDFs exist
        merged_pdf1 = os.path.join(subdir1, "project1_merged.pdf")
        merged_pdf2 = os.path.join(subdir2, "project2_merged.pdf")
        
        assert os.path.exists(merged_pdf1), f"Merged PDF not found: {merged_pdf1}"
        assert os.path.exists(merged_pdf2), f"Merged PDF not found: {merged_pdf2}"
        print(f"✓ Merged PDFs exist")
        
        # Extract text from merged PDFs
        content1 = pdf_to_text(merged_pdf1)
        content2 = pdf_to_text(merged_pdf2)
        
        # Check that content contains expected sections in order
        # (pandoc may add some formatting, so we check for key phrases)
        assert "Introduction" in content1, "Introduction section missing"
        assert "Body" in content1, "Body section missing"
        assert "Conclusion" in content1, "Conclusion section missing"
        
        # Verify order by checking positions
        intro_pos = content1.find("Introduction")
        body_pos = content1.find("Body")
        conclusion_pos = content1.find("Conclusion")
        
        assert intro_pos < body_pos < conclusion_pos, \
            f"Sections not in correct order: intro={intro_pos}, body={body_pos}, conclusion={conclusion_pos}"
        print(f"✓ Content is in correct order (intro->body->conclusion)")
        
        # Check project2 has its specific content
        assert "Project 2 specific content" in content2, "Project 2 specific content missing"
        assert "More details for project 2" in content2, "Project 2 body content missing"
        print(f"✓ Project-specific content preserved")
        
        print("✓ Test passed!")
        return True


def test_merge_configuration_mandatory():
    """Test that merge configuration is mandatory when using merge mode"""
    print("\n=== Test: Merge Configuration is Mandatory ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        root_dir = os.path.join(tmpdir, "test_root")
        os.makedirs(root_dir)
        
        subdir = os.path.join(root_dir, "project1")
        os.makedirs(subdir)
        
        # Create a simple PDF
        md_file = os.path.join(subdir, "test.md")
        create_markdown_file(md_file, "# Test\n\nTest content.")
        pdf_file = os.path.join(subdir, "test.pdf")
        markdown_to_pdf(md_file, pdf_file)
        
        # Try to merge without setting configuration
        merger = PDFMerger()
        
        try:
            merger.merge_pdfs(
                root_dir,
                "*.pdf",
                "{directory}_merged.pdf",
                use_merge_config=True
            )
            assert False, "Should have raised exception for missing configuration"
        except Exception as e:
            assert "required but not set" in str(e), f"Wrong error message: {e}"
            print(f"✓ Correctly rejected merge without configuration")
            print(f"  Error message: {e}")
        
        print("✓ Test passed!")
        return True


def test_merge_configuration_missing_files():
    """Test that subdirectories with missing files are skipped"""
    print("\n=== Test: Skip Subdirectories with Missing Files ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        root_dir = os.path.join(tmpdir, "test_root")
        os.makedirs(root_dir)
        
        # Create three subdirectories
        subdir1 = os.path.join(root_dir, "complete")
        subdir2 = os.path.join(root_dir, "incomplete")
        subdir3 = os.path.join(root_dir, "also_complete")
        os.makedirs(subdir1)
        os.makedirs(subdir2)
        os.makedirs(subdir3)
        
        # Create complete set for subdir1
        for name in ["intro", "body", "conclusion"]:
            md_file = os.path.join(subdir1, f"{name}.md")
            create_markdown_file(md_file, f"# {name.capitalize()}\n\nContent for {name}.")
            pdf_file = os.path.join(subdir1, f"{name}.pdf")
            markdown_to_pdf(md_file, pdf_file)
        
        # Create incomplete set for subdir2 (missing conclusion)
        for name in ["intro", "body"]:
            md_file = os.path.join(subdir2, f"{name}.md")
            create_markdown_file(md_file, f"# {name.capitalize()}\n\nContent for {name}.")
            pdf_file = os.path.join(subdir2, f"{name}.pdf")
            markdown_to_pdf(md_file, pdf_file)
        
        # Create complete set for subdir3
        for name in ["intro", "body", "conclusion"]:
            md_file = os.path.join(subdir3, f"{name}.md")
            create_markdown_file(md_file, f"# {name.capitalize()}\n\nContent for {name}.")
            pdf_file = os.path.join(subdir3, f"{name}.pdf")
            markdown_to_pdf(md_file, pdf_file)
        
        # Set configuration and merge
        merger = PDFMerger()
        merge_order = ["intro", "body", "conclusion"]
        merger.set_merge_config(root_dir, merge_order)
        
        # Collect progress messages
        messages = []
        def callback(msg):
            messages.append(msg)
            print(f"  {msg}")
        
        results = merger.merge_pdfs(
            root_dir,
            "*.pdf",
            "{directory}_merged.pdf",
            progress_callback=callback,
            use_merge_config=True
        )
        
        # Should only have 2 results (subdir2 should be skipped)
        assert len(results) == 2, f"Expected 2 merged PDFs, got {len(results)}"
        print(f"✓ Only complete subdirectories were merged")
        
        # Verify that incomplete directory was skipped
        skip_messages = [m for m in messages if "Skipping" in m or "Missing" in m]
        assert len(skip_messages) > 0, "No skip messages found"
        print(f"✓ Incomplete directory was properly skipped")
        
        # Verify merged PDFs exist for complete directories
        merged_pdf1 = os.path.join(subdir1, "complete_merged.pdf")
        merged_pdf3 = os.path.join(subdir3, "also_complete_merged.pdf")
        
        assert os.path.exists(merged_pdf1), "Merged PDF for complete directory not found"
        assert os.path.exists(merged_pdf3), "Merged PDF for also_complete directory not found"
        print(f"✓ Merged PDFs created for complete directories")
        
        # Verify no merged PDF for incomplete directory
        merged_pdf2 = os.path.join(subdir2, "incomplete_merged.pdf")
        assert not os.path.exists(merged_pdf2), "Merged PDF should not exist for incomplete directory"
        print(f"✓ No merged PDF created for incomplete directory")
        
        print("✓ Test passed!")
        return True


def test_merge_configuration_case_insensitive():
    """Test that file matching is case-insensitive"""
    print("\n=== Test: Case-Insensitive File Matching ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        root_dir = os.path.join(tmpdir, "test_root")
        os.makedirs(root_dir)
        
        subdir = os.path.join(root_dir, "mixed_case")
        os.makedirs(subdir)
        
        # Create files with different cases
        files_to_create = [
            ("INTRO", "# Introduction\n\nIntro content."),
            ("Body", "# Body\n\nBody content."),
            ("conclusion", "# Conclusion\n\nConclusion content.")
        ]
        
        for name, content in files_to_create:
            md_file = os.path.join(subdir, f"{name}.md")
            create_markdown_file(md_file, content)
            pdf_file = os.path.join(subdir, f"{name}.pdf")
            markdown_to_pdf(md_file, pdf_file)
        
        # Set configuration with lowercase names
        merger = PDFMerger()
        merge_order = ["intro", "body", "conclusion"]
        merger.set_merge_config(root_dir, merge_order)
        
        # Merge
        results = merger.merge_pdfs(
            root_dir,
            "*.pdf",
            "{directory}_merged.pdf",
            use_merge_config=True
        )
        
        assert len(results) == 1, f"Expected 1 merged PDF, got {len(results)}"
        print(f"✓ Successfully merged files with different cases")
        
        # Verify merged PDF exists
        merged_pdf = os.path.join(subdir, "mixed_case_merged.pdf")
        assert os.path.exists(merged_pdf), "Merged PDF not found"
        
        # Extract text from merged PDF and verify order
        content = pdf_to_text(merged_pdf)
        
        # Verify all sections are present
        assert "Introduction" in content or "Intro content" in content, "Introduction section missing"
        assert "Body" in content or "Body content" in content, "Body section missing"
        assert "Conclusion" in content or "Conclusion content" in content, "Conclusion section missing"
        print(f"✓ All sections present in merged PDF")
        
        print("✓ Test passed!")
        return True


def test_merge_configuration_path_normalization():
    """Test that different path formats for the same directory work correctly"""
    print("\n=== Test: Path Normalization ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        root_dir = os.path.join(tmpdir, "test_root")
        os.makedirs(root_dir)
        
        subdir = os.path.join(root_dir, "project")
        os.makedirs(subdir)
        
        # Create test files
        md_file = os.path.join(subdir, "test.md")
        create_markdown_file(md_file, "# Test\n\nTest content.")
        pdf_file = os.path.join(subdir, "test.pdf")
        markdown_to_pdf(md_file, pdf_file)
        
        merger = PDFMerger()
        
        # Set configuration with absolute path
        abs_path = os.path.abspath(root_dir)
        merger.set_merge_config(abs_path, ["test"])
        
        # Try to get config with same path but potentially different format
        # (e.g., with trailing slash, or ./ prefix)
        config1 = merger.get_merge_config(abs_path)
        config2 = merger.get_merge_config(root_dir)
        
        assert config1 == ["test"], f"Config not found with absolute path"
        assert config2 == ["test"], f"Config not found with original path"
        print(f"✓ Configuration found with different path formats")
        
        print("✓ Test passed!")
        return True


def run_all_tests():
    """Run all tests and report results"""
    tests = [
        test_merge_configuration_basic,
        test_merge_configuration_mandatory,
        test_merge_configuration_missing_files,
        test_merge_configuration_case_insensitive,
        test_merge_configuration_path_normalization,
    ]
    
    passed = 0
    failed = 0
    
    print("=" * 70)
    print("Running PDF Merger Tests")
    print("=" * 70)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            failed += 1
            print(f"\n✗ Test failed: {test.__name__}")
            print(f"  Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 70)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Setup script for PDF Merger application
"""

from setuptools import setup, find_packages

# Read README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pdf-merger",
    version="1.0.0",
    author="walliscode",
    description="A Python application for merging PDF files in subdirectories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/walliscode/pdf_merger",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "pdf-merger=cli:main",
            "pdf-merger-gui=main:main",
        ],
    },
    extras_require={
        "gui": ["tkinter"],
    },
    include_package_data=True,
    zip_safe=False,
)
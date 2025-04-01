# Markdown to EPUB/DOCX Converter

A Python script that converts Markdown files to EPUB or DOCX format, with smart handling for citations and references.

## Prerequisites

1. **Python 3.x**: Required to run the script
2. **Pandoc**: Required by the pypandoc library. [Download from pandoc.org](https://pandoc.org/installing.html)

## Setup

1. **Clone or download this repository**

2. **Set up a virtual environment**:
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**:
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Activate the virtual environment** (if not already activated)

2. **Run the script**:
   ```bash
   # Default: Convert to EPUB (best for e-readers)
   python md_to_docx_converter.py
   
   # Convert to DOCX (Microsoft Word format)
   python md_to_docx_converter.py --format docx
   
   # Interactive format selection
   python md_to_docx_converter.py --interactive
   ```

3. **Select a Markdown file** from the list presented

4. **View output**: The converted file will be saved in the `output` directory

## Command-line Options

- `-f FORMAT, --format FORMAT`: Choose output format: epub (default) or docx
- `-i, --interactive`: Run in interactive mode to select format via prompt
- `-h, --help`: Show help message

## Features

- Converts Markdown files to EPUB (default) or DOCX format
- EPUB output includes table of contents for better navigation on e-readers
- Smart citation handling: converts citation-style links to proper footnotes
- Clean source URLs by removing tracking fragments from links
- Places Markdown files in the 'input' folder for better organization
- Extracts title from H1 header or first sentence for the filename
- Sanitizes filenames to be compatible with all operating systems
- Creates an organized output directory structure

## Notes

- This script requires Pandoc to be installed and available in your system PATH
- The virtual environment keeps the dependencies isolated from your global Python environment
- EPUB format is recommended for e-readers (Kindle, Kobo, etc.)
- When using with Kindle, you may need to convert the EPUB to MOBI or AZW3 format using Calibre 
# Markdown to EPUB/DOCX Converter

A Python script that converts Markdown files to EPUB or DOCX format, with smart handling for citations and e-reader compatibility.

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
   # Default: Convert to EPUB
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
- `-r, --remove-citations`: Remove all citations instead of converting them to footnotes
- `-h, --help`: Show help message

## Features

- Converts Markdown files to EPUB (default) or DOCX format
- **Citation Handling Options**:
  - Convert citation-style links to proper footnotes (default)
  - Completely remove citations (using `-r` flag) for cleaner text
- **E-reader Compatibility**:
  - Enhanced EPUB outputs with e-reader friendly settings
  - Proper handling of structure, metadata and fonts
- EPUB output includes table of contents for better navigation
- Smart citation handling: converts citation-style links to proper footnotes
- Clean source URLs by removing tracking fragments from links
- Places Markdown files in the 'input' folder for better organization
- Extracts title from H1 header or first sentence for the filename
- Sanitizes filenames to be compatible with all operating systems
- Creates an organized output directory structure

## E-reader Compatibility

For Kindle compatibility:
1. Use the EPUB format, which is now supported by modern Kindle devices
2. If your Kindle device shows errors with EPUB files, update your Kindle to the latest firmware
3. If you encounter any issues with the EPUB file, you can use the Amazon Send to Kindle service, which will convert it to an appropriate format

## Customizing EPUB Output

You can customize the EPUB output with these optional files:

1. **metadata.yaml**: Add metadata to your EPUB file (title, author, date, etc.)
   ```yaml
   ---
   title: Your Book Title
   author: Your Name
   date: 2025-04-01
   lang: en-US
   ---
   ```

2. **cover.png**: Add a cover image to your EPUB file
   - Place a PNG image named `cover.png` in the project directory
   - Recommended size: 1600×2400 pixels

## Notes

- This script requires Pandoc to be installed and available in your system PATH
- The virtual environment keeps the dependencies isolated from your global Python environment
- EPUB format works with most e-readers including newer Kindle devices, Kobo, Nook, etc. 
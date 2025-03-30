# Markdown to DOCX Converter

A Python script that converts Markdown files to DOCX format, with special handling for citation-style links.

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
   python md_to_docx_converter.py
   ```

3. **Select a Markdown file** from the list presented

4. **View output**: The converted DOCX file will be saved in the `output` directory

## Features

- Converts Markdown files to DOCX format
- Extracts title from H1 header or first sentence for the filename
- Removes citation-style links in the format `([Link Text](URL))` for cleaner output
- Sanitizes filenames to be compatible with all operating systems
- Creates an organized output directory structure

## Notes

- This script requires Pandoc to be installed and available in your system PATH
- The virtual environment keeps the dependencies isolated from your global Python environment 
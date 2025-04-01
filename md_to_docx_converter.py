import os
import re
import sys
import glob
import argparse

try:
    import pypandoc
except ImportError:
    print("Error: 'pypandoc' library not found.")
    print("Please install it using: pip install pypandoc")
    # Also remind about Pandoc itself
    print("\nNote: pypandoc requires Pandoc to be installed on your system.")
    print("Download Pandoc from: https://pandoc.org/installing.html")
    sys.exit(1)

# --- Configuration ---
OUTPUT_DIR = "output"
INPUT_DIR = "input"  # Added input directory configuration
MAX_FILENAME_LENGTH = 60 # Keep filenames reasonably short

# --- Helper Functions ---

def check_pandoc():
    """Checks if Pandoc executable is available."""
    try:
        pypandoc.get_pandoc_path()
        print("Pandoc found.")
    except OSError:
        print("Error: Pandoc installation not found in system PATH.")
        print("Please install Pandoc from https://pandoc.org/installing.html")
        print("and ensure it's added to your system's PATH.")
        sys.exit(1)

def find_md_files(directory=INPUT_DIR):  # Changed default directory to INPUT_DIR
    """Finds all .md files in the specified directory."""
    # Create the input directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    return glob.glob(os.path.join(directory, "*.md"))

def select_md_file(files):
    """Presents a list of files and prompts the user to select one."""
    if not files:
        print("No .md files found in the current directory.")
        return None

    print("\nPlease select the Markdown file to convert:")
    for i, f in enumerate(files):
        print(f"{i + 1}. {os.path.basename(f)}")

    while True:
        try:
            choice = input(f"Enter number (1-{len(files)}): ")
            index = int(choice) - 1
            if 0 <= index < len(files):
                return files[index]
            else:
                print("Invalid number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(0)


def sanitize_filename(filename):
    """Removes or replaces characters invalid for filenames."""
    # Remove leading/trailing whitespace
    filename = filename.strip()
    # Replace invalid characters with underscores
    filename = re.sub(r'[<>:"/\\|?*\']', '_', filename)
     # Replace multiple spaces/underscores with a single underscore
    filename = re.sub(r'[\s_]+', '_', filename)
    # Limit length
    return filename[:MAX_FILENAME_LENGTH]

def extract_title_and_preprocess(md_content):
    """
    Extracts title (H1 or first sentence) and preprocesses the Markdown content.
    Converts redundant link format to footnotes for cleaner output.
    """
    title = None
    # Try to find the first H1 header
    h1_match = re.search(r'^#\s+(.+)', md_content, re.MULTILINE)
    if h1_match:
        title = h1_match.group(1).strip()
        print(f"Found H1 title: '{title}'")
    else:
        # Find the first non-empty line as fallback title
        lines = md_content.strip().split('\n')
        first_line = next((line.strip() for line in lines if line.strip()), None)
        if first_line:
             # Remove markdown formatting like *, **, _, etc. from the beginning/end for title
            first_line = re.sub(r'^[\*\_\#\s]+|[\*\_\s]+$', '', first_line)
            # Take the first sentence (up to a period, question mark, or exclamation mark)
            sentence_match = re.match(r'([^.!?]+[.!?]?)', first_line)
            if sentence_match:
                title = sentence_match.group(1).strip()
            else: # If no punctuation, take the whole line (clipped)
                title = first_line
            print(f"No H1 found. Using first sentence/line part for title: '{title}'")
        else:
            title = "Untitled_Document" # Default if file is empty or only whitespace
            print("Warning: Could not determine title from content. Using default.")

    # --- Preprocessing for citation-style links ---
    # Target pattern: ` ([Link Text](URL))` possibly repeated
    # Strategy: Convert these citation-like links to proper footnotes
    processed_content = md_content
    
    # This regex captures citation-style links: ([Link Text](URL))
    link_pattern = r'\s*\(\[([^\]]+)\]\(([^)]+)\)\)'
    
    # Counter for footnotes
    footnote_count = 1
    
    # Function to replace each match with a footnote reference
    def replace_with_footnote(match):
        nonlocal footnote_count
        link_text = match.group(1)
        url = match.group(2)
        
        # Check if the URL contains fragment identifiers (like #:~:text=)
        # and clean it if needed
        clean_url = re.sub(r'#:~:text=.*$', '', url)
        
        # Create the footnote reference and definition
        footnote = f"[^{footnote_count}]"
        footnote_def = f"\n[^{footnote_count}]: {link_text}. {clean_url}"
        
        footnote_count += 1
        return footnote + footnote_def
    
    # Replace citation links with footnotes
    processed_content = re.sub(link_pattern, replace_with_footnote, processed_content)
    
    print("Preprocessing: Converted citation-style links '([Text](URL))' to footnotes.")
    return title, processed_content

def convert_markdown(md_file_path, output_dir, output_format='epub'):
    """Converts a single Markdown file to the specified format (EPUB by default)."""
    print(f"\nProcessing '{os.path.basename(md_file_path)}'...")

    try:
        # Read the Markdown file content
        with open(md_file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Extract title and preprocess content
        title, processed_content = extract_title_and_preprocess(md_content)

        # Sanitize the title for use as a filename
        base_filename = sanitize_filename(title)
        
        # Set output format specific settings
        if output_format.lower() == 'docx':
            extension = 'docx'
            format_name = 'DOCX'
            extra_args = ['--wrap=none']
        else:  # epub is default
            extension = 'epub'
            format_name = 'EPUB'
            extra_args = ['--toc', '--toc-depth=2']  # Add table of contents for EPUB
            
        output_filename = f"{base_filename}.{extension}"
        output_path = os.path.join(output_dir, output_filename)

        # Create the output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Perform the conversion using pypandoc
        print(f"Converting to {format_name}...")
        pypandoc.convert_text(
            processed_content,
            extension,
            format='md',
            outputfile=output_path,
            extra_args=extra_args
        )

        print(f"Successfully converted '{os.path.basename(md_file_path)}'")
        print(f"Output saved to: '{output_path}'")

    except FileNotFoundError:
        print(f"Error: Input file not found at '{md_file_path}'")
    except Exception as e:
        print(f"An error occurred during conversion: {e}")
        print("Ensure Pandoc is installed correctly and the Markdown file is valid.")

def select_output_format():
    """Asks the user to select the output format."""
    print("\nSelect output format:")
    print("1. EPUB (default, best for e-readers)")
    print("2. DOCX (Microsoft Word)")
    
    while True:
        try:
            choice = input("Enter your choice (default: 1): ").strip() or "1"
            if choice == "1":
                return "epub"
            elif choice == "2":
                return "docx"
            else:
                print("Invalid choice. Please enter 1 or 2.")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(0)

# --- Main Execution ---
if __name__ == "__main__":
    # Set up command line arguments
    parser = argparse.ArgumentParser(description="Convert Markdown files to EPUB or DOCX")
    parser.add_argument("-f", "--format", choices=["epub", "docx"], default="epub",
                        help="Output format: epub (default) or docx")
    parser.add_argument("-i", "--interactive", action="store_true",
                        help="Run in interactive mode to select format via prompt")
    
    args = parser.parse_args()
    
    check_pandoc() # Verify pandoc is available first
    
    # Ensure input directory exists
    os.makedirs(INPUT_DIR, exist_ok=True)
    
    # Get output format
    output_format = args.format
    if args.interactive:
        output_format = select_output_format()
    
    md_files = find_md_files()
    selected_file = select_md_file(md_files)

    if selected_file:
        convert_markdown(selected_file, OUTPUT_DIR, output_format)
    else:
        print("No file selected. Exiting.") 
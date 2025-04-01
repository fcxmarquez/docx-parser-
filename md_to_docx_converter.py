import os
import re
import sys
import glob

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
    Specifically targets the redundant link format for cleaner output.
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

    # --- Preprocessing for links ---
    # Target pattern: ` ([Link Text](URL))` possibly repeated
    # Strategy: Remove these citation-like links entirely for a cleaner read.
    # This regex looks for optional whitespace, then '([', text, '](', url, '))'
    processed_content = md_content
    link_pattern = r'\s*\(\[([^\]]+)\]\(([^)]+)\)\)'

    # Repeatedly remove the pattern until no more matches are found
    previous_content = None
    while previous_content != processed_content:
        previous_content = processed_content
        processed_content = re.sub(link_pattern, '', processed_content)

    # Optional: Handle standard markdown links if needed (e.g., convert to footnotes)
    # For now, Pandoc handles standard [Text](URL) links correctly by default.

    print("Preprocessing: Removed citation-like links '([Text](URL))'.")
    return title, processed_content


def convert_md_to_docx(md_file_path, output_dir):
    """Converts a single Markdown file to DOCX."""
    print(f"\nProcessing '{os.path.basename(md_file_path)}'...")

    try:
        # Read the Markdown file content
        with open(md_file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Extract title and preprocess content
        title, processed_content = extract_title_and_preprocess(md_content)

        # Sanitize the title for use as a filename
        base_filename = sanitize_filename(title)
        output_filename = f"{base_filename}.docx"
        output_path = os.path.join(output_dir, output_filename)

        # Create the output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Perform the conversion using pypandoc
        print(f"Converting to DOCX...")
        pypandoc.convert_text(
            processed_content,
            'docx',
            format='md',
            outputfile=output_path,
            extra_args=['--wrap=none'] # Optional: Prevent auto line wrapping if desired
        )

        print(f"Successfully converted '{os.path.basename(md_file_path)}'")
        print(f"Output saved to: '{output_path}'")

    except FileNotFoundError:
        print(f"Error: Input file not found at '{md_file_path}'")
    except Exception as e:
        print(f"An error occurred during conversion: {e}")
        print("Ensure Pandoc is installed correctly and the Markdown file is valid.")

# --- Main Execution ---
if __name__ == "__main__":
    check_pandoc() # Verify pandoc is available first
    
    # Ensure input directory exists
    os.makedirs(INPUT_DIR, exist_ok=True)
    
    md_files = find_md_files()
    selected_file = select_md_file(md_files)

    if selected_file:
        convert_md_to_docx(selected_file, OUTPUT_DIR)
    else:
        print("No file selected. Exiting.") 
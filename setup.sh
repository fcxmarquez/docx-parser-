#!/bin/bash

# Colors for better output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Setting up Markdown to DOCX Converter ===${NC}"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3 first.${NC}"
    exit 1
fi

echo -e "${GREEN}Python 3 is installed.${NC}"

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to create virtual environment.${NC}"
        exit 1
    fi
    echo -e "${GREEN}Virtual environment created.${NC}"
else
    echo -e "${GREEN}Virtual environment already exists.${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to activate virtual environment.${NC}"
    exit 1
fi
echo -e "${GREEN}Virtual environment activated.${NC}"

# Install Python dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to install Python dependencies.${NC}"
    exit 1
fi
echo -e "${GREEN}Python dependencies installed.${NC}"

# Check if Pandoc is installed
if ! command -v pandoc &> /dev/null; then
    echo -e "${YELLOW}Pandoc is not installed. Let's install it.${NC}"
    
    # Check the OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo -e "${YELLOW}Detected Linux. Trying to install with apt...${NC}"
        sudo apt-get update && sudo apt-get install -y pandoc
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo -e "${YELLOW}Detected macOS. Trying to install with Homebrew...${NC}"
        if ! command -v brew &> /dev/null; then
            echo -e "${RED}Homebrew is not installed. Please install Homebrew first: https://brew.sh/${NC}"
            echo -e "${RED}Or install Pandoc manually: https://pandoc.org/installing.html${NC}"
            exit 1
        else
            brew install pandoc
        fi
    else
        echo -e "${RED}Could not determine your OS. Please install Pandoc manually: https://pandoc.org/installing.html${NC}"
        exit 1
    fi
    
    # Check if Pandoc was installed successfully
    if ! command -v pandoc &> /dev/null; then
        echo -e "${RED}Failed to install Pandoc. Please install manually: https://pandoc.org/installing.html${NC}"
        exit 1
    else
        echo -e "${GREEN}Pandoc installed successfully.${NC}"
    fi
else
    echo -e "${GREEN}Pandoc is already installed.${NC}"
fi

echo -e "${GREEN}Setup completed successfully!${NC}"
echo -e "${YELLOW}To run the converter, use: python md_to_docx_converter.py${NC}" 
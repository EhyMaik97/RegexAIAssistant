# AI Regex Generator

A desktop application that uses AI to generate regex patterns from sample text and target values.

## Features

- Modern, dark-themed UI
- AI-powered regex pattern generation
- Simple copy-paste functionality
- Cross-platform compatibility

## Requirements

- A GROQ API key (sign up at [groq.com](https://console.groq.com))

## Installation

### Option 1: Executable (Windows)

1. Download the latest `RegexAIAssistant.exe` from the releases section
2. Run the executable
3. When prompted, enter your GROQ API key
4. The application will save your API key for future use

### Option 2: Run from source code

1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install requirements: `pip install -r requirements.txt`
5. Create a `.env` file in the project root with: `GROQ_API_KEY=your_api_key_here`
6. Run the application: `python app/app.py`

## Building from Source

To build the executable from source:

1. Make sure you have all requirements installed
2. Run the build script: `python build.py`
3. The executable will be created in the `dist` directory

## Usage

1. Enter sample text containing the value you want to extract
2. Enter the exact target value that should be matched
3. Click "Generate Regex" to create a regex pattern
4. Copy the generated pattern to use in your code or tools

## Technical Details

- Built with PyQt5 for the user interface
- Uses LangChain with Groq's LLM API for AI reasoning
- Packaged with PyInstaller for distribution


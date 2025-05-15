# AI Regex Generator

A modern desktop application that leverages AI to generate optimal regular expression patterns from sample text, powered by Groq's LLM API.

![Regex AI Assistant](assets/app_icon.png)

## Features

- **Modern Dark-themed UI**: Sleek, contemporary interface with dark mode
- **AI-powered Regex Generation**: Uses Groq's LLaMA 3.3 70B model to create precise regex patterns
- **User-friendly Experience**: Simple input of sample text and target value
- **Real-time Processing**: Asynchronous processing to keep the UI responsive
- **Cross-platform**: Works on Windows, macOS, and Linux

## Requirements

- A Groq API key (sign up at [console.groq.com](https://console.groq.com))

## Installation

### Windows Executable

1. Download the latest `RegexAIAssistant.exe` from the [Releases](../../releases) section
2. Run the executable
3. When prompted, enter your Groq API key
4. The application will save your API key for future use

### From Source Code

1. Clone this repository:
   ```
   git clone <repository-url>
   cd regex-ai-assistant
   ```

2. Create and activate a virtual environment:
   ```
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your Groq API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

5. Run the application:
   ```
   python app/app.py
   ```

## Building from Source

To create your own executable:

1. Install all dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the build script:
   ```
   python build.py
   ```

3. The executable will be created in the `dist` directory

## Usage Guide

1. **Enter Sample Text**: Paste or type the text containing the value you want to extract
2. **Target Value**: Enter the specific value you want to match with regex
3. **Generate**: Click the "Generate Regex" button to create the optimal pattern
4. **Copy**: Use the "Copy to Clipboard" button to copy the generated regex
5. **Clear**: Reset all fields with the "Clear All" button

## How It Works

The application uses:
- **PyQt5** for the user interface
- **LangChain** with **Groq's API** for AI-powered regex generation
- **Prompt Engineering** to guide the AI in creating optimal regex patterns
- **Threading** to keep the UI responsive during API calls

## Technical Architecture

```
├── app/
│   ├── app.py          # Main application code 
│   ├── chains.py       # LangChain integration
│   └── template.txt    # Prompt template
├── assets/             # Icons and assets
├── build.py            # Script to build the executable
└── requirements.txt    # Project dependencies
```

## Troubleshooting

- **API Key Issues**: If you encounter API authentication errors, check your Groq API key in the .env file
- **Missing Dependencies**: Run `pip install -r requirements.txt` to ensure all packages are installed
- **Executable Errors**: Try running from source if the executable has issues

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

- UI design inspired by modern code editors
- Regex generation powered by [Groq](https://groq.com)'s LLaMA 3.3 70B model
- Built with [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) and [LangChain](https://www.langchain.com)


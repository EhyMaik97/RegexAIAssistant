# Regex AI Assistant

Welcome to **Regex AI Assistant**, a powerful tool that helps you generate the most accurate and minimal regular expressions (regex) to extract specific values from text. Powered by an AI model, this app can quickly generate regex patterns for various use cases. You can enter a sample text and the target value you want to extract, and the app will generate the regex pattern to match that value.


![alt text](gif.gif)


## Features

- **Input Text**: Enter a sample text (can be natural language or structured data like logs).
- **Target Value**: Provide the target value you want to extract (e.g., "example_value" from `example_key="example_value"`).
- **Generate Regex**: Get the most accurate and minimal regex pattern to extract the value from the text.
- **Copy Regex**: Easily copy the generated regex pattern with a click.

## AI Technology

This application uses **[GroqCloud](https://console.groq.com/home)** as the backend language model provider. It offers ultra-low-latency inference for large language models, making the user experience fast and responsive.

The specific model used is **[LLaMA 3.1 70B Versatile](https://console.groq.com/docs/model/llama-3.3-70b-versatile)** by Meta, known for its strong natural language understanding and generation capabilities. This model is particularly well-suited for tasks like pattern recognition and text extraction, making it ideal for generating precise regular expressions.


## Installation

To get started with **Regex AI Assistant**, follow these installation steps based on your operating system.

### Prerequisites

- Python 3.7+
- A working GroqCloud API key

### 1. Clone the Repository

```bash
git clone https://github.com/EhyMaik97/regex-ai-assistant.git
cd regex-ai-assistant
```

### 2. Set Up the Environment

Create and activate a Python virtual environment (optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # For Windows, use `venv\Scripts\activate`
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the root directory and add your API key:

```bash
GROQ_API_KEY=your_api_key_here
```

### 4. Running the Streamlit App

You can run the app as a web-based Streamlit application:

```bash
streamlit run main.py
```
This will open the app in your browser at http://localhost:8501, where you can start using the Regex AI Assistant.

## 


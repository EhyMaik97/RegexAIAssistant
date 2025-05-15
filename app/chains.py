import os
import sys
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv, find_dotenv

# Add support for PyInstaller packaged app
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# Try to load from various locations
load_dotenv(find_dotenv(usecwd=True))

MODEL_NAME = "llama-3.3-70b-versatile"
TEMPERATURE = 0
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TEMPLATE_FILE = resource_path("app/template.txt")

class Chain:
    """
    A class that contains the logic for the regex generation chain.
    """
    
    def __init__(self):
        """
        Initialize the Chain class with the LLM and the template.
        """
        self.llm = ChatGroq(temperature=TEMPERATURE, groq_api_key=GROQ_API_KEY, model_name=MODEL_NAME)
        try:
            with open(TEMPLATE_FILE) as f: 
                self.template = f.read()
        except FileNotFoundError:
            # Fallback to direct path for development
            with open("app/template.txt") as f:
                self.template = f.read()
            
    def write_regex(self, sample_text: str, target_value: str) -> str:
        """
        Write a regex pattern that extracts the target value from the sample text.
        """
        prompt_regex = PromptTemplate.from_template(
            self.template
        )

        chain_regex = prompt_regex | self.llm
        res = chain_regex.invoke({
            "sample_text": sample_text,
            "target_value": target_value
        })
        return res.content.strip()

if __name__ == "__main__":
    print(GROQ_API_KEY)
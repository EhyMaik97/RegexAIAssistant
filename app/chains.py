import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

class Chain:
    """
    A class that contains the logic for the regex generation chain.
    """
    
    def __init__(self):
        """
        Initialize the Chain class with the LLM and the template.
        """
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile")
        with open("template.txt") as f: 
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
    print(os.getenv("GROQ_API_KEY"))
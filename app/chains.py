import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile")

    def write_regex(self, sample_text, target_value):
        prompt_regex = PromptTemplate.from_template(
            """
            ### INSTRUCTION:
            You are a highly skilled regular expression (regex) expert.
            Your task is to generate the most accurate and minimal regex pattern 
            that extracts a specific value from a given input text.

            The input will include:
            - A sample text (realistic, natural language or structured)
            - A specific target value that appears somewhere in that text

            Your job is to:
            1. Analyze the context and structure of the input text.
            2. Identify the target value within it.
            3. Generate a regex pattern that matches only the value (e.g., "value_123_example") **exactly**, 
            excluding any key names or extra characters (such as `key1=`).
            4. Return only the regex pattern NOT THE VALUE ALREADY CALUCALTED (without code or explanation).

            Ensure that the regex captures the value inside the quotes and does not include the field name (e.g., `subtype=`).

            ### NO PREAMBLE AND NO backtick:

            [text]
            {sample_text}

            [value]
            {target_value}

            [regex]
            """
        )

        chain_regex = prompt_regex | self.llm
        res = chain_regex.invoke({
            "sample_text": str(sample_text),
            "target_value": str(target_value)
        })
        return res.content.strip()

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))
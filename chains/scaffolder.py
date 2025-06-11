from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv  
from typing import Any, Dict
import os
import sys

load_dotenv()



class DirSchema(BaseModel):
    project_name: str = Field(description="Name of the project")
    structure: Dict[str, Any] = Field(description="Directory structure in JSON format")

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")


directory_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """ 
            You are a senior software architect and project manager.
            Your job is to create a comprehensive directory and its file structure for software projects.
            You will receive a project name and a detailed project description and tech stack.
            Your output should be a JSON object with two fields:
            - `project_name`: the name of the project
            - `structure`: a JSON object representing the directory structure
            The structure should be well-organized, modular, and suitable for a software project of this type.

            Note : use the standard naming conventions for directories and files.
            The output should be a valid JSON object with the following format:

        """
    ),
        ("user", "{Project_description}")
])

parser = JsonOutputParser(pydantic_object=DirSchema)

scapefolding_chain = directory_prompt | llm | parser


def create_structure(base_path, structure_dict):
    """Recursively creates directories and files based on the structure dictionary."""
    for name, content in structure_dict.items():
        item_path = os.path.join(base_path, name)

        if isinstance(content, dict):
            # It's a directory
            print(f"Creating directory: {item_path}")
            os.makedirs(item_path, exist_ok=True) # exist_ok=True prevents error if dir already exists
            # Recurse into this new directory
            create_structure(item_path, content)
        elif isinstance(content, str):
            # It's a file (value is an empty string)
            print(f"Creating file: {item_path}")
            # Create an empty file
            try:
                with open(item_path, 'w') as f:
                    f.write(content) # Write the content (empty string in this case)
            except IOError as e:
                print(f"Error creating file {item_path}: {e}", file=sys.stderr)

        else:
            print(f"Warning: Unknown type for item '{name}' at path '{base_path}'. Skipping.", file=sys.stderr)

# Example usage
# result = chain.invoke({
#     "Project_description": output
# })
# print(result)
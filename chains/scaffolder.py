# from pydantic import BaseModel, Field
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_core.output_parsers import JsonOutputParser
# from dotenv import load_dotenv  
# from typing import Any, Dict
# import os
# import sys

# load_dotenv()



# class DirSchema(BaseModel):
#     project_name: str = Field(description="Name of the project")
#     structure: Dict[str, Any] = Field(description="Directory structure in JSON format")

# llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")


# directory_prompt = ChatPromptTemplate.from_messages([
#     (
#         "system",
#         """ 
#             You are a senior software architect and project manager.
#             Your job is to create a comprehensive directory and its file structure for software projects.
#             You will receive a project name and a detailed project description and tech stack.
#             Your output should be a JSON object with two fields:
#             - `project_name`: the name of the project
#             - `structure`: a JSON object representing the directory structure
#             The structure should be well-organized, modular, and suitable for a software project of this type.

#             Note : use the standard naming conventions for directories and files.
#             The output should be a valid JSON object with the following format:

#         """
#     ),
#         ("user", "{Project_description}")
# ])

# parser = JsonOutputParser(pydantic_object=DirSchema)

# scapefolding_chain = directory_prompt | llm | parser


# def create_structure(base_path, structure_dict):
#     """Recursively creates directories and files based on the structure dictionary."""
#     for name, content in structure_dict.items():
#         item_path = os.path.join(base_path, name)

#         if isinstance(content, dict):
#             # It's a directory
#             print(f"Creating directory: {item_path}")
#             os.makedirs(item_path, exist_ok=True) # exist_ok=True prevents error if dir already exists
#             # Recurse into this new directory
#             create_structure(item_path, content)
#         elif isinstance(content, str):
#             # It's a file (value is an empty string)
#             print(f"Creating file: {item_path}")
#             # Create an empty file
#             try:
#                 with open(item_path, 'w') as f:
#                     f.write(content) # Write the content (empty string in this case)
#             except IOError as e:
#                 print(f"Error creating file {item_path}: {e}", file=sys.stderr)

#         else:
#             print(f"Warning: Unknown type for item '{name}' at path '{base_path}'. Skipping.", file=sys.stderr)

# # Example usage
# # result = chain.invoke({
# #     "Project_description": output
# # })
# # print(result)




import asyncio
import json
from dotenv import load_dotenv
from typing import Dict, Union
from pydantic import BaseModel, Field
import uuid
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain.agents import Agent,AgentExecutor,AgentOutputParser
from langchain.agents import create_tool_calling_agent
from langchain_core.runnables import RunnableLambda
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.client import MultiServerMCPClient
from tools.repo_search import search_repos
from tools.MakeDir import generate_project

# Load env vars
load_dotenv()

# Pydantic schema for structured output
class ProjectDirectory(BaseModel):
    projectName: str = Field(..., description="Name of the project")
    directory: Dict[str, Union[str, dict]] = Field(..., description="Directory and file structure of the project")

# Setup MCP client
client = MultiServerMCPClient({
    "repo": {
        "command": "node",
        "args": ["mcpservers/gh-mcp-server/build/index.js"],
        "transport": "stdio",
    },
})

# prompt = ChatPromptTemplate.from_messages([
#     ("system", """
#     You are a senior software architect and project planner.
#         - Make 2 - 3 search queries then execute all queries on search repo tool
#          and take top 3 github repo atmost and atleast one to understand the structure of project

#         You have access to these tools:
#         - `search_repos`: Given a search query, returns matching GitHub repositories.
#         - `get-repo-structure`: Given a GitHub owner and repo name, returns its full directory structure.

#         Your job:
#         1. Read the user's project description.
#         2. Make and execute more than 2 github repo search queries, it should be advanced search queries
#         3. Use `search_repos` to find relevant GitHub repositories.
#         4. Use `get-repo-structure` on that repository to get its directory layout.
#         5. From that structures of multiple repos select atmost 3 structures.
#         5. From that structure, create a simplified and clean JSON layout for the project by understanding 
#             that structures with your own knowledge and that repos structures.

#         You should only return two field:
#         `projectName`: str = Field(..., description="Name of the project")
#         `directory`: Dict[str, Union[str, dict]] = Field(..., description="Directory and file structure of the project")
        

#         ⚠️ You MUST use these tools before producing the final JSON.

#         Note : Your final response should be JSON 
     
#         {messages}

#     """),
#     MessagesPlaceholder(variable_name="messages")
#     # MessagesPlaceholder(variable_name="agent_scratchpad")
# ])

prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a senior software architect and technical planner.

Your task is to analyze a user-provided project description and produce a clean, modular, and semantically meaningful directory and file structure for the entire project. You must **first investigate real-world open-source repositories** before generating output.

You have access to the following tools:
- `search_repos`: Given a search query, returns matching GitHub repositories.
- `get-repo-structure`: Given a GitHub owner and repo name, returns its full directory structure.

          
Your workflow:
1. Read the user's detailed project description and understand the technical requirements, domains, and expected features.
2. Generate at least 2'3 advanced and diverse GitHub repository search queries covering similar domains, frameworks, or problem scopes.
3. Execute these queries using `search_repos` and extract up to **3** high-quality, relevant repositories (at least 1 is mandatory).
4. Use `get-repo-structure` on each to understand how real projects structure their codebases, YOu need see structure for the repos which are search but if you found any releavent and sufficient information from any one repo also then you can start with next step.
5. Learn from those structures and your domain knowledge to generate a **customized**, **clean**, and **semantically grouped** directory structure.

✳️ Your output must:
- Be a Python-like JSON object
- Contain exactly two fields:
  - `projectName`: str = Name of the project
  - `directory`: Dict = Custom, modular directory structure

🧠 Tips for designing the structure:
- Follow good architecture principles (separation of concerns, layers).
- Clearly distinguish backend and frontend (if applicable).
- Group backend into `models`, `schemas`, `services`, `routes`, `utils`, etc.
- Group frontend into `pages`, `components`, `services`, etc.

📌 Example output format (simplified):

```json
{{
  "projectName": "MyApp",
  "directory": {{
    "project_root": {{
      "backend": {{
        "app": {{
          "main.py": "Entry point for FastAPI app",
          "models": {{
            "user.py": ["User", "Role"]
          }},
          "services": {{
            "auth.py": ["register_user()", "login_user()"]
          }}
        }},
        "requirements.txt": "Python dependencies"
      }},
      "frontend": {{
        "src": {{
          "pages": {{
            "Login.tsx": "Handles user login"
          }},
          "components": {{
            "Navbar.tsx": "Top-level navigation"
          }}
        }},
        "package.json": "Frontend dependencies"
      }},
      "README.md": "Project overview and instructions"
    }}
  }}
}}
Note: Use industry-level naming conventions for files and folders.

⚠️ Do NOT make up generic folders or APIs. Infer them from real project patterns and adapt to the user's domain (e.g., healthcare, finance, ecommerce, education, etc.)
⚠️ You MUST use these tools before producing the final JSON.
     
Remember:
you must use First use search_repos and get-repo-structure tools
Then return the final output in proper JSON

{messages}
"""),
MessagesPlaceholder(variable_name="messages")
])

async def build_dir_structure(query: str):
    async with client.session("repo") as session:
        mcp_tools = await load_mcp_tools(session)

        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

        tools = mcp_tools + [search_repos]
  
        # user_query = "Build a lightweight e-commerce dashboard using Angular or Vue and PostgreSQL like Amazon."
        user_query = query

        agent = create_react_agent(model=llm, tools=tools, prompt=prompt)

        response_text = await agent.ainvoke({"messages": [{"role": "user", "content": user_query}]})

        print(response_text['messages'][-1])

        output = JsonOutputParser(pydantic_object=ProjectDirectory).parse(response_text['messages'][-1].content)
        project = ProjectDirectory(**output)

        print(project.model_dump_json(indent=2))
        print(type(project))
        print(type(dict(project)))
        generate_project(dict(project), user_id= "abc_12345")

        # return project
        
        

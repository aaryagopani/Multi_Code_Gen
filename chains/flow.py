from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv

load_dotenv() 

llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash")


flow_prompt =  ChatPromptTemplate.from_messages([
    (
        "system",
        """
            You are a software architect agent.
            Your task is to analyze a user-provided project idea which contains system overview, tech stack and various other things which need to be taken care
            According to that try to generate a clean, modular backend and frontend functionality and feature list.

            Analyse and write the functionality step by step each sub-system needed in for my project idea
            **Note:** 
                - Mention any externel API is needed
                - Mention each and every thing such that programmer just need to code according to it

            You will recieve and thinker agent output which is high level blueprint for the project according to it break down and provide a clean and modular functionalities as an output.

        """
    ),
    ("user", "{thinker_output}")
    # MessagesPlaceholder(variable_name="thinker_output"),
    
])


flow_chain = flow_prompt | llm

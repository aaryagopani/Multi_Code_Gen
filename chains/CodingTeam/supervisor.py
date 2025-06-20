from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import Literal

load_dotenv()

# Simple Output Model
class SupervisorOutput(BaseModel):
    agent_name: Literal["frontend", "backend", "database"] = Field(
        description="The agent to be called next"
    )
    task_details: str = Field(
        description="Detailed explanation of what needs to be coded next"
    )
    status_message: str = Field(
        description="Short progress update (2-3 sentences) including the filename where the next code changes should be applied"
    )

# Simple Supervisor Prompt
supervisor_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a software project manager supervising an AI coding team.

Your team: [frontend, backend, database]

You receive:
- Directory structure: {directory}
- Implementation flow: {flow}
- Conversation history between agents which tracks the progress of what work has been done to guide the next task.

Your job:
1. Look at what's been done in the conversation
2. Decide which agent should work next
3. Tell them exactly what to code
4. Give a short status update

Rules:
- Work step by step, not everything at once
- Build backend before frontend that uses it
- Database setup before backend that uses database
- One clear task per agent call

Output exactly 3 things:
1. Which agent to call
2. What they should code (be detailed and specific)
3. Short status message for tracking progress"""
    ),
    MessagesPlaceholder(variable_name="messages"),
])

# Create supervisor chain

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")  
supervisor_parser = JsonOutputParser(pydantic_object=SupervisorOutput)
supervisor_chain = supervisor_prompt | llm | supervisor_parser




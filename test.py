from dotenv import load_dotenv
from langchain_core.tools import tool
load_dotenv()  # This loads the GEMINI_API_KEY from .env
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

from langgraph.graph import add_messages
from typing_extensions import TypedDict
from typing import Annotated, List
from langchain_core.messages import BaseMessage, HumanMessage

class State(TypedDict): 
    messages : Annotated[List[BaseMessage], add_messages]
    clarification_count: int
    clarification_needed: bool

# Define the prompt for the thinker agent
thinker_prompt = ChatPromptTemplate.from_messages([
    (
        "system", 
        """You are a senior product analyst and technical solution designer.

Your job is to clarify and refine software project ideas through a structured conversation.

Follow these rules:
1. If the user's idea is unclear, ask ONE follow-up question to get better clarity.
2. After asking the question, immediately call the tool `back_to_user_tool()` to notify the system that you are awaiting the user's clarification.
3. Repeat this process for at most 3 rounds.
4. If the idea becomes sufficiently clear, provide a structured summary of the project. The summary must include:
   - Project goals
   - Target users
   - Key components or features

IMPORTANT:
- When clarification is needed, DO NOT provide a summary or partial analysis.
- Always phrase the follow-up as a conversational assistant message, and then call the tool.
- The tool will handle flow control — your job is to decide when to ask or summarize.
"""
    ),
    MessagesPlaceholder(variable_name="messages"),
]) 

@tool
def back_to_user_tool(state: State) -> str:
    """
    Tool is helpful for the thinker agent to clarify the project idea or prompt.
    It can be used to ask follow-up questions or provide a summary of the project idea.
    It is not intended to generate code or solutions directly.
    This tool is used to interact with the user to refine their project idea.
    """
    state["clarification_needed"] = True
    state["clarification_count"] += 1

    return thinker_prompt.invoke({
        "messages": state.get("messages", []),
    }).content


# Initialize state
state = State(messages=[], clarification_count=0, clarification_needed=False)

# Initialize LLM and bind tool
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
llm_with_tools = llm.bind_tools([back_to_user_tool])

# Combine prompt and LLM into a chain
thinker_chain = thinker_prompt | llm_with_tools

def thinker_node(state: State):
    response = thinker_chain.invoke({
        "messages": state.get("messages", []),
    })
    print("\n--- DEBUG: Raw LLM Output ---")
    print(response)

    if hasattr(response, "tool_calls"):
        print("\n--- Tool Calls Detected ---")
        for tool_call in response.tool_calls:
            print(f"Tool Name: {tool_call['name']}")
            print(f"Tool Args: {tool_call['args']}")

    if hasattr(response, "content"):
        print("\n--- Assistant Message ---")
        print(response.content)

    return response

def get_user_input_and_update_state(state: State) -> State:
    user_input = input("User: ")
    # Append the user message to state messages list
    state["messages"].append(HumanMessage(content=user_input))
    return state


# Run once
state = get_user_input_and_update_state(state)
ai_response = thinker_node(state)
state["messages"].append(ai_response)

print("\n--- Full Conversation ---")
for msg in state["messages"]:
    print(f"{msg.type}: {msg.content}")

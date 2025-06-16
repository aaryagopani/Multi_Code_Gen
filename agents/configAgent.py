from models.models import CodeState
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.client import MultiServerMCPClient

client = MultiServerMCPClient({
    "filesystem": {
        "command": "node",
        "args": ["mcpservers/filesystem/dist/index.js"],
        "transport": "stdio",
    },
})

prompt = """
    You are an expert configuration agent that helps to set up and manage the project environment and configuration.
    You will be called prior to any other agent for setting the configuration of project.
    You will recieve the CodeState object which contains 3 fields:
        1. Flow: A detailed start-to-end implementation plan for the project.
        2. Directory: The current directory structure of the project.
        3. ProjectStatus: The current status of the project, indicating how much has been completed.

    You will have tools available to you that can help you in setting up the project environment.
        1. FileSystem: This tool allows you to interact with the filesystem, enabling you to create, read, update, and delete files and directories.
        2. InternetSearch: This tool allows you to search the internet for information, which can be useful for gathering additional context or resources needed for the project configuration.

    To Use the tools, you will need to call them with the appropriate parameters.
    For InternetSearch, you should create atmost 3 queries and atleast 1 query and use this tool for getting result.
    For FileSystem, you can create, read, update, or delete files and directories as needed.

    Your task is to identify the what configuration file needed for making the project run successfully.
    For it you can create a new file, update an existing file, or delete a file if it is not needed.
    You can also create directories if needed to organize the project structure better.
    You need write configuration code also in the directory structure provided in the CodeState object or if you create any new files.

    You will also need to ensure that the project is set up correctly based on the Flow and Directory provided.

    - At last you should return the status Message for the project configuration which you have completed.

    ⚠️ Important:
    - Always refer to the CodeState object for the current project status and directory structure.
    - Use the tools provided to you effectively to manage the project configuration.

    ⚠️ Don't Deviate from the CodeState object, as it contains crucial information about the project.

"""

async def configAgent(CodeState: CodeState):
    async with client.session("filesystem") as session:
        tools_list = await load_mcp_tools(session)
        # mcp_tools = {tool.name: tool for tool in tools_list}

        


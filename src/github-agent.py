from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.dataclasses import ChatMessage
from haystack.components.agents import Agent
from haystack_integrations.tools.mcp import MCPTool, StdioServerInfo
from haystack.utils import Secret
import os

github_mcp_server = StdioServerInfo(
        ## TODO: Add correct params for the Github MCP Server (official or legacy)
        command = "../github-mcp-server/github-mcp-server",
        args = ["stdio"],
        env = {
            "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"), # DO NOT ADD IT TO YOUR COMMIT
            "GITHUB_ENABLE_COMMAND_LOGGING": "true"
        }
    )

print("MCP server is created")

## TODO: Create your tools here:

tool_list_files = MCPTool(name="search_code", server_info=github_mcp_server)
tool_read_file = MCPTool(name="get_file_contents", server_info=github_mcp_server)
tool_create_issue = MCPTool(name="create_issue", server_info=github_mcp_server)

tools = [tool_list_files, tool_read_file, tool_create_issue]

print("MCP tools are created")

## TODO: Create your Agent here:

generator = OpenAIChatGenerator(
    api_key = Secret.from_token(os.getenv("api_key")),
    model = "o4-mini"
)

agent = Agent(
    tools = tools,
    chat_generator = generator,
)

print("Agent created")

## Example query to test your agent
user_input = "Can you find the typo in the README of jmpltanga/spring-into-haystack and open an issue about how to fix it?"

## (OPTIONAL) Feel free to add other example queries that can be resolved with this Agent

response = agent.run(messages=[ChatMessage.from_user(text=user_input)])

## Print the agent thinking process
print(response)
## Print the final response
print(response["messages"][-1].text)
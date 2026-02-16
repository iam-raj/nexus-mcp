from mcp.server.fastmcp import FastMCP
from tools.system import register_system_tools
from tools.nexus_notes import register_note_tools
from tools.network import register_network_tools

# Initialize the Nexus-MCP Server
# The name here is what the AI will see as the tool provider
mcp = FastMCP("nexus-mcp")

# Register modular toolsets
register_system_tools(mcp)
register_note_tools(mcp)
register_network_tools(mcp)

if __name__ == "__main__":
    mcp.run()

from mcp.server.fastmcp import FastMCP
import os
import platform
import datetime

# Initialize the Nexus-MCP Server
# The name here is what the AI will see as the tool provider
mcp = FastMCP("nexus-mcp")

@mcp.tool()
def get_system_info() -> str:
    """Returns basic information about the host computer."""
    sys_info = {
        "OS": platform.system(),
        "Release": platform.release(),
        "Time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return f"Nexus-MCP is running on: {sys_info}"

@mcp.tool()
def write_nexus_note(filename: str, content: str) -> str:
    """
    Creates or appends a note to a file in the 'nexus_notes' folder.
    Use this to store memories or task lists.
    """
    # Ensure a directory for notes exists
    os.makedirs("nexus_notes", exist_ok=True)
    
    path = os.path.join("nexus_notes", filename)
    with open(path, "a") as f:
        f.write(f"[{datetime.datetime.now()}] {content}\n")
    
    return f"Successfully added note to {path}"

@mcp.tool()
def list_nexus_notes() -> str:
    """Lists all files currently stored in the Nexus memory bank."""
    if not os.path.exists("nexus_notes"):
        return "Nexus memory bank is currently empty."
    
    files = os.listdir("nexus_notes")
    return "Stored notes: " + ", ".join(files)

if __name__ == "__main__":
    mcp.run()

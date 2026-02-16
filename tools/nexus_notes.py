import os
import datetime
from mcp.server.fastmcp import FastMCP

def register_note_tools(mcp: FastMCP):
    @mcp.tool()
    def write_nexus_note(filename: str, content: str) -> str:
        """Creates or appends a note to the memory bank."""
        os.makedirs("nexus_notes", exist_ok=True)
        path = os.path.join("nexus_notes", filename)
        with open(path, "a") as f:
            f.write(f"[{datetime.datetime.now()}] {content}\n")
        return f"Successfully added note to {path}"

    @mcp.tool()
    def list_nexus_notes() -> str:
        """Lists all files in the memory bank."""
        if not os.path.exists("nexus_notes"):
            return "Memory bank is empty."
        return "Stored notes: " + ", ".join(os.listdir("nexus_notes"))
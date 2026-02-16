import platform
import datetime
import psutil
import shutil
from mcp.server.fastmcp import FastMCP

def register_system_tools(mcp: FastMCP):
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
    def check_system_health() -> str:
        """Retrieves CPU, Memory, and Disk health metrics."""
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        total, used, free = shutil.disk_usage("/")
        
        report = [
            f"CPU: {cpu}%",
            f"RAM: {mem.percent}%",
            f"Disk: {(used/total)*100:.1f}% free"
        ]
        return " | ".join(report)
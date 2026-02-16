import socket
import time
from mcp.server.fastmcp import FastMCP

def register_network_tools(mcp: FastMCP):
    @mcp.tool()
    def check_connectivity(host: str = "google.com", port: int = 443, timeout: int = 3) -> str:
        """
        Tests TCP connectivity to a specific host and port.
        Useful for verifying if APIs, databases, or web services are reachable.
        """
        start_time = time.time()
        try:
            socket.setdefaulttimeout(timeout)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                result = sock.connect_ex((host, port))
                end_time = time.time()
                latency = round((end_time - start_time) * 1000, 2)
                
                if result == 0:
                    return f"✅ Connected to {host}:{port} successfully. Latency: {latency}ms"
                else:
                    return f"❌ Failed to connect to {host}:{port}. Error code: {result}"
        except Exception as e:
            return f"⚠️ Error attempting to connect to {host}: {str(e)}"

    @mcp.tool()
    def resolve_dns(hostname: str) -> str:
        """Resolves a hostname to an IP address. Useful for debugging DNS issues."""
        try:
            ip_address = socket.gethostbyname(hostname)
            return f"🌐 {hostname} resolved to {ip_address}"
        except socket.gaierror:
            return f"❌ Could not resolve hostname: {hostname}"
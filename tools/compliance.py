import os
import re
from mcp.server.fastmcp import FastMCP

# Common high-risk patterns (AWS, Slack, Generic Keys)
SECRET_PATTERNS = {
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "Generic Secret": r"(?i)(password|secret|passwd|api_key|token)[\s:=]+['\"]?([a-zA-Z0-9\-_]{8,})['\"]?",
    "Bearer Token": r"Bearer\s+[a-zA-Z0-9\-\._~+/]+=*",
}

def register_compliance_tools(mcp: FastMCP):
    @mcp.tool()
    def scan_for_secrets(directory: str = ".") -> str:
        """
        Scans files in the given directory for hardcoded secrets or unencrypted .env files.
        Essential for FinTech security compliance before pushing to git.
        """
        findings = []
        
        # 1. Check for unignored .env files
        if os.path.exists(os.path.join(directory, ".env")):
            findings.append("⚠️ CRITICAL: Unencrypted .env file found in root. Ensure this is in .gitignore!")

        # 2. Scan file contents for patterns
        for root, _, files in os.walk(directory):
            # Skip hidden git folders or virtual envs
            if any(x in root for x in [".git", "venv", "__pycache__", "node_modules"]):
                continue
                
            for file in files:
                if file.endswith((".py", ".js", ".tf", ".yaml", ".yml", ".json")):
                    path = os.path.join(root, file)
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            content = f.read()
                            for name, pattern in SECRET_PATTERNS.items():
                                if re.search(pattern, content):
                                    findings.append(f"❌ {name} potentially exposed in: {path}")
                    except Exception:
                        continue

        if not findings:
            return "✅ Compliance Scan Passed: No obvious secrets or exposed .env files detected."
        
        return "--- Compliance Audit Findings ---\n" + "\n".join(findings)
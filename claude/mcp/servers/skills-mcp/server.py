"""
MCP Server for Claude Code Learning System Skills.

Implements the Model Context Protocol pattern for 98.7% token reduction:
- Exposes skills as importable Python modules
- Executes code locally in sandboxed environment
- Returns only filtered results to agent

Based on Anthropic's MCP Code Execution pattern:
https://www.anthropic.com/engineering/mcp-code-execution
"""

import sys
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict

# Add project root to path
PROJECT_ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

from skills.execution.sandboxed_executor import SandboxedExecutor, SandboxConfig
from skills.execution.code_executor import ExecutionResult


@dataclass
class MCPRequest:
    """MCP execution request."""
    code: str
    context: Optional[Dict[str, Any]] = None
    timeout: Optional[int] = None


@dataclass
class MCPResponse:
    """MCP execution response."""
    success: bool
    result: Any = None
    error: Optional[str] = None
    stdout: str = ""
    stderr: str = ""
    duration: float = 0.0
    tokens_saved: Optional[int] = None


class MCPServer:
    """
    MCP Server for skill execution.

    Provides code execution environment where agents can:
    1. Import skills as Python modules
    2. Process data locally
    3. Filter/transform results
    4. Return only relevant data

    Example usage:
        server = MCPServer(workspace_dir="/path/to/project")

        request = MCPRequest(code='''
from skills.code_analysis import analyze_codebase
from skills.common.filters import ResultFilter

# Analyze codebase
files = analyze_codebase("src/")

# Filter locally (98.7% token savings!)
nav_files = ResultFilter.search(files, "navigation", ["path"])
result = ResultFilter.top_n_by_field(nav_files, "complexity", 5)
        ''')

        response = server.execute(request)
        print(response.result)  # Only 5 files instead of 10,000!
    """

    def __init__(
        self,
        workspace_dir: Optional[str] = None,
        sandbox_config: Optional[SandboxConfig] = None
    ):
        """
        Initialize MCP server.

        Args:
            workspace_dir: Project workspace directory
            sandbox_config: Sandbox configuration (optional)
        """
        self.workspace_dir = workspace_dir or os.getcwd()
        self.executor = SandboxedExecutor(
            workspace_dir=self.workspace_dir,
            config=sandbox_config
        )

    def execute(self, request: MCPRequest) -> MCPResponse:
        """
        Execute code request.

        Args:
            request: MCP execution request

        Returns:
            MCPResponse with results
        """
        # Execute in sandbox
        result = self.executor.execute(
            code=request.code,
            context=request.context,
            timeout=request.timeout
        )

        # Convert ExecutionResult to MCPResponse
        return self._convert_result(result)

    def _convert_result(self, result: ExecutionResult) -> MCPResponse:
        """Convert ExecutionResult to MCPResponse."""
        return MCPResponse(
            success=result.success,
            result=result.output,
            error=result.error,
            stdout=result.stdout,
            stderr=result.stderr,
            duration=result.duration,
            tokens_saved=result.tokens_saved
        )

    def execute_json(self, request_json: str) -> str:
        """
        Execute code request from JSON.

        Args:
            request_json: JSON-encoded MCPRequest

        Returns:
            JSON-encoded MCPResponse
        """
        try:
            # Parse request
            data = json.loads(request_json)
            request = MCPRequest(**data)

            # Execute
            response = self.execute(request)

            # Return JSON
            return json.dumps(asdict(response), indent=2)

        except Exception as e:
            error_response = MCPResponse(
                success=False,
                error=f"Server error: {str(e)}"
            )
            return json.dumps(asdict(error_response), indent=2)

    def get_available_skills(self) -> List[Dict[str, Any]]:
        """
        Get list of available skills.

        Returns:
            List of skill metadata
        """
        skills_dir = Path(PROJECT_ROOT) / "skills"
        available_skills = []

        for skill_path in skills_dir.iterdir():
            if not skill_path.is_dir():
                continue

            skill_md = skill_path / "SKILL.md"
            if not skill_md.exists():
                continue

            # Parse SKILL.md for metadata
            try:
                with open(skill_md) as f:
                    content = f.read()

                    # Extract YAML frontmatter (basic parsing)
                    if content.startswith("---"):
                        parts = content.split("---", 2)
                        if len(parts) >= 3:
                            # Simple YAML parsing (just for demo)
                            metadata = {
                                "name": skill_path.name,
                                "path": f"skills.{skill_path.name}",
                                "description": "See SKILL.md for details"
                            }
                            available_skills.append(metadata)

            except Exception:
                pass

        return available_skills

    def get_stats(self) -> Dict[str, Any]:
        """Get server statistics."""
        return {
            "workspace_dir": self.workspace_dir,
            "sandbox_stats": self.executor.get_stats(),
            "available_skills": len(self.get_available_skills())
        }


def start_stdio_server():
    """
    Start MCP server in STDIO mode.

    This is the standard MCP server mode where:
    - Requests come via stdin (JSON)
    - Responses go via stdout (JSON)
    - Agent communicates via standard I/O
    """
    server = MCPServer()

    print(json.dumps({
        "status": "ready",
        "server": "claude-code-skills-mcp",
        "version": "1.0.0",
        "capabilities": {
            "code_execution": True,
            "skill_imports": True,
            "sandboxed": True,
            "token_optimization": True
        }
    }), flush=True)

    # Process requests from stdin
    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue

            try:
                # Parse request
                request_data = json.loads(line)

                if request_data.get("type") == "execute":
                    # Execute code
                    request = MCPRequest(
                        code=request_data["code"],
                        context=request_data.get("context"),
                        timeout=request_data.get("timeout")
                    )
                    response = server.execute(request)
                    print(json.dumps(asdict(response)), flush=True)

                elif request_data.get("type") == "list_skills":
                    # List available skills
                    skills = server.get_available_skills()
                    print(json.dumps({"skills": skills}), flush=True)

                elif request_data.get("type") == "stats":
                    # Get server stats
                    stats = server.get_stats()
                    print(json.dumps(stats), flush=True)

                elif request_data.get("type") == "shutdown":
                    # Shutdown server
                    print(json.dumps({"status": "shutdown"}), flush=True)
                    break

                else:
                    print(json.dumps({
                        "error": f"Unknown request type: {request_data.get('type')}"
                    }), flush=True)

            except Exception as e:
                print(json.dumps({
                    "error": f"Request processing error: {str(e)}"
                }), flush=True)

    except KeyboardInterrupt:
        print(json.dumps({"status": "shutdown"}), flush=True)


def start_http_server(port: int = 8080):
    """
    Start MCP server in HTTP mode (for development/testing).

    Args:
        port: Port to listen on
    """
    try:
        from http.server import HTTPServer, BaseHTTPRequestHandler
    except ImportError:
        print("HTTP server requires Python 3.x", file=sys.stderr)
        sys.exit(1)

    server = MCPServer()

    class MCPRequestHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')

            response_json = server.execute_json(body)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(response_json.encode('utf-8'))

        def log_message(self, format, *args):
            # Suppress HTTP logs
            pass

    httpd = HTTPServer(('localhost', port), MCPRequestHandler)
    print(f"MCP server listening on http://localhost:{port}", file=sys.stderr)
    print(f"Send POST requests with JSON body: {{'code': '...', 'context': {{...}}}}", file=sys.stderr)
    httpd.serve_forever()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MCP Server for Claude Code Skills")
    parser.add_argument(
        "--mode",
        choices=["stdio", "http"],
        default="stdio",
        help="Server mode (stdio for Claude Desktop, http for testing)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Port for HTTP mode"
    )
    parser.add_argument(
        "--workspace",
        type=str,
        default=None,
        help="Workspace directory"
    )

    args = parser.parse_args()

    if args.mode == "stdio":
        start_stdio_server()
    else:
        start_http_server(port=args.port)

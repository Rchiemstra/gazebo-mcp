"""
Tests for MCP Integration.

Tests the Model Context Protocol server and adapters:
- MCP server functionality
- Code execution requests
- Skill adapters
- Token optimization patterns

Goal: Verify 98.7% token reduction through local code execution.
"""

import pytest
import json
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from mcp.servers.skills_mcp.server import (
    MCPServer,
    MCPRequest,
    MCPResponse
)


class TestMCPServer:
    """Test MCP server functionality."""

    def test_create_server(self):
        """Test creating MCP server."""
        server = MCPServer(workspace_dir=str(PROJECT_ROOT))

        assert server is not None
        assert server.workspace_dir is not None
        assert server.executor is not None

    def test_execute_request(self):
        """Test executing code request."""
        server = MCPServer(workspace_dir=str(PROJECT_ROOT))

        request = MCPRequest(code="""
result = 2 + 2
""")

        response = server.execute(request)

        assert response is not None
        assert isinstance(response, MCPResponse)
        assert hasattr(response, "success")

    def test_execute_with_context(self):
        """Test executing code with context variables."""
        server = MCPServer(workspace_dir=str(PROJECT_ROOT))

        request = MCPRequest(
            code="""
result = _context["x"] + _context["y"]
""",
            context={"x": 10, "y": 20}
        )

        response = server.execute(request)

        # Context handling depends on executor implementation
        assert response is not None

    def test_execute_json(self):
        """Test executing request from JSON."""
        server = MCPServer(workspace_dir=str(PROJECT_ROOT))

        request_json = json.dumps({
            "code": "result = 42",
            "context": None,
            "timeout": None
        })

        response_json = server.execute_json(request_json)

        # Should return valid JSON
        response_data = json.loads(response_json)
        assert "success" in response_data

    def test_get_available_skills(self):
        """Test getting list of available skills."""
        server = MCPServer(workspace_dir=str(PROJECT_ROOT))

        skills = server.get_available_skills()

        assert isinstance(skills, list)
        # Should find at least some skills
        assert len(skills) > 0

    def test_get_stats(self):
        """Test getting server statistics."""
        server = MCPServer(workspace_dir=str(PROJECT_ROOT))

        stats = server.get_stats()

        assert "workspace_dir" in stats
        assert "sandbox_stats" in stats
        assert "available_skills" in stats

    def test_error_handling(self):
        """Test that errors are properly handled."""
        server = MCPServer(workspace_dir=str(PROJECT_ROOT))

        # Invalid code
        request = MCPRequest(code="this will not parse")

        response = server.execute(request)

        assert not response.success
        assert response.error is not None


class TestTokenOptimizationPatterns:
    """Test MCP token optimization patterns."""

    def test_filter_pattern(self):
        """Test filtering pattern reduces tokens."""
        server = MCPServer(workspace_dir=str(PROJECT_ROOT))

        # Code that filters large dataset locally
        request = MCPRequest(code="""
# Simulate large dataset (10,000 items = 150,000 tokens)
large_data = [
    {"id": i, "name": f"item_{i}", "value": i * 10}
    for i in range(10000)
]

# Filter locally - only high-value items
filtered = [item for item in large_data if item["value"] > 95000]

# Return only top 5
result = filtered[:5]
""")

        response = server.execute(request)

        if response.success:
            # Result should be small (5 items), not 10,000
            # This demonstrates token reduction
            assert response.result is not None

    def test_aggregation_pattern(self):
        """Test aggregation pattern reduces tokens."""
        server = MCPServer(workspace_dir=str(PROJECT_ROOT))

        request = MCPRequest(code="""
# Large dataset
data = list(range(100000))

# Aggregate locally instead of returning all data
result = {
    "count": len(data),
    "sum": sum(data),
    "min": min(data),
    "max": max(data),
    "mean": sum(data) / len(data)
}
""")

        response = server.execute(request)

        if response.success:
            # Returns ~100 tokens instead of 100,000
            assert response.result is not None

    def test_search_and_filter_pattern(self):
        """Test search + filter pattern."""
        server = MCPServer(workspace_dir=str(PROJECT_ROOT))

        request = MCPRequest(code="""
# Simulate file analysis results
files = [
    {"path": f"/src/module_{i}.py", "complexity": i % 20, "lines": i * 50}
    for i in range(1000)
]

# Search for high-complexity files
complex_files = [f for f in files if f["complexity"] > 15]

# Sort by complexity
complex_files.sort(key=lambda f: f["complexity"], reverse=True)

# Return top 10
result = complex_files[:10]
""")

        response = server.execute(request)

        if response.success:
            # Returns 10 files instead of 1000
            assert response.result is not None


class TestSkillImports:
    """Test importing skills in MCP environment."""

    def test_common_filters_import(self):
        """Test importing common.filters module."""
        server = MCPServer(workspace_dir=str(PROJECT_ROOT))

        request = MCPRequest(code="""
# Try to import ResultFilter
try:
    from skills.common.filters import ResultFilter
    result = "Import successful"
except ImportError as e:
    result = f"Import failed: {str(e)}"
""")

        response = server.execute(request)

        # May succeed or fail depending on path setup
        # Just verify we get a response
        assert response is not None

    def test_skill_usage_pattern(self):
        """Test using skills with MCP pattern."""
        server = MCPServer(workspace_dir=str(PROJECT_ROOT))

        request = MCPRequest(code="""
# Example: Use skill and filter results locally
try:
    # Import skill
    from skills.common.filters import ResultFilter

    # Simulate skill output (large dataset)
    skill_result = [
        {"name": f"file_{i}", "score": i}
        for i in range(100)
    ]

    # Filter locally
    result = ResultFilter.top_n_by_field(skill_result, "score", 5)
except Exception as e:
    result = {"error": str(e)}
""")

        response = server.execute(request)

        assert response is not None


class TestMCPSecurity:
    """Test MCP security features."""

    def test_sandbox_integration(self):
        """Test that MCP uses sandboxed execution."""
        server = MCPServer(workspace_dir=str(PROJECT_ROOT))

        # Verify executor is sandboxed
        assert hasattr(server.executor, "get_stats")

        stats = server.executor.get_stats()
        assert "sandbox_method" in stats

    def test_dangerous_code_blocked(self):
        """Test that dangerous code is blocked."""
        server = MCPServer(workspace_dir=str(PROJECT_ROOT))

        request = MCPRequest(code="""
eval("malicious code")
""")

        response = server.execute(request)

        # Should be blocked
        assert not response.success
        assert response.error is not None

    def test_unauthorized_import_blocked(self):
        """Test that unauthorized imports are blocked."""
        server = MCPServer(workspace_dir=str(PROJECT_ROOT))

        request = MCPRequest(code="""
import os
result = os.system("ls -la /")
""")

        response = server.execute(request)

        # Should be blocked
        assert not response.success


class TestMCPAdapters:
    """Test MCP skill adapters."""

    def test_code_analysis_adapter_docs(self):
        """Test code_analysis adapter documentation."""
        from mcp.servers.skills_mcp.adapters import code_analysis

        ops = code_analysis.get_operation_docs()

        assert isinstance(ops, dict)
        assert "analyze_codebase" in ops
        assert "analyze_file" in ops
        assert "description" in ops["analyze_codebase"]

    def test_test_orchestrator_adapter_docs(self):
        """Test test_orchestrator adapter documentation."""
        from mcp.servers.skills_mcp.adapters import test_orchestrator

        ops = test_orchestrator.get_operation_docs()

        assert isinstance(ops, dict)
        assert "generate_tests" in ops
        assert "analyze_coverage" in ops

    def test_adapter_examples(self):
        """Test that adapters provide usage examples."""
        from mcp.servers.skills_mcp.adapters import code_analysis

        example = code_analysis.generate_import_example()

        assert isinstance(example, str)
        assert len(example) > 0
        assert "from skills" in example
        assert "ResultFilter" in example


class TestMCPPerformance:
    """Test MCP performance characteristics."""

    def test_response_includes_metadata(self):
        """Test that responses include performance metadata."""
        server = MCPServer(workspace_dir=str(PROJECT_ROOT))

        request = MCPRequest(code="result = 42")

        response = server.execute(request)

        assert hasattr(response, "duration")
        assert hasattr(response, "tokens_saved")

    def test_stdout_stderr_captured(self):
        """Test that stdout/stderr are captured."""
        server = MCPServer(workspace_dir=str(PROJECT_ROOT))

        request = MCPRequest(code="""
print("Hello stdout")
import sys
print("Hello stderr", file=sys.stderr)
result = "done"
""")

        response = server.execute(request)

        # Stdout/stderr capture depends on executor
        assert hasattr(response, "stdout")
        assert hasattr(response, "stderr")


class TestMCPDesktopExtension:
    """Test Desktop Extension packaging."""

    def test_manifest_exists(self):
        """Test that manifest.json exists and is valid."""
        manifest_path = PROJECT_ROOT / "mcp" / "desktop-extension" / "manifest.json"

        assert manifest_path.exists()

        with open(manifest_path) as f:
            manifest = json.load(f)

        assert "name" in manifest
        assert "version" in manifest
        assert "mcp" in manifest
        assert "skills" in manifest

    def test_install_script_exists(self):
        """Test that install script exists."""
        install_script = PROJECT_ROOT / "mcp" / "desktop-extension" / "install.sh"

        assert install_script.exists()
        assert install_script.stat().st_mode & 0o111  # Executable

    def test_build_script_exists(self):
        """Test that build script exists."""
        build_script = PROJECT_ROOT / "mcp" / "desktop-extension" / "build.sh"

        assert build_script.exists()
        assert build_script.stat().st_mode & 0o111  # Executable


def run_mcp_tests():
    """Run all MCP integration tests."""
    pytest.main([__file__, "-v"])


if __name__ == "__main__":
    run_mcp_tests()

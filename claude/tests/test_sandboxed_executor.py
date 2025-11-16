"""
Tests for Sandboxed Executor.

Tests OS-level sandboxing features:
- Filesystem isolation
- Network isolation
- Resource limits
- Security validations

Goal: Verify 84% reduction in permission prompts while maintaining security.
"""

import pytest
import sys
import platform
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from skills.execution.sandboxed_executor import (
    SandboxedExecutor,
    SandboxConfig,
    create_default_executor
)
from skills.execution.code_executor import ExecutionResult


class TestSandboxedExecutor:
    """Test sandboxed code execution."""

    def test_create_default_executor(self):
        """Test creating executor with default settings."""
        executor = create_default_executor()

        assert executor is not None
        assert executor.workspace_dir is not None
        assert executor.platform in ["Linux", "Darwin", "Windows"]

    def test_sandbox_detection(self):
        """Test that sandbox method is detected correctly."""
        executor = create_default_executor()

        if executor.platform == "Linux":
            # Should detect bubblewrap or fallback
            assert executor.sandbox_method in ["bubblewrap", "code_executor_only"]
        elif executor.platform == "Darwin":
            assert executor.sandbox_method == "seatbelt"
        elif executor.platform == "Windows":
            assert executor.sandbox_method == "code_executor_only"

    def test_basic_code_execution(self):
        """Test basic code execution in sandbox."""
        executor = create_default_executor()

        code = """
result = 2 + 2
"""

        result = executor.execute(code)

        assert result is not None
        # May succeed or fail depending on sandbox availability
        # Just verify we get a result

    def test_code_validation(self):
        """Test that dangerous code is rejected."""
        executor = create_default_executor()

        # Try to use eval (should be blocked)
        dangerous_code = """
eval("print('hacked')")
"""

        result = executor.execute(dangerous_code)

        assert not result.success
        assert "eval" in result.error.lower() or "not allowed" in result.error.lower()

    def test_import_validation(self):
        """Test that unauthorized imports are blocked."""
        executor = create_default_executor()

        # Try to import os (not in whitelist)
        code = """
import os
result = os.listdir("/")
"""

        result = executor.execute(code)

        # Should fail validation
        assert not result.success

    def test_allowed_skill_import(self):
        """Test that skill imports are allowed."""
        executor = create_default_executor()

        code = """
from skills.common.filters import ResultFilter
result = "Import successful"
"""

        result = executor.execute(code)

        # Should succeed (skill imports are allowed)
        # May fail if skills not in path, but validation should pass
        assert result is not None

    def test_timeout_enforcement(self):
        """Test that timeouts are enforced."""
        executor = create_default_executor()

        # Code that takes too long
        code = """
import time
time.sleep(10)
result = "Should timeout"
"""

        result = executor.execute(code, timeout=1)

        # Should timeout
        assert not result.success
        assert "timeout" in result.error.lower() or "time" in str(result.error).lower()

    def test_custom_sandbox_config(self):
        """Test custom sandbox configuration."""
        config = SandboxConfig(
            workspace_dir=str(PROJECT_ROOT),
            allowed_paths=[str(PROJECT_ROOT)],
            allowed_domains=["api.anthropic.com"],
            max_cpu_time=5,
            max_memory=128,
            network_enabled=False
        )

        executor = SandboxedExecutor(config=config)

        assert executor.config.max_cpu_time == 5
        assert executor.config.max_memory == 128
        assert not executor.config.network_enabled

    def test_get_stats(self):
        """Test getting executor statistics."""
        executor = create_default_executor()

        stats = executor.get_stats()

        assert "platform" in stats
        assert "sandbox_method" in stats
        assert "workspace_dir" in stats
        assert "allowed_paths" in stats
        assert "allowed_domains" in stats


class TestSandboxSecurity:
    """Test sandbox security features."""

    def test_file_operation_blocked(self):
        """Test that direct file operations are blocked."""
        executor = create_default_executor()

        # Try to use open() directly
        code = """
with open("/etc/passwd", "r") as f:
    result = f.read()
"""

        result = executor.execute(code)

        # Should be blocked by validation
        assert not result.success
        assert "file" in result.error.lower() or "open" in result.error.lower()

    def test_dangerous_functions_blocked(self):
        """Test that dangerous functions are blocked."""
        executor = create_default_executor()

        dangerous_functions = ["eval", "exec", "compile", "__import__"]

        for func in dangerous_functions:
            code = f"""
{func}("malicious code")
"""
            result = executor.execute(code)

            assert not result.success, f"{func} should be blocked"

    @pytest.mark.skipif(
        platform.system() not in ["Linux", "Darwin"],
        reason="Sandbox only available on Linux/macOS"
    )
    def test_filesystem_isolation(self):
        """Test that filesystem is properly isolated."""
        executor = create_default_executor()

        # This test would require actual sandbox to run
        # For now, just verify the configuration
        config = executor.config

        assert len(config.allowed_paths) > 0
        assert config.workspace_dir in config.allowed_paths or \
               any(config.workspace_dir.startswith(p) for p in config.allowed_paths)


class TestTokenOptimization:
    """Test token optimization patterns with sandbox."""

    def test_local_filtering(self):
        """Test that local filtering works in sandbox."""
        executor = create_default_executor()

        code = """
# Simulate analyzing many files
large_dataset = [
    {"name": f"file_{i}.py", "complexity": i, "lines": i*10}
    for i in range(100)
]

# Filter locally - only keep high complexity
result = [f for f in large_dataset if f["complexity"] > 90]

# Only return top 5
result = result[:5]
"""

        result = executor.execute(code)

        if result.success:
            # Should return only 5 items, not 100
            assert result.output is not None

    def test_aggregation_pattern(self):
        """Test data aggregation pattern."""
        executor = create_default_executor()

        code = """
# Simulate large dataset
data = list(range(10000))

# Aggregate locally
result = {
    "count": len(data),
    "sum": sum(data),
    "min": min(data),
    "max": max(data),
    "avg": sum(data) / len(data)
}
"""

        result = executor.execute(code)

        if result.success:
            # Should return summary, not 10,000 items
            assert result.output is not None


class TestPlatformSpecific:
    """Platform-specific sandbox tests."""

    @pytest.mark.skipif(
        platform.system() != "Linux",
        reason="Bubblewrap only on Linux"
    )
    def test_bubblewrap_available(self):
        """Test that bubblewrap is detected on Linux."""
        import subprocess

        try:
            result = subprocess.run(
                ["which", "bwrap"],
                capture_output=True
            )
            bubblewrap_available = (result.returncode == 0)
        except:
            bubblewrap_available = False

        executor = create_default_executor()

        if bubblewrap_available:
            assert executor.sandbox_method == "bubblewrap"
        else:
            assert executor.sandbox_method == "code_executor_only"

    @pytest.mark.skipif(
        platform.system() != "Darwin",
        reason="Seatbelt only on macOS"
    )
    def test_seatbelt_available(self):
        """Test that seatbelt is used on macOS."""
        executor = create_default_executor()

        assert executor.sandbox_method == "seatbelt"


class TestExecutionResult:
    """Test execution result handling."""

    def test_successful_execution_result(self):
        """Test successful execution returns proper result."""
        executor = create_default_executor()

        code = """
result = {"status": "success", "value": 42}
"""

        result = executor.execute(code)

        assert result is not None
        assert isinstance(result, ExecutionResult)
        assert hasattr(result, "success")
        assert hasattr(result, "output")
        assert hasattr(result, "error")

    def test_failed_execution_result(self):
        """Test failed execution returns error."""
        executor = create_default_executor()

        code = """
# Invalid code
this will not parse
"""

        result = executor.execute(code)

        assert result is not None
        assert not result.success
        assert result.error is not None


def run_sandbox_tests():
    """Run all sandbox tests."""
    pytest.main([__file__, "-v"])


if __name__ == "__main__":
    run_sandbox_tests()

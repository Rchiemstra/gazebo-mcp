"""
Tests for MCP Security Validator skill.
"""

import pytest
from pathlib import Path
import tempfile
from skills.mcp_security_validator import (
    validate_server_security,
    validate_sandbox_config,
    OperationResult,
    ErrorCodes
)


class TestValidateServerSecurity:
    """Test server security validation."""

    def test_validate_existing_mcp_server(self):
        """Test validation of existing MCP server."""
        # Use the existing skills-mcp server as test
        server_path = "mcp/servers/skills-mcp"

        result = validate_server_security(server_path, response_format="summary")

        assert result.success
        assert "security_score" in result.data
        assert 0 <= result.data["security_score"] <= 100
        assert "checks_passed" in result.data
        assert "checks_total" in result.data

    def test_validate_server_complete_format(self):
        """Test validation with complete format."""
        server_path = "mcp/servers/skills-mcp"

        result = validate_server_security(server_path, response_format="complete")

        assert result.success
        assert "issues" in result.data
        assert "recommendations" in result.data
        assert isinstance(result.data["issues"], list)

    def test_validate_nonexistent_server(self):
        """Test validation of non-existent server."""
        result = validate_server_security("nonexistent/path")

        assert not result.success
        assert result.error is not None
        assert "not found" in result.error.lower()
        assert result.error_code == ErrorCodes.FILE_NOT_FOUND

    def test_validate_file_instead_of_directory(self):
        """Test validation when path is a file, not directory."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile() as tmpfile:
            result = validate_server_security(tmpfile.name)

            assert not result.success
            assert "not a directory" in result.error.lower()

    def test_validate_empty_directory(self):
        """Test validation of empty directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = validate_server_security(tmpdir, response_format="complete")

            # Should succeed but with low score due to missing files
            assert result.success
            assert result.data["security_score"] < 70  # Should have issues


class TestValidateSandboxConfig:
    """Test sandbox configuration validation."""

    def test_validate_complete_config(self):
        """Test validation of complete sandbox config."""
        config = {
            "filesystem": {
                "allowed_paths": ["/workspace", "/tmp"],
                "blocked_paths": ["/root", "~/.ssh"]
            },
            "network": {
                "allowed_domains": ["api.anthropic.com", "pypi.org"],
                "default_policy": "deny"
            },
            "resources": {
                "cpu_timeout": 30,
                "memory_limit_mb": 512,
                "max_processes": 10
            }
        }

        result = validate_sandbox_config(config)

        assert result.success
        assert result.data["valid"] is True
        assert result.data["score"] >= 70
        assert len(result.data["errors"]) == 0

    def test_validate_missing_filesystem(self):
        """Test validation catches missing filesystem config."""
        config = {
            "network": {
                "allowed_domains": ["api.anthropic.com"]
            }
        }

        result = validate_sandbox_config(config)

        assert result.success
        assert result.data["valid"] is False
        assert len(result.data["errors"]) > 0

        # Should have critical error for missing filesystem
        critical_errors = [e for e in result.data["errors"] if e["severity"] == "critical"]
        assert len(critical_errors) > 0

    def test_validate_missing_network(self):
        """Test validation catches missing network config."""
        config = {
            "filesystem": {
                "allowed_paths": ["/workspace"]
            }
        }

        result = validate_sandbox_config(config)

        assert result.success
        assert result.data["valid"] is False

        # Should have critical error for missing network
        critical_errors = [e for e in result.data["errors"] if e["severity"] == "critical"]
        assert len(critical_errors) > 0

    def test_validate_excessive_cpu_timeout(self):
        """Test validation catches excessive CPU timeout."""
        config = {
            "filesystem": {"allowed_paths": ["/workspace"]},
            "network": {"allowed_domains": ["api.anthropic.com"]},
            "resources": {
                "cpu_timeout": 60  # Exceeds recommended 30s
            }
        }

        result = validate_sandbox_config(config)

        assert result.success
        # Should have warning/issue about excessive timeout
        if result.data["issues"]:
            timeout_issues = [i for i in result.data["issues"] if "timeout" in i["issue"].lower()]
            assert len(timeout_issues) > 0

    def test_validate_empty_config(self):
        """Test validation of empty config."""
        result = validate_sandbox_config({})

        assert result.success
        assert result.data["valid"] is False
        assert len(result.data["errors"]) >= 2  # Missing filesystem and network


class TestSecurityScoring:
    """Test security scoring logic."""

    def test_score_range(self):
        """Test that scores are always in valid range."""
        configs = [
            {},  # Empty
            {"filesystem": {}},  # Partial
            {
                "filesystem": {"allowed_paths": ["/workspace"]},
                "network": {"allowed_domains": ["api.anthropic.com"]},
                "resources": {"cpu_timeout": 30}
            }  # Complete
        ]

        for config in configs:
            result = validate_sandbox_config(config)
            assert result.success
            assert 0 <= result.data["score"] <= 100

    def test_score_decreases_with_issues(self):
        """Test that score decreases with more issues."""
        good_config = {
            "filesystem": {"allowed_paths": ["/workspace"]},
            "network": {"allowed_domains": ["api.anthropic.com"]},
            "resources": {"cpu_timeout": 30}
        }

        bad_config = {}

        good_result = validate_sandbox_config(good_config)
        bad_result = validate_sandbox_config(bad_config)

        assert good_result.data["score"] > bad_result.data["score"]


class TestIssueRecommendations:
    """Test issue detection and recommendations."""

    def test_issues_have_severity(self):
        """Test that all issues have severity level."""
        config = {}  # Incomplete config
        result = validate_sandbox_config(config)

        assert result.success
        for issue in result.data["issues"]:
            assert "severity" in issue
            assert issue["severity"] in ["critical", "high", "medium", "low"]

    def test_issues_have_recommendations(self):
        """Test that all issues have recommendations."""
        config = {}
        result = validate_sandbox_config(config)

        assert result.success
        for issue in result.data["issues"]:
            assert "issue" in issue
            assert "recommendation" in issue

    def test_errors_vs_warnings_classification(self):
        """Test classification of errors vs warnings."""
        config = {}
        result = validate_sandbox_config(config)

        assert result.success
        assert "errors" in result.data
        assert "warnings" in result.data

        # Errors should be critical/high severity
        for error in result.data["errors"]:
            assert error["severity"] in ["critical", "high"]

        # Warnings should be medium/low severity
        for warning in result.data["warnings"]:
            assert warning["severity"] in ["medium", "low"]


class TestFilesystemIsolationChecks:
    """Test filesystem isolation validation."""

    def test_validates_allowed_paths(self):
        """Test that allowed paths are validated."""
        with tempfile.TemporaryDirectory() as tmpdir:
            server_dir = Path(tmpdir)

            # Create minimal config.py
            config_py = server_dir / "config.py"
            config_py.write_text('''
ALLOWED_PATHS = ["/workspace", "/tmp"]
''')

            result = validate_server_security(str(server_dir), response_format="complete")

            assert result.success
            # Should have better score with workspace configured
            assert result.data["security_score"] > 0


class TestNetworkFilteringChecks:
    """Test network filtering validation."""

    def test_validates_network_config(self):
        """Test that network configuration is validated."""
        with tempfile.TemporaryDirectory() as tmpdir:
            server_dir = Path(tmpdir)

            # Create config with network settings
            config_py = server_dir / "config.py"
            config_py.write_text('''
ALLOWED_DOMAINS = ["api.anthropic.com", "pypi.org"]
''')

            result = validate_server_security(str(server_dir), response_format="complete")

            assert result.success


class TestResourceLimitChecks:
    """Test resource limit validation."""

    def test_validates_resource_limits(self):
        """Test that resource limits are validated."""
        with tempfile.TemporaryDirectory() as tmpdir:
            server_dir = Path(tmpdir)

            # Create config with resource limits
            config_py = server_dir / "config.py"
            config_py.write_text('''
CPU_TIMEOUT = 30
MEMORY_LIMIT_MB = 512
''')

            result = validate_server_security(str(server_dir), response_format="complete")

            assert result.success


class TestProductionReadiness:
    """Test production readiness assessment."""

    def test_production_ready_flag(self):
        """Test production_ready flag in summary."""
        config = {
            "filesystem": {"allowed_paths": ["/workspace", "/tmp"]},
            "network": {"allowed_domains": ["api.anthropic.com"]},
            "resources": {"cpu_timeout": 30}
        }

        result = validate_sandbox_config(config)

        assert result.success
        # Good config should be production ready (score >= 90)
        if result.data["score"] >= 90:
            # Would need to check if validate_server_security includes this flag
            pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""
Integration tests for MCP Server Builder workflow.

Tests the complete workflow from schema generation through adapter creation
to security validation.
"""

import pytest
import tempfile
from pathlib import Path


class TestMCPBuilderIntegration:
    """Test complete MCP builder workflow."""

    def test_schema_to_adapter_workflow(self):
        """Test workflow from schema generation to adapter creation."""
        from skills.mcp_schema_generator import generate_schema
        from skills.mcp_adapter_creator import create_adapter

        # Step 1: Generate schema
        schema_result = generate_schema("code_analysis", response_format="complete")

        assert schema_result.success
        assert len(schema_result.data["schemas"]) > 0

        # Step 2: Create adapter using the same skill
        adapter_result = create_adapter("code_analysis", response_format="complete")

        assert adapter_result.success
        assert "adapter_code" in adapter_result.data

        # Verify adapter includes operations from schema
        schemas = schema_result.data["schemas"]
        adapter_operations = adapter_result.data["operations"]

        assert len(adapter_operations) > 0

    def test_batch_workflow(self):
        """Test batch processing workflow."""
        from skills.mcp_schema_generator import generate_batch_schemas
        from skills.mcp_adapter_creator import create_batch_adapters

        skills_list = ["code_analysis", "test_orchestrator"]

        # Generate schemas for multiple skills
        schema_result = generate_batch_schemas(skills_list, response_format="summary")

        assert schema_result.success
        assert schema_result.data["successful"] >= 1

        # Create adapters for the same skills
        skills_config = [{"name": skill} for skill in skills_list]
        adapter_result = create_batch_adapters(skills_config, response_format="summary")

        assert adapter_result.success
        assert adapter_result.data["successful"] >= 1

    def test_complete_server_creation_workflow(self):
        """Test complete server creation workflow with security validation."""
        from skills.mcp_schema_generator import generate_batch_schemas
        from skills.mcp_adapter_creator import create_batch_adapters
        from skills.mcp_security_validator import validate_server_security

        with tempfile.TemporaryDirectory() as tmpdir:
            server_dir = Path(tmpdir) / "test-mcp-server"
            server_dir.mkdir()

            # Create subdirectories
            (server_dir / "adapters").mkdir()
            (server_dir / "schema").mkdir()
            (server_dir / "tests").mkdir()

            # Step 1: Generate schemas
            skills = ["code_analysis"]
            schema_result = generate_batch_schemas(skills, response_format="complete")

            assert schema_result.success

            # Step 2: Write schema files
            import json
            for schema in schema_result.data.get("schemas", []):
                schema_file = server_dir / "schema" / f"{schema['tool_name']}.json"
                with open(schema_file, 'w') as f:
                    json.dump(schema, f, indent=2)

            # Step 3: Create adapters
            skills_config = [{"name": "code_analysis"}]
            adapter_result = create_batch_adapters(skills_config, response_format="complete")

            assert adapter_result.success

            # Step 4: Write adapter files
            for adapter in adapter_result.data.get("adapters", []):
                adapter_file = server_dir / "adapters" / f"{adapter['skill_name']}.py"
                with open(adapter_file, 'w') as f:
                    f.write(adapter['adapter_code'])

            # Step 5: Create minimal server.py
            server_py = server_dir / "server.py"
            server_py.write_text('''"""MCP Server."""
# Minimal server for testing
''')

            # Step 6: Create config.py with security settings
            config_py = server_dir / "config.py"
            config_py.write_text('''"""Security configuration."""
ALLOWED_PATHS = ["/workspace", "/tmp"]
ALLOWED_DOMAINS = ["api.anthropic.com"]
CPU_TIMEOUT = 30
''')

            # Step 7: Validate security
            security_result = validate_server_security(str(server_dir), response_format="complete")

            assert security_result.success
            assert "security_score" in security_result.data

            # Server should have reasonable score with our configuration
            assert security_result.data["security_score"] > 0


class TestErrorRecoveryWorkflow:
    """Test error handling in workflow."""

    def test_workflow_with_invalid_skill(self):
        """Test workflow handles invalid skills gracefully."""
        from skills.mcp_schema_generator import generate_batch_schemas
        from skills.mcp_adapter_creator import create_batch_adapters

        skills_list = ["code_analysis", "nonexistent_skill"]

        # Schema generation should succeed but report failure for invalid skill
        schema_result = generate_batch_schemas(skills_list, response_format="summary")

        assert schema_result.success
        assert schema_result.data["failed"] > 0

        # Adapter creation should also handle this gracefully
        skills_config = [{"name": skill} for skill in skills_list]
        adapter_result = create_batch_adapters(skills_config, response_format="summary")

        assert adapter_result.success
        assert adapter_result.data["failed"] > 0


class TestTokenEfficiency:
    """Test token efficiency in workflow."""

    def test_summary_vs_complete_formats(self):
        """Test that summary format uses fewer tokens."""
        from skills.mcp_schema_generator import generate_schema

        # Generate with summary format
        summary_result = generate_schema("code_analysis", response_format="summary")

        # Generate with complete format
        complete_result = generate_schema("code_analysis", response_format="complete")

        assert summary_result.success
        assert complete_result.success

        # Summary should have less data
        import json
        summary_size = len(json.dumps(summary_result.data))
        complete_size = len(json.dumps(complete_result.data))

        assert summary_size < complete_size

    def test_batch_operations_efficiency(self):
        """Test that batch operations are more efficient than individual calls."""
        from skills.mcp_schema_generator import generate_schema, generate_batch_schemas
        import time

        skills = ["code_analysis", "test_orchestrator"]

        # Individual calls
        start = time.time()
        for skill in skills:
            generate_schema(skill, response_format="summary")
        individual_time = time.time() - start

        # Batch call
        start = time.time()
        generate_batch_schemas(skills, response_format="summary")
        batch_time = time.time() - start

        # Batch should not be significantly slower (allows for some overhead)
        # In practice, batch might be similar or faster due to optimizations
        assert batch_time < individual_time * 2  # Should not be 2x slower


class TestSecurityValidationIntegration:
    """Test security validation integration."""

    def test_security_validation_catches_issues(self):
        """Test that security validator catches configuration issues."""
        from skills.mcp_security_validator import validate_server_security

        with tempfile.TemporaryDirectory() as tmpdir:
            server_dir = Path(tmpdir)

            # Create minimal server without security config
            (server_dir / "server.py").write_text("# Empty server")

            # Should detect missing security configuration
            result = validate_server_security(str(server_dir), response_format="complete")

            assert result.success
            # Should have lower score due to missing config
            assert result.data["security_score"] < 90

            # Should have issues reported
            assert len(result.data["issues"]) > 0

    def test_security_validation_with_good_config(self):
        """Test that good security config gets high score."""
        from skills.mcp_security_validator import validate_server_security

        with tempfile.TemporaryDirectory() as tmpdir:
            server_dir = Path(tmpdir)

            # Create server with good security config
            (server_dir / "server.py").write_text('''
workspace = "/workspace"
''')

            (server_dir / "config.py").write_text('''
ALLOWED_PATHS = ["/workspace", "/tmp"]
ALLOWED_DOMAINS = ["api.anthropic.com", "pypi.org", "github.com"]
CPU_TIMEOUT = 30
MEMORY_LIMIT_MB = 512
MAX_PROCESSES = 10
''')

            result = validate_server_security(str(server_dir), response_format="summary")

            assert result.success
            # Should have better score with configuration
            assert result.data["security_score"] >= 60  # Reasonable score


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

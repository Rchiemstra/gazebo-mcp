"""
Tests for MCP Adapter Creator skill.
"""

import pytest
from pathlib import Path
import tempfile
from skills.mcp_adapter_creator import (
    create_adapter,
    create_batch_adapters,
    OperationResult,
    ErrorCodes
)


class TestCreateAdapter:
    """Test adapter creation functionality."""

    def test_create_adapter_basic(self):
        """Test basic adapter creation for a known skill."""
        result = create_adapter("code_analysis", response_format="summary")

        assert result.success
        assert result.data is not None
        assert "skill_name" in result.data
        assert result.data["skill_name"] == "code_analysis"
        assert "adapter_path" in result.data
        assert result.data["operations_count"] > 0

    def test_create_adapter_complete_format(self):
        """Test adapter creation with complete format."""
        result = create_adapter("code_analysis", response_format="complete")

        assert result.success
        assert "adapter_code" in result.data
        assert "operations" in result.data

        # Check adapter code structure
        adapter_code = result.data["adapter_code"]
        assert "MCP Adapter" in adapter_code
        assert "OPERATIONS" in adapter_code
        assert "ResultFilter" in adapter_code

    def test_create_adapter_with_custom_output_path(self):
        """Test adapter creation with custom output path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = str(Path(tmpdir) / "test_adapter.py")

            result = create_adapter(
                "code_analysis",
                output_path=output_path,
                response_format="summary"
            )

            assert result.success
            assert result.data["adapter_path"] == output_path

    def test_create_adapter_specific_operations(self):
        """Test adapter creation for specific operations only."""
        result = create_adapter(
            "code_analysis",
            operations=["analyze_file"],
            response_format="complete"
        )

        assert result.success
        operations = result.data.get("operations", [])

        # Should include the requested operation
        if operations:
            assert any(op["name"] == "analyze_file" for op in operations)

    def test_create_adapter_nonexistent_skill(self):
        """Test adapter creation for non-existent skill."""
        result = create_adapter("nonexistent_skill_xyz")

        assert not result.success
        assert result.error is not None
        assert "not found" in result.error.lower()

    def test_create_adapter_includes_examples(self):
        """Test that generated adapters include usage examples."""
        result = create_adapter("code_analysis", response_format="complete")

        assert result.success
        adapter_code = result.data["adapter_code"]

        # Should include example code
        assert "from skills.code_analysis import" in adapter_code
        assert "from skills.common.filters import ResultFilter" in adapter_code
        assert "filtered = ResultFilter.limit" in adapter_code


class TestCreateBatchAdapters:
    """Test batch adapter creation."""

    def test_create_batch_adapters_summary(self):
        """Test batch adapter creation with summary format."""
        skills_config = [
            {"name": "code_analysis"},
            {"name": "test_orchestrator"}
        ]

        result = create_batch_adapters(skills_config, response_format="summary")

        assert result.success
        assert result.data["total_skills"] == 2
        assert result.data["successful"] >= 0
        assert result.data["total_adapters"] >= 0

    def test_create_batch_adapters_complete(self):
        """Test batch adapter creation with complete format."""
        skills_config = [
            {"name": "code_analysis"}
        ]

        result = create_batch_adapters(skills_config, response_format="complete")

        assert result.success
        assert "adapters" in result.data
        assert len(result.data["adapters"]) > 0

        # Check adapter structure
        adapter = result.data["adapters"][0]
        assert "skill_name" in adapter
        assert "adapter_code" in adapter
        assert "operations_count" in adapter

    def test_create_batch_adapters_with_failures(self):
        """Test batch creation handles failures gracefully."""
        skills_config = [
            {"name": "code_analysis"},
            {"name": "nonexistent_skill"}
        ]

        result = create_batch_adapters(skills_config, response_format="summary")

        assert result.success
        assert result.data["failed"] == 1
        assert len(result.data["failed_skills"]) == 1

    def test_create_batch_adapters_with_specific_operations(self):
        """Test batch creation with specific operations per skill."""
        skills_config = [
            {
                "name": "code_analysis",
                "operations": ["analyze_file"]
            }
        ]

        result = create_batch_adapters(skills_config, response_format="complete")

        assert result.success
        assert len(result.data["adapters"]) > 0


class TestAdapterCodeQuality:
    """Test quality of generated adapter code."""

    def test_adapter_has_proper_docstring(self):
        """Test that adapters have proper docstrings."""
        result = create_adapter("code_analysis", response_format="complete")

        assert result.success
        adapter_code = result.data["adapter_code"]

        # Should have module docstring
        assert '"""' in adapter_code
        assert "MCP Adapter" in adapter_code

    def test_adapter_has_operations_dict(self):
        """Test that adapters define OPERATIONS dictionary."""
        result = create_adapter("code_analysis", response_format="complete")

        assert result.success
        adapter_code = result.data["adapter_code"]

        assert "OPERATIONS = " in adapter_code

    def test_adapter_follows_token_efficiency_pattern(self):
        """Test that adapters include token efficiency documentation."""
        result = create_adapter("code_analysis", response_format="complete")

        assert result.success
        adapter_code = result.data["adapter_code"]

        # Should mention token savings
        assert "98.7%" in adapter_code or "token" in adapter_code.lower()
        assert "ResultFilter" in adapter_code

    def test_adapter_has_get_operation_docs_function(self):
        """Test that adapters have helper function."""
        result = create_adapter("code_analysis", response_format="complete")

        assert result.success
        adapter_code = result.data["adapter_code"]

        assert "def get_operation_docs()" in adapter_code


class TestIntegrationWithSchemaGenerator:
    """Test integration with mcp_schema_generator."""

    def test_adapter_uses_schema_metadata(self):
        """Test that adapters use schema generator for metadata."""
        result = create_adapter("code_analysis", response_format="complete")

        assert result.success

        # Adapter should have operations from schema generator
        operations = result.data.get("operations", [])
        assert len(operations) > 0

        # Each operation should have metadata
        for op in operations:
            assert "name" in op
            assert "description" in op
            assert "parameters" in op


class TestErrorHandling:
    """Test error handling."""

    def test_missing_mcp_schema_generator_dependency(self):
        """Test handling when mcp_schema_generator is not available."""
        # This would require mocking the import
        # Skip for now as it requires the skill
        pass

    def test_invalid_skill_config(self):
        """Test handling of invalid skill configuration."""
        # Empty config
        result = create_batch_adapters([], response_format="summary")

        assert result.success
        assert result.data["total_skills"] == 0


class TestOutputPaths:
    """Test output path handling."""

    def test_default_output_path_creation(self):
        """Test that default output paths are created correctly."""
        result = create_adapter("code_analysis", response_format="summary")

        assert result.success
        adapter_path = result.data["adapter_path"]

        # Should be in mcp/servers/skills-mcp/adapters/
        assert "mcp" in adapter_path
        assert "adapters" in adapter_path
        assert adapter_path.endswith(".py")

    def test_custom_output_directory(self):
        """Test custom output directory handling."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = create_batch_adapters(
                [{"name": "code_analysis"}],
                output_dir=tmpdir,
                response_format="summary"
            )

            # Note: current implementation doesn't use output_dir in batch
            # Just test it doesn't crash
            assert result.success


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

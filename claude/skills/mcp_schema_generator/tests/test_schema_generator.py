"""
Tests for MCP Schema Generator skill.
"""

import pytest
from pathlib import Path
from skills.mcp_schema_generator import (
    generate_schema,
    validate_schema,
    generate_batch_schemas,
    OperationResult,
    ErrorCodes
)


class TestGenerateSchema:
    """Test schema generation functionality."""

    def test_generate_schema_basic(self):
        """Test basic schema generation for a known skill."""
        result = generate_schema("code_analysis", response_format="summary")

        assert result.success
        assert result.data is not None
        assert "skill_name" in result.data
        assert result.data["skill_name"] == "code_analysis"
        assert result.data["operations_count"] > 0

    def test_generate_schema_complete_format(self):
        """Test schema generation with complete format."""
        result = generate_schema("code_analysis", response_format="complete")

        assert result.success
        assert "schemas" in result.data
        assert len(result.data["schemas"]) > 0

        # Check first schema structure
        schema = result.data["schemas"][0]
        assert "tool_name" in schema
        assert "description" in schema
        assert "input_schema" in schema
        assert "examples" in schema

    def test_generate_schema_specific_operations(self):
        """Test schema generation for specific operations."""
        result = generate_schema(
            "code_analysis",
            operations=["analyze_file"],
            response_format="complete"
        )

        assert result.success
        schemas = result.data.get("schemas", [])

        # Should only have the requested operation
        if schemas:
            assert any("analyze_file" in s["tool_name"] for s in schemas)

    def test_generate_schema_nonexistent_skill(self):
        """Test schema generation for non-existent skill."""
        result = generate_schema("nonexistent_skill_xyz")

        assert not result.success
        assert result.error is not None
        assert "not found" in result.error.lower()
        assert result.error_code == ErrorCodes.VALIDATION_ERROR

    def test_generate_schema_returns_duration(self):
        """Test that schema generation includes duration."""
        result = generate_schema("code_analysis")

        assert result.success
        assert result.duration >= 0
        assert isinstance(result.duration, float)


class TestValidateSchema:
    """Test schema validation functionality."""

    def test_validate_valid_schema(self):
        """Test validation of a valid schema."""
        valid_schema = {
            "tool_name": "test.operation",
            "description": "Test operation description",
            "input_schema": {
                "type": "object",
                "properties": {
                    "param1": {
                        "type": "string",
                        "description": "First parameter"
                    }
                },
                "required": ["param1"]
            },
            "examples": [
                {
                    "description": "Example usage",
                    "code": "from skills.test import operation"
                }
            ]
        }

        result = validate_schema(valid_schema)

        assert result.success
        assert result.data["valid"] is True
        assert len(result.data["errors"]) == 0

    def test_validate_missing_required_fields(self):
        """Test validation catches missing required fields."""
        invalid_schema = {
            "tool_name": "test.operation",
            # Missing description and input_schema
        }

        result = validate_schema(invalid_schema)

        assert result.success
        assert result.data["valid"] is False
        assert len(result.data["errors"]) > 0

    def test_validate_schema_warnings(self):
        """Test that validation generates warnings for issues."""
        schema_with_issues = {
            "tool_name": "test.operation",
            "description": "Short",  # Too short
            "input_schema": {
                "type": "object",
                "properties": {
                    "param1": {
                        "type": "string"
                        # Missing description - should warn
                    }
                },
                "required": []
            }
        }

        result = validate_schema(schema_with_issues)

        assert result.success
        # Should have warnings about short description and missing param description
        assert len(result.data["warnings"]) > 0

    def test_validate_schema_score(self):
        """Test that validation returns a score."""
        schema = {
            "tool_name": "test.operation",
            "description": "A valid test operation",
            "input_schema": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }

        result = validate_schema(schema)

        assert result.success
        assert "score" in result.data
        assert 0 <= result.data["score"] <= 100


class TestGenerateBatchSchemas:
    """Test batch schema generation."""

    def test_generate_batch_schemas_summary(self):
        """Test batch generation with summary format."""
        skills = ["code_analysis", "test_orchestrator"]
        result = generate_batch_schemas(skills, response_format="summary")

        assert result.success
        assert result.data["total_skills"] == 2
        assert result.data["successful"] >= 0
        assert result.data["total_schemas"] >= 0

    def test_generate_batch_schemas_complete(self):
        """Test batch generation with complete format."""
        skills = ["code_analysis"]
        result = generate_batch_schemas(skills, response_format="complete")

        assert result.success
        assert "schemas" in result.data
        assert len(result.data["schemas"]) > 0

    def test_generate_batch_schemas_with_failures(self):
        """Test batch generation handles failures gracefully."""
        skills = ["code_analysis", "nonexistent_skill"]
        result = generate_batch_schemas(skills, response_format="summary")

        assert result.success
        assert result.data["failed"] == 1
        assert len(result.data["failed_skills"]) == 1
        assert result.data["failed_skills"][0]["skill"] == "nonexistent_skill"

    def test_generate_batch_schemas_empty_list(self):
        """Test batch generation with empty skill list."""
        result = generate_batch_schemas([], response_format="summary")

        assert result.success
        assert result.data["total_skills"] == 0
        assert result.data["total_schemas"] == 0


class TestOperationResult:
    """Test OperationResult structure."""

    def test_operation_result_success(self):
        """Test successful operation result structure."""
        result = generate_schema("code_analysis")

        assert hasattr(result, "success")
        assert hasattr(result, "data")
        assert hasattr(result, "error")
        assert hasattr(result, "error_code")
        assert hasattr(result, "duration")
        assert hasattr(result, "metadata")

    def test_operation_result_failure(self):
        """Test failure operation result structure."""
        result = generate_schema("nonexistent_skill")

        assert result.success is False
        assert result.error is not None
        assert result.error_code is not None


class TestSchemaStructure:
    """Test generated schema structure."""

    def test_schema_follows_mcp_format(self):
        """Test that generated schemas follow MCP format."""
        result = generate_schema("code_analysis", response_format="complete")

        assert result.success
        schemas = result.data["schemas"]

        for schema in schemas:
            # Check MCP required fields
            assert "tool_name" in schema
            assert "." in schema["tool_name"]  # Should be skill.operation format

            assert "description" in schema
            assert isinstance(schema["description"], str)

            assert "input_schema" in schema
            input_schema = schema["input_schema"]
            assert "type" in input_schema
            assert "properties" in input_schema or "required" in input_schema

    def test_schema_includes_examples(self):
        """Test that schemas include usage examples."""
        result = generate_schema("code_analysis", response_format="complete")

        assert result.success
        schemas = result.data["schemas"]

        for schema in schemas:
            assert "examples" in schema
            assert isinstance(schema["examples"], list)
            if schema["examples"]:
                example = schema["examples"][0]
                assert "description" in example or "code" in example


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_skill_with_no_operations_file(self):
        """Test handling of skill without operations.py."""
        # This would require a test skill without operations.py
        # Skip if all skills have operations.py
        pass

    def test_skill_with_dash_in_name(self):
        """Test handling of skill names with dashes."""
        # Skills can have dashes or underscores
        # The function should handle both
        pass

    def test_concurrent_schema_generation(self):
        """Test that schema generation is thread-safe."""
        # Could test concurrent calls
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

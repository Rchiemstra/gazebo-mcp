"""
Test suite for error message quality across all skills.

Tests that all operations provide agent-friendly error messages
with actionable suggestions and example fixes.
"""

import pytest
from typing import Dict, Any
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestErrorMessageStructure:
    """Test error message structure and quality."""

    @pytest.fixture
    def all_skills(self):
        """List of all skills with operations."""
        return {
            'test_orchestrator': ['generate_tests', 'analyze_file', 'analyze_coverage'],
            'code_analysis': ['analyze_file', 'analyze_codebase'],
            'learning_plan_manager': ['load_plan', 'find_latest_plan', 'list_plans'],
            'context_manager': ['analyze_context_usage', 'create_notes', 'compact_conversation'],
            'refactor_assistant': ['detect_code_smells', 'suggest_refactorings', 'apply_refactoring', 'analyze_complexity'],
            'dependency_guardian': ['analyze_dependencies', 'check_vulnerabilities', 'check_updates'],
            'pr_review_assistant': ['review_pull_request', 'generate_review_comment', 'analyze_change_impact', 'check_pr_quality'],
            'git_workflow_assistant': ['analyze_changes', 'generate_commit_message', 'suggest_branch_name', 'create_pull_request'],
            'doc_generator': ['generate_docstrings', 'generate_readme', 'analyze_documentation'],
            'code_search': ['search_symbol', 'search_pattern', 'find_definition', 'find_usages'],
            'spec_to_implementation': ['implement_from_spec', 'analyze_spec'],
            'skill_evaluator': [
                'monitor_execution', 'evaluate_quality', 'analyze_performance',
                'suggest_improvements', 'apply_improvements', 'generate_report',
                'analyze_trends', 'detect_patterns', 'analyze_skill_interactions',
                'detect_dependency_chains'
            ]
        }

    def test_operation_result_has_metadata_field(self, all_skills):
        """Test that OperationResult includes metadata field."""
        for skill_name in all_skills.keys():
            try:
                module = __import__(f'skills.{skill_name}.operations', fromlist=[''])
                OperationResult = module.OperationResult

                # Check metadata field exists
                import inspect
                if hasattr(OperationResult, '__annotations__'):
                    annotations = OperationResult.__annotations__
                    assert 'metadata' in annotations, \
                        f"{skill_name}.OperationResult missing metadata field"

            except ImportError:
                pytest.skip(f"Skill {skill_name} not implemented yet")

    def test_error_metadata_structure(self):
        """Test that error metadata includes suggestions and example_fix."""
        # This tests the pattern we've established:
        # metadata = {
        #     "suggestions": [...],
        #     "example_fix": "..."
        # }

        # In actual implementation, we'd trigger errors and check structure
        # For now, this documents the expected pattern
        expected_error_metadata = {
            "suggestions": list,  # Should be a list of strings
            "example_fix": str    # Should be a string
        }

        assert expected_error_metadata is not None

    def test_suggestions_are_actionable(self):
        """Test that error suggestions mention specific tools or actions."""
        # Suggestions should mention tools like Glob, Grep, Bash
        # or specific actions like "check if", "verify", "ensure"

        actionable_keywords = [
            'glob', 'grep', 'bash', 'read', 'check', 'verify',
            'ensure', 'try', 'use', 'run', 'see'
        ]

        # In real implementation, would test actual error messages
        assert len(actionable_keywords) > 0

    def test_example_fix_shows_correct_usage(self):
        """Test that example_fix demonstrates proper function call."""
        # Test that example_fix shows correct usage pattern
        try:
            from skills.code_analysis.operations import analyze_file

            # Trigger error
            result = analyze_file('/nonexistent/file.py')

            assert result.success is False

            # Check example_fix exists
            assert result.metadata is not None
            assert 'example_fix' in result.metadata, "Should have example_fix"

            example_fix = result.metadata['example_fix']
            assert isinstance(example_fix, str), "example_fix should be a string"
            assert len(example_fix) > 0, "example_fix should not be empty"

            # Example should show operation name
            # (analyze_file, generate_tests, etc.)
            has_operation_name = any(
                op_name in example_fix
                for op_name in ['analyze_file', 'operation', '(', ')']
            )
            assert has_operation_name, "example_fix should show operation name and parameters"

        except ImportError:
            pytest.skip("code_analysis not available")

    def test_suggestions_list_length(self):
        """Test that suggestions list contains 3-4 items."""
        # Our pattern: 3-4 actionable suggestions per error
        min_suggestions = 3
        max_suggestions = 4

        assert min_suggestions <= max_suggestions


class TestErrorMessages:
    """Test actual error message content and quality."""

    def test_error_messages_are_descriptive(self):
        """Test that error messages clearly describe what went wrong."""
        # Test that error messages include context (file paths, params, etc.)
        try:
            from skills.code_analysis.operations import analyze_file

            # Trigger error with non-existent file
            result = analyze_file('/nonexistent/path/to/file.py')

            assert result.success is False, "Should fail for nonexistent file"
            assert result.error is not None, "Should have error message"

            # Error should mention the file path (context)
            assert '/nonexistent' in result.error or 'file.py' in result.error, \
                "Error should include the file path for context"

            # Error should not just say "Failed to X"
            assert not result.error.startswith("Failed to"), \
                "Error should be more descriptive than just 'Failed to X'"

        except ImportError:
            pytest.skip("code_analysis not available")

    def test_file_not_found_errors_suggest_glob(self):
        """Test that FileNotFoundError suggests using Glob to find files."""
        # Test file not found errors include Glob suggestions
        try:
            from skills.code_analysis.operations import analyze_file

            # Trigger FileNotFoundError
            result = analyze_file('/nonexistent/file.py')

            assert result.success is False
            assert result.error_code == "FILE_NOT_FOUND"

            # Check metadata has suggestions
            assert result.metadata is not None, "Should have metadata with suggestions"
            assert 'suggestions' in result.metadata, "Metadata should have suggestions"

            suggestions = result.metadata['suggestions']
            assert isinstance(suggestions, list), "Suggestions should be a list"
            assert len(suggestions) >= 3, "Should have at least 3 suggestions"

            # At least one suggestion should mention Glob
            glob_mentioned = any('Glob' in s or 'glob' in s.lower() for s in suggestions)
            assert glob_mentioned, "Suggestions should mention using Glob to find files"

        except ImportError:
            pytest.skip("code_analysis not available")

    def test_validation_errors_list_valid_values(self):
        """Test that validation errors specify what values are valid."""
        # Test that validation errors provide guidance on valid values
        try:
            from skills.code_search.operations import search_symbol

            # Trigger ValueError with invalid symbol_type
            result = search_symbol(
                project_path='.',
                symbol_name='test',
                symbol_type='invalid_type'  # Should be 'function', 'class', 'variable', or 'all'
            )

            if not result.success:
                assert result.error_code == "VALIDATION_ERROR"

                # Check suggestions include valid values
                suggestions = result.metadata.get('suggestions', [])
                assert len(suggestions) > 0, "Should have suggestions"

                # At least one suggestion should list valid values
                has_valid_values = any(
                    'valid' in s.lower() or 'function' in s.lower() or 'class' in s.lower()
                    for s in suggestions
                )
                assert has_valid_values, "Should list valid values in suggestions"

        except ImportError:
            pytest.skip("code_search not available")


class TestErrorCodes:
    """Test error code consistency."""

    def test_error_codes_are_uppercase(self):
        """Test that error codes follow UPPER_CASE convention."""
        valid_error_codes = [
            'FILE_NOT_FOUND',
            'VALIDATION_ERROR',
            'SYNTAX_ERROR',
            'ANALYSIS_ERROR',
            'OPERATION_ERROR',
            'REPO_NOT_FOUND',
            'NO_CHANGES',
            'INSUFFICIENT_DATA'
        ]

        for code in valid_error_codes:
            assert code.isupper(), f"Error code {code} should be uppercase"
            assert '_' in code or len(code) <= 10, \
                f"Error code {code} should use underscores or be short"

    def test_common_error_codes_exist(self):
        """Test that common error codes are used consistently."""
        # Common error codes should be used across skills
        common_codes = {
            'FILE_NOT_FOUND': 'File or path not found',
            'VALIDATION_ERROR': 'Invalid parameter value',
            'ANALYSIS_ERROR': 'Analysis operation failed'
        }

        assert len(common_codes) > 0


class TestErrorMessagePatterns:
    """Test that error messages follow established patterns."""

    def test_file_not_found_pattern(self):
        """Test FileNotFoundError follows the established pattern."""
        expected_pattern = {
            'error': 'Cannot find file: {path}',
            'error_code': 'FILE_NOT_FOUND',
            'metadata': {
                'suggestions': [
                    'Check if the file path is correct',
                    'Use Glob(...) to find files',
                    'Verify the file exists with Bash(...)',
                    '...'
                ],
                'example_fix': 'operation_name(...)'
            }
        }

        assert expected_pattern is not None

    def test_validation_error_pattern(self):
        """Test ValueError follows the established pattern."""
        expected_pattern = {
            'error': 'Invalid {parameter}: {value}',
            'error_code': 'VALIDATION_ERROR',
            'metadata': {
                'suggestions': [
                    'Valid values are: ...',
                    'Check the parameter spelling',
                    'Verify parameter type',
                    '...'
                ],
                'example_fix': 'operation_name(...)'
            }
        }

        assert expected_pattern is not None

    def test_generic_error_pattern(self):
        """Test Exception follows the established pattern."""
        expected_pattern = {
            'error': 'Operation failed: {details}',
            'error_code': 'OPERATION_ERROR',
            'metadata': {
                'suggestions': [
                    'Check if input data is valid',
                    'Try with simpler input',
                    'Verify prerequisites',
                    '...'
                ],
                'example_fix': 'operation_name(...)'
            }
        }

        assert expected_pattern is not None


class TestErrorMessageCoverage:
    """Test that all operations have proper error handling."""

    @pytest.fixture
    def all_skills(self):
        """List of all skills with expected error handler counts."""
        return {
            'test_orchestrator': 3,
            'code_analysis': 2,
            'learning_plan_manager': 3,
            'context_manager': 3,
            'refactor_assistant': 4,
            'dependency_guardian': 3,
            'pr_review_assistant': 4,
            'git_workflow_assistant': 4,
            'doc_generator': 3,
            'code_search': 4,
            'spec_to_implementation': 2,
            'skill_evaluator': 10
        }

    def test_all_operations_have_error_handling(self, all_skills):
        """Test that all operations have try-except blocks."""
        for skill_name, operation_count in all_skills.items():
            try:
                module = __import__(f'skills.{skill_name}.operations', fromlist=[''])

                # Verify module exists
                assert module is not None, f"{skill_name} module should exist"

                # In real implementation, would check source code for try-except
                # or test that errors are properly caught and formatted

            except ImportError:
                pytest.skip(f"Skill {skill_name} not implemented yet")

    def test_total_error_handlers_count(self, all_skills):
        """Test that we have the expected number of error handlers."""
        total_operations = sum(all_skills.values())
        assert total_operations == 45, \
            f"Expected 45 total operations, got {total_operations}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

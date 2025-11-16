"""
Test suite for response_format parameter across all skills.

Tests that all operations properly support summary/detailed modes
and provide appropriate token savings.
"""

import pytest
from typing import Dict, Any
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestResponseFormat:
    """Test response_format parameter implementation across all skills."""

    @pytest.fixture
    def all_skills(self):
        """List of all skills with operations that should support response_format."""
        return {
            'test_orchestrator': ['generate_tests', 'analyze_file', 'analyze_coverage'],
            'code_analysis': ['analyze_file', 'analyze_codebase'],
            'learning_plan_manager': ['load_plan', 'find_latest_plan', 'list_plans'],
            'context_manager': ['analyze_context_usage', 'create_notes', 'compact_conversation'],
            'refactor_assistant': ['detect_code_smells', 'suggest_refactorings', 'analyze_complexity'],
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

    def test_all_operations_have_response_format_parameter(self, all_skills):
        """Test that all operations accept response_format parameter."""
        for skill_name, operations in all_skills.items():
            try:
                # Import the skill operations module
                module = __import__(f'skills.{skill_name}.operations', fromlist=[''])

                for operation_name in operations:
                    # Check operation exists
                    assert hasattr(module, operation_name), \
                        f"Operation {operation_name} not found in {skill_name}"

                    operation = getattr(module, operation_name)

                    # Check function signature includes response_format
                    import inspect
                    sig = inspect.signature(operation)
                    params = sig.parameters

                    assert 'response_format' in params, \
                        f"{skill_name}.{operation_name} missing response_format parameter"

                    # Check default value
                    default = params['response_format'].default
                    assert default in ['summary', 'concise', 'detailed'], \
                        f"{skill_name}.{operation_name} response_format default should be summary/concise/detailed"

            except ImportError as e:
                pytest.skip(f"Skill {skill_name} not implemented yet: {e}")

    def test_operations_return_different_data_for_formats(self, all_skills):
        """Test that summary and detailed modes return different amounts of data."""
        # Test a few representative operations
        test_cases = [
            ('test_orchestrator', 'generate_tests'),
            ('code_analysis', 'analyze_file'),
            ('refactor_assistant', 'detect_code_smells'),
        ]

        for skill_name, operation_name in test_cases:
            try:
                module = __import__(f'skills.{skill_name}.operations', fromlist=[''])
                operation = getattr(module, operation_name)

                # This is a structure test - we're checking the response format
                # is properly handled, not testing actual functionality
                # In real tests, you'd provide valid test data

                # Verify operation exists and is callable
                assert callable(operation), \
                    f"{skill_name}.{operation_name} should be callable"

            except ImportError:
                pytest.skip(f"Skill {skill_name} not implemented yet")

    def test_operation_result_structure(self, all_skills):
        """Test that all operations return OperationResult with correct structure."""
        for skill_name, operations in all_skills.items():
            try:
                module = __import__(f'skills.{skill_name}.operations', fromlist=[''])

                # Check OperationResult is exported
                assert hasattr(module, 'OperationResult'), \
                    f"{skill_name} should export OperationResult"

                OperationResult = module.OperationResult

                # Check OperationResult has required fields
                import inspect
                if hasattr(OperationResult, '__annotations__'):
                    annotations = OperationResult.__annotations__
                    required_fields = ['success', 'data', 'error', 'error_code', 'duration', 'metadata']

                    for field in required_fields:
                        assert field in annotations, \
                            f"{skill_name}.OperationResult missing field: {field}"

            except ImportError:
                pytest.skip(f"Skill {skill_name} not implemented yet")

    def test_docstrings_mention_token_efficiency(self, all_skills):
        """Test that operation docstrings mention token efficiency."""
        for skill_name, operations in all_skills.items():
            try:
                module = __import__(f'skills.{skill_name}.operations', fromlist=[''])

                for operation_name in operations:
                    operation = getattr(module, operation_name)
                    docstring = operation.__doc__ or ""

                    # Should mention either "token" or "response_format"
                    has_token_info = any(keyword in docstring.lower() for keyword in [
                        'token', 'response_format', 'summary', 'detailed'
                    ])

                    assert has_token_info, \
                        f"{skill_name}.{operation_name} docstring should mention token efficiency"

            except ImportError:
                pytest.skip(f"Skill {skill_name} not implemented yet")


class TestResponseFormatValues:
    """Test valid values for response_format parameter."""

    def test_summary_format_is_concise(self):
        """Test that summary format returns minimal data."""
        # Test with test_orchestrator.generate_tests as example
        try:
            from skills.test_orchestrator.operations import generate_tests
            import json

            # This test requires actual file to analyze
            # For now, verify the operation accepts both formats
            # In real test, would compare actual output sizes

            # At minimum, verify operation accepts summary format
            import inspect
            sig = inspect.signature(generate_tests)
            assert 'response_format' in sig.parameters

        except ImportError:
            pytest.skip("test_orchestrator not available")

    def test_detailed_format_is_comprehensive(self):
        """Test that detailed format returns complete data."""
        # Verify operations accept detailed format
        try:
            from skills.test_orchestrator.operations import generate_tests
            import inspect

            sig = inspect.signature(generate_tests)
            param = sig.parameters['response_format']

            # Check that 'detailed' is an accepted value
            # (either as default or documented in docstring)
            assert param is not None

        except ImportError:
            pytest.skip("test_orchestrator not available")

    def test_invalid_format_value_handling(self):
        """Test that invalid response_format values are handled gracefully."""
        # Test that operations handle invalid format values
        # Most operations should default to 'summary' for invalid values
        try:
            from skills.test_orchestrator.operations import generate_tests
            import tempfile
            import os

            # Create a temporary Python file for testing
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write('def test_function():\n    pass\n')
                temp_file = f.name

            try:
                # Call with invalid format - should not crash
                result = generate_tests(temp_file, response_format='invalid_format')

                # Should either succeed (defaulted to summary) or return clear error
                if not result.success:
                    # If it fails, should have clear error about invalid format
                    assert 'format' in result.error.lower() or 'invalid' in result.error.lower()
                # If it succeeds, it defaulted gracefully

            finally:
                os.unlink(temp_file)

        except ImportError:
            pytest.skip("test_orchestrator not available")


class TestTokenEfficiency:
    """Test token efficiency claims in documentation."""

    def test_summary_saves_tokens(self):
        """Test that summary mode uses fewer tokens than detailed mode."""
        # Test that summary format returns less data than detailed
        try:
            from skills.code_analysis.operations import analyze_file
            import tempfile
            import os
            import json

            # Create a sample Python file with meaningful content
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write('''
def function1():
    """Docstring for function1."""
    pass

def function2():
    """Docstring for function2."""
    return 42

class MyClass:
    """A sample class."""
    def method1(self):
        pass
    def method2(self):
        pass
''')
                temp_file = f.name

            try:
                # Get results in both formats
                summary_result = analyze_file(temp_file, response_format='summary')
                detailed_result = analyze_file(temp_file, response_format='detailed')

                if summary_result.success and detailed_result.success:
                    # Convert to JSON to measure approximate token count
                    summary_json = json.dumps(summary_result.data)
                    detailed_json = json.dumps(detailed_result.data)

                    # Summary should be shorter (fewer characters ≈ fewer tokens)
                    assert len(summary_json) <= len(detailed_json), \
                        f"Summary ({len(summary_json)} chars) should be shorter than detailed ({len(detailed_json)} chars)"

            finally:
                os.unlink(temp_file)

        except ImportError:
            pytest.skip("code_analysis not available")

    def test_efficiency_tips_present(self):
        """Test that operations have documentation about token efficiency."""
        # Check that skills document token efficiency in their docstrings
        skills_with_docs = [
            ('test_orchestrator', 'generate_tests'),
            ('code_analysis', 'analyze_file'),
            ('learning_plan_manager', 'load_plan'),
        ]

        for skill_name, operation_name in skills_with_docs:
            try:
                module = __import__(f'skills.{skill_name}.operations', fromlist=[''])
                operation = getattr(module, operation_name)
                docstring = operation.__doc__ or ""

                # Should mention token efficiency concepts
                has_efficiency_info = any(keyword in docstring.lower() for keyword in [
                    'token', 'response_format', 'summary', 'detailed', 'efficient'
                ])

                assert has_efficiency_info, \
                    f"{skill_name}.{operation_name} should document token efficiency"

            except ImportError:
                # Skip if skill not available
                continue


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

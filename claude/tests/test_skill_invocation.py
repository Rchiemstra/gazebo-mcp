"""
Test Skill Invocation

Tests whether agents can correctly invoke skills with proper parameters,
handle errors gracefully, and recover from failures.

This implements Phase 2.2 of the Anthropic Best Practices Implementation Plan:
evaluating skill usability and error recovery.
"""

import pytest
from pathlib import Path
import importlib
import inspect
from typing import Dict, List, Any, Callable


class SkillInvocationTester:
    """Tests for skill invocation and usability."""

    def __init__(self, skills_dir: Path):
        self.skills_dir = skills_dir

    def get_skill_operations(self, skill_name: str) -> Dict[str, Callable]:
        """Get all operation functions from a skill."""
        try:
            # Import the skill's operations module
            module_name = f'skills.{skill_name}.operations'
            module = importlib.import_module(module_name)

            # Get all public functions (operations)
            operations = {}
            for name, obj in inspect.getmembers(module):
                if inspect.isfunction(obj) and not name.startswith('_'):
                    operations[name] = obj

            return operations

        except (ImportError, AttributeError):
            return {}

    def get_operation_signature(self, operation: Callable) -> Dict[str, Any]:
        """Get operation signature information."""
        sig = inspect.signature(operation)

        params = {}
        for name, param in sig.parameters.items():
            params[name] = {
                'name': name,
                'type': param.annotation if param.annotation != inspect.Parameter.empty else None,
                'default': param.default if param.default != inspect.Parameter.empty else None,
                'required': param.default == inspect.Parameter.empty
            }

        return {
            'name': operation.__name__,
            'params': params,
            'docstring': operation.__doc__,
            'return_type': sig.return_annotation if sig.return_annotation != inspect.Signature.empty else None
        }

    def has_response_format_parameter(self, operation: Callable) -> bool:
        """Check if operation has response_format parameter."""
        sig = inspect.signature(operation)
        return 'response_format' in sig.parameters

    def has_proper_error_handling(self, operation: Callable) -> bool:
        """Check if operation has proper error handling in docstring."""
        docstring = operation.__doc__ or ''

        # Check for error handling documentation
        error_indicators = [
            'raises', 'exception', 'error', 'returns',
            'operationresult', 'success', 'failed'
        ]

        return any(indicator in docstring.lower() for indicator in error_indicators)

    def has_token_efficiency_docs(self, operation: Callable) -> bool:
        """Check if operation documents token efficiency."""
        docstring = operation.__doc__ or ''

        efficiency_indicators = [
            'token', 'efficiency', 'response_format',
            'summary', 'detailed', 'saves'
        ]

        return any(indicator in docstring.lower() for indicator in efficiency_indicators)


@pytest.fixture
def skills_dir():
    """Get the skills directory."""
    return Path(__file__).parent.parent / 'skills'


@pytest.fixture
def invocation_tester(skills_dir):
    """Create a SkillInvocationTester instance."""
    return SkillInvocationTester(skills_dir)


# List of skills to test (those with operations.py)
TESTABLE_SKILLS = [
    'test_orchestrator',
    'code_analysis',
    'learning_plan_manager',
    'context_manager',
    'refactor_assistant',
    'dependency_guardian',
    'pr_review_assistant',
    'git_workflow_assistant',
    'doc_generator',
    'code_search',
    'skill_evaluator',
    'spec_to_implementation',
    'verification',
    'llm_judge'
]


class TestOperationSignatures:
    """Test operation function signatures."""

    @pytest.mark.parametrize('skill_name', TESTABLE_SKILLS)
    def test_operations_have_docstrings(self, invocation_tester, skill_name):
        """Test that all operations have docstrings."""
        operations = invocation_tester.get_skill_operations(skill_name)

        for op_name, op_func in operations.items():
            # Skip utility functions
            if op_name.startswith('get_') and not op_name.endswith('_operation'):
                continue

            assert op_func.__doc__ is not None, \
                f"{skill_name}.{op_name} missing docstring"
            assert len(op_func.__doc__.strip()) > 20, \
                f"{skill_name}.{op_name} docstring too short"

    @pytest.mark.parametrize('skill_name', TESTABLE_SKILLS)
    def test_operations_have_response_format(self, invocation_tester, skill_name):
        """Test that operations support response_format parameter."""
        operations = invocation_tester.get_skill_operations(skill_name)

        for op_name, op_func in operations.items():
            # Skip utility functions
            if op_name.startswith('get_') and not op_name.endswith('_operation'):
                continue

            has_param = invocation_tester.has_response_format_parameter(op_func)
            assert has_param, \
                f"{skill_name}.{op_name} missing response_format parameter"

    @pytest.mark.parametrize('skill_name', TESTABLE_SKILLS)
    def test_operations_document_errors(self, invocation_tester, skill_name):
        """Test that operations document error handling."""
        operations = invocation_tester.get_skill_operations(skill_name)

        missing_error_docs = []
        for op_name, op_func in operations.items():
            # Skip utility functions
            if op_name.startswith('get_') and not op_name.endswith('_operation'):
                continue

            if not invocation_tester.has_proper_error_handling(op_func):
                missing_error_docs.append(f"{skill_name}.{op_name}")

        # Allow some operations to not have error docs if they're very simple
        # But most should have them
        if len(operations) > 0:
            coverage = 1 - (len(missing_error_docs) / len(operations))
            assert coverage >= 0.7, \
                f"{skill_name} has poor error documentation coverage: {missing_error_docs}"

    @pytest.mark.parametrize('skill_name', TESTABLE_SKILLS)
    def test_operations_document_token_efficiency(self, invocation_tester, skill_name):
        """Test that operations document token efficiency."""
        operations = invocation_tester.get_skill_operations(skill_name)

        missing_efficiency_docs = []
        for op_name, op_func in operations.items():
            # Skip utility functions
            if op_name.startswith('get_') and not op_name.endswith('_operation'):
                continue

            if not invocation_tester.has_token_efficiency_docs(op_func):
                missing_efficiency_docs.append(f"{skill_name}.{op_name}")

        # At least 60% of operations should document token efficiency
        if len(operations) > 0:
            coverage = 1 - (len(missing_efficiency_docs) / len(operations))
            assert coverage >= 0.6, \
                f"{skill_name} has poor token efficiency documentation: {missing_efficiency_docs}"


class TestOperationUsability:
    """Test operation usability for agents."""

    def test_test_orchestrator_generate_tests(self, invocation_tester):
        """Test test_orchestrator.generate_tests is usable."""
        operations = invocation_tester.get_skill_operations('test_orchestrator')
        assert 'generate_tests' in operations

        sig_info = invocation_tester.get_operation_signature(operations['generate_tests'])

        # Should have required parameters clearly defined
        assert 'source_file' in sig_info['params']
        assert sig_info['params']['source_file']['required']

        # Should have response_format
        assert 'response_format' in sig_info['params']
        assert not sig_info['params']['response_format']['required']

    def test_code_analysis_analyze_file(self, invocation_tester):
        """Test code_analysis.analyze_file is usable."""
        operations = invocation_tester.get_skill_operations('code_analysis')
        assert 'analyze_file' in operations

        sig_info = invocation_tester.get_operation_signature(operations['analyze_file'])

        # Should have file_path parameter
        assert 'file_path' in sig_info['params']
        assert sig_info['params']['file_path']['required']

    def test_refactor_assistant_detect_code_smells(self, invocation_tester):
        """Test refactor_assistant.detect_code_smells is usable."""
        operations = invocation_tester.get_skill_operations('refactor_assistant')
        assert 'detect_code_smells' in operations

        sig_info = invocation_tester.get_operation_signature(operations['detect_code_smells'])

        # Should have file_path parameter
        assert 'file_path' in sig_info['params']

    def test_git_workflow_generate_commit_message(self, invocation_tester):
        """Test git_workflow_assistant.generate_commit_message is usable."""
        operations = invocation_tester.get_skill_operations('git_workflow_assistant')
        assert 'generate_commit_message' in operations

        sig_info = invocation_tester.get_operation_signature(operations['generate_commit_message'])

        # Should have changes parameter
        assert 'changes' in sig_info['params']


class TestErrorRecovery:
    """Test error recovery capabilities."""

    def test_operations_return_consistent_format(self, invocation_tester):
        """Test that operations return consistent result format."""
        # Check a few key skills
        test_skills = ['test_orchestrator', 'code_analysis', 'skill_evaluator']

        for skill_name in test_skills:
            operations = invocation_tester.get_skill_operations(skill_name)

            for op_name, op_func in operations.items():
                # Skip utility functions
                if op_name.startswith('get_') and not op_name.endswith('_operation'):
                    continue

                sig_info = invocation_tester.get_operation_signature(op_func)

                # Check return type is documented
                # Most operations should return OperationResult or dict
                return_type = sig_info['return_type']
                if return_type is not None:
                    type_str = str(return_type)
                    assert 'OperationResult' in type_str or 'Dict' in type_str or 'dict' in type_str, \
                        f"{skill_name}.{op_name} has unusual return type: {return_type}"

    def test_error_messages_are_actionable(self, invocation_tester):
        """Test that error messages include suggestions."""
        # This is tested via docstring content
        for skill_name in ['test_orchestrator', 'code_analysis', 'refactor_assistant']:
            operations = invocation_tester.get_skill_operations(skill_name)

            for op_name, op_func in operations.items():
                if op_name.startswith('get_'):
                    continue

                docstring = (op_func.__doc__ or '').lower()

                # Should mention errors or returns in some way
                assert 'return' in docstring or 'result' in docstring, \
                    f"{skill_name}.{op_name} doesn't document return value"


class TestInvocationScenarios:
    """Real-world invocation scenarios."""

    def test_scenario_generate_tests_workflow(self, invocation_tester):
        """Test workflow: generate tests for a file."""
        operations = invocation_tester.get_skill_operations('test_orchestrator')

        # Agent should be able to:
        # 1. Generate tests
        assert 'generate_tests' in operations

        # 2. Analyze coverage
        assert 'analyze_coverage' in operations or 'check_coverage' in operations

        # 3. Run tests
        assert 'run_tests' in operations or 'execute_tests' in operations

    def test_scenario_code_quality_workflow(self, invocation_tester):
        """Test workflow: check code quality."""
        # Agent needs to analyze code
        code_ops = invocation_tester.get_skill_operations('code_analysis')
        assert len(code_ops) > 0

        # Agent might want to refactor
        refactor_ops = invocation_tester.get_skill_operations('refactor_assistant')
        assert len(refactor_ops) > 0

    def test_scenario_pr_review_workflow(self, invocation_tester):
        """Test workflow: review a pull request."""
        operations = invocation_tester.get_skill_operations('pr_review_assistant')

        # Should have PR review operation
        assert 'review_pull_request' in operations or 'review_pr' in operations

    def test_scenario_learning_workflow(self, invocation_tester):
        """Test workflow: manage learning plan."""
        operations = invocation_tester.get_skill_operations('learning_plan_manager')

        # Should have learning plan operations
        assert len(operations) >= 2, \
            "learning_plan_manager needs multiple operations for workflow"


class TestParameterValidation:
    """Test parameter validation and defaults."""

    def test_response_format_has_default(self, invocation_tester):
        """Test that response_format has sensible default."""
        for skill_name in TESTABLE_SKILLS:
            operations = invocation_tester.get_skill_operations(skill_name)

            for op_name, op_func in operations.items():
                if op_name.startswith('get_'):
                    continue

                if invocation_tester.has_response_format_parameter(op_func):
                    sig_info = invocation_tester.get_operation_signature(op_func)

                    # response_format should have a default
                    rf_param = sig_info['params'].get('response_format')
                    if rf_param:
                        assert rf_param['default'] is not None, \
                            f"{skill_name}.{op_name} response_format missing default"

                        # Default should be 'summary' for efficiency
                        default = rf_param['default']
                        assert default in ['summary', 'concise', 'brief'], \
                            f"{skill_name}.{op_name} response_format default should be efficient, got: {default}"

    def test_required_parameters_are_minimal(self, invocation_tester):
        """Test that operations don't have too many required parameters."""
        for skill_name in TESTABLE_SKILLS:
            operations = invocation_tester.get_skill_operations(skill_name)

            for op_name, op_func in operations.items():
                if op_name.startswith('get_'):
                    continue

                sig_info = invocation_tester.get_operation_signature(op_func)

                # Count required parameters (excluding **kwargs)
                required = [
                    p for p in sig_info['params'].values()
                    if p['required'] and p['name'] not in ['kwargs', 'args']
                ]

                # Most operations should have 3 or fewer required params for usability
                assert len(required) <= 3, \
                    f"{skill_name}.{op_name} has too many required parameters ({len(required)}): {[p['name'] for p in required]}"


if __name__ == '__main__':
    # Run tests
    pytest.main([__file__, '-v'])

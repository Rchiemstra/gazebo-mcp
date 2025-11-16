"""
Test Validator

Validates test quality and coverage.
"""

import ast
from typing import Dict, List, Any, Set
from dataclasses import dataclass, field


@dataclass
class TestValidationResult:
    """Result of test validation"""
    is_valid: bool
    test_count: int = 0
    coverage_functions: Set[str] = field(default_factory=set)
    issues: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)


class TestValidator:
    """Validates test code quality"""

    def validate_tests(self, test_code: str, source_code: Optional[str] = None) -> TestValidationResult:
        """
        Validate test code.

        Args:
            test_code: Test code to validate
            source_code: Optional source code being tested (for coverage analysis)

        Returns:
            TestValidationResult
        """
        issues = []
        test_count = 0
        coverage_functions = set()
        metrics = {}

        try:
            tree = ast.parse(test_code)

            # Find all test functions
            test_functions = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                    test_functions.append(node)
                    test_count += 1

            if test_count == 0:
                issues.append("No test functions found (functions should start with 'test_')")

            # Analyze each test function
            for test_func in test_functions:
                # Check for assertions
                has_assertions = any(
                    isinstance(node, ast.Assert) or
                    (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and
                     hasattr(node.value.func, 'attr') and node.value.func.attr.startswith('assert'))
                    for node in ast.walk(test_func)
                )

                if not has_assertions:
                    issues.append(f"Test '{test_func.name}' has no assertions")

                # Check for docstring
                if not ast.get_docstring(test_func):
                    issues.append(f"Test '{test_func.name}' missing docstring")

            # If source code provided, check coverage
            if source_code:
                coverage_functions = self._check_coverage(test_code, source_code)
                source_tree = ast.parse(source_code)
                source_functions = {
                    node.name for node in ast.walk(source_tree)
                    if isinstance(node, ast.FunctionDef) and not node.name.startswith('_')
                }

                uncovered = source_functions - coverage_functions
                if uncovered:
                    issues.append(f"Functions not covered by tests: {uncovered}")

                metrics['coverage_ratio'] = len(coverage_functions) / len(source_functions) if source_functions else 0.0

            # Calculate metrics
            metrics.update({
                'test_count': test_count,
                'tests_with_assertions': sum(
                    1 for func in test_functions
                    if any(isinstance(node, ast.Assert) for node in ast.walk(func))
                ),
                'tests_with_docstrings': sum(
                    1 for func in test_functions
                    if ast.get_docstring(func)
                )
            })

            # Determine if valid
            is_valid = test_count > 0 and not any('has no assertions' in issue for issue in issues)

            return TestValidationResult(
                is_valid=is_valid,
                test_count=test_count,
                coverage_functions=coverage_functions,
                issues=issues,
                metrics=metrics
            )

        except SyntaxError as e:
            return TestValidationResult(
                is_valid=False,
                issues=[f"Syntax error in test code: {e}"]
            )

    def _check_coverage(self, test_code: str, source_code: str) -> Set[str]:
        """
        Check which functions are covered by tests.

        Args:
            test_code: Test code
            source_code: Source code

        Returns:
            Set of covered function names
        """
        covered = set()

        try:
            test_tree = ast.parse(test_code)
            source_tree = ast.parse(source_code)

            # Get source function names
            source_functions = {
                node.name for node in ast.walk(source_tree)
                if isinstance(node, ast.FunctionDef)
            }

            # Find function calls in tests
            for node in ast.walk(test_tree):
                if isinstance(node, ast.Call):
                    if hasattr(node.func, 'id') and node.func.id in source_functions:
                        covered.add(node.func.id)
                    elif hasattr(node.func, 'attr') and node.func.attr in source_functions:
                        covered.add(node.func.attr)

        except (SyntaxError, AttributeError):
            pass

        return covered

    def suggest_missing_tests(self, source_code: str, test_code: Optional[str] = None) -> List[str]:
        """
        Suggest missing test cases.

        Args:
            source_code: Source code to analyze
            test_code: Optional existing test code

        Returns:
            List of suggestions for missing tests
        """
        suggestions = []

        try:
            tree = ast.parse(source_code)

            # Find all functions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
                    func_name = node.name

                    # Check if function is tested
                    if test_code:
                        test_tree = ast.parse(test_code)
                        is_tested = any(
                            func_name in ast.unparse(test_node) if hasattr(ast, 'unparse') else True
                            for test_node in ast.walk(test_tree)
                            if isinstance(test_node, ast.FunctionDef) and test_node.name.startswith('test_')
                        )

                        if not is_tested:
                            suggestions.append(f"Add test for function '{func_name}'")

                    # Suggest edge case tests
                    has_conditionals = any(isinstance(n, (ast.If, ast.While, ast.For)) for n in ast.walk(node))
                    if has_conditionals:
                        suggestions.append(f"Add edge case tests for '{func_name}' (has conditional logic)")

                    # Suggest error handling tests
                    has_exception_handling = any(isinstance(n, ast.Try) for n in ast.walk(node))
                    if has_exception_handling:
                        suggestions.append(f"Add exception handling tests for '{func_name}'")

        except SyntaxError:
            pass

        return suggestions

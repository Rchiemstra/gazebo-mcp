"""
Test Generator for Test Orchestrator

Generates pytest test scaffolds from code analysis.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from .analyzer import FunctionInfo, ClassInfo, AnalysisResult


@dataclass
class GeneratedTest:
    """Information about a generated test."""
    test_name: str
    test_code: str
    purpose: str
    test_type: str  # unit, integration, edge_case


@dataclass
class TestSuite:
    """A complete test suite for a module."""
    file_path: str
    imports: List[str]
    fixtures: List[str]
    tests: List[GeneratedTest]


class TestGenerator:
    """Generates pytest test code from analysis results."""

    def generate_tests(self, analysis: AnalysisResult, target_coverage: float = 80.0) -> TestSuite:
        """
        Generate comprehensive test suite from analysis.

        Args:
            analysis: Analysis result from CodeAnalyzer
            target_coverage: Desired coverage percentage (default 80%)

        Returns:
            TestSuite with generated tests
        """
        imports = self._generate_imports(analysis)
        fixtures = self._generate_fixtures(analysis)
        tests = []

        # Generate tests for module-level functions
        for func in analysis.functions:
            tests.extend(self._generate_function_tests(func))

        # Generate tests for class methods
        for cls in analysis.classes:
            for method in cls.methods:
                tests.extend(self._generate_method_tests(cls.name, method))

        return TestSuite(
            file_path=self._get_test_file_path(analysis.file_path),
            imports=imports,
            fixtures=fixtures,
            tests=tests
        )

    def generate_test_file(self, test_suite: TestSuite) -> str:
        """
        Generate complete test file content.

        Args:
            test_suite: TestSuite with generated tests

        Returns:
            Complete test file as string
        """
        lines = []

        # Imports
        lines.append('"""Generated tests."""')
        lines.append("")
        for imp in test_suite.imports:
            lines.append(imp)
        lines.append("")

        # Fixtures
        if test_suite.fixtures:
            lines.append("")
            for fixture in test_suite.fixtures:
                lines.append(fixture)
                lines.append("")

        # Tests
        for test in test_suite.tests:
            lines.append("")
            lines.append(test.test_code)
            lines.append("")

        return "\n".join(lines)

    def _generate_imports(self, analysis: AnalysisResult) -> List[str]:
        """Generate necessary imports for tests."""
        imports = [
            "import pytest",
            "from unittest.mock import Mock, patch, MagicMock",
        ]

        # Add import for the module being tested
        module_path = Path(analysis.file_path)
        if "src" in module_path.parts:
            # Convert src/services/payment.py -> from src.services.payment import ...
            parts = list(module_path.parts)
            src_index = parts.index("src")
            module_parts = parts[src_index:-1]  # Exclude .py extension
            module_name = module_path.stem
            import_path = ".".join(module_parts + [module_name])
        else:
            # Simple case
            import_path = module_path.stem

        imports.append(f"from {import_path} import *")

        return imports

    def _generate_fixtures(self, analysis: AnalysisResult) -> List[str]:
        """Generate pytest fixtures for common dependencies."""
        fixtures = []

        # Identify common dependencies
        all_deps = set()
        for func in analysis.functions:
            all_deps.update(func.dependencies)
        for cls in analysis.classes:
            for method in cls.methods:
                all_deps.update(method.dependencies)

        # Generate mock fixtures for dependencies
        for dep in sorted(all_deps):
            if dep not in ['self', 'cls', 'super'] and not dep.startswith('_'):
                fixture_code = f'''@pytest.fixture
def mock_{dep.lower()}():
    """Mock {dep} for testing."""
    mock = Mock(spec={dep})
    return mock'''
                fixtures.append(fixture_code)

        return fixtures

    def _generate_function_tests(self, func: FunctionInfo) -> List[GeneratedTest]:
        """Generate tests for a function."""
        tests = []

        # 1. Happy path test
        tests.append(self._generate_happy_path_test(func))

        # 2. Edge case tests
        if "null_check" in func.edge_cases:
            tests.append(self._generate_null_check_test(func))

        if "boundary_condition" in func.edge_cases:
            tests.append(self._generate_boundary_test(func))

        if "empty_collection" in func.edge_cases:
            tests.append(self._generate_empty_collection_test(func))

        # 3. Exception tests
        for exception in func.raises:
            tests.append(self._generate_exception_test(func, exception))

        # 4. Parametrized test for multiple inputs
        if len(func.params) > 0:
            tests.append(self._generate_parametrized_test(func))

        return tests

    def _generate_method_tests(self, class_name: str, method: FunctionInfo) -> List[GeneratedTest]:
        """Generate tests for a class method."""
        # Similar to function tests but with class context
        return self._generate_function_tests(method)

    def _generate_happy_path_test(self, func: FunctionInfo) -> GeneratedTest:
        """Generate basic happy path test."""
        test_name = f"test_{func.name}_success"

        # Generate sample parameters
        params = self._generate_sample_params(func.params)
        param_str = ", ".join(f"{p}={v}" for p, v in params.items())

        # Generate assertion based on return type
        if func.returns and func.returns != "None":
            assertion = "assert result is not None"
            if "bool" in func.returns.lower():
                assertion = "assert isinstance(result, bool)"
            elif "str" in func.returns.lower():
                assertion = "assert isinstance(result, str)"
            elif "int" in func.returns.lower():
                assertion = "assert isinstance(result, int)"
            elif "list" in func.returns.lower():
                assertion = "assert isinstance(result, list)"
            elif "dict" in func.returns.lower():
                assertion = "assert isinstance(result, dict)"
        else:
            assertion = "# No return value to assert"

        test_code = f'''def {test_name}():
    """Test {func.name} with valid inputs."""
    result = {func.name}({param_str})
    {assertion}'''

        return GeneratedTest(
            test_name=test_name,
            test_code=test_code,
            purpose=f"Test {func.name} with valid inputs",
            test_type="unit"
        )

    def _generate_null_check_test(self, func: FunctionInfo) -> GeneratedTest:
        """Generate test for None/null parameter."""
        test_name = f"test_{func.name}_with_none"

        if func.params:
            first_param = func.params[0]
            test_code = f'''def {test_name}():
    """Test {func.name} with None parameter."""
    with pytest.raises(Exception):  # TODO: Specify exact exception
        {func.name}({first_param}=None)'''
        else:
            test_code = f'''def {test_name}():
    """Test {func.name} handles None correctly."""
    # TODO: Implement None handling test
    pass'''

        return GeneratedTest(
            test_name=test_name,
            test_code=test_code,
            purpose=f"Test {func.name} with None parameter",
            test_type="edge_case"
        )

    def _generate_boundary_test(self, func: FunctionInfo) -> GeneratedTest:
        """Generate boundary condition test."""
        test_name = f"test_{func.name}_boundary_conditions"

        test_code = f'''def {test_name}():
    """Test {func.name} with boundary values."""
    # Test minimum boundary
    # TODO: Add minimum value test

    # Test maximum boundary
    # TODO: Add maximum value test

    # Test zero/empty
    # TODO: Add zero/empty test'''

        return GeneratedTest(
            test_name=test_name,
            test_code=test_code,
            purpose=f"Test {func.name} with boundary values",
            test_type="edge_case"
        )

    def _generate_empty_collection_test(self, func: FunctionInfo) -> GeneratedTest:
        """Generate empty collection test."""
        test_name = f"test_{func.name}_empty_collection"

        test_code = f'''def {test_name}():
    """Test {func.name} with empty collection."""
    result = {func.name}([])  # TODO: Adjust parameter
    # TODO: Add assertion for empty collection handling'''

        return GeneratedTest(
            test_name=test_name,
            test_code=test_code,
            purpose=f"Test {func.name} with empty collection",
            test_type="edge_case"
        )

    def _generate_exception_test(self, func: FunctionInfo, exception: str) -> GeneratedTest:
        """Generate exception handling test."""
        test_name = f"test_{func.name}_raises_{exception.lower()}"

        params = self._generate_sample_params(func.params)
        param_str = ", ".join(f"{p}={v}" for p, v in params.items())

        test_code = f'''def {test_name}():
    """Test {func.name} raises {exception}."""
    with pytest.raises({exception}):
        # TODO: Set up conditions that trigger {exception}
        {func.name}({param_str})'''

        return GeneratedTest(
            test_name=test_name,
            test_code=test_code,
            purpose=f"Test {func.name} raises {exception}",
            test_type="exception"
        )

    def _generate_parametrized_test(self, func: FunctionInfo) -> GeneratedTest:
        """Generate parametrized test with multiple inputs."""
        test_name = f"test_{func.name}_parametrized"

        # Generate sample test cases
        param_names = ", ".join(func.params) if func.params else "input_val"
        test_cases = self._generate_test_cases(func)

        test_code = f'''@pytest.mark.parametrize("{param_names}, expected", [
    {test_cases}
])
def {test_name}({param_names}, expected):
    """Test {func.name} with various inputs."""
    result = {func.name}({param_names})
    assert result == expected  # TODO: Adjust assertion'''

        return GeneratedTest(
            test_name=test_name,
            test_code=test_code,
            purpose=f"Test {func.name} with multiple input combinations",
            test_type="parametrized"
        )

    def _generate_sample_params(self, params: List[str]) -> dict:
        """Generate sample parameter values."""
        sample_params = {}
        for param in params:
            # Simple heuristics for parameter values
            if 'id' in param.lower():
                sample_params[param] = '"test_id_123"'
            elif 'name' in param.lower():
                sample_params[param] = '"test_name"'
            elif 'amount' in param.lower() or 'price' in param.lower():
                sample_params[param] = '100.0'
            elif 'count' in param.lower() or 'num' in param.lower():
                sample_params[param] = '5'
            elif 'email' in param.lower():
                sample_params[param] = '"test@example.com"'
            elif 'data' in param.lower():
                sample_params[param] = '{}'
            elif 'items' in param.lower() or 'list' in param.lower():
                sample_params[param] = '[]'
            else:
                sample_params[param] = 'None  # TODO: Provide value'

        return sample_params

    def _generate_test_cases(self, func: FunctionInfo) -> str:
        """Generate sample test cases for parametrized tests."""
        # Generate 3 sample test cases
        cases = [
            '# TODO: Add real test cases',
            '# (input1, input2, expected_output),',
            '# (input1, input2, expected_output),',
            '# (input1, input2, expected_output),',
        ]
        return "\n    ".join(cases)

    def _get_test_file_path(self, source_path: str) -> str:
        """Convert source file path to test file path."""
        path = Path(source_path)

        # Convert src/services/payment.py -> tests/test_payment.py
        # or src/services/payment.py -> tests/services/test_payment.py
        if "src" in path.parts:
            parts = list(path.parts)
            src_index = parts.index("src")
            # Replace 'src' with 'tests'
            test_parts = ["tests"] + parts[src_index + 1:-1]
            test_file = f"test_{path.stem}.py"
            return str(Path(*test_parts) / test_file)
        else:
            # Simple case: payment.py -> test_payment.py
            return f"test_{path.stem}.py"

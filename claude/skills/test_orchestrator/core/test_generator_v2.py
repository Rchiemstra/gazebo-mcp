"""
Enhanced Test Generator for Test Orchestrator (V2)

Improvements:
- Smart parameter value inference
- Better fixture generation (only what's needed)
- More complete test implementations
- Better assertions
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Set, Dict
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.analyzer import FunctionInfo, ClassInfo, AnalysisResult
from utils.parameter_inference import ParameterInference, ParameterHint


@dataclass
class GeneratedTest:
    """Information about a generated test."""
    test_name: str
    test_code: str
    purpose: str
    test_type: str  # unit, integration, edge_case
    completeness: float  # 0.0 to 1.0


@dataclass
class TestSuite:
    """A complete test suite for a module."""
    file_path: str
    imports: List[str]
    fixtures: List[str]
    tests: List[GeneratedTest]
    completeness_score: float = 0.0


class EnhancedTestGenerator:
    """Enhanced test generator with smart inference."""

    def __init__(self):
        self.param_inference = ParameterInference()

    def _clean_param_value(self, value: str) -> str:
        """Clean parameter value to avoid syntax errors."""
        # Remove inline TODO comments that break syntax
        value = value.replace(" # TODO: Provide value", "")
        # Strip and ensure it's not just whitespace
        value = value.strip()
        if not value or value == "":
            return "None"
        return value

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

        # Smart fixture generation - only for actual dependencies
        fixtures = self._generate_smart_fixtures(analysis)

        tests = []

        # Generate tests for module-level functions
        for func in analysis.functions:
            tests.extend(self._generate_function_tests(func, analysis))

        # Generate tests for class methods
        for cls in analysis.classes:
            for method in cls.methods:
                tests.extend(self._generate_method_tests(cls.name, method, analysis))

        # Calculate completeness
        completeness = sum(t.completeness for t in tests) / len(tests) if tests else 0.0

        return TestSuite(
            file_path=self._get_test_file_path(analysis.file_path),
            imports=imports,
            fixtures=fixtures,
            tests=tests,
            completeness_score=completeness
        )

    def generate_test_file(self, test_suite: TestSuite) -> str:
        """Generate complete test file content."""
        lines = []

        # Header
        lines.append('"""')
        lines.append('Generated tests - Enhanced Version')
        lines.append('')
        lines.append(f'Completeness Score: {test_suite.completeness_score:.1%}')
        lines.append(f'Total Tests: {len(test_suite.tests)}')
        lines.append('"""')
        lines.append("")

        # Imports
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

        return "\n".join(lines)

    def _generate_imports(self, analysis: AnalysisResult) -> List[str]:
        """Generate necessary imports for tests."""
        imports = [
            "import pytest",
            "from unittest.mock import Mock, patch, MagicMock, call",
        ]

        # Add import for the module being tested
        module_path = Path(analysis.file_path)
        module_name = module_path.stem
        imports.append(f"from {module_name} import *")

        return imports

    def _generate_smart_fixtures(self, analysis: AnalysisResult) -> List[str]:
        """
        Generate only necessary fixtures based on actual usage.

        Filters out built-ins and commonly mocked types.
        """
        fixtures = []

        # Collect real dependencies (filter out built-ins and common types)
        all_deps = set()
        SKIP_DEPS = {
            'self', 'cls', 'super', 'str', 'int', 'float', 'bool', 'list', 'dict',
            'tuple', 'set', 'None', 'True', 'False', 'len', 'range', 'enumerate',
            'zip', 'map', 'filter', 'sum', 'max', 'min', 'round', 'abs', 'print'
        }

        for func in analysis.functions:
            all_deps.update(func.dependencies - SKIP_DEPS)
        for cls in analysis.classes:
            for method in cls.methods:
                all_deps.update(method.dependencies - SKIP_DEPS)

        # Generate fixtures for real dependencies only
        for dep in sorted(all_deps):
            if not dep.startswith('_') and dep not in SKIP_DEPS:
                # Check if it's likely a class (capitalized)
                if dep[0].isupper():
                    fixture_code = f'''@pytest.fixture
def mock_{dep.lower()}():
    """Mock {dep} for testing."""
    mock = Mock(spec={dep})
    return mock'''
                    fixtures.append(fixture_code)

        return fixtures

    def _generate_function_tests(self, func: FunctionInfo, analysis: AnalysisResult) -> List[GeneratedTest]:
        """Generate enhanced tests for a function."""
        tests = []

        # Context for parameter inference
        context = {
            'function_name': func.name,
            'module': Path(analysis.file_path).stem
        }

        # 1. Happy path test - enhanced
        tests.append(self._generate_happy_path_test_v2(func, context))

        # 2. Edge case tests - enhanced
        if "null_check" in func.edge_cases:
            tests.append(self._generate_null_check_test_v2(func, context))

        if "boundary_condition" in func.edge_cases:
            tests.append(self._generate_boundary_test_v2(func, context))

        if "empty_collection" in func.edge_cases:
            tests.append(self._generate_empty_collection_test_v2(func, context))

        # 3. Exception tests - enhanced
        for exception in func.raises:
            tests.append(self._generate_exception_test_v2(func, exception, context))

        # 4. Parametrized test - enhanced
        if len(func.params) > 0 and len(func.params) <= 3:  # Only for manageable param counts
            tests.append(self._generate_parametrized_test_v2(func, context))

        return tests

    def _generate_method_tests(self, class_name: str, method: FunctionInfo, analysis: AnalysisResult) -> List[GeneratedTest]:
        """Generate tests for a class method."""
        # Similar to function tests but with class context
        context = {
            'function_name': method.name,
            'class_name': class_name,
            'module': Path(analysis.file_path).stem
        }
        return self._generate_function_tests(method, analysis)

    def _generate_happy_path_test_v2(self, func: FunctionInfo, context: Dict) -> GeneratedTest:
        """Generate enhanced happy path test with smart parameter values."""
        test_name = f"test_{func.name}_success"

        # Smart parameter inference
        params_dict = {}
        for param in func.params:
            param_hint = ParameterHint(name=param)
            value = self.param_inference.infer_value(param_hint, context)
            params_dict[param] = self._clean_param_value(value)

        # Build parameter string
        if params_dict:
            param_str = ", ".join(f"{p}={v}" for p, v in params_dict.items())
        else:
            param_str = ""

        # Smart assertion based on return type
        if func.returns and func.returns != "None":
            if "bool" in func.returns.lower():
                assertion = "assert isinstance(result, bool)"
                extra_check = "# Result is a boolean"
            elif "str" in func.returns.lower():
                assertion = 'assert isinstance(result, str)\n    assert len(result) > 0  # Non-empty string'
                extra_check = ""
            elif "int" in func.returns.lower():
                assertion = "assert isinstance(result, int)\n    assert result >= 0  # Non-negative"
                extra_check = ""
            elif "float" in func.returns.lower():
                assertion = "assert isinstance(result, float)"
                extra_check = ""
            elif "list" in func.returns.lower():
                assertion = "assert isinstance(result, list)"
                extra_check = ""
            elif "dict" in func.returns.lower():
                assertion = 'assert isinstance(result, dict)\n    assert "status" in result  # Has status field'
                extra_check = ""
            else:
                assertion = "assert result is not None"
                extra_check = ""
        else:
            assertion = "# No return value to assert"
            extra_check = "# Verify no exceptions raised"

        test_code = f'''def {test_name}():
    """Test {func.name} with valid inputs."""
    result = {func.name}({param_str})
    {assertion}'''

        # Calculate completeness (100% for happy path if params are inferred)
        has_todos = "TODO" in param_str
        completeness = 0.6 if has_todos else 1.0

        return GeneratedTest(
            test_name=test_name,
            test_code=test_code,
            purpose=f"Test {func.name} with valid inputs",
            test_type="unit",
            completeness=completeness
        )

    def _generate_null_check_test_v2(self, func: FunctionInfo, context: Dict) -> GeneratedTest:
        """Generate enhanced null check test."""
        test_name = f"test_{func.name}_with_none_parameter"

        if func.params:
            first_param = func.params[0]

            # Generate other params with valid values
            other_params = {}
            for param in func.params[1:]:
                param_hint = ParameterHint(name=param)
                value = self.param_inference.infer_value(param_hint, context)
                other_params[param] = self._clean_param_value(value)

            other_param_str = ", ".join(f"{p}={v}" for p, v in other_params.items())
            param_str = f"{first_param}=None" + (f", {other_param_str}" if other_param_str else "")

            # Determine expected exception
            expected_exception = "ValueError"  # Default
            if "InvalidAmountError" in func.raises or "ValidationError" in func.raises:
                expected_exception = func.raises[0] if func.raises else "ValueError"

            test_code = f'''def {test_name}():
    """Test {func.name} raises error with None parameter."""
    with pytest.raises(({expected_exception}, TypeError)):
        {func.name}({param_str})'''
        else:
            test_code = f'''def {test_name}():
    """Test {func.name} handles None correctly."""
    # TODO: Define test for None parameter
    pass'''

        completeness = 0.9 if func.params else 0.3

        return GeneratedTest(
            test_name=test_name,
            test_code=test_code,
            purpose=f"Test {func.name} with None parameter",
            test_type="edge_case",
            completeness=completeness
        )

    def _generate_boundary_test_v2(self, func: FunctionInfo, context: Dict) -> GeneratedTest:
        """Generate enhanced boundary condition test."""
        test_name = f"test_{func.name}_boundary_conditions"

        # Find numeric parameters
        numeric_params = [p for p in func.params if 'amount' in p.lower() or 'count' in p.lower()
                         or 'num' in p.lower() or 'age' in p.lower() or 'price' in p.lower()]

        if numeric_params:
            param = numeric_params[0]
            param_hint = ParameterHint(name=param)
            boundaries = self.param_inference.infer_boundary_values(param_hint)

            # Generate other params
            other_params = {}
            for p in func.params:
                if p != param:
                    value = self.param_inference.infer_value(ParameterHint(name=p), context)
                    other_params[p] = self._clean_param_value(value)

            other_str = ", ".join(f"{p}={v}" for p, v in other_params.items())
            other_suffix = f", {other_str}" if other_str else ""

            test_code = f'''def {test_name}():
    """Test {func.name} with boundary values."""
    # Test minimum boundary
    result_min = {func.name}({param}={boundaries.get("min", "0")}{other_suffix})
    assert result_min is not None

    # Test maximum reasonable value
    result_max = {func.name}({param}={boundaries.get("max", "1000000")}{other_suffix})
    assert result_max is not None

    # Test zero/edge case
    try:
        {func.name}({param}={boundaries.get("zero", "0")}{other_suffix})
    except Exception:
        pass  # May raise exception for zero value'''

            completeness = 0.85
        else:
            test_code = f'''def {test_name}():
    """Test {func.name} with boundary values."""
    # TODO: Add boundary value tests
    pass'''
            completeness = 0.2

        return GeneratedTest(
            test_name=test_name,
            test_code=test_code,
            purpose=f"Test {func.name} with boundary values",
            test_type="edge_case",
            completeness=completeness
        )

    def _generate_empty_collection_test_v2(self, func: FunctionInfo, context: Dict) -> GeneratedTest:
        """Generate enhanced empty collection test."""
        test_name = f"test_{func.name}_empty_collection"

        # Find collection parameters
        collection_params = [p for p in func.params if 'items' in p.lower() or 'list' in p.lower()
                            or 'data' in p.lower() or p.endswith('s')]

        if collection_params:
            param = collection_params[0]

            # Generate other params
            other_params = {}
            for p in func.params:
                if p != param:
                    value = self.param_inference.infer_value(ParameterHint(name=p), context)
                    other_params[p] = self._clean_param_value(value)

            other_str = ", ".join(f"{p}={v}" for p, v in other_params.items())
            other_suffix = f", {other_str}" if other_str else ""

            test_code = f'''def {test_name}():
    """Test {func.name} with empty collection."""
    result = {func.name}({param}=[]{other_suffix})
    # Should handle empty collection gracefully
    assert result is not None or result == [] or result == {{}}'''

            completeness = 0.8
        else:
            test_code = f'''def {test_name}():
    """Test {func.name} with empty collection."""
    # TODO: Identify collection parameter and test
    pass'''
            completeness = 0.2

        return GeneratedTest(
            test_name=test_name,
            test_code=test_code,
            purpose=f"Test {func.name} with empty collection",
            test_type="edge_case",
            completeness=completeness
        )

    def _generate_exception_test_v2(self, func: FunctionInfo, exception: str, context: Dict) -> GeneratedTest:
        """Generate enhanced exception test."""
        test_name = f"test_{func.name}_raises_{exception.lower()}"

        # Smart parameter values that trigger the exception
        params_dict = {}

        # Heuristics for exception-triggering values
        for param in func.params:
            if "amount" in param.lower() and "InvalidAmount" in exception:
                params_dict[param] = "-10.00"  # Negative amount
            elif "id" in param.lower() and "NotFound" in exception:
                params_dict[param] = '"nonexistent_id"'
            else:
                param_hint = ParameterHint(name=param)
                value = self.param_inference.infer_value(param_hint, context)
                params_dict[param] = self._clean_param_value(value)

        param_str = ", ".join(f"{p}={v}" for p, v in params_dict.items())

        test_code = f'''def {test_name}():
    """Test {func.name} raises {exception} appropriately."""
    with pytest.raises({exception}):
        {func.name}({param_str})'''

        completeness = 0.7  # Good but may need adjustment for specific trigger

        return GeneratedTest(
            test_name=test_name,
            test_code=test_code,
            purpose=f"Test {func.name} raises {exception}",
            test_type="exception",
            completeness=completeness
        )

    def _generate_parametrized_test_v2(self, func: FunctionInfo, context: Dict) -> GeneratedTest:
        """Generate enhanced parametrized test with realistic values."""
        test_name = f"test_{func.name}_various_inputs"

        # Generate multiple test cases
        test_cases = []
        param_names = func.params

        # Generate 3-5 realistic test cases
        for i in range(min(3, len(param_names) + 1)):
            case_values = []
            for param in param_names:
                param_hint = ParameterHint(name=param)
                values = self.param_inference.infer_multiple_values(param_hint, 3)
                case_values.append(values[min(i, len(values) - 1)])

            # Add expected result (placeholder)
            case_values.append("True")  # Placeholder expected value
            test_cases.append(f"    ({', '.join(case_values)})")

        param_list = ", ".join(param_names)
        test_cases_str = ",\n".join(test_cases)

        test_code = f'''@pytest.mark.parametrize("{param_list}, expected", [
{test_cases_str},
])
def {test_name}({param_list}, expected):
    """Test {func.name} with various input combinations."""
    result = {func.name}({param_list})
    # TODO: Adjust assertion based on expected behavior
    assert result is not None'''

        completeness = 0.6  # Need manual expected values

        return GeneratedTest(
            test_name=test_name,
            test_code=test_code,
            purpose=f"Test {func.name} with multiple input combinations",
            test_type="parametrized",
            completeness=completeness
        )

    def _get_test_file_path(self, source_path: str) -> str:
        """Convert source file path to test file path."""
        path = Path(source_path)
        return f"test_{path.stem}.py"

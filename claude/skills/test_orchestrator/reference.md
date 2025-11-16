# Test Orchestrator - API Reference

Complete documentation for all test_orchestrator operations.

---

## Overview

Test Orchestrator provides intelligent test generation and coverage analysis for Python code. It uses AST (Abstract Syntax Tree) analysis to understand code structure and generate comprehensive pytest test suites.

---

## Operations

### analyze_file

Analyze a Python source file to identify testable components.

#### Signature

```python
def analyze_file(
    source_file: str,
    response_format: str = "summary",
    **kwargs
) -> OperationResult
```

#### Parameters

**source_file** (str, required)
- Path to the Python source file to analyze
- Can be relative or absolute path
- Must exist and be readable

**response_format** (str, optional, default="summary")
- Controls the detail level of the response
- Options:
  - `"summary"` - Counts, names, and high-level statistics (200-500 tokens)
  - `"detailed"` - Full function details, parameters, edge cases (2000-5000 tokens)

#### Returns

**OperationResult** with the following data structure:

**Summary format:**
```python
{
    "success": True,
    "data": {
        "source_file": "src/payment.py",
        "total_functions": 12,
        "total_classes": 3,
        "total_complexity": 45,
        "avg_complexity": 3.75,
        "function_names": ["process_payment", "validate_card", ...],
        "class_names": ["PaymentProcessor", "CardValidator", ...],
        "most_complex_function": "process_payment",
        "efficiency_tip": "Analysis complete! Found 12 functions..."
    }
}
```

**Detailed format:**
```python
{
    "success": True,
    "data": {
        "source_file": "src/payment.py",
        "total_functions": 12,
        "total_classes": 3,
        "total_complexity": 45,
        "avg_complexity": 3.75,
        "functions": [
            {
                "name": "process_payment",
                "line_number": 45,
                "complexity": 8,
                "parameters": [
                    {"name": "amount", "type": "float"},
                    {"name": "card", "type": "CreditCard"}
                ],
                "return_type": "PaymentResult",
                "raises": ["ValueError", "PaymentError"],
                "edge_cases": [
                    "amount is negative",
                    "amount is zero",
                    "card is expired"
                ],
                "dependencies": ["CreditCard", "PaymentResult"]
            },
            ...
        ],
        "classes": [
            {
                "name": "PaymentProcessor",
                "line_number": 10,
                "base_classes": ["ABC"],
                "methods": ["process", "validate", "refund"]
            },
            ...
        ],
        "imports": ["typing", "datetime", "decimal"]
    }
}
```

#### Error Handling

**FILE_NOT_FOUND:**
```python
{
    "success": False,
    "error": "Cannot find source file: nonexistent.py",
    "error_code": "FILE_NOT_FOUND",
    "suggestions": [
        "Check if the file path is correct",
        "Use Glob('**/*.py') to find Python files",
        "Verify the file exists with Bash('ls -la src/')"
    ],
    "example_fix": "analyze_file('src/services/payment.py')"
}
```

**SYNTAX_ERROR:**
```python
{
    "success": False,
    "error": "Python syntax error in payment.py at line 45: invalid syntax",
    "error_code": "SYNTAX_ERROR",
    "suggestions": [
        "Check for missing colons, parentheses, or quotes",
        "Run python -m py_compile payment.py to see full error",
        "Fix syntax errors before analysis"
    ],
    "example_fix": "Fix syntax errors, then retry: analyze_file('payment.py')"
}
```

#### Token Efficiency

- **Summary format:** 200-500 tokens (most common use case)
- **Detailed format:** 2000-5000 tokens (when you need full details)
- **Savings:** Up to 90% for large files with summary format

**Best Practice:**
1. Start with summary to get overview
2. Use detailed only when you need specific function details
3. For large files (>20 functions), always use summary first

---

### generate_tests

Generate pytest test cases for a Python source file.

#### Signature

```python
def generate_tests(
    source_file: str,
    target_coverage: float = 80.0,
    response_format: str = "concise",
    **kwargs
) -> OperationResult
```

#### Parameters

**source_file** (str, required)
- Path to the Python source file to generate tests for
- Must exist and be valid Python code

**target_coverage** (float, optional, default=80.0)
- Target code coverage percentage (0-100)
- Higher values generate more comprehensive tests
- Affects number of edge case tests generated

**response_format** (str, optional, default="concise")
- Controls the detail level of the response
- Options:
  - `"concise"` - Summary only, no test code in response (300-600 tokens)
  - `"detailed"` - Full test code included in response (5000-10000 tokens)

**Note:** In both formats, tests are **written to disk**. The difference is whether the test code is also **returned in the response**.

#### Returns

**OperationResult** with the following data structure:

**Concise format (default):**
```python
{
    "success": True,
    "data": {
        "tests_generated": 15,
        "coverage_estimate": 85.0,
        "quality_score": 0.82,
        "test_file": "tests/test_payment.py",
        "functions_tested": 12,
        "edge_cases_covered": 23,
        "fixtures_created": 5,
        "efficiency_tip": "Generated 15 tests (estimated 4800 tokens saved)...",
        "next_step": "Run tests with: pytest tests/test_payment.py -v"
    }
}
```

**Detailed format:**
```python
{
    "success": True,
    "data": {
        "tests_generated": 15,
        "coverage_estimate": 85.0,
        "quality_score": 0.82,
        "test_file": "tests/test_payment.py",
        "test_content": "import pytest\n\n@pytest.fixture\ndef payment_processor():\n...",
        "functions_tested": 12,
        "edge_cases_covered": 23,
        "fixtures_created": 5,
        "test_breakdown": [
            {
                "function": "process_payment",
                "tests": ["test_process_payment_success", "test_process_payment_negative_amount"],
                "edge_cases": ["negative amount", "zero amount", "expired card"]
            },
            ...
        ]
    }
}
```

#### Generated Test Structure

Tests include:
- **Pytest fixtures** for common test data
- **Parametrized tests** for edge cases
- **Assertions** for expected behavior
- **Exception testing** for error conditions
- **Mocks** for external dependencies
- **Type hints** for clarity

Example generated test:
```python
import pytest
from src.payment import PaymentProcessor

@pytest.fixture
def payment_processor():
    """Fixture providing a PaymentProcessor instance."""
    return PaymentProcessor()

def test_process_payment_success(payment_processor):
    """Test successful payment processing."""
    result = payment_processor.process(100.0, valid_card())
    assert result.success is True
    assert result.amount == 100.0

@pytest.mark.parametrize("amount", [-100, 0, -0.01])
def test_process_payment_invalid_amount(payment_processor, amount):
    """Test payment processing with invalid amounts."""
    with pytest.raises(ValueError):
        payment_processor.process(amount, valid_card())
```

#### Error Handling

**FILE_NOT_FOUND:**
```python
{
    "success": False,
    "error": "Cannot find source file: nonexistent.py",
    "error_code": "FILE_NOT_FOUND",
    "suggestions": [
        "Check if the file path is correct",
        "Use Glob('**/*.py') to find Python files",
        "Verify the file exists"
    ],
    "example_fix": "generate_tests('src/services/payment.py')"
}
```

**INVALID_COVERAGE:**
```python
{
    "success": False,
    "error": "Invalid target coverage: 150. Must be between 0 and 100",
    "error_code": "INVALID_COVERAGE",
    "suggestions": [
        "Use coverage between 70-90 for normal cases",
        "Use 90-100 for critical code",
        "Use 50-70 for exploratory testing"
    ],
    "example_fix": "generate_tests('payment.py', target_coverage=85)"
}
```

#### Token Efficiency

- **Concise format:** 300-600 tokens (recommended default)
- **Detailed format:** 5000-10000 tokens (when reviewing test code)
- **Savings:** Up to 95% with concise format

**Best Practice:**
1. Use concise format (default) for normal test generation
2. Test file is written to disk in both cases
3. Use detailed format only when you need to review/modify test code
4. Review generated tests by reading the test file with Read tool

---

### analyze_coverage

Analyze test coverage and identify gaps.

#### Signature

```python
def analyze_coverage(
    test_file: str,
    source_file: str,
    response_format: str = "summary",
    **kwargs
) -> OperationResult
```

#### Parameters

**test_file** (str, required)
- Path to the test file (e.g., "tests/test_payment.py")
- Must be a valid Python test file

**source_file** (str, required)
- Path to the source file being tested
- Must exist and be valid Python code

**response_format** (str, optional, default="summary")
- Controls the detail level of the response
- Options:
  - `"summary"` - Coverage percentage and gap counts (200-400 tokens)
  - `"detailed"` - Specific missing functions, branches, edge cases (1000-3000 tokens)

#### Returns

**OperationResult** with the following data structure:

**Summary format:**
```python
{
    "success": True,
    "data": {
        "coverage_percent": 75.5,
        "lines_covered": 302,
        "lines_total": 400,
        "functions_covered": 10,
        "functions_total": 12,
        "branches_covered": 45,
        "branches_total": 60,
        "gap_summary": "2 functions and 15 branches not covered",
        "recommendation": "Focus on testing error handling paths"
    }
}
```

**Detailed format:**
```python
{
    "success": True,
    "data": {
        "coverage_percent": 75.5,
        "lines_covered": 302,
        "lines_total": 400,
        "functions_covered": 10,
        "functions_total": 12,
        "branches_covered": 45,
        "branches_total": 60,
        "missing_functions": [
            {
                "name": "handle_refund",
                "line_number": 156,
                "complexity": 5,
                "priority": "high"
            },
            {
                "name": "_validate_internal",
                "line_number": 203,
                "complexity": 2,
                "priority": "low"
            }
        ],
        "missing_branches": [
            {
                "function": "process_payment",
                "line_number": 78,
                "condition": "if amount > 1000",
                "branch": "false",
                "edge_case": "large payment validation"
            },
            ...
        ],
        "missing_edge_cases": [
            "negative amount",
            "zero amount",
            "expired card",
            "network timeout"
        ],
        "recommendations": [
            "Add tests for error handling in process_payment",
            "Test edge case: negative amounts",
            "Cover timeout scenarios with mocks"
        ]
    }
}
```

#### Error Handling

**FILE_NOT_FOUND:**
```python
{
    "success": False,
    "error": "Cannot find test file: test_nonexistent.py",
    "error_code": "FILE_NOT_FOUND",
    "suggestions": [
        "Check if the test file path is correct",
        "Generate tests first with generate_tests()",
        "Verify file exists with Bash('ls -la tests/')"
    ],
    "example_fix": "analyze_coverage('tests/test_payment.py', 'src/payment.py')"
}
```

**NO_COVERAGE_DATA:**
```python
{
    "success": False,
    "error": "No coverage data available. Run tests with coverage first.",
    "error_code": "NO_COVERAGE_DATA",
    "suggestions": [
        "Run: pytest --cov=src tests/",
        "Ensure pytest-cov is installed: pip install pytest-cov",
        "Check that tests actually execute"
    ],
    "example_fix": "Run pytest with coverage, then: analyze_coverage(...)"
}
```

#### Token Efficiency

- **Summary format:** 200-400 tokens (quick coverage check)
- **Detailed format:** 1000-3000 tokens (identify specific gaps)
- **Savings:** Up to 85% with summary format

**Best Practice:**
1. Use summary for quick coverage checks
2. Use detailed when coverage is below threshold
3. Focus on high-priority missing functions first

---

## Common Workflows

### Workflow 1: TDD (Test-Driven Development)

```python
# 1. Analyze source file
analysis = analyze_file("payment.py", response_format="summary")
print(f"Functions to test: {analysis.data['total_functions']}")

# 2. Generate comprehensive tests
tests = generate_tests("payment.py", target_coverage=90)
print(f"Generated: {tests.data['test_file']}")

# 3. Run tests (they should fail - no implementation yet)
# Bash("pytest tests/test_payment.py -v")

# 4. Implement code to make tests pass
# (user writes implementation)

# 5. Verify coverage
coverage = analyze_coverage("tests/test_payment.py", "payment.py")
print(f"Coverage: {coverage.data['coverage_percent']}%")
```

### Workflow 2: Legacy Code Testing

```python
# 1. Analyze complex legacy file
analysis = analyze_file("legacy_payment.py", response_format="detailed")

# 2. Start with high-complexity functions
complex_functions = [
    f for f in analysis.data['functions']
    if f['complexity'] > 5
]

# 3. Generate tests with moderate coverage
tests = generate_tests("legacy_payment.py", target_coverage=70)

# 4. Check what's missing
gaps = analyze_coverage(
    "tests/test_legacy_payment.py",
    "legacy_payment.py",
    response_format="detailed"
)

# 5. Incrementally add tests for gaps
for missing in gaps.data['missing_functions']:
    if missing['priority'] == 'high':
        print(f"TODO: Test {missing['name']} at line {missing['line_number']}")
```

### Workflow 3: Code Review Integration

```python
# Before merging PR, check test coverage
coverage = analyze_coverage("tests/test_new_feature.py", "new_feature.py")

if coverage.data['coverage_percent'] < 80:
    gaps = analyze_coverage(
        "tests/test_new_feature.py",
        "new_feature.py",
        response_format="detailed"
    )

    print("PR BLOCKED: Insufficient test coverage")
    print(f"Missing: {gaps.data['gap_summary']}")
    print("Recommendations:")
    for rec in gaps.data['recommendations']:
        print(f"  - {rec}")
```

---

## Best Practices

### 1. Start with Summary Format

Always start with summary/concise format to minimize token usage:

```python
# ✅ Good: Start light
analysis = analyze_file("file.py")  # Default: summary
tests = generate_tests("file.py")   # Default: concise

# ❌ Wasteful: Always detailed
analysis = analyze_file("file.py", response_format="detailed")  # 10x tokens!
```

### 2. Use Detailed Only When Needed

Request detailed format only for specific needs:

```python
# Check coverage first
coverage = analyze_coverage("test_payment.py", "payment.py")

# Only get details if coverage is low
if coverage.data['coverage_percent'] < 80:
    gaps = analyze_coverage(
        "test_payment.py",
        "payment.py",
        response_format="detailed"  # Now justified
    )
```

### 3. Target Coverage Based on Code Type

```python
# Critical code: high coverage
generate_tests("payment.py", target_coverage=95)

# Business logic: moderate coverage
generate_tests("reporting.py", target_coverage=85)

# Utilities: standard coverage
generate_tests("helpers.py", target_coverage=75)

# Experimental: light coverage
generate_tests("prototype.py", target_coverage=60)
```

### 4. Review Generated Tests

Always review and refine generated tests:

```python
# 1. Generate tests (concise - fast)
result = generate_tests("payment.py")

# 2. Review test file (use Read tool)
# Read(result.data['test_file'])

# 3. Refine as needed (use Edit tool)
# Edit(test_file, old="...", new="...")

# 4. Run to verify
# Bash("pytest tests/test_payment.py -v")
```

### 5. Iterate on Coverage

Don't aim for 100% immediately:

```python
# Iteration 1: Generate basic tests (70% coverage)
generate_tests("complex.py", target_coverage=70)

# Iteration 2: Check gaps
gaps = analyze_coverage("test_complex.py", "complex.py", response_format="detailed")

# Iteration 3: Add tests for critical gaps
# (manual or generate_tests for specific functions)

# Iteration 4: Reach target (85% coverage)
coverage = analyze_coverage("test_complex.py", "complex.py")
# coverage_percent: 85%
```

---

## Performance Notes

### Token Usage Summary

| Operation | Summary | Detailed | Savings |
|-----------|---------|----------|---------|
| analyze_file | 200-500 | 2000-5000 | 75-90% |
| generate_tests | 300-600 | 5000-10000 | 94-95% |
| analyze_coverage | 200-400 | 1000-3000 | 80-85% |

### Execution Time

- **analyze_file:** 0.1-0.5 seconds (typical)
- **generate_tests:** 0.5-2.0 seconds (depends on file size)
- **analyze_coverage:** 1.0-5.0 seconds (requires running tests)

### File Size Limits

- **Recommended:** < 1000 lines per file
- **Maximum:** < 5000 lines (may be slow)
- **For large files:** Split into modules first

---

## Related Skills

- **code_analysis** - Deeper code analysis (AST, dependencies, patterns)
- **pr_review_assistant** - Comprehensive code review including test quality
- **refactor_assistant** - Refactor code to improve testability

---

## Dependencies

### Required

- Python 3.8+
- AST standard library

### Optional (for full functionality)

- pytest (for test generation)
- pytest-cov (for coverage analysis)

---

*Last Updated: 2025-11-07*

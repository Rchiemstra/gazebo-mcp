---
name: test-orchestrator
description: Intelligent test generation and coverage analysis for Python code. Analyzes source files, generates pytest test cases, and identifies coverage gaps.
version: 1.0.0
category: testing
tags:
  - python
  - testing
  - coverage
  - pytest
  - quality-assurance
activation: manual
tools:
  - Read
  - Write
  - Bash
dependencies: []
---

# Test Orchestrator Skill

## When to Use This Skill

Use test-orchestrator when you need to:
- **Analyze Python files** for testable components (functions, classes, edge cases)
- **Generate test cases** automatically with pytest fixtures and assertions
- **Check test coverage** and identify gaps in existing test suites
- **Improve test quality** by detecting missing edge cases or untested scenarios
- **Accelerate TDD** by quickly scaffolding comprehensive test suites

## Quick Start

```python
from skills.test_orchestrator.operations import analyze_file, generate_tests

# 1. Analyze source file (summary format for efficiency)
result = analyze_file("src/payment.py")
print(f"Found {result.data['total_functions']} functions")

# 2. Generate tests (concise format: summary only, no code)
result = generate_tests("src/payment.py")
print(f"Generated {result.data['tests_generated']} tests")
print(f"Test file: {result.data['test_file']}")
```

For detailed documentation, see **reference.md**.
For usage examples, see **examples.md**.

## Operations

### analyze_file(source_file, response_format="summary")
Analyze Python source file to identify testable components.

**Returns:** Function/class counts, complexity metrics, and names (summary) or full details (detailed)

### generate_tests(source_file, target_coverage=80.0, response_format="concise")
Generate pytest test cases for a Python source file.

**Returns:** Test count, coverage estimate, test file path (concise) or full test code (detailed)

### analyze_coverage(test_file, source_file, response_format="summary")
Analyze test coverage and identify gaps.

**Returns:** Coverage percentage, gap counts (summary) or detailed missing functions/branches (detailed)

See **reference.md** for complete parameter specifications and response formats.

## Token Efficiency

This skill supports multiple response formats to optimize token usage:

| Operation | Format | Token Usage | Use When |
|-----------|--------|-------------|----------|
| analyze_file | summary | 200-500 | Quick overview, planning |
| analyze_file | detailed | 2000-5000 | Need full function details |
| generate_tests | concise | 300-600 | Normal use (summary only) |
| generate_tests | detailed | 5000-10000 | Need to review test code |
| analyze_coverage | summary | 200-400 | Quick coverage check |
| analyze_coverage | detailed | 1000-3000 | Identify specific gaps |

**Best Practice:** Start with summary/concise, then request detailed only for specific items.

## Example Workflow

```python
# 1. Analyze source (summary)
analysis = analyze_file("payment.py")

# 2. Generate tests (concise - no code in response)
tests = generate_tests("payment.py", target_coverage=90)

# 3. Use Write tool to create test file
# (test code is written to disk, not returned in response)

# 4. Check coverage (summary)
coverage = analyze_coverage("test_payment.py", "payment.py")

# 5. If coverage low, get details
if coverage.data["coverage_percent"] < 80:
    gaps = analyze_coverage(
        "test_payment.py",
        "payment.py",
        response_format="detailed"
    )
    print(f"Missing tests for: {gaps.data['missing_functions']}")
```

## Error Handling

All operations return `OperationResult` with agent-friendly errors:

```python
result = generate_tests("nonexistent.py")

if not result.success:
    print(result.error)       # "Cannot find source file: nonexistent.py"
    print(result.error_code)  # "FILE_NOT_FOUND"

    # Actionable suggestions
    for suggestion in result.suggestions:
        print(f"  - {suggestion}")
    # - Check if the file path is correct
    # - Use Glob('**/*.py') to find Python files
    # - Verify the file exists with Bash('ls -la src/')

    # Example fix
    print(result.example_fix)
    # generate_tests('src/services/payment.py')
```

## Integration

**With TDD Workflow:**
```python
# Write failing test first
tests = generate_tests("payment.py", response_format="detailed")
# Review generated tests, modify as needed
# Implement code to make tests pass
```

**With Code Review:**
```python
# Check if new code has tests
coverage = analyze_coverage("test_payment.py", "payment.py")
if coverage.data["coverage_percent"] < 80:
    print("Warning: Low test coverage for new feature")
```

**With Learning Plans:**
```python
# Student learning TDD
analysis = analyze_file("student_code.py")
print(f"This code has {analysis.data['total_functions']} functions to test")
print("Try writing tests for the simplest function first!")
```

## Next Steps

- **Read reference.md** for complete API documentation
- **Read examples.md** for real-world usage patterns
- **Try the skill** with your own Python files
- **Combine with pr_review_assistant** for comprehensive quality checks

---

*Last Updated: 2025-11-07*

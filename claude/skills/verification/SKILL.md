---
name: verification
description: Validates code, output, and tests to ensure quality and correctness
version: 1.0.0
category: quality
tags:
  - validation
  - testing
  - quality-assurance
activation: manual
tools:
  - Read
dependencies: []
---

# Verification Skill

## When to Use This Skill

Use the verification skill when you need to:
- **Validate student code** for syntax, style, and security issues
- **Verify program output** matches expected results
- **Check test quality** and coverage
- **Provide automated feedback** on code submissions
- **Ensure teaching quality** by validating student work

## Quick Start

```python
from skills.verification import validate_code, validate_output, validate_tests

# Validate code
result = validate_code(code_string)
if result.success:
    print(f"Valid: {result.data['is_valid']}")
    print(f"Issues: {result.data['issue_count']}")

# Validate output
result = validate_output(
    expected="Hello, World!",
    actual=program_output,
    match_type="exact"
)
print(f"Match: {result.data['is_match']}")

# Validate tests
result = validate_tests(test_code, source_code)
print(f"Test count: {result.data['test_count']}")
print(f"Coverage: {result.data.get('coverage_ratio', 0):.0%}")
```

## Operations

**Code Validation:**
- `validate_code` - Validate Python code for syntax, style, and security

**Output Validation:**
- `validate_output` - Verify program output matches expectations

**Test Validation:**
- `validate_tests` - Check test quality and coverage

## Token Efficiency

All operations support `response_format` parameter:
- **"summary"**: Overview only (70-90% token savings)
- **"detailed"**: Full analysis with all issues

## Documentation

- See [reference.md](./reference.md) for complete API documentation
- See [examples.md](./examples.md) for usage examples

## Example Use Cases

1. **Automated Code Review**
   - Student submits code
   - Validate for syntax/style/security
   - Provide actionable feedback

2. **Test-Driven Development**
   - Student writes tests
   - Validate test quality
   - Suggest missing tests

3. **Learning Verification**
   - Verify student understands concepts
   - Check output matches expected results
   - Track progress over time

## Related Skills

- **test_orchestrator** - Generate tests automatically
- **code_analysis** - Analyze code complexity
- **skill_evaluator** - Evaluate skill effectiveness

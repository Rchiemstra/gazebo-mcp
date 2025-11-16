# Verification Skill Reference

Complete API documentation for the verification skill.

---

## validate_code

Validates Python code for syntax, style, and security issues.

### Signature

```python
def validate_code(
    code: str,
    check_style: bool = True,
    check_security: bool = True,
    response_format: str = "summary",
    **kwargs
) -> OperationResult
```

### Parameters

- **code** (`str`, required): Python code to validate
- **check_style** (`bool`, default=True): Whether to check style issues
- **check_security** (`bool`, default=True): Whether to check security issues
- **response_format** (`str`, default="summary"):
  - `"summary"`: Just validity and issue counts
  - `"detailed"`: All issues with line numbers and suggestions

### Returns

`OperationResult` with:

**Summary Format:**
```python
{
    "is_valid": bool,
    "issue_count": int,
    "error_count": int,
    "warning_count": int,
    "top_issues": [str, ...],  # Top 3 issues
    "efficiency_tip": str
}
```

**Detailed Format:**
```python
{
    "is_valid": bool,
    "issue_count": int,
    "error_count": int,
    "warning_count": int,
    "issues": [
        {
            "severity": "error" | "warning" | "info",
            "category": "syntax" | "style" | "security",
            "message": str,
            "line": int | None,
            "suggestion": str | None
        },
        ...
    ],
    "metrics": {
        "total_lines": int,
        "non_empty_lines": int,
        "functions": int,
        "classes": int,
        "imports": int
    }
}
```

### Validation Checks

**Syntax:**
- Valid Python syntax
- Parseable AST

**Style:**
- Lines < 120 characters
- Docstrings present
- Naming conventions

**Security:**
- No `eval()` or `exec()`
- No bare `except` clauses
- Safe file operations

---

## validate_output

Validates program output against expected results.

### Signature

```python
def validate_output(
    expected: str,
    actual: str,
    match_type: str = "exact",
    response_format: str = "summary",
    **kwargs
) -> OperationResult
```

### Parameters

- **expected** (`str`, required): Expected output
- **actual** (`str`, required): Actual output from program
- **match_type** (`str`, default="exact"):
  - `"exact"`: Exact string match
  - `"contains"`: Actual contains expected
  - `"regex"`: Pattern matching
  - `"json"`: JSON object comparison
  - `"lines"`: Line-by-line comparison
- **response_format** (`str`, default="summary"):
  - `"summary"`: Match result and similarity score
  - `"detailed"`: Full difference analysis

### Returns

`OperationResult` with:

**Summary Format:**
```python
{
    "is_match": bool,
    "similarity_score": float,  # 0.0 to 1.0
    "match_type": str,
    "difference_count": int,  # If not matching
    "efficiency_tip": str
}
```

**Detailed Format:**
```python
{
    "is_match": bool,
    "similarity_score": float,
    "match_type": str,
    "differences": [str, ...],  # Diff output or error descriptions
    "details": {
        # Match type specific details
    }
}
```

---

## validate_tests

Validates test code quality and coverage.

### Signature

```python
def validate_tests(
    test_code: str,
    source_code: Optional[str] = None,
    response_format: str = "summary",
    **kwargs
) -> OperationResult
```

### Parameters

- **test_code** (`str`, required): Test code to validate
- **source_code** (`str`, optional): Source code being tested (for coverage analysis)
- **response_format** (`str`, default="summary"):
  - `"summary"`: Test count and validity
  - `"detailed"`: All issues and improvement suggestions

### Returns

`OperationResult` with:

**Summary Format:**
```python
{
    "is_valid": bool,
    "test_count": int,
    "issue_count": int,
    "coverage_ratio": float,  # If source_code provided
    "functions_covered": int,  # If source_code provided
    "top_issues": [str, ...],  # Top 3 issues
    "efficiency_tip": str
}
```

**Detailed Format:**
```python
{
    "is_valid": bool,
    "test_count": int,
    "issue_count": int,
    "coverage_ratio": float,  # If source_code provided
    "functions_covered": int,  # If source_code provided
    "issues": [str, ...],  # All validation issues
    "metrics": {
        "test_count": int,
        "tests_with_assertions": int,
        "tests_with_docstrings": int
    },
    "covered_functions": [str, ...],
    "suggestions_for_improvement": [str, ...]  # Top 5
}
```

### Test Validation Checks

**Structure:**
- Functions start with `test_`
- At least one test function exists
- Tests have assertions
- Tests have docstrings

**Coverage:**
- Which source functions are tested
- Suggestions for missing tests
- Edge case coverage

---

## Error Codes

All operations return agent-friendly errors with these codes:

- `VALIDATION_ERROR`: General validation failure
- `INVALID_MATCH_TYPE`: Invalid match_type parameter (validate_output)

Each error includes:
- Clear error message
- 3-4 actionable suggestions
- Example fix showing correct usage

---

## Token Efficiency Guide

### Summary Format (Recommended for Most Cases)

```python
# Use summary for quick validation
result = validate_code(code)  # ~200-500 tokens
```

**When to use:**
- Just need to know if valid
- Count of issues is sufficient
- Large code/output to validate

**Token savings:** 70-90%

### Detailed Format (Use When Needed)

```python
# Use detailed when you need specifics
result = validate_code(code, response_format="detailed")  # ~1000-3000 tokens
```

**When to use:**
- Need exact line numbers
- Want all suggestions
- Providing feedback to student
- Analyzing specific issues

---

## Best Practices

1. **Start with summary format**
   - Get overview first
   - Request details only if needed

2. **Use appropriate match_type**
   - `exact`: For precise validation
   - `contains`: For flexible output
   - `json`: For structured data
   - `regex`: For pattern-based validation

3. **Provide source_code for test validation**
   - Enables coverage analysis
   - Gets specific suggestions
   - Better feedback quality

4. **Handle validation results**
   - Always check `result.success`
   - Use suggestions from errors
   - Provide feedback to students

---

## Version

**Current Version:** 1.0.0

**Dependencies:** None (uses Python stdlib only)

**Required Tools:** Read (for loading files)

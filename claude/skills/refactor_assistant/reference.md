# Refactor Assistant - API Reference

Complete documentation for all refactor_assistant operations.

---

## Overview

Refactor Assistant provides intelligent code refactoring capabilities with safe transformations and behavior preservation. It analyzes Python code for maintainability issues and suggests targeted improvements.

---

## Operations

### detect_code_smells

Detect code smells and refactoring opportunities in a file.

#### Signature

```python
def detect_code_smells(
    file_path: str,
    severity_threshold: str = "low",
    **kwargs
) -> OperationResult
```

#### Parameters

**file_path** (str, required)
- Path to Python file to analyze
- Must be valid Python file (.py)
- File must exist and be readable

**severity_threshold** (str, optional, default="low")
- Minimum severity level to report
- Valid values: `"low"`, `"medium"`, `"high"`, `"critical"`
- Higher thresholds return fewer, more important issues

#### Returns

```python
{
    "success": True,
    "data": {
        "file_path": "src/payment.py",
        "total_smells": 12,
        "critical": 1,
        "high": 3,
        "medium": 5,
        "low": 3,
        "smells": [
            {
                "type": "long_function",
                "severity": "high",
                "line_number": 45,
                "function_name": "process_payment",
                "class_name": None,
                "description": "Function 'process_payment' is 75 lines long (max: 50)",
                "suggestion": "Consider extracting smaller helper functions",
                "metrics": {
                    "length": 75,
                    "threshold": 50
                }
            },
            {
                "type": "complex_function",
                "severity": "critical",
                "line_number": 45,
                "function_name": "process_payment",
                "class_name": None,
                "description": "Function has cyclomatic complexity of 15 (max: 10)",
                "suggestion": "Simplify logic or extract methods to reduce complexity",
                "metrics": {
                    "complexity": 15,
                    "threshold": 10
                }
            }
        ],
        "metrics": {
            "total_lines": 350,
            "total_functions": 12,
            "total_classes": 2,
            "avg_function_length": 25,
            "max_complexity": 15
        }
    },
    "duration": 0.234,
    "metadata": {
        "skill": "refactor-assistant",
        "operation": "detect_code_smells",
        "version": "0.1.0",
        "severity_threshold": "low"
    }
}
```

#### Smell Types Detected

| Type | Severity | Threshold | Description |
|------|----------|-----------|-------------|
| long_function | Medium-High | >50 lines | Functions that are too long |
| long_parameter_list | Medium | >5 params | Too many function parameters |
| complex_function | High-Critical | complexity >10 | High cyclomatic complexity |
| deep_nesting | Medium-High | >4 levels | Too many nested blocks |
| too_many_returns | Medium | >5 returns | Multiple return points |
| cognitive_complexity | High | Variable | Hard to understand logic |
| god_class | High | >20 methods | Class doing too much |
| long_class | Medium | >200 lines | Class is too long |
| magic_number | Low-Medium | N/A | Unnamed numeric constants |
| poor_naming | Low-Medium | N/A | Unclear variable names |
| duplicate_code | Medium-High | N/A | Copy-paste patterns |
| dead_code | Low-Medium | N/A | Unreachable code |
| mutable_default | High | N/A | Dangerous default args |
| broad_exception | Medium | N/A | Catching base Exception |
| empty_except | High | N/A | Silent error handling |

#### Error Handling

**FILE_NOT_FOUND:**
```python
{
    "success": False,
    "error": "File not found: src/missing.py",
    "error_code": "FILE_NOT_FOUND",
    "duration": 0.001
}
```

**SYNTAX_ERROR:**
```python
{
    "success": False,
    "error": "Syntax error in file: invalid syntax (line 45)",
    "error_code": "SYNTAX_ERROR",
    "duration": 0.012
}
```

**DETECTION_ERROR:**
```python
{
    "success": False,
    "error": "Code smell detection failed: <reason>",
    "error_code": "DETECTION_ERROR",
    "duration": 0.056
}
```

---

### suggest_refactorings

Suggest specific refactorings for code based on detected issues.

#### Signature

```python
def suggest_refactorings(
    file_path: str,
    max_suggestions: int = 10,
    **kwargs
) -> OperationResult
```

#### Parameters

**file_path** (str, required)
- Path to Python file to analyze
- Must be valid Python file
- File must exist and be readable

**max_suggestions** (int, optional, default=10)
- Maximum number of suggestions to return
- Suggestions are ranked by estimated impact
- Range: 1-50 (practical limit)

#### Returns

```python
{
    "success": True,
    "data": {
        "file_path": "src/payment.py",
        "total_suggestions": 7,
        "suggestions": [
            {
                "refactoring_type": "extract_method",
                "line_number": 45,
                "description": "Extract validation logic into separate method",
                "estimated_impact": 85,  # 0-100, higher = more beneficial
                "parameters": {
                    "start_line": 52,
                    "end_line": 67,
                    "suggested_name": "validate_payment_details"
                },
                "preview": "def validate_payment_details(amount, account):\n    ..."
            },
            {
                "refactoring_type": "extract_constant",
                "line_number": 103,
                "description": "Extract magic number 0.15 to named constant",
                "estimated_impact": 60,
                "parameters": {
                    "value": 0.15,
                    "suggested_name": "TAX_RATE"
                },
                "preview": "TAX_RATE = 0.15"
            },
            {
                "refactoring_type": "rename_symbol",
                "line_number": 120,
                "description": "Rename unclear variable 'x' to descriptive name",
                "estimated_impact": 45,
                "parameters": {
                    "old_name": "x",
                    "suggested_name": "transaction_id"
                },
                "preview": None
            }
        ]
    },
    "duration": 0.187,
    "metadata": {
        "skill": "refactor-assistant",
        "operation": "suggest_refactorings",
        "version": "0.1.0",
        "max_suggestions": 10
    }
}
```

#### Refactoring Types

| Type | Impact Range | Use Case |
|------|--------------|----------|
| extract_method | 60-95 | Long functions, duplicate code |
| extract_variable | 40-70 | Complex expressions |
| extract_constant | 50-80 | Magic numbers |
| rename_symbol | 30-60 | Poor naming |
| simplify_conditional | 55-85 | Complex if statements |
| inline_variable | 20-40 | Unnecessary variables |
| remove_dead_code | 30-50 | Unreachable code |

#### Error Handling

Same error codes as `detect_code_smells`:
- FILE_NOT_FOUND
- SYNTAX_ERROR
- SUGGESTION_ERROR (generic failure)

---

### apply_refactoring

Apply a refactoring transformation to code.

#### Signature

```python
def apply_refactoring(
    file_path: str,
    refactoring_type: str,
    location: Dict[str, Any],
    parameters: Dict[str, Any],
    run_tests: bool = False,
    **kwargs
) -> OperationResult
```

#### Parameters

**file_path** (str, required)
- Path to Python file to refactor
- File will be modified in place
- Original backed up to `{file_path}.backup`

**refactoring_type** (str, required)
- Type of refactoring to apply
- Valid values: `"extract_method"`, `"extract_variable"`, `"rename_symbol"`, `"extract_constant"`, `"simplify_conditional"`, `"inline_variable"`, `"remove_dead_code"`

**location** (Dict[str, Any], required)
- Location information for refactoring
- Format varies by refactoring type:

```python
# For extract_method, extract_variable
location = {
    "start_line": 52,
    "end_line": 67,
    "start_col": 0,    # Optional
    "end_col": 80      # Optional
}

# For rename_symbol
location = {
    "line_number": 45,
    "symbol_name": "old_name"
}

# For extract_constant
location = {
    "line_number": 103,
    "value": 0.15
}
```

**parameters** (Dict[str, Any], required)
- Refactoring-specific parameters
- Format varies by refactoring type:

```python
# For extract_method
parameters = {
    "new_name": "validate_payment_details",
    "extract_as_static": False,  # Optional
    "parameters": ["amount", "account"]  # Optional, auto-detected
}

# For rename_symbol
parameters = {
    "new_name": "transaction_id",
    "scope": "function"  # or "class", "module"
}

# For extract_constant
parameters = {
    "constant_name": "TAX_RATE",
    "placement": "top"  # or "before_use"
}
```

**run_tests** (bool, optional, default=False)
- Whether to run tests after refactoring
- Requires tests to exist
- Uses pytest by default
- Reverts changes if tests fail

#### Returns

```python
{
    "success": True,
    "data": {
        "file_path": "src/payment.py",
        "refactoring_type": "extract_method",
        "changes_made": [
            "Extracted lines 52-67 to new method 'validate_payment_details'",
            "Added method definition at line 45",
            "Replaced original code with method call"
        ],
        "original_code": "# Original code from lines 52-67...",
        "refactored_code": "def validate_payment_details(amount, account):\n    ...",
        "backup_path": "src/payment.py.backup",
        "test_results": {
            "tests_run": 15,
            "passed": 15,
            "failed": 0,
            "duration": 1.234
        }
    },
    "duration": 1.456,
    "metadata": {
        "skill": "refactor-assistant",
        "operation": "apply_refactoring",
        "version": "0.1.0",
        "refactoring_type": "extract_method",
        "tests_run": True
    }
}
```

#### Error Handling

**FILE_NOT_FOUND:**
```python
{
    "success": False,
    "error": "File not found: src/missing.py",
    "error_code": "FILE_NOT_FOUND"
}
```

**VALIDATION_ERROR:**
```python
{
    "success": False,
    "error": "Invalid refactoring parameters: missing required field 'new_name'",
    "error_code": "VALIDATION_ERROR"
}
```

**REFACTORING_ERROR:**
```python
{
    "success": False,
    "error": "Refactoring failed: could not extract method - invalid line range",
    "error_code": "REFACTORING_ERROR"
}
```

---

### analyze_complexity

Analyze code complexity metrics focusing on maintainability.

#### Signature

```python
def analyze_complexity(
    file_path: str,
    **kwargs
) -> OperationResult
```

#### Parameters

**file_path** (str, required)
- Path to Python file to analyze
- Must be valid Python file
- File must exist and be readable

#### Returns

```python
{
    "success": True,
    "data": {
        "file_path": "src/payment.py",
        "metrics": {
            "total_lines": 350,
            "total_functions": 12,
            "total_classes": 2,
            "avg_complexity": 7.5,
            "max_complexity": 15,
            "avg_function_length": 25,
            "max_function_length": 75
        },
        "complexity_issues": [
            {
                "type": "complex_function",
                "severity": "critical",
                "line_number": 45,
                "function_name": "process_payment",
                "description": "Function has cyclomatic complexity of 15 (max: 10)",
                "suggestion": "Simplify logic or extract methods to reduce complexity",
                "metrics": {
                    "complexity": 15,
                    "threshold": 10
                }
            },
            {
                "type": "deep_nesting",
                "severity": "high",
                "line_number": 52,
                "function_name": "process_payment",
                "description": "Nesting depth of 5 levels (max: 4)",
                "suggestion": "Extract nested logic to separate functions",
                "metrics": {
                    "nesting_depth": 5,
                    "threshold": 4
                }
            }
        ],
        "total_complexity_issues": 2,
        "recommendations": [
            "Simplify logic or extract methods to reduce complexity",
            "Extract nested logic to separate functions"
        ]
    },
    "duration": 0.156,
    "metadata": {
        "skill": "refactor-assistant",
        "operation": "analyze_complexity",
        "version": "0.1.0"
    }
}
```

#### Complexity Metrics

| Metric | Threshold | Severity if Exceeded |
|--------|-----------|---------------------|
| Cyclomatic Complexity | >10 | High-Critical |
| Nesting Depth | >4 | Medium-High |
| Function Length | >50 lines | Medium-High |
| Cognitive Complexity | >15 | High |

#### Error Handling

Same error codes as `detect_code_smells`:
- FILE_NOT_FOUND
- ANALYSIS_ERROR

---

## Configuration Thresholds

These thresholds are used by the smell detector:

```python
# Function metrics
MAX_FUNCTION_LENGTH = 50      # lines
MAX_PARAMETERS = 5            # parameters
MAX_COMPLEXITY = 10           # cyclomatic complexity
MAX_NESTING_DEPTH = 4         # levels
MAX_RETURNS = 5               # return statements

# Class metrics
MAX_CLASS_LENGTH = 200        # lines
MAX_CLASS_METHODS = 20        # methods
```

These are sensible defaults but can vary by project. Adjust expectations accordingly.

---

## Best Practices

### 1. Analyze Before Applying

```python
# ✅ Good: Understand issues first
smells = detect_code_smells("payment.py")
suggestions = suggest_refactorings("payment.py")
# Review suggestions manually
# Then apply specific refactorings

# ❌ Bad: Apply blindly
apply_refactoring(...)  # Without understanding impact
```

### 2. Use Severity Filtering

```python
# ✅ Good: Focus on important issues
result = detect_code_smells("file.py", severity_threshold="high")

# ❌ Bad: Get overwhelmed with minor issues
result = detect_code_smells("file.py", severity_threshold="low")
```

### 3. Run Tests After Refactoring

```python
# ✅ Good: Verify behavior preserved
result = apply_refactoring(
    file_path="payment.py",
    refactoring_type="extract_method",
    location={...},
    parameters={...},
    run_tests=True  # Ensure tests pass
)

# ❌ Bad: Skip verification
result = apply_refactoring(..., run_tests=False)
```

### 4. Start with Low-Risk Refactorings

```python
# ✅ Good: Start with safe refactorings
# 1. Rename variables
# 2. Extract constants
# 3. Extract methods
# 4. Complex refactorings

# ❌ Bad: Jump to complex transformations
# Immediately try to refactor core logic
```

### 5. Handle Errors Gracefully

```python
# ✅ Good: Check success and handle errors
result = detect_code_smells("file.py")

if result.success:
    # Process results
    for smell in result.data["smells"]:
        print(f"{smell['type']}: {smell['description']}")
else:
    # Handle error
    print(f"Error: {result.error}")
    if result.error_code == "SYNTAX_ERROR":
        print("Fix syntax errors first")

# ❌ Bad: Assume success
smells = result.data["smells"]  # May crash if not success
```

---

## Common Workflows

### Workflow 1: Pre-commit Quality Check

```python
from skills.refactor_assistant.operations import detect_code_smells

# Check all modified files
files = ["src/payment.py", "src/account.py"]

for file in files:
    result = detect_code_smells(file, severity_threshold="high")

    if result.success:
        if result.data["critical"] > 0:
            print(f"❌ {file}: {result.data['critical']} critical issues")
            # Block commit
        elif result.data["high"] > 0:
            print(f"⚠️  {file}: {result.data['high']} high priority issues")
            # Warn but allow
        else:
            print(f"✅ {file}: No critical/high issues")
```

### Workflow 2: Guided Refactoring

```python
from skills.refactor_assistant.operations import (
    detect_code_smells,
    suggest_refactorings,
    apply_refactoring
)

# 1. Find issues
smells = detect_code_smells("legacy.py")
print(f"Found {smells.data['total_smells']} issues")

# 2. Get suggestions
suggestions = suggest_refactorings("legacy.py", max_suggestions=5)
print(f"Top {len(suggestions.data['suggestions'])} suggestions:")

for i, sug in enumerate(suggestions.data['suggestions'], 1):
    print(f"{i}. {sug['description']} (impact: {sug['estimated_impact']})")

# 3. Apply top suggestion (after manual review)
top = suggestions.data['suggestions'][0]
result = apply_refactoring(
    file_path="legacy.py",
    refactoring_type=top['refactoring_type'],
    location={"start_line": top['line_number']},
    parameters=top['parameters'],
    run_tests=True
)

if result.success:
    print("Refactoring applied successfully!")
    print(f"Tests: {result.data['test_results']['passed']}/{result.data['test_results']['tests_run']} passed")
```

### Workflow 3: Complexity Hotspot Analysis

```python
from skills.refactor_assistant.operations import analyze_complexity
from skills.common.filters import ResultFilter

# Find complex files
files = glob.glob("src/**/*.py", recursive=True)
complexity_data = []

for file in files:
    result = analyze_complexity(file)
    if result.success:
        complexity_data.append({
            "file": file,
            "max_complexity": result.data["metrics"]["max_complexity"],
            "issues": result.data["total_complexity_issues"]
        })

# Sort by complexity
sorted_files = sorted(complexity_data, key=lambda x: x["max_complexity"], reverse=True)

# Refactor top 5 most complex files
for item in sorted_files[:5]:
    print(f"Refactor: {item['file']} (complexity: {item['max_complexity']})")
```

---

## Performance Notes

### Execution Time

| Operation | Typical Time | Depends On |
|-----------|--------------|------------|
| detect_code_smells | 100-500ms | File size, complexity |
| suggest_refactorings | 150-600ms | Code structure |
| apply_refactoring | 200ms-2s | Transformation type, tests |
| analyze_complexity | 100-400ms | File size |

### Token Usage

- **detect_code_smells**: 500-2000 tokens (depends on severity_threshold)
- **suggest_refactorings**: 800-3000 tokens (depends on max_suggestions)
- **apply_refactoring**: 1000-5000 tokens (includes code preview)
- **analyze_complexity**: 400-1500 tokens (focused on complexity)

---

## Related Skills

- **code_analysis** - Broader AST analysis, dependency graphs, pattern detection
- **test_orchestrator** - Generate tests before refactoring to ensure safety
- **pr_review_assistant** - Review refactored code for quality

---

## Dependencies

### Required

- Python 3.8+
- AST module (built-in)

### Optional

- pytest (for `run_tests=True` in apply_refactoring)

---

*Last Updated: 2025-11-08*

---
name: refactor-assistant
description: Intelligently refactors code to improve quality, maintainability, and performance while preserving behavior
version: 0.1.0
category: development
tags:
  - refactoring
  - code-quality
  - maintainability
  - code-smells
activation: manual
tools:
  - Read
  - Write
  - Bash
dependencies: []
---

# Refactor Assistant

Intelligent code refactoring assistant that detects code smells, suggests improvements, and applies transformations safely.

---

## When to Use This Skill

Use refactor-assistant when you need to:

- **Detect code smells** - Find maintainability issues in code
- **Get refactoring suggestions** - Identify improvement opportunities
- **Apply safe transformations** - Refactor code while preserving behavior
- **Improve code quality** - Reduce complexity and improve readability
- **Prepare for code review** - Clean up code before submitting PR

**Don't use for:**
- Syntax errors (use linting tools)
- Security vulnerabilities (use dependency_guardian)
- Architecture redesign (use code-architecture-mentor agent)

---

## Quick Start

```python
from skills.refactor_assistant.operations import detect_code_smells

# Detect code smells in a file
result = detect_code_smells("src/legacy_payment.py")

if result.success:
    print(f"Found {result.data['total_smells']} code smells")
    print(f"Critical: {result.data['critical']}, High: {result.data['high']}")
```

---

## Operations

### detect_code_smells
Detect code smells and refactoring opportunities in a file.

**Returns:** Code smells by severity with suggestions for improvement

### suggest_refactorings
Suggest specific refactorings for code based on analysis.

**Returns:** Ranked list of refactoring suggestions with impact estimates

### apply_refactoring
Apply a refactoring transformation to code safely.

**Returns:** Modified code with change summary and optional test results

### analyze_complexity
Analyze code complexity metrics and identify complex areas.

**Returns:** Complexity metrics focused on maintainability issues

---

## Code Smells Detected (15 types)

**Function-level:**
- Long function (>50 lines)
- Long parameter list (>5 params)
- Complex function (cyclomatic complexity >10)
- Deep nesting (>4 levels)
- Too many returns (>5)
- Cognitive complexity (hard to understand)

**Class-level:**
- God class (>20 methods)
- Long class (>200 lines)

**Code quality:**
- Magic numbers (unnamed constants)
- Poor naming (single letters, unclear names)
- Duplicate code (copy-paste patterns)
- Dead code (unreachable or unused)

**Error handling:**
- Mutable default arguments
- Broad exception catching
- Empty except blocks

---

## Refactoring Types (7 types)

- **Extract Method** - Pull code into separate function
- **Extract Variable** - Name complex expressions
- **Extract Constant** - Convert magic numbers to named constants
- **Rename Symbol** - Improve variable/function names
- **Simplify Conditional** - Simplify complex if statements
- **Inline Variable** - Remove unnecessary variables
- **Remove Dead Code** - Delete unreachable code

---

## Token Efficiency

**Uses Read, Write, and Bash tools** - Moderate token usage

**Tip:** Use `severity_threshold` to filter results:
- `"critical"` - Only critical issues (~200 tokens)
- `"high"` - Critical + high severity (~500 tokens)
- `"medium"` - Medium and above (~1000 tokens)
- `"low"` - All issues (~2000 tokens, default)

```python
# ✅ Efficient - filter by severity
result = detect_code_smells("file.py", severity_threshold="high")
# Returns only high/critical issues

# ❌ Inefficient - get all smells
result = detect_code_smells("file.py", severity_threshold="low")
# Returns every minor issue
```

---

## Security

**Safety Level:** Medium (uses Write and Bash)

**Safe because:**
- Read-only analysis for smell detection
- Applies transformations only when explicitly requested
- Can run tests to verify behavior preservation
- Creates backups before major changes

**Audit focus:**
- File write operations
- Test execution (optional)
- Code transformation logic

See `../SECURITY.md` for details.

---

## Documentation

**For complete API reference:** See `reference.md`
- Full operation signatures
- All parameters and return values
- Error codes and handling
- Complexity thresholds

**For usage examples:** See `examples.md`
- 9 real-world scenarios
- Common refactoring workflows
- Integration with other skills
- Best practices

---

## Common Patterns

### Pattern 1: Find and Fix
```python
# 1. Detect smells
smells = detect_code_smells("payment.py", severity_threshold="high")

# 2. Get specific suggestions
suggestions = suggest_refactorings("payment.py", max_suggestions=5)

# 3. Apply top suggestion (manually review first!)
# apply_refactoring(...)  # See examples.md for details
```

### Pattern 2: Pre-commit Quality Check
```python
# Check quality before committing
result = detect_code_smells("src/new_feature.py", severity_threshold="medium")

if result.data["critical"] > 0 or result.data["high"] > 0:
    print("Fix critical/high issues before committing")
```

### Pattern 3: Complexity Analysis
```python
# Find the most complex code
complexity = analyze_complexity("legacy/old_module.py")

# Prioritize refactoring based on complexity
if complexity.data["total_complexity_issues"] > 10:
    print("High complexity - refactor recommended")
```

---

## Related Skills

- **code_analysis** - For broader code analysis (AST, dependencies)
- **test_orchestrator** - Generate tests before refactoring
- **pr_review_assistant** - Review refactored code

---

## Quick Reference

**Detect issues:**
```python
detect_code_smells(file_path, severity_threshold="high")
```

**Get suggestions:**
```python
suggest_refactorings(file_path, max_suggestions=10)
```

**Analyze complexity:**
```python
analyze_complexity(file_path)
```

---

*Last Updated: 2025-11-08*

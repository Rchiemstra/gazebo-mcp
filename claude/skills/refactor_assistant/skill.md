---
name: refactor-assistant
description: Intelligently refactors code to improve quality, maintainability, and performance while preserving behavior
version: 0.1.0
author: Claude Code Skills
category: code-quality
tags:
  - refactoring
  - code-quality
  - maintainability
  - technical-debt
  - code-smells
tools:
  - Read
  - Edit
  - Write
  - Bash
activation: manual
dependencies:
  - test-orchestrator
operations:
  detect_code_smells: "Analyzes code to identify refactoring opportunities and code smells"
  suggest_refactorings: "Suggests specific refactorings with estimated impact"
  apply_refactoring: "Safely applies a refactoring transformation with optional test execution"
  analyze_complexity: "Analyzes code complexity metrics and provides recommendations"
---

# Refactor Assistant

An intelligent skill that identifies refactoring opportunities and safely transforms code to improve quality, maintainability, and performance.

## Features

- **Code Smell Detection**: Identifies 20+ types of code smells
- **Safe Refactoring**: Validates changes don't break behavior
- **Multi-language Support**: Python, JavaScript/TypeScript
- **Test Integration**: Works with test-orchestrator to ensure safety
- **Impact Analysis**: Predicts effects of refactorings
- **Automated Transformations**: Applies common refactoring patterns

## Refactoring Patterns

### Structural Refactorings
- Extract Method/Function
- Inline Method/Function
- Extract Variable
- Inline Variable
- Rename Symbol
- Move Method/Function

### Code Smells Detected
- Long Functions (>50 lines)
- Long Parameter Lists (>5 params)
- Duplicate Code
- Complex Conditionals
- Magic Numbers
- Dead Code
- God Classes
- Feature Envy
- Inappropriate Intimacy
- Lazy Classes

### Quality Improvements
- Reduce Cyclomatic Complexity
- Improve Naming
- Extract Constants
- Remove Dead Code
- Simplify Conditionals
- Break Up Large Classes

## Operations

### detect_code_smells

Analyzes code to identify refactoring opportunities.

**Parameters:**
- `file_path` (str): Path to file to analyze
- `severity_threshold` (str): Minimum severity (low, medium, high)

**Returns:**
- `total_smells`: Number of code smells found
- `by_severity`: Breakdown by severity
- `smells`: List of detected code smells with locations

### suggest_refactorings

Suggests specific refactorings for code.

**Parameters:**
- `file_path` (str): Path to file to refactor
- `max_suggestions` (int): Maximum number of suggestions

**Returns:**
- `suggestions`: List of refactoring suggestions
- `estimated_impact`: Predicted impact scores

### apply_refactoring

Safely applies a refactoring transformation.

**Parameters:**
- `file_path` (str): Path to file to refactor
- `refactoring_type` (str): Type of refactoring
- `location` (dict): Location details (line, column)
- `parameters` (dict): Refactoring-specific parameters
- `run_tests` (bool): Run tests after refactoring

**Returns:**
- `success`: Whether refactoring succeeded
- `changes`: Description of changes made
- `test_results`: Results if tests were run
- `rollback_info`: Information for reverting changes

### analyze_complexity

Analyzes code complexity metrics.

**Parameters:**
- `file_path` (str): Path to file to analyze

**Returns:**
- `cyclomatic_complexity`: Complexity score per function
- `cognitive_complexity`: Cognitive load score
- `maintainability_index`: Overall maintainability
- `recommendations`: Specific improvement suggestions

## Usage Examples

```python
from skills.refactor_assistant import (
    detect_code_smells,
    suggest_refactorings,
    apply_refactoring
)

# Detect code smells
result = detect_code_smells("legacy_module.py")
print(f"Found {result['total_smells']} code smells")

# Get refactoring suggestions
suggestions = suggest_refactorings("legacy_module.py")
for suggestion in suggestions['suggestions']:
    print(f"- {suggestion['type']}: {suggestion['description']}")

# Apply a refactoring
result = apply_refactoring(
    file_path="legacy_module.py",
    refactoring_type="extract_method",
    location={"start_line": 45, "end_line": 67},
    parameters={"new_name": "calculate_total"},
    run_tests=True
)
```

## Integration with Agents

Agents can use refactor-assistant to:
1. Continuously improve code quality
2. Reduce technical debt systematically
3. Prepare code for new features
4. Improve code before reviews
5. Automate refactoring tasks

## Safety Guarantees

Refactor-assistant ensures safety through:
- **Static Analysis**: Validates transformations preserve structure
- **Test Execution**: Runs tests before and after (with test-orchestrator)
- **Rollback Support**: Provides automatic rollback on failure
- **Impact Analysis**: Predicts effects before applying changes
- **Incremental Changes**: Applies one refactoring at a time

## Best Practices

1. Always run tests after refactoring
2. Commit before and after refactorings
3. Apply refactorings incrementally
4. Review automated refactorings
5. Use version control

## Output Format

All operations return structured data suitable for:
- Display to users
- Agent decision-making
- CI/CD integration
- Quality metrics tracking

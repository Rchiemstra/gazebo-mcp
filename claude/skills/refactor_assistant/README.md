# Refactor Assistant

An intelligent skill that analyzes code quality, detects code smells, and suggests safe refactorings to improve maintainability and performance.

## Overview

Refactor Assistant helps developers and agents systematically improve code quality by:
- Detecting 15+ types of code smells
- Suggesting targeted refactorings
- Analyzing code complexity and maintainability
- Providing impact estimates for refactorings
- Ensuring safety through test integration

## Features

### 🔍 Code Smell Detection

**Structural Smells:**
- Long Functions (>50 lines)
- Long Classes (>200 lines)
- God Classes (>20 methods)
- Long Parameter Lists (>5 params)
- Deep Nesting (>4 levels)
- Too Many Returns (>5 returns)

**Quality Smells:**
- High Cyclomatic Complexity (>10)
- High Cognitive Complexity
- Duplicate Code Blocks
- Magic Numbers
- Poor Naming (single-letter variables/functions)

**Anti-patterns:**
- Mutable Default Arguments
- Broad Exception Handling
- Empty Except Blocks
- Dead Code

### 🔧 Refactoring Suggestions

**Supported Refactorings:**
- Extract Method/Function
- Extract Variable
- Extract Constant
- Rename Symbol
- Inline Variable
- Simplify Conditional
- Remove Dead Code

**Impact Analysis:**
- Estimated improvement score (0-100%)
- Affected code locations
- Suggested parameter names
- Preview of changes

### 📊 Quality Metrics

- **Cyclomatic Complexity**: Decision point analysis
- **Nesting Depth**: Code structure complexity
- **Code Smells Density**: Smells per 100 lines
- **Overall Quality Score**: Composite health metric

## Installation

No external dependencies! Uses Python's built-in `ast` module.

```bash
# Optional: For enhanced refactoring
pip install rope  # Advanced Python refactoring library
```

## Quick Start

```python
from refactor_assistant import (
    detect_code_smells,
    suggest_refactorings,
    apply_refactoring
)

# Detect code smells
result = detect_code_smells("legacy_module.py")
print(f"Found {result['total_smells']} code smells")

# Filter by severity
result_high = detect_code_smells("legacy_module.py", severity_threshold="high")

# Get refactoring suggestions
suggestions = suggest_refactorings("legacy_module.py", max_suggestions=5)
for suggestion in suggestions['suggestions']:
    print(f"- {suggestion['description']}")

# Apply a refactoring (with tests)
result = apply_refactoring(
    file_path="legacy_module.py",
    refactoring_type="extract_method",
    location={"start_line": 45, "end_line": 67},
    parameters={"new_name": "calculate_total"},
    run_tests=True
)
```

## API Reference

### detect_code_smells

Analyzes code to identify refactoring opportunities.

```python
detect_code_smells(
    file_path: str,
    severity_threshold: str = "low"  # "low", "medium", "high", "critical"
) -> Dict
```

**Returns:**
```python
{
    'file_path': str,
    'total_smells': int,
    'by_severity': {
        'critical': int,
        'high': int,
        'medium': int,
        'low': int
    },
    'smells': [
        {
            'type': str,  # e.g., 'long_function'
            'severity': str,
            'line': int,
            'function': Optional[str],
            'class': Optional[str],
            'description': str,
            'suggestion': str,
            'metrics': dict
        },
        ...
    ],
    'metrics': {
        'total_lines': int,
        'total_functions': int,
        'total_classes': int
    }
}
```

### suggest_refactorings

Suggests specific refactorings for code improvements.

```python
suggest_refactorings(
    file_path: str,
    max_suggestions: int = 10
) -> Dict
```

**Returns:**
```python
{
    'file_path': str,
    'total_suggestions': int,
    'suggestions': [
        {
            'type': str,  # 'extract_method', 'extract_variable', etc.
            'line': int,
            'description': str,
            'estimated_impact': float,  # 0-100
            'parameters': dict,
            'preview': Optional[str]
        },
        ...
    ]
}
```

### apply_refactoring

Applies a specific refactoring transformation.

```python
apply_refactoring(
    file_path: str,
    refactoring_type: str,
    location: Dict,
    parameters: Dict,
    run_tests: bool = False
) -> Dict
```

**Returns:**
```python
{
    'success': bool,
    'refactoring_type': str,
    'file_path': str,
    'changes_made': [str, ...],
    'error': Optional[str],
    'test_results': Optional[dict]
}
```

## Code Smell Types

### Critical & High Severity

**God Class**
```python
# BAD: Class with too many responsibilities
class DataProcessor:
    def load_data(self): ...
    def save_data(self): ...
    def validate_data(self): ...
    def transform_data(self): ...
    # ... 20+ methods
```

**Fix**: Break into smaller, focused classes (DataLoader, DataValidator, DataTransformer)

**Empty Except**
```python
# BAD: Silently ignoring errors
try:
    risky_operation()
except:
    pass
```

**Fix**: Handle specific exceptions and log errors

**Mutable Default Arguments**
```python
# BAD: Dangerous default argument
def add_item(item, items=[]):
    items.append(item)
    return items
```

**Fix**: Use None and initialize inside function

### Medium Severity

**Long Function**
```python
# BAD: Function with 100+ lines
def process_payment(amount, method, ...):
    # 100 lines of code
    ...
```

**Fix**: Extract methods to break down functionality

**High Complexity**
```python
# BAD: Complex nested conditionals
def calculate(x):
    if x > 0:
        if x < 10:
            if x % 2 == 0:
                if x > 5:
                    return x * 2
```

**Fix**: Use early returns or extract logic

**Deep Nesting**
```python
# BAD: Deeply nested logic
def process(data):
    for item in data:
        if item.valid:
            if item.active:
                if item.approved:
                    if not item.processed:
                        # Do something
```

**Fix**: Use early continues or extract functions

### Low Severity

**Magic Numbers**
```python
# BAD: Unexplained constants
fee = amount * 0.029 + 0.30
```

**Fix**: Extract to named constants
```python
TRANSACTION_RATE = 0.029
TRANSACTION_FEE = 0.30
fee = amount * TRANSACTION_RATE + TRANSACTION_FEE
```

**Poor Naming**
```python
# BAD: Unclear variable names
def x(a, b):
    return a + b
```

**Fix**: Use descriptive names
```python
def calculate_total(price, tax):
    return price + tax
```

## Agent Integration

### Example: Automated Code Quality Bot

```python
class CodeQualityAgent:
    """Agent that maintains code quality."""

    def on_pull_request(self, pr_files):
        """Run on every PR."""
        issues = []

        for file_path in pr_files:
            result = detect_code_smells(file_path, severity_threshold="high")

            if result['by_severity']['critical'] > 0:
                issues.append({
                    'severity': 'critical',
                    'file': file_path,
                    'message': f"Found {result['by_severity']['critical']} critical code smells"
                })

        if issues:
            self.block_merge()
            self.comment_on_pr(issues)

        return len(issues) == 0
```

### Example: Automated Refactoring Bot

```python
class RefactoringAgent:
    """Agent that automatically refactors code."""

    def refactor_file(self, file_path):
        """Apply safe refactorings."""
        # 1. Detect smells
        smells = detect_code_smells(file_path)

        # 2. Get suggestions
        suggestions = suggest_refactorings(file_path)

        # 3. Filter safe refactorings
        safe_refactorings = [
            s for s in suggestions['suggestions']
            if s['type'] in ['extract_constant', 'rename_symbol']
        ]

        # 4. Apply each refactoring
        for refactoring in safe_refactorings:
            result = apply_refactoring(
                file_path=file_path,
                refactoring_type=refactoring['type'],
                location={'line': refactoring['line']},
                parameters=refactoring['parameters'],
                run_tests=True
            )

            if not result['success']:
                # Rollback on failure
                print(f"Refactoring failed: {result['error']}")
                break

        return True
```

### Example: Technical Debt Tracker

```python
class TechnicalDebtTracker:
    """Tracks code quality over time."""

    def analyze_codebase(self, project_path):
        """Generate tech debt report."""
        all_smells = []
        total_score = 0

        for file_path in self.find_python_files(project_path):
            result = detect_code_smells(file_path)
            all_smells.extend(result['smells'])

            # Calculate file score
            score = 100
            score -= result['by_severity']['critical'] * 20
            score -= result['by_severity']['high'] * 10
            score -= result['by_severity']['medium'] * 5
            score -= result['by_severity']['low'] * 2
            total_score += max(0, score)

        # Generate report
        return {
            'total_smells': len(all_smells),
            'average_quality': total_score / len(files),
            'high_priority': [s for s in all_smells if s['severity'] in ['critical', 'high']],
            'trends': self.calculate_trends()
        }
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Code Quality Check

on: [pull_request]

jobs:
  refactor-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Run Refactor Assistant
        run: |
          python -c "
          from refactor_assistant import detect_code_smells
          import sys
          import glob

          files = glob.glob('**/*.py', recursive=True)
          critical_issues = 0

          for f in files:
              result = detect_code_smells(f, severity_threshold='high')
              critical_issues += result['by_severity']['critical']

          if critical_issues > 0:
              print(f'Found {critical_issues} critical issues')
              sys.exit(1)
          "
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running code quality check..."

python -c "
from refactor_assistant import detect_code_smells
import sys

# Check staged Python files
for file in $(git diff --cached --name-only --diff-filter=ACM | grep '\.py$'):
    result = detect_code_smells(file, severity_threshold='medium')

    if result['by_severity']['high'] > 0 or result['by_severity']['critical'] > 0:
        print(f'⚠️  {file}: Found critical/high severity code smells')
        print('Run: python -m refactor_assistant detect {file}')
        sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo "❌ Commit blocked due to code quality issues"
    exit 1
fi

echo "✅ Code quality check passed"
```

## Best Practices

### 1. Start with High Severity

Focus on critical and high severity issues first:
- Fix god classes
- Remove empty except blocks
- Handle mutable defaults

### 2. Refactor Incrementally

Don't refactor everything at once:
- Apply one refactoring at a time
- Commit after each successful refactoring
- Run tests after each change

### 3. Ensure Test Coverage

Before refactoring:
- Generate tests with test-orchestrator
- Aim for >80% coverage
- Verify tests pass

### 4. Use Version Control

Always commit before refactoring:
```bash
git add .
git commit -m "Pre-refactoring snapshot"
# Refactor
git commit -m "Refactor: extract method from process_payment"
```

### 5. Measure Improvement

Track quality over time:
- Run smell detection regularly
- Monitor quality score trends
- Celebrate improvements!

## Refactoring Workflow

### Step 1: Detect Smells

```bash
python -m refactor_assistant detect my_module.py
```

### Step 2: Prioritize

Focus on:
1. Critical/high severity issues
2. Smells affecting multiple areas
3. High-impact refactorings

### Step 3: Generate Tests

```bash
python -m test_orchestrator generate my_module.py
```

### Step 4: Apply Refactorings

```python
# Extract long method
apply_refactoring(
    "my_module.py",
    "extract_method",
    {"start_line": 45, "end_line": 67},
    {"new_name": "calculate_shipping"},
    run_tests=True
)
```

### Step 5: Verify

- Re-run smell detection
- Confirm quality improved
- Ensure tests pass

## Demo

Run the comprehensive demo:

```bash
cd skills/refactor_assistant
python demo.py
```

The demo analyzes a legacy code file with 36 code smells and shows:
- Detailed smell breakdown
- Refactoring suggestions
- Impact analysis
- Quality scoring
- Agent integration patterns

## Example Output

```
📊 Analysis Results:
   Total code smells: 36

   Severity Breakdown:
   🔴 Critical: 0
   🟠 High:     4
   🟡 Medium:   5
   🔵 Low:      27

🟠 HIGH: God Class
   Line 12
   Class: DataProcessor
   📝 Class 'DataProcessor' has 21 methods (threshold: 20)
   💡 Consider breaking this class into smaller, focused classes

💡 Refactoring Suggestions:
   1. Extract Method
      Impact: [███████░░░] 70%
      📝 Extract complex block from 'process_payment' into separate method
```

## Limitations

### Current Implementation

- **Python Only**: Currently supports Python, JavaScript/TypeScript planned
- **Static Analysis**: Detects smells but doesn't execute code
- **Simple Refactorings**: Advanced refactorings require manual review
- **No IDE Integration**: CLI-based, not integrated with IDEs yet

### Future Enhancements

- Multi-language support (JavaScript, TypeScript, Java, Go)
- More sophisticated refactoring transformations
- IDE plugins (VS Code, PyCharm)
- Machine learning-based smell detection
- Automatic refactoring application
- Historical trend analysis

## Troubleshooting

### "No code smells found"

- Check that file is valid Python
- Lower severity threshold (`severity_threshold="low"`)
- Verify file contains actual code (not just imports)

### "Refactoring failed"

- Ensure tests exist and pass beforehand
- Check that location parameters are correct
- Review error message for specific issues

### "Quality score is 0"

- This is expected for files with many smells
- Focus on fixing high-severity issues first
- Quality will improve incrementally

## Related Skills

- **test-orchestrator**: Generate tests before refactoring
- **dependency-guardian**: Check dependencies during refactoring
- **pr-review-assistant**: Review refactored code

## Contributing

To extend Refactor Assistant:

1. **Add New Smell Detector**: Extend `smell_detector.py`
2. **Add New Refactoring**: Extend `refactoring_engine.py`
3. **Add New Language**: Create language-specific detector

## License

Part of Claude Code Skills framework.

## Support

- Run demo: `python demo.py`
- Check API: Read docstrings in source files
- Integration examples: See README sections above

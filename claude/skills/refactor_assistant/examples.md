# Refactor Assistant - Usage Examples

Real-world usage examples for refactor_assistant skill.

---

## Example 1: Basic Code Smell Detection

**Scenario:** You want to check a file for code quality issues before submitting a pull request.

```python
from skills.refactor_assistant.operations import detect_code_smells

# Detect all code smells in a file
result = detect_code_smells("src/services/payment.py")

if result.success:
    print(f"Code Quality Report for {result.data['file_path']}")
    print(f"=" * 60)
    print(f"Total Issues: {result.data['total_smells']}")
    print(f"  Critical: {result.data['critical']}")
    print(f"  High:     {result.data['high']}")
    print(f"  Medium:   {result.data['medium']}")
    print(f"  Low:      {result.data['low']}")
    print()

    # Show critical and high priority issues
    for smell in result.data['smells']:
        if smell['severity'] in ['critical', 'high']:
            print(f"❌ {smell['severity'].upper()}: {smell['description']}")
            print(f"   Line {smell['line_number']}: {smell['function_name'] or 'module level'}")
            print(f"   → {smell['suggestion']}")
            print()
else:
    print(f"Error: {result.error}")
```

**Output:**
```
Code Quality Report for src/services/payment.py
============================================================
Total Issues: 8
  Critical: 1
  High:     2
  Medium:   3
  Low:      2

❌ CRITICAL: Function has cyclomatic complexity of 15 (max: 10)
   Line 45: process_payment
   → Simplify logic or extract methods to reduce complexity

❌ HIGH: Function 'process_payment' is 75 lines long (max: 50)
   Line 45: process_payment
   → Consider extracting smaller helper functions

❌ HIGH: Nesting depth of 5 levels (max: 4)
   Line 52: process_payment
   → Extract nested logic to separate functions
```

**Token Usage:** ~1500 tokens (all smells, all severities)

---

## Example 2: Focused Quality Check (High Priority Only)

**Scenario:** You're on a tight deadline and only want to fix critical issues.

```python
from skills.refactor_assistant.operations import detect_code_smells

# Only get high and critical severity issues
result = detect_code_smells(
    "src/services/payment.py",
    severity_threshold="high"  # Filter out medium and low
)

if result.success:
    issues = result.data['critical'] + result.data['high']

    if issues == 0:
        print("✅ No critical or high priority issues!")
    else:
        print(f"⚠️  Found {issues} high priority issues to fix:")
        for smell in result.data['smells']:
            print(f"  - {smell['description']}")
            print(f"    Fix: {smell['suggestion']}")
else:
    print(f"Error: {result.error}")
```

**Output:**
```
⚠️  Found 3 high priority issues to fix:
  - Function has cyclomatic complexity of 15 (max: 10)
    Fix: Simplify logic or extract methods to reduce complexity
  - Function 'process_payment' is 75 lines long (max: 50)
    Fix: Consider extracting smaller helper functions
  - Nesting depth of 5 levels (max: 4)
    Fix: Extract nested logic to separate functions
```

**Token Usage:** ~400 tokens (filtered to high/critical only)

---

## Example 3: Getting Refactoring Suggestions

**Scenario:** You know there are issues but want specific suggestions on how to fix them.

```python
from skills.refactor_assistant.operations import suggest_refactorings

# Get top 5 refactoring suggestions
result = suggest_refactorings(
    "src/services/payment.py",
    max_suggestions=5
)

if result.success:
    print(f"Top {len(result.data['suggestions'])} Refactoring Suggestions:")
    print("=" * 60)

    for i, suggestion in enumerate(result.data['suggestions'], 1):
        impact = suggestion['estimated_impact']
        impact_label = "🔥 High" if impact > 70 else "⚡ Medium" if impact > 50 else "💡 Low"

        print(f"{i}. {impact_label} Impact ({impact}/100)")
        print(f"   Type: {suggestion['refactoring_type']}")
        print(f"   Line {suggestion['line_number']}: {suggestion['description']}")

        if suggestion.get('preview'):
            print(f"   Preview: {suggestion['preview']}")
        print()
else:
    print(f"Error: {result.error}")
```

**Output:**
```
Top 5 Refactoring Suggestions:
============================================================
1. 🔥 High Impact (85/100)
   Type: extract_method
   Line 45: Extract validation logic into separate method
   Preview: def validate_payment_details(amount, account):
    ...

2. 🔥 High Impact (78/100)
   Type: extract_method
   Line 52: Extract error handling into helper method

3. ⚡ Medium Impact (65/100)
   Type: extract_constant
   Line 103: Extract magic number 0.15 to named constant
   Preview: TAX_RATE = 0.15

4. ⚡ Medium Impact (60/100)
   Type: rename_symbol
   Line 120: Rename unclear variable 'x' to descriptive name

5. ⚡ Medium Impact (55/100)
   Type: simplify_conditional
   Line 89: Simplify complex conditional with early returns
```

**Token Usage:** ~1200 tokens (5 suggestions with previews)

---

## Example 4: Apply Simple Refactoring (Extract Constant)

**Scenario:** You have magic numbers in your code and want to extract them to named constants.

```python
from skills.refactor_assistant.operations import apply_refactoring

# Extract magic number to constant
result = apply_refactoring(
    file_path="src/services/payment.py",
    refactoring_type="extract_constant",
    location={
        "line_number": 103,
        "value": 0.15
    },
    parameters={
        "constant_name": "TAX_RATE",
        "placement": "top"  # Place at top of file
    },
    run_tests=False  # Quick refactoring, no tests needed
)

if result.success:
    print("✅ Refactoring applied successfully!")
    print(f"Changes made:")
    for change in result.data['changes_made']:
        print(f"  - {change}")

    print(f"\nRefactored code:")
    print(result.data['refactored_code'])

    print(f"\nBackup saved to: {result.data['backup_path']}")
else:
    print(f"❌ Refactoring failed: {result.error}")
    if result.error_code == "VALIDATION_ERROR":
        print("Check your parameters and try again")
```

**Output:**
```
✅ Refactoring applied successfully!
Changes made:
  - Added constant 'TAX_RATE = 0.15' at line 5
  - Replaced magic number at line 103 with TAX_RATE
  - Replaced magic number at line 187 with TAX_RATE (found duplicate)

Refactored code:
TAX_RATE = 0.15

Backup saved to: src/services/payment.py.backup
```

**Token Usage:** ~800 tokens

---

## Example 5: Apply Complex Refactoring (Extract Method)

**Scenario:** A function is too long and complex. You want to extract part of it into a separate method.

```python
from skills.refactor_assistant.operations import apply_refactoring

# Extract lines 52-67 into new method
result = apply_refactoring(
    file_path="src/services/payment.py",
    refactoring_type="extract_method",
    location={
        "start_line": 52,
        "end_line": 67
    },
    parameters={
        "new_name": "validate_payment_details",
        "extract_as_static": False,  # Instance method
        # Parameters auto-detected from usage
    },
    run_tests=True  # Verify behavior preserved
)

if result.success:
    print("✅ Method extracted successfully!")

    print("\nChanges:")
    for change in result.data['changes_made']:
        print(f"  {change}")

    print("\nNew method:")
    print(result.data['refactored_code'])

    # Check test results
    tests = result.data.get('test_results')
    if tests:
        if tests['failed'] == 0:
            print(f"\n✅ All tests passed ({tests['passed']}/{tests['tests_run']})")
        else:
            print(f"\n❌ {tests['failed']} tests failed!")
            print("Refactoring was reverted")
else:
    print(f"❌ Refactoring failed: {result.error}")
```

**Output:**
```
✅ Method extracted successfully!

Changes:
  Extracted lines 52-67 to new method 'validate_payment_details'
  Added method definition at line 45
  Replaced original code with method call
  Auto-detected parameters: ['amount', 'account']

New method:
def validate_payment_details(self, amount, account):
    """Validate payment amount and account details."""
    if amount <= 0:
        raise ValueError("Amount must be positive")

    if not account or not account.is_active:
        raise ValueError("Invalid account")

    if amount > account.balance:
        raise ValueError("Insufficient funds")

    return True

✅ All tests passed (15/15)
```

**Token Usage:** ~2500 tokens (includes code preview and test results)

---

## Example 6: Complexity Analysis for Prioritization

**Scenario:** You have a large codebase and want to find the most complex files to refactor first.

```python
from skills.refactor_assistant.operations import analyze_complexity
import glob

# Analyze all Python files
files = glob.glob("src/**/*.py", recursive=True)
complexity_data = []

for file in files:
    result = analyze_complexity(file)

    if result.success:
        complexity_data.append({
            "file": file,
            "max_complexity": result.data["metrics"]["max_complexity"],
            "avg_complexity": result.data["metrics"]["avg_complexity"],
            "issues": result.data["total_complexity_issues"],
            "recommendations": result.data["recommendations"]
        })

# Sort by maximum complexity
sorted_files = sorted(
    complexity_data,
    key=lambda x: x["max_complexity"],
    reverse=True
)

# Show top 5 most complex files
print("🔥 Top 5 Most Complex Files (Refactoring Priority)")
print("=" * 70)

for i, item in enumerate(sorted_files[:5], 1):
    print(f"{i}. {item['file']}")
    print(f"   Max Complexity: {item['max_complexity']} (avg: {item['avg_complexity']:.1f})")
    print(f"   Issues: {item['issues']}")

    if item['recommendations']:
        print(f"   → {item['recommendations'][0]}")
    print()
```

**Output:**
```
🔥 Top 5 Most Complex Files (Refactoring Priority)
======================================================================
1. src/services/payment.py
   Max Complexity: 15 (avg: 7.5)
   Issues: 3
   → Simplify logic or extract methods to reduce complexity

2. src/legacy/account_manager.py
   Max Complexity: 18 (avg: 9.2)
   Issues: 5
   → Extract nested logic to separate functions

3. src/utils/validators.py
   Max Complexity: 12 (avg: 6.8)
   Issues: 2
   → Simplify logic or extract methods to reduce complexity

4. src/api/handlers.py
   Max Complexity: 11 (avg: 5.5)
   Issues: 1
   → Extract nested logic to separate functions

5. src/models/transaction.py
   Max Complexity: 10 (avg: 4.2)
   Issues: 1
   → Simplify logic or extract methods to reduce complexity
```

**Token Usage:** ~600 tokens per file × 5 files = ~3000 tokens

---

## Example 7: Pre-commit Hook Integration

**Scenario:** Automatically check code quality before allowing commits.

```python
# .git/hooks/pre-commit (make executable with chmod +x)
#!/usr/bin/env python3

import sys
from skills.refactor_assistant.operations import detect_code_smells
import subprocess

# Get list of staged Python files
result = subprocess.run(
    ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
    capture_output=True,
    text=True
)

staged_files = [
    f for f in result.stdout.strip().split('\n')
    if f.endswith('.py')
]

if not staged_files:
    sys.exit(0)  # No Python files, allow commit

# Check each staged file
has_critical_issues = False
has_high_issues = False

for file in staged_files:
    result = detect_code_smells(file, severity_threshold="high")

    if result.success:
        critical = result.data['critical']
        high = result.data['high']

        if critical > 0:
            print(f"❌ {file}: {critical} critical issues")
            has_critical_issues = True

            # Show the issues
            for smell in result.data['smells']:
                if smell['severity'] == 'critical':
                    print(f"   Line {smell['line_number']}: {smell['description']}")

        elif high > 0:
            print(f"⚠️  {file}: {high} high priority issues")
            has_high_issues = True

# Decision: block on critical, warn on high
if has_critical_issues:
    print("\n❌ Commit blocked due to critical code quality issues")
    print("Fix critical issues or use 'git commit --no-verify' to bypass")
    sys.exit(1)
elif has_high_issues:
    print("\n⚠️  High priority issues found but commit allowed")
    print("Consider fixing these issues before pushing")
    sys.exit(0)
else:
    print("✅ All staged files pass quality checks")
    sys.exit(0)
```

**Usage:**
```bash
# Attempt commit with critical issues
$ git commit -m "Add payment processing"
❌ src/services/payment.py: 1 critical issues
   Line 45: Function has cyclomatic complexity of 15 (max: 10)

❌ Commit blocked due to critical code quality issues
Fix critical issues or use 'git commit --no-verify' to bypass

# After fixing
$ git commit -m "Add payment processing"
✅ All staged files pass quality checks
[main abc1234] Add payment processing
```

---

## Example 8: Integration with Test Orchestrator

**Scenario:** Generate tests before refactoring to ensure safety.

```python
from skills.test_orchestrator.operations import generate_tests, run_tests
from skills.refactor_assistant.operations import (
    suggest_refactorings,
    apply_refactoring
)

# Step 1: Generate tests for the file (if not exist)
print("Step 1: Generating tests...")
test_result = generate_tests(
    source_file="src/services/payment.py",
    target_coverage=80
)

if test_result.success:
    test_file = test_result.data['test_file']
    print(f"✅ Tests generated: {test_file}")

    # Step 2: Run tests to establish baseline
    print("\nStep 2: Running baseline tests...")
    baseline = run_tests(test_file=test_file)

    if baseline.success and baseline.data['failed'] == 0:
        print(f"✅ Baseline: {baseline.data['passed']} tests passing")

        # Step 3: Get refactoring suggestions
        print("\nStep 3: Getting refactoring suggestions...")
        suggestions = suggest_refactorings("src/services/payment.py", max_suggestions=3)

        # Step 4: Apply top suggestion with test verification
        print("\nStep 4: Applying refactoring with test verification...")
        top = suggestions.data['suggestions'][0]

        refactor_result = apply_refactoring(
            file_path="src/services/payment.py",
            refactoring_type=top['refactoring_type'],
            location={"start_line": top['line_number']},
            parameters=top['parameters'],
            run_tests=True  # Auto-verify with tests
        )

        if refactor_result.success:
            tests = refactor_result.data['test_results']
            if tests['failed'] == 0:
                print(f"✅ Refactoring successful! All {tests['passed']} tests still passing")
            else:
                print(f"❌ Refactoring broke {tests['failed']} tests (reverted)")
        else:
            print(f"❌ Refactoring failed: {refactor_result.error}")
    else:
        print("❌ Baseline tests failing - fix tests before refactoring")
else:
    print(f"❌ Test generation failed: {test_result.error}")
```

**Output:**
```
Step 1: Generating tests...
✅ Tests generated: tests/test_payment.py

Step 2: Running baseline tests...
✅ Baseline: 15 tests passing

Step 3: Getting refactoring suggestions...

Step 4: Applying refactoring with test verification...
✅ Refactoring successful! All 15 tests still passing
```

---

## Example 9: Batch Refactoring with Rollback

**Scenario:** Apply multiple refactorings but rollback if any fail.

```python
from skills.refactor_assistant.operations import (
    suggest_refactorings,
    apply_refactoring
)
import shutil
from pathlib import Path

def safe_batch_refactor(file_path, max_refactorings=5):
    """Apply multiple refactorings safely with rollback on failure."""

    # Create backup
    backup_path = f"{file_path}.batch_backup"
    shutil.copy(file_path, backup_path)

    print(f"Created backup: {backup_path}")

    # Get suggestions
    suggestions_result = suggest_refactorings(file_path, max_suggestions=max_refactorings)

    if not suggestions_result.success:
        print(f"❌ Could not get suggestions: {suggestions_result.error}")
        return False

    suggestions = suggestions_result.data['suggestions']
    print(f"Applying {len(suggestions)} refactorings...")

    successful_refactorings = []
    failed = False

    for i, suggestion in enumerate(suggestions, 1):
        print(f"\n{i}. {suggestion['description']}")

        result = apply_refactoring(
            file_path=file_path,
            refactoring_type=suggestion['refactoring_type'],
            location={"start_line": suggestion['line_number']},
            parameters=suggestion.get('parameters', {}),
            run_tests=True
        )

        if result.success:
            tests = result.data.get('test_results', {})
            if tests.get('failed', 0) == 0:
                print(f"   ✅ Success (tests: {tests.get('passed', 0)}/{tests.get('tests_run', 0)})")
                successful_refactorings.append(suggestion['description'])
            else:
                print(f"   ❌ Tests failed ({tests['failed']} failures)")
                failed = True
                break
        else:
            print(f"   ❌ Failed: {result.error}")
            failed = True
            break

    if failed:
        print(f"\n❌ Batch refactoring failed at step {i}")
        print("Rolling back all changes...")
        shutil.copy(backup_path, file_path)
        print("✅ Rollback complete")
        return False
    else:
        print(f"\n✅ All {len(successful_refactorings)} refactorings applied successfully:")
        for desc in successful_refactorings:
            print(f"  - {desc}")

        # Clean up backup
        Path(backup_path).unlink()
        return True

# Use it
success = safe_batch_refactor("src/services/payment.py", max_refactorings=5)

if success:
    print("\n🎉 Batch refactoring complete!")
else:
    print("\n⚠️  Some refactorings failed - file restored to original state")
```

**Output (Success Case):**
```
Created backup: src/services/payment.py.batch_backup
Applying 5 refactorings...

1. Extract validation logic into separate method
   ✅ Success (tests: 15/15)

2. Extract error handling into helper method
   ✅ Success (tests: 15/15)

3. Extract magic number 0.15 to named constant
   ✅ Success (tests: 15/15)

4. Rename unclear variable 'x' to descriptive name
   ✅ Success (tests: 15/15)

5. Simplify complex conditional with early returns
   ✅ Success (tests: 15/15)

✅ All 5 refactorings applied successfully:
  - Extract validation logic into separate method
  - Extract error handling into helper method
  - Extract magic number 0.15 to named constant
  - Rename unclear variable 'x' to descriptive name
  - Simplify complex conditional with early returns

🎉 Batch refactoring complete!
```

**Output (Failure Case):**
```
Created backup: src/services/payment.py.batch_backup
Applying 5 refactorings...

1. Extract validation logic into separate method
   ✅ Success (tests: 15/15)

2. Extract error handling into helper method
   ❌ Tests failed (3 failures)

❌ Batch refactoring failed at step 2
Rolling back all changes...
✅ Rollback complete

⚠️  Some refactorings failed - file restored to original state
```

---

## Best Practices Summary

### 1. Always Analyze Before Applying
- Use `detect_code_smells` or `suggest_refactorings` first
- Understand what you're changing and why

### 2. Use Severity Filtering
- Start with `severity_threshold="high"` for focused work
- Use `"critical"` when time is limited

### 3. Verify with Tests
- Always use `run_tests=True` for complex refactorings
- Generate tests first if they don't exist (use test_orchestrator)

### 4. Start Simple
- Begin with low-risk refactorings (rename, extract constant)
- Build confidence before complex transformations

### 5. Batch Carefully
- Apply multiple refactorings in sequence
- Implement rollback mechanism for safety

### 6. Integrate into Workflow
- Pre-commit hooks for quality gates
- CI/CD pipeline checks
- Regular code health monitoring

---

## Token Efficiency Tips

**Use severity filtering:**
```python
# Full report: ~2000 tokens
detect_code_smells("file.py", severity_threshold="low")

# Focused: ~400 tokens
detect_code_smells("file.py", severity_threshold="high")
```

**Limit suggestions:**
```python
# Many suggestions: ~3000 tokens
suggest_refactorings("file.py", max_suggestions=20)

# Focused: ~600 tokens
suggest_refactorings("file.py", max_suggestions=3)
```

**Skip tests when safe:**
```python
# With tests: ~2500 tokens
apply_refactoring(..., run_tests=True)

# Without tests (safe refactorings only): ~800 tokens
apply_refactoring(..., run_tests=False)
```

---

## Related Examples

- **test_orchestrator/examples.md** - Generating tests for refactoring safety
- **code_analysis/examples.md** - Deeper code analysis patterns
- **pr_review_assistant/examples.md** - Reviewing refactored code

---

*Last Updated: 2025-11-08*

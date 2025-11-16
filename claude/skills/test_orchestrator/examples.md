# Test Orchestrator - Usage Examples

Real-world examples demonstrating how to use test_orchestrator effectively.

---

## Example 1: Basic Test Generation

**Scenario:** You have a new Python module and need to generate tests quickly.

```python
from skills.test_orchestrator.operations import generate_tests

# Generate tests with default settings
result = generate_tests("src/services/payment.py")

if result.success:
    print(f"✓ Generated {result.data['tests_generated']} tests")
    print(f"  Test file: {result.data['test_file']}")
    print(f"  Estimated coverage: {result.data['coverage_estimate']}%")
    print(f"  Quality score: {result.data['quality_score']}")
    print(f"\nNext step: {result.data['next_step']}")
else:
    print(f"✗ Error: {result.error}")
    for suggestion in result.suggestions:
        print(f"  - {suggestion}")
```

**Output:**
```
✓ Generated 12 tests
  Test file: tests/test_payment.py
  Estimated coverage: 82.0%
  Quality score: 0.78

Next step: Run tests with: pytest tests/test_payment.py -v
```

---

## Example 2: Analyzing Before Generating

**Scenario:** Understand the code structure before generating tests.

```python
from skills.test_orchestrator.operations import analyze_file, generate_tests

# Step 1: Analyze the file (summary mode for efficiency)
analysis = analyze_file("src/auth/authentication.py")

print(f"File Analysis:")
print(f"  Functions: {analysis.data['total_functions']}")
print(f"  Classes: {analysis.data['total_classes']}")
print(f"  Avg Complexity: {analysis.data['avg_complexity']:.1f}")
print(f"  Most complex: {analysis.data['most_complex_function']}")

# Step 2: Decide coverage target based on complexity
if analysis.data['avg_complexity'] > 5:
    target = 90  # High complexity = high coverage
elif analysis.data['avg_complexity'] > 3:
    target = 85  # Moderate complexity
else:
    target = 75  # Low complexity

# Step 3: Generate tests with appropriate coverage
result = generate_tests(
    "src/auth/authentication.py",
    target_coverage=target
)

print(f"\n✓ Generated {result.data['tests_generated']} tests")
print(f"  Target coverage: {target}%")
print(f"  Estimated coverage: {result.data['coverage_estimate']}%")
```

**Output:**
```
File Analysis:
  Functions: 8
  Classes: 2
  Avg Complexity: 6.2
  Most complex: authenticate_user

✓ Generated 15 tests
  Target coverage: 90%
  Estimated coverage: 88.5%
```

---

## Example 3: TDD Workflow

**Scenario:** Write tests first, then implement functionality.

```python
from skills.test_orchestrator.operations import generate_tests, analyze_coverage

# Step 1: Generate tests for unimplemented code
print("Step 1: Generating tests for new feature...")
result = generate_tests(
    "src/features/user_profile.py",
    target_coverage=85,
    response_format="detailed"  # Get test code to review
)

if result.success:
    print(f"✓ Generated {result.data['tests_generated']} tests")

    # Review test code (optional)
    print("\nTest preview (first 500 chars):")
    print(result.data['test_content'][:500])
    print("...")

# Step 2: Run tests (they should fail - RED phase)
print("\nStep 2: Running tests (expect failures)...")
# Bash("pytest tests/test_user_profile.py -v")
# Output: All tests fail (not implemented yet)

# Step 3: Implement code (GREEN phase)
print("\nStep 3: Implement code to make tests pass...")
# User implements code in user_profile.py

# Step 4: Run tests again
print("\nStep 4: Re-running tests...")
# Bash("pytest tests/test_user_profile.py -v")
# Output: Tests pass

# Step 5: Check coverage
print("\nStep 5: Checking coverage...")
coverage = analyze_coverage(
    "tests/test_user_profile.py",
    "src/features/user_profile.py"
)

print(f"✓ Coverage: {coverage.data['coverage_percent']}%")
if coverage.data['coverage_percent'] >= 85:
    print("  Excellent coverage! ✓")
else:
    print(f"  Need {85 - coverage.data['coverage_percent']:.1f}% more coverage")
```

---

## Example 4: Coverage Gap Analysis

**Scenario:** Find and fix gaps in existing test suite.

```python
from skills.test_orchestrator.operations import analyze_coverage

# Step 1: Check current coverage (summary first)
coverage = analyze_coverage(
    "tests/test_payment_processor.py",
    "src/payment_processor.py"
)

print(f"Current Coverage: {coverage.data['coverage_percent']}%")
print(f"Gap Summary: {coverage.data['gap_summary']}")

# Step 2: If coverage is low, get detailed gaps
if coverage.data['coverage_percent'] < 80:
    print("\nCoverage below threshold! Getting details...")

    gaps = analyze_coverage(
        "tests/test_payment_processor.py",
        "src/payment_processor.py",
        response_format="detailed"
    )

    # Step 3: Show missing functions
    print(f"\nMissing Functions ({len(gaps.data['missing_functions'])}):")
    for func in gaps.data['missing_functions']:
        priority = func['priority'].upper()
        print(f"  [{priority}] {func['name']} (line {func['line_number']}, complexity: {func['complexity']})")

    # Step 4: Show missing branches
    print(f"\nMissing Branches ({len(gaps.data['missing_branches'])}):")
    for branch in gaps.data['missing_branches'][:5]:  # Show first 5
        print(f"  {branch['function']} (line {branch['line_number']})")
        print(f"    Condition: {branch['condition']}")
        print(f"    Missing: {branch['branch']} branch")
        print(f"    Edge case: {branch['edge_case']}")

    # Step 5: Show recommendations
    print(f"\nRecommendations:")
    for rec in gaps.data['recommendations']:
        print(f"  • {rec}")
```

**Output:**
```
Current Coverage: 68.5%
Gap Summary: 3 functions and 12 branches not covered

Coverage below threshold! Getting details...

Missing Functions (3):
  [HIGH] handle_refund (line 156, complexity: 7)
  [HIGH] process_chargeback (line 203, complexity: 6)
  [LOW] _log_transaction (line 89, complexity: 2)

Missing Branches (12):
  process_payment (line 45)
    Condition: if amount > 1000
    Missing: false branch
    Edge case: large payment validation

  validate_card (line 78)
    Condition: if card.expiry < today
    Missing: true branch
    Edge case: expired card

  ...

Recommendations:
  • Add tests for error handling in process_payment
  • Test edge case: large payment amounts (>$1000)
  • Cover expired card scenario in validate_card
  • Add timeout tests with mocks for network calls
```

---

## Example 5: Detailed Analysis for Complex File

**Scenario:** Deep dive into a complex file to understand testability.

```python
from skills.test_orchestrator.operations import analyze_file

# Get detailed analysis of complex file
analysis = analyze_file(
    "src/complex/order_processor.py",
    response_format="detailed"  # Get full details
)

if analysis.success:
    print(f"Source: {analysis.data['source_file']}")
    print(f"Total Functions: {analysis.data['total_functions']}")
    print(f"Total Complexity: {analysis.data['total_complexity']}")

    # Find high-complexity functions
    print("\nHigh-Complexity Functions (complexity > 5):")
    for func in analysis.data['functions']:
        if func['complexity'] > 5:
            print(f"\n  {func['name']} (complexity: {func['complexity']})")
            print(f"    Line: {func['line_number']}")
            print(f"    Parameters: {len(func['parameters'])}")

            # Show edge cases to test
            if func['edge_cases']:
                print(f"    Edge cases to test:")
                for edge in func['edge_cases']:
                    print(f"      - {edge}")

            # Show exceptions to handle
            if func['raises']:
                print(f"    Exceptions: {', '.join(func['raises'])}")

    # Show class structure
    print(f"\nClasses ({len(analysis.data['classes'])}):")
    for cls in analysis.data['classes']:
        print(f"\n  {cls['name']}")
        print(f"    Line: {cls['line_number']}")
        if cls['base_classes']:
            print(f"    Inherits from: {', '.join(cls['base_classes'])}")
        print(f"    Methods: {', '.join(cls['methods'])}")
```

**Output:**
```
Source: src/complex/order_processor.py
Total Functions: 15
Total Complexity: 78

High-Complexity Functions (complexity > 5):

  process_order (complexity: 12)
    Line: 45
    Parameters: 3
    Edge cases to test:
      - empty order
      - invalid items
      - out of stock items
      - payment failure
    Exceptions: ValueError, PaymentError, InventoryError

  calculate_shipping (complexity: 8)
    Line: 134
    Parameters: 2
    Edge cases to test:
      - international shipping
      - oversized items
      - express delivery
    Exceptions: ShippingError

Classes (2):

  OrderProcessor
    Line: 10
    Inherits from: ABC, LoggerMixin
    Methods: process, validate, calculate_total, apply_discounts

  OrderValidator
    Line: 156
    Methods: validate_items, validate_payment, validate_shipping
```

---

## Example 6: Batch Test Generation

**Scenario:** Generate tests for multiple related files.

```python
from skills.test_orchestrator.operations import generate_tests
from pathlib import Path

# Find all Python files in a directory
source_dir = Path("src/services")
python_files = list(source_dir.glob("*.py"))

print(f"Found {len(python_files)} Python files in {source_dir}")

results = []
for py_file in python_files:
    print(f"\nProcessing: {py_file.name}...")

    result = generate_tests(
        str(py_file),
        target_coverage=80
    )

    if result.success:
        results.append({
            'file': py_file.name,
            'tests': result.data['tests_generated'],
            'coverage': result.data['coverage_estimate'],
            'test_file': result.data['test_file']
        })
        print(f"  ✓ {result.data['tests_generated']} tests generated")
    else:
        print(f"  ✗ Error: {result.error}")

# Summary
print("\n" + "="*60)
print("SUMMARY")
print("="*60)
total_tests = sum(r['tests'] for r in results)
avg_coverage = sum(r['coverage'] for r in results) / len(results) if results else 0

print(f"Files processed: {len(results)}/{len(python_files)}")
print(f"Total tests generated: {total_tests}")
print(f"Average coverage: {avg_coverage:.1f}%")

print("\nDetails:")
for r in results:
    print(f"  {r['file']}: {r['tests']} tests ({r['coverage']:.1f}% coverage)")
```

**Output:**
```
Found 5 Python files in src/services

Processing: payment.py...
  ✓ 12 tests generated

Processing: inventory.py...
  ✓ 8 tests generated

Processing: shipping.py...
  ✓ 10 tests generated

Processing: notification.py...
  ✓ 6 tests generated

Processing: logging.py...
  ✗ Error: File contains no testable functions

============================================================
SUMMARY
============================================================
Files processed: 4/5
Total tests generated: 36
Average coverage: 82.5%

Details:
  payment.py: 12 tests (85.0% coverage)
  inventory.py: 8 tests (78.5% coverage)
  shipping.py: 10 tests (84.2% coverage)
  notification.py: 6 tests (82.3% coverage)
```

---

## Example 7: Integration with Code Review

**Scenario:** Check test coverage as part of PR review process.

```python
from skills.test_orchestrator.operations import analyze_coverage

# Files changed in this PR (from git diff)
changed_files = [
    "src/features/new_feature.py",
    "src/utils/helpers.py"
]

print("PR Test Coverage Check")
print("="*60)

coverage_results = []
for source_file in changed_files:
    # Determine expected test file location
    test_file = source_file.replace("src/", "tests/test_")

    # Check coverage
    coverage = analyze_coverage(test_file, source_file)

    coverage_results.append({
        'file': source_file,
        'coverage': coverage.data['coverage_percent'] if coverage.success else 0,
        'status': coverage.success
    })

    if coverage.success:
        status = "✓" if coverage.data['coverage_percent'] >= 80 else "✗"
        print(f"{status} {source_file}: {coverage.data['coverage_percent']}%")

        if coverage.data['coverage_percent'] < 80:
            print(f"    {coverage.data['gap_summary']}")
            print(f"    Recommendation: {coverage.data['recommendation']}")
    else:
        print(f"✗ {source_file}: No test file found")

# Overall verdict
print("\n" + "="*60)
all_covered = all(
    r['status'] and r['coverage'] >= 80
    for r in coverage_results
)

if all_covered:
    print("✓ PR APPROVED: All files have adequate test coverage")
else:
    print("✗ PR BLOCKED: Insufficient test coverage")
    print("\nAction required:")
    for r in coverage_results:
        if not r['status'] or r['coverage'] < 80:
            print(f"  - Add tests for {r['file']}")
```

**Output:**
```
PR Test Coverage Check
============================================================
✓ src/features/new_feature.py: 87.5%
✗ src/utils/helpers.py: 62.3%
    3 functions and 8 branches not covered
    Recommendation: Focus on testing error handling paths

============================================================
✗ PR BLOCKED: Insufficient test coverage

Action required:
  - Add tests for src/utils/helpers.py
```

---

## Example 8: Progressive Test Development

**Scenario:** Build test suite incrementally, starting simple.

```python
from skills.test_orchestrator.operations import generate_tests, analyze_coverage

source_file = "src/data/processor.py"

# Phase 1: Start with basic coverage (quick wins)
print("Phase 1: Basic test coverage (60%)")
result = generate_tests(source_file, target_coverage=60)
print(f"  ✓ Generated {result.data['tests_generated']} tests")

# Check what we have
coverage = analyze_coverage(f"tests/test_processor.py", source_file)
print(f"  Coverage: {coverage.data['coverage_percent']}%\n")

# Phase 2: Increase to standard coverage
print("Phase 2: Standard coverage (80%)")
result = generate_tests(source_file, target_coverage=80)
print(f"  ✓ Generated {result.data['tests_generated']} tests")

coverage = analyze_coverage(f"tests/test_processor.py", source_file)
print(f"  Coverage: {coverage.data['coverage_percent']}%\n")

# Phase 3: Identify remaining gaps
print("Phase 3: Identify specific gaps")
gaps = analyze_coverage(
    f"tests/test_processor.py",
    source_file,
    response_format="detailed"
)

if gaps.data['missing_functions']:
    print(f"  Missing {len(gaps.data['missing_functions'])} functions:")
    for func in gaps.data['missing_functions'][:3]:
        print(f"    - {func['name']} (priority: {func['priority']})")

# Phase 4: Target high-priority gaps
print("\nPhase 4: Add high-priority tests (manual refinement)")
print("  Review gaps and add targeted tests for:")
for rec in gaps.data['recommendations'][:3]:
    print(f"    • {rec}")
```

**Output:**
```
Phase 1: Basic test coverage (60%)
  ✓ Generated 8 tests
  Coverage: 62.5%

Phase 2: Standard coverage (80%)
  ✓ Generated 14 tests
  Coverage: 78.3%

Phase 3: Identify specific gaps
  Missing 2 functions:
    - handle_error (priority: high)
    - _validate_schema (priority: medium)

Phase 4: Add high-priority tests (manual refinement)
  Review gaps and add targeted tests for:
    • Add tests for error handling in handle_error
    • Test edge case: invalid schema formats
    • Cover timeout scenarios with mocks
```

---

## Example 9: Token-Efficient Workflow

**Scenario:** Minimize token usage while generating comprehensive tests.

```python
from skills.test_orchestrator.operations import (
    analyze_file,
    generate_tests,
    analyze_coverage
)

# ✅ EFFICIENT: Use summary formats
print("Token-Efficient Workflow")
print("="*60)

# Step 1: Quick analysis (summary format - ~300 tokens)
analysis = analyze_file("src/billing.py")  # Default: summary
print(f"1. Analysis: {analysis.data['total_functions']} functions")
print(f"   Token estimate: ~300")

# Step 2: Generate tests (concise format - ~500 tokens)
tests = generate_tests("src/billing.py")  # Default: concise
print(f"2. Test generation: {tests.data['tests_generated']} tests")
print(f"   Token estimate: ~500")

# Step 3: Check coverage (summary format - ~300 tokens)
coverage = analyze_coverage("tests/test_billing.py", "src/billing.py")
print(f"3. Coverage check: {coverage.data['coverage_percent']}%")
print(f"   Token estimate: ~300")

# Step 4: Get details ONLY if needed
if coverage.data['coverage_percent'] < 80:
    gaps = analyze_coverage(
        "tests/test_billing.py",
        "src/billing.py",
        response_format="detailed"  # Only now request details
    )
    print(f"4. Gap analysis: {len(gaps.data['missing_functions'])} functions")
    print(f"   Token estimate: ~2000")

    total_tokens = 300 + 500 + 300 + 2000  # 3100 tokens
else:
    print(f"4. Coverage adequate, skip gap analysis")
    total_tokens = 300 + 500 + 300  # 1100 tokens

print(f"\nTotal tokens used: ~{total_tokens}")
print("\n❌ INEFFICIENT alternative would use: ~15000 tokens")
print(f"   Savings: {((15000 - total_tokens) / 15000 * 100):.1f}%")
```

---

## Common Patterns

### Pattern: Error Recovery

```python
result = generate_tests("payment.py")

if not result.success:
    print(f"Error: {result.error}")

    # Try suggestions
    if result.error_code == "FILE_NOT_FOUND":
        # Use suggestion to find file
        from skills.common.tools import Glob
        files = Glob("**/*payment*.py")
        print(f"Did you mean one of these? {files}")

    # Or use example fix
    print(f"Example: {result.example_fix}")
```

### Pattern: Conditional Detail Level

```python
# Start with summary
result = analyze_file("complex.py")

# Request details only for complex files
if result.data['total_complexity'] > 50:
    detailed = analyze_file("complex.py", response_format="detailed")
    # Now work with detailed data
```

### Pattern: Iterative Coverage

```python
target_coverage = 80
max_iterations = 3

for i in range(max_iterations):
    # Generate tests
    generate_tests("file.py", target_coverage=target_coverage)

    # Check coverage
    coverage = analyze_coverage("test_file.py", "file.py")

    if coverage.data['coverage_percent'] >= target_coverage:
        print(f"✓ Reached {target_coverage}% coverage in {i+1} iterations")
        break

    # Increase target for next iteration
    target_coverage += 5
```

---

## Next Steps

- Review **reference.md** for complete API documentation
- Try these examples with your own code
- Combine with **pr_review_assistant** for comprehensive quality checks
- Integrate into CI/CD pipeline for automated test generation

---

*Last Updated: 2025-11-07*

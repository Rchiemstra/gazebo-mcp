# Verification Skill Examples

Practical usage examples for the verification skill.

---

## Example 1: Validate Student Code Submission

```python
from skills.verification import validate_code

# Student submits code
student_code = '''
def calculate_average(numbers):
    total = sum(numbers)
    return total / len(numbers)
'''

# Validate the code
result = validate_code(student_code)

if result.success:
    if result.data['is_valid']:
        print("✅ Code is valid!")
        print(f"Found {result.data['issue_count']} style suggestions")
    else:
        print("❌ Code has errors:")
        for issue in result.data.get('top_issues', []):
            print(f"  - {issue}")
```

---

## Example 2: Verify Program Output

```python
from skills.verification import validate_output

# Expected output from exercise
expected = "Hello, World!"

# Student's program output
actual = student_program_output

# Validate
result = validate_output(expected, actual, match_type="exact")

if result.success:
    if result.data['is_match']:
        print("✅ Output matches!")
    else:
        print(f"❌ Output differs (similarity: {result.data['similarity_score']:.0%})")
        # Get detailed diff
        detailed = validate_output(expected, actual, response_format="detailed")
        print("\nDifferences:")
        for diff in detailed.data['differences'][:5]:
            print(f"  {diff}")
```

---

## Example 3: Check Test Coverage

```python
from skills.verification import validate_tests

source_code = '''
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b
'''

test_code = '''
def test_add():
    """Test addition"""
    assert add(2, 3) == 5
'''

# Validate tests with coverage
result = validate_tests(test_code, source_code, response_format="detailed")

if result.success:
    print(f"Tests: {result.data['test_count']}")
    print(f"Coverage: {result.data['coverage_ratio']:.0%}")
    print(f"Covered: {result.data['covered_functions']}")

    if result.data.get('suggestions_for_improvement'):
        print("\nSuggestions:")
        for suggestion in result.data['suggestions_for_improvement']:
            print(f"  - {suggestion}")
```

---

## Example 4: Automated Code Review Workflow

```python
from skills.verification import validate_code, validate_tests

def review_submission(code, tests):
    """Complete code review workflow"""
    print("🔍 Reviewing submission...")

    # 1. Validate code
    code_result = validate_code(code, response_format="detailed")
    if not code_result.success:
        return f"Error: {code_result.error}"

    # 2. Check for critical errors
    if not code_result.data['is_valid']:
        errors = [i for i in code_result.data['issues'] if i['severity'] == 'error']
        print(f"❌ Found {len(errors)} error(s)")
        for error in errors:
            print(f"  Line {error['line']}: {error['message']}")
        return "Please fix errors before resubmitting"

    # 3. Validate tests
    test_result = validate_tests(tests, code, response_format="detailed")
    if not test_result.success:
        return f"Test validation error: {test_result.error}"

    # 4. Check test quality
    if test_result.data['test_count'] == 0:
        return "Please add tests for your code"

    coverage = test_result.data.get('coverage_ratio', 0)
    if coverage < 0.8:
        print(f"⚠️  Test coverage is {coverage:.0%}, aim for 80%+")
        print("Missing tests for:")
        uncovered = set(code_result.data['metrics']['functions']) - set(test_result.data['covered_functions'])
        for func in uncovered:
            print(f"  - {func}()")

    # 5. Summary
    print(f"\n✅ Review complete!")
    print(f"  Code: {code_result.data['warning_count']} warnings")
    print(f"  Tests: {test_result.data['test_count']} tests, {coverage:.0%} coverage")

    return "Looks good!"

# Use it
result = review_submission(student_code, student_tests)
print(result)
```

---

## Example 5: JSON Output Validation

```python
from skills.verification import validate_output
import json

# Expected JSON structure
expected = {
    "status": "success",
    "data": {
        "user": "Alice",
        "score": 100
    }
}

# Student's program output (as string)
actual_output = '''{
    "status": "success",
    "data": {
        "user": "Alice",
        "score": 100
    }
}'''

# Validate JSON
result = validate_output(
    expected=json.dumps(expected),
    actual=actual_output,
    match_type="json"
)

if result.success and result.data['is_match']:
    print("✅ JSON output is correct!")
else:
    print(f"❌ JSON mismatch (similarity: {result.data['similarity_score']:.0%})")
```

---

## Example 6: Regex Pattern Validation

```python
from skills.verification import validate_output

# Expected pattern: email address
pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# Student's output
email = "student@university.edu"

# Validate
result = validate_output(
    expected=pattern,
    actual=email,
    match_type="regex"
)

if result.success and result.data['is_match']:
    print("✅ Valid email format!")
else:
    print("❌ Invalid email format")
```

---

## Example 7: Security Check

```python
from skills.verification import validate_code

# Code with potential security issues
risky_code = '''
def run_command(cmd):
    return eval(cmd)  # Security risk!
'''

# Validate with security checks
result = validate_code(risky_code, check_security=True, response_format="detailed")

if result.success:
    security_issues = [
        i for i in result.data['issues']
        if i['category'] == 'security'
    ]

    if security_issues:
        print("⚠️  Security issues found:")
        for issue in security_issues:
            print(f"  {issue['message']}")
            if issue['suggestion']:
                print(f"  Suggestion: {issue['suggestion']}")
```

---

## Example 8: Progressive Testing Feedback

```python
from skills.verification import validate_tests

def provide_test_feedback(test_code, source_code, student_level="beginner"):
    """Provide feedback appropriate to student level"""

    # Validate tests
    result = validate_tests(test_code, source_code, response_format="detailed")

    if not result.success:
        return f"Error: {result.error}"

    feedback = []

    # Basic feedback for all levels
    feedback.append(f"You wrote {result.data['test_count']} test(s).")

    # Beginner: Focus on basics
    if student_level == "beginner":
        if result.data['test_count'] == 0:
            feedback.append("Start by writing one simple test.")
        else:
            feedback.append("Great start! Your tests are running.")

            no_assertions = [i for i in result.data['issues'] if 'no assertions' in i]
            if no_assertions:
                feedback.append("Remember: tests need assertions to check results.")
                feedback.append("Example: assert add(2, 3) == 5")

    # Intermediate: Coverage
    elif student_level == "intermediate":
        coverage = result.data.get('coverage_ratio', 0)
        feedback.append(f"Coverage: {coverage:.0%}")

        if coverage < 0.6:
            feedback.append("Try to cover more functions with tests.")
            suggestions = result.data.get('suggestions_for_improvement', [])
            if suggestions:
                feedback.append(f"Next: {suggestions[0]}")

    # Advanced: Quality
    else:
        metrics = result.data['metrics']
        tests_with_docs = metrics.get('tests_with_docstrings', 0)
        if tests_with_docs < result.data['test_count']:
            feedback.append("Consider adding docstrings to all tests.")

        suggestions = result.data.get('suggestions_for_improvement', [])
        edge_cases = [s for s in suggestions if 'edge case' in s.lower()]
        if edge_cases:
            feedback.append("Don't forget edge cases!")

    return "\n".join(feedback)

# Use it
feedback = provide_test_feedback(student_tests, source_code, student_level="beginner")
print(feedback)
```

---

## Integration with Other Skills

### With test_orchestrator

```python
from skills.test_orchestrator import generate_tests
from skills.verification import validate_tests

# 1. Generate tests automatically
result = generate_tests("payment.py")
generated_tests = result.data['test_code']

# 2. Validate generated tests
validation = validate_tests(generated_tests, source_code="payment.py")

print(f"Generated {validation.data['test_count']} tests")
print(f"Coverage: {validation.data.get('coverage_ratio', 0):.0%}")
```

### With code_analysis

```python
from skills.code_analysis import analyze_file
from skills.verification import validate_code

# 1. Analyze complexity
analysis = analyze_file("module.py")

# 2. Validate code quality
validation = validate_code(code_string)

# 3. Combine insights
if validation.data['is_valid'] and analysis.data['total_complexity'] < 20:
    print("✅ Code is valid and not too complex")
```

---

## Common Patterns

### Pattern: Validate Then Provide Feedback

```python
result = validate_code(code)
if result.success:
    if result.data['is_valid']:
        provide_positive_feedback()
    else:
        provide_improvement_guidance(result.data['top_issues'])
```

### Pattern: Progressive Disclosure

```python
# Start with summary
result = validate_code(code)

# If issues found, get details
if result.data['issue_count'] > 0:
    detailed = validate_code(code, response_format="detailed")
    analyze_specific_issues(detailed.data['issues'])
```

### Pattern: Test-Driven Learning

```python
# 1. Student writes test
test_result = validate_tests(student_test)

# 2. Student writes code
code_result = validate_code(student_code)

# 3. Verify output
output_result = validate_output(expected, actual)

# 4. Check all pass
if all([r.success and r.data.get('is_valid') or r.data.get('is_match')
        for r in [test_result, code_result, output_result]]):
    print("🎉 Exercise complete!")
```

---

## Tips

1. **Use summary format first** - Get overview before details
2. **Provide actionable feedback** - Use suggestions from detailed mode
3. **Combine validations** - Code + tests + output = complete verification
4. **Adapt to student level** - Beginners need simpler feedback
5. **Celebrate success** - Validate what works, not just errors

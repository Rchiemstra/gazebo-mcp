# Tests Directory Guide

This directory contains the test suite for the Claude Code Learning System.

---

## 📋 What's in This Directory

This directory contains **unit tests**, **integration tests**, and **test utilities** that ensure the system works correctly and reliably.

---

## 🔍 Using Metadata for Navigation

**Skills have YAML frontmatter** in their SKILL.md files:
```yaml
---
name: test-orchestrator
category: testing
tools: [Read, Write, Bash]
dependencies: []
---
```

**Quick skill discovery:**
```bash
# Find skills by category
grep "category: testing" ../skills/*/SKILL.md

# Find skills using specific tools
grep "tools:.*Bash" ../skills/*/SKILL.md

# Find skills with no dependencies
grep "dependencies: \[\]" ../skills/*/SKILL.md
```

**Progressive disclosure pattern:**
1. Load SKILL.md first (~200-500 tokens) - Quick overview
2. Load reference.md on demand - Complete API
3. Load examples.md as needed - Usage patterns

---

## 📁 Directory Structure

### Test Organization

```
tests/
├── CLAUDE.md                    # This file
├── conftest.py                 # Pytest configuration and fixtures
├── test_*.py                   # Unit tests for individual modules
├── integration/                # Integration tests
│   └── test_*.py
├── fixtures/                   # Test data and fixtures
│   ├── sample_code/
│   ├── sample_plans/
│   └── sample_data/
└── utils/                      # Test utilities
    └── *.py
```

### Test Files by Component

**Skills Tests:**
- `test_test_orchestrator.py` - Test generation and coverage analysis
- `test_code_analysis.py` - AST analysis and complexity metrics
- `test_learning_plan_manager.py` - Plan parsing and management
- `test_learning_analytics.py` - Progress tracking and analytics
- `test_session_state.py` - Session management
- `test_code_search.py` - Code search functionality
- `test_refactor_assistant.py` - Refactoring operations
- `test_pr_review_assistant.py` - PR review automation
- `test_git_workflow_assistant.py` - Git operations
- `test_dependency_guardian.py` - Dependency analysis
- `test_doc_generator.py` - Documentation generation
- `test_interactive_diagram.py` - Diagram generation

**Integration Tests:**
- `integration/test_skill_composition.py` - Multi-skill workflows
- `integration/test_agent_coordination.py` - Agent interactions
- `integration/test_end_to_end.py` - Complete workflows

**Utilities:**
- `utils/test_helpers.py` - Test helper functions
- `utils/mock_data.py` - Mock data generators

---

## 🚀 Running Tests

### Quick Start

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_code_analysis.py

# Run specific test function
pytest tests/test_code_analysis.py::test_analyze_codebase

# Run tests matching pattern
pytest -k "test_token_efficiency"
```

### With Coverage

```bash
# Run tests with coverage report
pytest --cov=skills --cov-report=html

# View coverage report
open htmlcov/index.html

# Coverage for specific module
pytest --cov=skills.code_analysis tests/test_code_analysis.py

# Show missing lines
pytest --cov=skills --cov-report=term-missing
```

### Common Test Commands

```bash
# Fast: Run only unit tests (skip slow integration tests)
pytest -m "not integration"

# Slow: Run only integration tests
pytest -m integration

# Failed: Re-run only failed tests
pytest --lf

# Debug: Stop at first failure
pytest -x

# Parallel: Run tests in parallel (requires pytest-xdist)
pytest -n auto

# Markers: Run tests with specific marker
pytest -m "smoke"  # Quick smoke tests
pytest -m "slow"   # Long-running tests
```

---

## 📝 Writing Tests

### Test Structure Template

```python
"""
Tests for [component_name].

This module tests:
- [Functionality 1]
- [Functionality 2]
- [Edge cases]
"""

import pytest
from skills.component import operation


class TestComponentName:
    """Tests for ComponentName."""

    def test_basic_functionality(self):
        """Test basic use case."""
        # Arrange
        input_data = "test"

        # Act
        result = operation(input_data)

        # Assert
        assert result.success is True
        assert result.data is not None

    def test_error_handling(self):
        """Test error cases."""
        # Test with invalid input
        result = operation(invalid_input)

        assert result.success is False
        assert result.error_code == "EXPECTED_ERROR_CODE"
        assert len(result.suggestions) > 0

    @pytest.mark.parametrize("input,expected", [
        ("case1", "output1"),
        ("case2", "output2"),
        ("case3", "output3"),
    ])
    def test_multiple_cases(self, input, expected):
        """Test multiple input cases."""
        result = operation(input)
        assert result.data == expected
```

### Test Fixtures

Common fixtures are defined in `conftest.py`:

```python
# Use fixtures in your tests
def test_with_sample_code(sample_python_file):
    """Test using sample code fixture."""
    result = analyze_file(sample_python_file)
    assert result.success is True

def test_with_temp_dir(tmp_path):
    """Test using temporary directory."""
    test_file = tmp_path / "test.py"
    test_file.write_text("print('hello')")
    # Test with test_file
```

### Testing Best Practices

**1. Arrange-Act-Assert Pattern:**
```python
def test_operation():
    # Arrange: Set up test data
    input_data = create_test_data()

    # Act: Execute the operation
    result = operation(input_data)

    # Assert: Verify the result
    assert result.success is True
    assert result.data["key"] == "expected_value"
```

**2. Test One Thing:**
```python
# ✅ Good: Tests one specific behavior
def test_returns_error_for_missing_file():
    result = analyze_file("nonexistent.py")
    assert result.success is False
    assert result.error_code == "FILE_NOT_FOUND"

# ❌ Bad: Tests multiple unrelated things
def test_everything():
    # Tests file analysis, error handling, and formatting
    # Should be 3 separate tests
```

**3. Descriptive Names:**
```python
# ✅ Good: Clear what it tests
def test_analyze_file_returns_function_count_in_summary_format():
    pass

# ❌ Bad: Unclear what it tests
def test_analyze():
    pass
```

**4. Use Fixtures for Setup:**
```python
@pytest.fixture
def sample_payment_code():
    """Fixture providing sample payment code."""
    return '''
def process_payment(amount, card):
    if amount <= 0:
        raise ValueError("Invalid amount")
    return charge_card(card, amount)
'''

def test_analyze_payment_code(sample_payment_code, tmp_path):
    """Test analyzing payment code."""
    # Use the fixture
    file_path = tmp_path / "payment.py"
    file_path.write_text(sample_payment_code)

    result = analyze_file(str(file_path))
    assert result.data["total_functions"] == 1
```

---

## 🧪 Test Categories

### Unit Tests

**Purpose:** Test individual functions/classes in isolation

**Characteristics:**
- Fast (< 0.1s each)
- No external dependencies
- Use mocks for dependencies
- Test one component at a time

**Example:**
```python
def test_result_filter_search():
    """Test ResultFilter.search function."""
    data = [
        {"name": "payment.py", "path": "src/payment.py"},
        {"name": "auth.py", "path": "src/auth.py"},
    ]

    result = ResultFilter.search(data, "payment", ["name", "path"])

    assert len(result) == 1
    assert result[0]["name"] == "payment.py"
```

### Integration Tests

**Purpose:** Test multiple components working together

**Characteristics:**
- Slower (0.1s - 5s each)
- Test real interactions
- Minimal mocking
- Test workflows

**Example:**
```python
@pytest.mark.integration
def test_analyze_and_generate_tests_workflow(tmp_path):
    """Test complete analysis → test generation workflow."""
    # Create source file
    source = tmp_path / "payment.py"
    source.write_text(SAMPLE_CODE)

    # Analyze
    analysis = analyze_file(str(source))
    assert analysis.success

    # Generate tests based on analysis
    tests = generate_tests(
        str(source),
        target_coverage=analysis.data["avg_complexity"] * 10
    )
    assert tests.success
    assert tests.data["tests_generated"] > 0
```

### End-to-End Tests

**Purpose:** Test complete user workflows

**Characteristics:**
- Slowest (1s - 30s each)
- Test from user perspective
- Real file I/O
- Complete scenarios

**Example:**
```python
@pytest.mark.e2e
def test_complete_learning_workflow(tmp_path):
    """Test complete learning plan workflow."""
    # Create plan
    plan = create_learning_plan(
        topic="Python Testing",
        student_level="beginner"
    )

    # Save plan
    plan_file = tmp_path / "testing-plan.md"
    save_plan(plan, str(plan_file))

    # Load and verify
    loaded = load_plan(str(plan_file))
    assert loaded.success
    assert loaded.data["topic"] == "Python Testing"

    # Track progress
    update_progress(str(plan_file), phase=1, task=1, status="completed")

    # Analyze progress
    analytics = analyze_progress(str(plan_file))
    assert analytics.data["velocity"] > 0
```

---

## 🎯 Test Markers

Use pytest markers to categorize tests:

```python
# Mark slow tests
@pytest.mark.slow
def test_large_codebase_analysis():
    pass

# Mark integration tests
@pytest.mark.integration
def test_skill_composition():
    pass

# Mark tests requiring network
@pytest.mark.network
def test_external_api():
    pass

# Mark smoke tests (quick sanity checks)
@pytest.mark.smoke
def test_basic_import():
    pass

# Skip test conditionally
@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
def test_unix_specific():
    pass
```

Run tests by marker:
```bash
pytest -m "not slow"        # Skip slow tests
pytest -m "smoke"           # Run only smoke tests
pytest -m "integration"     # Run integration tests
```

---

## 📊 Test Coverage Goals

### Coverage Targets

| Component | Target | Current |
|-----------|--------|---------|
| Core skills | 90%+ | TBD |
| Utilities | 85%+ | TBD |
| Integration | 70%+ | TBD |
| Examples | 50%+ | TBD |

### Coverage Reports

```bash
# Generate HTML coverage report
pytest --cov=skills --cov-report=html

# Check coverage percentage
pytest --cov=skills --cov-report=term

# Fail if coverage below threshold
pytest --cov=skills --cov-fail-under=80
```

### What to Test

**High Priority (Must Test):**
- ✅ Core skill operations (analyze, generate, etc.)
- ✅ Error handling and validation
- ✅ Agent-friendly error messages
- ✅ Token efficiency (response formats)
- ✅ Data transformations
- ✅ Security boundaries

**Medium Priority (Should Test):**
- ⚠️ Edge cases and boundary conditions
- ⚠️ Integration between skills
- ⚠️ File I/O operations
- ⚠️ Configuration parsing

**Low Priority (Nice to Have):**
- 📝 Example scripts
- 📝 Documentation generation
- 📝 Utility functions

---

## 🛠️ Test Utilities

### Mock Data Generators

```python
from tests.utils.mock_data import (
    create_sample_python_file,
    create_sample_learning_plan,
    create_sample_codebase
)

def test_with_sample_data():
    """Test using generated mock data."""
    sample_file = create_sample_python_file(
        functions=5,
        classes=2,
        complexity="high"
    )

    result = analyze_file(sample_file)
    assert result.data["total_functions"] == 5
```

### Test Helpers

```python
from tests.utils.test_helpers import (
    assert_success,
    assert_error,
    assert_token_count_below
)

def test_with_helpers():
    """Test using helper assertions."""
    result = operation()

    # Use helper for common assertions
    assert_success(result)
    assert result.data["key"] == "value"
```

### Fixtures

Common fixtures available:

```python
def test_example(
    tmp_path,              # Temporary directory
    sample_python_file,    # Sample Python code
    sample_learning_plan,  # Sample learning plan
    mock_anthropic_client  # Mocked API client
):
    """Test using multiple fixtures."""
    # Use fixtures in test
    pass
```

---

## 🔍 Debugging Tests

### Print Debugging

```python
def test_with_debug_output(capsys):
    """Test with debug output."""
    result = operation()

    # Debug output
    print(f"Result: {result}")
    print(f"Data: {result.data}")

    # Capture output
    captured = capsys.readouterr()
    assert "Result:" in captured.out
```

### Pytest Debugging

```bash
# Stop at first failure
pytest -x

# Drop into debugger on failure
pytest --pdb

# Show local variables on failure
pytest -l

# Verbose output
pytest -vv

# Show print statements
pytest -s
```

### VS Code Debugging

Add to `.vscode/launch.json`:

```json
{
    "name": "Python: Pytest Current File",
    "type": "python",
    "request": "launch",
    "module": "pytest",
    "args": [
        "${file}",
        "-v"
    ],
    "console": "integratedTerminal"
}
```

---

## 🔐 Security & Test Safety

### Safe Testing Practices

**Test Isolation:**
- Tests run in isolated environments
- Use `tmp_path` fixture for file operations
- Mock external services and network calls
- Clean up resources after each test

**Testing Security Features:**
```python
def test_sandboxing_blocks_unauthorized_access():
    """Test that sandboxing prevents unauthorized file access."""
    # Attempt to access file outside sandbox
    result = read_file("/etc/passwd")

    # Should be blocked
    assert result.success is False
    assert result.error_code == "ACCESS_DENIED"
```

**Testing Tool Permissions:**
```python
def test_skill_respects_tool_allowlist():
    """Test that skills only use allowed tools."""
    skill = load_skill("test_orchestrator")

    # Check tool usage
    assert "Read" in skill.allowed_tools
    assert "Write" in skill.allowed_tools

    # Verify unauthorized tools are rejected
    with pytest.raises(PermissionError):
        skill.use_tool("WebFetch")
```

### Security Test Categories

**1. Sandboxing Tests:**
- Filesystem access boundaries
- Network request filtering
- Process isolation
- Tool permission enforcement

**2. Input Validation Tests:**
- Path traversal prevention
- Command injection prevention
- SQL injection prevention (if applicable)
- XSS prevention (if applicable)

**3. Authentication/Authorization Tests:**
- Tool permission checks
- Agent access control
- API key handling
- Token validation

### Test Data Security

**Safe Test Data:**
```python
# ✅ Good: Use mock/fake data
MOCK_API_KEY = "test_key_12345"
FAKE_USER = {"name": "Test User", "id": "test_123"}

# ❌ Bad: Use real credentials
API_KEY = os.environ["REAL_API_KEY"]  # Don't do this!
```

**Sensitive Data in Tests:**
- Never commit real credentials
- Use environment variables for secrets (with test defaults)
- Mock external API calls
- Use `.env.test` for test-specific config

### Running Security Tests

```bash
# Run security-focused tests
pytest -m security

# Run with coverage
pytest --cov=skills --cov-report=html -m security

# Test specific security feature
pytest tests/test_sandboxing.py -v
```

**Security Test Markers:**
```python
@pytest.mark.security
def test_prevents_path_traversal():
    """Test path traversal prevention."""
    pass

@pytest.mark.security
@pytest.mark.slow
def test_full_sandboxing_suite():
    """Comprehensive sandboxing test."""
    pass
```

### Testing in Sandboxed Environment

All tests automatically run in sandboxed environment:
- **Filesystem**: Limited to test directories
- **Network**: Mocked or isolated
- **Resources**: Cleaned up after tests

**Verify Sandboxing:**
```python
def test_sandbox_active():
    """Verify sandbox is active during tests."""
    import os

    # Should be in test directory
    cwd = os.getcwd()
    assert "tests" in cwd or "tmp" in cwd

    # Should not access system dirs
    with pytest.raises(PermissionError):
        open("/etc/passwd").read()
```

### Security Regression Tests

**Purpose:** Ensure security fixes aren't broken by future changes

```python
@pytest.mark.security
@pytest.mark.regression
def test_cve_2024_xxxx_fixed():
    """Test that CVE-2024-XXXX vulnerability is fixed."""
    # Test the specific vulnerability
    result = vulnerable_function(malicious_input)

    # Verify it's blocked
    assert result.success is False
    assert "blocked" in result.error.lower()
```

**When to Add Regression Tests:**
- After fixing security vulnerabilities
- After adding new security features
- After updating dependencies with security fixes

See `../docs/SANDBOXING_GUIDE.md` for complete security testing guidelines.

---

## 📚 Related Documentation

- `../CLAUDE.md` - Project navigation
- `../skills/CLAUDE.md` - Skills to test
- `../docs/SANDBOXING_GUIDE.md` - Security considerations
- `../examples/CLAUDE.md` - Example usage to test

---

## 🎓 Testing Best Practices Summary

### Do's ✅

- **Write tests first** (TDD when possible)
- **Test one thing** per test function
- **Use descriptive names** that explain what's tested
- **Use fixtures** for common setup
- **Mock external dependencies** in unit tests
- **Test error cases** as thoroughly as success cases
- **Keep tests fast** (< 0.1s for unit tests)
- **Use parametrize** for multiple similar cases
- **Clean up** resources after tests
- **Maintain high coverage** (80%+ for core code)

### Don'ts ❌

- **Don't test implementation details** - test behavior
- **Don't write flaky tests** - ensure consistency
- **Don't skip cleanup** - prevent test pollution
- **Don't ignore warnings** - fix or suppress explicitly
- **Don't over-mock** - test real interactions when possible
- **Don't write slow unit tests** - move to integration
- **Don't test third-party code** - trust their tests
- **Don't duplicate coverage** - one test per behavior

---

## 🚀 Quick Reference

### Run Common Test Suites

```bash
# Smoke tests (quick sanity check)
pytest -m smoke

# Unit tests only (fast)
pytest -m "not integration and not slow"

# Pre-commit checks
pytest --cov=skills --cov-fail-under=80 -m "not slow"

# Full suite with coverage
pytest --cov=skills --cov-report=html

# Specific skill
pytest tests/test_code_analysis.py -v
```

### Add New Test File

```bash
# 1. Create test file
touch tests/test_new_skill.py

# 2. Write tests using template above

# 3. Run new tests
pytest tests/test_new_skill.py -v

# 4. Check coverage
pytest --cov=skills.new_skill tests/test_new_skill.py
```

### Continuous Integration

Tests run automatically on:
- Every commit (if CI configured)
- Pull requests
- Pre-merge checks

Ensure tests pass before committing:
```bash
# Run pre-commit checks
pytest --cov=skills --cov-fail-under=80 -m "not slow" -x
```

---

**Remember:** Good tests are the foundation of reliable software. Write tests that document behavior and catch regressions! 🧪

*Last Updated: 2025-11-08*

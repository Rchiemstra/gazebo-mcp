# Skill Specification: test-orchestrator

**Skill Name:** test-orchestrator
**Priority:** Tier 1 (High-Impact Core)
**Status:** Design Phase
**Estimated Complexity:** Medium-High

---

## Overview

The **test-orchestrator** skill provides intelligent test generation, execution, coverage analysis, and quality recommendations. It automates the tedious parts of testing while teaching best practices.

### Key Capabilities
- Auto-detect testing framework (pytest, jest, go test, cargo test, etc.)
- Generate test scaffolds from source code
- Run tests with smart filtering (changed files, failed tests, etc.)
- Calculate and visualize coverage gaps
- Suggest missing test cases based on code paths
- Generate mocks/stubs automatically
- Support TDD workflows
- Mutation testing for test quality

### Differentiation
Unlike traditional test generators:
- ✅ Context-aware (understands what's already tested)
- ✅ Framework-agnostic (auto-detects and adapts)
- ✅ Multi-language support
- ✅ Generates meaningful tests (not just empty scaffolds)
- ✅ Identifies coverage gaps intelligently
- ✅ Suggests edge cases based on code analysis

---

## When to Use

### Ideal Use Cases
1. **New Feature Testing** - Generate tests for newly implemented features
2. **Coverage Improvement** - Identify and fill coverage gaps
3. **Regression Prevention** - Add tests for bug fixes
4. **Refactoring Safety** - Ensure tests exist before refactoring
5. **TDD Support** - Generate test scaffolds before implementation
6. **Legacy Code** - Add tests to untested legacy code
7. **Test Quality** - Validate test effectiveness with mutation testing

### NOT Suitable For
- ❌ Complex business logic (requires human understanding)
- ❌ UI/UX testing (requires visual validation)
- ❌ Load/performance testing (specialized tools needed)

---

## Workflow

### Mode 1: Test Generation

**1. Analyze Source Code**
```python
# Input: Source file
src/services/payment_service.py

# Analysis:
Skill(code-analysis):
- Parse AST
- Extract functions/methods
- Identify code paths
- Detect edge cases (null checks, error handling, loops)
- Find dependencies (for mocking)

Output:
{
  "file": "src/services/payment_service.py",
  "functions": [
    {
      "name": "process_payment",
      "params": ["amount", "currency", "card_token"],
      "returns": "PaymentResult",
      "raises": ["InvalidAmountError", "PaymentGatewayError"],
      "edge_cases": ["amount <= 0", "invalid currency", "network failure"],
      "dependencies": ["PaymentGateway", "Database"]
    }
  ]
}
```

**2. Check Existing Tests**
```python
# Find existing test file
tests/services/test_payment_service.py

# Analysis:
- Extract existing test cases
- Identify what's already tested
- Find coverage gaps

Output:
{
  "existing_tests": ["test_successful_payment", "test_invalid_amount"],
  "coverage": 45.2,
  "missing_tests": [
    "test_invalid_currency",
    "test_network_failure",
    "test_duplicate_payment"
  ]
}
```

**3. Generate Test Scaffolds**
```python
# Generate missing tests
import pytest
from unittest.mock import Mock, patch
from src.services.payment_service import (
    process_payment,
    InvalidAmountError,
    PaymentGatewayError
)


class TestProcessPayment:
    """Tests for payment processing functionality."""

    @pytest.fixture
    def payment_gateway(self):
        """Mock payment gateway."""
        gateway = Mock()
        gateway.charge.return_value = {"status": "success", "transaction_id": "tx_123"}
        return gateway

    @pytest.fixture
    def database(self):
        """Mock database."""
        db = Mock()
        return db

    def test_successful_payment(self, payment_gateway, database):
        """Test successful payment processing."""
        result = process_payment(
            amount=100.00,
            currency="USD",
            card_token="tok_visa_4242",
            gateway=payment_gateway,
            db=database
        )

        assert result.status == "success"
        assert result.transaction_id == "tx_123"
        payment_gateway.charge.assert_called_once_with(
            amount=100.00,
            currency="USD",
            card_token="tok_visa_4242"
        )
        database.save_transaction.assert_called_once()

    def test_invalid_amount_raises_error(self):
        """Test that invalid amount raises InvalidAmountError."""
        with pytest.raises(InvalidAmountError, match="Amount must be positive"):
            process_payment(amount=-10.00, currency="USD", card_token="tok_visa")

    def test_invalid_currency_raises_error(self):
        """Test that invalid currency code raises error."""
        with pytest.raises(ValueError, match="Unsupported currency"):
            process_payment(amount=100.00, currency="XXX", card_token="tok_visa")

    @patch('src.services.payment_service.PaymentGateway')
    def test_network_failure_handling(self, mock_gateway):
        """Test proper handling of network failures."""
        mock_gateway.charge.side_effect = ConnectionError("Network unavailable")

        with pytest.raises(PaymentGatewayError, match="Payment gateway unavailable"):
            process_payment(amount=100.00, currency="USD", card_token="tok_visa")

    def test_duplicate_payment_prevention(self, payment_gateway, database):
        """Test that duplicate payments are prevented."""
        database.transaction_exists.return_value = True

        result = process_payment(
            amount=100.00,
            currency="USD",
            card_token="tok_visa",
            idempotency_key="key_123",
            gateway=payment_gateway,
            db=database
        )

        assert result.status == "duplicate"
        payment_gateway.charge.assert_not_called()

    @pytest.mark.parametrize("amount,currency,expected", [
        (100.00, "USD", True),
        (50.00, "EUR", True),
        (0.01, "GBP", True),
        (999999.99, "USD", True),
    ])
    def test_various_valid_amounts(self, amount, currency, expected):
        """Test payment processing with various valid amounts."""
        # ... test implementation
```

**4. Suggest Edge Cases**
```
Missing edge cases detected:

1. Boundary Tests:
   - Test with amount = 0.01 (minimum)
   - Test with amount = 999999.99 (maximum)
   - Test with very long card token

2. Error Conditions:
   - Test with null/None parameters
   - Test with malformed currency code
   - Test database save failure

3. Concurrent Operations:
   - Test concurrent payment attempts
   - Test race condition with idempotency

4. Performance:
   - Test with timeout scenario
   - Test with slow gateway response

Add these tests? (y/n)
```

### Mode 2: Test Execution

**1. Smart Test Selection**
```python
# Options:
run_tests(
    mode="changed",        # Only test changed files
    mode="failed",         # Re-run failed tests
    mode="coverage_gaps",  # Run tests for low-coverage areas
    mode="all"             # Run entire suite
)

# Changed files detection:
git diff --name-only HEAD
→ src/services/payment_service.py changed

# Find affected tests:
- tests/services/test_payment_service.py (direct)
- tests/integration/test_checkout_flow.py (indirect)

# Run only affected tests
pytest tests/services/test_payment_service.py tests/integration/test_checkout_flow.py
```

**2. Parallel Execution**
```python
# Detect test parallelization capability
pytest-xdist installed? Yes → Use -n auto
jest? Yes → Use --maxWorkers=auto

# Run in parallel
pytest -n auto --cov=src --cov-report=html
```

**3. Result Analysis**
```
Test Results:
✅ 47 passed
❌ 2 failed
⚠️  3 skipped

Failed Tests:
1. test_network_failure_handling
   Error: AssertionError: Expected PaymentGatewayError but got ConnectionError
   Location: tests/services/test_payment_service.py:78
   Fix suggestion: Add error wrapping in payment_service.py:42

2. test_duplicate_payment_prevention
   Error: Mock was not called
   Location: tests/services/test_payment_service.py:92
   Fix suggestion: Check idempotency logic implementation

Coverage: 67.3% (target: 80%)
Missing coverage:
- src/services/payment_service.py:45-52 (error recovery)
- src/services/payment_service.py:67-71 (logging)
```

### Mode 3: Coverage Analysis

**1. Calculate Coverage**
```python
# Run coverage analysis
coverage run -m pytest
coverage report
coverage html

# Parse results
{
  "overall": 67.3,
  "files": [
    {
      "file": "src/services/payment_service.py",
      "coverage": 72.1,
      "missing_lines": [45-52, 67-71],
      "missing_branches": ["if amount > 1000000"]
    }
  ]
}
```

**2. Visualize Gaps**
```
Coverage Report:

src/services/payment_service.py                72.1%
┌────────────────────────────────────────────────────┐
│ ████████████████████░░░░░░░░░░                     │
│                                                    │
│ Missing Coverage:                                  │
│   Lines 45-52:  Error recovery logic              │
│   Lines 67-71:  Transaction logging               │
│   Branch:       Large amount handling (>1M)       │
└────────────────────────────────────────────────────┘

Recommendations:
1. Add test: test_large_amount_handling()
2. Add test: test_error_recovery_with_retry()
3. Add test: test_transaction_logging()
```

**3. Generate Tests for Gaps**
```python
# Auto-generate tests for uncovered code
def test_error_recovery_with_retry(self, payment_gateway):
    """Test error recovery with automatic retry."""
    # Lines 45-52 test
    payment_gateway.charge.side_effect = [
        ConnectionError("Temporary failure"),
        {"status": "success", "transaction_id": "tx_456"}
    ]

    result = process_payment(
        amount=100.00,
        currency="USD",
        card_token="tok_visa",
        gateway=payment_gateway
    )

    assert result.status == "success"
    assert payment_gateway.charge.call_count == 2  # Retry happened


def test_large_amount_handling(self):
    """Test handling of amounts over 1 million."""
    # Branch coverage test
    result = process_payment(
        amount=1500000.00,
        currency="USD",
        card_token="tok_visa"
    )

    # Should trigger manual review
    assert result.status == "pending_review"
    assert result.review_required is True
```

### Mode 4: Mutation Testing

**1. Generate Mutations**
```python
# Original code
def is_valid_amount(amount):
    return amount > 0

# Mutations:
# 1. Change operator
def is_valid_amount(amount):
    return amount >= 0  # Mutation: > to >=

# 2. Change constant
def is_valid_amount(amount):
    return amount > 1  # Mutation: 0 to 1

# 3. Negate condition
def is_valid_amount(amount):
    return not (amount > 0)  # Mutation: negate

# Run tests against mutations
Mutation 1: ❌ SURVIVED (tests didn't catch this!)
Mutation 2: ✅ KILLED (test caught this)
Mutation 3: ✅ KILLED (test caught this)

# Result: Weak test detected
Test Quality Score: 67% (2/3 mutations killed)

Recommendation: Add test for boundary case (amount = 0)
```

---

## Input/Output Format

### Input
```json
{
  "operation": "generate_tests",
  "target": "src/services/payment_service.py",
  "mode": "comprehensive",
  "options": {
    "framework": "auto_detect",
    "coverage_target": 80,
    "include_edge_cases": true,
    "generate_mocks": true,
    "mutation_testing": false
  }
}
```

### Output
```json
{
  "operation": "generate_tests",
  "status": "completed",
  "analysis": {
    "source_file": "src/services/payment_service.py",
    "functions_analyzed": 5,
    "edge_cases_detected": 12,
    "dependencies": ["PaymentGateway", "Database"]
  },
  "existing_tests": {
    "file": "tests/services/test_payment_service.py",
    "test_count": 8,
    "coverage": 45.2
  },
  "generated_tests": {
    "file": "tests/services/test_payment_service_generated.py",
    "test_count": 15,
    "new_coverage_estimate": 87.3,
    "tests": [
      {
        "name": "test_invalid_currency_raises_error",
        "type": "error_condition",
        "purpose": "Verify error handling for unsupported currencies"
      },
      {
        "name": "test_network_failure_handling",
        "type": "exception_handling",
        "purpose": "Verify resilience to network failures"
      }
    ]
  },
  "recommendations": [
    "Merge generated tests with existing test file",
    "Review edge case tests for business logic accuracy",
    "Consider adding integration tests for payment flow",
    "Run mutation testing to validate test quality"
  ],
  "coverage_improvement": {
    "before": 45.2,
    "after_estimate": 87.3,
    "improvement": 42.1
  }
}
```

---

## Multi-Language Support

### Python (pytest)
```python
# Auto-detect: pytest.ini or conftest.py exists
# Generate:
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def setup_data():
    return {"key": "value"}

def test_example(setup_data):
    assert setup_data["key"] == "value"

@pytest.mark.parametrize("input,expected", [
    (1, 2), (2, 4), (3, 6)
])
def test_parametrized(input, expected):
    assert input * 2 == expected
```

### JavaScript (Jest)
```javascript
// Auto-detect: jest.config.js exists or "jest" in package.json
// Generate:
import { processPayment } from '../services/paymentService';

describe('PaymentService', () => {
  let mockGateway;

  beforeEach(() => {
    mockGateway = {
      charge: jest.fn().mockResolvedValue({ status: 'success' })
    };
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('should process payment successfully', async () => {
    const result = await processPayment(100, 'USD', 'tok_visa', mockGateway);

    expect(result.status).toBe('success');
    expect(mockGateway.charge).toHaveBeenCalledWith(
      expect.objectContaining({ amount: 100, currency: 'USD' })
    );
  });

  it('should throw error for invalid amount', async () => {
    await expect(processPayment(-10, 'USD', 'tok_visa'))
      .rejects.toThrow('Amount must be positive');
  });

  it.each([
    [100, 'USD', true],
    [50, 'EUR', true],
    [-10, 'USD', false],
  ])('should validate amount %d %s correctly', async (amount, currency, valid) => {
    if (valid) {
      await expect(processPayment(amount, currency, 'tok_visa')).resolves.toBeDefined();
    } else {
      await expect(processPayment(amount, currency, 'tok_visa')).rejects.toThrow();
    }
  });
});
```

### Go (testing package)
```go
// Auto-detect: *_test.go files exist
// Generate:
package payment

import (
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/mock"
)

type MockGateway struct {
    mock.Mock
}

func (m *MockGateway) Charge(amount float64, currency string) (Result, error) {
    args := m.Called(amount, currency)
    return args.Get(0).(Result), args.Error(1)
}

func TestProcessPaymentSuccess(t *testing.T) {
    gateway := new(MockGateway)
    gateway.On("Charge", 100.0, "USD").Return(
        Result{Status: "success", TransactionID: "tx_123"},
        nil,
    )

    result, err := ProcessPayment(100.0, "USD", "tok_visa", gateway)

    assert.NoError(t, err)
    assert.Equal(t, "success", result.Status)
    gateway.AssertExpectations(t)
}

func TestProcessPaymentInvalidAmount(t *testing.T) {
    _, err := ProcessPayment(-10.0, "USD", "tok_visa", nil)

    assert.Error(t, err)
    assert.Contains(t, err.Error(), "amount must be positive")
}

func TestProcessPaymentParametrized(t *testing.T) {
    tests := []struct {
        name     string
        amount   float64
        currency string
        wantErr  bool
    }{
        {"valid USD", 100.0, "USD", false},
        {"valid EUR", 50.0, "EUR", false},
        {"invalid negative", -10.0, "USD", true},
        {"invalid zero", 0.0, "USD", true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            _, err := ProcessPayment(tt.amount, tt.currency, "tok_visa", nil)
            if tt.wantErr {
                assert.Error(t, err)
            } else {
                assert.NoError(t, err)
            }
        })
    }
}
```

### Rust (cargo test)
```rust
// Auto-detect: Cargo.toml exists
// Generate:
#[cfg(test)]
mod tests {
    use super::*;
    use mockall::predicate::*;
    use mockall::mock;

    mock! {
        Gateway {}
        impl PaymentGateway for Gateway {
            fn charge(&self, amount: f64, currency: &str) -> Result<PaymentResult>;
        }
    }

    #[test]
    fn test_process_payment_success() {
        let mut mock_gateway = MockGateway::new();
        mock_gateway
            .expect_charge()
            .with(eq(100.0), eq("USD"))
            .times(1)
            .returning(|_, _| Ok(PaymentResult {
                status: "success".to_string(),
                transaction_id: "tx_123".to_string(),
            }));

        let result = process_payment(100.0, "USD", "tok_visa", &mock_gateway);

        assert!(result.is_ok());
        assert_eq!(result.unwrap().status, "success");
    }

    #[test]
    #[should_panic(expected = "amount must be positive")]
    fn test_process_payment_invalid_amount() {
        process_payment(-10.0, "USD", "tok_visa", &MockGateway::new()).unwrap();
    }

    #[test]
    fn test_process_payment_network_failure() {
        let mut mock_gateway = MockGateway::new();
        mock_gateway
            .expect_charge()
            .returning(|_, _| Err(PaymentError::NetworkError));

        let result = process_payment(100.0, "USD", "tok_visa", &mock_gateway);

        assert!(result.is_err());
        assert!(matches!(result.unwrap_err(), PaymentError::NetworkError));
    }

    #[parameterized(
        amount = { 100.0, 50.0, 0.01 },
        currency = { "USD", "EUR", "GBP" }
    )]
    fn test_valid_amounts(amount: f64, currency: &str) {
        let result = validate_payment(amount, currency);
        assert!(result.is_ok());
    }
}
```

---

## Framework Detection

```python
def detect_testing_framework(project_path: str) -> TestFramework:
    """Auto-detect testing framework."""

    # Python
    if exists("pytest.ini") or exists("conftest.py"):
        return TestFramework.PYTEST
    if exists("setup.py") and contains("unittest"):
        return TestFramework.UNITTEST

    # JavaScript/TypeScript
    if exists("jest.config.js") or package_json_has("jest"):
        return TestFramework.JEST
    if exists("vitest.config.ts") or package_json_has("vitest"):
        return TestFramework.VITEST
    if exists("karma.conf.js"):
        return TestFramework.KARMA

    # Go
    if exists("go.mod"):
        return TestFramework.GO_TEST

    # Rust
    if exists("Cargo.toml"):
        return TestFramework.CARGO_TEST

    # Java
    if contains_dependency("junit"):
        return TestFramework.JUNIT
    if contains_dependency("testng"):
        return TestFramework.TESTNG

    # Default
    return TestFramework.UNKNOWN
```

---

## Integration with Other Skills

### With code-analysis
```python
# Use code-analysis to understand code structure
analysis = code_analysis.analyze_file("src/services/payment_service.py")

# Generate tests based on analysis
for function in analysis.functions:
    tests = generate_tests_for_function(
        function=function,
        complexity=function.complexity,
        dependencies=function.dependencies
    )
```

### With spec-to-implementation
```python
# spec-to-implementation calls test-orchestrator
# to generate tests for newly implemented features
spec_to_impl.implement_feature("user authentication")
→ calls test_orchestrator.generate_tests("src/auth/")
→ returns comprehensive test suite
```

### With refactor-assistant
```python
# Before refactoring, ensure tests exist
refactor_assistant.extract_method("process_payment", "validate_amount")
→ calls test_orchestrator.ensure_coverage("process_payment")
→ if coverage < threshold: generate missing tests
→ proceed with refactoring
```

---

## Performance

### Targets
- **Test Generation:** < 5 seconds per file
- **Test Execution:** Parallel by default
- **Coverage Analysis:** < 10 seconds for typical project
- **Mutation Testing:** < 2 minutes for single file

### Optimizations
1. **Caching:** Cache AST analysis between runs
2. **Parallel Execution:** Use all CPU cores
3. **Incremental Analysis:** Only analyze changed files
4. **Smart Selection:** Run only affected tests

---

## Success Metrics

- **Coverage Improvement:** +30% average coverage increase
- **Test Generation Time:** 80% faster than manual
- **Test Quality:** 90%+ mutation score
- **Developer Adoption:** Used in 70%+ of PRs

---

**Status:** Ready for implementation
**Dependencies:** code-analysis skill
**Next Steps:** Implement Python/pytest MVP

# Skill Specification: refactor-assistant

**Skill Name:** refactor-assistant
**Priority:** Tier 1 (High-Impact Core)
**Status:** Design Phase
**Estimated Complexity:** High

---

## Overview

The **refactor-assistant** skill provides safe, intelligent code refactoring with impact analysis and automated safety checks. It transforms risky manual refactoring into confident, automated improvements.

### Key Capabilities
- Extract method/function with automated parameter detection
- Rename symbols with dependency tracking across files
- Remove dead code detection and safe removal
- Simplify complex conditionals and logic
- Impact analysis before refactoring (what will break)
- Automated test verification (preserve behavior)
- Multi-language support (Python, JS/TS, Go, Rust)
- Rollback support with git integration

### Differentiation
Unlike IDE refactoring tools:
- ✅ **Cross-file impact analysis** - Shows all affected files
- ✅ **Test verification** - Ensures behavior preservation
- ✅ **AI-powered suggestions** - Identifies refactoring opportunities
- ✅ **Safety guarantees** - Pre-flight checks before changes
- ✅ **Dead code detection** - Finds unused code safely
- ✅ **Complexity reduction** - Simplifies logic automatically

---

## When to Use

### Ideal Use Cases
1. **Extract Method** - Long functions → smaller, testable functions
2. **Rename Refactoring** - Safe renaming across entire codebase
3. **Remove Dead Code** - Identify and remove unused code
4. **Simplify Logic** - Complex conditionals → readable code
5. **Inline Variables** - Single-use variables → direct usage
6. **Move Method** - Reorganize code between classes/modules
7. **Replace Magic Numbers** - Numbers → named constants
8. **Dependency Inversion** - Reduce coupling between components

### NOT Suitable For
- ❌ Architectural redesign (too large scope)
- ❌ Algorithm changes (behavior modification)
- ❌ Database schema refactoring (needs migration)

---

## Refactoring Operations

### 1. Extract Method/Function

**Purpose:** Break down long functions into smaller, focused units

**Before:**
```python
def process_order(order_data):
    # Validation (20 lines)
    if not order_data:
        raise ValueError("Order data required")
    if not order_data.get("customer_id"):
        raise ValueError("Customer ID required")
    if not order_data.get("items"):
        raise ValueError("Items required")
    # ... more validation

    # Payment processing (30 lines)
    payment_method = order_data.get("payment_method")
    if payment_method == "credit_card":
        card_token = order_data.get("card_token")
        result = gateway.charge(card_token, order_data["total"])
        # ... card processing logic
    elif payment_method == "paypal":
        # ... PayPal logic
    # ... more payment logic

    # Inventory update (25 lines)
    for item in order_data["items"]:
        product = db.get_product(item["product_id"])
        if product.stock < item["quantity"]:
            raise InsufficientStockError()
        product.stock -= item["quantity"]
        db.save(product)
    # ... more inventory logic

    # Order creation (15 lines)
    # ... order creation logic

    return order
```

**Refactored:**
```python
def process_order(order_data):
    """Process customer order through validation, payment, and fulfillment."""
    validate_order_data(order_data)
    payment_result = process_payment(order_data)
    update_inventory(order_data["items"])
    order = create_order_record(order_data, payment_result)
    return order


def validate_order_data(order_data: dict) -> None:
    """Validate order data completeness and correctness."""
    if not order_data:
        raise ValueError("Order data required")
    if not order_data.get("customer_id"):
        raise ValueError("Customer ID required")
    if not order_data.get("items"):
        raise ValueError("Items required")
    # ... validation logic


def process_payment(order_data: dict) -> PaymentResult:
    """Process payment through appropriate gateway."""
    payment_method = order_data.get("payment_method")
    if payment_method == "credit_card":
        return process_credit_card_payment(order_data)
    elif payment_method == "paypal":
        return process_paypal_payment(order_data)
    raise ValueError(f"Unsupported payment method: {payment_method}")


def update_inventory(items: list) -> None:
    """Update product inventory for ordered items."""
    for item in items:
        product = db.get_product(item["product_id"])
        if product.stock < item["quantity"]:
            raise InsufficientStockError(
                f"Insufficient stock for {product.name}"
            )
        product.stock -= item["quantity"]
        db.save(product)


def create_order_record(order_data: dict, payment_result: PaymentResult) -> Order:
    """Create order record in database."""
    # ... order creation logic
    return order
```

**Analysis Output:**
```json
{
  "operation": "extract_method",
  "source_function": "process_order",
  "complexity_before": 28,
  "complexity_after": 6,
  "extracted_functions": [
    {
      "name": "validate_order_data",
      "lines": 8,
      "complexity": 4,
      "parameters": ["order_data"],
      "returns": "None"
    },
    {
      "name": "process_payment",
      "lines": 12,
      "complexity": 5,
      "parameters": ["order_data"],
      "returns": "PaymentResult"
    },
    {
      "name": "update_inventory",
      "lines": 10,
      "complexity": 3,
      "parameters": ["items"],
      "returns": "None"
    },
    {
      "name": "create_order_record",
      "lines": 8,
      "complexity": 2,
      "parameters": ["order_data", "payment_result"],
      "returns": "Order"
    }
  ],
  "improvement": {
    "complexity_reduction": 79,
    "lines_per_function_before": 90,
    "lines_per_function_after": 15,
    "testability": "significantly_improved"
  }
}
```

### 2. Rename Symbol (Safe Cross-File)

**Purpose:** Rename variables, functions, classes across entire codebase

**Workflow:**
```
1. Find all usages:
   Skill(code-analysis): Find all references to symbol
   → 47 usages found across 12 files

2. Impact analysis:
   Files affected:
   - src/services/payment.py (23 usages)
   - src/api/checkout.py (8 usages)
   - tests/test_payment.py (16 usages)
   - ... 9 more files

3. Check external dependencies:
   Public API? Yes
   → WARNING: This function is exposed in public API
   → Breaking change! Consider deprecation instead

4. Generate preview:
   Show diff for all affected files

5. Safety checks:
   ✅ All usages found
   ✅ No dynamic string usage detected
   ✅ Tests exist for this function
   ⚠️  Public API - breaking change

6. Execute rename:
   Rename: process_payment → process_customer_payment
   Files modified: 12
   Lines changed: 47

7. Verify:
   Run tests: ✅ All tests passing
   Lint checks: ✅ No issues
```

**Example:**
```python
# Before
def calc(x, y):  # Poorly named
    return x * y + tax_rate

# Usage across codebase
total = calc(price, quantity)
cost = calc(item.price, item.qty)

# After renaming
def calculate_total_with_tax(price, quantity):
    return price * quantity + tax_rate

# All usages updated automatically
total = calculate_total_with_tax(price, quantity)
cost = calculate_total_with_tax(item.price, item.qty)
```

### 3. Remove Dead Code

**Purpose:** Safely identify and remove unused code

**Detection:**
```python
# Analyze codebase
Skill(code-analysis): Build call graph

Dead code detected:

1. Unused Functions (7):
   - src/utils/old_payment.py::process_legacy_payment
     Last used: Never (created 2 years ago)
     Safe to remove: ✅ No references

   - src/helpers/deprecated.py::convert_currency_old
     Last used: 6 months ago (removed from main.py)
     Safe to remove: ✅ No references

2. Unused Imports (23):
   - src/api/checkout.py: import json (unused)
   - src/services/payment.py: from typing import Optional (unused)

3. Unused Variables (15):
   - src/services/order.py:42: temp_data (assigned but never read)

4. Unreachable Code (3):
   - src/validators/schema.py:78-82 (after return statement)

5. Commented Code (45 blocks):
   - src/legacy/ contains 12 files of commented code
     Last modified: 18 months ago
     Safe to remove: ⚠️  Needs review

Total lines that can be removed: 1,247
```

**Safety Analysis:**
```json
{
  "analysis": {
    "total_dead_code_lines": 1247,
    "confidence_levels": {
      "safe_to_remove": 892,
      "probably_safe": 234,
      "needs_review": 121
    }
  },
  "categorized_removal": {
    "unused_functions": {
      "count": 7,
      "lines": 342,
      "safety": "safe",
      "reasoning": "No callers found in static analysis"
    },
    "unused_imports": {
      "count": 23,
      "lines": 23,
      "safety": "safe",
      "reasoning": "Import not referenced in file"
    },
    "unreachable_code": {
      "count": 3,
      "lines": 18,
      "safety": "safe",
      "reasoning": "Code after return/break/continue"
    },
    "commented_code": {
      "count": 45,
      "lines": 864,
      "safety": "needs_review",
      "reasoning": "Cannot determine if needed for reference"
    }
  },
  "recommendations": [
    "Remove unused functions and imports immediately (892 lines)",
    "Review commented code blocks before removal",
    "Create git branch for easy rollback if needed"
  ]
}
```

### 4. Simplify Complex Conditionals

**Purpose:** Make complex logic more readable

**Before:**
```python
def calculate_discount(customer, order):
    if customer.vip_status == True and (order.total > 1000 or (order.total > 500 and customer.purchase_count > 10)) or (customer.vip_status == False and order.total > 2000 and customer.purchase_count > 20):
        if customer.referral_source == "partner" or customer.referral_source == "affiliate":
            discount = 0.20
        else:
            if order.total > 5000:
                discount = 0.15
            else:
                discount = 0.10
    else:
        discount = 0.0
    return discount
```

**Complexity Analysis:**
```json
{
  "complexity": 12,
  "nesting_depth": 4,
  "condition_count": 11,
  "readability_score": 23,
  "issues": [
    "Deeply nested conditions (4 levels)",
    "Complex boolean expressions",
    "Magic numbers (1000, 500, 20, etc.)",
    "Repeated logic patterns"
  ]
}
```

**After:**
```python
# Extract constants
LARGE_ORDER_THRESHOLD = 1000
MEDIUM_ORDER_THRESHOLD = 500
HUGE_ORDER_THRESHOLD = 5000
VIP_PURCHASE_REQUIREMENT = 10
REGULAR_PURCHASE_REQUIREMENT = 20

PARTNER_DISCOUNT = 0.20
LARGE_ORDER_DISCOUNT = 0.15
STANDARD_DISCOUNT = 0.10
NO_DISCOUNT = 0.0


def calculate_discount(customer, order):
    """Calculate order discount based on customer status and order value."""
    if not qualifies_for_discount(customer, order):
        return NO_DISCOUNT

    if is_partner_referral(customer):
        return PARTNER_DISCOUNT

    if order.total > HUGE_ORDER_THRESHOLD:
        return LARGE_ORDER_DISCOUNT

    return STANDARD_DISCOUNT


def qualifies_for_discount(customer, order):
    """Check if customer qualifies for any discount."""
    if customer.vip_status:
        return qualifies_as_vip(customer, order)
    return qualifies_as_regular(customer, order)


def qualifies_as_vip(customer, order):
    """Check VIP discount qualification."""
    return (
        order.total > LARGE_ORDER_THRESHOLD or
        (order.total > MEDIUM_ORDER_THRESHOLD and
         customer.purchase_count > VIP_PURCHASE_REQUIREMENT)
    )


def qualifies_as_regular(customer, order):
    """Check regular customer discount qualification."""
    return (
        order.total > 2000 and
        customer.purchase_count > REGULAR_PURCHASE_REQUIREMENT
    )


def is_partner_referral(customer):
    """Check if customer came from partner/affiliate."""
    return customer.referral_source in ["partner", "affiliate"]
```

**Improvement:**
```json
{
  "complexity_before": 12,
  "complexity_after": 3,
  "nesting_before": 4,
  "nesting_after": 2,
  "readability_improvement": 85,
  "benefits": [
    "Named constants replace magic numbers",
    "Complex conditions broken into named functions",
    "Each function has single responsibility",
    "Much easier to test individually",
    "Business logic is self-documenting"
  ]
}
```

### 5. Inline Variable

**Purpose:** Remove unnecessary intermediate variables

**Before:**
```python
def calculate_total(items):
    subtotal = sum(item.price for item in items)
    tax_amount = subtotal * 0.08
    shipping_cost = 10.00
    total_amount = subtotal + tax_amount + shipping_cost
    return total_amount
```

**After:**
```python
def calculate_total(items):
    subtotal = sum(item.price for item in items)
    return subtotal + (subtotal * 0.08) + 10.00
```

**Or better yet:**
```python
TAX_RATE = 0.08
STANDARD_SHIPPING = 10.00

def calculate_total(items):
    subtotal = sum(item.price for item in items)
    return subtotal * (1 + TAX_RATE) + STANDARD_SHIPPING
```

### 6. Replace Magic Numbers

**Purpose:** Convert hardcoded values to named constants

**Before:**
```python
def is_eligible_for_promotion(customer):
    if customer.age >= 18 and customer.age <= 65:
        if customer.purchase_count > 5:
            if customer.lifetime_value > 1000:
                return True
    return False
```

**After:**
```python
MIN_PROMOTION_AGE = 18
MAX_PROMOTION_AGE = 65
REQUIRED_PURCHASES = 5
MINIMUM_LIFETIME_VALUE = 1000


def is_eligible_for_promotion(customer):
    """Check if customer qualifies for promotional offers."""
    return (
        is_promotion_age(customer.age) and
        customer.purchase_count > REQUIRED_PURCHASES and
        customer.lifetime_value > MINIMUM_LIFETIME_VALUE
    )


def is_promotion_age(age):
    """Check if age is within promotion eligibility range."""
    return MIN_PROMOTION_AGE <= age <= MAX_PROMOTION_AGE
```

---

## Safety Mechanisms

### Pre-Flight Checks

**Before ANY refactoring:**
```python
def pre_flight_check(refactoring_plan):
    """Comprehensive safety check before refactoring."""

    checks = {
        "git_status": check_git_clean(),
        "tests_exist": check_tests_exist(),
        "tests_passing": run_tests(),
        "no_uncommitted": check_no_uncommitted_changes(),
        "impact_analysis": analyze_impact(),
        "backup_created": create_backup()
    }

    if not all(checks.values()):
        return RefactoringStatus.BLOCKED, checks

    return RefactoringStatus.SAFE_TO_PROCEED, checks
```

**Check Details:**
```json
{
  "pre_flight_checks": {
    "git_status": {
      "status": "✅ clean",
      "message": "Working directory clean"
    },
    "tests_exist": {
      "status": "✅ passed",
      "message": "47 tests found for affected code"
    },
    "tests_passing": {
      "status": "✅ passed",
      "message": "All 47 tests passing"
    },
    "impact_analysis": {
      "status": "⚠️ warning",
      "message": "12 files will be modified",
      "files": ["src/payment.py", "src/checkout.py", "..."],
      "estimated_changes": 234
    },
    "backup_created": {
      "status": "✅ created",
      "message": "Branch 'backup/refactor-payment' created"
    }
  },
  "recommendation": "SAFE_TO_PROCEED_WITH_CAUTION"
}
```

### Post-Refactoring Verification

**After refactoring:**
```python
def verify_refactoring(original_state, refactored_state):
    """Verify refactoring preserved behavior."""

    verifications = {
        "tests_still_pass": run_tests(),
        "no_new_warnings": check_linter(),
        "no_type_errors": check_type_hints(),
        "coverage_maintained": check_coverage(),
        "performance_maintained": check_performance()
    }

    if not all(verifications.values()):
        rollback_refactoring(original_state)
        return RefactoringStatus.FAILED, verifications

    return RefactoringStatus.SUCCESS, verifications
```

### Automatic Rollback

**If anything fails:**
```python
def rollback_refactoring(backup_branch):
    """Automatic rollback on failure."""
    git checkout {backup_branch}
    git branch -D refactor/in-progress
    return "Refactoring rolled back successfully"
```

---

## Input/Output Format

### Input
```json
{
  "operation": "extract_method",
  "file": "src/services/order_processor.py",
  "function": "process_order",
  "extract_lines": [15, 45],
  "new_function_name": "process_payment",
  "options": {
    "run_tests_after": true,
    "auto_rollback_on_failure": true,
    "create_backup": true
  }
}
```

### Output
```json
{
  "operation": "extract_method",
  "status": "success",
  "pre_flight_checks": {
    "all_passed": true,
    "details": { "..." }
  },
  "refactoring": {
    "files_modified": 1,
    "lines_added": 32,
    "lines_removed": 30,
    "functions_created": 1,
    "complexity_before": 28,
    "complexity_after": 8
  },
  "verification": {
    "tests_run": 47,
    "tests_passed": 47,
    "tests_failed": 0,
    "coverage_before": 78.3,
    "coverage_after": 82.1,
    "linter_issues": 0
  },
  "improvement_metrics": {
    "complexity_reduction": 71,
    "readability_improvement": 65,
    "testability": "significantly_improved"
  },
  "backup": {
    "branch": "backup/refactor-order-processor",
    "commit": "a7f3d92"
  }
}
```

---

## Integration with Other Skills

### With test-orchestrator
```python
# Before refactoring
refactor_assistant.extract_method("process_order", lines=[15, 45])
→ test_orchestrator.ensure_coverage("process_order") # ✅ 85% coverage
→ proceed with refactoring
→ test_orchestrator.run_tests() # ✅ All passing
```

### With code-analysis
```python
# Find refactoring opportunities
code_analysis.detect_code_smells("src/")
→ [
    {"type": "long_function", "location": "order_processor.py:process_order"},
    {"type": "complex_conditional", "location": "discount.py:calculate_discount"}
  ]
→ refactor_assistant.suggest_refactorings(smells)
```

### With pr-review-assistant
```python
# After refactoring
refactor_assistant.simplify_conditionals("discount.py")
→ pr_review_assistant.create_pr(
    title="Refactor: Simplify discount calculation logic",
    changes=refactoring_result
  )
```

---

## Success Metrics

- **Safety Rate:** 99%+ successful refactorings without breaking tests
- **Complexity Reduction:** 40-70% average reduction
- **Time Savings:** 85% faster than manual refactoring
- **Confidence:** Developers trust automated refactoring

---

**Status:** Ready for implementation
**Dependencies:** code-analysis, test-orchestrator
**Next Steps:** Implement extract method (MVP)

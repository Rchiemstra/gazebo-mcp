# Skill Specification: pr-review-assistant

**Skill Name:** pr-review-assistant
**Priority:** Tier 1 (High-Impact Core)
**Status:** Design Phase
**Estimated Complexity:** Medium-High

---

## Overview

The **pr-review-assistant** skill provides automated code review, PR description generation, quality checks, and review comment drafting. It makes code reviews faster, more consistent, and more thorough.

### Key Capabilities
- Generate comprehensive PR descriptions from git diff
- Code quality checklist verification
- Breaking change detection
- Test coverage requirements validation
- Documentation update checks
- Security pattern scanning
- Review comment drafting with suggestions
- PR size/complexity analysis
- Automated reviewer suggestions
- Merge conflict detection

### Differentiation
Unlike basic PR tools:
- ✅ **AI-powered analysis** - Understands code context
- ✅ **Comprehensive checks** - 20+ quality checks
- ✅ **Actionable feedback** - Specific suggestions, not just warnings
- ✅ **Learning system** - Improves from accepted reviews
- ✅ **Multi-language** - Works across tech stack
- ✅ **Team standards** - Enforces project conventions

---

## When to Use

### Ideal Use Cases
1. **PR Creation** - Generate description and checklist
2. **Self-Review** - Review own code before submission
3. **Team Review** - Automated first-pass review
4. **Quality Gates** - Block merges that don't meet standards
5. **Review Comments** - Draft constructive feedback
6. **Breaking Changes** - Detect API/interface changes
7. **Documentation** - Ensure docs are updated
8. **Security** - Catch common security issues

### NOT Suitable For
- ❌ Business logic validation (requires domain knowledge)
- ❌ UI/UX review (requires visual inspection)
- ❌ Complex architectural decisions

---

## Core Operations

### 1. PR Description Generation

**Input:** Git diff
**Output:** Comprehensive PR description

**Example:**

**Git diff:**
```diff
diff --git a/src/services/payment.py b/src/services/payment.py
+ def process_refund(transaction_id, amount):
+     """Process refund for a transaction."""
+     transaction = db.get_transaction(transaction_id)
+     if not transaction:
+         raise TransactionNotFoundError()
+
+     if amount > transaction.amount:
+         raise InvalidRefundAmountError()
+
+     refund_result = gateway.refund(transaction.gateway_id, amount)
+     db.create_refund_record(transaction_id, amount, refund_result)
+     return refund_result

diff --git a/tests/test_payment.py b/tests/test_payment.py
+ def test_process_refund_success():
+     result = process_refund("tx_123", 50.00)
+     assert result.status == "success"
+
+ def test_process_refund_invalid_amount():
+     with pytest.raises(InvalidRefundAmountError):
+         process_refund("tx_123", 999.00)
```

**Generated PR Description:**
````markdown
## Summary

Adds refund processing capability to the payment service, enabling customers to receive refunds for completed transactions.

## Changes

### New Features
- ✨ **Refund Processing** (`src/services/payment.py`)
  - Added `process_refund()` function to handle transaction refunds
  - Validates refund amount doesn't exceed original transaction
  - Integrates with payment gateway for actual refund processing
  - Creates refund record in database for tracking

### Tests Added
- ✅ `test_process_refund_success()` - Happy path test
- ✅ `test_process_refund_invalid_amount()` - Error handling test

## Impact Analysis

### Files Changed
- `src/services/payment.py` (+15 lines)
- `tests/test_payment.py` (+8 lines)

### Breaking Changes
None detected ✅

### API Changes
**New public function:**
```python
def process_refund(transaction_id: str, amount: float) -> RefundResult
```

### Dependencies
No new dependencies added ✅

### Database Changes
None (assumes `refund_records` table already exists)

### Security Considerations
- ✅ Validates transaction exists before refund
- ✅ Validates refund amount doesn't exceed transaction
- ⚠️  Consider adding: Rate limiting for refund requests
- ⚠️  Consider adding: Audit logging for refund operations

## Testing

### Test Coverage
- Lines covered: 15/15 (100%)
- Branches covered: 4/4 (100%)

### Test Types
- ✅ Unit tests added
- ⚠️  Integration tests missing
- ⚠️  E2E tests missing

### Manual Testing Checklist
- [ ] Test refund with partial amount
- [ ] Test refund with full amount
- [ ] Test refund for already-refunded transaction
- [ ] Test refund for cancelled transaction
- [ ] Test refund with invalid transaction ID
- [ ] Test concurrent refund requests

## Documentation

- ⚠️  API documentation needs updating (`docs/API.md`)
- ⚠️  User guide should mention refund feature
- ⚠️  Changelog needs entry

## Deployment Notes

- No special deployment steps required
- No environment variable changes
- No database migration needed (assumes schema exists)

## Rollback Plan

If issues arise:
1. Revert this commit
2. No data migration needed
3. Existing transactions unaffected

## Checklist

- [x] Code follows project style guidelines
- [x] Self-review completed
- [x] Unit tests added and passing
- [ ] Integration tests added
- [ ] Documentation updated
- [x] No breaking changes
- [ ] Security review completed
- [ ] Performance impact assessed

## Related Issues

Closes #456 - Add refund processing
Related to #234 - Payment gateway integration

## Reviewers

**Suggested reviewers:**
- @payment-team-lead (domain expertise)
- @security-lead (security validation)
- @backend-dev (code review)

**Estimated review time:** 15-20 minutes

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
````

### 2. Code Quality Checks

**Comprehensive quality analysis:**

```
Code Quality Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overall Score: 78/100 (GOOD)

PASSED CHECKS (18)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Code style consistent with project
✅ No linting errors
✅ Type hints present
✅ Docstrings added for new functions
✅ No hardcoded credentials detected
✅ No SQL injection vulnerabilities
✅ Error handling present
✅ Tests added for new code
✅ Test coverage > 80% (100%)
✅ No duplicate code detected
✅ Function complexity acceptable (<10)
✅ No magic numbers (constants used)
✅ No TODO/FIXME comments left
✅ Git commit message follows convention
✅ File size acceptable (<500 lines)
✅ No console.log/print statements left
✅ No commented-out code
✅ Proper variable naming

WARNINGS (4)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  Integration tests missing
   Impact: Medium
   Recommendation: Add tests for gateway interaction
   Location: tests/integration/test_payment_gateway.py

⚠️  API documentation not updated
   Impact: Medium
   Recommendation: Add refund endpoint to docs/API.md
   Location: docs/API.md

⚠️  No rate limiting on refund requests
   Impact: Low-Medium
   Recommendation: Add rate limiting to prevent abuse
   Location: src/services/payment.py:process_refund

⚠️  Audit logging not implemented
   Impact: Low-Medium
   Recommendation: Log refund operations for compliance
   Location: src/services/payment.py:process_refund

FAILED CHECKS (0)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
None ✅

SUGGESTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Consider adding idempotency key to prevent duplicate refunds
💡 Consider adding webhook notification for successful refunds
💡 Consider supporting partial refunds for line items

SECURITY ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ No critical security issues
✅ Input validation present
✅ Error messages don't leak sensitive info
⚠️  Consider adding refund request rate limiting
⚠️  Consider adding fraud detection for large refunds

PERFORMANCE ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ No obvious performance issues
✅ Database queries optimized
💡 Consider caching transaction lookups

COMPLEXITY METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Cyclomatic Complexity: 4 (Good - target <10)
Lines of Code: 15 (Good - target <50)
Nesting Depth: 2 (Good - target <4)

PR SIZE ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Size: SMALL ✅
Files changed: 2
Lines added: 23
Lines removed: 0
Estimated review time: 15 minutes

Recommendation: Good PR size for thorough review
```

### 3. Breaking Change Detection

**Automated breaking change analysis:**

```
Breaking Change Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Status: ⚠️  BREAKING CHANGES DETECTED (2)

BREAKING CHANGE #1: Function Signature Modified
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
File: src/api/checkout.py
Function: process_checkout()

Before:
```python
def process_checkout(user_id, items):
    ...
```

After:
```python
def process_checkout(user_id, items, payment_method):
    ...
```

Impact: HIGH
- New required parameter added: `payment_method`
- All existing callers will break
- 12 call sites found in codebase

Affected files:
- src/api/routes/checkout.py (3 calls)
- src/services/order_service.py (5 calls)
- tests/test_checkout.py (4 calls)

Recommended fix:
```python
# Option 1: Make parameter optional (backward compatible)
def process_checkout(user_id, items, payment_method=None):
    if payment_method is None:
        payment_method = get_default_payment_method(user_id)
    ...

# Option 2: Create new function (deprecation path)
def process_checkout_v2(user_id, items, payment_method):
    ...

def process_checkout(user_id, items):  # Deprecated
    warnings.warn("Use process_checkout_v2", DeprecationWarning)
    return process_checkout_v2(user_id, items, None)
```

BREAKING CHANGE #2: Return Type Changed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
File: src/services/payment.py
Function: charge_card()

Before:
```python
def charge_card(amount, token) -> bool:
    # Returns True/False
    ...
```

After:
```python
def charge_card(amount, token) -> PaymentResult:
    # Returns PaymentResult object
    ...
```

Impact: MEDIUM
- Return type changed from bool to PaymentResult
- Callers expecting boolean will break
- 8 call sites found

Affected files:
- src/api/payment_routes.py (3 calls)
- src/services/subscription.py (5 calls)

Recommended fix:
```python
# Update all callers:
# Before:
if charge_card(amount, token):
    success_handler()

# After:
result = charge_card(amount, token)
if result.success:
    success_handler()
```

SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Breaking changes: 2
Files requiring updates: 7
Total call sites: 20

Recommended Actions:
1. Add deprecation warnings for old interfaces
2. Provide migration guide in PR description
3. Update all affected call sites in this PR
4. Consider versioning (v2 functions)
5. Update changelog with BREAKING CHANGE section

Migration Guide Template:
```markdown
## Breaking Changes

### 1. process_checkout() signature changed
**Old:**
```python
process_checkout(user_id, items)
```

**New:**
```python
process_checkout(user_id, items, payment_method="card")
```

**Migration:**
Add payment_method parameter to all calls.

### 2. charge_card() return type changed
**Old:**
Returns `bool`

**New:**
Returns `PaymentResult` object

**Migration:**
```python
# Before
if charge_card(amount, token):
    ...

# After
result = charge_card(amount, token)
if result.success:
    ...
```
```
```

### 4. Review Comment Drafting

**AI-generated review comments:**

```
Review Comments (Draft)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Generated 7 review comments

CRITICAL (0)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
None ✅

HIGH PRIORITY (2)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 src/services/payment.py:45
```python
def process_refund(transaction_id, amount):
    transaction = db.get_transaction(transaction_id)
```

⚠️  **Potential Race Condition**

Multiple concurrent refund requests for the same transaction could result in over-refunding.

**Suggestion:**
Use database-level locking to prevent concurrent refund processing:

```python
def process_refund(transaction_id, amount):
    with db.transaction():
        transaction = db.get_transaction(
            transaction_id,
            for_update=True  # Row-level lock
        )

        # Check if already fully refunded
        total_refunded = db.get_total_refunded(transaction_id)
        if total_refunded + amount > transaction.amount:
            raise InvalidRefundAmountError("Exceeds available refund amount")

        # Process refund
        ...
```

**Alternatively**, add idempotency key:
```python
def process_refund(transaction_id, amount, idempotency_key):
    # Check if already processed with this key
    existing = db.get_refund_by_idempotency_key(idempotency_key)
    if existing:
        return existing  # Return cached result
    ...
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 src/services/payment.py:52
```python
refund_result = gateway.refund(transaction.gateway_id, amount)
```

⚠️  **Missing Error Handling**

Gateway refund call could fail due to network issues, timeout, or gateway errors. This could leave the system in an inconsistent state.

**Suggestion:**
Add comprehensive error handling and retry logic:

```python
try:
    refund_result = gateway.refund(
        transaction.gateway_id,
        amount,
        timeout=30  # 30 second timeout
    )
except GatewayTimeoutError:
    # Gateway call timed out - status unknown
    # Create pending refund record for manual investigation
    db.create_pending_refund(transaction_id, amount)
    raise RefundPendingError(
        "Refund submitted but confirmation pending. "
        "Check status with gateway."
    )
except GatewayError as e:
    # Gateway rejected refund
    logger.error(f"Refund failed: {e}")
    raise RefundFailedError(f"Gateway error: {e.message}")
except Exception as e:
    # Unexpected error
    logger.exception("Unexpected refund error")
    raise
```

MEDIUM PRIORITY (3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 src/services/payment.py:40
```python
def process_refund(transaction_id, amount):
```

💡 **Missing Type Hints**

While docstring is present, type hints would improve IDE support and catch type errors earlier.

**Suggestion:**
```python
def process_refund(
    transaction_id: str,
    amount: Decimal,
    reason: Optional[str] = None
) -> RefundResult:
    """Process refund for a transaction.

    Args:
        transaction_id: ID of transaction to refund
        amount: Amount to refund (must be <= transaction amount)
        reason: Optional reason for refund

    Returns:
        RefundResult with status and refund ID

    Raises:
        TransactionNotFoundError: Transaction doesn't exist
        InvalidRefundAmountError: Amount exceeds transaction
        RefundFailedError: Gateway rejected refund
    """
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 tests/test_payment.py:67
```python
def test_process_refund_success():
    result = process_refund("tx_123", 50.00)
    assert result.status == "success"
```

💡 **Test Could Be More Comprehensive**

Test only checks happy path and doesn't verify all side effects.

**Suggestion:**
```python
def test_process_refund_success(mock_gateway, mock_db):
    # Arrange
    transaction = Transaction(id="tx_123", amount=100.00)
    mock_db.get_transaction.return_value = transaction
    mock_gateway.refund.return_value = RefundResult(
        status="success",
        refund_id="ref_456"
    )

    # Act
    result = process_refund("tx_123", 50.00)

    # Assert
    assert result.status == "success"
    assert result.refund_id == "ref_456"

    # Verify gateway was called correctly
    mock_gateway.refund.assert_called_once_with(
        transaction.gateway_id,
        50.00
    )

    # Verify refund record was created
    mock_db.create_refund_record.assert_called_once_with(
        "tx_123",
        50.00,
        result
    )
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 src/services/payment.py (general)

💡 **Consider Adding Audit Logging**

For compliance and debugging, refund operations should be logged.

**Suggestion:**
```python
def process_refund(transaction_id, amount):
    logger.info(
        "Processing refund",
        extra={
            "transaction_id": transaction_id,
            "amount": amount,
            "user_id": get_current_user_id(),
            "timestamp": datetime.utcnow()
        }
    )

    try:
        # ... refund logic ...

        logger.info(
            "Refund successful",
            extra={
                "transaction_id": transaction_id,
                "refund_id": refund_result.id
            }
        )
        return refund_result
    except Exception as e:
        logger.error(
            "Refund failed",
            extra={
                "transaction_id": transaction_id,
                "error": str(e)
            }
        )
        raise
```

LOW PRIORITY (2)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 src/services/payment.py:48
```python
if amount > transaction.amount:
```

📝 **Consider Edge Case**

What if amount equals transaction.amount but transaction was already partially refunded?

**Suggestion:**
```python
total_refunded = db.get_total_refunded(transaction_id)
remaining_amount = transaction.amount - total_refunded

if amount > remaining_amount:
    raise InvalidRefundAmountError(
        f"Refund amount {amount} exceeds remaining amount {remaining_amount}"
    )
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 docs/API.md

📝 **Documentation Update Needed**

New refund endpoint should be documented in API docs.

**Suggestion:**
Add to `docs/API.md`:

```markdown
### POST /api/refunds

Process a refund for a transaction.

**Request:**
```json
{
  "transaction_id": "tx_123",
  "amount": 50.00,
  "reason": "Customer request"
}
```

**Response:**
```json
{
  "status": "success",
  "refund_id": "ref_456",
  "amount": 50.00,
  "created_at": "2025-10-25T10:30:00Z"
}
```

**Errors:**
- 404: Transaction not found
- 400: Invalid refund amount
- 500: Gateway error
```
```

SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total comments: 7
- Critical: 0
- High: 2 (must address)
- Medium: 3 (should address)
- Low: 2 (nice to have)

Overall Assessment: APPROVE WITH COMMENTS
Code quality is good, but addressing the race condition and error handling would make it production-ready.
```

### 5. Automated Reviewer Suggestions

**Smart reviewer matching:**

```
Suggested Reviewers
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Based on:
- Files changed
- Domain expertise
- Code ownership
- Review history
- Availability

REQUIRED REVIEWERS (2)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. @alice (Code Owner: src/services/payment.py)
   Expertise: Payment processing, refunds
   Recent reviews: 23 in last month
   Average review time: 3 hours
   Approval rate for similar PRs: 85%

   Why: Code owner of modified file, payment domain expert

2. @security-team (Required for payment changes)
   Expertise: Security, compliance

   Why: All payment-related changes require security review

RECOMMENDED REVIEWERS (2)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3. @bob (Frequent contributor: src/services/)
   Expertise: Backend services, error handling
   Recent reviews: 15 in last month
   Average review time: 2 hours

   Why: Has reviewed similar refactoring changes, quick turnaround

4. @charlie (Test expert)
   Expertise: Testing, quality assurance

   Why: Tests were added, could provide testing feedback

NOT RECOMMENDED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- @dave: On vacation (out of office)
- @eve: Overloaded (15 pending reviews)
- @frank: No relevant expertise for this change

REVIEW ASSIGNMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Minimum reviewers: 2
Recommended: @alice (required), @security-team (required), @bob (optional)

Estimated total review time: 4-6 hours
Expected approval: Within 1 business day
```

---

## Input/Output Format

### Input
```json
{
  "operation": "review_pr",
  "pr_number": 123,
  "options": {
    "generate_description": true,
    "quality_checks": true,
    "breaking_changes": true,
    "suggest_reviewers": true,
    "draft_comments": true
  }
}
```

### Output
```json
{
  "operation": "review_pr",
  "pr_number": 123,
  "status": "completed",
  "description": {
    "generated": true,
    "content": "## Summary\n..."
  },
  "quality_score": 78,
  "quality_checks": {
    "passed": 18,
    "warnings": 4,
    "failed": 0,
    "details": ["..."]
  },
  "breaking_changes": {
    "detected": true,
    "count": 2,
    "severity": "high",
    "details": ["..."]
  },
  "review_comments": {
    "generated": 7,
    "critical": 0,
    "high": 2,
    "medium": 3,
    "low": 2,
    "comments": ["..."]
  },
  "suggested_reviewers": [
    {"username": "alice", "reason": "code_owner", "required": true},
    {"username": "bob", "reason": "expertise", "required": false}
  ],
  "recommendation": "APPROVE_WITH_COMMENTS",
  "estimated_review_time": "15 minutes"
}
```

---

## Integration with Other Skills

### With test-orchestrator
```python
# Check test coverage
pr_review_assistant.review_pr(#123)
→ test_orchestrator.calculate_coverage(changed_files)
→ Coverage: 85% ✅ (meets 80% requirement)
```

### With dependency-guardian
```python
# Check dependency changes
pr_review_assistant.review_pr(#123)
→ dependency_guardian.audit_changes()
→ New vulnerability: ⚠️ Block merge
```

### With refactor-assistant
```python
# Suggest refactoring opportunities
pr_review_assistant.review_pr(#123)
→ refactor_assistant.detect_opportunities()
→ Suggestion: Extract method (complexity 15)
```

### With spec-to-implementation
```python
# After feature implementation
spec_to_impl.implement_feature("refunds")
→ pr_review_assistant.create_pr(changes)
→ Auto-generated PR description
```

---

## Quality Checks (Full List)

### Code Quality (10 checks)
1. ✅ Linting errors
2. ✅ Type hints present
3. ✅ Docstrings added
4. ✅ No commented code
5. ✅ No TODO/FIXME left
6. ✅ Consistent style
7. ✅ Function complexity
8. ✅ Variable naming
9. ✅ No magic numbers
10. ✅ No duplicate code

### Testing (5 checks)
11. ✅ Tests added
12. ✅ Test coverage > threshold
13. ✅ Tests passing
14. ✅ Integration tests
15. ✅ E2E tests (if applicable)

### Security (5 checks)
16. ✅ No hardcoded secrets
17. ✅ No SQL injection
18. ✅ Input validation
19. ✅ Error messages safe
20. ✅ Security patterns followed

### Documentation (3 checks)
21. ✅ API docs updated
22. ✅ README updated
23. ✅ Changelog updated

### Git (2 checks)
24. ✅ Commit message convention
25. ✅ No merge conflicts

---

## Success Metrics

- **PR Description Quality:** 90% require no edits
- **Review Time Reduction:** 40% faster reviews
- **Issue Detection:** 95% of issues caught
- **False Positives:** < 10%
- **Team Adoption:** 80%+ of PRs use assistant

---

**Status:** Ready for implementation
**Dependencies:** test-orchestrator, dependency-guardian, code-analysis
**Next Steps:** Implement PR description generation (MVP)

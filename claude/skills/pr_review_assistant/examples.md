# PR Review Assistant - Usage Examples

Real-world usage examples for pr_review_assistant skill.

---

## Example 1: Basic PR Review

**Scenario:** You want to review a pull request with a few file changes.

```python
from skills.pr_review_assistant.operations import review_pull_request

# Define PR changes
pr_changes = {
    "added": ["src/services/payment_processor.py"],
    "modified": ["src/api/payment_routes.py", "tests/test_payment.py"],
    "deleted": []
}

# Review the PR
result = review_pull_request(
    pr_changes=pr_changes,
    base_branch="main",
    target_branch="feature/add-payment-processor"
)

if result.success:
    review = result.data

    print(f"PR Review: {result.metadata['target_branch']}")
    print("=" * 60)
    print(f"Overall Score: {review['overall_score']}/100")
    print(f"Approval Status: {review['approval_status']}")
    print()

    print(f"Issues Found: {review['total_issues']}")
    print(f"  Critical: {review['critical_issues']}")
    print(f"  Major: {review['major_issues']}")
    print(f"  Minor: {review['minor_issues']}")
    print(f"  Suggestions: {review['suggestions']}")
    print()

    print("Category Scores:")
    for category, data in review['categories'].items():
        score = data['score']
        emoji = "✅" if score >= 80 else "⚠️" if score >= 60 else "❌"
        print(f"  {emoji} {category.replace('_', ' ').title()}: {score}/100")
        if data['issues']:
            print(f"     ({len(data['issues'])} issues)")
    print()

    if review['critical_issues'] > 0 or review['major_issues'] > 0:
        print("Key Issues to Address:")
        for category, data in review['categories'].items():
            for issue in data['issues']:
                if issue['severity'] in ['critical', 'major']:
                    print(f"  - [{issue['severity'].upper()}] {issue['file']}")
                    print(f"    {issue['title']}")
                    print(f"    → {issue['suggestion']}")
                    print()
else:
    print(f"❌ Review failed: {result.error}")
```

**Output:**
```
PR Review: feature/add-payment-processor
============================================================
Overall Score: 78/100
Approval Status: approved_with_comments

Issues Found: 8
  Critical: 0
  Major: 2
  Minor: 5
  Suggestions: 1

Category Scores:
  ✅ Code Quality: 75/100
     (2 issues)
  ✅ Best Practices: 85/100
     (1 issues)
  ⚠️ Testing: 65/100
     (3 issues)
  ✅ Security: 95/100
     (0 issues)
  ⚠️ Documentation: 60/100
     (2 issues)

Key Issues to Address:
  - [MAJOR] src/services/payment_processor.py
    High cyclomatic complexity in process_payment method
    → Consider breaking down into smaller methods

  - [MAJOR] tests/test_payment.py
    Missing edge case tests
    → Add tests for negative amounts and invalid card numbers
```

**Token Usage:** ~2000 tokens (3 files reviewed, multiple issues)

---

## Example 2: CI/CD Quality Gate

**Scenario:** Integrate into CI/CD pipeline to block PRs that don't meet quality standards.

```python
#!/usr/bin/env python3
# .github/workflows/pr_quality_gate.py

import sys
from skills.pr_review_assistant.operations import check_pr_quality

def quality_gate(pr_changes):
    """Fast quality check for CI/CD."""

    print("🔍 Running PR Quality Gate...")

    result = check_pr_quality(
        pr_changes=pr_changes,
        include_tests=True,
        include_security=True
    )

    if not result.success:
        print(f"❌ Quality check failed: {result.error}")
        return 1

    data = result.data
    score = data['overall_quality_score']
    level = data['quality_level']

    print(f"Quality Score: {score}/100 ({level})")
    print()

    # Check individual criteria
    print("Checklist:")
    print(f"  {'✅' if data['has_tests'] else '❌'} Tests included")
    if data.get('test_files'):
        for tf in data['test_files']:
            print(f"      - {tf}")

    print(f"  {'✅' if data['has_documentation'] else '❌'} Documentation updated")
    print(f"  {'✅' if data['follows_conventions'] else '❌'} Follows conventions")
    print(f"  {'✅' if not data['security_concerns'] else '⚠️ '} No security concerns")

    if data['security_concerns']:
        print("\n⚠️  Security Concerns:")
        for concern in data['security_concerns']:
            print(f"    - {concern}")

    print()

    # Gate decision
    if score < 70:
        print(f"❌ QUALITY GATE FAILED (Score: {score}/100)")
        print("Minimum score required: 70/100")
        print()
        print("Issues to fix:")
        if not data['has_tests']:
            print("  - Add tests for your changes")
        if not data['has_documentation']:
            print("  - Update documentation (README, docstrings, etc.)")
        if data['security_concerns']:
            print("  - Address security concerns listed above")
        return 1

    if data['security_concerns']:
        print("⚠️  QUALITY GATE PASSED WITH WARNINGS")
        print("Address security concerns before final merge")
        return 0

    print("✅ QUALITY GATE PASSED")
    return 0

if __name__ == "__main__":
    # Get PR changes from CI environment
    pr_changes = {
        "added": ["src/new_feature.py"],
        "modified": ["src/config.py"],
        "deleted": []
    }

    sys.exit(quality_gate(pr_changes))
```

**CI Output (Failure):**
```
🔍 Running PR Quality Gate...
Quality Score: 60/100 (needs_improvement)

Checklist:
  ❌ Tests included
  ❌ Documentation updated
  ✅ Follows conventions
  ⚠️  No security concerns

⚠️  Security Concerns:
    - Potential sensitive data in: src/config/credentials.py

❌ QUALITY GATE FAILED (Score: 60/100)
Minimum score required: 70/100

Issues to fix:
  - Add tests for your changes
  - Update documentation (README, docstrings, etc.)
  - Address security concerns listed above

Process exited with code 1
```

---

## Example 3: Generate GitHub Review Comment

**Scenario:** Generate a formatted review comment to post on GitHub PR.

```python
from skills.pr_review_assistant.operations import (
    review_pull_request,
    generate_review_comment
)

# Get PR changes (from GitHub API or git diff)
pr_changes = {
    "added": ["src/api/users.py", "tests/test_users.py"],
    "modified": ["src/models/user.py", "README.md"],
    "deleted": []
}

# Perform review
review_result = review_pull_request(
    pr_changes=pr_changes,
    base_branch="main",
    target_branch="feature/user-api"
)

if review_result.success:
    # Generate GitHub-formatted comment
    comment_result = generate_review_comment(
        review_result=review_result.data,
        format="github"
    )

    if comment_result.success:
        print("Generated GitHub Comment:")
        print("=" * 70)
        print(comment_result.data['comment'])
        print("=" * 70)
        print(f"\nComment length: {comment_result.data['length']} chars")
        print(f"Overall score: {comment_result.data['overall_score']}/100")

        # In real usage, post to GitHub:
        # gh_api.create_review_comment(pr_number, comment_result.data['comment'])
    else:
        print(f"❌ Failed to generate comment: {comment_result.error}")
else:
    print(f"❌ Review failed: {review_result.error}")
```

**Output:**
```
Generated GitHub Comment:
======================================================================
## PR Review Summary

**Overall Score:** 85/100 ✅
**Status:** Approved with comments

### Issues Found
- **Major (1):** Address before merging
- **Minor (3):** Consider fixing
- **Suggestions (2):** Optional improvements

### 📊 Category Scores
- Code Quality: 90/100 ✅
- Best Practices: 85/100 ✅
- Testing: 75/100 ⚠️
- Security: 95/100 ✅
- Documentation: 80/100 ✅

### ⚠️ Major Issues

**1. tests/test_users.py** - Missing edge case tests
- No tests for invalid email formats
- Suggestion: Add test cases for malformed email addresses

### 💡 Minor Issues & Suggestions

**2. src/api/users.py:23** - Consider adding input validation
- Email validation could be more robust
- Suggestion: Use regex pattern for email validation

**3. README.md** - API documentation could be more detailed
- Missing request/response examples
- Suggestion: Add example API calls with expected responses

---
*Generated by PR Review Assistant v0.1.0*
======================================================================

Comment length: 956 chars
Overall score: 85/100
```

**Token Usage:** ~1500 tokens (review + comment generation)

---

## Example 4: Change Impact Analysis

**Scenario:** Assess the risk and scope of a large PR before detailed review.

```python
from skills.pr_review_assistant.operations import analyze_change_impact

# Large PR with many changes
pr_changes = {
    "added": [
        "src/features/notifications.py",
        "src/services/email_service.py",
        "tests/test_notifications.py",
        "docs/notifications.md"
    ],
    "modified": [
        "src/api/routes.py",
        "src/models/user.py",
        "src/models/notification.py",
        "src/utils/helpers.py",
        "requirements.txt",
        "README.md",
        "docs/api.md"
    ],
    "deleted": [
        "src/legacy/old_notifications.py",
        "src/legacy/email.py"
    ]
}

result = analyze_change_impact(pr_changes)

if result.success:
    impact = result.data

    print("📊 PR Change Impact Analysis")
    print("=" * 60)
    print(f"Total Files Changed: {impact['total_files_changed']}")
    print(f"  Added:    {impact['files_added']}")
    print(f"  Modified: {impact['files_modified']}")
    print(f"  Deleted:  {impact['files_deleted']}")
    print()

    print("File Types:")
    for file_type, count in sorted(impact['file_types'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {file_type}: {count} files")
    print()

    # Risk assessment
    risk = impact['risk_level']
    risk_emoji = "🔴" if risk == "high" else "🟡" if risk == "medium" else "🟢"

    print(f"Risk Level: {risk_emoji} {risk.upper()}")
    print()

    # Recommendations
    if impact['recommendations']:
        print("⚠️  Recommendations:")
        for rec in impact['recommendations']:
            print(f"  - {rec}")
        print()

    # Workflow decision
    if risk == "high":
        print("🚨 High Risk PR - Extra Scrutiny Required:")
        print("  1. Require 2+ experienced reviewers")
        print("  2. Run full test suite + integration tests")
        print("  3. Manual QA testing required")
        print("  4. Staged rollout recommended")
        print("  5. Monitor metrics closely after merge")
    elif risk == "medium":
        print("⚠️  Medium Risk - Standard Review Process:")
        print("  1. At least 1 reviewer required")
        print("  2. Run standard test suite")
        print("  3. Consider manual testing for critical paths")
    else:
        print("✅ Low Risk - Fast-Track Review:")
        print("  1. Single reviewer acceptable")
        print("  2. Automated tests sufficient")
```

**Output:**
```
📊 PR Change Impact Analysis
============================================================
Total Files Changed: 13
  Added:    4
  Modified: 7
  Deleted:  2

File Types:
  .py: 9 files
  .md: 3 files
  .txt: 1 files

Risk Level: 🟡 MEDIUM

⚠️  Recommendations:
  - Large number of deletions - verify no breaking changes

⚠️  Medium Risk - Standard Review Process:
  1. At least 1 reviewer required
  2. Run standard test suite
  3. Consider manual testing for critical paths
```

**Token Usage:** ~300 tokens (lightweight analysis)

---

## Example 5: Integration with Test Orchestrator

**Scenario:** Check if PR includes tests, generate missing tests if needed.

```python
from skills.pr_review_assistant.operations import check_pr_quality
from skills.test_orchestrator.operations import generate_tests

pr_changes = {
    "added": [],
    "modified": ["src/payment.py", "src/utils/validators.py"],
    "deleted": []
}

print("1. Checking PR quality...")
quality = check_pr_quality(pr_changes)

if quality.success:
    if not quality.data['has_tests']:
        print("⚠️  No tests found in PR")
        print()

        # Generate tests for modified files
        print("2. Generating tests for modified files...")

        for file in pr_changes['modified']:
            if file.endswith('.py') and not file.startswith('test_'):
                print(f"\nGenerating tests for {file}...")

                test_result = generate_tests(
                    source_file=file,
                    response_format="concise"
                )

                if test_result.success:
                    print(f"✅ Generated: {test_result.data['test_file']}")
                    print(f"   Tests created: {test_result.data['tests_generated']}")
                else:
                    print(f"❌ Failed: {test_result.error}")

        print()
        print("💡 Suggestion: Add generated tests to your PR")
    else:
        print("✅ Tests included:")
        for test_file in quality.data['test_files']:
            print(f"  - {test_file}")
```

**Output:**
```
1. Checking PR quality...
⚠️  No tests found in PR

2. Generating tests for modified files...

Generating tests for src/payment.py...
✅ Generated: tests/test_payment.py
   Tests created: 8

Generating tests for src/utils/validators.py...
✅ Generated: tests/test_validators.py
   Tests created: 5

💡 Suggestion: Add generated tests to your PR
```

---

## Example 6: Security-Focused Review

**Scenario:** Extra scrutiny for security-sensitive PRs.

```python
from skills.pr_review_assistant.operations import (
    review_pull_request,
    check_pr_quality
)
from skills.dependency_guardian.operations import check_vulnerabilities

pr_changes = {
    "added": ["src/auth/oauth_handler.py"],
    "modified": [
        "src/api/auth_routes.py",
        "src/middleware/security.py",
        "requirements.txt"
    ],
    "deleted": []
}

print("🔒 Security-Focused PR Review")
print("=" * 60)

# 1. Quick security check
print("\n1. Quick security scan...")
quality = check_pr_quality(pr_changes, include_security=True)

if quality.success:
    if quality.data['security_concerns']:
        print("⚠️  Security concerns found:")
        for concern in quality.data['security_concerns']:
            print(f"  - {concern}")
    else:
        print("✅ No obvious security concerns in filenames")

# 2. Full review with security focus
print("\n2. Comprehensive security review...")
review = review_pull_request(pr_changes)

if review.success:
    security_score = review.data['categories']['security']['score']

    print(f"Security Score: {security_score}/100")

    if security_score < 80:
        print("⚠️  Security issues found:")
        for issue in review.data['categories']['security']['issues']:
            print(f"\n  {issue['severity'].upper()}: {issue['file']}")
            print(f"  {issue['title']}")
            print(f"  → {issue['suggestion']}")
    else:
        print("✅ Security review passed")

# 3. Check dependency changes
if "requirements.txt" in pr_changes['modified']:
    print("\n3. Checking dependency changes...")
    vulns = check_vulnerabilities(".")

    if vulns.success:
        if vulns.data['total_vulnerabilities'] > 0:
            print(f"⚠️  {vulns.data['total_vulnerabilities']} vulnerabilities in dependencies")
            print(f"  Critical: {vulns.data['critical']}")
            print(f"  High: {vulns.data['high']}")
        else:
            print("✅ No vulnerabilities in dependencies")

# 4. Final verdict
print("\n" + "=" * 60)
print("Security Review Summary:")

security_approved = (
    quality.success and
    not quality.data.get('security_concerns') and
    review.success and
    review.data['categories']['security']['score'] >= 80 and
    (vulns.success and vulns.data['total_vulnerabilities'] == 0 if 'vulns' in locals() else True)
)

if security_approved:
    print("✅ APPROVED - No security issues found")
else:
    print("⛔ CHANGES REQUESTED - Address security issues")
```

**Output:**
```
🔒 Security-Focused PR Review
============================================================

1. Quick security scan...
⚠️  Security concerns found:
  - Potential sensitive data in: src/auth/oauth_handler.py

2. Comprehensive security review...
Security Score: 75/100
⚠️  Security issues found:

  MAJOR: src/auth/oauth_handler.py
  OAuth credentials may be logged
  → Ensure sensitive data is not logged or exposed

3. Checking dependency changes...
✅ No vulnerabilities in dependencies

============================================================
Security Review Summary:
⛔ CHANGES REQUESTED - Address security issues
```

---

## Example 7: Risk-Based Reviewer Assignment

**Scenario:** Assign reviewers based on PR risk level and expertise.

```python
from skills.pr_review_assistant.operations import analyze_change_impact

# Reviewer pools by expertise
REVIEWERS = {
    "senior": ["alice@example.com", "bob@example.com"],
    "mid": ["carol@example.com", "dave@example.com"],
    "junior": ["eve@example.com", "frank@example.com"]
}

def assign_reviewers(pr_changes):
    """Assign reviewers based on risk level."""

    impact = analyze_change_impact(pr_changes)

    if not impact.success:
        print(f"❌ Impact analysis failed: {impact.error}")
        return []

    data = impact.data
    risk = data['risk_level']

    print(f"Risk Level: {risk.upper()}")
    print(f"Files Changed: {data['total_files_changed']}")
    print()

    # Assign based on risk
    reviewers = []

    if risk == "high":
        # High risk: 2 senior reviewers
        reviewers = REVIEWERS["senior"][:2]
        print("High risk - assigning 2 senior reviewers:")

    elif risk == "medium":
        # Medium risk: 1 senior + 1 mid
        reviewers = [REVIEWERS["senior"][0], REVIEWERS["mid"][0]]
        print("Medium risk - assigning 1 senior + 1 mid-level reviewer:")

    else:
        # Low risk: 1 mid-level reviewer
        reviewers = [REVIEWERS["mid"][0]]
        print("Low risk - assigning 1 mid-level reviewer:")

    for reviewer in reviewers:
        print(f"  - {reviewer}")

    return reviewers

# Example usage
pr_changes = {
    "added": ["src/feature.py"],
    "modified": ["src/api.py", "tests/test_api.py"],
    "deleted": []
}

assigned = assign_reviewers(pr_changes)
```

**Output:**
```
Risk Level: LOW
Files Changed: 3

Low risk - assigning 1 mid-level reviewer:
  - carol@example.com
```

---

## Example 8: Automated Approval Workflow

**Scenario:** Automatically approve PRs that meet all criteria.

```python
from skills.pr_review_assistant.operations import (
    review_pull_request,
    check_pr_quality,
    generate_review_comment
)

def auto_review_workflow(pr_changes):
    """Automated PR review and approval workflow."""

    print("🤖 Automated PR Review Workflow")
    print("=" * 60)

    # Step 1: Quick quality check
    print("\nStep 1: Quality Gate...")
    quality = check_pr_quality(pr_changes)

    if not quality.success or quality.data['overall_quality_score'] < 70:
        print("❌ Failed quality gate")
        return "rejected"

    print("✅ Passed quality gate")

    # Step 2: Full review
    print("\nStep 2: Full Review...")
    review = review_pull_request(pr_changes)

    if not review.success:
        print(f"❌ Review failed: {review.error}")
        return "error"

    score = review.data['overall_score']
    critical = review.data['critical_issues']
    major = review.data['major_issues']

    print(f"Score: {score}/100")
    print(f"Critical issues: {critical}")
    print(f"Major issues: {major}")

    # Step 3: Approval decision
    print("\nStep 3: Approval Decision...")

    if critical > 0:
        decision = "changes_requested"
        print("⛔ CHANGES REQUESTED - Critical issues must be fixed")

    elif major > 0:
        decision = "approved_with_comments"
        print("⚠️  APPROVED WITH COMMENTS - Address major issues in follow-up")

    elif score >= 80:
        decision = "approved"
        print("✅ APPROVED - All checks passed")

    else:
        decision = "approved_with_comments"
        print("⚠️  APPROVED WITH COMMENTS - Minor improvements suggested")

    # Step 4: Generate comment
    print("\nStep 4: Generating Review Comment...")
    comment = generate_review_comment(review.data, format="github")

    if comment.success:
        print("✅ Comment generated")
        # In real usage: post_comment_to_github(comment.data['comment'])

    return decision

# Example usage
pr_changes = {
    "added": ["src/feature.py", "tests/test_feature.py"],
    "modified": ["README.md"],
    "deleted": []
}

decision = auto_review_workflow(pr_changes)
print(f"\n{'=' * 60}")
print(f"Final Decision: {decision.upper()}")
```

**Output:**
```
🤖 Automated PR Review Workflow
============================================================

Step 1: Quality Gate...
✅ Passed quality gate

Step 2: Full Review...
Score: 92/100
Critical issues: 0
Major issues: 0

Step 3: Approval Decision...
✅ APPROVED - All checks passed

Step 4: Generating Review Comment...
✅ Comment generated

============================================================
Final Decision: APPROVED
```

---

## Example 9: Team PR Dashboard

**Scenario:** Generate a dashboard summary for all open PRs.

```python
from skills.pr_review_assistant.operations import (
    check_pr_quality,
    analyze_change_impact
)

# Simulate multiple open PRs
OPEN_PRS = [
    {
        "number": 123,
        "title": "Add user authentication",
        "author": "alice",
        "changes": {
            "added": ["src/auth.py", "tests/test_auth.py"],
            "modified": ["src/api.py"],
            "deleted": []
        }
    },
    {
        "number": 124,
        "title": "Fix payment bug",
        "author": "bob",
        "changes": {
            "added": [],
            "modified": ["src/payment.py"],
            "deleted": []
        }
    },
    {
        "number": 125,
        "title": "Refactor database layer",
        "author": "carol",
        "changes": {
            "added": ["src/db/new_orm.py"],
            "modified": [f"src/models/model{i}.py" for i in range(15)],
            "deleted": ["src/db/old_orm.py"]
        }
    }
]

print("📊 Team PR Dashboard")
print("=" * 70)

for pr in OPEN_PRS:
    print(f"\nPR #{pr['number']}: {pr['title']}")
    print(f"Author: {pr['author']}")

    # Quick analysis
    quality = check_pr_quality(pr['changes'])
    impact = analyze_change_impact(pr['changes'])

    if quality.success and impact.success:
        # Quality indicators
        score = quality.data['overall_quality_score']
        score_emoji = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"

        print(f"  Quality: {score_emoji} {score}/100")

        # Risk indicator
        risk = impact.data['risk_level']
        risk_emoji = "🔴" if risk == "high" else "🟡" if risk == "medium" else "🟢"

        print(f"  Risk: {risk_emoji} {risk}")

        # Change stats
        files = impact.data['total_files_changed']
        print(f"  Files: {files} changed")

        # Test coverage
        has_tests = "✅" if quality.data['has_tests'] else "❌"
        print(f"  Tests: {has_tests}")

        # Recommendation
        if score >= 80 and risk == "low" and quality.data['has_tests']:
            print(f"  → Ready to merge")
        elif score < 60 or risk == "high":
            print(f"  → Needs review")
        else:
            print(f"  → Review in progress")

print("\n" + "=" * 70)
```

**Output:**
```
📊 Team PR Dashboard
======================================================================

PR #123: Add user authentication
Author: alice
  Quality: 🟢 85/100
  Risk: 🟢 low
  Files: 3 changed
  Tests: ✅
  → Ready to merge

PR #124: Fix payment bug
Author: bob
  Quality: 🟡 65/100
  Risk: 🟢 low
  Files: 1 changed
  Tests: ❌
  → Review in progress

PR #125: Refactor database layer
Author: carol
  Quality: 🟡 70/100
  Risk: 🟡 medium
  Files: 17 changed
  Tests: ✅
  → Needs review

======================================================================
```

---

## Best Practices Summary

### 1. Use Right Tool for the Job
- Quick checks: `check_pr_quality`
- Full analysis: `review_pull_request`
- Risk assessment: `analyze_change_impact`

### 2. Integrate into CI/CD
- Run quality gates on every PR
- Auto-generate review comments
- Block merges on critical issues

### 3. Risk-Based Workflows
- High risk = more reviewers + manual QA
- Low risk = fast-track approval
- Adjust process based on impact

### 4. Combine with Other Skills
- `test_orchestrator` for missing tests
- `dependency_guardian` for dependency changes
- `refactor_assistant` for code improvements

### 5. Automate When Possible
- Auto-approve low-risk, high-quality PRs
- Auto-assign reviewers based on risk
- Auto-generate review comments

---

## Token Efficiency Tips

**Use quick checks for gates:**
```python
# Quick: ~200 tokens
check_pr_quality(pr_changes)

# Full: ~2000 tokens
review_pull_request(pr_changes)
```

**Generate concise comments:**
```python
# Detailed: ~2000 tokens
generate_review_comment(review, format="github")

# Concise: ~800 tokens
generate_review_comment(review, format="markdown")
```

**Impact analysis is lightweight:**
```python
# Very fast: ~200 tokens
analyze_change_impact(pr_changes)
```

---

## Related Examples

- **test_orchestrator/examples.md** - Generating tests for PRs
- **dependency_guardian/examples.md** - Checking dependency changes
- **refactor_assistant/examples.md** - Code improvement suggestions

---

*Last Updated: 2025-11-08*

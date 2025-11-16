# PR Review Assistant - API Reference

Complete documentation for all pr_review_assistant operations.

---

## Overview

PR Review Assistant provides automated pull request review capabilities with comprehensive code analysis, quality checks, and formatted feedback generation. It helps maintain code quality and catches issues before merging.

---

## Operations

### review_pull_request

Perform comprehensive pull request review.

#### Signature

```python
def review_pull_request(
    pr_changes: Dict[str, Any],
    base_branch: str = "main",
    target_branch: str = "feature",
    checklist: Optional[List[str]] = None,
    **kwargs
) -> OperationResult
```

#### Parameters

**pr_changes** (Dict[str, Any], required)
- Dictionary containing file changes
- Required keys: `"added"`, `"modified"`, `"deleted"`
- Each key contains list of file paths

```python
pr_changes = {
    "added": ["src/new_module.py", "tests/test_new_module.py"],
    "modified": ["src/existing.py", "README.md"],
    "deleted": ["src/deprecated.py"]
}
```

**base_branch** (str, optional, default="main")
- Base branch name (target for merge)
- Common values: `"main"`, `"master"`, `"develop"`

**target_branch** (str, optional, default="feature")
- Feature branch name (source of changes)
- Used for context and reporting

**checklist** (Optional[List[str]], optional, default=None)
- Custom review checklist items
- If None, uses default checklist
- Example: `["Security review", "Performance check"]`

#### Returns

```python
{
    "success": True,
    "data": {
        "overall_score": 85,  # 0-100
        "total_issues": 12,
        "critical_issues": 0,
        "major_issues": 2,
        "minor_issues": 7,
        "suggestions": 3,
        "files_reviewed": 5,
        "categories": {
            "code_quality": {
                "score": 80,
                "issues": [
                    {
                        "file": "src/payment.py",
                        "line": 45,
                        "severity": "major",
                        "category": "complexity",
                        "title": "High cyclomatic complexity",
                        "description": "Function 'process_payment' has complexity of 15",
                        "suggestion": "Consider breaking down into smaller functions"
                    }
                ]
            },
            "best_practices": {
                "score": 90,
                "issues": []
            },
            "testing": {
                "score": 75,
                "issues": [
                    {
                        "file": "tests/test_payment.py",
                        "severity": "minor",
                        "category": "coverage",
                        "title": "Missing edge case tests",
                        "description": "No tests for negative amounts",
                        "suggestion": "Add test for amount < 0"
                    }
                ]
            },
            "security": {
                "score": 95,
                "issues": []
            },
            "documentation": {
                "score": 70,
                "issues": [
                    {
                        "file": "src/new_module.py",
                        "severity": "minor",
                        "category": "documentation",
                        "title": "Missing docstrings",
                        "description": "Public functions lack documentation",
                        "suggestion": "Add docstrings to public API"
                    }
                ]
            }
        },
        "summary": "Good PR with minor issues. Address complexity concern in payment.py.",
        "approval_status": "approved_with_comments",  # approved | approved_with_comments | changes_requested
        "checklist_status": {
            "Tests included": True,
            "Documentation updated": False,
            "Breaking changes documented": "N/A"
        }
    },
    "duration": 2.345,
    "metadata": {
        "skill": "pr-review-assistant",
        "operation": "review_pull_request",
        "version": "0.1.0",
        "base_branch": "main",
        "target_branch": "feature/payment-updates",
        "files_reviewed": 5
    }
}
```

#### Issue Severity Levels

| Severity | Description | Blocks Merge |
|----------|-------------|--------------|
| critical | Must fix before merge | Yes |
| major | Should fix before merge | Recommended |
| minor | Consider fixing | No |
| suggestion | Optional improvement | No |

#### Approval Status

- **approved** - No issues, ready to merge
- **approved_with_comments** - Minor issues, can merge after review
- **changes_requested** - Must address issues before merge

#### Error Handling

**VALIDATION_ERROR:**
```python
{
    "success": False,
    "error": "Invalid pr_changes format: missing key 'added'",
    "error_code": "VALIDATION_ERROR"
}
```

**FILE_NOT_FOUND:**
```python
{
    "success": False,
    "error": "File not found: src/payment.py",
    "error_code": "FILE_NOT_FOUND"
}
```

**REVIEW_ERROR:**
```python
{
    "success": False,
    "error": "PR review failed: Unable to parse file",
    "error_code": "REVIEW_ERROR"
}
```

---

### generate_review_comment

Generate formatted review comment from review results.

#### Signature

```python
def generate_review_comment(
    review_result: Dict[str, Any],
    format: str = "github",
    **kwargs
) -> OperationResult
```

#### Parameters

**review_result** (Dict[str, Any], required)
- Result from `review_pull_request` operation
- Must contain `overall_score`, `categories`, etc.

**format** (str, optional, default="github")
- Output format for comment
- Valid values: `"github"`, `"gitlab"`, `"markdown"`
- Each format optimized for its platform

#### Returns

```python
{
    "success": True,
    "data": {
        "comment": "## PR Review Summary\n\n...",
        "format": "github",
        "length": 1234,
        "overall_score": 85
    },
    "duration": 0.123,
    "metadata": {
        "skill": "pr-review-assistant",
        "operation": "generate_review_comment",
        "version": "0.1.0",
        "format": "github"
    }
}
```

#### Comment Formats

**GitHub format:**
```markdown
## PR Review Summary

**Overall Score:** 85/100 ✅
**Status:** Approved with comments

### Issues Found
- **Major (2):** Address before merging
- **Minor (7):** Consider fixing
- **Suggestions (3):** Optional improvements

### 📊 Category Scores
- Code Quality: 80/100
- Best Practices: 90/100
- Testing: 75/100
- Security: 95/100
- Documentation: 70/100

### ⚠️ Major Issues
1. **src/payment.py:45** - High cyclomatic complexity
   - Function 'process_payment' has complexity of 15
   - Consider breaking down into smaller functions

### 💡 Suggestions
- Add docstrings to public API in src/new_module.py
- Add test for negative amounts

---
*Generated by PR Review Assistant*
```

**GitLab format:** Similar but uses GitLab-specific markdown

**Markdown format:** Plain markdown without platform-specific formatting

#### Error Handling

**VALIDATION_ERROR:**
```python
{
    "success": False,
    "error": "Invalid format or review result: Unknown format 'slack'",
    "error_code": "VALIDATION_ERROR"
}
```

---

### analyze_change_impact

Analyze the impact and risk level of PR changes.

#### Signature

```python
def analyze_change_impact(
    pr_changes: Dict[str, Any],
    **kwargs
) -> OperationResult
```

#### Parameters

**pr_changes** (Dict[str, Any], required)
- Dictionary containing file changes
- Same format as `review_pull_request`

#### Returns

```python
{
    "success": True,
    "data": {
        "total_files_changed": 15,
        "files_added": 3,
        "files_modified": 10,
        "files_deleted": 2,
        "file_types": {
            ".py": 8,
            ".js": 4,
            ".md": 2,
            ".json": 1
        },
        "risk_level": "medium",  # low | medium | high
        "recommendations": [
            "Large changeset - consider splitting into smaller PRs",
            "Large number of deletions - verify no breaking changes"
        ]
    },
    "duration": 0.045,
    "metadata": {
        "skill": "pr-review-assistant",
        "operation": "analyze_change_impact",
        "version": "0.1.0"
    }
}
```

#### Risk Level Thresholds

| Files Changed | Risk Level |
|---------------|------------|
| 0-10 | low |
| 11-20 | medium |
| 21+ | high |

#### Recommendation Triggers

- **Large changeset** - More than 15 files changed
- **Many deletions** - More than 5 files deleted
- **Many additions** - 2x more additions than modifications
- **Mixed file types** - Changes span multiple languages/domains

---

### check_pr_quality

Quick quality check for PR changes.

#### Signature

```python
def check_pr_quality(
    pr_changes: Dict[str, Any],
    include_tests: bool = True,
    include_security: bool = True,
    **kwargs
) -> OperationResult
```

#### Parameters

**pr_changes** (Dict[str, Any], required)
- Dictionary containing file changes
- Same format as `review_pull_request`

**include_tests** (bool, optional, default=True)
- Check for test coverage
- Looks for test files in changes

**include_security** (bool, optional, default=True)
- Perform basic security checks
- Looks for sensitive keywords in filenames

#### Returns

```python
{
    "success": True,
    "data": {
        "has_tests": True,
        "test_files": ["tests/test_payment.py", "tests/test_api.py"],
        "has_documentation": True,
        "follows_conventions": True,
        "security_concerns": [
            "Potential sensitive data in: src/config/credentials.py"
        ],
        "overall_quality_score": 70,  # 0-100
        "quality_level": "good"  # excellent | good | needs_improvement
    },
    "duration": 0.023,
    "metadata": {
        "skill": "pr-review-assistant",
        "operation": "check_pr_quality",
        "version": "0.1.0"
    }
}
```

#### Quality Score Calculation

| Factor | Points |
|--------|--------|
| Has tests | 40 |
| Has documentation | 30 |
| Follows conventions | 20 |
| No security concerns | 10 |
| **Total** | **100** |

#### Quality Levels

- **excellent** - 90-100 points
- **good** - 70-89 points
- **needs_improvement** - 0-69 points

#### Security Checks

Flags files containing these keywords:
- password, secret, key, token, credential
- private_key, api_key, auth_token
- .env, credentials, secrets

---

## Best Practices

### 1. Use Quick Checks for Gates

```python
# ✅ Good: Fast quality gate
quality = check_pr_quality(pr_changes)

if quality.data['overall_quality_score'] < 70:
    print("Failed quality gate")
    exit(1)

# ❌ Bad: Full review for simple gate
review = review_pull_request(pr_changes)  # Slower, more tokens
```

### 2. Generate Platform-Specific Comments

```python
# ✅ Good: Use correct format
comment = generate_review_comment(review, format="github")
# GitHub-optimized markdown

# ❌ Bad: Generic format
comment = generate_review_comment(review, format="markdown")
# Loses platform-specific features
```

### 3. Check Impact Early

```python
# ✅ Good: Assess risk first
impact = analyze_change_impact(pr_changes)

if impact.data['risk_level'] == 'high':
    # Extra scrutiny, more reviewers, etc.
    pass

# ❌ Bad: Skip impact assessment
# Miss opportunity for risk-based workflow
```

### 4. Handle Review Results Appropriately

```python
# ✅ Good: Act on approval status
review = review_pull_request(pr_changes)

if review.data['approval_status'] == 'changes_requested':
    # Block merge, notify author
elif review.data['approval_status'] == 'approved_with_comments':
    # Allow merge, create follow-up issues
else:
    # Approved, merge

# ❌ Bad: Ignore approval status
# Merge without considering issues
```

---

## Common Workflows

### Workflow 1: CI/CD Quality Gate

```python
from skills.pr_review_assistant.operations import check_pr_quality

pr_changes = get_pr_changes()  # From CI environment

quality = check_pr_quality(pr_changes)

if quality.success:
    score = quality.data['overall_quality_score']

    if score < 70:
        print(f"❌ Quality gate failed: {score}/100")
        print("Issues:")
        if not quality.data['has_tests']:
            print("  - No tests included")
        if not quality.data['has_documentation']:
            print("  - No documentation updates")
        if quality.data['security_concerns']:
            print(f"  - Security concerns: {len(quality.data['security_concerns'])}")
        exit(1)

    print(f"✅ Quality gate passed: {score}/100")
```

### Workflow 2: Automated Review Comments

```python
from skills.pr_review_assistant.operations import (
    review_pull_request,
    generate_review_comment
)

pr_changes = get_pr_changes()

# Perform review
review = review_pull_request(pr_changes, base_branch="main")

if review.success:
    # Generate formatted comment
    comment = generate_review_comment(review.data, format="github")

    # Post to GitHub
    if comment.success:
        post_pr_comment(comment.data['comment'])

    # Decide on approval
    if review.data['approval_status'] == 'changes_requested':
        request_changes_on_pr()
    elif review.data['critical_issues'] == 0:
        approve_pr()
```

### Workflow 3: Risk-Based Review

```python
from skills.pr_review_assistant.operations import analyze_change_impact

pr_changes = get_pr_changes()

# Assess impact
impact = analyze_change_impact(pr_changes)

if impact.success:
    risk = impact.data['risk_level']

    print(f"Risk Level: {risk}")
    print(f"Files Changed: {impact.data['total_files_changed']}")

    # Adjust review process based on risk
    if risk == 'high':
        print("High risk PR:")
        print("  - Require 2+ reviewers")
        print("  - Run extended test suite")
        print("  - Manual QA required")

        for rec in impact.data['recommendations']:
            print(f"  - {rec}")
    elif risk == 'medium':
        print("Medium risk - standard review process")
    else:
        print("Low risk - fast-track review")
```

---

## Performance Notes

### Execution Time

| Operation | Typical Time | Depends On |
|-----------|--------------|------------|
| review_pull_request | 2-5s | Number of files, file size |
| generate_review_comment | <0.2s | Review complexity |
| analyze_change_impact | <0.1s | Number of files |
| check_pr_quality | <0.1s | Number of files |

### Token Usage

| Operation | Token Usage | Notes |
|-----------|-------------|-------|
| review_pull_request | 1500-3000 | Full review with all categories |
| generate_review_comment | 500-2000 | Depends on issues found |
| analyze_change_impact | 200-400 | Lightweight analysis |
| check_pr_quality | 100-300 | Quick check only |

---

## Related Skills

- **refactor_assistant** - Get specific refactoring suggestions for code issues
- **test_orchestrator** - Generate tests for uncovered code
- **dependency_guardian** - Check dependency changes in PR
- **code_analysis** - Deep code analysis for complex changes

---

## Dependencies

### Required

- Python 3.8+

### Optional

- GitHub API (for posting comments)
- GitLab API (for posting comments)

---

*Last Updated: 2025-11-08*

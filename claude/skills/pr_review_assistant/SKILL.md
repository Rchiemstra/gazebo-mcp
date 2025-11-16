---
name: pr-review-assistant
description: Automated pull request review system that analyzes code changes, checks quality, security, and best practices
version: 0.1.0
category: development
tags:
  - code-review
  - pull-requests
  - quality
  - security
  - best-practices
activation: manual
tools:
  - Read
dependencies: []
---

# PR Review Assistant

Automated pull request review system that provides comprehensive code analysis, quality checks, security scanning, and best practice recommendations.

---

## When to Use This Skill

Use pr-review-assistant when you need to:

- **Review pull requests** - Comprehensive code change analysis
- **Generate review comments** - Formatted feedback for GitHub/GitLab
- **Assess change impact** - Understand risk and scope of changes
- **Quick quality checks** - Verify tests, docs, and security
- **Automated PR gates** - CI/CD integration for quality control

**Don't use for:**
- Code refactoring (use refactor_assistant)
- Security vulnerability scanning (use dependency_guardian)
- Generating tests (use test_orchestrator)

---

## Quick Start

```python
from skills.pr_review_assistant.operations import review_pull_request

# Review a PR
pr_changes = {
    "added": ["src/new_feature.py"],
    "modified": ["src/payment.py", "tests/test_payment.py"],
    "deleted": []
}

result = review_pull_request(
    pr_changes=pr_changes,
    base_branch="main",
    target_branch="feature/new-payment"
)

if result.success:
    review = result.data
    print(f"Review Score: {review['overall_score']}/100")
    print(f"Issues Found: {review['total_issues']}")
```

---

## Operations

### review_pull_request
Perform comprehensive pull request review.

**Returns:** Detailed review with issues, suggestions, and overall score

### generate_review_comment
Generate formatted review comment from review results.

**Returns:** Markdown/GitHub/GitLab formatted comment ready to post

### analyze_change_impact
Analyze the impact and risk level of PR changes.

**Returns:** Impact metrics, risk assessment, and recommendations

### check_pr_quality
Quick quality check for PR changes.

**Returns:** Quality score with checks for tests, docs, and security

---

## Review Categories

**Code Quality:**
- Style and formatting
- Code complexity
- Naming conventions
- Code duplication

**Best Practices:**
- Design patterns
- Error handling
- Resource management
- Performance considerations

**Testing:**
- Test coverage
- Test quality
- Edge cases
- Integration tests

**Security:**
- Sensitive data exposure
- Input validation
- Authentication/authorization
- Dependency vulnerabilities

**Documentation:**
- Code comments
- README updates
- API documentation
- Migration guides

---

## Quality Score

Review results include an overall quality score (0-100):

- **90-100** - Excellent: Ready to merge
- **70-89** - Good: Minor improvements suggested
- **50-69** - Needs Work: Address issues before merging
- **<50** - Poor: Significant changes required

---

## Token Efficiency

**Uses Read tool** - Low to moderate token usage

**Tip:** Use `check_pr_quality` for quick checks:
```python
# Quick check: ~300 tokens
check_pr_quality(pr_changes)

# Full review: ~1500-3000 tokens
review_pull_request(pr_changes)
```

**Format options:**
```python
# Detailed GitHub comment: ~2000 tokens
generate_review_comment(review, format="github")

# Concise markdown: ~500 tokens
generate_review_comment(review, format="markdown")
```

---

## Security

**Safety Level:** Low (Read-only analysis)

**Safe because:**
- Read-only file analysis
- No code execution
- No external network calls
- Reports only, no modifications

**Audit focus:**
- File reading patterns
- No sensitive areas expected

See `../SECURITY.md` for details.

---

## Documentation

**For complete API reference:** See `reference.md`
- Full operation signatures
- All parameters and return values
- Review format details
- Error codes and handling

**For usage examples:** See `examples.md`
- 9 real-world scenarios
- CI/CD integration patterns
- Multi-file PR reviews
- Automated comment generation

---

## Common Patterns

### Pattern 1: Quick Quality Gate
```python
# Fast quality check for CI/CD
quality = check_pr_quality(pr_changes)

if quality.data['overall_quality_score'] < 70:
    print("❌ Quality check failed")
```

### Pattern 2: Full Review with Comments
```python
# Complete review workflow
review = review_pull_request(pr_changes)
comment = generate_review_comment(review.data, format="github")

# Post comment to GitHub PR
```

### Pattern 3: Impact Assessment
```python
# Understand change scope
impact = analyze_change_impact(pr_changes)

if impact.data['risk_level'] == 'high':
    print("⚠️  High risk changes - extra scrutiny needed")
```

---

## Related Skills

- **refactor_assistant** - Refactoring suggestions for code improvements
- **test_orchestrator** - Generate missing tests identified in review
- **dependency_guardian** - Check dependency changes in PR
- **code_analysis** - Deeper code analysis for complex changes

---

## Quick Reference

**Full review:**
```python
review_pull_request(pr_changes, base_branch="main")
```

**Generate comment:**
```python
generate_review_comment(review_result, format="github")
```

**Impact analysis:**
```python
analyze_change_impact(pr_changes)
```

**Quality check:**
```python
check_pr_quality(pr_changes, include_tests=True, include_security=True)
```

---

*Last Updated: 2025-11-08*

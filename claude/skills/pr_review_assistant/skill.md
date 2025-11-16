---
name: pr-review-assistant
description: Automated pull request review system that analyzes code changes, checks quality, security, and best practices
version: 0.1.0
author: Claude Code Skills
category: code-review
tags:
  - code-review
  - pull-requests
  - quality-assurance
  - automation
  - best-practices
tools:
  - Read
  - Bash
  - Grep
activation: manual
dependencies:
  - test-orchestrator
  - refactor-assistant
  - dependency-guardian
operations:
  review_pull_request: "Performs comprehensive PR review with quality, security, and test coverage analysis"
  generate_review_comment: "Generates formatted review comment from review results"
  analyze_change_impact: "Analyzes the impact and risk level of PR changes"
  check_pr_quality: "Performs quick quality check on PR changes"
---

# PR Review Assistant

An intelligent skill that automates code review by analyzing pull requests for quality, security, test coverage, and best practices.

## Features

- **Automated Review**: Comprehensive PR analysis with actionable feedback
- **Multi-Skill Integration**: Leverages test-orchestrator, refactor-assistant, and dependency-guardian
- **Review Checklist**: Customizable review criteria and standards
- **Security Analysis**: Detects potential security vulnerabilities
- **Test Coverage**: Validates test coverage for changed code
- **Code Quality**: Identifies code smells and quality issues
- **Dependency Check**: Reviews dependency changes for security
- **Best Practices**: Enforces coding standards and conventions

## Review Dimensions

### Code Quality (30%)
- Code smells and anti-patterns
- Complexity metrics
- Naming conventions
- Code organization

### Test Coverage (25%)
- Unit test coverage for new code
- Test quality and completeness
- Edge case coverage
- Mutation testing score

### Security (20%)
- Dependency vulnerabilities
- Security anti-patterns
- Sensitive data handling
- Input validation

### Best Practices (15%)
- Style guide compliance
- Documentation quality
- Error handling
- Performance considerations

### Change Impact (10%)
- Breaking changes detection
- API compatibility
- Performance impact
- Scope appropriateness

## Operations

### review_pull_request

Performs comprehensive PR review.

**Parameters:**
- `pr_changes` (dict): Changed files with diffs
- `base_branch` (str): Base branch name
- `target_branch` (str): Target branch name
- `checklist` (list, optional): Custom review checklist

**Returns:**
- `overall_score`: Overall review score (0-100)
- `dimension_scores`: Scores by dimension
- `issues`: List of identified issues
- `recommendations`: Actionable recommendations
- `approval_status`: approve/request_changes/comment

### generate_review_comment

Generates formatted review comment for PR.

**Parameters:**
- `review_result` (dict): Result from review_pull_request
- `format` (str): Format (markdown, github, gitlab)

**Returns:**
- `comment`: Formatted review comment

### check_review_requirements

Checks if PR meets review requirements.

**Parameters:**
- `pr_changes` (dict): Changed files
- `requirements` (dict): Review requirements

**Returns:**
- `passes`: Whether requirements are met
- `failures`: List of failed requirements

### suggest_reviewers

Suggests appropriate reviewers based on changes.

**Parameters:**
- `pr_changes` (dict): Changed files
- `team_expertise` (dict): Team member expertise areas

**Returns:**
- `suggested_reviewers`: List of recommended reviewers

## Usage Examples

```python
from skills.pr_review_assistant import review_pull_request, generate_review_comment

# Review a PR
result = review_pull_request(
    pr_changes={
        'added': ['new_feature.py'],
        'modified': ['existing_module.py'],
        'deleted': []
    },
    base_branch='main',
    target_branch='feature/new-api'
)

print(f"Overall Score: {result['overall_score']}/100")
print(f"Status: {result['approval_status']}")

# Generate review comment
comment = generate_review_comment(result, format='github')
print(comment)
```

## Integration with Agents

Agents can use pr-review-assistant to:
1. Automate initial PR reviews
2. Enforce quality gates
3. Provide consistent feedback
4. Reduce reviewer burden
5. Maintain coding standards

## Review Process

1. **Analyze Changes**: Parse diff and identify modified code
2. **Run Quality Checks**: Use refactor-assistant for code smells
3. **Check Test Coverage**: Use test-orchestrator to validate tests
4. **Security Scan**: Use dependency-guardian for vulnerabilities
5. **Generate Feedback**: Create actionable review comments
6. **Calculate Score**: Compute overall quality score
7. **Make Decision**: Approve, request changes, or comment

## Quality Gates

Default requirements for approval:
- Overall score ≥ 70/100
- No critical security vulnerabilities
- Test coverage ≥ 80% for new code
- No critical code smells
- All CI checks pass

## Output Format

All operations return structured data suitable for:
- GitHub/GitLab PR comments
- CI/CD integration
- Quality dashboards
- Team notifications

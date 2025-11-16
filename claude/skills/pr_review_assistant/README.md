# PR Review Assistant

An intelligent automated code review system that analyzes pull requests for quality, security, test coverage, and best practices.

## Overview

PR Review Assistant provides comprehensive automated code review by:
- Analyzing code changes across multiple dimensions
- Detecting security vulnerabilities and anti-patterns
- Validating test coverage for new code
- Checking code quality and best practices
- Generating formatted review comments
- Making approval/rejection decisions

## Features

### 🔍 Multi-Dimensional Review

**Code Quality (30% weight)**
- File size and complexity
- Naming conventions
- Code smells detection
- Integration with refactor-assistant

**Test Coverage (25% weight)**
- Test files for new code
- Test naming conventions
- Coverage validation
- Integration with test-orchestrator

**Security (20% weight)**
- Hardcoded secrets detection
- SQL injection patterns
- Sensitive file detection
- Integration with dependency-guardian

**Best Practices (15% weight)**
- Documentation updates
- Error handling patterns
- Code organization
- PR scope appropriateness

**Change Impact (10% weight)**
- Breaking changes detection
- API compatibility
- Deleted files impact
- Scope validation

### 📊 Automated Scoring

- **Overall Score**: Weighted composite (0-100)
- **Dimension Scores**: Individual metric tracking
- **Pass/Fail Checks**: Specific validation rules
- **Approval Decision**: approve/request_changes/comment

### 💬 Formatted Comments

-Generated markdown comments for GitHub/GitLab
- Visual score bars and emojis
- Severity-grouped issues
- Actionable recommendations
- Change statistics

## Installation

No external dependencies required!

```bash
# Optional: For enhanced integration
pip install pygithub  # For GitHub API integration
```

## Quick Start

```python
from pr_review_assistant import review_pull_request, generate_review_comment

# Define PR changes
pr_changes = {
    'added': ['new_feature.py'],
    'modified': ['existing_module.py'],
    'deleted': []
}

# Review the PR
result = review_pull_request(
    pr_changes=pr_changes,
    base_branch='main',
    target_branch='feature/new-api'
)

print(f"Overall Score: {result['overall_score']}/100")
print(f"Status: {result['approval_status']}")

# Generate formatted comment
comment = generate_review_comment(result, format='github')
print(comment)
```

## API Reference

### review_pull_request

Performs comprehensive PR review.

```python
review_pull_request(
    pr_changes: Dict,
    base_branch: str = "main",
    target_branch: str = "feature",
    checklist: Optional[List[str]] = None
) -> Dict
```

**Parameters:**
- `pr_changes`: Dictionary with 'added', 'modified', 'deleted' file lists
- `base_branch`: Base branch name (default: "main")
- `target_branch`: Target branch name (default: "feature")
- `checklist`: Optional custom review checklist

**Returns:**
```python
{
    'overall_score': float,  # 0-100
    'approval_status': str,  # 'approve', 'request_changes', 'comment'
    'dimension_scores': [
        {
            'dimension': str,
            'score': float,
            'weight': float,
            'issues_count': int,
            'passed_checks': int,
            'total_checks': int
        },
        ...
    ],
    'issues': [
        {
            'category': str,
            'severity': str,  # 'blocker', 'critical', 'major', 'minor', 'info'
            'file_path': str,
            'line_number': Optional[int],
            'title': str,
            'description': str,
            'suggestion': str,
            'code_snippet': Optional[str]
        },
        ...
    ],
    'recommendations': [str, ...],
    'statistics': {
        'files_added': int,
        'files_modified': int,
        'files_deleted': int,
        'total_files_changed': int
    }
}
```

### generate_review_comment

Generates formatted review comment.

```python
generate_review_comment(
    review_result: Dict,
    format: str = "github"  # 'github', 'gitlab', 'markdown'
) -> str
```

**Returns:** Formatted markdown comment string

## Review Dimensions

### Code Quality

Checks:
- ✅ File size (< 500 lines)
- ✅ Naming conventions (snake_case for Python, camelCase for JS)
- ✅ No print() in production code

Example Issue:
```
🟠 MAJOR: Large file added
File: large_module.py (687 lines)
💡 Split into focused, cohesive modules (< 500 lines each)
```

### Test Coverage

Checks:
- ✅ Test files exist for new source files
- ✅ Test file naming conventions (test_*.py or *_test.py)

Example Issue:
```
🔴 CRITICAL: No tests for new code
Added 3 source files but no test files
💡 Add test files with >80% coverage for new code
```

### Security

Checks:
- ✅ No hardcoded secrets/API keys
- ✅ No sensitive file types (.env, .key, .pem)
- ✅ No SQL injection patterns
- ✅ Dependency changes reviewed

Example Issue:
```
🚫 BLOCKER: Potential hardcoded secret detected
File: api_client.py
💡 Use environment variables or secret management systems
```

### Best Practices

Checks:
- ✅ Documentation updated for significant changes
- ✅ No bare except clauses
- ✅ Appropriate PR scope (< 20 files)

Example Issue:
```
🟠 MAJOR: Bare except clause
File: payment.py
💡 Catch specific exceptions (e.g., except ValueError:)
```

### Change Impact

Checks:
- ✅ No undocumented breaking changes
- ✅ Deleted files verified

Example Issue:
```
🟠 MAJOR: Potential breaking change
Changes to public API files: api/__init__.py
💡 Document breaking changes and update version accordingly
```

## Approval Logic

### Decision Tree

```
Has BLOCKER issues?
  Yes → REQUEST_CHANGES
  No  ↓

Has CRITICAL issues?
  Yes → REQUEST_CHANGES
  No  ↓

Overall Score < 60?
  Yes → REQUEST_CHANGES
  No  ↓

Overall Score < 80?
  Yes → COMMENT (minor improvements)
  No  → APPROVE (ready to merge)
```

### Quality Gates

Default requirements for approval:
- Overall score ≥ 80/100
- No blocker or critical issues
- Test coverage exists for new code
- No hardcoded secrets
- No SQL injection patterns

## Agent Integration

### Example: GitHub Action Bot

```yaml
name: Automated PR Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Get changed files
        id: changes
        run: |
          echo "added=$(git diff --name-only --diff-filter=A ${{ github.event.pull_request.base.sha }})" >> $GITHUB_OUTPUT
          echo "modified=$(git diff --name-only --diff-filter=M ${{ github.event.pull_request.base.sha }})" >> $GITHUB_OUTPUT
          echo "deleted=$(git diff --name-only --diff-filter=D ${{ github.event.pull_request.base.sha }})" >> $GITHUB_OUTPUT

      - name: Run PR Review
        run: |
          python -c "
          from pr_review_assistant import review_pull_request, generate_review_comment
          import json

          pr_changes = {
              'added': '${{ steps.changes.outputs.added }}'.split(),
              'modified': '${{ steps.changes.outputs.modified }}'.split(),
              'deleted': '${{ steps.changes.outputs.deleted }}'.split()
          }

          result = review_pull_request(pr_changes)
          comment = generate_review_comment(result)

          print(comment)

          # Exit with error if changes requested
          if result['approval_status'] == 'request_changes':
              exit(1)
          "
```

### Example: Quality Gate Enforcer

```python
class PRQualityGate:
    """Enforces quality gates on PRs."""

    def check_pr(self, pr_number: int) -> bool:
        """Check if PR meets quality gates."""
        # Get PR changes
        pr_changes = self.get_pr_changes(pr_number)

        # Run review
        result = review_pull_request(pr_changes)

        # Check gates
        if result['approval_status'] == 'approve':
            self.post_approval_comment(pr_number, result)
            return True
        else:
            self.post_rejection_comment(pr_number, result)
            self.block_merge(pr_number)
            return False

    def post_approval_comment(self, pr_number: int, result: Dict):
        """Post approval comment."""
        comment = generate_review_comment(result)
        self.github_api.post_comment(pr_number, comment)
        self.github_api.approve_pr(pr_number)

    def post_rejection_comment(self, pr_number: int, result: Dict):
        """Post rejection comment."""
        comment = generate_review_comment(result)
        self.github_api.post_comment(pr_number, comment)
        self.github_api.request_changes(pr_number)
```

### Example: Multi-Skill Integration

```python
class ComprehensiveReviewer:
    """Comprehensive review using multiple skills."""

    def review_pr(self, pr_changes):
        """Perform comprehensive review."""
        # 1. Base PR review
        pr_result = review_pull_request(pr_changes)

        # 2. Detailed code smell detection
        from refactor_assistant import detect_code_smells
        for file in pr_changes['added'] + pr_changes['modified']:
            smells = detect_code_smells(file)
            # Add to pr_result issues

        # 3. Test generation for new code
        from test_orchestrator import generate_tests
        for file in pr_changes['added']:
            if self.is_source_file(file):
                tests = generate_tests(file)
                # Check if tests exist

        # 4. Dependency security check
        from dependency_guardian import check_vulnerabilities
        if self.has_dependency_changes(pr_changes):
            vulns = check_vulnerabilities('.')
            # Add to pr_result issues

        # 5. Generate comprehensive comment
        comment = generate_review_comment(pr_result)

        return pr_result, comment
```

## CI/CD Integration

### GitHub Actions

Create `.github/workflows/pr-review.yml`:

```yaml
name: Automated Code Review

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  automated-review:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
      contents: read

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Run automated review
        id: review
        run: |
          # Install skills
          pip install -e skills/pr_review_assistant

          # Run review
          python scripts/automated_review.py \
            --pr-number ${{ github.event.pull_request.number }}

      - name: Post review comment
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const comment = fs.readFileSync('review_comment.md', 'utf8');

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
```

### GitLab CI

Create `.gitlab-ci.yml`:

```yaml
automated_review:
  stage: test
  script:
    - pip install -e skills/pr_review_assistant
    - python scripts/automated_review.py --mr-id $CI_MERGE_REQUEST_IID
    - |
      if [ -f review_comment.md ]; then
        curl --request POST \
          --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
          --data-urlencode "body=$(cat review_comment.md)" \
          "$CI_API_V4_URL/projects/$CI_PROJECT_ID/merge_requests/$CI_MERGE_REQUEST_IID/notes"
      fi
  only:
    - merge_requests
```

## Example Output

```markdown
## 🤖 Automated Code Review

**Overall Score:** 50.0/100 ❌
**Status:** ❌ **CHANGES REQUESTED** - Please address issues

### 📊 Review Dimensions

**Code Quality** (30% weight)
Score: 66.7/100 🟡 ██████░░░░
Checks: 2/3 passed

**Test Coverage** (25% weight)
Score: 0.0/100 🔴 ░░░░░░░░░░
Checks: 0/2 passed

**Security** (20% weight)
Score: 50.0/100 🔴 █████░░░░░
Checks: 2/4 passed

### ⚠️ Issues Found (5)

#### 🚫 Blocker (1)

**Hardcoded API key detected**
📁 File: api_client.py
💡 Use environment variables or secret management

#### 🔴 Critical (2)

**No tests for new code**
💡 Add test files with >80% coverage

**SQL injection vulnerability**
📁 File: database.py
💡 Use parameterized queries

### 💡 Recommendations

- 🚨 Fix 1 blocker issue(s) before merging
- ⚠️  Address 2 critical issue(s)
- 🧪 Add tests for new code (target: 80% coverage)
- 🔒 Review and fix security vulnerabilities
```

## Best Practices

### 1. Run on Every PR

Configure CI to run automated review on all PRs:
- Catches issues early
- Provides consistent feedback
- Reduces reviewer burden

### 2. Customize Quality Gates

Adjust thresholds based on your needs:
```python
# Strict gates for production
APPROVAL_THRESHOLD = 85
BLOCK_ON_MAJOR = True

# Relaxed for experimental branches
APPROVAL_THRESHOLD = 60
BLOCK_ON_MAJOR = False
```

### 3. Combine with Human Review

Automated review complements, doesn't replace:
- Bot catches mechanical issues
- Humans review business logic
- Faster overall review process

### 4. Track Metrics Over Time

Monitor quality trends:
- Average PR scores
- Most common issues
- Time to approval
- Issue recurrence

### 5. Integrate Other Skills

Leverage the full skills ecosystem:
- refactor-assistant for code smells
- test-orchestrator for test generation
- dependency-guardian for security
- Complete coverage!

## Customization

### Custom Review Checklist

```python
custom_checklist = [
    "All functions have docstrings",
    "No TODO comments in production code",
    "Performance tests for API changes",
    "Database migrations included",
    "Documentation updated"
]

result = review_pull_request(
    pr_changes=pr_changes,
    checklist=custom_checklist
)
```

### Custom Severity Thresholds

Modify `PRAnalyzer` class:
```python
class CustomPRAnalyzer(PRAnalyzer):
    DIMENSION_WEIGHTS = {
        'code_quality': 0.40,  # More weight on quality
        'test_coverage': 0.30,  # More weight on tests
        'security': 0.15,
        'best_practices': 0.10,
        'change_impact': 0.05
    }
```

## Limitations

### Current Implementation

- **Pattern-Based Detection**: Uses regex patterns, not deep semantic analysis
- **Python Focus**: Best support for Python, basic for JS/TS
- **Local Analysis**: Doesn't fetch external data (e.g., CVE databases)
- **No Execution**: Static analysis only, doesn't run code

### Future Enhancements

- AST-based semantic analysis
- Multi-language support (Java, Go, Rust)
- Integration with external security databases
- Performance regression detection
- Machine learning-based issue prioritization
- Automatic fix suggestions with diffs

## Troubleshooting

### "No issues found but score is low"

- Dimension scores based on pass/fail checks
- All dimensions contribute to overall score
- Check individual dimension scores for details

### "False positive security issues"

- Pattern matching can have false positives
- Review suggestions and apply where appropriate
- Customize patterns for your codebase

### "PR blocked unfairly"

- Adjust quality gate thresholds
- Review approval logic
- Consider using 'comment' status instead of 'request_changes'

## Demo

Run the comprehensive demo:

```bash
cd skills/pr_review_assistant
python demo.py
```

Shows:
- Complete PR review process
- Multi-dimensional analysis
- Issue detection and categorization
- Formatted comment generation
- Approval decision logic
- Agent integration patterns

## Related Skills

- **test-orchestrator**: Generate tests for PR changes
- **refactor-assistant**: Detect code smells in depth
- **dependency-guardian**: Security vulnerability scanning
- **skills-integration**: Orchestrate multiple skills

## License

Part of Claude Code Skills framework.

## Support

- Run demo: `python demo.py`
- Check API: Read docstrings in source files
- Integration examples: See README sections above

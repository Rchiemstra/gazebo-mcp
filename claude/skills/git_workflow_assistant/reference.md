# Git Workflow Assistant - API Reference

Complete documentation for all git_workflow_assistant operations.

---

## Overview

Git Workflow Assistant provides intelligent Git workflow automation with conventional commits, standardized branch naming, change analysis, and automated PR creation. It helps teams maintain consistent Git practices and reduces manual effort.

---

## Operations

### analyze_changes

Analyze staged and unstaged changes in a git repository.

#### Signature

```python
def analyze_changes(
    repo_path: str = ".",
    include_unstaged: bool = False,
    **kwargs
) -> OperationResult
```

#### Parameters

**repo_path** (str, optional, default=".")
- Path to git repository
- Can be relative or absolute
- Must be valid git repository (contains `.git/`)

**include_unstaged** (bool, optional, default=False)
- Include unstaged changes in analysis
- If False, only analyzes staged changes
- Useful for pre-commit analysis

#### Returns

```python
{
    "success": True,
    "data": {
        "repo_path": "/home/user/project",
        "current_branch": "feature/user-auth",
        "total_files_changed": 8,
        "files_staged": 5,
        "files_unstaged": 3,
        "changes": {
            "added": ["src/auth/oauth.py", "tests/test_oauth.py"],
            "modified": ["src/api/routes.py", "README.md", "requirements.txt"],
            "deleted": [],
            "renamed": []
        },
        "statistics": {
            "lines_added": 245,
            "lines_deleted": 67,
            "net_lines": 178
        },
        "file_types": {
            ".py": 4,
            ".md": 1,
            ".txt": 1
        },
        "categorization": {
            "features": ["src/auth/oauth.py"],
            "tests": ["tests/test_oauth.py"],
            "documentation": ["README.md"],
            "dependencies": ["requirements.txt"],
            "configuration": [],
            "other": ["src/api/routes.py"]
        },
        "commit_type_suggestion": "feat",  # Based on change analysis
        "scope_suggestion": "auth"  # Detected from file paths
    },
    "duration": 0.234,
    "metadata": {
        "skill": "git-workflow-assistant",
        "operation": "analyze_changes",
        "version": "0.1.0",
        "include_unstaged": False
    }
}
```

#### Commit Type Suggestions

Automatically suggests commit type based on changes:

| Changes Detected | Suggested Type |
|-----------------|----------------|
| New files in src/ | feat (feature) |
| Modified existing code | fix or refactor |
| Only test files | test |
| Only docs/README | docs |
| Only package.json/requirements | build |
| Only .github/workflows | ci |

#### Error Handling

**REPO_NOT_FOUND:**
```python
{
    "success": False,
    "error": "Repository not found: /path/to/dir is not a git repository",
    "error_code": "REPO_NOT_FOUND"
}
```

**ANALYSIS_ERROR:**
```python
{
    "success": False,
    "error": "Change analysis failed: git command failed",
    "error_code": "ANALYSIS_ERROR"
}
```

---

### generate_commit_message

Generate conventional commit message from staged changes.

#### Signature

```python
def generate_commit_message(
    repo_path: str = ".",
    commit_type: Optional[str] = None,
    scope: Optional[str] = None,
    breaking: bool = False,
    **kwargs
) -> OperationResult
```

#### Parameters

**repo_path** (str, optional, default=".")
- Path to git repository
- Must have staged changes

**commit_type** (Optional[str], optional, default=None)
- Override commit type
- If None, auto-detected from changes
- Valid: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`

**scope** (Optional[str], optional, default=None)
- Commit scope (component/module affected)
- If None, auto-detected from file paths
- Example: `auth`, `api`, `db`

**breaking** (bool, optional, default=False)
- Mark as breaking change
- Adds `!` to type and `BREAKING CHANGE:` footer
- Use for incompatible API changes

#### Returns

```python
{
    "success": True,
    "data": {
        "commit_message": "feat(auth): add OAuth2 authentication\n\nImplements OAuth2 flow for user authentication.\nAdds OAuth handler and token management.\n\nBREAKING CHANGE: Changes authentication API endpoints",
        "commit_type": "feat",
        "scope": "auth",
        "subject": "add OAuth2 authentication",
        "body": "Implements OAuth2 flow for user authentication.\nAdds OAuth handler and token management.",
        "footer": "BREAKING CHANGE: Changes authentication API endpoints",
        "is_breaking": True,
        "conventional_format": True,
        "files_analyzed": 5
    },
    "duration": 0.456,
    "metadata": {
        "skill": "git-workflow-assistant",
        "operation": "generate_commit_message",
        "version": "0.1.0",
        "commit_type": "feat",
        "breaking": True
    }
}
```

#### Conventional Commit Format

```
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

**Examples:**

Simple feature:
```
feat: add user authentication
```

Feature with scope:
```
feat(api): add user authentication endpoint
```

Breaking change:
```
feat(api)!: redesign authentication API

BREAKING CHANGE: Authentication endpoints moved to /v2/auth
```

Fix with body:
```
fix(db): prevent connection pool exhaustion

Adds maximum connection limits and proper cleanup
to prevent pool exhaustion under high load.
```

#### Error Handling

**REPO_NOT_FOUND:**
```python
{
    "success": False,
    "error": "Repository not found: not a git repository",
    "error_code": "REPO_NOT_FOUND"
}
```

**NO_CHANGES:**
```python
{
    "success": False,
    "error": "No staged changes found: nothing to commit",
    "error_code": "NO_CHANGES"
}
```

**GENERATION_ERROR:**
```python
{
    "success": False,
    "error": "Commit message generation failed: unable to analyze changes",
    "error_code": "GENERATION_ERROR"
}
```

---

### suggest_branch_name

Suggest branch name following conventions.

#### Signature

```python
def suggest_branch_name(
    description: str = "",
    branch_type: str = "feature",
    issue_number: Optional[str] = None,
    strategy: str = "gitflow",
    **kwargs
) -> OperationResult
```

#### Parameters

**description** (str, optional, default="")
- Description of the work
- Used to generate descriptive branch name
- Example: "add user authentication"

**branch_type** (str, optional, default="feature")
- Type of branch
- Valid: `feature`, `bugfix`, `hotfix`, `release`, `docs`, `test`
- Affects branch prefix

**issue_number** (Optional[str], optional, default=None)
- Issue or ticket number
- Incorporated into branch name
- Example: "JIRA-123" → `feature/JIRA-123-add-auth`

**strategy** (str, optional, default="gitflow")
- Branching strategy to follow
- Valid: `gitflow`, `github-flow`, `gitlab-flow`
- Different conventions for each

#### Returns

```python
{
    "success": True,
    "data": {
        "branch_name": "feature/JIRA-123-add-user-authentication",
        "strategy": "gitflow",
        "branch_type": "feature",
        "description": "add user authentication",
        "issue_number": "JIRA-123",
        "alternative_names": [
            "feature/add-user-auth",
            "feature/auth-system",
            "feature/user-authentication"
        ],
        "convention": {
            "prefix": "feature/",
            "include_issue": True,
            "separator": "-",
            "max_length": 50
        }
    },
    "duration": 0.045,
    "metadata": {
        "skill": "git-workflow-assistant",
        "operation": "suggest_branch_name",
        "version": "0.1.0",
        "branch_type": "feature"
    }
}
```

#### Branching Strategies

**GitFlow:**
- **feature/** - New features (`feature/user-auth`)
- **bugfix/** - Bug fixes (`bugfix/login-error`)
- **hotfix/** - Urgent production fixes (`hotfix/security-patch`)
- **release/** - Release branches (`release/1.2.0`)
- **docs/** - Documentation (`docs/api-guide`)
- **test/** - Test improvements (`test/integration-tests`)

**GitHub Flow:**
- Simple descriptive names (`add-user-authentication`)
- Optional username prefix (`alice/add-user-auth`)
- No strict prefixes required

**GitLab Flow:**
- Similar to GitFlow but simpler
- **feature/** for features
- **bugfix/** for fixes
- Environment branches: `staging`, `production`

#### Branch Name Rules

- Lowercase only
- Use hyphens, not spaces or underscores
- Keep under 50 characters
- Descriptive but concise
- Remove special characters
- No trailing/leading hyphens

#### Error Handling

**VALIDATION_ERROR:**
```python
{
    "success": False,
    "error": "Invalid branch parameters: branch_type must be feature|bugfix|hotfix|release",
    "error_code": "VALIDATION_ERROR"
}
```

---

### create_pull_request

Create pull request with auto-generated description.

#### Signature

```python
def create_pull_request(
    repo_path: str = ".",
    base_branch: str = "main",
    head_branch: Optional[str] = None,
    **kwargs
) -> OperationResult
```

#### Parameters

**repo_path** (str, optional, default=".")
- Path to git repository
- Must be valid git repository

**base_branch** (str, optional, default="main")
- Base branch (target for merge)
- Common: `main`, `master`, `develop`

**head_branch** (Optional[str], optional, default=None)
- Head branch (source of changes)
- If None, uses current branch
- Must have commits ahead of base

#### Returns

```python
{
    "success": True,
    "data": {
        "title": "feat(auth): Add OAuth2 authentication",
        "body": "## Summary\n\nImplements OAuth2 authentication flow for user login.\n\n## Changes\n- Add OAuth2 handler\n- Implement token management\n- Add user authentication endpoints\n\n## Testing\n- [ ] Unit tests passing\n- [ ] Integration tests passing\n- [ ] Manual testing completed\n\n## Breaking Changes\nChanges authentication API endpoints to /v2/auth\n\nCloses #123",
        "base_branch": "main",
        "head_branch": "feature/JIRA-123-add-auth",
        "commits_ahead": 5,
        "files_changed": 8,
        "metadata": {
            "conventional_commit": True,
            "breaking_changes": True,
            "has_tests": True,
            "closes_issues": ["#123"]
        }
    },
    "duration": 0.678,
    "metadata": {
        "skill": "git-workflow-assistant",
        "operation": "create_pull_request",
        "version": "0.1.0",
        "base_branch": "main"
    }
}
```

#### PR Description Format

```markdown
## Summary

Brief description of changes.

## Changes
- Bullet list of major changes
- Key features added
- Important modifications

## Testing
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Manual testing completed
- [ ] Documentation updated

## Breaking Changes
(if applicable) Description of breaking changes

## Related Issues
Closes #123
Refs #456
```

#### Error Handling

**REPO_NOT_FOUND:**
```python
{
    "success": False,
    "error": "Repository not found: not a git repository",
    "error_code": "REPO_NOT_FOUND"
}
```

**VALIDATION_ERROR:**
```python
{
    "success": False,
    "error": "Invalid PR parameters: head branch must be ahead of base",
    "error_code": "VALIDATION_ERROR"
}
```

**CREATION_ERROR:**
```python
{
    "success": False,
    "error": "PR creation failed: unable to generate description",
    "error_code": "CREATION_ERROR"
}
```

---

## Best Practices

### 1. Use Conventional Commits

```python
# ✅ Good: Let tool generate conventional commit
commit = generate_commit_message()
# Produces: "feat(auth): add OAuth2 authentication"

# ❌ Bad: Manual non-standard commit
# Produces: "added some auth stuff"
```

### 2. Analyze Before Committing

```python
# ✅ Good: Understand changes first
changes = analyze_changes()
print(f"Committing {changes.data['total_files_changed']} files")

commit = generate_commit_message()

# ❌ Bad: Blind commit
commit = generate_commit_message()  # Without knowing what's changing
```

### 3. Follow Team's Branching Strategy

```python
# ✅ Good: Use team's strategy
branch = suggest_branch_name(
    description="add user auth",
    strategy="gitflow"  # Team uses GitFlow
)

# ❌ Bad: Inconsistent naming
# create branch manually with random name
```

### 4. Include Issue Numbers

```python
# ✅ Good: Link to issue tracker
branch = suggest_branch_name(
    description="fix login bug",
    issue_number="JIRA-456"
)
# Produces: bugfix/JIRA-456-fix-login-bug

# ❌ Bad: No traceability
branch = suggest_branch_name(description="fix bug")
# Hard to track in issue system
```

---

## Common Workflows

### Workflow 1: Feature Development

```python
from skills.git_workflow_assistant.operations import (
    suggest_branch_name,
    analyze_changes,
    generate_commit_message,
    create_pull_request
)

# 1. Create feature branch
branch = suggest_branch_name(
    description="add user notifications",
    branch_type="feature",
    issue_number="JIRA-789"
)

print(f"Create branch: git checkout -b {branch.data['branch_name']}")

# 2. (Make changes...)

# 3. Analyze and commit
changes = analyze_changes()
print(f"Changed {changes.data['total_files_changed']} files")

commit = generate_commit_message()
print(f"Commit message:\n{commit.data['commit_message']}")

# git commit -m "{commit.data['commit_message']}"

# 4. Create PR
pr = create_pull_request(base_branch="develop")
print(f"PR Title: {pr.data['title']}")
print(f"PR Body:\n{pr.data['body']}")
```

### Workflow 2: Hotfix

```python
# Urgent production fix
branch = suggest_branch_name(
    description="fix security vulnerability",
    branch_type="hotfix",
    issue_number="SEC-123"
)

# git checkout -b {branch.data['branch_name']}
# (Make fix...)

# Generate commit with breaking flag if needed
commit = generate_commit_message(
    commit_type="fix",
    scope="security",
    breaking=False
)

# Expedited PR to main
pr = create_pull_request(base_branch="main")
```

---

## Performance Notes

### Execution Time

| Operation | Typical Time | Depends On |
|-----------|--------------|------------|
| analyze_changes | 0.1-0.5s | Repository size, # changes |
| generate_commit_message | 0.2-0.6s | # staged files |
| suggest_branch_name | <0.1s | String processing only |
| create_pull_request | 0.3-0.8s | Commit history, files changed |

### Token Usage

| Operation | Token Usage | Notes |
|-----------|-------------|-------|
| analyze_changes | 300-800 | Depends on # files |
| generate_commit_message | 200-500 | Includes body and footer |
| suggest_branch_name | 100-200 | Lightweight |
| create_pull_request | 400-1000 | Full PR description |

---

## Related Skills

- **pr_review_assistant** - Review PRs created by this skill
- **test_orchestrator** - Run tests before committing
- **code_analysis** - Deeper analysis of code changes

---

## Dependencies

### Required

- Python 3.8+
- Git 2.20+

### Optional

- GitHub CLI (for `gh pr create`)
- GitLab CLI (for `glab mr create`)

---

*Last Updated: 2025-11-08*

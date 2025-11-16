---
name: git-workflow-assistant
description: Git automation specialist for branch management, conventional commits, and workflow automation
version: 0.1.0
category: development
tags:
  - git
  - version-control
  - automation
  - commits
  - branches
  - pull-requests
activation: manual
tools:
  - Read
  - Bash
dependencies: []
---

# Git Workflow Assistant

Intelligent Git workflow automation providing conventional commits, branch naming, change analysis, and PR creation following best practices.

---

## When to Use This Skill

Use git-workflow-assistant when you need to:

- **Generate commit messages** - Conventional commits from staged changes
- **Create branches** - Following naming conventions (GitFlow, GitHub Flow, etc.)
- **Analyze changes** - Understand what's been changed before committing
- **Create pull requests** - With auto-generated descriptions
- **Automate Git workflows** - Standardize team Git practices

**Don't use for:**
- Low-level git commands (use Bash directly)
- Git learning/teaching (use git-workflow-expert agent)
- Manual git operations

---

## Quick Start

```python
from skills.git_workflow_assistant.operations import generate_commit_message

# Generate conventional commit message from staged changes
result = generate_commit_message()

if result.success:
    message = result.data['commit_message']
    print(f"Suggested commit:\n{message}")

    # Use the message
    # git commit -m "{message}"
```

---

## Operations

### analyze_changes
Analyze staged and unstaged changes in a git repository.

**Returns:** File changes, statistics, and change categorization

### generate_commit_message
Generate conventional commit message from staged changes.

**Returns:** Formatted commit message following conventions

### suggest_branch_name
Suggest branch name following conventions.

**Returns:** Branch name following GitFlow, GitHub Flow, or GitLab Flow

### create_pull_request
Create pull request with auto-generated description.

**Returns:** PR details with title, body, and metadata

---

## Conventional Commits

Generates commit messages following the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types:**
- **feat** - New feature
- **fix** - Bug fix
- **docs** - Documentation changes
- **style** - Code style (formatting, semicolons, etc.)
- **refactor** - Code refactoring
- **perf** - Performance improvements
- **test** - Test changes
- **build** - Build system changes
- **ci** - CI/CD changes
- **chore** - Maintenance tasks

**Breaking Changes:**
- Adds `BREAKING CHANGE:` footer
- Adds `!` after type/scope: `feat!:` or `feat(api)!:`

---

## Branching Strategies

Supports multiple branching strategies:

**GitFlow:**
- `feature/description`
- `bugfix/description`
- `hotfix/description`
- `release/version`

**GitHub Flow:**
- `description` (simple descriptive names)
- `username/description`

**GitLab Flow:**
- `feature/description`
- `bugfix/description`
- Includes environment branches (staging, production)

---

## Token Efficiency

**Uses Read and Bash tools** - Low to moderate token usage

**Tip:** Most operations are lightweight:
```python
# Analyze changes: ~300-800 tokens
analyze_changes()

# Generate commit: ~200-500 tokens
generate_commit_message()

# Suggest branch: ~100 tokens
suggest_branch_name("add user auth")
```

---

## Security

**Safety Level:** Medium (uses Bash for git commands)

**Safe because:**
- Read-only for analysis operations
- Git commands are well-defined and safe
- No destructive operations without explicit intent
- Works within git's safety mechanisms

**Audit focus:**
- Git bash commands
- Repository access patterns
- Branch/commit operations

See `../SECURITY.md` for details.

---

## Documentation

**For complete API reference:** See `reference.md`
- Full operation signatures
- All parameters and return values
- Conventional commit formats
- Branching strategy details
- Error codes and handling

**For usage examples:** See `examples.md`
- 9 real-world scenarios
- Automated commit workflows
- Branch management patterns
- PR automation examples

---

## Common Patterns

### Pattern 1: Automated Commit
```python
# Analyze, generate, commit
changes = analyze_changes()
commit_msg = generate_commit_message()

# git commit -m "{commit_msg.data['commit_message']}"
```

### Pattern 2: Feature Branch Creation
```python
# Suggest branch name for new feature
branch = suggest_branch_name(
    description="add user authentication",
    branch_type="feature"
)

# git checkout -b {branch.data['branch_name']}
```

### Pattern 3: PR Creation
```python
# Create PR with auto-generated description
pr = create_pull_request(base_branch="main")

# PR ready to submit
```

---

## Related Skills

- **pr_review_assistant** - Review PRs created by this skill
- **test_orchestrator** - Run tests before committing
- **code_analysis** - Analyze changes before committing

---

## Quick Reference

**Analyze changes:**
```python
analyze_changes(repo_path=".", include_unstaged=False)
```

**Generate commit:**
```python
generate_commit_message(commit_type="feat", scope="auth", breaking=False)
```

**Suggest branch:**
```python
suggest_branch_name(description="fix login bug", branch_type="bugfix")
```

**Create PR:**
```python
create_pull_request(base_branch="main")
```

---

*Last Updated: 2025-11-08*

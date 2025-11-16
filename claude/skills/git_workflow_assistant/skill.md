---
name: git-workflow-assistant
version: 0.1.0
description: Intelligent git workflow automation including commit messages, branch management, and PR creation
category: developer-productivity
author: Claude Code Skills
tools:
  - Bash
  - Read
dependencies: []
tags: [git, version-control, workflow, commits, branches, pull-requests]
operations:
  analyze_changes: "Analyze staged and unstaged changes in a git repository"
  generate_commit_message: "Generate conventional commit message from staged changes"
  suggest_branch_name: "Suggest branch name following conventions"
  create_pull_request: "Create pull request with generated description"
---

# Git Workflow Assistant

## Overview

Git Workflow Assistant automates and streamlines git workflows by analyzing repository state, generating meaningful commit messages, managing branches according to best practices, and automating pull request creation.

## Capabilities

### 📊 Repository Analysis
- Analyze staged changes and uncommitted work
- Identify change patterns and impact
- Detect breaking changes
- Calculate change statistics
- Identify affected modules and files

### ✍️ Commit Message Generation
- Generate conventional commit messages automatically
- Follow semantic commit conventions (feat, fix, docs, etc.)
- Include scope and breaking change indicators
- Add detailed descriptions from diffs
- Support custom commit templates

### 🌿 Branch Management
- Suggest branch names from ticket/issue
- Validate branch naming conventions
- Manage GitFlow, GitHub Flow, GitLab Flow
- Track branch lifecycle
- Detect stale branches

### 🔄 Pull Request Automation
- Generate PR titles and descriptions
- Extract changes and create summaries
- Add labels and reviewers automatically
- Link to related issues
- Generate checklists

### 📋 Workflow Templates
- Support multiple branching strategies
- Customizable commit templates
- PR description templates
- Release workflow automation
- Hotfix workflows

## Operations

### analyze_changes
Analyze staged and unstaged changes.

**Input:**
```python
{
    'repo_path': str,           # Path to git repository
    'include_unstaged': bool    # Include unstaged changes
}
```

**Output:**
```python
{
    'staged_files': [str],
    'unstaged_files': [str],
    'change_type': str,         # 'feature', 'fix', 'docs', etc.
    'breaking_changes': [str],
    'impact_level': str,        # 'low', 'medium', 'high'
    'statistics': dict
}
```

### generate_commit_message
Generate conventional commit message.

**Input:**
```python
{
    'repo_path': str,           # Path to repository
    'commit_type': str,         # Optional: override detected type
    'scope': str,               # Optional: commit scope
    'breaking': bool            # Is breaking change
}
```

**Output:**
```python
{
    'message': str,             # Complete commit message
    'type': str,                # Commit type (feat, fix, etc.)
    'scope': str,               # Commit scope
    'description': str,         # Short description
    'body': str,                # Detailed body
    'footer': str               # Footer with breaking changes
}
```

### suggest_branch_name
Suggest branch name from context.

**Input:**
```python
{
    'issue_number': str,        # Issue/ticket number
    'description': str,         # Brief description
    'branch_type': str,         # 'feature', 'bugfix', 'hotfix'
    'strategy': str             # 'gitflow', 'github-flow', 'gitlab-flow'
}
```

**Output:**
```python
{
    'branch_name': str,         # Suggested branch name
    'base_branch': str,         # Branch to branch from
    'strategy': str             # Applied strategy
}
```

### create_pull_request
Generate PR content.

**Input:**
```python
{
    'repo_path': str,           # Path to repository
    'source_branch': str,       # Source branch
    'target_branch': str,       # Target branch
    'template': str             # Optional PR template
}
```

**Output:**
```python
{
    'title': str,               # PR title
    'description': str,         # PR description
    'labels': [str],            # Suggested labels
    'reviewers': [str],         # Suggested reviewers
    'checklist': [str]          # PR checklist items
}
```

## Integration

Works with other skills:
- **pr-review-assistant**: Validate PR quality
- **code-search**: Find related changes
- **test-orchestrator**: Ensure tests exist
- **doc-generator**: Update documentation

## Usage Example

```python
from git_workflow_assistant import (
    analyze_changes,
    generate_commit_message,
    suggest_branch_name,
    create_pull_request
)

# Analyze current changes
analysis = analyze_changes(repo_path='.')
print(f"Change type: {analysis['change_type']}")
print(f"Impact: {analysis['impact_level']}")

# Generate commit message
commit = generate_commit_message(repo_path='.')
print(f"Commit message:\n{commit['message']}")

# Suggest branch name
branch = suggest_branch_name(
    issue_number='PROJ-123',
    description='Add user authentication',
    branch_type='feature'
)
print(f"Branch: {branch['branch_name']}")

# Create PR content
pr = create_pull_request(
    repo_path='.',
    source_branch='feature/auth',
    target_branch='main'
)
print(f"PR Title: {pr['title']}")
```

## Commit Conventions

Supports semantic commit format:

```
<type>(<scope>): <description>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code refactoring
- `test`: Add tests
- `chore`: Maintenance

## Branch Strategies

### GitFlow
- `main`: Production
- `develop`: Development
- `feature/*`: Features
- `release/*`: Releases
- `hotfix/*`: Hotfixes

### GitHub Flow
- `main`: Production
- `feature/*`: All changes

### GitLab Flow
- `main`: Production
- `feature/*`: Features
- `production`: Deployment

# Git Workflow Assistant

## Overview

Git Workflow Assistant is a skill that automates and streamlines git workflows by analyzing repository state, generating meaningful commit messages, managing branches according to best practices, and automating pull request creation.

## Features

### Commit Message Generation
- Analyzes staged changes to understand context
- Generates conventional commit messages (feat, fix, docs, etc.)
- Follows commit message best practices
- Includes appropriate scope and description

### Branch Management
- Suggests branch names following conventions
- Supports feature/, bugfix/, hotfix/, release/ prefixes
- Kebab-case formatting for consistency

### Pull Request Automation
- Generates comprehensive PR descriptions
- Includes change summary, testing notes, and impact analysis
- Links related issues automatically

### Change Analysis
- Examines staged and unstaged changes
- Categorizes changes by type (features, fixes, refactoring)
- Provides structured analysis for decision-making

## Operations

### `analyze_changes`
Analyzes the current state of the git repository including staged and unstaged changes.

**Parameters:**
- `repo_path` (optional): Path to git repository (defaults to current directory)
- `include_unstaged` (bool): Include unstaged changes in analysis

**Returns:**
```python
{
  "staged": {...},
  "unstaged": {...},
  "summary": "..."
}
```

### `generate_commit_message`
Generates a conventional commit message based on staged changes.

**Parameters:**
- `repo_path` (optional): Path to git repository
- `style` (optional): Commit message style ("conventional", "angular", "simple")

**Returns:**
```python
{
  "message": "feat(auth): add OAuth2 login support",
  "body": "...",
  "type": "feat",
  "scope": "auth"
}
```

### `suggest_branch_name`
Suggests an appropriate branch name based on current work or issue description.

**Parameters:**
- `description`: Description of the work
- `issue_number` (optional): Related issue number
- `type` (optional): Branch type ("feature", "bugfix", "hotfix", "release")

**Returns:**
```python
{
  "branch_name": "feature/add-oauth2-login",
  "full_name": "feature/123-add-oauth2-login"
}
```

### `create_pull_request`
Creates a pull request with an auto-generated description.

**Parameters:**
- `repo_path` (optional): Path to git repository
- `base_branch`: Target branch (e.g., "main", "develop")
- `title` (optional): PR title (auto-generated if not provided)
- `draft` (bool): Create as draft PR

**Returns:**
```python
{
  "pr_url": "https://github.com/user/repo/pull/42",
  "pr_number": 42,
  "description": "..."
}
```

## Usage Examples

### Example 1: Generate Commit Message

```python
from skills.git_workflow_assistant.operations import generate_commit_message

result = generate_commit_message(
    repo_path="/path/to/repo",
    style="conventional"
)

if result.success:
    print(f"Suggested commit: {result.data['message']}")
```

### Example 2: Branch Name Suggestion

```python
from skills.git_workflow_assistant.operations import suggest_branch_name

result = suggest_branch_name(
    description="Add user authentication with OAuth2",
    issue_number=123,
    type="feature"
)

if result.success:
    print(f"Suggested branch: {result.data['branch_name']}")
```

### Example 3: Analyze Changes

```python
from skills.git_workflow_assistant.operations import analyze_changes

result = analyze_changes(
    repo_path="/path/to/repo",
    include_unstaged=True
)

if result.success:
    print(f"Change summary: {result.data['summary']}")
```

## Integration with Agents

Teaching agents and development coordinators can use this skill to:
- Guide students through proper git workflows
- Automate repetitive git tasks
- Enforce commit message conventions
- Streamline PR creation process
- Teach version control best practices

## Dependencies

- Git must be installed and accessible in PATH
- Repository must be a valid git repository
- User must have appropriate git credentials configured

## Error Handling

All operations return `OperationResult` objects with:
- `success`: Boolean indicating operation success
- `data`: Operation-specific return data
- `error`: Error message if operation failed
- `error_code`: Standardized error code
- `duration`: Operation execution time

Common error codes:
- `NOT_A_GIT_REPO`: Path is not a git repository
- `NO_STAGED_CHANGES`: No changes staged for commit
- `GIT_ERROR`: Git command failed
- `VALIDATION_ERROR`: Invalid parameters

## Best Practices

1. **Commit Messages**: Follow conventional commit format
2. **Branch Names**: Use descriptive kebab-case names with type prefixes
3. **Pull Requests**: Include comprehensive descriptions with testing notes
4. **Change Analysis**: Review changes before committing

## Version History

- **v0.1.0**: Initial release with core git workflow automation

## License

Part of the Claude Code Skills ecosystem.

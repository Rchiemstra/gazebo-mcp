# Git Integration for Learning Sessions

The Claude Learning System includes automatic Git integration that creates branches for each learning project and commits/pushes changes after each phase completion.

## Overview

When enabled, the system automatically:

1. **Creates a Git branch** for each new learning session
2. **Tracks the branch** in the session metadata
3. **Checks out the branch** when continuing a session
4. **Commits changes** after each phase is completed
5. **Pushes to remote** automatically (optional)

## Features

### Automatic Branch Creation

When you start a new learning session, a Git branch is automatically created with the format:

```
learning/<topic>-<session-id>
```

For example:
- `learning/python-decorators-a3b4c5d6`
- `learning/ros2-navigation-7e8f9g0h`
- `learning/async-programming-1a2b3c4d`

### Branch Switching

When you continue a session, the system automatically checks out the associated branch:

```python
# Start session 1
session1 = await client.start_learning_session(topic="Async Programming")
# Creates and checks out: learning/async-programming-abc123

# Start session 2
session2 = await client.start_learning_session(topic="Testing")
# Creates and checks out: learning/testing-def456

# Continue session 1
await client.continue_session(session1, "What is asyncio?")
# Automatically checks out: learning/async-programming-abc123
```

### Phase Commits

After completing each learning phase, the system creates a structured commit:

```
Learning Progress: Python Decorators - Phase 1

Completed: research
Timestamp: 2025-10-11 14:30

Learned fundamentals of Python decorators and common use cases

---
Auto-committed by Claude Learning System
```

### Automatic Push

If configured, commits are automatically pushed to the remote repository after each phase.

## Configuration

### Environment Variables

```bash
# Enable/disable Git integration
CLAUDE_ENABLE_GIT=true

# Auto-create branch for each session
CLAUDE_AUTO_CREATE_BRANCH=true

# Auto-commit after phase completion
CLAUDE_AUTO_COMMIT=true

# Auto-push commits to remote
CLAUDE_AUTO_PUSH=true

# Optional: Override Git author
GIT_AUTHOR_NAME=Your Name
GIT_AUTHOR_EMAIL=your.email@example.com
```

### Programmatic Configuration

```python
from claude_learning import AgentClient, AgentConfig

# Option 1: Use environment variables
config = AgentConfig.from_env()
client = AgentClient(config)

# Option 2: Override settings
config = AgentConfig.from_env()
config.enable_git = True
config.auto_create_branch = True
config.auto_commit = True
config.auto_push = False  # Don't auto-push
client = AgentClient(config)

# Option 3: Full manual configuration
config = AgentConfig(
    enable_git=True,
    auto_create_branch=True,
    auto_commit=True,
    auto_push=True,
    git_author_name="Claude Learning",
    git_author_email="learning@example.com",
)
client = AgentClient(config)
```

## Usage Examples

### Basic Workflow

```python
import asyncio
from claude_learning import AgentClient, AgentType, LearningPhase

async def main():
    client = AgentClient.from_env()

    # Start session - creates branch
    session = await client.start_learning_session(
        topic="Python Decorators",
        agent_type=AgentType.PYTHON_BEST_PRACTICES,
        initial_phase=LearningPhase.RESEARCH,
    )

    print(f"Branch: {session.git_branch}")

    # Do research work...
    await client.continue_session(session, "Explain decorators")

    # Complete research phase - commits and pushes
    await client.complete_phase(
        session=session,
        phase=LearningPhase.RESEARCH,
        summary="Learned decorator fundamentals and use cases",
    )

    # Move to design phase
    await client.continue_session(
        session=session,
        prompt="Design a timing decorator",
        update_phase=LearningPhase.DESIGN,
    )

    # Complete design phase - commits and pushes
    await client.complete_phase(
        session=session,
        phase=LearningPhase.DESIGN,
        summary="Designed timing decorator with context manager",
    )

asyncio.run(main())
```

### Multiple Sessions with Branch Switching

```python
# Create first session
session1 = await client.start_learning_session(
    topic="Async Programming",
)
# On branch: learning/async-programming-abc123

# Create second session (switches branch)
session2 = await client.start_learning_session(
    topic="Testing Strategies",
)
# On branch: learning/testing-strategies-def456

# Continue first session (automatically switches back)
await client.continue_session(session1, "Explain async/await")
# Automatically checked out: learning/async-programming-abc123

# Continue second session (switches again)
await client.continue_session(session2, "What is TDD?")
# Automatically checked out: learning/testing-strategies-def456
```

### Manual Phase Completion

```python
# Complete a phase manually
success = await client.complete_phase(
    session=session,
    phase=LearningPhase.IMPLEMENT,
    summary="Implemented decorator with logging and error handling",
)

if success:
    print("Phase committed and pushed successfully")
    print(f"Total commits: {len(session.phase_commits)}")
else:
    print("Phase commit failed")
```

### Check Session Commit History

```python
# View commit history
for commit in session.phase_commits:
    print(f"Phase: {commit['phase']}")
    print(f"Time: {commit['timestamp']}")
    print(f"Hash: {commit.get('commit_hash', 'N/A')}")
    print()
```

## Branch Naming

Branches are automatically named using:
1. Prefix: `learning/`
2. Topic: Sanitized version of the learning topic
3. Session ID: First 8 characters of the session UUID

The topic is sanitized by:
- Converting to lowercase
- Replacing spaces with hyphens
- Removing special characters

Examples:
- "Python Decorators" → `learning/python-decorators-a3b4c5d6`
- "ROS2 Navigation!" → `learning/ros2-navigation-7e8f9g0h`
- "C++ Best Practices" → `learning/c-best-practices-1a2b3c4d`

## Commit Message Format

Phase completion commits use this format:

```
Learning Progress: <topic> - Phase <number>

Completed: <phase-name>
Timestamp: <YYYY-MM-DD HH:MM>

<optional-summary>

---
Auto-committed by Claude Learning System
```

## Requirements

- **Git repository**: Workspace must be initialized as a Git repository
- **Git installed**: Git command-line tool must be available
- **Remote configured** (for auto-push): Remote origin must be set up

## Troubleshooting

### "Not a Git repository" Warning

**Problem**: Git integration enabled but workspace is not a Git repo

**Solution**:
```bash
cd /path/to/workspace
git init
git remote add origin <your-repo-url>
```

### Branch Already Exists

**Problem**: Branch name conflicts with existing branch

**Solution**: The system will checkout the existing branch instead of creating a new one. If you want a fresh branch, delete the old one first:

```bash
git branch -d learning/old-topic-abc123
```

### Failed to Push

**Problem**: Push fails due to authentication or network issues

**Solution**:
1. Configure Git credentials:
   ```bash
   git config --global credential.helper store
   ```

2. Or disable auto-push:
   ```bash
   export CLAUDE_AUTO_PUSH=false
   ```

3. Push manually later:
   ```bash
   git push -u origin learning/your-branch
   ```

### No Changes to Commit

**Problem**: `complete_phase()` reports no changes

**Solution**: This is normal if no files were modified during the phase. The system will skip the commit.

### Permission Denied

**Problem**: Can't push to remote repository

**Solution**:
1. Check SSH keys: `ssh -T git@github.com`
2. Or use HTTPS with credentials
3. Or disable auto-push and push manually

## Disabling Git Integration

### Completely Disable

```bash
export CLAUDE_ENABLE_GIT=false
```

Or in code:
```python
config = AgentConfig.from_env()
config.enable_git = False
```

### Disable Specific Features

```bash
# Keep Git enabled but don't auto-create branches
export CLAUDE_AUTO_CREATE_BRANCH=false

# Keep Git enabled but don't auto-commit
export CLAUDE_AUTO_COMMIT=false

# Keep Git enabled but don't auto-push
export CLAUDE_AUTO_PUSH=false
```

## Best Practices

1. **Use meaningful phase summaries**: Provide clear summaries when completing phases
   ```python
   await client.complete_phase(
       session=session,
       phase=LearningPhase.RESEARCH,
       summary="Researched A* algorithm, compared with Dijkstra, found optimal for grid-based pathfinding"
   )
   ```

2. **Commit regularly**: Use `complete_phase()` after finishing each phase

3. **Review before merging**: When done with a learning session, review the branch before merging:
   ```bash
   git checkout main
   git merge learning/your-topic-abc123
   ```

4. **Clean up branches**: Delete completed learning branches periodically
   ```bash
   git branch -d learning/old-topic-abc123
   git push origin --delete learning/old-topic-abc123
   ```

5. **Use .gitignore**: Exclude temporary files and sensitive data
   ```gitignore
   .env
   __pycache__/
   *.pyc
   .temp/
   ```

## Integration with Slash Commands

When using slash commands like `/create-plan` or `/update-plan`, you can manually commit phases:

```python
# After working on a phase
await client.complete_phase(
    session=current_session,
    phase=LearningPhase.DESIGN,
    summary="Completed system design for navigation component"
)
```

## Examples

See `examples/git_integration_demo.py` for comprehensive examples:

```bash
python examples/git_integration_demo.py
```

## Technical Details

### Git Operations

The system uses subprocess to execute Git commands:
- `git checkout -b <branch>` - Create and checkout branch
- `git add .` - Stage all changes
- `git commit -m "<message>"` - Create commit
- `git push -u origin <branch>` - Push to remote

### Error Handling

- Git errors are logged but don't stop the learning session
- Failed commits/pushes log warnings but allow continuation
- Non-Git workspaces automatically disable Git features

### Performance

- Git operations are asynchronous and non-blocking
- Branch switching is fast (< 100ms typically)
- Commits include all modified files in the workspace

## See Also

- [API_CLI_FALLBACK.md](./API_CLI_FALLBACK.md) - API/CLI mode switching
- [SDK_INTEGRATION.md](./SDK_INTEGRATION.md) - Python SDK integration guide
- [examples/git_integration_demo.py](../examples/git_integration_demo.py) - Working examples

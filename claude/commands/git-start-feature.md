---
name: git-start-feature
description: Create a new feature branch for development work. Sets up Git workflow for new tasks.
example: /git-start-feature stereo-camera
---

# Git Start Feature Command

Creates a new feature branch and sets up the Git workflow for development.

## Usage

```bash
# Create feature branch
/git-start-feature stereo-camera

# Create bug fix branch
/git-start-feature fix/camera-init

# Create refactoring branch
/git-start-feature refactor/motor-control
```

## Branch Naming Conventions

The command supports these branch types:

- `feature/<name>` - New features (default)
- `fix/<name>` - Bug fixes
- `refactor/<name>` - Code refactoring
- `docs/<name>` - Documentation
- `test/<name>` - Testing work
- `experimental/<name>` - Experiments

## What It Does

1. **Validates**: Checks current Git state
2. **Creates Branch**: Creates appropriately named branch
3. **Switches**: Checks out the new branch
4. **Pushes**: Optionally pushes to remote with tracking
5. **Reports**: Confirms setup complete

## Delegation

Delegates to **git-automation-agent** which:
- Checks for uncommitted changes
- Determines base branch (main/master)
- Creates and checks out branch
- Sets up remote tracking
- Reports branch status

## Output Format

```
✅ Feature Branch Created
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Branch: feature/stereo-camera
Base: main
Remote: origin/feature/stereo-camera
Status: Ready for development
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next Steps:
• Make your changes
• Use /git-stage-commit to commit stages
• Create PR when ready
```

## Integration Examples

### With Planning Workflow
```bash
/create-plan "implement stereo camera"
# Plan created

/git-start-feature stereo-camera
# Branch created: feature/stereo-camera

# Work on stages, committing each one
/git-stage-commit
```

### Standalone Feature
```bash
/git-start-feature obstacle-avoidance
# Start working on new feature
```

### Bug Fix
```bash
/git-start-feature fix/camera-timeout
# Fix the bug
/git-stage-commit "fix timeout in camera initialization"
```

## Agent Prompt Template

```
You are working with the git-automation-agent to create a new feature branch.

REQUESTED BRANCH: {branch_name}

Please:
1. Check current Git status
2. Determine appropriate branch type and naming
3. Create and checkout the branch
4. Set up remote tracking (if remote configured)
5. Report branch details and next steps

Handle any uncommitted changes appropriately (stash, warn, or abort).
```

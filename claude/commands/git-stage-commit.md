---
name: git-stage-commit
description: Commit completed development stage with descriptive message. Integrates with development plans and workflows.
example: /git-stage-commit
---

# Git Stage Commit Command

Automatically commits changes for a completed development stage using the git-automation-agent.

## Usage

```bash
# Commit current stage with auto-generated message
/git-stage-commit

# Commit specific stage with custom message
/git-stage-commit "stage 2 - stereo matching implementation"

# Commit with full custom message
/git-stage-commit "feat(perception): add GPU-accelerated stereo matching"
```

## What It Does

1. **Checks Status**: Reviews uncommitted changes
2. **Stages Files**: Adds relevant changed files
3. **Generates Message**: Creates descriptive commit message based on context
4. **Commits**: Creates commit with conventional format
5. **Reports**: Shows commit hash and summary

## Delegation

This command delegates to the **git-automation-agent** which:
- Analyzes changed files
- Generates appropriate commit message
- Follows conventional commit format
- Includes plan/stage context if available
- Handles Git errors gracefully

## Integration with Workflows

### With Development Plans
When working on a multi-stage plan:
```bash
# Start feature
/create-plan "implement stereo camera"
# Creates plan with stages

# Work on stage 1...
/git-stage-commit
# Commits: "feat(perception): stage 1 - camera interface"

# Work on stage 2...
/git-stage-commit
# Commits: "feat(perception): stage 2 - stereo processor"
```

### With Learning Sessions
```bash
/start-learning "ROS2 perception pipeline"
# Work through learning exercises
/git-stage-commit "exercise 1 - basic camera node"
```

### Standalone Usage
```bash
# Fixed a bug
/git-stage-commit "fix camera initialization race condition"

# Completed refactoring
/git-stage-commit "refactor motor control to use strategy pattern"
```

## Output Format

```
✅ Stage Committed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Commit: abc123d
Message: feat(perception): stage 1 - camera interface
Files: 3 changed (src/perception/camera_interface.{hpp,cpp}, tests/)
Branch: feature/stereo-camera
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Smart Features

- **Auto-Detection**: Detects commit type from changed files
- **Scope Inference**: Infers scope from package/directory
- **Stage Tracking**: Includes stage number if working from plan
- **Error Recovery**: Handles common Git issues

## Prompt

When you invoke this command, you should:

1. **Delegate to git-automation-agent**
2. **Provide context**: Current plan stage, task description
3. **Pass user message** if provided
4. **Request commit execution**

## Agent Prompt Template

```
You are working with the git-automation-agent to commit a completed development stage.

CONTEXT:
- Current Task: {task_description}
- Stage: {stage_number} - {stage_name}
- Plan Reference: {plan_file}

USER MESSAGE: {user_provided_message}

Please:
1. Check git status and show changed files
2. Generate appropriate conventional commit message
3. Stage and commit the changes
4. Report the commit details

If the user provided a message, incorporate it appropriately.
Otherwise, generate a descriptive message based on the changed files and context.
```

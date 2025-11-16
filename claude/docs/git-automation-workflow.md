# Git Automation Workflow Guide

Complete guide to using the `git-automation-agent` for automated version control in your development workflow.

## Quick Start

### Basic Workflow
```bash
# 1. Start new feature
/git-start-feature obstacle-detection

# 2. Work on your code...

# 3. Commit your changes
/git-stage-commit

# 4. Continue development...
```

## Integration with Learning Plans

### Automated Plan-Based Development

When working with `/create-plan` and `/continue-plan`, the git-automation-agent can automatically:
- Create feature branches at plan start
- Commit each completed stage with context
- Track progress through Git history
- Generate meaningful commit messages

**Example Flow:**

```bash
# Step 1: Create Learning Plan
/create-plan "implement stereo camera perception"

# Output:
# Plan created: plans/2025-10-05-stereo-camera-learning-plan.md
# Phases:
#   1. Research stereo vision concepts
#   2. Design camera interface
#   3. Implement stereo processor
#   4. Integrate and test

# Step 2: Start Feature Branch
/git-start-feature stereo-camera

# Output:
# ✅ Feature Branch Created
# Branch: feature/stereo-camera
# Base: main
# Status: Ready for development

# Step 3: Work on Phase 1 (Research)
# ... research stereo vision, take notes ...

# Step 4: Commit Research Phase
/git-stage-commit "phase 1 - stereo vision research complete"

# Output:
# ✅ Committed: docs(learning): phase 1 - stereo vision research complete (a1b2c3d)
# Files: docs/stereo-research.md, plans/stereo-camera-learning-plan.md

# Step 5: Work on Phase 2 (Design)
# ... design camera interface ...

# Step 6: Commit Design Phase
/git-stage-commit

# Output (auto-generated from context):
# ✅ Committed: feat(perception): phase 2 - camera interface design (d4e5f6g)
# Files: include/camera_interface.hpp, docs/design-notes.md

# Step 7: Work on Phase 3 (Implementation)
# ... implement stereo processor ...

# Step 8: Commit Implementation
/git-stage-commit

# Output (auto-generated):
# ✅ Committed: feat(perception): phase 3 - stereo processor implementation (h7i8j9k)
# Files: src/stereo_processor.cpp, include/stereo_processor.hpp, tests/
```

## Direct Agent Usage

You can also call the `git-automation-agent` directly for more control:

### Using Task Tool

```
Please use the git-automation-agent to:

1. Check current Git status
2. Create a feature branch named "feature/depth-estimation"
3. Show me the branch details
```

The agent will:
- Validate Git state
- Create and checkout branch
- Set up remote tracking
- Report status

### Complex Operations

```
Please use the git-automation-agent to:

1. Review the changes in src/perception/
2. Create a commit for the stereo matching implementation
3. Use conventional commit format with scope "perception"
4. Include reference to issue #42
5. Push to remote
```

## Commit Message Conventions

The git-automation-agent follows **Conventional Commits** specification:

### Format
```
<type>(<scope>): <short description>

<detailed description>

<footer>
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **refactor**: Code refactoring (no functionality change)
- **docs**: Documentation only
- **test**: Adding or updating tests
- **perf**: Performance improvement
- **chore**: Maintenance tasks
- **build**: Build system changes
- **ci**: CI/CD changes

### Scopes (Package-based)
- **perception**: jetank_perception package
- **motor**: jetank_motor_control package
- **main**: jetank_ros_main package
- **learning**: Learning/documentation work

### Examples

```bash
# New feature
feat(perception): add GPU-accelerated stereo matching

# Bug fix
fix(motor): correct PWM frequency calculation

# Refactoring
refactor(perception): extract camera strategy pattern

# Documentation
docs(learning): add stereo vision research notes

# Tests
test(perception): add stereo processor unit tests

# Performance
perf(perception): optimize point cloud generation
```

## Branch Naming Conventions

### Format
```
<type>/<descriptive-name>
```

### Types
- **feature/**: New features or enhancements
- **fix/**: Bug fixes
- **refactor/**: Code refactoring
- **docs/**: Documentation work
- **test/**: Testing additions
- **experimental/**: Experimental work

### Examples
- `feature/stereo-camera`
- `fix/camera-initialization`
- `refactor/motor-control-architecture`
- `docs/api-documentation`
- `test/integration-tests`
- `experimental/gpu-acceleration`

## Multi-Agent Collaboration

The git-automation-agent integrates seamlessly with other agents:

### With Plan Generation Mentor

```bash
/create-plan "autonomous navigation"
# plan-generation-mentor creates detailed plan

/git-start-feature autonomous-navigation
# git-automation-agent creates branch

# Work through phases, committing each one
# git-automation-agent auto-detects phase context
```

### With ROS2 Learning Mentor

```bash
# Learning to create ROS2 node
/learn-ros2-node camera_publisher

# After implementing
/git-stage-commit
# git-automation-agent: "feat(perception): implement camera publisher node"
```

### With Code Architecture Mentor

```bash
# Refactoring with design patterns
# code-architecture-mentor suggests Strategy pattern

/git-start-feature refactor/camera-strategies

# Implement each strategy
/git-stage-commit "strategy 1 - CSI camera implementation"
/git-stage-commit "strategy 2 - USB camera implementation"
/git-stage-commit "strategy 3 - virtual camera implementation"
```

### With Testing Specialist

```bash
# Add tests for feature
/git-start-feature test/stereo-processor

# Implement tests
/git-stage-commit
# git-automation-agent: "test(perception): add stereo processor unit tests"
```

## Advanced Features

### Automatic Stage Detection

The agent analyzes context to determine:
- Current plan phase/stage
- Package scope from changed files
- Appropriate commit type
- Related issue numbers

**Example:**
```bash
# Working in src/jetank_perception/src/stereo_processor.cpp
/git-stage-commit

# Agent automatically generates:
# "feat(perception): implement stereo processor core algorithm"
```

### Smart File Grouping

The agent groups related changes into logical commits:

```bash
# Changed files:
# - src/camera_interface.hpp
# - src/camera_interface.cpp
# - tests/camera_interface_test.cpp
# - config/camera_params.yaml

# Agent suggests:
# Commit 1: feat(perception): implement camera interface
#   - src/camera_interface.{hpp,cpp}
#   - tests/camera_interface_test.cpp
#
# Commit 2: feat(perception): add camera configuration
#   - config/camera_params.yaml
```

### Error Recovery

The agent handles common Git issues:

**Uncommitted changes when switching branches:**
```
⚠️  Warning: Uncommitted changes detected
Files: config/params.yaml

Options:
1. Stash changes (recommended)
2. Commit changes first
3. Discard changes (dangerous)

Choose option: 1

✅ Changes stashed as stash@{0}
✅ Switched to branch: feature/new-feature
```

**Branch already exists:**
```
❌ Error: Branch 'feature/stereo-camera' already exists
Current branch: main

Options:
1. Switch to existing branch: git checkout feature/stereo-camera
2. Choose different name: /git-start-feature stereo-camera-v2
3. Delete old branch (if merged): git branch -d feature/stereo-camera

What would you like to do?
```

## Best Practices

### 1. Atomic Commits
Each commit should represent **one logical change**:

✅ **Good:**
```bash
/git-stage-commit "add camera initialization"
/git-stage-commit "add error handling for camera failures"
/git-stage-commit "add unit tests for camera interface"
```

❌ **Bad:**
```bash
/git-stage-commit "various camera changes and tests and docs"
```

### 2. Meaningful Messages
Explain **WHY**, not just **WHAT**:

✅ **Good:**
```
fix(perception): correct camera initialization sequence

Camera was initialized before GPIO setup, causing
intermittent failures on Jetson platform. Now GPIO
is configured first, ensuring stable camera access.

Fixes: #42
```

❌ **Bad:**
```
fix camera
```

### 3. Regular Commits
Commit **frequently** at logical checkpoints:
- After completing a function
- After adding tests
- After completing a stage/phase
- Before switching context

### 4. Branch Hygiene
- Create new branch for each feature/fix
- Delete merged branches
- Keep branch names descriptive
- Don't accumulate stale branches

### 5. Never Force Push
Avoid `git push --force` on shared branches:
- Breaks collaboration
- Loses history
- Confuses teammates

## Workflow Patterns

### Pattern 1: Feature Development
```bash
/git-start-feature <feature-name>
# Develop feature in stages
/git-stage-commit # after each stage
# When complete, create PR
```

### Pattern 2: Bug Fix
```bash
/git-start-feature fix/<bug-description>
# Fix the bug
/git-stage-commit "fix: <description>"
# Push and create PR
```

### Pattern 3: Learning Journey
```bash
/create-plan <learning-topic>
/git-start-feature <topic>
# Work through plan phases
/git-stage-commit # after each phase
/update-plan # update learning progress
```

### Pattern 4: Refactoring
```bash
/git-start-feature refactor/<component>
# Refactor in small steps
/git-stage-commit # after each refactor step
# Ensure tests pass between commits
```

### Pattern 5: Experimentation
```bash
/git-start-feature experimental/<experiment>
# Try experimental approach
/git-stage-commit # save progress
# If successful, clean up and merge
# If failed, abandon branch
```

## Troubleshooting

### Issue: "uncommitted changes" error
**Solution:** Commit or stash changes before creating branch
```bash
/git-stage-commit
# or manually: git stash
```

### Issue: "branch already exists"
**Solution:** Either switch to it or choose new name
```bash
git checkout existing-branch
# or
/git-start-feature different-name
```

### Issue: "merge conflict"
**Solution:** Agent guides through resolution
```
⚠️  Merge conflict in src/camera_interface.cpp

Conflicting changes from:
- Your branch: feature/stereo-camera
- Target branch: main

Run: git status
Edit conflicting files
Then: git add <resolved-files>
Finally: /git-stage-commit "merge: resolve camera interface conflicts"
```

### Issue: Need to amend last commit
**Solution:** Only if not pushed
```bash
# Make additional changes
git add <files>
git commit --amend --no-edit
# Warning: Only do this if you haven't pushed!
```

## Summary

The **git-automation-agent** provides:

✅ **Automated branch management**
✅ **Smart commit message generation**
✅ **Context-aware Git operations**
✅ **Integration with learning workflows**
✅ **Error handling and recovery**
✅ **Conventional commit compliance**
✅ **Multi-agent collaboration**

Use it to:
- Maintain clean Git history
- Track learning progress
- Automate repetitive Git tasks
- Follow best practices consistently
- Integrate version control with development plans

**Remember:** Git is not just about saving code - it's about documenting your learning and development journey! 🚀

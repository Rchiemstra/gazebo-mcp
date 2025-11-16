# Quick Reference Card

## Setup & Maintenance

| Task | Command | Notes |
|------|---------|-------|
| **Install globally** | `./install.sh` | One-time setup |
| **Update skills** | `./update.sh skills` | After editing Python code |
| **Update settings** | `./update.sh settings` | Sync global settings |
| **Full update check** | `./update.sh` | After git pull |
| **Test installation** | `./test-installation.sh` | Verify everything works |
| **Uninstall** | `./uninstall.sh` | Remove global installation |

## File Changes - What Needs Updating?

| You Changed | Action Required | Reason |
|-------------|-----------------|--------|
| `.claude/agents/*.md` | ✅ None | Auto-updates (symlinked) |
| `.claude/commands/*.md` | ✅ None | Auto-updates (symlinked) |
| `.claude/agent-registry.json` | ✅ None | Auto-updates (symlinked) |
| `skills/*/*.py` | ⚠️ Run `./update.sh skills` | Python package needs reinstall |
| `.claude/settings.local.json` | ⚠️ Run `./update.sh settings` | Settings are copied, not linked |
| Added new agent | ✅ None | Immediately available |
| Added new command | ✅ None | Immediately available |
| Added new skill | ⚠️ Run `./update.sh skills` | Package needs update |

## Common Workflows

### Edit an Agent
```bash
vim .claude/agents/ros2-learning-mentor.md
# Restart Claude Code - that's it!
```

### Edit a Skill
```bash
vim skills/code_analysis/analyzer.py
./update.sh skills
# Test and commit
```

### Pull Updates from Git
```bash
git pull origin main
# If skills changed:
./update.sh skills
```

### Add New Feature
```bash
# Create files
vim .claude/agents/new-agent.md
vim .claude/commands/new-command.md
mkdir -p skills/new_skill

# Update if needed
./update.sh skills  # Only if you created a new skill

# Test and commit
```

## File Locations

| Component | Source (Edit Here) | Global Location |
|-----------|-------------------|-----------------|
| Agents | `.claude/agents/` | `~/.config/claude-code/agents/` → |
| Commands | `.claude/commands/` | `~/.config/claude-code/commands/` → |
| Registry | `.claude/agent-registry.json` | `~/.config/claude-code/agent-registry.json` → |
| Settings | `.claude/settings.local.json` | `~/.config/claude-code/settings.json` (copy) |
| Skills | `skills/*/` | Python site-packages (installed) |

**→** = symlink (auto-updates)
**(copy)** = copied file (needs manual sync)

## Available Commands

```bash
/start-learning      # Begin guided learning
/continue-plan       # Resume learning journey
/update-plan         # Track progress
/ask-specialist      # Get expert help
/check-understanding # Verify comprehension
/create-plan         # Generate learning plan
/git-start-feature   # New feature branch
/git-stage-commit    # Commit development stage
```

## Available Agents

```
learning-coordinator           # Master learning orchestrator
plan-generation-mentor        # Educational plan creator
ros2-learning-mentor          # ROS2 teaching specialist
code-architecture-mentor      # Design patterns teacher
robotics-vision-navigator     # Computer vision guide
jetank-hardware-specialist    # Hardware integration teacher
python-best-practices         # Python patterns guide
cpp-best-practices           # C++ patterns guide
debugging-detective          # Debugging methodology
testing-specialist           # Testing strategies
git-workflow-expert          # Git teaching
git-automation-agent         # Git automation
documentation-generator      # Documentation helper
```

## Available Skills

```
code_analysis              # AST-based code analysis
code_search               # Intelligent code search
refactor_assistant        # Code refactoring
test_orchestrator         # Test generation & execution
dependency_guardian       # Dependency management
doc_generator             # Documentation generation
git_workflow_assistant    # Git automation
pr_review_assistant       # PR review automation
learning_analytics        # Learning progress tracking
learning_plan_manager     # Learning plan operations
interactive_diagram       # Visual diagram generation
spec_to_implementation    # Spec to code transformation
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Command not found | Check symlinks: `ls -la ~/.config/claude-code/` |
| Agent not loading | Restart Claude Code completely |
| Skill import error | Run `./update.sh skills` |
| Changes not appearing | Verify you edited files in repository, not global config |
| Wrong repository linked | Run `./update.sh` and choose to relink |

## Git Workflow

```bash
# 1. Make changes
vim .claude/agents/my-agent.md

# 2. Test (restart Claude Code)

# 3. Commit
git add .claude/agents/my-agent.md
git commit -m "Improve my-agent"

# 4. Push
git push origin main

# On another machine:
git pull origin main
# Changes appear automatically for agents/commands!
# For skills:
./update.sh skills
```

## Environment Variables

```bash
# Required for skills Python SDK
export ANTHROPIC_API_KEY="your-key-here"

# Optional: Custom config location
export CLAUDE_CONFIG_DIR="$HOME/.config/claude-code"

# Optional: Add to PATH for easier access
export PATH="$PATH:/path/to/claude_code"
```

## Testing

```bash
# Test installation
./test-installation.sh

# Test specific agent
# (Open Claude Code and try the command/agent)

# Test skills import
python -c "from skills.code_analysis import CodeAnalysisSkill; print('✓')"

# Test skills functionality
cd examples/
python basic_query.py
```

## Documentation

- [INSTALLATION.md](./INSTALLATION.md) - Detailed installation guide
- [UPDATE_GUIDE.md](./UPDATE_GUIDE.md) - Complete update instructions
- [COMMANDS_README.md](./COMMANDS_README.md) - Command documentation
- [docs/](./docs/) - Additional documentation

## Support

- Check symlinks: `ls -la ~/.config/claude-code/`
- Verify package: `pip show claude-learning`
- Test import: `python -c "from skills import *"`
- Full diagnostic: `./test-installation.sh`

---

**Remember:** Most changes auto-update! Only skills need `./update.sh skills`

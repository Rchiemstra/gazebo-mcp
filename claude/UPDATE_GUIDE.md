# Update Guide

How to update your global Claude Code installation after making changes.

## TL;DR - Quick Reference

```bash
# Most updates (agents, commands): No action needed! (auto-update via symlinks)

# After changing Python skills code:
./update.sh skills

# After changing settings:
./update.sh settings

# Full update (check everything):
./update.sh
```

## How Updates Work

Your installation uses **symlinks**, which means most updates happen automatically!

### Component Update Behavior

| Component | Update Method | Action Required |
|-----------|---------------|-----------------|
| **Agents** (`agents/*.md`) | Auto-update | ✓ None - just edit files |
| **Commands** (`commands/*.md`) | Auto-update | ✓ None - just edit files |
| **Agent Registry** | Auto-update | ✓ None - just edit file |
| **Skills** (Python code) | Manual | ⚠️ Run `./update.sh skills` |
| **Settings** | Manual | ⚠️ Run `./update.sh settings` |

## Detailed Update Instructions

### 1. Updating Agents

**Location:** `.claude/agents/*.md`

```bash
# Edit any agent file
nano .claude/agents/ros2-learning-mentor.md

# NO UPDATE NEEDED - Changes are immediately available!
# Just restart Claude Code to pick up changes
```

**Why?** The global config symlinks to your repository:
```
~/.config/claude-code/agents → /path/to/claude_code/.claude/agents
```

### 2. Updating Commands

**Location:** `.claude/commands/*.md`

```bash
# Edit any command file
nano .claude/commands/start-learning.md

# NO UPDATE NEEDED - Changes are immediately available!
# Just restart Claude Code
```

**Why?** Same reason - global config symlinks to your repository.

### 3. Updating Skills (Python Code)

**Location:** `skills/*/*.py`

```bash
# Edit skill code
nano skills/code_analysis/skill.py

# REQUIRED: Reinstall the package
./update.sh skills

# OR manually:
pip install -e . --upgrade
```

**Why?** Python code changes require the package to be reinstalled for changes to take effect, especially if:
- You changed function signatures
- You added new dependencies
- You modified imports

### 4. Updating Settings

**Location:** `.claude/settings.local.json`

```bash
# Edit settings
nano .claude/settings.local.json

# REQUIRED: Sync to global config
./update.sh settings

# This will prompt before overwriting global settings
```

**Why?** Settings are **copied**, not symlinked, because you might want different global vs. local settings.

### 5. Adding New Files

#### New Agent

```bash
# Create new agent
echo "# New Agent" > .claude/agents/my-new-agent.md

# NO UPDATE NEEDED - Immediately available!
```

#### New Command

```bash
# Create new command
echo "# New Command" > .claude/commands/my-command.md

# NO UPDATE NEEDED - Immediately available!
```

#### New Skill

```bash
# Create new skill directory
mkdir -p skills/my_new_skill
echo "class MySkill: pass" > skills/my_new_skill/skill.py

# REQUIRED: Reinstall package
./update.sh skills
```

## Update Workflows

### Scenario 1: Tweaking an Agent's Behavior

```bash
# 1. Edit the agent
vim .claude/agents/code-architecture-mentor.md

# 2. Test immediately (no update needed)
# Open Claude Code and use the agent

# 3. Commit changes
git add .claude/agents/code-architecture-mentor.md
git commit -m "Improve architecture mentor prompts"
```

### Scenario 2: Improving a Skill

```bash
# 1. Edit skill code
vim skills/code_analysis/analyzer.py

# 2. Update installation
./update.sh skills

# 3. Test
python -c "from skills.code_analysis import CodeAnalysisSkill; print('Works!')"

# 4. Commit
git add skills/code_analysis/analyzer.py
git commit -m "Add AST caching to code analyzer"
```

### Scenario 3: Adding New Features

```bash
# 1. Create new agent
cat > .claude/agents/security-scanner.md << 'EOF'
# Security Scanner Agent
...
EOF

# 2. Create new command
cat > .claude/commands/security-scan.md << 'EOF'
# Security Scan Command
...
EOF

# 3. Create new skill
mkdir -p skills/security_scanner
echo "class SecurityScanner: pass" > skills/security_scanner/skill.py

# 4. Update registry
vim .claude/agent-registry.json

# 5. Update skills package
./update.sh skills

# 6. Test and commit
git add .
git commit -m "Add security scanning feature"
```

### Scenario 4: Pulling Updates from Git

```bash
# 1. Pull latest changes
git pull origin main

# 2. Check what changed
git log -1 --stat

# 3. If only agents/commands changed:
#    → No action needed!

# 4. If skills changed:
./update.sh skills

# 5. If settings changed:
./update.sh settings  # Optional, will prompt
```

## Troubleshooting Updates

### Changes Not Appearing

**Problem:** Edited an agent but Claude Code doesn't see changes.

**Solutions:**
1. Restart Claude Code completely
2. Verify symlink is correct:
   ```bash
   ls -la ~/.config/claude-code/agents
   # Should show: ... -> /path/to/your/claude_code/.claude/agents
   ```
3. Check file was saved correctly:
   ```bash
   cat .claude/agents/your-agent.md
   ```

### Skills Import Errors

**Problem:** `ImportError: cannot import name 'MySkill'`

**Solutions:**
1. Reinstall package:
   ```bash
   ./update.sh skills
   ```
2. Check Python path:
   ```bash
   python -c "import sys; print('\n'.join(sys.path))"
   # Should include your claude_code directory
   ```
3. Verify package installation:
   ```bash
   pip show claude-learning
   ```

### Symlink Broken

**Problem:** Symlink points to wrong location or is broken.

**Solution:**
```bash
# Run full update to fix symlinks
./update.sh

# OR manually relink
ln -sf /path/to/claude_code/.claude/agents ~/.config/claude-code/agents
ln -sf /path/to/claude_code/.claude/commands ~/.config/claude-code/commands
```

### Multiple Repositories

**Problem:** You have multiple claude_code clones and global config points to wrong one.

**Solution:**
```bash
# Check current links
ls -la ~/.config/claude-code/

# Relink to desired repository
cd /path/to/desired/repository
./update.sh full

# When prompted about different location, select Yes to relink
```

## Best Practices

1. **Edit in Repository:** Always edit files in your cloned repository, not in `~/.config/claude-code/` directly.

2. **Test Before Commit:**
   ```bash
   # Edit
   vim .claude/agents/my-agent.md

   # Test
   # (Open Claude Code and try it)

   # Commit only after verification
   git add .claude/agents/my-agent.md
   git commit -m "Improve my-agent behavior"
   ```

3. **Skills Development Workflow:**
   ```bash
   # Edit → Update → Test → Commit
   vim skills/my_skill/skill.py
   ./update.sh skills
   python -m pytest tests/test_my_skill.py
   git commit -am "Fix skill bug"
   ```

4. **Keep Repository Clean:**
   ```bash
   # Don't commit local test files
   echo "test_output/" >> .gitignore

   # Don't commit local settings if you customized them
   # (global settings are already gitignored)
   ```

5. **Document Changes:**
   ```bash
   # Update CHANGELOG when adding features
   echo "- Added security-scanner agent" >> CHANGELOG.md
   git add CHANGELOG.md
   ```

## Update Scripts Summary

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `./update.sh` | Full update check | After git pull, general maintenance |
| `./update.sh skills` | Update Python package only | After editing Python code |
| `./update.sh settings` | Sync settings to global | After changing settings |
| `./update.sh agents` | Verify agents (no-op) | Diagnostic only |
| `./update.sh commands` | Verify commands (no-op) | Diagnostic only |

## Integration with Development

### Pre-commit Hook

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash

# Check if skills were modified
if git diff --cached --name-only | grep -q "^skills/"; then
    echo "Skills modified - remember to run: ./update.sh skills"
fi
```

### Makefile

Add to `Makefile`:

```makefile
.PHONY: update update-skills update-all

update:
	@./update.sh

update-skills:
	@./update.sh skills

update-all:
	@git pull origin main
	@./update.sh
```

Usage:
```bash
make update-skills  # Quick skills update
make update-all     # Pull and update everything
```

## Conclusion

Most updates are **automatic** thanks to symlinks!

Only run update scripts when:
- ✓ You modified Python skills code
- ✓ You want to sync settings
- ✓ You pulled major changes from git
- ✓ Something seems broken

Happy coding! 🚀

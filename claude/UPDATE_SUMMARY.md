# Update Summary - Quick Answer

## The Simple Answer

**Q: What if I update the skills, how to update it globally?**

**A: Just run:**
```bash
./update.sh skills
```

That's it! Your changes are now available everywhere you use Claude Code.

## Why?

Your global installation uses **two different technologies**:

1. **Symlinks** (for agents/commands) → Auto-update ✅
2. **Python package** (for skills) → Need manual update ⚠️

## The Complete Picture

### What Auto-Updates (No Action Needed)

When you edit these files, changes appear immediately after restarting Claude Code:

- ✅ `.claude/agents/*.md` - All your agents
- ✅ `.claude/commands/*.md` - All your commands  
- ✅ `.claude/agent-registry.json` - Agent registry

**Why?** These are **symlinked** from `~/.config/claude-code/` to your repository.

### What Needs Manual Update

When you edit these files, you must run `./update.sh skills`:

- ⚠️ `skills/*/*.py` - All Python skill code
- ⚠️ New skill directories
- ⚠️ Changed dependencies

**Why?** Python caches compiled bytecode (`.pyc` files) and needs reinstallation to refresh.

## Common Scenarios

### 1. You tweaked an agent's prompts
```bash
vim .claude/agents/ros2-learning-mentor.md
# ✅ Just restart Claude Code - done!
```

### 2. You fixed a bug in skill code
```bash
vim skills/code_analysis/analyzer.py
./update.sh skills  # ⚠️ Required
# ✅ Now test it
```

### 3. You pulled updates from git
```bash
git pull origin main
# Check what changed:
git log -1 --stat

# If only .claude/ files changed:
# ✅ Just restart Claude Code

# If skills/ changed:
./update.sh skills  # ⚠️ Required
```

### 4. You added a new skill
```bash
mkdir -p skills/my_new_skill
vim skills/my_new_skill/skill.py
./update.sh skills  # ⚠️ Required
```

## Update Commands

| Command | Use When |
|---------|----------|
| `./update.sh` | General update check (recommended after git pull) |
| `./update.sh skills` | You changed Python code in `skills/` |
| `./update.sh settings` | You changed `.claude/settings.local.json` |

## Visual Flow

```
You edit a file
│
├─ File in .claude/agents/ or .claude/commands/?
│  │
│  ├─ YES → ✅ Symlinked
│  │        Just restart Claude Code
│  │
│  └─ NO → Continue...
│
└─ File in skills/*/?
   │
   └─ YES → ⚠️ Python package
            Run: ./update.sh skills
```

## How It Works Behind the Scenes

### Symlinks (Auto-Update)
```bash
# Your file:
~/claude-extensions/claude_code/.claude/agents/my-agent.md

# Global config has a symlink:
~/.config/claude-code/agents/my-agent.md 
    → ~/claude-extensions/claude_code/.claude/agents/my-agent.md

# When you edit your file, the symlink points to the updated file
# Claude Code reads from the symlink location
# So it automatically sees your changes!
```

### Python Package (Manual Update)
```bash
# Editable install points to your repo:
pip install -e ~/claude-extensions/claude_code

# But Python caches compiled bytecode:
skills/__pycache__/my_skill.cpython-39.pyc  # ← OLD CODE CACHED!

# ./update.sh skills does:
pip install -e . --upgrade  # Clears cache, reinstalls
# Now imports use new code!
```

## Troubleshooting

**Problem:** "I edited an agent but don't see changes"
**Solution:** Restart Claude Code completely

**Problem:** "I ran ./update.sh skills but skill changes don't appear"
**Solution:** 
```bash
# Force reinstall:
pip uninstall claude-learning
pip install -e .
```

**Problem:** "Command not found after installation"
**Solution:** 
```bash
# Verify symlinks:
ls -la ~/.config/claude-code/
# Should show symlinks to your repository
```

## Key Files Reference

| File/Directory | Location | Update Method |
|----------------|----------|---------------|
| **Agents** | `.claude/agents/*.md` | Symlink (auto) |
| **Commands** | `.claude/commands/*.md` | Symlink (auto) |
| **Registry** | `.claude/agent-registry.json` | Symlink (auto) |
| **Settings** | `.claude/settings.local.json` | Copy (manual) |
| **Skills** | `skills/*/*.py` | Pip install (manual) |

## Learn More

- [UPDATE_GUIDE.md](./UPDATE_GUIDE.md) - Comprehensive update guide
- [UPDATE_FLOW.md](./UPDATE_FLOW.md) - Visual diagrams
- [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) - Quick reference card

## TL;DR

**Agents/Commands:** Edit and restart = ✅  
**Skills:** Edit, run `./update.sh skills`, then test = ✅

That's all you need to know!

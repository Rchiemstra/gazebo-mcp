# Update Flow Diagram

## How Global Installation Updates

```
┌─────────────────────────────────────────────────────────────┐
│         Your Repository: ~/claude-extensions/claude_code     │
│                                                              │
│  ┌──────────────────┐      ┌──────────────┐                │
│  │ .claude/         │      │ skills/      │                │
│  │  ├── agents/     │      │  ├── code_*/ │                │
│  │  ├── commands/   │      │  ├── test_*/ │                │
│  │  └── registry    │      │  └── ...     │                │
│  └──────────────────┘      └──────────────┘                │
│         ↓ symlink               ↓ pip install -e            │
└─────────────────────────────────────────────────────────────┘
                ↓                           ↓
┌─────────────────────────────────────────────────────────────┐
│      Global Claude Config: ~/.config/claude-code/           │
│                                                              │
│  ┌──────────────────┐      ┌──────────────────────┐        │
│  │ agents/      ──→ │      │ Python site-packages │        │
│  │ commands/    ──→ │      │   claude-learning/   │        │
│  │ registry     ──→ │      │     ├── skills/      │        │
│  │ settings (copy)  │      │     └── ...          │        │
│  └──────────────────┘      └──────────────────────┘        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                ↓
        Claude Code reads from here
```

## Update Scenarios

### Scenario 1: Edit Agent File (Auto-Update)

```
You:  vim ~/claude-extensions/claude_code/.claude/agents/ros2-mentor.md
      ↓
File: Changed in repository
      ↓
Symlink: ~/.config/claude-code/agents/ros2-mentor.md → [points to changed file]
      ↓
Claude Code: Restart to see changes
      ✅ NO ./update.sh NEEDED!
```

### Scenario 2: Edit Skill Code (Manual Update)

```
You:  vim ~/claude-extensions/claude_code/skills/code_analysis/analyzer.py
      ↓
File: Changed in repository
      ↓
Python: Still using OLD cached bytecode
      ⚠️ NEED TO UPDATE!
      ↓
You:  ./update.sh skills
      ↓
Pip:  Reinstalls package, refreshes cache
      ↓
Claude Code: Import now uses new code
      ✅ UPDATED!
```

### Scenario 3: Git Pull (Mixed Update)

```
You:  git pull origin main
      ↓
Git:  Downloads changes
      ├── Changed: agents/my-agent.md       → Auto-updates ✅
      ├── Changed: commands/my-cmd.md       → Auto-updates ✅
      └── Changed: skills/my_skill/code.py  → Needs update ⚠️
      ↓
You:  ./update.sh skills  (or just ./update.sh)
      ↓
All:  Now up to date! ✅
```

## Update Decision Tree

```
Did you change a file?
│
├─ Is it in .claude/agents/ ?
│  └─ YES → ✅ Auto-update (just restart Claude)
│
├─ Is it in .claude/commands/ ?
│  └─ YES → ✅ Auto-update (just restart Claude)
│
├─ Is it .claude/agent-registry.json ?
│  └─ YES → ✅ Auto-update (just restart Claude)
│
├─ Is it in skills/*/*.py ?
│  └─ YES → ⚠️ Run: ./update.sh skills
│
└─ Is it .claude/settings.local.json ?
   └─ YES → ⚠️ Run: ./update.sh settings (optional)
```

## Behind the Scenes

### Symlinks Behavior

```bash
# After installation:
$ ls -la ~/.config/claude-code/agents
lrwxrwxrwx ... agents -> /home/you/claude-extensions/claude_code/.claude/agents

# When you edit:
$ vim /home/you/claude-extensions/claude_code/.claude/agents/my-agent.md

# The symlink makes it appear as if you edited:
# ~/.config/claude-code/agents/my-agent.md

# Claude Code reads from ~/.config/claude-code/agents/my-agent.md
# But the symlink points to your repository file
# So it automatically sees your changes!
```

### Python Package Behavior

```bash
# After installation:
$ pip install -e /home/you/claude-extensions/claude_code

# This creates a link in site-packages:
$ cat $(python -c "import site; print(site.getsitepackages()[0])")/claude-learning.egg-link
/home/you/claude-extensions/claude_code

# When you import:
>>> from skills.code_analysis import CodeAnalysisSkill

# Python:
# 1. Finds claude-learning in site-packages
# 2. Follows egg-link to your repository
# 3. Imports from your repository code
# 4. BUT uses cached .pyc files

# When you edit Python code:
$ vim /home/you/claude-extensions/claude_code/skills/code_analysis/analyzer.py

# Python still uses old .pyc cache!
# Need to reinstall to refresh:
$ ./update.sh skills  # This clears cache and reinstalls
```

## File Type Summary

| File Type | Technology | Update Method |
|-----------|------------|---------------|
| Markdown (agents/commands) | Symlink | Automatic |
| JSON (registry) | Symlink | Automatic |
| JSON (settings) | File copy | Manual sync |
| Python (.py) | Editable install | Manual reinstall |

## Visual: What Happens on ./update.sh skills

```
Before:
Repository:       skills/code_analysis/analyzer.py (NEW CODE ✨)
Site-packages:    skills/code_analysis/__pycache__/analyzer.cpython-39.pyc (OLD)
Import:           Uses OLD cached bytecode ❌

After ./update.sh skills:
↓
pip install -e . --upgrade
↓
Clears __pycache__
Reinstalls package
↓
Repository:       skills/code_analysis/analyzer.py (NEW CODE ✨)
Site-packages:    [cache cleared]
Import:           Compiles NEW code, uses NEW bytecode ✅
```

## Best Practices Visual

```
┌─────────────────────────────────────────────┐
│           Development Workflow              │
└─────────────────────────────────────────────┘

1. EDIT FILES IN REPOSITORY
   ~/claude-extensions/claude_code/
   ├── .claude/agents/my-agent.md  ← Edit here ✅
   └── skills/my_skill/code.py     ← Edit here ✅

   NOT HERE:
   ~/.config/claude-code/
   └── agents/my-agent.md  ← Don't edit here ❌
                             (This is just a symlink!)

2. UPDATE IF NEEDED
   Changed Python?  → ./update.sh skills
   Changed settings? → ./update.sh settings
   Changed agent?    → No action needed!

3. TEST
   Restart Claude Code
   Try your changes

4. COMMIT
   git add .
   git commit -m "Your changes"
   git push
```

## Multi-Machine Workflow

```
Machine A (Desktop)                    Machine B (Laptop)
─────────────────                      ──────────────────

1. git pull                            1. git pull
2. ./install.sh (first time)           2. ./install.sh (first time)
   ↓                                      ↓
   Both machines now share config!        │
   ↓                                      │
3. Edit agent file                        │
4. git push                               │
   ↓                                      │
   ────────────────────────────────────> │
                                          │
                                       5. git pull
                                       6. Restart Claude
                                          ✅ Changes appear!

                                       7. Edit skill code
                                       8. ./update.sh skills
                                       9. git push
   ↓                                      │
   <──────────────────────────────────────
   │
10. git pull
11. ./update.sh skills
    ✅ Changes appear!
```

## Common Patterns

### Daily Development
```
vim .claude/agents/my-agent.md
# Test (restart Claude)
git commit -am "improve prompts"
```

### Skills Development
```
vim skills/my_skill/skill.py
./update.sh skills
pytest tests/test_my_skill.py
git commit -am "fix bug"
```

### Morning Routine
```
cd ~/claude-extensions/claude_code
git pull origin main
./update.sh  # Full check
# Start coding!
```

### After Pulling Updates
```
git log --stat  # See what changed
# If only .claude/ files → Restart Claude
# If skills/ changed → ./update.sh skills
# If both → ./update.sh
```

---

**Key Takeaway:** Symlinks make most updates automatic! Only Python code needs manual updates.

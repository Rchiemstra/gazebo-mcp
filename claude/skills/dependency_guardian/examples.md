# Dependency Guardian - Usage Examples

Real-world usage examples for dependency_guardian skill.

---

## Example 1: Basic Vulnerability Check

**Scenario:** You want to quickly check if your project has any known security vulnerabilities.

```python
from skills.dependency_guardian.operations import check_vulnerabilities

# Quick security scan
result = check_vulnerabilities(".")

if result.success:
    data = result.data

    print(f"Security Scan Results")
    print("=" * 60)
    print(f"Total vulnerabilities: {data['total_vulnerabilities']}")
    print(f"  Critical: {data['critical']}")
    print(f"  High:     {data['high']}")
    print(f"  Medium:   {data['medium']}")
    print(f"  Low:      {data['low']}")
    print()

    if data['total_vulnerabilities'] == 0:
        print("✅ No vulnerabilities found!")
    else:
        print("Affected packages:")
        for vuln in data['vulnerabilities']:
            print(f"  {vuln['package']} {vuln['installed_version']}")
            print(f"    {vuln['severity'].upper()}: {vuln['title']}")
            print(f"    Fix: {vuln['remediation']}")
            print()
else:
    print(f"❌ Scan failed: {result.error}")
```

**Output:**
```
Security Scan Results
============================================================
Total vulnerabilities: 3
  Critical: 1
  High:     1
  Medium:   1
  Low:      0

Affected packages:
  requests 2.25.0
    CRITICAL: Server-side request forgery in requests
    Fix: Upgrade to requests 2.31.0 or later

  urllib3 1.26.5
    HIGH: urllib3 Cookie request header not stripped
    Fix: Upgrade to urllib3 1.26.18 or later

  jinja2 3.0.0
    MEDIUM: Cross-site scripting vulnerability
    Fix: Upgrade to jinja2 3.1.3 or later
```

**Token Usage:** ~2000 tokens (3 vulnerabilities with full details)

---

## Example 2: Focused Security Check (Critical/High Only)

**Scenario:** You're preparing for a release and only want to address critical and high severity issues.

```python
from skills.dependency_guardian.operations import check_vulnerabilities

# Focus on critical and high severity only
result = check_vulnerabilities(".", include_low=False)

if result.success:
    data = result.data

    critical_high = data['critical'] + data['high']

    if critical_high == 0:
        print("✅ No critical or high severity vulnerabilities!")
        print("Safe to proceed with release")
    else:
        print(f"🚨 RELEASE BLOCKED: {critical_high} critical/high vulnerabilities")
        print()

        # Show only critical and high
        for vuln in data['vulnerabilities']:
            if vuln['severity'] in ['critical', 'high']:
                print(f"{vuln['severity'].upper()}: {vuln['package']} {vuln['installed_version']}")
                print(f"  Issue: {vuln['title']}")
                print(f"  CVE: {vuln['cve_id']}")
                print(f"  CVSS: {vuln['cvss_score']}/10")
                print(f"  Fix: {vuln['remediation']}")
                print()

                if vuln.get('exploitability') == 'high':
                    print(f"  ⚠️  Actively exploited in the wild!")
                print()
else:
    print(f"❌ Scan failed: {result.error}")
```

**Output:**
```
🚨 RELEASE BLOCKED: 2 critical/high vulnerabilities

CRITICAL: requests 2.25.0
  Issue: Server-side request forgery in requests
  CVE: CVE-2024-XXXXX
  CVSS: 9.8/10
  Fix: Upgrade to requests 2.31.0 or later

  ⚠️  Actively exploited in the wild!

HIGH: urllib3 1.26.5
  Issue: urllib3 Cookie request header not stripped
  CVE: CVE-2023-45803
  CVSS: 7.5/10
  Fix: Upgrade to urllib3 1.26.18 or later
```

**Token Usage:** ~600 tokens (filtered to critical/high only)

---

## Example 3: Check for Updates

**Scenario:** You want to see which dependencies have available updates.

```python
from skills.dependency_guardian.operations import check_updates

# Check for minor/patch updates (safe, no breaking changes)
result = check_updates(".", include_major=False)

if result.success:
    data = result.data

    print(f"Dependency Update Report")
    print("=" * 60)
    print(f"Total packages: {data['total_packages']}")
    print(f"Up to date: {data['up_to_date']}")
    print(f"Updates available: {data['total_updates']}")
    print()

    if data['total_updates'] == 0:
        print("✅ All dependencies are up to date!")
    else:
        # Categorize updates
        security = [u for u in data['updates'] if u.get('security_fixes')]
        regular = [u for u in data['updates'] if not u.get('security_fixes')]

        if security:
            print(f"🔒 Security Updates ({len(security)}):")
            for update in security:
                print(f"  {update['package']}: {update['current_version']} → {update['latest_version']}")
                print(f"    Action: {update['recommended_action']}")
            print()

        if regular:
            print(f"📦 Regular Updates ({len(regular)}):")
            for update in regular:
                print(f"  {update['package']}: {update['current_version']} → {update['latest_version']} ({update['update_type']})")
            print()
else:
    print(f"❌ Update check failed: {result.error}")
```

**Output:**
```
Dependency Update Report
============================================================
Total packages: 45
Up to date: 37
Updates available: 8

🔒 Security Updates (2):
  requests: 2.28.0 → 2.31.0
    Action: upgrade

  urllib3: 1.26.5 → 1.26.18
    Action: upgrade

📦 Regular Updates (6):
  flask: 2.0.1 → 2.3.0 (minor)
  pytest: 7.1.0 → 7.4.3 (minor)
  black: 22.3.0 → 23.11.0 (minor)
  mypy: 0.950 → 0.991 (patch)
  flake8: 4.0.1 → 6.1.0 (minor)
  isort: 5.10.1 → 5.12.0 (minor)
```

**Token Usage:** ~1200 tokens (8 updates with details)

---

## Example 4: Full Dependency Analysis

**Scenario:** You want a complete overview of your project's dependencies.

```python
from skills.dependency_guardian.operations import analyze_dependencies

# Analyze all dependencies
result = analyze_dependencies(".")

if result.success:
    data = result.data

    print(f"Dependency Analysis: {data['manifest_file']}")
    print("=" * 60)
    print(f"Ecosystem: {data['ecosystem']}")
    print(f"Total dependencies: {data['total_dependencies']}")
    print(f"  Direct: {data['direct_dependencies']}")
    print(f"  Transitive: {data['transitive_dependencies']}")
    print()

    # License summary
    print("License Distribution:")
    for license, count in sorted(data['licenses'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {license}: {count}")
    print()

    # Show direct dependencies
    print(f"Direct Dependencies ({data['direct_dependencies']}):")
    direct_deps = [d for d in data['dependencies'] if d['type'] == 'direct']

    for dep in direct_deps[:10]:  # Show first 10
        print(f"  {dep['name']} {dep['version']}")
        if dep.get('description'):
            print(f"    {dep['description'][:60]}...")
        if dep.get('dependencies'):
            print(f"    → Requires: {', '.join(dep['dependencies'][:3])}")
        print()

    if len(direct_deps) > 10:
        print(f"  ... and {len(direct_deps) - 10} more")
else:
    print(f"❌ Analysis failed: {result.error}")
```

**Output:**
```
Dependency Analysis: requirements.txt
============================================================
Ecosystem: python
Total dependencies: 45
  Direct: 12
  Transitive: 33

License Distribution:
  MIT: 25
  Apache-2.0: 10
  BSD-3-Clause: 8
  Unknown: 2

Direct Dependencies (12):
  requests 2.31.0
    HTTP library for Python
    → Requires: urllib3, certifi, charset-normalizer

  flask 2.3.0
    A simple framework for building complex web applications
    → Requires: werkzeug, jinja2, click

  sqlalchemy 2.0.0
    Database Abstraction Library
    → Requires: greenlet, typing-extensions

  ... and 9 more
```

**Token Usage:** ~2500 tokens (full dependency tree and metadata)

---

## Example 5: CI/CD Security Gate

**Scenario:** Integrate security checks into your CI/CD pipeline to block releases with critical vulnerabilities.

```python
# In .github/workflows/security.yml or similar CI pipeline
import sys
from skills.dependency_guardian.operations import check_vulnerabilities

def security_gate():
    """Fail build on critical/high vulnerabilities."""

    print("🔒 Running dependency security gate...")

    result = check_vulnerabilities(".", include_low=False)

    if not result.success:
        print(f"❌ Security scan failed: {result.error}")
        return 1

    data = result.data

    # Report all findings
    print(f"Scan results: {data['total_vulnerabilities']} vulnerabilities")
    print(f"  Critical: {data['critical']}")
    print(f"  High: {data['high']}")
    print(f"  Medium: {data['medium']}")
    print()

    # Fail on critical
    if data['critical'] > 0:
        print(f"💥 BUILD FAILED: {data['critical']} critical vulnerabilities")
        print("Critical vulnerabilities must be fixed before release!")
        print()

        for vuln in data['vulnerabilities']:
            if vuln['severity'] == 'critical':
                print(f"  {vuln['package']}: {vuln['title']}")
                print(f"    {vuln['remediation']}")
        print()
        return 1

    # Warn on high
    if data['high'] > 0:
        print(f"⚠️  WARNING: {data['high']} high severity vulnerabilities")
        print("Consider fixing before release")
        print()

        for vuln in data['vulnerabilities']:
            if vuln['severity'] == 'high':
                print(f"  {vuln['package']}: {vuln['title']}")
        print()

        # Optional: fail on high too
        # return 1

    # Pass
    print("✅ Security gate passed")
    return 0

if __name__ == "__main__":
    sys.exit(security_gate())
```

**CI Output (Failure):**
```
🔒 Running dependency security gate...
Scan results: 3 vulnerabilities
  Critical: 1
  High: 2
  Medium: 0

💥 BUILD FAILED: 1 critical vulnerabilities
Critical vulnerabilities must be fixed before release!

  requests: Server-side request forgery in requests
    Upgrade to requests 2.31.0 or later

⚠️  WARNING: 2 high severity vulnerabilities
Consider fixing before release

  urllib3: urllib3 Cookie request header not stripped
  jinja2: Cross-site scripting vulnerability

Process exited with code 1
```

---

## Example 6: Weekly Security Report

**Scenario:** Generate a weekly report of dependency health for the team.

```python
from skills.dependency_guardian.operations import (
    analyze_dependencies,
    check_vulnerabilities,
    check_updates
)
from datetime import datetime

def generate_security_report(project_path="."):
    """Generate comprehensive dependency security report."""

    print(f"📊 Dependency Security Report")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
    print()

    # 1. Dependency overview
    deps = analyze_dependencies(project_path)
    if deps.success:
        print(f"📦 Dependencies: {deps.data['total_dependencies']} total")
        print(f"   Direct: {deps.data['direct_dependencies']}")
        print(f"   Transitive: {deps.data['transitive_dependencies']}")
        print()

    # 2. Security vulnerabilities
    vulns = check_vulnerabilities(project_path, include_low=False)
    if vulns.success:
        print(f"🔒 Security Vulnerabilities:")
        if vulns.data['total_vulnerabilities'] == 0:
            print("   ✅ No vulnerabilities found")
        else:
            print(f"   Total: {vulns.data['total_vulnerabilities']}")
            print(f"   Critical: {vulns.data['critical']}")
            print(f"   High: {vulns.data['high']}")
            print(f"   Medium: {vulns.data['medium']}")

            if vulns.data['critical'] > 0 or vulns.data['high'] > 0:
                print()
                print("   Action Required:")
                for vuln in vulns.data['vulnerabilities'][:5]:  # Top 5
                    if vuln['severity'] in ['critical', 'high']:
                        print(f"   - {vuln['package']}: {vuln['remediation']}")
        print()

    # 3. Available updates
    updates = check_updates(project_path, include_major=False)
    if updates.success:
        print(f"🔄 Available Updates:")
        print(f"   Total updates: {updates.data['total_updates']}")
        print(f"   Minor: {updates.data['minor_updates']}")
        print(f"   Patch: {updates.data['patch_updates']}")

        # Security updates
        security_updates = [
            u for u in updates.data['updates']
            if u.get('security_fixes')
        ]

        if security_updates:
            print()
            print(f"   Security Updates ({len(security_updates)}):")
            for update in security_updates:
                print(f"   - {update['package']}: {update['current_version']} → {update['latest_version']}")
        print()

    # 4. Overall health score
    health_score = 100
    if vulns.success:
        health_score -= vulns.data['critical'] * 20
        health_score -= vulns.data['high'] * 10
        health_score -= vulns.data['medium'] * 5
    if updates.success:
        security_update_count = len([u for u in updates.data.get('updates', []) if u.get('security_fixes')])
        health_score -= security_update_count * 5

    health_score = max(0, health_score)

    print(f"📈 Dependency Health Score: {health_score}/100")
    if health_score >= 90:
        print("   ✅ Excellent - dependencies are well maintained")
    elif health_score >= 70:
        print("   ⚠️  Good - some attention needed")
    elif health_score >= 50:
        print("   ⚠️  Fair - security updates recommended")
    else:
        print("   🚨 Poor - immediate action required")

    print()
    print("=" * 70)

# Generate report
generate_security_report(".")
```

**Output:**
```
📊 Dependency Security Report
Generated: 2025-11-08 10:30
======================================================================

📦 Dependencies: 45 total
   Direct: 12
   Transitive: 33

🔒 Security Vulnerabilities:
   Total: 3
   Critical: 1
   High: 2
   Medium: 0

   Action Required:
   - requests: Upgrade to requests 2.31.0 or later
   - urllib3: Upgrade to urllib3 1.26.18 or later

🔄 Available Updates:
   Total updates: 8
   Minor: 6
   Patch: 2

   Security Updates (2):
   - requests: 2.28.0 → 2.31.0
   - urllib3: 1.26.5 → 1.26.18

📈 Dependency Health Score: 50/100
   ⚠️  Fair - security updates recommended

======================================================================
```

---

## Example 7: Smart Update Strategy

**Scenario:** Automatically categorize and prioritize dependency updates.

```python
from skills.dependency_guardian.operations import check_updates

def categorize_updates(project_path="."):
    """Categorize updates by priority and safety."""

    result = check_updates(project_path, include_major=True)

    if not result.success:
        print(f"❌ Failed: {result.error}")
        return

    updates = result.data['updates']

    # Categorize
    critical = []  # Security fixes
    safe = []      # Minor/patch, no breaking changes
    review = []    # Major or breaking changes

    for update in updates:
        if update.get('security_fixes'):
            critical.append(update)
        elif update['update_type'] in ['minor', 'patch'] and not update.get('breaking_changes'):
            safe.append(update)
        else:
            review.append(update)

    # Report
    print("📊 Update Priority Report")
    print("=" * 60)

    if critical:
        print(f"\n🚨 CRITICAL - Apply Immediately ({len(critical)}):")
        for u in critical:
            print(f"  {u['package']}: {u['current_version']} → {u['latest_version']}")
            print(f"    Security fixes included")
        print("\n  Action: Update now and test")

    if safe:
        print(f"\n✅ SAFE - Low Risk ({len(safe)}):")
        for u in safe[:5]:  # Show first 5
            print(f"  {u['package']}: {u['current_version']} → {u['latest_version']} ({u['update_type']})")
        if len(safe) > 5:
            print(f"  ... and {len(safe) - 5} more")
        print("\n  Action: Batch update in next sprint")

    if review:
        print(f"\n⚠️  REVIEW REQUIRED - Breaking Changes ({len(review)}):")
        for u in review:
            print(f"  {u['package']}: {u['current_version']} → {u['latest_version']} (major)")
            if u.get('migration_guide'):
                print(f"    Migration guide: {u['migration_guide']}")
        print("\n  Action: Plan migration, review changelog, test thoroughly")

    print()

categorize_updates(".")
```

**Output:**
```
📊 Update Priority Report
============================================================

🚨 CRITICAL - Apply Immediately (2):
  requests: 2.28.0 → 2.31.0
    Security fixes included
  urllib3: 1.26.5 → 1.26.18
    Security fixes included

  Action: Update now and test

✅ SAFE - Low Risk (6):
  pytest: 7.1.0 → 7.4.3 (minor)
  black: 22.3.0 → 23.11.0 (minor)
  mypy: 0.950 → 0.991 (patch)
  flake8: 4.0.1 → 6.1.0 (minor)
  isort: 5.10.1 → 5.12.0 (minor)

  Action: Batch update in next sprint

⚠️  REVIEW REQUIRED - Breaking Changes (2):
  django: 3.2.0 → 4.2.7 (major)
    Migration guide: https://docs.djangoproject.com/en/4.2/howto/upgrade-version/
  flask-sqlalchemy: 2.5.1 → 3.1.1 (major)

  Action: Plan migration, review changelog, test thoroughly
```

---

## Example 8: Multi-Ecosystem Project

**Scenario:** You have a project with both Python and JavaScript dependencies.

```python
from skills.dependency_guardian.operations import check_vulnerabilities

def check_all_ecosystems(project_path="."):
    """Check all ecosystems in a multi-language project."""

    ecosystems = ["python", "npm"]

    print("🔒 Multi-Ecosystem Security Scan")
    print("=" * 60)

    total_vulns = 0

    for ecosystem in ecosystems:
        print(f"\n{ecosystem.upper()}:")

        result = check_vulnerabilities(
            project_path,
            ecosystem=ecosystem,
            include_low=False
        )

        if result.success:
            data = result.data

            vulns = data['total_vulnerabilities']
            total_vulns += vulns

            if vulns == 0:
                print("  ✅ No vulnerabilities")
            else:
                print(f"  ⚠️  {vulns} vulnerabilities found")
                print(f"     Critical: {data['critical']}, High: {data['high']}, Medium: {data['medium']}")

                # Show critical/high only
                for vuln in data['vulnerabilities']:
                    if vuln['severity'] in ['critical', 'high']:
                        print(f"     - {vuln['package']}: {vuln['title']}")
        else:
            if result.error_code == "FILE_NOT_FOUND":
                print(f"  ℹ️  No {ecosystem} dependencies found")
            else:
                print(f"  ❌ Scan failed: {result.error}")

    print("\n" + "=" * 60)
    print(f"Total vulnerabilities across all ecosystems: {total_vulns}")

    if total_vulns == 0:
        print("✅ All ecosystems are secure")
    else:
        print("⚠️  Action required - see details above")

check_all_ecosystems(".")
```

**Output:**
```
🔒 Multi-Ecosystem Security Scan
============================================================

PYTHON:
  ⚠️  3 vulnerabilities found
     Critical: 1, High: 2, Medium: 0
     - requests: Server-side request forgery in requests
     - urllib3: urllib3 Cookie request header not stripped

NPM:
  ⚠️  2 vulnerabilities found
     Critical: 0, High: 1, Medium: 1
     - axios: Cross-site request forgery vulnerability

============================================================
Total vulnerabilities across all ecosystems: 5
⚠️  Action required - see details above
```

---

## Example 9: Integration with PR Review

**Scenario:** Check dependency changes in a pull request before merging.

```python
from skills.dependency_guardian.operations import (
    check_vulnerabilities,
    check_updates
)

def review_dependency_changes():
    """Review dependency changes in PR."""

    print("🔍 Dependency Change Review")
    print("=" * 60)

    # 1. Check current state for vulnerabilities
    print("\n1. Security check on new dependencies...")
    vulns = check_vulnerabilities(".", include_low=False)

    if vulns.success:
        if vulns.data['total_vulnerabilities'] > 0:
            print(f"   ❌ {vulns.data['total_vulnerabilities']} vulnerabilities introduced!")

            for vuln in vulns.data['vulnerabilities']:
                if vuln['severity'] in ['critical', 'high']:
                    print(f"   {vuln['severity'].upper()}: {vuln['package']} {vuln['installed_version']}")
                    print(f"     {vuln['title']}")
                    print(f"     Action: {vuln['remediation']}")

            print("\n   ⛔ PR REVIEW FAILED - Fix vulnerabilities before merging")
            return False
        else:
            print("   ✅ No vulnerabilities in new dependencies")

    # 2. Check if dependencies are up to date
    print("\n2. Checking if dependencies are current...")
    updates = check_updates(".", include_major=False)

    if updates.success:
        outdated_count = updates.data['total_updates']

        if outdated_count > 0:
            print(f"   ℹ️  {outdated_count} dependencies could be newer")

            security_updates = [
                u for u in updates.data['updates']
                if u.get('security_fixes')
            ]

            if security_updates:
                print(f"   ⚠️  {len(security_updates)} have security fixes available:")
                for u in security_updates:
                    print(f"     - {u['package']}: use {u['latest_version']} instead of {u['current_version']}")
                print("\n   Consider updating to latest secure versions")
            else:
                print("   ℹ️  But no security issues with current versions")
        else:
            print("   ✅ All dependencies are current")

    # 3. Final verdict
    print("\n" + "=" * 60)
    print("✅ PR APPROVED - Dependencies look good")
    return True

# Use in PR review workflow
if __name__ == "__main__":
    import sys
    sys.exit(0 if review_dependency_changes() else 1)
```

**Output (PR with issues):**
```
🔍 Dependency Change Review
============================================================

1. Security check on new dependencies...
   ❌ 2 vulnerabilities introduced!
   CRITICAL: requests 2.25.0
     Server-side request forgery in requests
     Action: Upgrade to requests 2.31.0 or later
   HIGH: urllib3 1.26.5
     urllib3 Cookie request header not stripped
     Action: Upgrade to urllib3 1.26.18 or later

   ⛔ PR REVIEW FAILED - Fix vulnerabilities before merging
```

**Output (Clean PR):**
```
🔍 Dependency Change Review
============================================================

1. Security check on new dependencies...
   ✅ No vulnerabilities in new dependencies

2. Checking if dependencies are current...
   ✅ All dependencies are current

============================================================
✅ PR APPROVED - Dependencies look good
```

---

## Best Practices Summary

### 1. Regular Security Scans
- Run `check_vulnerabilities` daily or on every PR
- Focus on critical/high with `include_low=False`

### 2. Categorize Updates by Risk
- Security updates: Apply immediately
- Minor/patch: Batch in sprints
- Major: Plan migration carefully

### 3. Use in CI/CD
- Fail builds on critical vulnerabilities
- Warn on high severity
- Generate reports for team visibility

### 4. Multi-Ecosystem Support
- Check all ecosystems in mixed projects
- Different ecosystems may have different risk profiles

### 5. Integrate with Workflow
- PR reviews for dependency changes
- Weekly reports for team awareness
- Automated updates for low-risk packages

---

## Token Efficiency Tips

**Filter by severity:**
```python
# Full scan: ~3000 tokens
check_vulnerabilities(".", include_low=True)

# Focused: ~700 tokens
check_vulnerabilities(".", include_low=False)
```

**Limit update scope:**
```python
# All updates: ~2500 tokens
check_updates(".", include_major=True)

# Safe updates only: ~1000 tokens
check_updates(".", include_major=False)
```

**Specify ecosystem:**
```python
# Auto-detect all: ~2000 tokens
check_vulnerabilities(".")

# Specific ecosystem: ~1200 tokens
check_vulnerabilities(".", ecosystem="python")
```

---

## Related Examples

- **pr_review_assistant/examples.md** - PR review integration
- **git_workflow_assistant/examples.md** - Automated dependency update PRs
- **test_orchestrator/examples.md** - Testing after updates

---

*Last Updated: 2025-11-08*

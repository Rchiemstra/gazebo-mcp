# Skill Specification: dependency-guardian

**Skill Name:** dependency-guardian
**Priority:** Tier 1 (High-Impact Core)
**Status:** Design Phase
**Estimated Complexity:** Medium

---

## Overview

The **dependency-guardian** skill provides comprehensive dependency management, security scanning, update recommendations, and license compliance checking across multiple languages and package managers.

### Key Capabilities
- Auto-detect package managers (npm, pip, cargo, go mod, maven, etc.)
- Security vulnerability scanning with severity ratings
- Update suggestions with changelog summaries
- License compliance checking and reporting
- Dependency graph visualization
- Detect unused dependencies
- Breaking change warnings
- Dependency conflict resolution
- Automated security patches

### Differentiation
Unlike basic dependency tools:
- ✅ **Multi-language support** - Works across entire tech stack
- ✅ **Security-first** - Prioritizes vulnerabilities
- ✅ **Intelligent updates** - Understands breaking changes
- ✅ **License compliance** - Prevents legal issues
- ✅ **Automated fixes** - Can auto-patch vulnerabilities
- ✅ **Impact analysis** - Shows what depends on what

---

## When to Use

### Ideal Use Cases
1. **Security Scanning** - Find and fix vulnerabilities
2. **Dependency Updates** - Safely update dependencies
3. **New Project Setup** - Audit initial dependencies
4. **License Compliance** - Ensure legal compliance
5. **Dependency Cleanup** - Remove unused packages
6. **Conflict Resolution** - Fix version conflicts
7. **Supply Chain Security** - Detect malicious packages
8. **Automated Maintenance** - Regular dependency updates

### NOT Suitable For
- ❌ Application-level configuration
- ❌ Runtime dependency injection
- ❌ Package development/publishing

---

## Core Operations

### 1. Security Vulnerability Scanning

**Workflow:**
```
1. Detect package manager
2. Run security audit
3. Analyze vulnerabilities
4. Generate report with fixes
```

**Example Output:**
```
Security Audit Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Found 12 vulnerabilities (3 critical, 4 high, 5 moderate)

CRITICAL (3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📛 CVE-2024-12345 - SQL Injection in pg-promise
   Severity: CRITICAL (CVSS 9.8)
   Affected: pg-promise 10.12.1
   Fixed in: 10.15.0
   Vulnerable path: your-app → pg-promise@10.12.1

   Impact:
   Allows arbitrary SQL execution through unsanitized input

   Recommended Action: UPGRADE IMMEDIATELY
   $ npm install pg-promise@10.15.0

   Breaking Changes: None
   Migration Guide: https://github.com/vitaly-t/pg-promise/releases/v10.15.0

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📛 CVE-2024-23456 - Prototype Pollution in lodash
   Severity: CRITICAL (CVSS 9.1)
   Affected: lodash 4.17.20
   Fixed in: 4.17.21
   Vulnerable paths: (3 dependencies use this)
     - your-app → express@4.18.0 → lodash@4.17.20
     - your-app → async@3.2.0 → lodash@4.17.20
     - your-app → lodash@4.17.20 (direct)

   Impact:
   Allows attackers to modify object prototypes, leading to RCE

   Recommended Action: UPGRADE IMMEDIATELY
   $ npm install lodash@4.17.21

   Breaking Changes: None
   Auto-fix available: ✅ Yes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📛 CVE-2024-34567 - Path Traversal in express-fileupload
   Severity: CRITICAL (CVSS 8.9)
   Affected: express-fileupload 1.3.0
   Fixed in: 1.4.0
   Vulnerable path: your-app → express-fileupload@1.3.0

   Impact:
   Allows arbitrary file write outside intended directory

   Recommended Action: UPGRADE IMMEDIATELY + CODE REVIEW
   $ npm install express-fileupload@1.4.0

   Breaking Changes: API changes required
   ⚠️  Manual code changes needed:
   - useTempFiles option now required
   - Validation of file paths needed

   Migration Guide: https://github.com/.../MIGRATION_1.4.md

HIGH (4)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
... (4 more vulnerabilities)

MODERATE (5)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
... (5 more vulnerabilities)

Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total dependencies: 487
Vulnerable dependencies: 12
Auto-fixable: 8
Require manual intervention: 4

Recommended Actions (Priority Order):
1. ⚡ Auto-fix 8 vulnerabilities: Run `npm audit fix`
2. 🔧 Manually upgrade 4 packages with breaking changes
3. 📝 Review code for breaking changes in express-fileupload
4. ✅ Re-run security audit to verify fixes

Quick Fix Command:
$ npm audit fix --force  # ⚠️  May introduce breaking changes

Safe Fix Command:
$ npm audit fix          # Only safe updates (fixes 8/12)
```

**JSON Output:**
```json
{
  "operation": "security_scan",
  "package_manager": "npm",
  "timestamp": "2025-10-25T10:30:00Z",
  "summary": {
    "total_dependencies": 487,
    "vulnerable_dependencies": 12,
    "critical": 3,
    "high": 4,
    "moderate": 5,
    "low": 0
  },
  "vulnerabilities": [
    {
      "id": "CVE-2024-12345",
      "severity": "critical",
      "cvss_score": 9.8,
      "package": "pg-promise",
      "affected_version": "10.12.1",
      "fixed_version": "10.15.0",
      "title": "SQL Injection vulnerability",
      "description": "Allows arbitrary SQL execution through unsanitized input",
      "vulnerable_paths": [
        "your-app → pg-promise@10.12.1"
      ],
      "fix": {
        "type": "upgrade",
        "command": "npm install pg-promise@10.15.0",
        "auto_fixable": true,
        "breaking_changes": false
      },
      "references": [
        "https://nvd.nist.gov/vuln/detail/CVE-2024-12345",
        "https://github.com/vitaly-t/pg-promise/security/advisories/..."
      ]
    }
  ],
  "recommendations": [
    {
      "priority": 1,
      "action": "auto_fix",
      "command": "npm audit fix",
      "fixes_count": 8,
      "description": "Automatically fix 8 vulnerabilities without breaking changes"
    },
    {
      "priority": 2,
      "action": "manual_upgrade",
      "packages": ["express-fileupload", "..."],
      "description": "Manually upgrade 4 packages with breaking changes"
    }
  ]
}
```

### 2. Dependency Updates

**Smart Update Recommendations:**
```
Dependency Update Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Available Updates: 23 packages

SECURITY UPDATES (Priority: CRITICAL)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. express: 4.17.1 → 4.18.2 (security fix)
   ⚠️  Fixes CVE-2024-29041
   Breaking changes: None
   Changelog highlights:
   - Security: Fix open redirect vulnerability
   - Fix: Improved error handling
   Auto-apply: ✅ Recommended

MAJOR UPDATES (May contain breaking changes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. react: 17.0.2 → 18.2.0 (major)
   ⚠️  BREAKING CHANGES DETECTED
   Breaking changes:
   - Automatic batching behavior changed
   - New concurrent features require code changes
   - ReactDOM.render deprecated (use createRoot)

   Migration effort: Medium (2-4 hours)
   Migration guide: https://react.dev/blog/2022/03/08/react-18-upgrade-guide

   Benefits:
   + Concurrent rendering improvements
   + Automatic batching (performance improvement)
   + New hooks (useId, useTransition, useDeferredValue)

   Risks:
   - May require code changes in 12 components
   - Third-party libraries may not be compatible

   Auto-apply: ❌ Manual review required

3. typescript: 4.9.5 → 5.2.2 (major)
   ⚠️  BREAKING CHANGES DETECTED
   Breaking changes:
   - Stricter type checking
   - Some decorators syntax changes
   - lib.d.ts changes

   Migration effort: Low-Medium (1-2 hours)
   Impact: May require fixing ~15 type errors

   Benefits:
   + Better type inference
   + New features (const type parameters, using declarations)
   + Performance improvements (faster --watch mode)

   Auto-apply: ❌ Requires type checking after update

MINOR/PATCH UPDATES (Safe to apply)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. axios: 1.4.0 → 1.6.2 (minor)
   ✅ No breaking changes
   Changelog highlights:
   - Feature: New timeout configuration options
   - Fix: Better error messages
   - Performance: 15% faster for large payloads
   Auto-apply: ✅ Recommended

5. jest: 29.5.0 → 29.7.0 (patch)
   ✅ No breaking changes
   Changelog highlights:
   - Fix: Memory leak in watch mode
   - Feature: Better TypeScript support
   Auto-apply: ✅ Recommended

... (18 more safe updates)

Dependency Health Score: 72/100
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Factors:
✅ All dependencies have recent updates
✅ No deprecated packages
⚠️  3 dependencies have security vulnerabilities
⚠️  5 dependencies are >2 major versions behind
⚠️  12 dependencies not updated in >1 year

Recommendations:
1. Apply security updates immediately (1 package)
2. Apply safe minor/patch updates (20 packages)
3. Plan upgrade for major versions (react, typescript)
4. Review and remove stale dependencies

Batch Update Commands:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Security fixes only
$ npm update express

# Safe updates (no breaking changes)
$ npm update axios jest lodash ... (20 packages)

# Major updates (requires testing)
$ npm install react@18 react-dom@18
$ npm install typescript@5

Estimated time: 30 minutes (excluding major updates testing)
```

### 3. License Compliance

**License Audit:**
```
License Compliance Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total packages: 487
Unique licenses: 23

LICENSE SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MIT:             312 packages (64.1%)
Apache-2.0:       78 packages (16.0%)
ISC:              45 packages (9.2%)
BSD-3-Clause:     23 packages (4.7%)
BSD-2-Clause:     12 packages (2.5%)
CC0-1.0:           8 packages (1.6%)
Unlicense:         3 packages (0.6%)
⚠️ GPL-3.0:        4 packages (0.8%)  # POTENTIAL ISSUE
⚠️ AGPL-3.0:       1 package  (0.2%)  # POTENTIAL ISSUE
⚠️ Unknown:        1 package  (0.2%)  # REQUIRES REVIEW

COMPLIANCE ISSUES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  COPYLEFT LICENSES DETECTED (5 packages)

1. GPL-3.0 Packages (4):
   - node-jq@1.12.0
   - some-gpl-lib@2.3.1
   - gpl-utility@1.0.0
   - legacy-parser@0.8.2

   ⚠️  GPL-3.0 requires:
   - You must open-source your entire application
   - You must license your code under GPL-3.0
   - Commercial use may be restricted

   Recommendation: Replace with MIT/Apache alternatives
   Alternatives found:
   - node-jq → jq-node (MIT)
   - some-gpl-lib → alternative-lib (Apache-2.0)

2. AGPL-3.0 Package (1):
   - ghostscript.js@1.1.0

   ⚠️  AGPL-3.0 requires:
   - Even SaaS/cloud usage requires source disclosure
   - Stricter than GPL-3.0

   Recommendation: REMOVE if using as SaaS
   Alternative: pdf-lib (MIT)

3. Unknown License (1):
   - custom-internal-package@1.0.0

   ⚠️  No license information found
   Recommendation: Contact package author or remove

LICENSE COMPATIBILITY MATRIX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your project license: MIT

Compatible: ✅ 481 packages (98.8%)
Incompatible: ⚠️ 5 packages (1.0%)
Review needed: ⚠️ 1 package (0.2%)

RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. CRITICAL: Remove AGPL-3.0 package
   $ npm uninstall ghostscript.js
   $ npm install pdf-lib

2. HIGH: Replace GPL-3.0 packages
   $ npm uninstall node-jq some-gpl-lib gpl-utility legacy-parser
   $ npm install jq-node alternative-lib ...

3. MEDIUM: Investigate unknown license
   Check: custom-internal-package@1.0.0

Compliance Score: 62/100
After fixes: 100/100 ✅

Legal Risk: MEDIUM → LOW (after fixes)
```

### 4. Unused Dependency Detection

**Unused Dependencies Report:**
```
Unused Dependencies Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Analyzed: 487 dependencies
Unused: 23 packages (waste: 45.3 MB)

DIRECT DEPENDENCIES (Unused)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. moment (2.29.4) - 2.1 MB
   Last used: Never (added 6 months ago)
   Possible reason: Replaced with date-fns
   Safe to remove: ✅ Yes

   $ npm uninstall moment

2. request (2.88.2) - 3.8 MB
   Last used: 8 months ago
   Deprecated: ⚠️ Yes (use axios or node-fetch)
   Safe to remove: ✅ Yes

   $ npm uninstall request

3. jquery (3.6.0) - 287 KB
   Last used: Never
   Possible reason: Migration to React
   Safe to remove: ⚠️ Check if used in HTML files

   $ npm uninstall jquery

... (20 more unused packages)

TOTAL SAVINGS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Disk space: 45.3 MB
Install time: ~8 seconds
node_modules size reduction: 9.3%

Batch removal command:
$ npm uninstall moment request jquery lodash ... (23 packages)
```

### 5. Dependency Conflict Resolution

**Conflict Detection:**
```
Dependency Conflict Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Found 3 dependency conflicts

CONFLICT 1: react
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Required versions:
- your-app requires: react@^18.2.0
- react-router@5.3.0 requires: react@^16.8.0 || ^17.0.0
- material-ui@4.12.0 requires: react@^16.8.0 || ^17.0.0

Resolved to: react@17.0.2 (downgrade from 18.2.0)

⚠️  This is a CONFLICT: You wanted react@18 but got react@17

Solution options:
1. Upgrade react-router to v6 (supports React 18)
   $ npm install react-router-dom@6

2. Upgrade material-ui to v5 (supports React 18)
   $ npm install @mui/material@5

3. Accept React 17 (keep current dependencies)
   ❌ Not recommended: Misses React 18 features

Recommended: Upgrade both react-router and material-ui
Estimated effort: 2-3 hours

CONFLICT 2: @types/node
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Required versions:
- your-app requires: @types/node@^20.0.0
- some-package requires: @types/node@^18.0.0

Resolved to: @types/node@18.19.3

Impact: Type definitions may be incomplete
Solution: Usually safe, but verify type errors

Recommended: Accept resolution (low risk)
```

### 6. Supply Chain Security

**Malicious Package Detection:**
```
Supply Chain Security Scan
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Checking for:
- Known malicious packages
- Typosquatting attempts
- Suspicious install scripts
- Exfiltration patterns

⚠️  1 SUSPICIOUS PACKAGE DETECTED

Package: reaqct (typosquatting)
Version: 18.2.0
Added: 2 days ago

Suspicious indicators:
🔴 Name similar to popular package "react"
🔴 Install script contains network calls
🔴 Package published <7 days ago
🔴 Author has 0 other packages
🔴 Downloads: 47 (react has 18M weekly)

Analysis:
This appears to be a typosquatting attack targeting "react".
The package contains code to exfiltrate environment variables
to external server.

IMMEDIATE ACTION REQUIRED:
1. Remove package immediately
   $ npm uninstall reaqct

2. Install correct package
   $ npm install react

3. Rotate any secrets/API keys in environment
4. Review git history for when package was added
5. Report to npm security: security@npmjs.com

Additional suspicious activity:
- Package attempted to read .env file
- Network connection to: suspicious-domain.com
- Attempted to read ~/.ssh directory
```

---

## Multi-Language Support

### Python (pip)
```bash
# Detect: requirements.txt, setup.py, pyproject.toml

# Security scan
$ pip-audit

# Update analysis
$ pip list --outdated

# License check
$ pip-licenses
```

### JavaScript (npm/yarn/pnpm)
```bash
# Detect: package.json

# Security scan
$ npm audit
$ yarn audit
$ pnpm audit

# Update analysis
$ npm outdated
$ yarn upgrade-interactive

# License check
$ npm license-checker
```

### Go
```bash
# Detect: go.mod

# Security scan
$ govulncheck ./...

# Update analysis
$ go list -u -m all

# Dependency graph
$ go mod graph
```

### Rust (Cargo)
```bash
# Detect: Cargo.toml

# Security scan
$ cargo audit

# Update analysis
$ cargo outdated

# Dependency tree
$ cargo tree
```

---

## Input/Output Format

### Input
```json
{
  "operation": "full_audit",
  "options": {
    "security_scan": true,
    "update_analysis": true,
    "license_check": true,
    "unused_detection": true,
    "auto_fix_safe": false
  }
}
```

### Output
```json
{
  "operation": "full_audit",
  "status": "completed",
  "package_manager": "npm",
  "project_path": "/home/user/project",
  "timestamp": "2025-10-25T10:30:00Z",
  "security": {
    "vulnerabilities_found": 12,
    "critical": 3,
    "high": 4,
    "moderate": 5,
    "auto_fixable": 8,
    "details": ["..."]
  },
  "updates": {
    "available": 23,
    "security": 1,
    "major": 2,
    "minor": 8,
    "patch": 12,
    "details": ["..."]
  },
  "licenses": {
    "total_packages": 487,
    "compliance_issues": 5,
    "incompatible_licenses": ["GPL-3.0", "AGPL-3.0"],
    "compliance_score": 62,
    "details": ["..."]
  },
  "unused": {
    "count": 23,
    "size_mb": 45.3,
    "packages": ["moment", "request", "..."]
  },
  "health_score": 72,
  "recommendations": [
    {
      "priority": "critical",
      "action": "fix_vulnerabilities",
      "command": "npm audit fix"
    },
    {
      "priority": "high",
      "action": "remove_incompatible_licenses",
      "packages": ["ghostscript.js", "..."]
    }
  ]
}
```

---

## Integration with Other Skills

### With spec-to-implementation
```python
# When implementing new feature
spec_to_impl.implement_feature("payment processing")
→ dependency_guardian.check_new_dependencies(["stripe", "pg-promise"])
→ Security check: ✅ No vulnerabilities
→ License check: ✅ Compatible
→ Proceed with implementation
```

### With pr-review-assistant
```python
# Before merging PR
pr_review_assistant.review_pr(#123)
→ dependency_guardian.audit_dependency_changes()
→ New dependencies: 2
→ Security: ⚠️ 1 vulnerability found
→ Block PR until fixed
```

---

## Performance

- **Security Scan:** < 30 seconds
- **Update Analysis:** < 10 seconds
- **License Check:** < 15 seconds
- **Full Audit:** < 60 seconds

---

## Success Metrics

- **Vulnerability Detection:** 100% of known CVEs
- **False Positives:** < 5%
- **Time Savings:** 90% vs manual audits
- **Security Incidents Prevented:** Measurable reduction

---

**Status:** Ready for implementation
**Dependencies:** None (standalone)
**Next Steps:** Implement npm/pip support (MVP)

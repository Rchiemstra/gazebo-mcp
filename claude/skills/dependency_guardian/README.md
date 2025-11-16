# Dependency Guardian

A comprehensive skill for monitoring, analyzing, and managing project dependencies across multiple ecosystems.

## Overview

Dependency Guardian helps developers and agents maintain secure, up-to-date dependencies by:
- Analyzing dependency manifests (requirements.txt, package.json, etc.)
- Scanning for known security vulnerabilities
- Checking for available updates
- Providing actionable recommendations
- Generating risk assessments

## Features

### 🔍 Dependency Analysis
- **Multi-ecosystem Support**: Python (pip), Node.js (npm)
- **Transitive Dependencies**: Identifies all dependency layers
- **Dev Dependencies**: Separate tracking of development dependencies
- **Manifest Parsing**: Supports multiple formats per ecosystem

### 🛡️ Security Scanning
- **Vulnerability Detection**: Checks against CVE and advisory databases
- **Severity Classification**: Critical, High, Medium, Low, Info
- **CVSS Scoring**: Industry-standard vulnerability scoring
- **Fix Recommendations**: Suggests specific versions to address vulnerabilities
- **Reference Links**: Direct links to security advisories

### 📦 Update Management
- **Version Tracking**: Identifies outdated packages
- **Semantic Versioning**: Classifies updates as major, minor, or patch
- **Breaking Change Detection**: Flags potentially breaking updates
- **Release Notes**: Links to changelogs and release documentation
- **Selective Updates**: Option to exclude major versions

### 📊 Risk Assessment
- **Risk Scoring**: Calculated based on vulnerabilities and outdated packages
- **Prioritized Actions**: Ordered list of recommendations
- **Health Metrics**: Overall project dependency health

## Installation

No external dependencies required! The skill uses Python's standard library.

```bash
# Optional: Install for production vulnerability databases
pip install requests  # For API calls to OSV, GitHub Advisory, etc.
```

## Quick Start

```python
from dependency_guardian import (
    analyze_dependencies,
    check_vulnerabilities,
    check_updates
)

# Analyze dependencies
analysis = analyze_dependencies("./my-project")
print(f"Found {analysis['total_dependencies']} dependencies")

# Check for vulnerabilities
vulns = check_vulnerabilities("./my-project")
if vulns['critical'] > 0:
    print(f"⚠️  {vulns['critical']} critical vulnerabilities!")

# Check for updates
updates = check_updates("./my-project", include_major=True)
print(f"{updates['outdated_count']} packages need updates")
```

## API Reference

### analyze_dependencies

Analyzes all dependencies in a project.

```python
analyze_dependencies(
    project_path: str,
    ecosystem: Optional[str] = None  # "python", "npm", or "auto"
) -> Dict
```

**Returns:**
```python
{
    'project_path': str,
    'ecosystem': str,
    'total_dependencies': int,
    'direct_dependencies': int,
    'transitive_dependencies': int,
    'dev_dependencies': int,
    'dependencies': [
        {
            'name': str,
            'version': str,
            'type': str,  # 'direct', 'transitive', 'dev'
            'spec': str,  # Original version specification
            'source_file': str
        },
        ...
    ],
    'manifest_files': [str, ...],
    'errors': [str, ...]
}
```

### check_vulnerabilities

Scans dependencies for known security vulnerabilities.

```python
check_vulnerabilities(
    project_path: str,
    ecosystem: Optional[str] = None,
    include_low: bool = True
) -> Dict
```

**Returns:**
```python
{
    'project_path': str,
    'total_vulnerabilities': int,
    'critical': int,
    'high': int,
    'medium': int,
    'low': int,
    'info': int,
    'scanned_packages': int,
    'vulnerabilities': [
        {
            'id': str,  # Advisory ID
            'package_name': str,
            'affected_version': str,
            'severity': str,
            'title': str,
            'description': str,
            'cve_id': Optional[str],
            'cvss_score': Optional[float],
            'fixed_in': Optional[str],
            'references': [str, ...],
            'published_date': Optional[str]
        },
        ...
    ],
    'errors': [str, ...]
}
```

### check_updates

Checks for available updates to dependencies.

```python
check_updates(
    project_path: str,
    ecosystem: Optional[str] = None,
    include_major: bool = False
) -> Dict
```

**Returns:**
```python
{
    'project_path': str,
    'outdated_count': int,
    'major_updates': int,
    'minor_updates': int,
    'patch_updates': int,
    'up_to_date_count': int,
    'updates_available': [
        {
            'package_name': str,
            'current_version': str,
            'latest_version': str,
            'update_type': str,  # 'major', 'minor', 'patch'
            'breaking_changes': bool,
            'release_notes_url': Optional[str],
            'published_date': Optional[str]
        },
        ...
    ],
    'errors': [str, ...]
}
```

## Ecosystem Support

### Python

**Supported Files:**
- `requirements.txt`
- `setup.py` (basic parsing)
- `pyproject.toml` (basic parsing)
- `Pipfile` (detection only)

**Example requirements.txt:**
```txt
django>=3.2.0,<4.0.0
flask==2.3.0
requests~=2.31.0
numpy>=1.24.0
```

### Node.js/npm

**Supported Files:**
- `package.json`
- `package-lock.json` (for transitive dependencies)

**Example package.json:**
```json
{
  "dependencies": {
    "express": "^4.18.2",
    "axios": "~1.6.0"
  },
  "devDependencies": {
    "jest": "^29.7.0"
  }
}
```

## Agent Integration

### Example: Automated Security Audit

```python
def security_audit_agent(project_path):
    """Agent that performs security audit."""
    # Scan for vulnerabilities
    result = check_vulnerabilities(project_path)

    # Block if critical vulnerabilities found
    if result['critical'] > 0:
        print(f"❌ BLOCKED: {result['critical']} critical vulnerabilities")
        for vuln in result['vulnerabilities']:
            if vuln['severity'] == 'critical':
                print(f"  - {vuln['package_name']}: {vuln['title']}")
                print(f"    Fix: Upgrade to {vuln['fixed_in']}")
        return False

    # Warn on high severity
    if result['high'] > 0:
        print(f"⚠️  WARNING: {result['high']} high severity vulnerabilities")

    return True
```

### Example: Automated Update PR

```python
def create_update_pr_agent(project_path):
    """Agent that creates PR for security updates."""
    # Check for updates
    updates = check_updates(project_path, include_major=False)

    # Filter security patches only
    security_updates = [
        u for u in updates['updates_available']
        if u['update_type'] == 'patch'
    ]

    if security_updates:
        # Create PR with updates
        pr_body = "## Security Updates\\n\\n"
        for upd in security_updates:
            pr_body += f"- {upd['package_name']}: "
            pr_body += f"{upd['current_version']} → {upd['latest_version']}\\n"

        # Use gh CLI or API to create PR
        # gh pr create --title "Security Updates" --body pr_body

        return pr_body

    return None
```

### Example: Weekly Health Report

```python
def generate_health_report(project_path):
    """Generate weekly dependency health report."""
    analysis = analyze_dependencies(project_path)
    vulns = check_vulnerabilities(project_path)
    updates = check_updates(project_path, include_major=True)

    # Calculate health score
    health_score = 100
    health_score -= vulns['critical'] * 20
    health_score -= vulns['high'] * 10
    health_score -= vulns['medium'] * 5
    health_score -= updates['outdated_count'] * 2
    health_score = max(0, health_score)

    report = f"""
# Dependency Health Report

## Summary
- Total Dependencies: {analysis['total_dependencies']}
- Health Score: {health_score}/100

## Security
- Critical: {vulns['critical']}
- High: {vulns['high']}
- Medium: {vulns['medium']}

## Updates
- Outdated: {updates['outdated_count']}
- Major Updates Available: {updates['major_updates']}

## Recommendation
"""

    if health_score >= 80:
        report += "✅ Dependencies are healthy"
    elif health_score >= 60:
        report += "⚠️  Address medium-priority issues"
    else:
        report += "🚨 Immediate action required"

    return report
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Dependency Audit

on:
  pull_request:
  schedule:
    - cron: '0 0 * * 1'  # Weekly on Monday

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Run Dependency Guardian
        run: |
          python skills/dependency_guardian/demo.py

      - name: Check for critical vulnerabilities
        run: |
          python -c "
          from dependency_guardian import check_vulnerabilities
          result = check_vulnerabilities('.')
          if result['critical'] > 0:
              print(f'Found {result[\"critical\"]} critical vulnerabilities')
              exit(1)
          "
```

### GitLab CI

```yaml
dependency-audit:
  stage: test
  script:
    - python skills/dependency_guardian/demo.py
    - |
      python -c "
      from dependency_guardian import check_vulnerabilities
      result = check_vulnerabilities('.')
      if result['critical'] > 0:
          exit(1)
      "
  only:
    - merge_requests
    - schedules
```

## Production Deployment

For production use, integrate with real vulnerability databases:

### OSV (Open Source Vulnerabilities)

```python
import requests

def check_osv_vulnerabilities(package, version, ecosystem):
    """Query OSV database for vulnerabilities."""
    url = "https://api.osv.dev/v1/query"
    payload = {
        "package": {"name": package, "ecosystem": ecosystem},
        "version": version
    }
    response = requests.post(url, json=payload)
    return response.json()
```

### GitHub Advisory Database

```python
def check_github_advisories(package, ecosystem):
    """Query GitHub Advisory Database."""
    url = f"https://api.github.com/advisories"
    params = {
        "affects": f"{ecosystem}/{package}",
        "per_page": 100
    }
    headers = {"Accept": "application/vnd.github+json"}
    response = requests.get(url, params=params, headers=headers)
    return response.json()
```

## Best Practices

### 1. Regular Scanning
Run dependency audits:
- On every pull request
- Weekly via scheduled jobs
- Before deployments

### 2. Prioritize Security
Address vulnerabilities in order:
1. Critical vulnerabilities (immediate)
2. High severity (within days)
3. Medium severity (within weeks)
4. Low severity (within months)

### 3. Update Strategy
- **Patches**: Apply immediately (bug fixes, security)
- **Minor**: Review and apply monthly
- **Major**: Plan and test thoroughly before upgrading

### 4. Lock Files
Always commit lock files:
- `package-lock.json` for npm
- Use `pip freeze > requirements.txt` for exact versions

### 5. Test Updates
Before applying updates:
- Run full test suite
- Check for breaking changes
- Review release notes
- Test in staging environment

## Limitations

### Current Implementation
- **Mock Data**: Demo uses mock vulnerability database
- **Basic Parsing**: Simple regex-based manifest parsing
- **No Caching**: Re-parses files on each run
- **Limited Ecosystems**: Python and npm only

### Production Enhancements
For production, consider:
- Integrate real vulnerability APIs (OSV, NVD, GitHub)
- Add caching layer for API responses
- Support more ecosystems (Go, Rust, Java, Ruby)
- Implement dependency graph visualization
- Add license compliance checking
- Support monorepo structures

## Troubleshooting

### "No dependencies found"
- Check that manifest files exist (requirements.txt, package.json)
- Verify project_path is correct
- Try specifying ecosystem explicitly

### "Errors parsing manifest"
- Ensure manifest files are valid format
- Check for syntax errors in requirements.txt or package.json
- Review error messages in returned errors array

### "No vulnerabilities detected"
- Demo uses mock database with limited entries
- For production, integrate real vulnerability databases
- Some packages may not have known vulnerabilities

## Contributing

To extend Dependency Guardian:

1. **Add New Ecosystem**: Implement parser in `dependency_analyzer.py`
2. **Add Vulnerability Source**: Extend `vulnerability_scanner.py`
3. **Add Update Source**: Extend `update_checker.py`
4. **Add License Checker**: Create new `license_checker.py` module

## Examples

See `demo.py` for comprehensive examples showing:
- Multi-ecosystem analysis
- Vulnerability detection
- Update checking
- Risk assessment
- Agent integration patterns

Run the demo:
```bash
python demo.py
```

## Related Skills

- **test-orchestrator**: Generate tests for dependencies
- **refactor-assistant**: Refactor code for new dependency versions
- **pr-review-assistant**: Review dependency update PRs

## License

Part of Claude Code Skills framework.

## Support

- View demo: `python demo.py`
- Check API: Read docstrings in source files
- Integration examples: See README sections above

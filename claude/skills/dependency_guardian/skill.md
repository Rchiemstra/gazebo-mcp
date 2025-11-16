---
name: dependency-guardian
description: Monitors and manages project dependencies, checking for security vulnerabilities, outdated packages, and compatibility issues
version: 0.1.0
author: Claude Code Skills
category: security-and-quality
tags:
  - dependencies
  - security
  - vulnerabilities
  - package-management
  - npm
  - python
tools:
  - Read
  - Bash
  - WebFetch
activation: manual
dependencies: []
operations:
  analyze_dependencies: "Analyzes all dependencies in a project"
  check_vulnerabilities: "Checks dependencies for known security vulnerabilities"
  check_updates: "Checks for available updates to dependencies"
---

# Dependency Guardian

A skill that monitors and manages project dependencies across multiple package ecosystems (npm, Python, etc.).

## Features

- **Dependency Analysis**: Parse and analyze dependency manifests
- **Security Scanning**: Check for known vulnerabilities (CVEs)
- **Update Detection**: Find outdated packages and suggest updates
- **Compatibility Checking**: Detect version conflicts and incompatibilities
- **License Auditing**: Review dependency licenses for compliance
- **Dependency Graph**: Visualize dependency trees

## Supported Ecosystems

- Python (requirements.txt, setup.py, pyproject.toml)
- Node.js (package.json, package-lock.json)
- Future: Go (go.mod), Rust (Cargo.toml), Java (pom.xml)

## Operations

### analyze_dependencies

Analyzes all dependencies in a project.

**Parameters:**
- `project_path` (str): Path to project directory
- `ecosystem` (str, optional): Specific ecosystem to analyze (python, npm, auto)

**Returns:**
- `total_dependencies`: Number of dependencies found
- `direct_dependencies`: Number of direct dependencies
- `transitive_dependencies`: Number of transitive dependencies
- `dependencies`: List of dependency objects

### check_vulnerabilities

Checks dependencies for known security vulnerabilities.

**Parameters:**
- `project_path` (str): Path to project directory
- `ecosystem` (str, optional): Specific ecosystem to check

**Returns:**
- `total_vulnerabilities`: Number of vulnerabilities found
- `critical`: Number of critical vulnerabilities
- `high`: Number of high severity vulnerabilities
- `medium`: Number of medium severity vulnerabilities
- `low`: Number of low severity vulnerabilities
- `vulnerabilities`: List of vulnerability details

### check_updates

Checks for available updates to dependencies.

**Parameters:**
- `project_path` (str): Path to project directory
- `ecosystem` (str, optional): Specific ecosystem to check
- `include_major` (bool): Include major version updates (default: False)

**Returns:**
- `outdated_count`: Number of outdated packages
- `updates_available`: List of available updates with versions

### generate_report

Generates a comprehensive dependency health report.

**Parameters:**
- `project_path` (str): Path to project directory
- `output_format` (str): Format (markdown, json, html)

**Returns:**
- `report`: Formatted report content
- `summary`: Summary statistics

## Usage Examples

```python
from skills.dependency_guardian import analyze_dependencies, check_vulnerabilities

# Analyze all dependencies
result = analyze_dependencies(project_path="./my-project")
print(f"Found {result['total_dependencies']} dependencies")

# Check for vulnerabilities
vulns = check_vulnerabilities(project_path="./my-project")
if vulns['critical'] > 0:
    print(f"⚠️  {vulns['critical']} critical vulnerabilities found!")
```

## Integration with Agents

Agents can use this skill to:
1. Audit dependencies before deployment
2. Automate security scanning in CI/CD
3. Generate dependency update PRs
4. Monitor license compliance
5. Detect supply chain risks

## Security Best Practices

- Run vulnerability checks regularly
- Keep dependencies up to date
- Review transitive dependencies
- Use lock files (package-lock.json, requirements.txt)
- Monitor for compromised packages
- Set up automated alerts

## Output Format

All operations return structured data that can be:
- Displayed to users
- Used by agents for decision making
- Exported to reports
- Integrated with other tools

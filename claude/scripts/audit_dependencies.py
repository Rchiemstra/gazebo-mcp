#!/usr/bin/env python3
"""
Dependency Security Audit Script

Checks Python dependencies for known vulnerabilities and outdated packages.
Uses safety, pip-audit, and manual checks.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class DependencyIssue:
    """Security issue in dependencies."""
    severity: str
    package: str
    current_version: str
    issue: str
    cve: str = ""
    fix_version: str = ""
    recommendation: str = ""


class DependencyAuditor:
    """Audit dependencies for security issues."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.issues: List[DependencyIssue] = []

    def audit_all(self) -> List[DependencyIssue]:
        """Run all dependency audits."""
        print("=" * 60)
        print("DEPENDENCY SECURITY AUDIT")
        print("=" * 60)
        print()

        self.check_requirements_exist()
        self.audit_with_pip_audit()
        self.check_outdated_packages()
        self.check_sensitive_packages()

        return self.issues

    def check_requirements_exist(self):
        """Check if requirements.txt exists."""
        print("Checking requirements.txt...")

        req_file = self.project_root / "requirements.txt"
        if not req_file.exists():
            self.issues.append(DependencyIssue(
                severity="high",
                package="N/A",
                current_version="N/A",
                issue="No requirements.txt found",
                recommendation="Create requirements.txt to track dependencies"
            ))
            print("  ⚠️  No requirements.txt found")
            return

        # Check if file is empty
        content = req_file.read_text().strip()
        if not content:
            self.issues.append(DependencyIssue(
                severity="medium",
                package="N/A",
                current_version="N/A",
                issue="requirements.txt is empty",
                recommendation="Add project dependencies to requirements.txt"
            ))
            print("  ⚠️  requirements.txt is empty")
            return

        # Count dependencies
        deps = [line.strip() for line in content.split("\n") if line.strip() and not line.startswith("#")]
        print(f"  ✓ Found {len(deps)} dependencies")

    def audit_with_pip_audit(self):
        """Audit with pip-audit if available."""
        print("\nChecking for known vulnerabilities...")

        try:
            # Try pip-audit first (more comprehensive)
            result = subprocess.run(
                ["pip-audit", "--format", "json"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=30
            )

            if result.returncode == 0:
                try:
                    data = json.loads(result.stdout)
                    vulnerabilities = data.get("vulnerabilities", [])

                    for vuln in vulnerabilities:
                        self.issues.append(DependencyIssue(
                            severity="high",
                            package=vuln.get("package", "unknown"),
                            current_version=vuln.get("installed_version", "unknown"),
                            issue=vuln.get("description", "Vulnerability found"),
                            cve=vuln.get("id", ""),
                            fix_version=vuln.get("fixed_version", ""),
                            recommendation=f"Upgrade to {vuln.get('fixed_version', 'latest')}"
                        ))

                    if vulnerabilities:
                        print(f"  🔴 Found {len(vulnerabilities)} vulnerabilities")
                    else:
                        print("  ✓ No vulnerabilities found")

                except json.JSONDecodeError:
                    print("  ⚠️  Could not parse pip-audit output")

        except FileNotFoundError:
            # pip-audit not installed, try safety
            print("  ℹ️  pip-audit not found, trying safety...")
            self.audit_with_safety()

        except subprocess.TimeoutExpired:
            print("  ⚠️  pip-audit timed out")

        except Exception as e:
            print(f"  ⚠️  pip-audit error: {e}")

    def audit_with_safety(self):
        """Audit with safety as fallback."""
        try:
            result = subprocess.run(
                ["safety", "check", "--json"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=30
            )

            if result.stdout:
                try:
                    vulnerabilities = json.loads(result.stdout)

                    for vuln in vulnerabilities:
                        self.issues.append(DependencyIssue(
                            severity="high",
                            package=vuln[0],  # Package name
                            current_version=vuln[2],  # Current version
                            issue=vuln[3],  # Description
                            cve=vuln[1],  # CVE ID
                            recommendation=f"Review and update package"
                        ))

                    if vulnerabilities:
                        print(f"  🔴 Found {len(vulnerabilities)} vulnerabilities")
                    else:
                        print("  ✓ No vulnerabilities found")

                except json.JSONDecodeError:
                    print("  ⚠️  Could not parse safety output")

        except FileNotFoundError:
            print("  ⚠️  Neither pip-audit nor safety found")
            print("       Install: pip install pip-audit safety")

        except Exception as e:
            print(f"  ⚠️  safety error: {e}")

    def check_outdated_packages(self):
        """Check for outdated packages."""
        print("\nChecking for outdated packages...")

        try:
            result = subprocess.run(
                ["pip", "list", "--outdated", "--format", "json"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                try:
                    outdated = json.loads(result.stdout)

                    # Filter for significant version differences
                    significant = []
                    for pkg in outdated:
                        current = pkg.get("version", "0.0.0")
                        latest = pkg.get("latest_version", "0.0.0")

                        # Parse major version
                        try:
                            current_major = int(current.split(".")[0])
                            latest_major = int(latest.split(".")[0])

                            if latest_major > current_major:
                                significant.append(pkg)
                        except (ValueError, IndexError):
                            pass

                    for pkg in significant:
                        self.issues.append(DependencyIssue(
                            severity="medium",
                            package=pkg.get("name", "unknown"),
                            current_version=pkg.get("version", "unknown"),
                            issue=f"Major version behind (latest: {pkg.get('latest_version')})",
                            fix_version=pkg.get("latest_version", ""),
                            recommendation=f"Consider upgrading to {pkg.get('latest_version')}"
                        ))

                    if significant:
                        print(f"  🟡 {len(significant)} packages significantly outdated")
                    else:
                        print(f"  ✓ All packages reasonably up-to-date")

                except json.JSONDecodeError:
                    print("  ⚠️  Could not parse pip list output")

        except Exception as e:
            print(f"  ⚠️  Could not check outdated packages: {e}")

    def check_sensitive_packages(self):
        """Check for potentially sensitive packages."""
        print("\nChecking for sensitive packages...")

        SENSITIVE_PATTERNS = {
            "requests": "network_access",
            "urllib": "network_access",
            "httpx": "network_access",
            "aiohttp": "network_access",
            "paramiko": "ssh_access",
            "fabric": "remote_execution",
            "ansible": "remote_execution",
            "docker": "container_access",
            "kubernetes": "cluster_access",
            "boto3": "aws_access",
            "google-cloud": "gcp_access",
            "azure": "azure_access",
        }

        req_file = self.project_root / "requirements.txt"
        if not req_file.exists():
            return

        content = req_file.read_text().lower()
        found_sensitive = []

        for pattern, category in SENSITIVE_PATTERNS.items():
            if pattern in content:
                found_sensitive.append((pattern, category))

        if found_sensitive:
            print(f"  ℹ️  Found {len(found_sensitive)} packages requiring review:")
            for pkg, category in found_sensitive:
                print(f"     - {pkg} ({category})")

                self.issues.append(DependencyIssue(
                    severity="info",
                    package=pkg,
                    current_version="unknown",
                    issue=f"Package provides {category}",
                    recommendation="Ensure package usage follows security best practices"
                ))
        else:
            print("  ✓ No sensitive packages detected")

    def print_report(self):
        """Print audit report."""
        print()
        print("=" * 60)
        print("DEPENDENCY AUDIT REPORT")
        print("=" * 60)
        print()

        if not self.issues:
            print("✅ No dependency issues found!")
            return

        # Group by severity
        by_severity = {
            "high": [],
            "medium": [],
            "low": [],
            "info": []
        }

        for issue in self.issues:
            by_severity[issue.severity].append(issue)

        # Print by severity
        for severity in ["high", "medium", "low", "info"]:
            issues = by_severity[severity]
            if not issues:
                continue

            icon = {
                "high": "🔴",
                "medium": "🟡",
                "low": "🔵",
                "info": "ℹ️"
            }[severity]

            print(f"{icon} {severity.upper()}: {len(issues)} issue(s)")
            print("-" * 60)

            for issue in issues:
                print(f"Package: {issue.package} (v{issue.current_version})")
                print(f"Issue: {issue.issue}")
                if issue.cve:
                    print(f"CVE: {issue.cve}")
                if issue.fix_version:
                    print(f"Fix Version: {issue.fix_version}")
                print(f"Recommendation: {issue.recommendation}")
                print()

        # Summary
        print("=" * 60)
        print(f"Total issues: {len(self.issues)}")
        print(f"  High: {len(by_severity['high'])}")
        print(f"  Medium: {len(by_severity['medium'])}")
        print(f"  Low: {len(by_severity['low'])}")
        print(f"  Info: {len(by_severity['info'])}")


def main():
    """Main entry point."""
    project_root = Path(__file__).parent.parent

    auditor = DependencyAuditor(project_root)
    auditor.audit_all()
    auditor.print_report()

    # Exit with error code if high severity issues found
    high = sum(1 for i in auditor.issues if i.severity == "high")

    if high > 0:
        print()
        print("⚠️  High severity issues found. Please address them.")
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

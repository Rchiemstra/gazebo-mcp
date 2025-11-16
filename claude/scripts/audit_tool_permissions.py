#!/usr/bin/env python3
"""
Tool Permission Audit Script

Audits tool permissions across agents, skills, and configuration files.
Identifies potentially dangerous patterns and security issues.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass


@dataclass
class SecurityIssue:
    """Security issue found during audit."""
    severity: str  # "critical", "high", "medium", "low", "info"
    category: str
    message: str
    location: str
    recommendation: str


class ToolPermissionAuditor:
    """Audit tool permissions for security issues."""

    DANGEROUS_PATTERNS = [
        r"Bash\(\*\)",  # All bash commands
        r"Bash\(rm:?\*\)",  # rm commands
        r"Bash\(sudo:?\*\)",  # sudo commands
        r"Bash\(chmod:?\*\)",  # chmod commands
        r"Bash\(curl:?\*\)",  # curl (network)
        r"Bash\(wget:?\*\)",  # wget (network)
    ]

    REVIEW_PATTERNS = [
        r"Bash\(python:?\*\)",  # Python execution
        r"Bash\(npm:?\*\)",  # NPM commands
        r"Bash\(pip:?\*\)",  # Pip commands
        r"Bash\(docker:?\*\)",  # Docker commands
        r"WebFetch",  # Web fetching
        r"WebSearch",  # Web searching
    ]

    SAFE_TOOLS = {
        "Read", "Glob", "Grep", "BashOutput"
    }

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.issues: List[SecurityIssue] = []

    def audit_all(self) -> List[SecurityIssue]:
        """Run all audits."""
        print("=" * 60)
        print("TOOL PERMISSION SECURITY AUDIT")
        print("=" * 60)
        print()

        self.audit_settings()
        self.audit_agents()
        self.audit_skills()

        return self.issues

    def audit_settings(self):
        """Audit settings.local.json."""
        print("Auditing settings.local.json...")

        settings_file = self.project_root / "settings.local.json"
        if not settings_file.exists():
            self.issues.append(SecurityIssue(
                severity="info",
                category="configuration",
                message="No settings.local.json found",
                location="settings.local.json",
                recommendation="Create settings.local.json with explicit tool allowlist"
            ))
            return

        try:
            with open(settings_file) as f:
                settings = json.load(f)

            allowed_tools = settings.get("allowedTools", [])

            if not allowed_tools:
                self.issues.append(SecurityIssue(
                    severity="high",
                    category="configuration",
                    message="No tool allowlist defined",
                    location="settings.local.json",
                    recommendation="Add 'allowedTools' array with explicit permissions"
                ))
                return

            # Check for dangerous patterns
            for tool in allowed_tools:
                for pattern in self.DANGEROUS_PATTERNS:
                    if re.search(pattern, tool):
                        self.issues.append(SecurityIssue(
                            severity="critical",
                            category="dangerous_tool",
                            message=f"Dangerous tool pattern found: {tool}",
                            location="settings.local.json",
                            recommendation=f"Remove or restrict: {tool}"
                        ))

                # Check for review patterns
                for pattern in self.REVIEW_PATTERNS:
                    if re.search(pattern, tool):
                        self.issues.append(SecurityIssue(
                            severity="medium",
                            category="review_needed",
                            message=f"Tool requires review: {tool}",
                            location="settings.local.json",
                            recommendation=f"Verify necessity of: {tool}"
                        ))

            print(f"  ✓ Checked {len(allowed_tools)} tools")

        except json.JSONDecodeError as e:
            self.issues.append(SecurityIssue(
                severity="high",
                category="configuration",
                message=f"Invalid JSON in settings.local.json: {e}",
                location="settings.local.json",
                recommendation="Fix JSON syntax errors"
            ))

    def audit_agents(self):
        """Audit agent tool requirements."""
        print("\nAuditing agents...")

        agents_dir = self.project_root / ".claude" / "agents"
        if not agents_dir.exists():
            return

        agent_files = list(agents_dir.glob("*.md"))
        for agent_file in agent_files:
            self._audit_agent_file(agent_file)

        print(f"  ✓ Checked {len(agent_files)} agents")

    def _audit_agent_file(self, agent_file: Path):
        """Audit a single agent file."""
        try:
            content = agent_file.read_text()

            # Extract YAML frontmatter
            frontmatter_match = re.search(
                r"^---\n(.*?)\n---",
                content,
                re.DOTALL | re.MULTILINE
            )

            if not frontmatter_match:
                self.issues.append(SecurityIssue(
                    severity="low",
                    category="documentation",
                    message=f"No YAML frontmatter found",
                    location=str(agent_file.relative_to(self.project_root)),
                    recommendation="Add YAML frontmatter with tools list"
                ))
                return

            frontmatter = frontmatter_match.group(1)

            # Check for tools declaration
            tools_match = re.search(r"tools:\s*\n((?:  - .*\n)*)", frontmatter)
            if not tools_match:
                self.issues.append(SecurityIssue(
                    severity="medium",
                    category="documentation",
                    message=f"No tools declared",
                    location=str(agent_file.relative_to(self.project_root)),
                    recommendation="Declare required tools in YAML frontmatter"
                ))
                return

            # Extract tools
            tools_text = tools_match.group(1)
            tools = re.findall(r"  - (\w+)", tools_text)

            # Check for excessive permissions
            if "Bash" in tools and "Write" in tools and "Read" in tools:
                self.issues.append(SecurityIssue(
                    severity="medium",
                    category="excessive_permissions",
                    message=f"Agent has full system access (Read+Write+Bash)",
                    location=str(agent_file.relative_to(self.project_root)),
                    recommendation="Review if all permissions are necessary"
                ))

            # Check for undocumented tool usage
            if "Bash" in tools:
                # Check if Bash usage is documented
                if "bash" not in content.lower() or "command" not in content.lower():
                    self.issues.append(SecurityIssue(
                        severity="low",
                        category="documentation",
                        message=f"Bash tool not documented in agent description",
                        location=str(agent_file.relative_to(self.project_root)),
                        recommendation="Document what Bash commands are used"
                    ))

        except Exception as e:
            self.issues.append(SecurityIssue(
                severity="low",
                category="audit_error",
                message=f"Could not audit agent: {e}",
                location=str(agent_file.relative_to(self.project_root)),
                recommendation="Check file format and permissions"
            ))

    def audit_skills(self):
        """Audit skill tool requirements."""
        print("\nAuditing skills...")

        skills_dir = self.project_root / "skills"
        if not skills_dir.exists():
            return

        skill_files = list(skills_dir.glob("*/SKILL.md"))
        for skill_file in skill_files:
            self._audit_skill_file(skill_file)

        print(f"  ✓ Checked {len(skill_files)} skills")

    def _audit_skill_file(self, skill_file: Path):
        """Audit a single skill file."""
        try:
            content = skill_file.read_text()

            # Extract YAML frontmatter
            frontmatter_match = re.search(
                r"^---\n(.*?)\n---",
                content,
                re.DOTALL | re.MULTILINE
            )

            if not frontmatter_match:
                return  # No frontmatter, skip

            frontmatter = frontmatter_match.group(1)

            # Check for tools declaration
            tools_match = re.search(r"tools:\s*\n((?:  - .*\n)*)", frontmatter)
            if not tools_match:
                return  # No tools declared

            # Extract tools
            tools_text = tools_match.group(1)
            tools = re.findall(r"  - (\w+)", tools_text)

            # Check for network tools without documentation
            if "WebFetch" in tools or "WebSearch" in tools:
                if "network" not in content.lower() and "domain" not in content.lower():
                    self.issues.append(SecurityIssue(
                        severity="medium",
                        category="documentation",
                        message=f"Network tool not documented",
                        location=str(skill_file.relative_to(self.project_root)),
                        recommendation="Document network access requirements"
                    ))

        except Exception as e:
            pass  # Skip errors in skill audit

    def print_report(self):
        """Print audit report."""
        print()
        print("=" * 60)
        print("AUDIT REPORT")
        print("=" * 60)
        print()

        if not self.issues:
            print("✅ No security issues found!")
            return

        # Group by severity
        by_severity = {
            "critical": [],
            "high": [],
            "medium": [],
            "low": [],
            "info": []
        }

        for issue in self.issues:
            by_severity[issue.severity].append(issue)

        # Print by severity
        for severity in ["critical", "high", "medium", "low", "info"]:
            issues = by_severity[severity]
            if not issues:
                continue

            icon = {
                "critical": "🔴",
                "high": "🟠",
                "medium": "🟡",
                "low": "🔵",
                "info": "ℹ️"
            }[severity]

            print(f"{icon} {severity.upper()}: {len(issues)} issue(s)")
            print("-" * 60)

            for issue in issues:
                print(f"Category: {issue.category}")
                print(f"Location: {issue.location}")
                print(f"Issue: {issue.message}")
                print(f"Recommendation: {issue.recommendation}")
                print()

        # Summary
        print("=" * 60)
        print(f"Total issues: {len(self.issues)}")
        print(f"  Critical: {len(by_severity['critical'])}")
        print(f"  High: {len(by_severity['high'])}")
        print(f"  Medium: {len(by_severity['medium'])}")
        print(f"  Low: {len(by_severity['low'])}")
        print(f"  Info: {len(by_severity['info'])}")


def main():
    """Main entry point."""
    import sys

    project_root = Path(__file__).parent.parent

    auditor = ToolPermissionAuditor(project_root)
    auditor.audit_all()
    auditor.print_report()

    # Exit with error code if critical/high issues found
    critical = sum(1 for i in auditor.issues if i.severity == "critical")
    high = sum(1 for i in auditor.issues if i.severity == "high")

    if critical > 0 or high > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Comprehensive Security Audit Script

Runs all security audits and generates a comprehensive report.
Can be used in CI/CD pipelines.
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict


class SecurityAudit:
    """Run comprehensive security audit."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.scripts_dir = project_root / "scripts"
        self.results: Dict[str, Dict] = {}

    def run_all_audits(self):
        """Run all security audits."""
        print("=" * 70)
        print("COMPREHENSIVE SECURITY AUDIT")
        print(f"Project: {self.project_root.name}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        print()

        audits = [
            ("Tool Permissions", "audit_tool_permissions.py"),
            ("Dependencies", "audit_dependencies.py"),
        ]

        all_passed = True

        for name, script in audits:
            success = self.run_audit(name, script)
            if not success:
                all_passed = False

        return all_passed

    def run_audit(self, name: str, script: str) -> bool:
        """Run a single audit script."""
        print()
        print("━" * 70)
        print(f"Running: {name}")
        print("━" * 70)

        script_path = self.scripts_dir / script

        if not script_path.exists():
            print(f"⚠️  Script not found: {script}")
            self.results[name] = {
                "status": "skipped",
                "reason": "Script not found"
            }
            return True

        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=self.project_root,
                capture_output=False,  # Show output directly
                timeout=60
            )

            success = result.returncode == 0
            self.results[name] = {
                "status": "passed" if success else "failed",
                "exit_code": result.returncode
            }

            return success

        except subprocess.TimeoutExpired:
            print(f"⚠️  Audit timed out: {name}")
            self.results[name] = {
                "status": "failed",
                "reason": "Timeout"
            }
            return False

        except Exception as e:
            print(f"⚠️  Audit error: {e}")
            self.results[name] = {
                "status": "failed",
                "reason": str(e)
            }
            return False

    def print_summary(self):
        """Print audit summary."""
        print()
        print("=" * 70)
        print("AUDIT SUMMARY")
        print("=" * 70)
        print()

        passed = sum(1 for r in self.results.values() if r["status"] == "passed")
        failed = sum(1 for r in self.results.values() if r["status"] == "failed")
        skipped = sum(1 for r in self.results.values() if r["status"] == "skipped")

        for name, result in self.results.items():
            status = result["status"]
            icon = {
                "passed": "✅",
                "failed": "❌",
                "skipped": "⏭️"
            }.get(status, "❓")

            print(f"{icon} {name}: {status.upper()}")

            if "reason" in result:
                print(f"   Reason: {result['reason']}")

        print()
        print("-" * 70)
        print(f"Total: {len(self.results)}")
        print(f"  Passed: {passed}")
        print(f"  Failed: {failed}")
        print(f"  Skipped: {skipped}")
        print()

        if failed > 0:
            print("⚠️  Some audits failed. Please review and address issues.")
        else:
            print("✅ All audits passed!")

    def save_report(self, output_file: Path = None):
        """Save audit report to file."""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.project_root / "logs" / f"security_audit_{timestamp}.json"

        # Ensure logs directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)

        import json

        report = {
            "timestamp": datetime.now().isoformat(),
            "project": str(self.project_root),
            "results": self.results
        }

        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)

        print(f"Report saved to: {output_file}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Run comprehensive security audit"
    )
    parser.add_argument(
        "--save-report",
        action="store_true",
        help="Save report to logs directory"
    )
    parser.add_argument(
        "--ci",
        action="store_true",
        help="CI mode: exit with error if any audit fails"
    )

    args = parser.parse_args()

    project_root = Path(__file__).parent.parent
    audit = SecurityAudit(project_root)

    all_passed = audit.run_all_audits()
    audit.print_summary()

    if args.save_report:
        audit.save_report()

    if args.ci and not all_passed:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

"""
Example 3: Validate MCP Server Security

This example demonstrates how to use the mcp_security_validator skill to check
MCP server security configuration and ensure compliance with Anthropic best practices.
"""

from skills.mcp_security_validator import validate_server_security, validate_sandbox_config
from skills.common.filters import ResultFilter


def example_1_validate_existing_server():
    """Validate an existing MCP server."""
    print("=== Example 1: Validate Existing MCP Server ===\n")

    # Validate the existing skills-mcp server
    result = validate_server_security("mcp/servers/skills-mcp", response_format="summary")

    if result.success:
        data = result.data
        print(f"✓ Security validation complete")
        print(f"  Security Score: {data['security_score']}/100")
        print(f"  Checks Passed: {data['checks_passed']}/{data['checks_total']}")

        issues_count = data.get('issues_count', {})
        print(f"\n  Issues by Severity:")
        print(f"    Critical: {issues_count.get('critical', 0)}")
        print(f"    High: {issues_count.get('high', 0)}")
        print(f"    Medium: {issues_count.get('medium', 0)}")
        print(f"    Low: {issues_count.get('low', 0)}")

        if data.get('production_ready'):
            print(f"\n  ✓ Server is production ready!")
        else:
            print(f"\n  ⚠ Server needs improvements before production")

    else:
        print(f"✗ Validation failed: {result.error}")

    print()


def example_2_detailed_security_report():
    """Get detailed security report with all issues."""
    print("=== Example 2: Detailed Security Report ===\n")

    result = validate_server_security("mcp/servers/skills-mcp", response_format="complete")

    if result.success:
        data = result.data
        print(f"Security Score: {data['security_score']}/100")
        print(f"Checks: {data['checks_passed']} passed, {data['checks_failed']} failed\n")

        # Show issues if any
        issues = data.get('issues', [])
        if issues:
            print(f"Issues Found: {len(issues)}\n")

            # Filter to critical issues first
            critical = ResultFilter.filter_by_field(issues, "severity", "critical")
            if critical:
                print("CRITICAL ISSUES:")
                for issue in critical:
                    print(f"  • {issue['issue']}")
                    print(f"    File: {issue['file']}")
                    print(f"    Fix: {issue['recommendation']}")
                    print()

            # Then high severity
            high = ResultFilter.filter_by_field(issues, "severity", "high")
            if high:
                print("HIGH SEVERITY ISSUES:")
                for issue in high:
                    print(f"  • {issue['issue']}")
                    print(f"    Fix: {issue['recommendation']}")
                    print()

        # Show recommendations
        recommendations = data.get('recommendations', [])
        if recommendations:
            print("Recommendations:")
            for rec in recommendations:
                print(f"  • {rec}")

    print()


def example_3_validate_sandbox_config():
    """Validate a sandbox configuration dictionary."""
    print("=== Example 3: Validate Sandbox Configuration ===\n")

    # Good configuration following Anthropic best practices
    good_config = {
        "filesystem": {
            "allowed_paths": ["/workspace", "/tmp"],
            "blocked_paths": ["/root", "~/.ssh", "~/.aws"]
        },
        "network": {
            "allowed_domains": ["api.anthropic.com", "pypi.org", "github.com"],
            "default_policy": "deny",
            "log_requests": True
        },
        "resources": {
            "cpu_timeout": 30,
            "memory_limit_mb": 512,
            "max_processes": 10
        }
    }

    result = validate_sandbox_config(good_config)

    if result.success:
        data = result.data
        print(f"Configuration Validation:")
        print(f"  Valid: {data['valid']}")
        print(f"  Score: {data['score']}/100")

        if data['errors']:
            print(f"\n  Errors: {len(data['errors'])}")
            for error in data['errors']:
                print(f"    [{error['severity'].upper()}] {error['issue']}")
                print(f"    Fix: {error['recommendation']}")

        if data['warnings']:
            print(f"\n  Warnings: {len(data['warnings'])}")
            for warning in data['warnings']:
                print(f"    • {warning['issue']}")

        if data['valid']:
            print("\n  ✓ Configuration is valid and ready for use!")

    print()


def example_4_compare_configurations():
    """Compare good vs poor security configurations."""
    print("=== Example 4: Compare Security Configurations ===\n")

    # Good configuration
    good_config = {
        "filesystem": {"allowed_paths": ["/workspace", "/tmp"]},
        "network": {"allowed_domains": ["api.anthropic.com"]},
        "resources": {"cpu_timeout": 30}
    }

    # Poor configuration (missing critical elements)
    poor_config = {
        "filesystem": {}  # Incomplete
    }

    print("Good Configuration:")
    good_result = validate_sandbox_config(good_config)
    if good_result.success:
        print(f"  Score: {good_result.data['score']}/100")
        print(f"  Valid: {good_result.data['valid']}")

    print("\nPoor Configuration:")
    poor_result = validate_sandbox_config(poor_config)
    if poor_result.success:
        print(f"  Score: {poor_result.data['score']}/100")
        print(f"  Valid: {poor_result.data['valid']}")
        print(f"  Errors: {len(poor_result.data['errors'])}")

    print(f"\nScore Difference: {good_result.data['score'] - poor_result.data['score']} points")

    print()


def example_5_filter_security_issues():
    """Filter security issues by severity."""
    print("=== Example 5: Filter Security Issues ===\n")

    result = validate_server_security("mcp/servers/skills-mcp", response_format="complete")

    if result.success:
        issues = result.data.get('issues', [])

        if issues:
            print(f"Total Issues: {len(issues)}\n")

            # Filter by severity
            critical = ResultFilter.filter_by_field(issues, "severity", "critical")
            high = ResultFilter.filter_by_field(issues, "severity", "high")
            medium = ResultFilter.filter_by_field(issues, "severity", "medium")

            print(f"Breakdown:")
            print(f"  Critical: {len(critical)}")
            print(f"  High: {len(high)}")
            print(f"  Medium: {len(medium)}")

            # Show only blocking issues (critical + high)
            blocking = critical + high
            if blocking:
                print(f"\n{len(blocking)} Blocking Issues (must fix before production):")
                for issue in blocking:
                    print(f"  • {issue['issue']}")
        else:
            print("✓ No security issues found!")

    print()


def example_6_security_checklist():
    """Generate a security checklist for MCP server."""
    print("=== Example 6: Security Checklist ===\n")

    print("MCP Server Security Checklist:")
    print()

    checklist = [
        ("Filesystem isolation configured", "✓"),
        ("Network filtering enabled", "✓"),
        ("Resource limits set", "✓"),
        ("Code validation enabled", "✓"),
        ("Sensitive paths blocked", "✓"),
        ("Allowed domains whitelisted", "✓"),
        ("Error handling secure", "✓"),
        ("Logging configured", "✓"),
    ]

    for item, status in checklist:
        print(f"  [{status}] {item}")

    print("\n  Recommendation: Run validate_server_security() to verify all items")

    print()


if __name__ == "__main__":
    print("MCP Security Validator Examples\n")
    print("=" * 60)
    print()

    example_1_validate_existing_server()
    example_2_detailed_security_report()
    example_3_validate_sandbox_config()
    example_4_compare_configurations()
    example_5_filter_security_issues()
    example_6_security_checklist()

    print("=" * 60)
    print("\nAll examples complete!")
    print("\nNext steps:")
    print("- Fix any critical/high security issues")
    print("- Ensure security score >= 90/100")
    print("- Review security best practices")
    print("- Test server in production environment")

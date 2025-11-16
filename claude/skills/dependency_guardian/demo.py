#!/usr/bin/env python3
"""
Dependency Guardian Demonstration

Demonstrates the dependency-guardian skill capabilities.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dependency_guardian import analyze_dependencies, check_vulnerabilities, check_updates


def print_header(text):
    """Print formatted header."""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")


def print_section(text):
    """Print formatted section."""
    print("\n" + "-" * 80)
    print(f"  {text}")
    print("-" * 80 + "\n")


def severity_icon(severity):
    """Get icon for severity level."""
    icons = {
        'critical': '🔴',
        'high': '🟠',
        'medium': '🟡',
        'low': '🔵',
        'info': '⚪'
    }
    return icons.get(severity, '⚪')


def main():
    """Run the demonstration."""
    print_header("DEPENDENCY GUARDIAN DEMONSTRATION")

    # Get example project paths
    python_project = Path(__file__).parent / "examples" / "python_project"
    npm_project = Path(__file__).parent / "examples" / "npm_project"

    # ===================================================================
    # PART 1: PYTHON PROJECT ANALYSIS
    # ===================================================================
    print_section("PART 1: PYTHON PROJECT ANALYSIS")

    print(f"📦 Analyzing Python project: {python_project}\n")

    # Step 1: Analyze dependencies
    print("Step 1: Dependency Analysis")
    print("-" * 40)

    analysis = analyze_dependencies(str(python_project), ecosystem="python")

    print(f"✅ Found {analysis['total_dependencies']} dependencies")
    print(f"   📌 Direct: {analysis['direct_dependencies']}")
    print(f"   🔗 Transitive: {analysis['transitive_dependencies']}")
    print(f"   🛠️  Dev: {analysis['dev_dependencies']}")
    print(f"   📄 Manifest files: {len(analysis['manifest_files'])}")

    if analysis['dependencies']:
        print("\n📋 Dependencies:")
        for dep in analysis['dependencies'][:8]:  # Show first 8
            print(f"   • {dep['name']:20} {dep['version']:15} ({dep['type']})")
        if len(analysis['dependencies']) > 8:
            print(f"   ... and {len(analysis['dependencies']) - 8} more")

    # Step 2: Security Vulnerability Scan
    print("\n\nStep 2: Security Vulnerability Scan")
    print("-" * 40)

    vulns = check_vulnerabilities(str(python_project), ecosystem="python")

    print(f"🔍 Scanned {vulns['scanned_packages']} packages")
    print(f"⚠️  Found {vulns['total_vulnerabilities']} vulnerabilities\n")

    if vulns['total_vulnerabilities'] > 0:
        print("   Severity Breakdown:")
        print(f"   🔴 Critical: {vulns['critical']}")
        print(f"   🟠 High:     {vulns['high']}")
        print(f"   🟡 Medium:   {vulns['medium']}")
        print(f"   🔵 Low:      {vulns['low']}")

        print("\n   📋 Vulnerability Details:")
        for vuln in vulns['vulnerabilities']:
            icon = severity_icon(vuln['severity'])
            print(f"\n   {icon} {vuln['severity'].upper()}: {vuln['title']}")
            print(f"      Package: {vuln['package_name']} {vuln['affected_version']}")
            print(f"      ID: {vuln['id']}")
            if vuln['cve_id']:
                print(f"      CVE: {vuln['cve_id']}")
            if vuln['cvss_score']:
                print(f"      CVSS Score: {vuln['cvss_score']}")
            if vuln['fixed_in']:
                print(f"      ✅ Fixed in: {vuln['fixed_in']}")
            print(f"      📝 {vuln['description'][:100]}...")

    # Step 3: Check for Updates
    print("\n\nStep 3: Check for Updates")
    print("-" * 40)

    updates = check_updates(str(python_project), ecosystem="python", include_major=True)

    print(f"📊 Update Summary:")
    print(f"   Outdated packages: {updates['outdated_count']}")
    print(f"   Up-to-date: {updates['up_to_date_count']}")
    print()
    print(f"   🔴 Major updates: {updates['major_updates']}")
    print(f"   🟡 Minor updates: {updates['minor_updates']}")
    print(f"   🟢 Patch updates: {updates['patch_updates']}")

    if updates['updates_available']:
        print("\n   📋 Available Updates:")
        for upd in updates['updates_available']:
            type_icon = {
                'major': '🔴',
                'minor': '🟡',
                'patch': '🟢'
            }.get(upd['update_type'], '⚪')

            print(f"\n   {type_icon} {upd['package_name']}")
            print(f"      Current: {upd['current_version']} → Latest: {upd['latest_version']}")
            print(f"      Type: {upd['update_type'].upper()}")
            if upd['breaking_changes']:
                print(f"      ⚠️  Breaking changes expected")
            if upd['release_notes_url']:
                print(f"      📖 Release notes: {upd['release_notes_url']}")

    # ===================================================================
    # PART 2: NODE.JS PROJECT ANALYSIS
    # ===================================================================
    print_section("PART 2: NODE.JS PROJECT ANALYSIS")

    print(f"📦 Analyzing npm project: {npm_project}\n")

    # Step 1: Analyze dependencies
    print("Step 1: Dependency Analysis")
    print("-" * 40)

    npm_analysis = analyze_dependencies(str(npm_project), ecosystem="npm")

    print(f"✅ Found {npm_analysis['total_dependencies']} dependencies")
    print(f"   📌 Direct: {npm_analysis['direct_dependencies']}")
    print(f"   🔗 Transitive: {npm_analysis['transitive_dependencies']}")
    print(f"   🛠️  Dev: {npm_analysis['dev_dependencies']}")

    if npm_analysis['dependencies']:
        print("\n📋 Dependencies:")
        for dep in npm_analysis['dependencies']:
            print(f"   • {dep['name']:20} {dep['version']:15} ({dep['type']})")

    # Step 2: Security Scan
    print("\n\nStep 2: Security Vulnerability Scan")
    print("-" * 40)

    npm_vulns = check_vulnerabilities(str(npm_project), ecosystem="npm")

    print(f"🔍 Scanned {npm_vulns['scanned_packages']} packages")
    print(f"⚠️  Found {npm_vulns['total_vulnerabilities']} vulnerabilities")

    if npm_vulns['total_vulnerabilities'] > 0:
        print("\n   📋 Vulnerability Details:")
        for vuln in npm_vulns['vulnerabilities']:
            icon = severity_icon(vuln['severity'])
            print(f"\n   {icon} {vuln['severity'].upper()}: {vuln['title']}")
            print(f"      Package: {vuln['package_name']} {vuln['affected_version']}")
            if vuln['fixed_in']:
                print(f"      ✅ Fixed in: {vuln['fixed_in']}")

    # Step 3: Check Updates
    print("\n\nStep 3: Check for Updates")
    print("-" * 40)

    npm_updates = check_updates(str(npm_project), ecosystem="npm", include_major=True)

    print(f"📊 Update Summary:")
    print(f"   Outdated packages: {npm_updates['outdated_count']}")
    print(f"   Up-to-date: {npm_updates['up_to_date_count']}")

    if npm_updates['updates_available']:
        print("\n   📋 Available Updates:")
        for upd in npm_updates['updates_available']:
            type_icon = {
                'major': '🔴',
                'minor': '🟡',
                'patch': '🟢'
            }.get(upd['update_type'], '⚪')

            print(f"\n   {type_icon} {upd['package_name']}")
            print(f"      {upd['current_version']} → {upd['latest_version']} ({upd['update_type']})")

    # ===================================================================
    # PART 3: ACTIONABLE RECOMMENDATIONS
    # ===================================================================
    print_section("PART 3: ACTIONABLE RECOMMENDATIONS")

    # Calculate risk scores
    total_vulns = vulns['total_vulnerabilities'] + npm_vulns['total_vulnerabilities']
    critical_vulns = vulns['critical'] + npm_vulns['critical']
    high_vulns = vulns['high'] + npm_vulns['high']
    total_outdated = updates['outdated_count'] + npm_updates['outdated_count']

    print("🎯 Priority Actions:\n")

    priority_number = 1

    # Critical vulnerabilities first
    if critical_vulns > 0:
        print(f"{priority_number}. 🚨 URGENT: Fix {critical_vulns} critical vulnerabilities")
        priority_number += 1

    # High vulnerabilities
    if high_vulns > 0:
        print(f"{priority_number}. ⚠️  HIGH: Address {high_vulns} high-severity vulnerabilities")
        priority_number += 1

    # Security updates
    security_updates = [u for u in updates['updates_available'] + npm_updates['updates_available']
                       if u['update_type'] == 'patch']
    if security_updates:
        print(f"{priority_number}. 🔒 Apply {len(security_updates)} security patch updates")
        priority_number += 1

    # Major updates with breaking changes
    breaking_updates = [u for u in updates['updates_available'] + npm_updates['updates_available']
                       if u['breaking_changes']]
    if breaking_updates:
        print(f"{priority_number}. 📋 Review {len(breaking_updates)} major updates (may have breaking changes)")
        priority_number += 1

    # General updates
    if total_outdated > len(breaking_updates):
        other_updates = total_outdated - len(breaking_updates)
        print(f"{priority_number}. 📦 Update {other_updates} other dependencies")
        priority_number += 1

    # Risk assessment
    print("\n📊 Risk Assessment:\n")

    risk_score = (
        critical_vulns * 10 +
        high_vulns * 5 +
        (vulns['medium'] + npm_vulns['medium']) * 2 +
        (total_outdated * 0.5)
    )

    if risk_score > 50:
        print("   🔴 HIGH RISK")
        print("   Immediate action required - critical security issues detected")
    elif risk_score > 20:
        print("   🟡 MEDIUM RISK")
        print("   Address security vulnerabilities and apply updates soon")
    elif risk_score > 5:
        print("   🟢 LOW RISK")
        print("   Dependencies are mostly secure, minor updates recommended")
    else:
        print("   ✅ MINIMAL RISK")
        print("   Dependencies are up-to-date and secure")

    print(f"\n   Risk Score: {risk_score:.1f}/100")

    # ===================================================================
    # PART 4: INTEGRATION EXAMPLES
    # ===================================================================
    print_section("PART 4: INTEGRATION WITH AGENTS")

    print("💡 How agents can use dependency-guardian:\n")

    print("1. 🤖 Automated Security Audits")
    print("   Agent runs vulnerability scans on every PR")
    print("   Blocks merge if critical vulnerabilities found")
    print()

    print("2. 🔄 Automated Dependency Updates")
    print("   Agent creates PRs for security patches")
    print("   Runs tests before proposing major updates")
    print()

    print("3. 📊 Dependency Health Monitoring")
    print("   Agent generates weekly dependency reports")
    print("   Alerts on new vulnerabilities")
    print()

    print("4. 🛡️  License Compliance")
    print("   Agent checks dependency licenses")
    print("   Flags incompatible or risky licenses")
    print()

    print("5. 📈 Dependency Trend Analysis")
    print("   Agent tracks dependency growth over time")
    print("   Identifies unused or duplicate dependencies")

    # ===================================================================
    # SUMMARY
    # ===================================================================
    print_section("SUMMARY")

    print("✅ Dependency Guardian successfully demonstrated:")
    print(f"   • Analyzed {analysis['total_dependencies'] + npm_analysis['total_dependencies']} dependencies")
    print(f"   • Detected {total_vulns} security vulnerabilities")
    print(f"   • Found {total_outdated} available updates")
    print(f"   • Provided actionable recommendations")
    print()

    print("🎯 Key Features:")
    print("   ✅ Multi-ecosystem support (Python, npm)")
    print("   ✅ Security vulnerability detection")
    print("   ✅ Update availability checking")
    print("   ✅ Risk assessment and prioritization")
    print("   ✅ Agent-ready API")
    print()

    print("📚 Next Steps:")
    print("   1. Integrate with CI/CD pipelines")
    print("   2. Set up automated security scanning")
    print("   3. Configure update notifications")
    print("   4. Review and apply recommended updates")
    print()

    print_header("DEMONSTRATION COMPLETE")

    return 0


if __name__ == "__main__":
    sys.exit(main())

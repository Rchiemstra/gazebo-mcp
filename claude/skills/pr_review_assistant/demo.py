#!/usr/bin/env python3
"""
PR Review Assistant Demonstration

Demonstrates automated PR review capabilities.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from pr_review_assistant import review_pull_request, generate_review_comment


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


def main():
    """Run the demonstration."""
    print_header("PR REVIEW ASSISTANT DEMONSTRATION")

    # ===================================================================
    # SCENARIO: Reviewing a Pull Request
    # ===================================================================

    print("📋 Scenario: Feature Branch PR Review")
    print()
    print("Pull Request: feature/payment-processing → main")
    print("Changes:")
    print("  + new_feature.py (new payment processing)")
    print("  M existing_module.py (fee calculation updates)")
    print()

    # Define PR changes
    pr_changes = {
        'added': [
            'skills/pr_review_assistant/examples/pr_files/new_feature.py'
        ],
        'modified': [
            'skills/pr_review_assistant/examples/pr_files/existing_module.py'
        ],
        'deleted': []
    }

    # ===================================================================
    # PART 1: AUTOMATED REVIEW
    # ===================================================================
    print_section("PART 1: AUTOMATED CODE REVIEW")

    print("🔍 Running automated review...\n")

    result = review_pull_request(
        pr_changes=pr_changes,
        base_branch='main',
        target_branch='feature/payment-processing'
    )

    print(f"✅ Review complete!\n")

    # Display overall results
    print("📊 Overall Results:")
    print(f"   Score: {result['overall_score']:.1f}/100")
    print(f"   Status: {result['approval_status'].upper()}")
    print(f"   Issues Found: {len(result['issues'])}")
    print(f"   Recommendations: {len(result['recommendations'])}")
    print()

    # Display dimension scores
    print("📈 Dimension Scores:")
    for dim in result['dimension_scores']:
        bar = create_visual_bar(dim['score'])
        print(f"   {dim['dimension'].replace('_', ' ').title():20} "
              f"{bar} {dim['score']:5.1f}/100 "
              f"({dim['passed_checks']}/{dim['total_checks']} checks)")

    # ===================================================================
    # PART 2: ISSUES BREAKDOWN
    # ===================================================================
    print_section("PART 2: ISSUES BREAKDOWN")

    # Group issues by severity
    issues_by_severity = {}
    for issue in result['issues']:
        severity = issue['severity']
        if severity not in issues_by_severity:
            issues_by_severity[severity] = []
        issues_by_severity[severity].append(issue)

    print(f"Found {len(result['issues'])} issues:\n")

    # Display by severity
    severity_order = ['blocker', 'critical', 'major', 'minor', 'info']
    for severity in severity_order:
        if severity in issues_by_severity:
            issues = issues_by_severity[severity]
            emoji = get_severity_emoji(severity)
            print(f"{emoji} {severity.upper()}: {len(issues)} issue(s)")

    print()

    # Show detailed issues
    print("📝 Detailed Issues:\n")

    for i, issue in enumerate(result['issues'][:8], 1):  # Show first 8
        emoji = get_severity_emoji(issue['severity'])
        print(f"{i}. {emoji} [{issue['severity'].upper()}] {issue['title']}")

        if issue['file_path']:
            # Shorten path for display
            short_path = Path(issue['file_path']).name
            print(f"   📁 File: {short_path}")

        if issue['line_number']:
            print(f"   📍 Line: {issue['line_number']}")

        print(f"   📝 {issue['description']}")
        print(f"   💡 {issue['suggestion']}")
        print()

    if len(result['issues']) > 8:
        print(f"   ... and {len(result['issues']) - 8} more issues\n")

    # ===================================================================
    # PART 3: RECOMMENDATIONS
    # ===================================================================
    print_section("PART 3: ACTIONABLE RECOMMENDATIONS")

    print("💡 Recommendations for this PR:\n")

    for i, rec in enumerate(result['recommendations'], 1):
        print(f"   {i}. {rec}")

    print()

    # ===================================================================
    # PART 4: FORMATTED REVIEW COMMENT
    # ===================================================================
    print_section("PART 4: FORMATTED REVIEW COMMENT")

    print("📝 Generating formatted review comment...\n")

    comment = generate_review_comment(result, format='github')

    print("This comment would be posted to the PR:")
    print()
    print("─" * 80)
    print(comment)
    print("─" * 80)

    # ===================================================================
    # PART 5: AGENT INTEGRATION EXAMPLES
    # ===================================================================
    print_section("PART 5: AGENT INTEGRATION")

    print("🤖 How agents can use pr-review-assistant:\n")

    print("1. 🚦 Quality Gate Enforcement")
    print("   Agent blocks merge if score < 70 or blockers exist")
    print("   Ensures minimum quality standards")
    print()

    print("2. 🔄 Automated PR Review")
    print("   Agent reviews every PR automatically")
    print("   Posts detailed feedback within minutes")
    print("   Reduces human reviewer burden")
    print()

    print("3. 📊 Quality Tracking")
    print("   Agent tracks quality metrics over time")
    print("   Identifies quality trends")
    print("   Generates team reports")
    print()

    print("4. 🎯 Smart Reviewer Assignment")
    print("   Agent suggests reviewers based on changes")
    print("   Matches expertise to changed files")
    print("   Balances review load")
    print()

    print("5. 🔧 Auto-Fix Simple Issues")
    print("   Agent can auto-fix minor issues")
    print("   Applies formatting, removes print statements")
    print("   Creates follow-up commits")

    # ===================================================================
    # PART 6: WORKFLOW EXAMPLE
    # ===================================================================
    print_section("PART 6: RECOMMENDED WORKFLOW")

    print("🔧 Automated PR Review Workflow:\n")

    print("1. 👤 Developer Creates PR")
    print("   Developer pushes feature branch and opens PR")
    print()

    print("2. 🤖 Agent Triggers Review")
    print("   GitHub webhook triggers automated review")
    print("   Agent calls pr-review-assistant.review_pull_request()")
    print()

    print("3. 📊 Multi-Skill Analysis")
    print("   - Code quality (refactor-assistant)")
    print("   - Test coverage (test-orchestrator)")
    print("   - Security (dependency-guardian)")
    print("   - Best practices (built-in checks)")
    print()

    print("4. 💬 Agent Posts Review")
    print("   Agent posts formatted comment to PR")
    print("   Includes scores, issues, and recommendations")
    print()

    print("5. 🚦 Quality Gate Decision")
    if result['approval_status'] == 'approve':
        print("   ✅ APPROVED: PR passes quality gates")
        print("   Ready for human review and merge")
    elif result['approval_status'] == 'request_changes':
        print("   ❌ BLOCKED: PR has critical issues")
        print("   Developer must address issues before merge")
    else:
        print("   💬 COMMENTED: Minor improvements needed")
        print("   PR can proceed with human review")
    print()

    print("6. 🔄 Iterate")
    print("   Developer addresses feedback")
    print("   Agent re-reviews on push")
    print("   Cycle continues until approved")

    # ===================================================================
    # PART 7: DECISION LOGIC
    # ===================================================================
    print_section("PART 7: APPROVAL DECISION LOGIC")

    print("🎯 How the decision was made:\n")

    print(f"Overall Score: {result['overall_score']:.1f}/100")

    # Check for blockers
    blockers = [i for i in result['issues'] if i['severity'] == 'blocker']
    critical = [i for i in result['issues'] if i['severity'] == 'critical']

    if blockers:
        print(f"🚫 Blockers: {len(blockers)} found → REQUEST CHANGES")
    elif critical:
        print(f"🔴 Critical: {len(critical)} found → REQUEST CHANGES")
    elif result['overall_score'] < 60:
        print(f"📉 Low score ({result['overall_score']:.1f}) → REQUEST CHANGES")
    elif result['overall_score'] < 80:
        print(f"🟡 Medium score ({result['overall_score']:.1f}) → COMMENT")
    else:
        print(f"🟢 High score ({result['overall_score']:.1f}) → APPROVE")

    print()
    print(f"Final Decision: {result['approval_status'].upper()}")

    # ===================================================================
    # SUMMARY
    # ===================================================================
    print_section("SUMMARY")

    print("✅ PR Review Assistant successfully demonstrated:")
    print(f"   • Analyzed {result['statistics']['total_files_changed']} changed file(s)")
    print(f"   • Identified {len(result['issues'])} issue(s)")
    print(f"   • Generated {len(result['recommendations'])} recommendation(s)")
    print(f"   • Calculated quality score: {result['overall_score']:.1f}/100")
    print(f"   • Made decision: {result['approval_status'].upper()}")
    print()

    print("🎯 Key Features:")
    print("   ✅ 5 review dimensions")
    print("   ✅ Security vulnerability detection")
    print("   ✅ Test coverage validation")
    print("   ✅ Code quality analysis")
    print("   ✅ Best practices enforcement")
    print("   ✅ Formatted GitHub comments")
    print()

    print("📚 Next Steps:")
    print("   1. Integrate with GitHub Actions")
    print("   2. Configure quality gates")
    print("   3. Customize review checklist")
    print("   4. Connect to other skills")
    print("   5. Track quality metrics")
    print()

    print_header("DEMONSTRATION COMPLETE")

    return 0


def create_visual_bar(score):
    """Create visual score bar."""
    filled = int(score / 10)
    empty = 10 - filled

    if score >= 80:
        return '🟢 ' + '█' * filled + '░' * empty
    elif score >= 60:
        return '🟡 ' + '█' * filled + '░' * empty
    else:
        return '🔴 ' + '█' * filled + '░' * empty


def get_severity_emoji(severity):
    """Get emoji for severity."""
    emoji_map = {
        'blocker': '🚫',
        'critical': '🔴',
        'major': '🟠',
        'minor': '🟡',
        'info': '🔵'
    }
    return emoji_map.get(severity, '⚪')


if __name__ == "__main__":
    sys.exit(main())

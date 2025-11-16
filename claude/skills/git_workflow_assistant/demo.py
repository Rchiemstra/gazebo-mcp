#!/usr/bin/env python3
"""
Git Workflow Assistant Demonstration

Demonstrates intelligent git workflow automation.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from git_workflow_assistant import (
    analyze_changes,
    generate_commit_message,
    suggest_branch_name,
    create_pull_request
)


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
    print_header("GIT WORKFLOW ASSISTANT DEMONSTRATION")

    # Use current repository for demo
    repo_path = Path(__file__).parent.parent.parent

    # ===================================================================
    # PART 1: ANALYZE CHANGES
    # ===================================================================
    print_section("PART 1: ANALYZE REPOSITORY CHANGES")

    print(f"Analyzing repository: {repo_path.name}\n")

    analysis = analyze_changes(repo_path=str(repo_path))

    print("Change Analysis:")
    print(f"  Change type: {analysis['change_type']}")
    print(f"  Impact level: {analysis['impact_level']}")
    print()

    print("Statistics:")
    stats = analysis['statistics']
    print(f"  Files changed: {stats['files_changed']}")
    print(f"  New files: {stats['new_files']}")
    print(f"  Modified files: {stats['modified_files']}")
    print(f"  Deleted files: {stats['deleted_files']}")
    print(f"  Total additions: +{stats['total_additions']}")
    print(f"  Total deletions: -{stats['total_deletions']}")
    print(f"  Net change: {stats['net_change']:+d}")
    print()

    if analysis['staged_files']:
        print(f"Staged files ({len(analysis['staged_files'])}):")
        for file in analysis['staged_files'][:10]:
            status_emoji = {
                'A': '✨',
                'M': '📝',
                'D': '🗑️'
            }.get(file['status'], '❓')
            print(f"  {status_emoji} {file['path']}")
            if file['additions'] or file['deletions']:
                print(f"     +{file['additions']} -{file['deletions']} lines")

        if len(analysis['staged_files']) > 10:
            print(f"  ... and {len(analysis['staged_files']) - 10} more files")
        print()
    else:
        print("No staged files (working directory is clean)\n")

    if analysis['breaking_changes']:
        print("⚠️  Breaking Changes Detected:")
        for change in analysis['breaking_changes']:
            print(f"  - {change}")
        print()

    if analysis['affected_modules']:
        print(f"Affected Modules:")
        for module in analysis['affected_modules']:
            print(f"  • {module}")
        print()

    # ===================================================================
    # PART 2: GENERATE COMMIT MESSAGE
    # ===================================================================
    print_section("PART 2: GENERATE COMMIT MESSAGE")

    print("Generating semantic commit message...\n")

    commit = generate_commit_message(repo_path=str(repo_path))

    print("Generated Commit Message:")
    print("=" * 80)
    print(commit['message'])
    print("=" * 80)
    print()

    print("Message Components:")
    print(f"  Type: {commit['type']}")
    if commit['scope']:
        print(f"  Scope: {commit['scope']}")
    print(f"  Description: {commit['description']}")
    if commit['is_breaking']:
        print(f"  Breaking: ⚠️  YES")
    print()

    # ===================================================================
    # PART 3: BRANCH NAME SUGGESTIONS
    # ===================================================================
    print_section("PART 3: SUGGEST BRANCH NAMES")

    print("Examples of branch name suggestions:\n")

    # Example 1: Feature branch
    print("1. Feature Branch (GitFlow)")
    suggestion = suggest_branch_name(
        issue_number='PROJ-123',
        description='Add user authentication',
        branch_type='feature',
        strategy='gitflow'
    )
    print(f"   Branch: {suggestion['branch_name']}")
    print(f"   Base: {suggestion['base_branch']}")
    print()

    # Example 2: Bugfix
    print("2. Bugfix Branch (GitHub Flow)")
    suggestion = suggest_branch_name(
        issue_number='456',
        description='Fix login redirect issue',
        branch_type='bugfix',
        strategy='github-flow'
    )
    print(f"   Branch: {suggestion['branch_name']}")
    print(f"   Base: {suggestion['base_branch']}")
    print()

    # Example 3: Hotfix
    print("3. Hotfix Branch (GitFlow)")
    suggestion = suggest_branch_name(
        issue_number='URGENT-789',
        description='Fix critical security vulnerability',
        branch_type='hotfix',
        strategy='gitflow'
    )
    print(f"   Branch: {suggestion['branch_name']}")
    print(f"   Base: {suggestion['base_branch']}")
    print()

    # Example 4: Documentation
    print("4. Documentation Branch")
    suggestion = suggest_branch_name(
        description='Update API documentation',
        branch_type='docs',
        strategy='gitflow'
    )
    print(f"   Branch: {suggestion['branch_name']}")
    print(f"   Base: {suggestion['base_branch']}")
    print()

    # ===================================================================
    # PART 4: PULL REQUEST GENERATION
    # ===================================================================
    print_section("PART 4: GENERATE PULL REQUEST")

    print("Generating pull request content...\n")

    pr = create_pull_request(
        repo_path=str(repo_path),
        source_branch='feature/demo',
        target_branch='main'
    )

    print("Pull Request Preview:")
    print("=" * 80)
    print(f"Title: {pr['title']}\n")
    print(pr['description'])
    print("=" * 80)
    print()

    if pr['labels']:
        print("Suggested Labels:")
        for label in pr['labels']:
            print(f"  🏷️  {label}")
        print()

    if pr['checklist']:
        print("PR Checklist:")
        for item in pr['checklist']:
            print(f"  {item}")
        print()

    # ===================================================================
    # PART 5: BRANCHING STRATEGIES
    # ===================================================================
    print_section("PART 5: BRANCHING STRATEGIES COMPARISON")

    print("Same feature across different strategies:\n")

    issue = "FEAT-100"
    desc = "Implement payment processing"

    strategies = ['gitflow', 'github-flow', 'gitlab-flow']

    for strategy in strategies:
        suggestion = suggest_branch_name(
            issue_number=issue,
            description=desc,
            branch_type='feature',
            strategy=strategy
        )

        print(f"{strategy.upper()}:")
        print(f"  Branch: {suggestion['branch_name']}")
        print(f"  Base: {suggestion['base_branch']}")
        print()

    # ===================================================================
    # PART 6: COMMIT MESSAGE TYPES
    # ===================================================================
    print_section("PART 6: COMMIT MESSAGE TYPES")

    print("Different commit types:\n")

    commit_types = [
        ('feat', 'New feature or functionality'),
        ('fix', 'Bug fix'),
        ('docs', 'Documentation changes'),
        ('style', 'Code formatting, no logic changes'),
        ('refactor', 'Code restructuring'),
        ('test', 'Add or update tests'),
        ('chore', 'Maintenance tasks'),
        ('perf', 'Performance improvements'),
        ('ci', 'CI/CD changes'),
        ('build', 'Build system changes')
    ]

    for type_name, description in commit_types:
        print(f"{type_name:12} - {description}")

    print()

    print("Example commit messages:")
    print()
    print("  feat(auth): add OAuth2 authentication")
    print("  fix(api): correct response status codes")
    print("  docs(readme): update installation instructions")
    print("  refactor(core): simplify data processing logic")
    print("  test(auth): add unit tests for login flow")
    print()

    # ===================================================================
    # PART 7: USE CASES
    # ===================================================================
    print_section("PART 7: USE CASES")

    print("How git-workflow-assistant can be used:\n")

    print("1. 🤖 Pre-commit Hook")
    print("   Auto-generate commit messages before commit")
    print("   Ensure consistent commit format")
    print()

    print("2. 🌿 Branch Creation Automation")
    print("   Generate branch names from Jira/GitHub issues")
    print("   Follow team branching conventions")
    print()

    print("3. 📝 Pull Request Templates")
    print("   Auto-generate PR descriptions from commits")
    print("   Include change summaries and checklists")
    print()

    print("4. 🔍 Change Impact Analysis")
    print("   Analyze changes before committing")
    print("   Identify breaking changes automatically")
    print()

    print("5. 📊 Release Notes Generation")
    print("   Extract commit messages for release notes")
    print("   Group changes by type")
    print()

    print("6. ✅ Commit Message Validation")
    print("   Enforce semantic commit format")
    print("   Block non-conforming commits")
    print()

    print("7. 🎯 Smart Reviewer Assignment")
    print("   Suggest reviewers based on affected modules")
    print("   Balance review workload")
    print()

    # ===================================================================
    # PART 8: WORKFLOW INTEGRATION
    # ===================================================================
    print_section("PART 8: WORKFLOW INTEGRATION")

    print("Complete git workflow with automation:\n")

    print("1. 🎫 Start from Issue")
    print("   Branch: suggest_branch_name(issue='PROJ-123', ...)")
    print("   git checkout -b <suggested_name>")
    print()

    print("2. 💻 Make Changes")
    print("   Edit code, add features, fix bugs")
    print()

    print("3. 🔍 Analyze Impact")
    print("   Analysis: analyze_changes()")
    print("   Review change type and impact")
    print()

    print("4. ✍️ Auto-generate Commit")
    print("   Message: generate_commit_message()")
    print("   git commit -m <generated_message>")
    print()

    print("5. 📤 Create Pull Request")
    print("   PR: create_pull_request()")
    print("   Use generated title and description")
    print()

    print("6. 👀 Code Review")
    print("   Reviewers use suggested labels")
    print("   Check PR checklist items")
    print()

    print("7. ✅ Merge")
    print("   Merge to base branch")
    print("   Delete feature branch")
    print()

    # ===================================================================
    # SUMMARY
    # ===================================================================
    print_section("SUMMARY")

    print("✅ Git Workflow Assistant successfully demonstrated:")
    print(f"   • Analyzed {stats['files_changed']} changed files")
    print("   • Generated semantic commit message")
    print("   • Suggested branch names for 3 strategies")
    print("   • Created pull request content")
    print("   • Demonstrated complete workflow")
    print()

    print("🎯 Key Capabilities:")
    print("   ✅ Intelligent change analysis")
    print("   ✅ Semantic commit message generation")
    print("   ✅ Conventional branch naming")
    print("   ✅ PR content generation")
    print("   ✅ Multiple branching strategies")
    print("   ✅ Breaking change detection")
    print()

    print("📚 Next Steps:")
    print("   1. Install as git hooks")
    print("   2. Configure for your strategy")
    print("   3. Integrate with issue tracker")
    print("   4. Automate PR creation")
    print("   5. Enforce commit conventions")
    print()

    print_header("DEMONSTRATION COMPLETE")

    return 0


if __name__ == "__main__":
    sys.exit(main())

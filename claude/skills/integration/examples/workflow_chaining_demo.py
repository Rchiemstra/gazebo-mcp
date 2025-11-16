#!/usr/bin/env python3
"""
Advanced Skill Chaining Workflow Demo

Demonstrates how agents can chain multiple skills together to accomplish
complex tasks. Shows real-world workflows and best practices.

Workflows demonstrated:
1. Code Quality Pipeline - refactor → test → document
2. Feature Development - search → implement → test → review
3. Dependency Security - analyze → check vulnerabilities → check updates
4. PR Workflow - analyze → commit message → branch name → create PR
"""

import sys
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from skills.integration import SkillInvoker, SkillLoader, SkillRegistry


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


def workflow_code_quality_pipeline(invoker):
    """
    Workflow 1: Code Quality Pipeline

    Chain: refactor-assistant → test-orchestrator → doc-generator

    This workflow demonstrates how an agent can assess code quality
    by combining insights from multiple skills.
    """
    print_section("WORKFLOW 1: Code Quality Pipeline")

    target_file = "skills/integration/skill_loader.py"

    print(f"🎯 Target: {target_file}\n")
    print("Agent orchestration:")
    print("  1. Detect code smells (refactor-assistant)")
    print("  2. Analyze test coverage (test-orchestrator)")
    print("  3. Check documentation (doc-generator)")
    print("  4. Generate quality score\n")

    # Step 1: Detect code smells
    print("📋 Step 1: Analyzing code quality...")
    refactor_result = invoker.invoke(
        'refactor-assistant',
        'detect_code_smells',
        {'source_file': target_file}
    )

    if refactor_result.success:
        smells = refactor_result.data.get('code_smells', [])
        complexity = refactor_result.data.get('complexity_issues', 0)
        print(f"   ✓ Code smells found: {len(smells)}")
        print(f"   ✓ Complexity issues: {complexity}")

        if len(smells) > 0:
            print(f"   ⚠ First smell: {smells[0].get('type', 'N/A')}")
    else:
        print(f"   ✗ Error: {refactor_result.error}")
        smells = []
        complexity = 0

    # Step 2: Check test coverage
    print("\n📋 Step 2: Checking test coverage...")
    coverage_result = invoker.invoke(
        'test-orchestrator',
        'analyze_coverage',
        {'coverage_file': '.coverage', 'min_coverage': 80.0}
    )

    if coverage_result.success:
        coverage = coverage_result.data.get('overall_coverage', 0)
        uncovered = coverage_result.data.get('uncovered_lines', [])
        print(f"   ✓ Overall coverage: {coverage:.1f}%")
        print(f"   ✓ Uncovered lines: {len(uncovered)}")
    else:
        print(f"   ⚠ Coverage not available: {coverage_result.error}")
        coverage = 0

    # Step 3: Analyze documentation
    print("\n📋 Step 3: Analyzing documentation...")
    doc_result = invoker.invoke(
        'doc-generator',
        'analyze_documentation',
        {'project_path': 'skills/integration'}
    )

    if doc_result.success:
        doc_coverage = doc_result.data.get('overall_coverage', 0)
        undocumented = doc_result.data.get('total_undocumented', 0)
        print(f"   ✓ Documentation coverage: {doc_coverage:.1f}%")
        print(f"   ✓ Undocumented items: {undocumented}")
    else:
        print(f"   ⚠ Documentation analysis not available: {doc_result.error}")
        doc_coverage = 0

    # Step 4: Generate quality score
    print("\n📋 Step 4: Computing quality score...")

    # Weighted scoring
    code_quality_score = max(0, 100 - (len(smells) * 10) - (complexity * 5))
    test_score = coverage if coverage_result.success else 50
    doc_score = doc_coverage if doc_result.success else 50

    overall_score = (
        code_quality_score * 0.4 +
        test_score * 0.3 +
        doc_score * 0.3
    )

    print(f"\n📊 Quality Report:")
    print(f"   • Code Quality: {code_quality_score:.1f}/100")
    print(f"   • Test Coverage: {test_score:.1f}/100")
    print(f"   • Documentation: {doc_score:.1f}/100")
    print(f"   ───────────────────────────")
    print(f"   • Overall Score: {overall_score:.1f}/100")

    if overall_score >= 80:
        print(f"   ✅ Excellent quality!")
    elif overall_score >= 60:
        print(f"   ⚠️  Good, but room for improvement")
    else:
        print(f"   ❌ Needs attention")

    return overall_score


def workflow_dependency_security(invoker):
    """
    Workflow 2: Dependency Security Pipeline

    Chain: dependency-guardian (analyze → vulnerabilities → updates)

    This workflow shows how to chain operations from a single skill
    to build a comprehensive security assessment.
    """
    print_section("WORKFLOW 2: Dependency Security Pipeline")

    project_path = "."

    print(f"🎯 Target: {project_path}\n")
    print("Agent orchestration:")
    print("  1. Analyze dependencies (dependency-guardian)")
    print("  2. Check for vulnerabilities (dependency-guardian)")
    print("  3. Check for updates (dependency-guardian)")
    print("  4. Generate security report\n")

    # Step 1: Analyze dependencies
    print("📋 Step 1: Analyzing dependencies...")
    deps_result = invoker.invoke(
        'dependency-guardian',
        'analyze_dependencies',
        {'project_path': project_path}
    )

    if deps_result.success:
        total = deps_result.data.get('total_dependencies', 0)
        direct = deps_result.data.get('direct_dependencies', 0)
        transitive = deps_result.data.get('transitive_dependencies', 0)
        print(f"   ✓ Total dependencies: {total}")
        print(f"   ✓ Direct: {direct}, Transitive: {transitive}")
    else:
        print(f"   ✗ Error: {deps_result.error}")
        total = 0

    # Step 2: Check vulnerabilities
    print("\n📋 Step 2: Checking for vulnerabilities...")
    vuln_result = invoker.invoke(
        'dependency-guardian',
        'check_vulnerabilities',
        {'project_path': project_path}
    )

    if vuln_result.success:
        vulns = vuln_result.data.get('total_vulnerabilities', 0)
        by_severity = vuln_result.data.get('vulnerabilities_by_severity', {})

        if vulns == 0:
            print(f"   ✅ No vulnerabilities found!")
        else:
            print(f"   ⚠️  Found {vulns} vulnerabilities")
            for severity in ['critical', 'high', 'medium', 'low']:
                count = by_severity.get(severity, 0)
                if count > 0:
                    print(f"      • {severity.capitalize()}: {count}")
    else:
        print(f"   ⚠ Vulnerability check not available: {vuln_result.error}")
        vulns = 0

    # Step 3: Check for updates
    print("\n📋 Step 3: Checking for updates...")
    updates_result = invoker.invoke(
        'dependency-guardian',
        'check_updates',
        {'project_path': project_path}
    )

    if updates_result.success:
        available = updates_result.data.get('total_updates_available', 0)
        major = updates_result.data.get('major_updates', 0)
        minor = updates_result.data.get('minor_updates', 0)
        patch = updates_result.data.get('patch_updates', 0)

        print(f"   ✓ Updates available: {available}")
        if available > 0:
            print(f"      • Major: {major}, Minor: {minor}, Patch: {patch}")
    else:
        print(f"   ⚠ Update check not available: {updates_result.error}")
        available = 0
        major = 0

    # Step 4: Generate security report
    print("\n📋 Step 4: Generating security report...")

    # Calculate security score
    vuln_penalty = vulns * 20
    major_update_penalty = major * 5
    security_score = max(0, 100 - vuln_penalty - major_update_penalty)

    print(f"\n🔒 Security Report:")
    print(f"   • Dependencies: {total}")
    print(f"   • Vulnerabilities: {vulns}")
    print(f"   • Major Updates Available: {major}")
    print(f"   ───────────────────────────")
    print(f"   • Security Score: {security_score:.1f}/100")

    if security_score >= 90:
        print(f"   ✅ Excellent security posture!")
    elif security_score >= 70:
        print(f"   ⚠️  Good, but updates recommended")
    else:
        print(f"   ❌ Critical security issues found!")

    return security_score


def workflow_git_pr_creation(invoker):
    """
    Workflow 3: Git PR Creation Workflow

    Chain: git-workflow-assistant (analyze → commit → branch → PR)

    This workflow demonstrates how to automate the entire PR creation
    process by chaining git workflow operations.
    """
    print_section("WORKFLOW 3: Git PR Creation Workflow")

    print("🎯 Target: Create PR for Phase 2 skills\n")
    print("Agent orchestration:")
    print("  1. Analyze changes (git-workflow-assistant)")
    print("  2. Generate commit message (git-workflow-assistant)")
    print("  3. Suggest branch name (git-workflow-assistant)")
    print("  4. Simulate PR creation\n")

    # Step 1: Analyze changes
    print("📋 Step 1: Analyzing repository changes...")
    changes_result = invoker.invoke(
        'git-workflow-assistant',
        'analyze_changes',
        {'repo_path': '.', 'include_unstaged': False}
    )

    if changes_result.success:
        files = changes_result.data.get('files_changed', [])
        insertions = changes_result.data.get('insertions', 0)
        deletions = changes_result.data.get('deletions', 0)
        print(f"   ✓ Files changed: {len(files)}")
        print(f"   ✓ Insertions: {insertions}, Deletions: {deletions}")
    else:
        print(f"   ⚠ No changes detected: {changes_result.error}")

    # Step 2: Generate commit message
    print("\n📋 Step 2: Generating commit message...")
    commit_result = invoker.invoke(
        'git-workflow-assistant',
        'generate_commit_message',
        {
            'repo_path': '.',
            'commit_type': 'feat',
            'scope': 'skills',
            'breaking': False
        }
    )

    if commit_result.success:
        message = commit_result.data.get('message', '')
        print(f"   ✓ Generated commit message:")
        for line in message.split('\n')[:3]:
            print(f"      {line}")
    else:
        print(f"   ⚠ Message generation not available: {commit_result.error}")

    # Step 3: Suggest branch name
    print("\n📋 Step 3: Suggesting branch name...")
    branch_result = invoker.invoke(
        'git-workflow-assistant',
        'suggest_branch_name',
        {
            'description': 'Add Phase 2 skills with operations interface',
            'branch_type': 'feature',
            'issue_number': 'SKILL-789',
            'strategy': 'gitflow'
        }
    )

    if branch_result.success:
        branch_name = branch_result.data.get('branch_name', '')
        print(f"   ✓ Suggested branch: {branch_name}")
        print(f"   ✓ Strategy: {branch_result.data.get('strategy', 'N/A')}")
    else:
        print(f"   ✗ Error: {branch_result.error}")

    # Step 4: Simulate PR creation
    print("\n📋 Step 4: Simulating PR creation...")
    print(f"   ℹ️  Would create PR:")
    print(f"      • Branch: {branch_result.data.get('branch_name', 'N/A') if branch_result.success else 'N/A'}")
    print(f"      • Base: main")
    print(f"      • Title: From commit message")
    print(f"      • Body: Generated from changes")

    return branch_result.success


def workflow_code_search_refactor(invoker):
    """
    Workflow 4: Code Search → Refactor

    Chain: code-search (find usages) → refactor-assistant (suggest refactorings)

    This workflow shows how to use code search to understand impact
    before making refactoring decisions.
    """
    print_section("WORKFLOW 4: Code Search & Refactor Pipeline")

    target_symbol = "SkillInvoker"
    project_path = "skills"

    print(f"🎯 Target: Refactor '{target_symbol}'\n")
    print("Agent orchestration:")
    print("  1. Find symbol definition (code-search)")
    print("  2. Find all usages (code-search)")
    print("  3. Analyze complexity (refactor-assistant)")
    print("  4. Suggest refactorings\n")

    # Step 1: Find definition
    print(f"📋 Step 1: Finding definition of '{target_symbol}'...")
    def_result = invoker.invoke(
        'code-search',
        'find_definition',
        {
            'project_path': project_path,
            'symbol_name': target_symbol
        }
    )

    if def_result.success and def_result.data.get('found'):
        definition = def_result.data.get('definition', {})
        file_path = definition.get('file_path', 'N/A')
        line = definition.get('line_number', 0)
        print(f"   ✓ Found at {file_path}:{line}")
    else:
        print(f"   ⚠ Definition not found: {def_result.error}")
        file_path = None

    # Step 2: Find usages
    print(f"\n📋 Step 2: Finding usages of '{target_symbol}'...")
    usage_result = invoker.invoke(
        'code-search',
        'find_usages',
        {
            'project_path': project_path,
            'symbol_name': target_symbol,
            'include_tests': True
        }
    )

    if usage_result.success:
        usages = usage_result.data.get('total_usages', 0)
        files = usage_result.data.get('files_searched', 0)
        print(f"   ✓ Found {usages} usages")
        print(f"   ✓ Searched {files} files")
    else:
        print(f"   ⚠ Usage search failed: {usage_result.error}")
        usages = 0

    # Step 3: Analyze complexity (if we found the file)
    if file_path and def_result.success:
        print(f"\n📋 Step 3: Analyzing complexity...")
        complexity_result = invoker.invoke(
            'refactor-assistant',
            'analyze_complexity',
            {'source_file': file_path}
        )

        if complexity_result.success:
            avg_complexity = complexity_result.data.get('average_complexity', 0)
            max_complexity = complexity_result.data.get('max_complexity', 0)
            print(f"   ✓ Average complexity: {avg_complexity:.1f}")
            print(f"   ✓ Max complexity: {max_complexity:.1f}")
        else:
            print(f"   ⚠ Complexity analysis failed: {complexity_result.error}")

    # Step 4: Make refactoring decision
    print(f"\n📋 Step 4: Refactoring recommendation...")
    if usages > 10:
        print(f"   ⚠️  High impact change ({usages} usages)")
        print(f"   ℹ️  Recommendation: Proceed with caution")
        print(f"      • Consider deprecation strategy")
        print(f"      • Update all usages atomically")
        print(f"      • Add comprehensive tests")
    elif usages > 0:
        print(f"   ✓ Moderate impact ({usages} usages)")
        print(f"   ℹ️  Recommendation: Safe to refactor")
        print(f"      • Update usages in same commit")
    else:
        print(f"   ✓ No usages found - safe to remove or refactor")

    return True


def main():
    """Run all workflow demonstrations."""
    print_header("ADVANCED SKILL CHAINING WORKFLOWS")
    print("Demonstrating real-world agent orchestration patterns\n")

    # Initialize integration layer
    print("Initializing skill system...")
    registry = SkillRegistry('skills')
    skills = registry.discover_skills()
    loader = SkillLoader(registry)
    invoker = SkillInvoker(loader)

    print(f"✅ Loaded {len(skills)} skills")
    print()

    # Run workflows
    results = {}

    try:
        results['quality'] = workflow_code_quality_pipeline(invoker)
    except Exception as e:
        print(f"❌ Workflow 1 failed: {e}")
        results['quality'] = 0

    try:
        results['security'] = workflow_dependency_security(invoker)
    except Exception as e:
        print(f"❌ Workflow 2 failed: {e}")
        results['security'] = 0

    try:
        results['git'] = workflow_git_pr_creation(invoker)
    except Exception as e:
        print(f"❌ Workflow 3 failed: {e}")
        results['git'] = False

    try:
        results['search'] = workflow_code_search_refactor(invoker)
    except Exception as e:
        print(f"❌ Workflow 4 failed: {e}")
        results['search'] = False

    # Display metrics
    print_section("WORKFLOW METRICS")

    print("📊 Per-Skill Invocation Metrics:\n")
    for skill_name in registry.list_skills():
        metrics = invoker.get_metrics(skill_name)
        if metrics and metrics.total_invocations > 0:
            success_rate = (1 - metrics.error_rate) * 100
            print(f"  • {skill_name}:")
            print(f"      Invocations: {metrics.total_invocations}")
            print(f"      Success Rate: {success_rate:.1f}%")
            print(f"      Avg Duration: {metrics.avg_duration:.3f}s")

    # Summary
    print_section("SUMMARY")

    print("✅ Demonstrated workflows:")
    print(f"   1. Code Quality Pipeline - Score: {results.get('quality', 0):.1f}/100")
    print(f"   2. Dependency Security - Score: {results.get('security', 0):.1f}/100")
    print(f"   3. Git PR Creation - {'✅ Success' if results.get('git') else '⚠️  Partial'}")
    print(f"   4. Code Search & Refactor - {'✅ Success' if results.get('search') else '⚠️  Partial'}")
    print()

    print("🎯 Key Patterns Demonstrated:")
    print("   • Multi-skill orchestration")
    print("   • Sequential operation chaining")
    print("   • Data flow between skills")
    print("   • Error handling & fallbacks")
    print("   • Conditional logic based on results")
    print("   • Quality scoring & reporting")
    print()

    print("🚀 The skill integration layer enables agents to:")
    print("   • Compose complex workflows from simple operations")
    print("   • Make intelligent decisions based on skill results")
    print("   • Handle errors gracefully across skill boundaries")
    print("   • Track performance and quality metrics")
    print()

    print_header("ALL WORKFLOWS COMPLETE")

    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Refactor Assistant Demonstration

Demonstrates the refactor-assistant skill capabilities.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from refactor_assistant import detect_code_smells, suggest_refactorings


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
        'low': '🔵'
    }
    return icons.get(severity, '⚪')


def main():
    """Run the demonstration."""
    print_header("REFACTOR ASSISTANT DEMONSTRATION")

    # Get example file
    legacy_file = Path(__file__).parent / "examples" / "legacy_code.py"

    if not legacy_file.exists():
        print(f"Error: Example file not found: {legacy_file}")
        return 1

    print(f"📄 Analyzing: {legacy_file}\n")

    # ===================================================================
    # PART 1: CODE SMELL DETECTION
    # ===================================================================
    print_section("PART 1: CODE SMELL DETECTION")

    print("🔍 Scanning for code smells...\n")

    result = detect_code_smells(str(legacy_file), severity_threshold="low")

    print(f"📊 Analysis Results:")
    print(f"   Total code smells: {result['total_smells']}")
    print()
    print(f"   Severity Breakdown:")
    print(f"   🔴 Critical: {result['by_severity']['critical']}")
    print(f"   🟠 High:     {result['by_severity']['high']}")
    print(f"   🟡 Medium:   {result['by_severity']['medium']}")
    print(f"   🔵 Low:      {result['by_severity']['low']}")
    print()

    print(f"   File Metrics:")
    print(f"   Total lines: {result['metrics']['total_lines']}")
    print(f"   Total functions: {result['metrics']['total_functions']}")
    print(f"   Total classes: {result['metrics']['total_classes']}")

    # Group smells by type
    smells_by_type = {}
    for smell in result['smells']:
        smell_type = smell['type']
        if smell_type not in smells_by_type:
            smells_by_type[smell_type] = []
        smells_by_type[smell_type].append(smell)

    print("\n📋 Code Smells by Type:\n")

    for smell_type, smells in sorted(smells_by_type.items()):
        count = len(smells)
        print(f"   • {smell_type.replace('_', ' ').title()}: {count}")

    # Show detailed smells
    print("\n📝 Detailed Code Smells:\n")

    # Sort by severity
    severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
    sorted_smells = sorted(
        result['smells'],
        key=lambda s: (severity_order[s['severity']], s['line'])
    )

    # Show first 10
    for i, smell in enumerate(sorted_smells[:10], 1):
        icon = severity_icon(smell['severity'])
        print(f"{i}. {icon} {smell['severity'].upper()}: {smell['type'].replace('_', ' ').title()}")
        print(f"   Line {smell['line']}")

        if smell['function']:
            print(f"   Function: {smell['function']}")
        if smell['class']:
            print(f"   Class: {smell['class']}")

        print(f"   📝 {smell['description']}")
        print(f"   💡 {smell['suggestion']}")

        if smell['metrics']:
            print(f"   📊 Metrics: {smell['metrics']}")

        print()

    if len(sorted_smells) > 10:
        print(f"   ... and {len(sorted_smells) - 10} more code smells")

    # ===================================================================
    # PART 2: REFACTORING SUGGESTIONS
    # ===================================================================
    print_section("PART 2: REFACTORING SUGGESTIONS")

    print("💡 Generating refactoring suggestions...\n")

    suggestions = suggest_refactorings(str(legacy_file), max_suggestions=5)

    print(f"Found {suggestions['total_suggestions']} refactoring opportunities:\n")

    for i, suggestion in enumerate(suggestions['suggestions'], 1):
        impact_bar = "█" * int(suggestion['estimated_impact'] / 10)
        impact_bar += "░" * (10 - len(impact_bar))

        print(f"{i}. {suggestion['type'].replace('_', ' ').title()}")
        print(f"   Line {suggestion['line']}")
        print(f"   📝 {suggestion['description']}")
        print(f"   📊 Impact: [{impact_bar}] {suggestion['estimated_impact']:.0f}%")

        if suggestion['parameters']:
            print(f"   Parameters: {suggestion['parameters']}")

        print()

    # ===================================================================
    # PART 3: IMPACT ANALYSIS
    # ===================================================================
    print_section("PART 3: IMPACT ANALYSIS")

    print("📊 Code Quality Assessment:\n")

    # Calculate quality score
    total_lines = result['metrics']['total_lines']
    smells_per_100_lines = (result['total_smells'] / total_lines) * 100

    # Base score
    quality_score = 100

    # Deduct for smells
    quality_score -= result['by_severity']['critical'] * 20
    quality_score -= result['by_severity']['high'] * 10
    quality_score -= result['by_severity']['medium'] * 5
    quality_score -= result['by_severity']['low'] * 2

    quality_score = max(0, quality_score)

    print(f"   Overall Quality Score: {quality_score:.1f}/100")
    print(f"   Code Smells Density: {smells_per_100_lines:.1f} smells per 100 lines")
    print()

    if quality_score >= 80:
        print("   ✅ EXCELLENT: Code is clean and maintainable")
    elif quality_score >= 60:
        print("   🟢 GOOD: Some minor improvements needed")
    elif quality_score >= 40:
        print("   🟡 FAIR: Significant refactoring recommended")
    elif quality_score >= 20:
        print("   🟠 POOR: Major refactoring required")
    else:
        print("   🔴 CRITICAL: Urgent refactoring needed")

    print("\n📈 Refactoring Priority:\n")

    # Group high-priority issues
    high_priority = [
        s for s in result['smells']
        if s['severity'] in ['critical', 'high']
    ]

    print(f"   1. Address {len(high_priority)} critical/high severity issues")

    # God classes
    god_classes = [s for s in result['smells'] if s['type'] == 'god_class']
    if god_classes:
        print(f"   2. Break down {len(god_classes)} god class(es)")

    # Complex functions
    complex_funcs = [s for s in result['smells'] if s['type'] == 'complex_function']
    if complex_funcs:
        print(f"   3. Simplify {len(complex_funcs)} complex function(s)")

    # Long functions
    long_funcs = [s for s in result['smells'] if s['type'] == 'long_function']
    if long_funcs:
        print(f"   4. Extract methods from {len(long_funcs)} long function(s)")

    # Duplicate code
    duplicates = [s for s in result['smells'] if s['type'] == 'duplicate_code']
    if duplicates:
        print(f"   5. Remove {len(duplicates)} duplicate code block(s)")

    # ===================================================================
    # PART 4: AGENT INTEGRATION EXAMPLES
    # ===================================================================
    print_section("PART 4: AGENT INTEGRATION")

    print("🤖 How agents can use refactor-assistant:\n")

    print("1. 🔄 Continuous Quality Improvement")
    print("   Agent analyzes code on every commit")
    print("   Suggests refactorings for new code")
    print("   Tracks quality metrics over time")
    print()

    print("2. 🎯 Technical Debt Reduction")
    print("   Agent identifies high-priority refactorings")
    print("   Creates issues for each code smell")
    print("   Proposes refactoring PRs")
    print()

    print("3. 📝 Pre-Review Cleanup")
    print("   Agent refactors code before review")
    print("   Applies safe, automated transformations")
    print("   Ensures code meets quality standards")
    print()

    print("4. 🧪 Test-Driven Refactoring")
    print("   Agent runs tests before refactoring")
    print("   Applies refactoring")
    print("   Verifies tests still pass")
    print("   Rolls back if tests fail")
    print()

    print("5. 📊 Quality Gate Enforcement")
    print("   Agent blocks merges if quality score too low")
    print("   Requires critical smells to be fixed")
    print("   Tracks quality trends")

    # ===================================================================
    # PART 5: REFACTORING WORKFLOW
    # ===================================================================
    print_section("PART 5: RECOMMENDED WORKFLOW")

    print("🔧 Step-by-Step Refactoring Process:\n")

    print("1. 📸 Commit Current State")
    print("   git commit -am 'Pre-refactoring snapshot'")
    print()

    print("2. 🔍 Detect Code Smells")
    print(f"   refactor-assistant detect {legacy_file}")
    print()

    print("3. 🎯 Prioritize by Impact")
    print("   Focus on critical/high severity first")
    print("   Address code smells that affect multiple areas")
    print()

    print("4. 🧪 Ensure Test Coverage")
    print("   Use test-orchestrator to generate tests")
    print("   Aim for >80% coverage before refactoring")
    print()

    print("5. 🔧 Apply Refactorings")
    print("   Start with safe, automated refactorings")
    print("   Apply one refactoring at a time")
    print("   Run tests after each change")
    print()

    print("6. ✅ Verify Quality Improvement")
    print("   Re-run smell detection")
    print("   Confirm quality score increased")
    print("   Ensure all tests pass")
    print()

    print("7. 📝 Commit and Review")
    print("   git commit -am 'Refactor: <description>'")
    print("   Create PR for team review")

    # ===================================================================
    # SUMMARY
    # ===================================================================
    print_section("SUMMARY")

    print("✅ Refactor Assistant successfully demonstrated:")
    print(f"   • Detected {result['total_smells']} code smells")
    print(f"   • Identified {len(high_priority)} critical issues")
    print(f"   • Generated {suggestions['total_suggestions']} refactoring suggestions")
    print(f"   • Calculated quality score: {quality_score:.1f}/100")
    print()

    print("🎯 Key Features:")
    print("   ✅ 15+ code smell detectors")
    print("   ✅ Severity classification")
    print("   ✅ Actionable suggestions")
    print("   ✅ Impact analysis")
    print("   ✅ Agent-ready API")
    print()

    print("📚 Next Steps:")
    print("   1. Review detected code smells")
    print("   2. Prioritize refactorings by impact")
    print("   3. Generate tests (test-orchestrator)")
    print("   4. Apply refactorings incrementally")
    print("   5. Verify improvements")
    print()

    print_header("DEMONSTRATION COMPLETE")

    return 0


if __name__ == "__main__":
    sys.exit(main())

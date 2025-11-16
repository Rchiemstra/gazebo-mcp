#!/usr/bin/env python3
"""
Doc Generator Demonstration

Demonstrates automated documentation generation capabilities.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from doc_generator import (
    analyze_documentation,
    generate_docstrings,
    generate_readme
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
    print_header("DOC GENERATOR DEMONSTRATION")

    examples_dir = Path(__file__).parent / 'examples'
    undocumented_file = examples_dir / 'undocumented_code.py'

    # ===================================================================
    # PART 1: ANALYZE DOCUMENTATION COVERAGE
    # ===================================================================
    print_section("PART 1: ANALYZE DOCUMENTATION COVERAGE")

    print("Analyzing documentation coverage...\n")

    result = analyze_documentation(str(examples_dir))

    print("Analysis Results:")
    print(f"  Coverage Score: {result['coverage_score']:.1f}%")
    print(f"  Quality Score: {result['quality_score']:.1f}%")
    print()

    print("Statistics:")
    stats = result['statistics']
    print(f"  Modules Analyzed: {stats['modules_analyzed']}")
    print(f"  Functions Analyzed: {stats['functions_analyzed']}")
    print(f"  Classes Analyzed: {stats['classes_analyzed']}")
    print(f"  Documented Functions: {stats['documented_functions']}/{stats['functions_analyzed']}")
    print(f"  Documented Classes: {stats['documented_classes']}/{stats['classes_analyzed']}")
    print()

    if result['missing_docstrings']:
        print(f"Missing Docstrings ({len(result['missing_docstrings'])}):")
        for item in result['missing_docstrings'][:10]:
            print(f"  - {item}")
        if len(result['missing_docstrings']) > 10:
            print(f"  ... and {len(result['missing_docstrings']) - 10} more")
        print()

    if result['quality_issues']:
        print(f"Quality Issues ({len(result['quality_issues'])}):")
        for issue in result['quality_issues'][:8]:
            severity_emoji = {
                'high': '🔴',
                'medium': '🟡',
                'low': '🔵'
            }.get(issue['severity'], '⚪')
            print(f"  {severity_emoji} [{issue['severity'].upper()}] {issue['description']}")
            print(f"     {issue['location']}:{issue['line_number']}")
            print(f"     💡 {issue['suggestion']}")
            print()

        if len(result['quality_issues']) > 8:
            print(f"  ... and {len(result['quality_issues']) - 8} more issues\n")

    print("Recommendations:")
    for rec in result['recommendations']:
        print(f"  {rec}")

    # ===================================================================
    # PART 2: GENERATE DOCSTRINGS
    # ===================================================================
    print_section("PART 2: GENERATE DOCSTRINGS")

    print("Generating docstrings for undocumented code...\n")

    # Test all three styles
    styles = ['google', 'numpy', 'sphinx']

    for style in styles:
        print(f"Generating {style.upper()} style docstrings...\n")

        result = generate_docstrings(
            file_path=str(undocumented_file),
            style=style,
            include_examples=True
        )

        print(f"Results:")
        print(f"  Docstrings Added: {result['docstrings_added']}")
        print(f"  Docstrings Updated: {result['docstrings_updated']}")
        print(f"  Coverage: {result['coverage_before']:.1f}% → {result['coverage_after']:.1f}%")
        print()

        if result['generated'] and style == 'google':
            # Show example docstring
            first_gen = result['generated'][0]
            print(f"Example Generated Docstring ({first_gen['target']}):")
            print("─" * 60)
            print(first_gen['generated'])
            print("─" * 60)
            print()

    # Show documented code sample
    print("Sample of documented code:")
    print("─" * 80)

    # Generate with Google style for display
    result = generate_docstrings(
        file_path=str(undocumented_file),
        style='google',
        include_examples=True
    )

    # Show first 30 lines
    lines = result['documented_code'].splitlines()[:30]
    for i, line in enumerate(lines, 1):
        print(f"{i:3} | {line}")

    if len(result['documented_code'].splitlines()) > 30:
        print(f"... ({len(result['documented_code'].splitlines()) - 30} more lines)")

    print("─" * 80)

    # ===================================================================
    # PART 3: GENERATE README
    # ===================================================================
    print_section("PART 3: GENERATE README")

    print("Generating README for doc_generator project...\n")

    project_dir = Path(__file__).parent
    result = generate_readme(
        project_path=str(project_dir),
        include_api=True,
        include_examples=True
    )

    print("README Generation Results:")
    print(f"  Sections Generated: {len(result['sections_generated'])}")
    for section in result['sections_generated']:
        print(f"    - {section}")
    print()

    print("Generated README Preview:")
    print("=" * 80)

    # Show first 50 lines
    readme_lines = result['readme_content'].splitlines()
    for line in readme_lines[:50]:
        print(line)

    if len(readme_lines) > 50:
        print(f"\n... ({len(readme_lines) - 50} more lines)")

    print("=" * 80)

    # ===================================================================
    # PART 4: DOCSTRING STYLE COMPARISON
    # ===================================================================
    print_section("PART 4: DOCSTRING STYLE COMPARISON")

    print("Comparing different docstring styles for the same function:\n")

    # Generate with each style
    styles_comparison = {}
    for style in ['google', 'numpy', 'sphinx']:
        result = generate_docstrings(
            file_path=str(undocumented_file),
            style=style,
            include_examples=False
        )
        if result['generated']:
            # Find the calculate_metrics function
            for gen in result['generated']:
                if gen['target'] == 'calculate_metrics':
                    styles_comparison[style] = gen['generated']
                    break

    for style, docstring in styles_comparison.items():
        print(f"{style.upper()} Style:")
        print("─" * 60)
        print(docstring)
        print("─" * 60)
        print()

    # ===================================================================
    # PART 5: USE CASES
    # ===================================================================
    print_section("PART 5: USE CASES")

    print("How doc-generator can be used:\n")

    print("1. 📚 New Project Bootstrap")
    print("   Generate comprehensive README for new projects")
    print("   Initialize documentation structure")
    print()

    print("2. 🔄 Legacy Code Documentation")
    print("   Add missing docstrings to undocumented code")
    print("   Improve documentation coverage")
    print()

    print("3. 🎯 Documentation Quality Gate")
    print("   Enforce documentation standards in CI/CD")
    print("   Block PRs with low documentation coverage")
    print()

    print("4. 📖 API Documentation")
    print("   Generate API reference from code")
    print("   Keep documentation in sync with code")
    print()

    print("5. ✅ Documentation Audit")
    print("   Analyze documentation quality")
    print("   Identify missing or incomplete docs")
    print()

    print("6. 🔧 IDE Integration")
    print("   Auto-generate docstrings on save")
    print("   Suggest documentation improvements")
    print()

    print("7. 🤖 PR Review Integration")
    print("   Check documentation in pull requests")
    print("   Require docs for new functions/classes")
    print()

    # ===================================================================
    # PART 6: INTEGRATION WITH OTHER SKILLS
    # ===================================================================
    print_section("PART 6: INTEGRATION WITH OTHER SKILLS")

    print("doc-generator works with other skills:\n")

    print("With test-orchestrator:")
    print("  1. Generate tests with test-orchestrator")
    print("  2. Add docstrings to tests with doc-generator")
    print("  3. Complete test documentation automatically")
    print()

    print("With refactor-assistant:")
    print("  1. Refactor code with refactor-assistant")
    print("  2. Update documentation with doc-generator")
    print("  3. Keep docs in sync with code changes")
    print()

    print("With pr-review-assistant:")
    print("  1. Review PR with pr-review-assistant")
    print("  2. Check documentation coverage with doc-generator")
    print("  3. Require 80%+ coverage for approval")
    print()

    print("With dependency-guardian:")
    print("  1. Analyze dependencies with dependency-guardian")
    print("  2. Generate README with dependency info")
    print("  3. Keep installation docs up to date")
    print()

    # ===================================================================
    # PART 7: WORKFLOW EXAMPLE
    # ===================================================================
    print_section("PART 7: AUTOMATED DOCUMENTATION WORKFLOW")

    print("Complete documentation workflow:\n")

    print("1. 📝 Developer writes code")
    print("   Focus on implementation, not docs")
    print()

    print("2. 🤖 Pre-commit hook runs doc-generator")
    print("   Analyze documentation coverage")
    print("   Generate missing docstrings")
    print()

    print("3. ✅ Commit with documentation")
    print("   Code and docs committed together")
    print("   Always in sync")
    print()

    print("4. 🔍 CI/CD checks documentation")
    print("   Verify 80%+ coverage requirement")
    print("   Check docstring quality")
    print()

    print("5. 📚 Auto-generate README")
    print("   Update README on main branch")
    print("   Keep project docs current")
    print()

    print("6. 🌐 Deploy documentation")
    print("   Generate API docs")
    print("   Publish to documentation site")
    print()

    # ===================================================================
    # SUMMARY
    # ===================================================================
    print_section("SUMMARY")

    print("✅ Doc Generator successfully demonstrated:")
    print("   • Documentation coverage analysis")
    print("   • Docstring generation (Google, NumPy, Sphinx)")
    print("   • README generation")
    print("   • Quality issue detection")
    print("   • Multiple integration patterns")
    print()

    print("🎯 Key Capabilities:")
    print("   ✅ Analyze documentation coverage and quality")
    print("   ✅ Generate comprehensive docstrings")
    print("   ✅ Support multiple docstring styles")
    print("   ✅ Generate project README files")
    print("   ✅ Detect documentation issues")
    print("   ✅ Provide actionable recommendations")
    print()

    print("📚 Next Steps:")
    print("   1. Integrate into development workflow")
    print("   2. Set documentation quality gates")
    print("   3. Automate README generation")
    print("   4. Connect with other skills")
    print("   5. Enforce documentation standards")
    print()

    print_header("DEMONSTRATION COMPLETE")

    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Spec to Implementation Demonstration

Demonstrates automated implementation from specifications.
"""

import sys
from pathlib import Path
import shutil

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from spec_to_implementation import implement_from_spec, analyze_spec


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
    print_header("SPEC TO IMPLEMENTATION DEMONSTRATION")

    spec_file = Path(__file__).parent / 'examples' / 'email_validator_spec.md'
    output_dir = Path(__file__).parent / 'examples' / 'generated_output'

    # Clean output directory if it exists
    if output_dir.exists():
        shutil.rmtree(output_dir)

    # ===================================================================
    # PART 1: ANALYZE SPECIFICATION
    # ===================================================================
    print_section("PART 1: ANALYZE SPECIFICATION")

    print(f"Analyzing specification: {spec_file.name}\n")

    analysis = analyze_spec(spec_file=str(spec_file))

    print("Specification Analysis:")
    print(f"  Total requirements: {len(analysis['requirements'])}")
    print(f"  Complexity estimate: {analysis['complexity_estimate']}")
    print(f"  Total risks: {len(analysis['risks'])}")
    print()

    print("Requirements:")
    for i, req in enumerate(analysis['requirements'], 1):
        print(f"  {i}. [{req['priority'].upper()}] {req['description']}")
    print()

    print("Implementation Plan:")
    plan = analysis['implementation_plan']
    print(f"  Title: {plan['title']}")
    print(f"  Total tasks: {len(plan['tasks'])}")
    print(f"  Files to create: {len(plan['files_to_create'])}")
    print()

    print("Tasks:")
    for task in plan['tasks']:
        complexity_emoji = {
            'trivial': '⚪',
            'simple': '🟢',
            'moderate': '🟡',
            'complex': '🟠',
            'very_complex': '🔴'
        }.get(task['complexity'], '⚪')

        print(f"  {task['id']} {complexity_emoji} [{task['type']}] {task['description']}")
    print()

    if analysis['risks']:
        print("⚠️  Identified Risks:")
        for risk in analysis['risks']:
            print(f"  - {risk}")
        print()

    # ===================================================================
    # PART 2: GENERATE IMPLEMENTATION
    # ===================================================================
    print_section("PART 2: GENERATE IMPLEMENTATION")

    print(f"Generating implementation to: {output_dir}\n")
    print("This will:")
    print("  1. Parse the specification")
    print("  2. Create implementation plan")
    print("  3. Generate code scaffolding")
    print("  4. Implement requirements")
    print("  5. Generate tests")
    print("  6. Add documentation")
    print("  7. Validate quality")
    print()

    result = implement_from_spec(
        spec_file=str(spec_file),
        output_dir=str(output_dir),
        quality_threshold=70.0,
        include_tests=True,
        include_docs=True
    )

    if result['success']:
        print("✅ Implementation SUCCESSFUL!\n")

        print(f"Results:")
        print(f"  Files created: {len(result['files_created'])}")
        print(f"  Tests generated: {result['tests_generated']}")
        print(f"  Quality score: {result['quality_score']:.1f}/100")
        print()

        print("Created files:")
        for file_path in sorted(result['files_created']):
            rel_path = Path(file_path).relative_to(output_dir)
            print(f"  ✓ {rel_path}")
        print()

    else:
        print("❌ Implementation FAILED\n")

        if result['errors']:
            print("Errors:")
            for error in result['errors']:
                print(f"  ❌ {error}")
            print()

    if result['warnings']:
        print("Warnings:")
        for warning in result['warnings']:
            print(f"  ⚠️  {warning}")
        print()

    # ===================================================================
    # PART 3: SHOW GENERATED CODE
    # ===================================================================
    print_section("PART 3: GENERATED CODE PREVIEW")

    if output_dir.exists():
        # Find main module
        python_files = list(output_dir.rglob("*.py"))

        if python_files:
            # Show core.py if it exists
            core_files = [f for f in python_files if f.name == 'core.py']

            if core_files:
                core_file = core_files[0]
                print(f"Preview of {core_file.relative_to(output_dir)}:")
                print("=" * 80)

                with open(core_file, 'r') as f:
                    lines = f.readlines()

                for i, line in enumerate(lines[:30], 1):
                    print(f"{i:3} | {line}", end='')

                if len(lines) > 30:
                    print(f"\n... ({len(lines) - 30} more lines)")

                print("=" * 80)
                print()

        # Show README if it exists
        readme_files = list(output_dir.rglob("README.md"))
        if readme_files:
            readme_file = readme_files[0]
            print(f"\nPreview of {readme_file.relative_to(output_dir)}:")
            print("=" * 80)

            with open(readme_file, 'r') as f:
                content = f.read()

            print(content[:500])
            if len(content) > 500:
                print(f"\n... ({len(content) - 500} more characters)")

            print("=" * 80)

    # ===================================================================
    # PART 4: VALIDATION RESULTS
    # ===================================================================
    print_section("PART 4: VALIDATION RESULTS")

    validation = result.get('validation_results', {})

    if validation:
        print("Quality Validation:")
        print(f"  Overall score: {validation.get('quality_score', 0):.1f}/100")
        print()

        if validation.get('passed_checks'):
            print("✅ Passed checks:")
            for check in validation['passed_checks']:
                print(f"  ✓ {check}")
            print()

        if validation.get('issues'):
            print("⚠️  Issues found:")
            for issue in validation['issues']:
                print(f"  • {issue}")
            print()
    else:
        print("Validation not available (skills not loaded)")
        print()

    # ===================================================================
    # PART 5: USE CASES
    # ===================================================================
    print_section("PART 5: USE CASES")

    print("How spec-to-implementation can be used:\n")

    print("1. 🚀 Rapid Prototyping")
    print("   Transform ideas into working code in minutes")
    print("   Get from specification to prototype quickly")
    print()

    print("2. 📋 Template Generation")
    print("   Generate boilerplate for new features")
    print("   Consistent code structure across projects")
    print()

    print("3. 🎓 Learning Tool")
    print("   See how specifications map to code")
    print("   Learn implementation patterns")
    print()

    print("4. 🔄 Specification Validation")
    print("   Test if specification is implementable")
    print("   Identify ambiguities and gaps")
    print()

    print("5. 🏗️  Code Scaffolding")
    print("   Generate project structure")
    print("   Create tests and documentation")
    print()

    print("6. 📚 Documentation Generation")
    print("   Auto-generate docs from specs")
    print("   Keep docs in sync with requirements")
    print()

    print("7. 🤝 Team Collaboration")
    print("   Standardize implementation from specs")
    print("   Consistent code across team")
    print()

    # ===================================================================
    # PART 6: WORKFLOW INTEGRATION
    # ===================================================================
    print_section("PART 6: WORKFLOW INTEGRATION")

    print("Spec-to-implementation workflow:\n")

    print("1. 📝 Write Specification")
    print("   Product owner writes feature spec in markdown")
    print("   Include requirements, constraints, examples")
    print()

    print("2. 🔍 Analyze Specification")
    print("   Run analyze_spec() to validate")
    print("   Review complexity and risks")
    print()

    print("3. ✅ Approve Plan")
    print("   Review implementation plan")
    print("   Adjust quality thresholds if needed")
    print()

    print("4. 🔨 Generate Implementation")
    print("   Run implement_from_spec()")
    print("   Code, tests, and docs generated automatically")
    print()

    print("5. 👨‍💻 Developer Review")
    print("   Developer reviews generated code")
    print("   Adds business logic and refinements")
    print()

    print("6. 🧪 Run Tests")
    print("   Execute generated tests")
    print("   Add additional test cases")
    print()

    print("7. 📦 Commit & Deploy")
    print("   Commit implementation")
    print("   Deploy to production")
    print()

    # ===================================================================
    # PART 7: INTEGRATION WITH OTHER SKILLS
    # ===================================================================
    print_section("PART 7: INTEGRATION WITH OTHER SKILLS")

    print("Spec-to-implementation orchestrates all skills:\n")

    print("Uses code-search:")
    print("  • Find similar implementations")
    print("  • Discover existing patterns")
    print("  • Avoid duplicate code")
    print()

    print("Uses test-orchestrator:")
    print("  • Generate comprehensive tests")
    print("  • Ensure test coverage")
    print("  • Validate requirements")
    print()

    print("Uses doc-generator:")
    print("  • Add docstrings")
    print("  • Generate README")
    print("  • Create API documentation")
    print()

    print("Uses refactor-assistant:")
    print("  • Check for code smells")
    print("  • Suggest improvements")
    print("  • Optimize generated code")
    print()

    print("Uses pr-review-assistant:")
    print("  • Validate quality")
    print("  • Check best practices")
    print("  • Ensure standards compliance")
    print()

    print("Uses dependency-guardian:")
    print("  • Validate dependencies")
    print("  • Check for vulnerabilities")
    print("  • Suggest alternatives")
    print()

    # ===================================================================
    # SUMMARY
    # ===================================================================
    print_section("SUMMARY")

    print("✅ Spec to Implementation successfully demonstrated:")
    if result['success']:
        print(f"   • Analyzed {len(analysis['requirements'])} requirements")
        print(f"   • Generated {len(result['files_created'])} files")
        print(f"   • Created {result['tests_generated']} test files")
        print(f"   • Achieved {result['quality_score']:.1f}/100 quality score")
    else:
        print("   • Parsed specification successfully")
        print("   • Created implementation plan")
        print("   • Demonstrated workflow")
    print()

    print("🎯 Key Capabilities:")
    print("   ✅ Parse specifications (markdown, plain text)")
    print("   ✅ Analyze requirements and complexity")
    print("   ✅ Generate implementation plans")
    print("   ✅ Create code scaffolding")
    print("   ✅ Generate tests and documentation")
    print("   ✅ Validate quality")
    print("   ✅ Orchestrate multiple skills")
    print()

    print("📚 Next Steps:")
    print("   1. Try with your own specifications")
    print("   2. Adjust quality thresholds")
    print("   3. Customize code generation templates")
    print("   4. Integrate into your workflow")
    print("   5. Extend with custom validators")
    print()

    print_header("DEMONSTRATION COMPLETE")

    return 0


if __name__ == "__main__":
    sys.exit(main())

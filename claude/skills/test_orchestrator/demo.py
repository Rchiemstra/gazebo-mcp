#!/usr/bin/env python3
"""
Test Orchestrator Demonstration

This script demonstrates the test-orchestrator skill by:
1. Analyzing a sample Python module
2. Generating comprehensive test scaffolds
3. Displaying the results
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from core.analyzer import CodeAnalyzer
from core.test_generator import TestGenerator


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def print_section(text):
    """Print a formatted section header."""
    print("\n" + "-" * 70)
    print(f"  {text}")
    print("-" * 70 + "\n")


def main():
    """Run the demonstration."""
    print_header("TEST ORCHESTRATOR DEMONSTRATION")

    # Path to sample module
    sample_file = Path(__file__).parent / "examples" / "sample_payment_service.py"

    if not sample_file.exists():
        print(f"Error: Sample file not found: {sample_file}")
        return 1

    print(f"Analyzing: {sample_file}\n")

    # Step 1: Analyze the code
    print_section("STEP 1: CODE ANALYSIS")

    analyzer = CodeAnalyzer()
    analysis = analyzer.analyze_file(str(sample_file))

    print(f"Total functions analyzed: {analysis.total_functions}")
    print(f"Total complexity: {analysis.total_complexity}")
    print(f"Imports detected: {len(analysis.imports)}")
    print()

    # Display function details
    print("Functions found:")
    for func in analysis.functions:
        print(f"\n  • {func.name}()")
        print(f"    Parameters: {', '.join(func.params) if func.params else 'None'}")
        print(f"    Returns: {func.returns or 'None'}")
        print(f"    Complexity: {func.complexity}")
        print(f"    Raises: {', '.join(func.raises) if func.raises else 'None'}")
        print(f"    Edge cases detected: {', '.join(func.edge_cases) if func.edge_cases else 'None'}")
        if func.dependencies:
            print(f"    Dependencies: {', '.join(func.dependencies)}")

    # Step 2: Generate tests
    print_section("STEP 2: TEST GENERATION")

    generator = TestGenerator()
    test_suite = generator.generate_tests(analysis)

    print(f"Generated {len(test_suite.tests)} tests")
    print(f"Target test file: {test_suite.file_path}")
    print()

    # Display generated tests summary
    print("Test breakdown:")
    test_types = {}
    for test in test_suite.tests:
        test_types[test.test_type] = test_types.get(test.test_type, 0) + 1

    for test_type, count in sorted(test_types.items()):
        print(f"  • {test_type}: {count} tests")

    # Step 3: Show generated test file
    print_section("STEP 3: GENERATED TEST FILE")

    test_content = generator.generate_test_file(test_suite)

    print("Preview of generated tests:\n")
    print(test_content)

    # Step 4: Save test file
    print_section("STEP 4: SAVE RESULTS")

    output_dir = Path(__file__).parent / "examples" / "generated_tests"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "test_sample_payment_service.py"

    with open(output_file, 'w') as f:
        f.write(test_content)

    print(f"✅ Test file saved to: {output_file}")
    print(f"✅ Generated {len(test_suite.tests)} tests")

    # Summary
    print_section("SUMMARY")

    print("Test Orchestrator successfully:")
    print(f"  ✅ Analyzed {analysis.total_functions} functions")
    print(f"  ✅ Detected {sum(len(f.edge_cases) for f in analysis.functions)} edge cases")
    print(f"  ✅ Generated {len(test_suite.tests)} comprehensive tests")
    print(f"  ✅ Created test file: {output_file}")
    print()

    print("Next steps:")
    print("  1. Review generated tests and fill in TODOs")
    print("  2. Run tests: pytest " + str(output_file))
    print("  3. Adjust test assertions as needed")
    print("  4. Measure coverage: pytest --cov=examples")
    print()

    print_header("DEMONSTRATION COMPLETE")

    return 0


if __name__ == "__main__":
    sys.exit(main())

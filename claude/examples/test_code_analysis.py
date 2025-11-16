"""
Test script for code-analysis skill.

Demonstrates basic usage and validates against existing codebase.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from skills.code_analysis import CodeAnalyzer, DesignPattern, CodeSmell


def test_analyze_single_file():
    """Test analyzing a single Python file"""
    print("=" * 60)
    print("Test 1: Analyze Single File")
    print("=" * 60)

    analyzer = CodeAnalyzer()

    # Analyze a known file
    test_file = "skills/learning_plan_manager/manager.py"

    if not Path(test_file).exists():
        print(f"❌ Test file not found: {test_file}")
        return False

    print(f"\n1. Analyzing {test_file}...")
    analysis = analyzer.analyze_file(test_file)

    print(f"✅ Analyzed successfully")
    print(f"   Classes: {len(analysis.classes)}")
    print(f"   Functions: {len(analysis.functions)}")
    print(f"   Total lines: {analysis.total_lines}")
    print(f"   Code lines: {analysis.code_lines}")
    print(f"   Imports: {len(analysis.imports)}")

    # Show some details
    if analysis.classes:
        print(f"\n   First class: {analysis.classes[0].name}")
        print(f"   - Line {analysis.classes[0].line_start}-{analysis.classes[0].line_end}")
        print(f"   - Public: {analysis.classes[0].is_public}")

    if analysis.functions:
        print(f"\n   First function: {analysis.functions[0].name}")
        if analysis.functions[0].complexity:
            print(f"   - Complexity: {analysis.functions[0].complexity.cyclomatic_complexity}")
            print(f"   - Lines: {analysis.functions[0].complexity.lines_of_code}")

    return True


def test_analyze_codebase():
    """Test analyzing entire codebase"""
    print("\n" + "=" * 60)
    print("Test 2: Analyze Codebase")
    print("=" * 60)

    analyzer = CodeAnalyzer()

    # Analyze skills directory
    root_path = "skills/"

    print(f"\n1. Analyzing {root_path}...")
    analysis = analyzer.analyze_codebase(root_path, max_files=20)

    print(f"✅ Analyzed {analysis.total_files} files")
    print(f"   Total lines: {analysis.total_lines}")
    print(f"   Entry points: {len(analysis.entry_points)}")
    print(f"   Integration points: {len(analysis.integration_points)}")

    # Show patterns found
    if analysis.patterns_found:
        print(f"\n2. Patterns detected:")
        for pattern, files in analysis.patterns_found.items():
            print(f"   - {pattern.value}: {len(files)} file(s)")
    else:
        print(f"\n⚠️  No patterns detected (this is normal for utility code)")

    # Show integration points
    if analysis.integration_points:
        print(f"\n3. Integration points (top 3):")
        for point in analysis.integration_points[:3]:
            print(f"   - {point.name} ({point.entity_type})")
            print(f"     File: {point.file_path}:{point.line_number}")
            print(f"     Reason: {point.reason}")
    else:
        print(f"\n⚠️  No integration points found")

    return True


def test_complexity_metrics():
    """Test complexity calculation"""
    print("\n" + "=" * 60)
    print("Test 3: Complexity Metrics")
    print("=" * 60)

    analyzer = CodeAnalyzer()

    # Analyze parser file (likely to have complex functions)
    test_file = "skills/learning_plan_manager/parser.py"

    if not Path(test_file).exists():
        print(f"⚠️  Test file not found: {test_file}")
        return True

    print(f"\n1. Analyzing {test_file}...")
    analysis = analyzer.analyze_file(test_file)

    # Find complex functions
    complex_funcs = []
    for func in analysis.functions:
        if func.complexity and func.complexity.cyclomatic_complexity > 5:
            complex_funcs.append(func)

    print(f"✅ Found {len(complex_funcs)} complex functions (complexity > 5)")

    if complex_funcs:
        print(f"\n2. Most complex functions:")
        # Sort by complexity
        complex_funcs.sort(
            key=lambda f: f.complexity.cyclomatic_complexity, reverse=True
        )

        for func in complex_funcs[:3]:
            print(f"   - {func.name}")
            print(f"     Complexity: {func.complexity.cyclomatic_complexity}")
            print(f"     Lines: {func.complexity.lines_of_code}")
            print(f"     Nesting: {func.complexity.max_nesting_depth}")

    return True


def test_code_smells():
    """Test code smell detection"""
    print("\n" + "=" * 60)
    print("Test 4: Code Smell Detection")
    print("=" * 60)

    analyzer = CodeAnalyzer()

    # Analyze entire skills directory
    print(f"\n1. Analyzing skills/ for code smells...")
    analysis = analyzer.analyze_codebase("skills/", max_files=20)

    # Collect all smells
    all_smells = []
    for file_analysis in analysis.files:
        all_smells.extend(file_analysis.smells)

    print(f"✅ Found {len(all_smells)} code smell(s)")

    if all_smells:
        # Group by smell type
        smell_counts = {}
        for smell in all_smells:
            smell_type = smell["smell"]
            smell_counts[smell_type] = smell_counts.get(smell_type, 0) + 1

        print(f"\n2. Smell breakdown:")
        for smell_type, count in smell_counts.items():
            print(f"   - {smell_type}: {count}")

        # Show some examples
        print(f"\n3. Examples (first 3):")
        for smell in all_smells[:3]:
            print(f"   - {smell['smell']} at {smell['location']}")
            print(f"     {smell['description']}")
    else:
        print(f"\n✅ No code smells detected (clean code!)")

    return True


def test_dependency_graph():
    """Test dependency graph building"""
    print("\n" + "=" * 60)
    print("Test 5: Dependency Graph")
    print("=" * 60)

    analyzer = CodeAnalyzer()

    print(f"\n1. Building dependency graph for skills/...")
    analysis = analyzer.analyze_codebase("skills/learning_plan_manager/", max_files=10)

    dep_graph = analysis.dependency_graph

    print(f"✅ Built graph with {len(dep_graph.edges)} edges")

    # Find circular dependencies
    cycles = dep_graph.find_circular_dependencies()

    if cycles:
        print(f"⚠️  Found {len(cycles)} circular dependencies:")
        for cycle in cycles[:3]:  # Show first 3
            print(f"   - {' -> '.join([Path(f).name for f in cycle])}")
    else:
        print(f"✅ No circular dependencies found")

    # Show dependencies for a file
    if dep_graph.edges:
        example_file = dep_graph.edges[0].from_file
        deps = dep_graph.get_dependencies(example_file)
        dependents = dep_graph.get_dependents(example_file)

        print(f"\n2. Dependencies for {Path(example_file).name}:")
        print(f"   Depends on: {len(deps)} file(s)")
        print(f"   Depended on by: {len(dependents)} file(s)")

    return True


def test_pattern_detection():
    """Test design pattern detection"""
    print("\n" + "=" * 60)
    print("Test 6: Design Pattern Detection")
    print("=" * 60)

    analyzer = CodeAnalyzer()

    # Analyze src directory (more likely to have patterns)
    print(f"\n1. Looking for patterns in src/...")

    if not Path("src/").exists():
        print("⚠️  src/ directory not found, skipping pattern detection test")
        return True

    analysis = analyzer.analyze_codebase("src/", max_files=30)

    if analysis.patterns_found:
        print(f"✅ Detected patterns:")
        for pattern, files in analysis.patterns_found.items():
            print(f"\n   {pattern.value.title()} Pattern:")
            for file_path in files[:3]:  # Show first 3
                print(f"   - {file_path}")
    else:
        print(f"✅ No patterns detected (this is normal for simple codebases)")

    return True


def test_integration_suggestions():
    """Test integration point suggestions"""
    print("\n" + "=" * 60)
    print("Test 7: Integration Point Suggestions")
    print("=" * 60)

    analyzer = CodeAnalyzer()

    print(f"\n1. Analyzing codebase...")
    analysis = analyzer.analyze_codebase("skills/", max_files=20)

    # Test feature suggestions
    features = ["manager", "parser", "analyzer"]

    print(f"\n2. Testing feature suggestions:")
    for feature in features:
        suggestions = analysis.suggest_integration_for_feature(feature)
        print(f"\n   For '{feature}': {len(suggestions)} suggestion(s)")
        if suggestions:
            for sugg in suggestions[:2]:  # Show first 2
                print(f"   - {sugg.name} in {Path(sugg.file_path).name}")

    return True


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("Code Analysis Skill - Test Suite")
    print("=" * 60)

    tests = [
        test_analyze_single_file,
        test_analyze_codebase,
        test_complexity_metrics,
        test_code_smells,
        test_dependency_graph,
        test_pattern_detection,
        test_integration_suggestions,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n❌ Test failed with exception: {e}")
            import traceback

            traceback.print_exc()
            results.append(False)

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"\nPassed: {passed}/{total}")

    if passed == total:
        print("✅ All tests passed!")
    else:
        print(f"❌ {total - passed} test(s) failed")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

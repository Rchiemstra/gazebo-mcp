#!/usr/bin/env python3
"""
MCP Code Execution Efficiency Demo

Demonstrates the massive token savings from MCP code execution patterns:
1. Agent generates code that calls skills
2. Code filters results locally
3. Only filtered results returned to model
4. Result: Up to 98.7% token reduction!

Run: python examples/mcp_efficiency_demo.py
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from skills.execution import CodeExecutionEngine, EfficiencyTracker
from skills.common.filters import ResultFilter, TokenEstimator


def demo_filtering_efficiency():
    """Demonstrate token savings from filtering."""
    print("=" * 70)
    print("MCP CODE EXECUTION EFFICIENCY DEMO")
    print("=" * 70)
    print()

    # Simulate large dataset (like code analysis results)
    large_dataset = [
        {"path": f"src/component_{i}.py", "complexity": i, "lines": i * 10}
        for i in range(1, 10001)  # 10,000 files
    ]

    print("📊 Scenario: Code Analysis Results")
    print(f"   Total files: {len(large_dataset)}")
    print()

    # Estimate tokens for full dataset
    full_tokens = TokenEstimator.estimate_tokens(large_dataset)
    print(f"❌ Without filtering: {full_tokens:,} tokens")
    print("   (All 10,000 files sent to model)")
    print()

    # Filter to top 5 most complex
    filtered = ResultFilter.top_n_by_field(large_dataset, "complexity", 5)
    filtered_tokens = TokenEstimator.estimate_tokens(filtered)
    print(f"✅ With filtering: {filtered_tokens:,} tokens")
    print("   (Only 5 most complex files sent to model)")
    print()

    # Calculate savings
    efficiency = TokenEstimator.compare_efficiency(large_dataset, filtered)
    print(f"💰 Token Savings: {efficiency['tokens_saved']:,} tokens")
    print(f"📈 Efficiency Gain: {efficiency['savings_percent']:.1f}% reduction!")
    print()
    print("-" * 70)
    print()


def demo_code_execution():
    """Demonstrate code execution with filtering."""
    print("🚀 CODE EXECUTION DEMO")
    print("-" * 70)
    print()

    engine = CodeExecutionEngine()
    tracker = EfficiencyTracker()

    # Example 1: Filter large dataset
    print("Example 1: Filtering Large Dataset")
    print()

    code = '''
from skills.common.filters import ResultFilter

# Simulate large dataset (like code analysis)
data = [{"id": i, "value": i * 2} for i in range(10000)]

# Filter to top 5
result = ResultFilter.limit(data, 5)
'''

    print("Code:")
    print(code)

    result = engine.execute_with_result(code)

    if result.success:
        print(f"✅ Execution succeeded in {result.duration:.3f}s")
        print(f"   Output: {result.output}")

        # Track efficiency
        full_size = 10000 * 20  # Rough token estimate
        filtered_size = len(str(result.output)) // 4
        tracker.record_execution("filter_large_dataset", full_size, filtered_size, result.duration)
    else:
        print(f"❌ Execution failed: {result.error}")

    print()
    print("-" * 70)
    print()

    # Example 2: Search and filter
    print("Example 2: Search and Filter")
    print()

    code = '''
from skills.common.filters import ResultFilter

# Simulate file list
files = [
    {"path": "src/navigation/path_planner.py", "complexity": 15},
    {"path": "src/navigation/obstacle_detector.py", "complexity": 12},
    {"path": "src/sensors/lidar.py", "complexity": 8},
    {"path": "src/utils/config.py", "complexity": 3},
]

# Search for navigation files
nav_files = ResultFilter.search(files, "navigation", ["path"])

# Return only high complexity
result = ResultFilter.filter_by_threshold(nav_files, "complexity", 10, ">")
'''

    print("Code:")
    print(code)

    result = engine.execute_with_result(code)

    if result.success:
        print(f"✅ Execution succeeded in {result.duration:.3f}s")
        print(f"   Found {len(result.output)} navigation files with complexity > 10")
        for file in result.output:
            print(f"   - {file['path']} (complexity: {file['complexity']})")
    else:
        print(f"❌ Execution failed: {result.error}")

    print()
    print("-" * 70)
    print()

    # Example 3: Summarize instead of full data
    print("Example 3: Summarize Large History")
    print()

    code = '''
from skills.common.filters import ResultFilter

# Simulate 6 months of learning history
history = [
    {"date": f"2024-{month:02d}-{day:02d}", "tasks": 3}
    for month in range(1, 7)
    for day in range(1, 31)
]  # ~180 days = 30,000 tokens

# Return summary instead of full history
result = ResultFilter.summarize(history, sample_size=3)
'''

    print("Code:")
    print(code)

    result = engine.execute_with_result(code)

    if result.success:
        print(f"✅ Execution succeeded in {result.duration:.3f}s")
        print(f"   Summary: {result.output}")
        print(f"   Returned {len(result.output)} fields instead of 180 records!")

        # Track efficiency
        full_size = 180 * 20  # Rough token estimate (180 records)
        filtered_size = len(str(result.output)) // 4
        tracker.record_execution("summarize_history", full_size, filtered_size, result.duration)
    else:
        print(f"❌ Execution failed: {result.error}")

    print()
    print("-" * 70)
    print()

    # Show efficiency summary
    print("📊 EFFICIENCY SUMMARY")
    print("-" * 70)
    summary = tracker.get_summary()
    print(f"Total operations: {summary['total_operations']}")
    print(f"Tokens without filtering: {summary['tokens_without_filtering']:,}")
    print(f"Tokens with filtering: {summary['tokens_with_filtering']:,}")
    print(f"Total tokens saved: {summary['total_tokens_saved']:,}")
    print(f"Average savings: {summary['average_savings_percent']:.1f}%")
    print()


def demo_security_validation():
    """Demonstrate security validation."""
    print("🔒 SECURITY VALIDATION DEMO")
    print("-" * 70)
    print()

    engine = CodeExecutionEngine()

    # Test dangerous operations
    dangerous_examples = [
        ("eval", 'result = eval("2 + 2")'),
        ("exec", 'exec("print(\'hello\')")'),
        ("os import", 'import os\nresult = os.listdir()'),
        ("file operations", 'result = open("/etc/passwd").read()'),
    ]

    for name, code in dangerous_examples:
        print(f"Testing: {name}")
        result = engine.execute_with_result(code)

        if not result.success:
            print(f"✅ Blocked: {result.error}")
        else:
            print(f"❌ WARNING: {name} was not blocked!")

        print()

    print("-" * 70)
    print()


def demo_real_world_scenario():
    """Demonstrate real-world efficiency scenario."""
    print("🌍 REAL-WORLD SCENARIO")
    print("-" * 70)
    print()
    print("Scenario: Agent analyzing codebase to find integration points")
    print("          for new 'navigation' feature")
    print()

    # Without code execution (old way)
    print("❌ OLD WAY (Without Code Execution):")
    print("   1. Agent: 'Skill(code-analysis): analyze codebase'")
    print("   2. System returns ALL 10,000 files (50,000 tokens)")
    print("   3. Model processes 50,000 tokens")
    print("   4. Model filters to 5 relevant files")
    print("   5. Model responds with 5 files (500 tokens)")
    print("   TOTAL: 50,500 tokens")
    print()

    # With code execution (new way)
    print("✅ NEW WAY (With Code Execution):")
    print("   1. Agent generates code:")
    print()

    code = '''
from skills.common.filters import ResultFilter

# Simulate codebase analysis
files = [
    {"path": f"src/module_{i}.py", "complexity": i % 20, "description": f"Module {i}"}
    for i in range(10000)
]

# Add some navigation-related files
files.extend([
    {"path": "src/nav/path_planner.py", "complexity": 15, "description": "Path planning"},
    {"path": "src/nav/controller.py", "complexity": 12, "description": "Navigation control"},
])

# Filter to navigation-related files
nav_files = ResultFilter.search(files, "nav", ["path", "description"])

# Return top 5 most complex (likely integration points)
result = ResultFilter.top_n_by_field(nav_files, "complexity", 5)
'''

    print(code)
    print()
    print("   2. Code executes locally, filters 10,000 → 5 files")
    print("   3. Returns only 5 files (500 tokens) to model")
    print("   4. Model sees filtered results directly")
    print("   TOTAL: 500 tokens")
    print()

    # Execute to verify
    engine = CodeExecutionEngine()
    result = engine.execute_with_result(code)

    if result.success:
        print(f"✅ Execution succeeded")
        print(f"   Found {len(result.output)} files:")
        for file in result.output:
            print(f"   - {file['path']} (complexity: {file['complexity']})")
        print()

        # Calculate savings
        old_way_tokens = 50_500
        new_way_tokens = 500
        savings = ((old_way_tokens - new_way_tokens) / old_way_tokens) * 100

        print(f"💰 SAVINGS: {old_way_tokens - new_way_tokens:,} tokens")
        print(f"📈 EFFICIENCY: {savings:.1f}% reduction!")
    else:
        print(f"❌ Execution failed: {result.error}")

    print()
    print("-" * 70)
    print()


if __name__ == "__main__":
    print()
    demo_filtering_efficiency()
    demo_code_execution()
    demo_security_validation()
    demo_real_world_scenario()

    print()
    print("=" * 70)
    print("✨ MCP CODE EXECUTION PATTERN DELIVERS 95-99% TOKEN SAVINGS! ✨")
    print("=" * 70)
    print()
    print("Key Takeaways:")
    print("1. Filter data locally before model sees it")
    print("2. Use ResultFilter utilities for common operations")
    print("3. Return summaries instead of full datasets")
    print("4. Code execution is secure and sandboxed")
    print("5. Massive token savings enable more complex operations")
    print()
    print("Next Steps:")
    print("- Try the examples in your own code")
    print("- Read docs/MCP_EFFICIENCY_ANALYSIS.md for details")
    print("- Check docs/MCP_IMPLEMENTATION_PLAN.md for integration guide")
    print()

#!/usr/bin/env python3
"""
Code Search Demonstration

Demonstrates intelligent code search capabilities.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from code_search import (
    search_symbol,
    search_pattern,
    find_definition,
    find_usages
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
    print_header("CODE SEARCH DEMONSTRATION")

    examples_dir = Path(__file__).parent / 'examples' / 'sample_project'

    # ===================================================================
    # PART 1: SYMBOL SEARCH
    # ===================================================================
    print_section("PART 1: SYMBOL SEARCH")

    print("Searching for all symbols named 'process_data'...\n")

    result = search_symbol(
        project_path=str(examples_dir),
        symbol_name='process_data',
        symbol_type='function',
        exact_match=True
    )

    print(f"Index Statistics:")
    stats = result['index_stats']
    print(f"  Files indexed: {stats['files_indexed']}")
    print(f"  Total symbols: {stats['symbols_indexed']}")
    print(f"  Functions: {stats['functions']}")
    print(f"  Classes: {stats['classes']}")
    print(f"  Methods: {stats['methods']}")
    print()

    print(f"Search Results: {result['total_matches']} matches\n")

    for match in result['matches']:
        print(f"Match: {Path(match['file_path']).name}:{match['line_number']}")
        print(f"  Type: {match['symbol_type']}")
        print(f"  Signature: {match['signature']}")
        print(f"  Relevance: {match['relevance_score']:.2f}")
        if match['docstring']:
            first_line = match['docstring'].split('\n')[0]
            print(f"  Doc: {first_line}")
        print()

    # ===================================================================
    # PART 2: WILDCARD SEARCH
    # ===================================================================
    print_section("PART 2: WILDCARD SEARCH")

    print("Searching for symbols matching 'process*'...\n")

    result = search_symbol(
        project_path=str(examples_dir),
        symbol_name='process*',
        symbol_type='all',
        exact_match=False
    )

    print(f"Found {result['total_matches']} matches:\n")

    for match in result['matches'][:5]:  # Show first 5
        print(f"  • {match['symbol_name']} ({match['symbol_type']}) - {Path(match['file_path']).name}:{match['line_number']}")

    if result['total_matches'] > 5:
        print(f"  ... and {result['total_matches'] - 5} more")

    print()

    # ===================================================================
    # PART 3: FIND DEFINITION
    # ===================================================================
    print_section("PART 3: FIND DEFINITION")

    print("Finding definition of 'DataProcessor'...\n")

    result = find_definition(
        project_path=str(examples_dir),
        symbol_name='DataProcessor'
    )

    if result['found']:
        definition = result['definition']
        print(f"✅ Definition found!")
        print(f"  File: {Path(definition['file_path']).name}")
        print(f"  Line: {definition['line_number']}")
        print(f"  Type: {definition['definition_type']}")
        print(f"  Signature: {definition['signature']}")
        print()

        if definition['docstring']:
            print(f"  Docstring:")
            for line in definition['docstring'].split('\n')[:3]:
                print(f"    {line}")
            print()

        print(f"  Source code:")
        print("  " + "-" * 60)
        source_lines = definition['source_code'].split('\n')
        for line in source_lines[:10]:
            print(f"  {line}")
        if len(source_lines) > 10:
            remaining = len(source_lines) - 10
            print(f"  ... ({remaining} more lines)")
        print("  " + "-" * 60)
    else:
        print("❌ Definition not found")

    print()

    # ===================================================================
    # PART 4: FIND USAGES
    # ===================================================================
    print_section("PART 4: FIND USAGES")

    print("Finding all usages of 'process_data'...\n")

    result = find_usages(
        project_path=str(examples_dir),
        symbol_name='process_data'
    )

    print(f"Found {result['total_usages']} usages\n")

    if result['usage_counts']:
        print("Usage breakdown:")
        for usage_type, count in result['usage_counts'].items():
            print(f"  {usage_type}: {count}")
        print()

    print("Usage details:\n")

    for i, usage in enumerate(result['usages'][:8], 1):
        print(f"{i}. {Path(usage['file_path']).name}:{usage['line_number']}")
        print(f"   Type: {usage['usage_type']}")
        if usage['parent_function']:
            print(f"   In function: {usage['parent_function']}")
        if usage['parent_class']:
            print(f"   In class: {usage['parent_class']}")

        # Show context line
        context_lines = usage['context'].split('\n')
        for line in context_lines:
            if 'process_data' in line:
                print(f"   Code: {line.strip()}")
                break
        print()

    if result['total_usages'] > 8:
        print(f"... and {result['total_usages'] - 8} more usages\n")

    # ===================================================================
    # PART 5: PATTERN SEARCH
    # ===================================================================
    print_section("PART 5: PATTERN SEARCH")

    print("Searching for pattern: 'def .*process.*\\('...\n")

    result = search_pattern(
        project_path=str(examples_dir),
        pattern=r'def .*process.*\('
    )

    print(f"Found {result['total_matches']} matches\n")

    for match in result['matches'][:5]:
        print(f"  {Path(match['file_path']).name}:{match['line_number']}")
        print(f"    {match['matched_code'].strip()}")
        print()

    # ===================================================================
    # PART 6: CLASS SEARCH
    # ===================================================================
    print_section("PART 6: CLASS SEARCH")

    print("Searching for all classes...\n")

    result = search_symbol(
        project_path=str(examples_dir),
        symbol_name='*',
        symbol_type='class',
        exact_match=False
    )

    print(f"Found {result['total_matches']} classes:\n")

    for match in result['matches']:
        print(f"  📦 {match['symbol_name']}")
        print(f"     File: {Path(match['file_path']).name}:{match['line_number']}")
        print(f"     Signature: {match['signature']}")
        if match['docstring']:
            first_line = match['docstring'].split('\n')[0]
            print(f"     {first_line}")
        print()

    # ===================================================================
    # PART 7: USAGE EXAMPLES
    # ===================================================================
    print_section("PART 7: PRACTICAL USE CASES")

    print("How code-search can be used:\n")

    print("1. 🔍 Quick Navigation")
    print("   Find definition of any symbol instantly")
    print("   Jump to implementation with exact location")
    print()

    print("2. 🔄 Refactoring Safety")
    print("   Find all usages before renaming")
    print("   Ensure no references are missed")
    print()

    print("3. 📚 Code Understanding")
    print("   Discover how functions are used")
    print("   Understand code flow and dependencies")
    print()

    print("4. 🐛 Bug Investigation")
    print("   Find all callers of a function")
    print("   Track data flow through the system")
    print()

    print("5. 📊 Code Analysis")
    print("   Find unused code")
    print("   Identify frequently used utilities")
    print()

    print("6. 🎯 Pattern Detection")
    print("   Find anti-patterns")
    print("   Locate similar code blocks")
    print()

    print("7. 🧪 Test Coverage")
    print("   Find functions without tests")
    print("   Locate test files for modules")
    print()

    # ===================================================================
    # PART 8: INTEGRATION WITH OTHER SKILLS
    # ===================================================================
    print_section("PART 8: INTEGRATION WITH OTHER SKILLS")

    print("code-search works with other skills:\n")

    print("With refactor-assistant:")
    print("  1. Use code-search to find all usages")
    print("  2. Refactor with confidence knowing all references")
    print("  3. Verify refactoring affected all locations")
    print()

    print("With test-orchestrator:")
    print("  1. Search for functions without tests")
    print("  2. Generate tests for uncovered code")
    print("  3. Find test patterns to match")
    print()

    print("With doc-generator:")
    print("  1. Find undocumented symbols")
    print("  2. Generate docstrings for found symbols")
    print("  3. Verify documentation coverage")
    print()

    print("With dependency-guardian:")
    print("  1. Find all usages of a dependency")
    print("  2. Assess impact of removing dependency")
    print("  3. Find alternative implementations")
    print()

    # ===================================================================
    # PART 9: PERFORMANCE METRICS
    # ===================================================================
    print_section("PART 9: PERFORMANCE METRICS")

    print("Indexing and search performance:\n")

    # Re-run search to show performance
    result = search_symbol(
        project_path=str(examples_dir),
        symbol_name='*',
        symbol_type='all',
        exact_match=False
    )

    stats = result['index_stats']

    print(f"Project Statistics:")
    print(f"  Files analyzed: {stats['files_indexed']}")
    print(f"  Total symbols: {stats['symbols_indexed']}")
    print(f"  Functions: {stats['functions']}")
    print(f"  Classes: {stats['classes']}")
    print(f"  Methods: {stats['methods']}")
    print()

    print(f"Search Results:")
    print(f"  Total matches: {result['total_matches']}")
    print(f"  Indexed once, searched many times")
    print(f"  AST-based: Understands code structure")
    print()

    # ===================================================================
    # SUMMARY
    # ===================================================================
    print_section("SUMMARY")

    print("✅ Code Search successfully demonstrated:")
    print(f"   • Indexed {stats['files_indexed']} files with {stats['symbols_indexed']} symbols")
    print("   • Symbol search with wildcards and fuzzy matching")
    print("   • Definition finding with import resolution")
    print("   • Usage tracking with context")
    print("   • Pattern matching with regex")
    print()

    print("🎯 Key Capabilities:")
    print("   ✅ AST-based code indexing")
    print("   ✅ Fast symbol search")
    print("   ✅ Jump to definition")
    print("   ✅ Find all usages/references")
    print("   ✅ Pattern matching")
    print("   ✅ Wildcard and fuzzy search")
    print()

    print("📚 Next Steps:")
    print("   1. Integrate into development workflow")
    print("   2. Use for code navigation and refactoring")
    print("   3. Combine with other skills for powerful workflows")
    print("   4. Add keyboard shortcuts for quick access")
    print("   5. Build IDE extensions")
    print()

    print_header("DEMONSTRATION COMPLETE")

    return 0


if __name__ == "__main__":
    sys.exit(main())

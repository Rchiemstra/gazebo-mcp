"""
Example 2: Create MCP Adapters for Skills

This example demonstrates how to use the mcp_adapter_creator skill to generate
MCP adapter files that expose skills via the Model Context Protocol.
"""

from skills.mcp_adapter_creator import create_adapter, create_batch_adapters
from pathlib import Path


def example_1_basic_adapter_creation():
    """Create adapter for a single skill."""
    print("=== Example 1: Basic Adapter Creation ===\n")

    result = create_adapter("code_analysis", response_format="summary")

    if result.success:
        print(f"✓ Successfully created adapter for {result.data['skill_name']}")
        print(f"  Adapter path: {result.data['adapter_path']}")
        print(f"  Operations: {result.data['operations_count']}")
        print(f"  Operations list: {', '.join(result.data['operations'])}")
        print(f"  Duration: {result.duration:.3f}s")
    else:
        print(f"✗ Failed: {result.error}")

    print()


def example_2_adapter_with_code():
    """Create adapter and view the generated code."""
    print("=== Example 2: Adapter with Generated Code ===\n")

    result = create_adapter("code_analysis", response_format="complete")

    if result.success:
        print(f"✓ Generated adapter for {result.data['skill_name']}\n")

        # Show snippet of generated code
        adapter_code = result.data['adapter_code']
        lines = adapter_code.split('\n')

        print("Code snippet (first 30 lines):")
        print("-" * 60)
        for i, line in enumerate(lines[:30], 1):
            print(f"{i:3d}: {line}")
        print("-" * 60)

        print(f"\nTotal lines: {len(lines)}")
        print(f"Operations: {result.data['operations_count']}")

    print()


def example_3_batch_adapter_creation():
    """Create adapters for multiple skills."""
    print("=== Example 3: Batch Adapter Creation ===\n")

    skills_config = [
        {"name": "code_analysis"},
        {"name": "test_orchestrator"},
        {"name": "learning_analytics"}
    ]

    result = create_batch_adapters(skills_config, response_format="summary")

    if result.success:
        data = result.data
        print(f"✓ Batch creation complete")
        print(f"  Total skills: {data['total_skills']}")
        print(f"  Successful: {data['successful']}")
        print(f"  Failed: {data['failed']}")
        print(f"  Total adapters: {data['total_adapters']}")

        if data['failed_skills']:
            print(f"\n  Failed skills:")
            for failed in data['failed_skills']:
                print(f"    - {failed['skill']}: {failed['error']}")

        print(f"\n  Duration: {result.duration:.3f}s")

    print()


def example_4_specific_operations():
    """Create adapter with specific operations only."""
    print("=== Example 4: Adapter with Specific Operations ===\n")

    result = create_adapter(
        "code_analysis",
        operations=["analyze_file"],  # Only this operation
        response_format="summary"
    )

    if result.success:
        print(f"✓ Created adapter with specific operations")
        print(f"  Skill: {result.data['skill_name']}")
        print(f"  Operations: {', '.join(result.data['operations'])}")
    else:
        print(f"✗ Failed: {result.error}")

    print()


def example_5_save_adapters_to_directory():
    """Create and save adapters to a custom directory."""
    print("=== Example 5: Save Adapters to Directory ===\n")

    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"Output directory: {tmpdir}\n")

        # Create adapters for multiple skills
        skills_config = [
            {"name": "code_analysis"},
            {"name": "test_orchestrator"}
        ]

        result = create_batch_adapters(skills_config, response_format="complete")

        if result.success:
            adapters = result.data['adapters']

            for adapter in adapters:
                # Write adapter to file
                adapter_path = Path(tmpdir) / f"{adapter['skill_name']}_adapter.py"

                with open(adapter_path, 'w') as f:
                    f.write(adapter['adapter_code'])

                print(f"✓ Saved {adapter_path.name}")
                print(f"  Operations: {adapter['operations_count']}")

            print(f"\n  Total adapters saved: {len(adapters)}")

    print()


def example_6_adapter_structure_analysis():
    """Analyze the structure of generated adapters."""
    print("=== Example 6: Adapter Structure Analysis ===\n")

    result = create_adapter("code_analysis", response_format="complete")

    if result.success:
        adapter_code = result.data['adapter_code']

        # Analyze the code
        has_docstring = '"""' in adapter_code
        has_operations_dict = "OPERATIONS = " in adapter_code
        has_result_filter = "ResultFilter" in adapter_code
        has_examples = "from skills." in adapter_code
        has_token_efficiency = "98.7%" in adapter_code or "token" in adapter_code.lower()

        print("Adapter Structure Analysis:")
        print(f"  ✓ Docstring: {has_docstring}")
        print(f"  ✓ OPERATIONS dict: {has_operations_dict}")
        print(f"  ✓ ResultFilter import: {has_result_filter}")
        print(f"  ✓ Usage examples: {has_examples}")
        print(f"  ✓ Token efficiency docs: {has_token_efficiency}")

        # Count operations
        operations = result.data['operations']
        print(f"\n  Total operations: {len(operations)}")
        for op in operations:
            print(f"    - {op['name']}")

    print()


if __name__ == "__main__":
    print("MCP Adapter Creator Examples\n")
    print("=" * 60)
    print()

    example_1_basic_adapter_creation()
    example_2_adapter_with_code()
    example_3_batch_adapter_creation()
    example_4_specific_operations()
    example_5_save_adapters_to_directory()
    example_6_adapter_structure_analysis()

    print("=" * 60)
    print("\nAll examples complete!")
    print("\nNext steps:")
    print("- Review generated adapter code")
    print("- Integrate adapters into your MCP server")
    print("- Test adapters with MCP protocol")
    print("- Validate security configuration")

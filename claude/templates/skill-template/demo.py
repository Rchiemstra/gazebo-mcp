"""
{{SKILL_NAME}} Skill Demonstration

This script demonstrates the usage of all operations provided by the {{SKILL_NAME}} skill.

Author: {{AUTHOR_NAME}}
Created: {{CREATED_DATE}}
"""

import sys
from pathlib import Path

# Add skill to path for importing
skill_dir = Path(__file__).parent
sys.path.insert(0, str(skill_dir.parent))

from {{SKILL_NAME}} import {{OPERATION_IMPORTS}}, OperationResult


def print_result(operation_name: str, result: OperationResult) -> None:
    """
    Pretty print an operation result.

    Args:
        operation_name: Name of the operation
        result: The OperationResult to print
    """
    print(f"\n{'='*60}")
    print(f"Operation: {operation_name}")
    print(f"{'='*60}")

    if result.success:
        print("✅ Status: SUCCESS")
        print(f"⏱️  Duration: {result.duration:.3f}s")

        if result.data:
            print("\n📊 Data:")
            for key, value in result.data.items():
                print(f"   {key}: {value}")

        if result.metadata:
            print("\n📋 Metadata:")
            for key, value in result.metadata.items():
                print(f"   {key}: {value}")
    else:
        print("❌ Status: FAILED")
        print(f"⏱️  Duration: {result.duration:.3f}s")
        print(f"\n🚨 Error: {result.error}")
        print(f"📟 Error Code: {result.error_code}")


def main():
    """
    Main demonstration function.

    Demonstrates all operations provided by the {{SKILL_NAME}} skill.
    """
    print("="*60)
    print(f"{{{{SKILL_NAME}}}} Skill Demonstration")
    print("="*60)
    print()
    print("This demo shows how to use all operations in the {{SKILL_NAME}} skill.")
    print()

    # ========================================
    # Demo 1: {{OPERATION_NAME_EXAMPLE}}
    # ========================================
    print("\n" + "="*60)
    print("Demo 1: {{OPERATION_NAME_EXAMPLE}}")
    print("="*60)
    print("\nDescription: {{OPERATION_DESCRIPTION_EXAMPLE}}")
    print("\nUsage:")
    print("```python")
    print("result = {{OPERATION_NAME_EXAMPLE}}(")
    print("    param1='value1',")
    print("    param2='value2'")
    print(")")
    print("```")

    # TODO: Update with actual operation call and parameters
    # result = {{OPERATION_NAME_EXAMPLE}}(
    #     param1="example_value",
    #     param2="example_value"
    # )
    # print_result("{{OPERATION_NAME_EXAMPLE}}", result)

    # ========================================
    # Demo 2: Error Handling
    # ========================================
    print("\n" + "="*60)
    print("Demo 2: Error Handling")
    print("="*60)
    print("\nDemonstrating how the skill handles errors:")

    # TODO: Add error handling example
    # result = {{OPERATION_NAME_EXAMPLE}}(
    #     param1="",  # Invalid: empty string
    # )
    # print_result("{{OPERATION_NAME_EXAMPLE}} (with error)", result)

    # ========================================
    # Demo 3: Agent Usage Example
    # ========================================
    print("\n" + "="*60)
    print("Demo 3: Agent Usage")
    print("="*60)
    print("\nAgents can invoke this skill using:")
    print("\n```markdown")
    print("Skill({{SKILL_NAME}}) with query: \"{{EXAMPLE_AGENT_QUERY}}\"")
    print("```")
    print("\nThe skill will process the natural language query and")
    print("execute the appropriate operation with extracted parameters.")

    # ========================================
    # Summary
    # ========================================
    print("\n" + "="*60)
    print("Summary")
    print("="*60)
    print("\nThis skill provides the following operations:")
    print("{{OPERATIONS_SUMMARY}}")
    print("\n✅ All operations return standardized OperationResult")
    print("✅ All operations track execution duration")
    print("✅ All operations have comprehensive error handling")
    print("\nFor more information, see:")
    print("- README.md: User documentation")
    print("- skill.md: Skill metadata and specifications")
    print("- operations.py: Implementation details")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

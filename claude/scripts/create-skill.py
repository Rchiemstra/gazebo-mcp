#!/usr/bin/env python3
"""
Create Skill - Interactive CLI tool for scaffolding new skills

This script creates a new skill with all required files following best practices
documented in docs/ANTHROPIC_BEST_PRACTICES.md and docs/BEST_PRACTICES_ENFORCEMENT_PLAN.md

Usage:
    python scripts/create-skill.py

Author: Claude Code Team
Created: 2025-11-10
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import shutil

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
TEMPLATE_DIR = PROJECT_ROOT / "templates" / "skill-template"
SKILLS_DIR = PROJECT_ROOT / "skills"


# Skill categories based on existing skills
CATEGORIES = [
    "developer-productivity",
    "security-and-quality",
    "documentation",
    "testing-and-analysis",
    "workflow-automation",
    "learning-and-education",
    "data-processing",
    "system-integration"
]


def print_header():
    """Print welcome header."""
    print("=" * 70)
    print("Create New Skill - Interactive Scaffolding Tool")
    print("=" * 70)
    print()
    print("This tool will guide you through creating a new skill with best practices.")
    print("Reference: docs/ANTHROPIC_BEST_PRACTICES.md")
    print()


def validate_kebab_case(name: str) -> bool:
    """
    Validate that a name is in kebab-case format.

    Args:
        name: Name to validate

    Returns:
        True if valid kebab-case, False otherwise
    """
    pattern = r'^[a-z][a-z0-9-]*$'
    return bool(re.match(pattern, name)) and not name.startswith('-') and not name.endswith('-')


def prompt_skill_name() -> str:
    """
    Prompt for skill name with validation.

    Returns:
        Valid skill name in kebab-case
    """
    print("Step 1: Skill Name")
    print("-" * 70)
    print("Enter the skill name in kebab-case (e.g., 'my-awesome-skill')")
    print("Requirements:")
    print("  - Lowercase letters, numbers, and hyphens only")
    print("  - Must start with a letter")
    print("  - Must not start or end with a hyphen")
    print()

    while True:
        name = input("Skill name: ").strip()

        if not name:
            print("❌ Skill name cannot be empty. Try again.")
            continue

        if not validate_kebab_case(name):
            print("❌ Invalid format. Use kebab-case (e.g., 'my-skill-name'). Try again.")
            continue

        # Check if skill already exists
        skill_path = SKILLS_DIR / name
        if skill_path.exists():
            print(f"❌ Skill '{name}' already exists at: {skill_path}")
            print("   Choose a different name.")
            continue

        print(f"✅ Skill name: {name}")
        return name


def prompt_description() -> str:
    """
    Prompt for skill description with validation.

    Returns:
        Valid description
    """
    print()
    print("Step 2: Description")
    print("-" * 70)
    print("Enter a brief one-line description of the skill")
    print("Requirements:")
    print("  - Clear and specific")
    print("  - Describes what the skill does, not how")
    print("  - Recommended: 20-100 characters")
    print()
    print("Example: 'Intelligent code search with AST-based indexing'")
    print()

    while True:
        description = input("Description: ").strip()

        if not description:
            print("❌ Description cannot be empty. Try again.")
            continue

        if len(description) < 10:
            print("❌ Description too short. Provide more detail. Try again.")
            continue

        if len(description) > 200:
            print("⚠️  Description is quite long. Consider making it more concise.")
            confirm = input("Use this description anyway? (y/n): ").strip().lower()
            if confirm != 'y':
                continue

        print(f"✅ Description: {description}")
        return description


def prompt_category() -> str:
    """
    Prompt for skill category.

    Returns:
        Selected category
    """
    print()
    print("Step 3: Category")
    print("-" * 70)
    print("Select a category for your skill:")
    print()

    for i, category in enumerate(CATEGORIES, 1):
        print(f"  [{i}] {category}")
    print(f"  [{len(CATEGORIES) + 1}] Other (specify)")
    print()

    while True:
        choice = input(f"Category (1-{len(CATEGORIES) + 1}): ").strip()

        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(CATEGORIES):
                category = CATEGORIES[choice_num - 1]
                print(f"✅ Category: {category}")
                return category
            elif choice_num == len(CATEGORIES) + 1:
                custom = input("Enter custom category (kebab-case): ").strip()
                if validate_kebab_case(custom):
                    print(f"✅ Category: {custom}")
                    return custom
                else:
                    print("❌ Invalid format. Use kebab-case.")
                    continue
        except ValueError:
            pass

        print(f"❌ Invalid choice. Enter a number between 1 and {len(CATEGORIES) + 1}.")


def prompt_operations() -> List[Dict[str, str]]:
    """
    Prompt for skill operations.

    Returns:
        List of operations with name and description
    """
    print()
    print("Step 4: Operations")
    print("-" * 70)
    print("Define operations that this skill provides.")
    print("Each operation should:")
    print("  - Have a clear, descriptive name (snake_case)")
    print("  - Represent a high-level, consolidated action")
    print("  - Follow best practices from docs/ANTHROPIC_BEST_PRACTICES.md")
    print()
    print("Tip: Start with 1-3 core operations. You can add more later.")
    print()

    operations = []
    operation_num = 1

    while True:
        print(f"\nOperation {operation_num}:")
        print("-" * 40)

        # Operation name
        while True:
            op_name = input(f"  Operation name (snake_case, or 'done' to finish): ").strip()

            if op_name.lower() == 'done':
                if len(operations) == 0:
                    print("  ❌ You must define at least one operation.")
                    continue
                return operations

            if not op_name:
                print("  ❌ Operation name cannot be empty.")
                continue

            # Validate snake_case
            if not re.match(r'^[a-z][a-z0-9_]*$', op_name):
                print("  ❌ Use snake_case format (e.g., 'search_code', 'analyze_dependencies').")
                continue

            # Check for duplicates
            if any(op['name'] == op_name for op in operations):
                print(f"  ❌ Operation '{op_name}' already defined.")
                continue

            break

        # Operation description
        while True:
            op_desc = input(f"  Description: ").strip()

            if not op_desc:
                print("  ❌ Description cannot be empty.")
                continue

            if len(op_desc) < 10:
                print("  ❌ Description too short. Be more specific.")
                continue

            break

        operations.append({
            'name': op_name,
            'description': op_desc
        })

        print(f"  ✅ Added operation: {op_name}")
        operation_num += 1

        # Ask if they want to add another
        if len(operations) >= 1:
            another = input("\nAdd another operation? (y/n): ").strip().lower()
            if another != 'y':
                return operations


def prompt_author() -> str:
    """
    Prompt for author name.

    Returns:
        Author name
    """
    print()
    print("Step 5: Author")
    print("-" * 70)

    default_author = "Claude Code Team"
    author = input(f"Author name (default: {default_author}): ").strip()

    if not author:
        author = default_author

    print(f"✅ Author: {author}")
    return author


def generate_operation_function(op_name: str, op_desc: str) -> str:
    """
    Generate Python code for an operation function.

    Args:
        op_name: Operation name in snake_case
        op_desc: Operation description

    Returns:
        Python code for the operation
    """
    return f'''
def {op_name}(
    param1: str,
    param2: Optional[str] = None,
    **kwargs
) -> OperationResult:
    """
    {op_desc}

    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2 (optional)
        **kwargs: Additional operation-specific parameters

    Returns:
        OperationResult with operation-specific data

    Example:
        >>> result = {op_name}("value1", param2="value2")
        >>> if result.success:
        ...     print(result.data)

    Error Codes:
        - VALIDATION_ERROR: Invalid input parameters
        - OPERATION_ERROR: General operation failure
    """
    start_time = time.time()

    try:
        # Input validation
        _validate_input(param1, "param1")

        logger.info(f"Starting {op_name} with param1={{param1}}")

        # TODO: Implement operation logic here
        # Call core implementation functions
        result_data = {{
            'status': 'completed',
            'param1': param1,
            'param2': param2,
        }}

        duration = time.time() - start_time
        logger.info(f"{op_name} completed in {{duration:.3f}}s")

        return OperationResult(
            success=True,
            data=result_data,
            duration=duration,
            metadata=_build_metadata("{op_name}", param1=param1, param2=param2)
        )

    except ValueError as e:
        return OperationResult(
            success=False,
            error=f"Invalid input: {{str(e)}}",
            error_code=ErrorCodes.VALIDATION_ERROR,
            duration=time.time() - start_time
        )
    except Exception as e:
        logger.error(f"{op_name} failed: {{str(e)}}", exc_info=True)
        return OperationResult(
            success=False,
            error=f"Operation failed: {{str(e)}}",
            error_code=ErrorCodes.OPERATION_ERROR,
            duration=time.time() - start_time
        )
'''


def create_skill_files(
    skill_name: str,
    description: str,
    category: str,
    operations: List[Dict[str, str]],
    author: str
):
    """
    Create all skill files from templates.

    Args:
        skill_name: Skill name in kebab-case
        description: Skill description
        category: Skill category
        operations: List of operations
        author: Author name
    """
    print()
    print("Step 6: Generating Files")
    print("-" * 70)

    skill_path = SKILLS_DIR / skill_name
    created_date = datetime.now().strftime("%Y-%m-%d")

    # Create directories
    skill_path.mkdir(parents=True, exist_ok=True)
    (skill_path / "core").mkdir(exist_ok=True)
    (skill_path / "tests").mkdir(exist_ok=True)

    print(f"📁 Created directory: {skill_path}")

    # Prepare replacements
    operations_yaml = "\n".join([
        f'  {op["name"]}: "{op["description"]}"'
        for op in operations
    ])

    operations_doc = "\n\n".join([
        f'''### {op["name"]}

**Description:** {op["description"]}

**Parameters:**
- `param1` (str): Description of parameter
- `param2` (Optional[str]): Description of optional parameter

**Returns:**
- `OperationResult` with operation-specific data

**Example:**
```python
result = {op["name"]}(param1="value")
if result.success:
    print(result.data)
```'''
        for op in operations
    ])

    operations_functions = "\n".join([
        generate_operation_function(op["name"], op["description"])
        for op in operations
    ])

    operations_imports = ",\n".join([f'    "{op["name"]}"' for op in operations])
    operations_exports = ",\n".join([f'    "{op["name"]}"' for op in operations])

    changelog_operations = "\n".join([f'- Added {op["name"]} operation' for op in operations])

    operation_example = operations[0]["name"] if operations else "operation_name"
    operation_desc_example = operations[0]["description"] if operations else "Description"

    replacements = {
        '{{SKILL_NAME}}': skill_name,
        '{{SKILL_DESCRIPTION}}': description,
        '{{SKILL_CATEGORY}}': category,
        '{{AUTHOR_NAME}}': author,
        '{{CREATED_DATE}}': created_date,
        '{{OPERATIONS_YAML}}': operations_yaml,
        '{{OPERATIONS_DOCUMENTATION}}': operations_doc,
        '{{OPERATIONS_FUNCTIONS}}': operations_functions,
        '{{OPERATIONS_IMPORTS}}': operations_imports,
        '{{OPERATIONS_EXPORTS}}': operations_exports,
        '{{OPERATION_NAME_EXAMPLE}}': operation_example,
        '{{OPERATION_DESCRIPTION_EXAMPLE}}': operation_desc_example,
        '{{OPERATION_IMPORTS}}': ", ".join([op["name"] for op in operations]),
        '{{CHANGELOG_OPERATIONS}}': changelog_operations,
        '{{DETAILED_OVERVIEW}}': f"The {skill_name} skill provides {description.lower()}",
        '{{SKILL_PURPOSE}}': description.lower(),
        '{{EXAMPLE_USAGE}}': f"perform {operation_example.replace('_', ' ')}",
        '{{EXAMPLE_QUERY}}': f"{operation_desc_example}",
        '{{FEATURES_LIST}}': "\n".join([f"- {op['description']}" for op in operations]),
        '{{OPERATIONS_TABLE}}': "\n".join([
            f"| `{op['name']}` | {op['description']} |"
            for op in operations
        ]),
        '{{EXAMPLE_1_TITLE}}': f"Using {operation_example}",
        '{{EXAMPLE_1_CODE}}': f'result = {operation_example}(param1="value")\nif result.success:\n    print(result.data)',
        '{{EXAMPLE_2_TITLE}}': "Error Handling",
        '{{EXAMPLE_2_CODE}}': f'result = {operation_example}(param1="")\nif not result.success:\n    print(f"Error: {{result.error}}")',
        '{{DEPENDENCIES_LIST}}': "No external dependencies required.",
        '{{LICENSE_INFO}}': "[Add license information]",
        '{{RELATED_SKILLS_LIST}}': "[List related skills]",
        '{{EXAMPLE_AGENT_QUERY}}': operation_desc_example,
        '{{OPERATIONS_SUMMARY}}': "\n".join([f"- {op['name']}: {op['description']}" for op in operations]),
        '{{OPERATION_NAME_PASCAL}}': operations[0]["name"].title().replace("_", "") if operations else "OperationName",
        '{{OPERATION_NAME_SNAKE}}': operation_example,
    }

    # Copy and process template files
    template_files = [
        'skill.md',
        'operations.py',
        '__init__.py',
        'README.md',
        'demo.py',
        'core/__init__.py',
        'tests/__init__.py',
        'tests/test_operations.py'
    ]

    for template_file in template_files:
        template_path = TEMPLATE_DIR / template_file
        target_path = skill_path / template_file

        if not template_path.exists():
            print(f"⚠️  Template not found: {template_path}")
            continue

        # Read template
        with open(template_path, 'r') as f:
            content = f.read()

        # Replace placeholders
        for placeholder, value in replacements.items():
            content = content.replace(placeholder, value)

        # Write file
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with open(target_path, 'w') as f:
            f.write(content)

        print(f"✅ Created: {target_path.relative_to(PROJECT_ROOT)}")

    print()
    print("✅ Skill created successfully!")


def print_next_steps(skill_name: str):
    """
    Print next steps for the user.

    Args:
        skill_name: Name of the created skill
    """
    skill_path = SKILLS_DIR / skill_name

    print()
    print("=" * 70)
    print("Next Steps")
    print("=" * 70)
    print()
    print(f"Your skill has been created at: {skill_path}")
    print()
    print("To complete the implementation:")
    print()
    print(f"1. Implement core logic:")
    print(f"   cd {skill_path}/core")
    print(f"   # Create implementation modules here")
    print()
    print(f"2. Update operations.py:")
    print(f"   vim {skill_path}/operations.py")
    print(f"   # Connect operations to core implementation")
    print()
    print(f"3. Create and run demo:")
    print(f"   python {skill_path}/demo.py")
    print()
    print(f"4. Write and run tests:")
    print(f"   pytest {skill_path}/tests/ -v")
    print()
    print(f"5. Validate your skill:")
    print(f"   python scripts/validate-all.py")
    print()
    print("6. Review best practices:")
    print("   docs/ANTHROPIC_BEST_PRACTICES.md")
    print("   docs/BEST_PRACTICES_CHECKLIST.md")
    print()
    print("7. Test with an agent:")
    print(f'   Skill({skill_name}) with query: "[your query here]"')
    print()
    print("=" * 70)


def main():
    """Main function."""
    try:
        print_header()

        # Step 1: Skill name
        skill_name = prompt_skill_name()

        # Step 2: Description
        description = prompt_description()

        # Step 3: Category
        category = prompt_category()

        # Step 4: Operations
        operations = prompt_operations()

        # Step 5: Author
        author = prompt_author()

        # Summary
        print()
        print("=" * 70)
        print("Summary")
        print("=" * 70)
        print(f"Skill Name:  {skill_name}")
        print(f"Description: {description}")
        print(f"Category:    {category}")
        print(f"Author:      {author}")
        print(f"Operations:  {len(operations)}")
        for i, op in enumerate(operations, 1):
            print(f"  {i}. {op['name']}: {op['description']}")
        print()

        # Confirm
        confirm = input("Create this skill? (y/n): ").strip().lower()
        if confirm != 'y':
            print("\n❌ Skill creation cancelled.")
            return 1

        # Step 6: Create files
        create_skill_files(skill_name, description, category, operations, author)

        # Print next steps
        print_next_steps(skill_name)

        return 0

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        return 130
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

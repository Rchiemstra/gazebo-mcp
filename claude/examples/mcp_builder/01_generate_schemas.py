"""
Example 1: Generate MCP Schemas for Skills

This example demonstrates how to use the mcp_schema_generator skill to create
MCP tool schemas from existing skills.
"""

from skills.mcp_schema_generator import generate_schema, generate_batch_schemas, validate_schema
from skills.common.filters import ResultFilter


def example_1_basic_schema_generation():
    """Generate schema for a single skill."""
    print("=== Example 1: Basic Schema Generation ===\n")

    # Generate schema for code_analysis skill
    result = generate_schema("code_analysis", response_format="summary")

    if result.success:
        print(f"✓ Successfully generated schema for {result.data['skill_name']}")
        print(f"  Operations: {result.data['operations_count']}")
        print(f"  Operations list: {', '.join(result.data['operations'])}")
        print(f"  Duration: {result.duration:.3f}s")
    else:
        print(f"✗ Failed: {result.error}")

    print()


def example_2_complete_schema_with_details():
    """Generate complete schema with all details."""
    print("=== Example 2: Complete Schema with Details ===\n")

    result = generate_schema("code_analysis", response_format="complete")

    if result.success:
        schemas = result.data['schemas']
        print(f"✓ Generated {len(schemas)} schemas\n")

        # Show details of first schema
        first_schema = schemas[0]
        print(f"Schema: {first_schema['tool_name']}")
        print(f"Description: {first_schema['description']}")
        print(f"Parameters: {list(first_schema['input_schema']['properties'].keys())}")
        print(f"Examples: {len(first_schema.get('examples', []))}")

        # Validate the schema
        validation = validate_schema(first_schema)
        if validation.success:
            print(f"\nValidation Score: {validation.data['score']}/100")
            if validation.data['valid']:
                print("✓ Schema is valid")
            else:
                print(f"✗ Validation errors: {validation.data['errors']}")

    print()


def example_3_batch_generation():
    """Generate schemas for multiple skills efficiently."""
    print("=== Example 3: Batch Schema Generation ===\n")

    skills = ["code_analysis", "test_orchestrator", "learning_analytics"]

    result = generate_batch_schemas(skills, response_format="summary")

    if result.success:
        data = result.data
        print(f"✓ Batch generation complete")
        print(f"  Total skills: {data['total_skills']}")
        print(f"  Successful: {data['successful']}")
        print(f"  Failed: {data['failed']}")
        print(f"  Total schemas: {data['total_schemas']}")

        if data['failed_skills']:
            print(f"\n  Failed skills:")
            for failed in data['failed_skills']:
                print(f"    - {failed['skill']}: {failed['error']}")

        print(f"\n  Duration: {result.duration:.3f}s")

    print()


def example_4_token_efficiency():
    """Demonstrate token efficiency with filtering."""
    print("=== Example 4: Token Efficiency ===\n")

    # Generate complete schemas
    result = generate_batch_schemas(
        ["code_analysis", "test_orchestrator"],
        response_format="complete"
    )

    if result.success:
        schemas = result.data['schemas']

        print(f"Total schemas generated: {len(schemas)}")

        # Filter to only schemas with warnings
        schemas_with_warnings = ResultFilter.filter_by_predicate(
            schemas,
            lambda s: len(s.get('warnings', [])) > 0
        )

        print(f"Schemas with warnings: {len(schemas_with_warnings)}")

        # Get just the schema names
        schema_names = [s['tool_name'] for s in schemas]
        print(f"\nSchema names: {', '.join(schema_names)}")

        # Token savings: Instead of returning all schema details,
        # return just what's needed
        print(f"\nToken efficiency: Returned {len(schema_names)} names")
        print(f"instead of {len(schemas)} complete schemas")

    print()


def example_5_write_schemas_to_files():
    """Write generated schemas to JSON files."""
    print("=== Example 5: Write Schemas to Files ===\n")

    import json
    from pathlib import Path

    # Generate schemas
    result = generate_batch_schemas(["code_analysis"], response_format="complete")

    if result.success:
        schemas = result.data['schemas']

        # Create output directory
        output_dir = Path("mcp_schemas_output")
        output_dir.mkdir(exist_ok=True)

        # Write each schema to a file
        for schema in schemas:
            filename = f"{schema['tool_name']}.json"
            filepath = output_dir / filename

            with open(filepath, 'w') as f:
                json.dump(schema, f, indent=2)

            print(f"✓ Wrote {filepath}")

        print(f"\n  Total files written: {len(schemas)}")

    print()


if __name__ == "__main__":
    print("MCP Schema Generator Examples\n")
    print("=" * 60)
    print()

    example_1_basic_schema_generation()
    example_2_complete_schema_with_details()
    example_3_batch_generation()
    example_4_token_efficiency()
    example_5_write_schemas_to_files()

    print("=" * 60)
    print("\nAll examples complete!")
    print("\nNext steps:")
    print("- Try generating schemas for other skills")
    print("- Use schemas to create MCP adapters")
    print("- Validate your own custom schemas")

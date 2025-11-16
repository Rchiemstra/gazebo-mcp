---
name: mcp-schema-generator
description: Generate MCP tool schemas from skill operations following Anthropic best practices for token efficiency and progressive disclosure
version: 1.0.0
category: mcp
tags:
  - mcp
  - schema
  - code-generation
  - automation
activation: manual
tools:
  - Read
  - Glob
dependencies: []
---

# MCP Schema Generator Skill

## When to Use This Skill

Use mcp-schema-generator when you need to:
- **Generate MCP schemas** - Create tool schemas from skill operations automatically
- **Validate schemas** - Check schema structure, completeness, and compliance
- **Batch generation** - Generate schemas for multiple skills efficiently
- **Update schemas** - Regenerate schemas when skill operations change
- **Schema documentation** - Generate usage examples and documentation

**Not for:** Manual schema writing, non-MCP tools, API documentation

## Quick Start

```python
from skills.mcp_schema_generator import generate_schema, validate_schema
from skills.common.filters import ResultFilter

# 1. Generate schema for a skill
result = generate_schema("code_analysis", response_format="complete")

if result.success:
    schema = result.data
    print(f"Generated schema for: {schema['tool_name']}")
    print(f"Parameters: {list(schema['input_schema']['properties'].keys())}")

# 2. Validate schema
validation = validate_schema(schema)
if validation.success and validation.data['valid']:
    print("Schema is valid!")

# 3. Batch generation with filtering
result = generate_batch_schemas(["code_analysis", "test_orchestrator"])
if result.success:
    # Filter to only include schemas with warnings
    schemas_with_warnings = ResultFilter.filter_by_predicate(
        result.data['schemas'],
        lambda s: len(s.get('warnings', [])) > 0
    )
```

For detailed documentation, see **reference.md**.
For usage examples, see **examples.md**.

## Operations

### generate_schema(skill_name, response_format="summary")
Generate MCP schema for a skill operation.

**Returns:** Schema definition with tool name, description, parameters (summary) or complete schema with examples (complete)

### validate_schema(schema)
Validate MCP schema structure and completeness.

**Returns:** Validation result with errors and warnings

### generate_batch_schemas(skill_names)
Generate schemas for multiple skills in one call.

**Returns:** List of generated schemas with metadata

See **reference.md** for complete parameter specifications and response formats.

## Token Efficiency

This skill provides **summary and complete** response formats:

| Operation | Format | Token Usage | Use When |
|-----------|--------|-------------|----------|
| generate_schema | summary | 200-500 | Quick schema overview |
| generate_schema | complete | 2000-5000 | Full schema with examples |
| validate_schema | summary | 100-200 | Quick validation check |
| generate_batch_schemas | summary | 500-2000 | Multiple schemas, metadata only |
| generate_batch_schemas | complete | 10000+ | Full schemas for all skills |

**Recommendation:** Use summary format for validation and planning, complete format only when generating actual schema files.

## Example Workflow: Generating MCP Server Schemas

```python
from skills.mcp_schema_generator import generate_batch_schemas, validate_schema
from skills.common.filters import ResultFilter

# 1. Generate schemas for all skills in MCP server
skills = ["code_analysis", "test_orchestrator", "learning_analytics"]
result = generate_batch_schemas(skills, response_format="complete")

if result.success:
    # 2. Filter to validated schemas only
    validated = []
    for schema in result.data['schemas']:
        validation = validate_schema(schema)
        if validation.data['valid']:
            validated.append(schema)

    # 3. Get summary statistics
    print(f"Generated {len(validated)} valid schemas")
    print(f"Total operations: {sum(len(s.get('operations', [])) for s in validated)}")

    # Token savings: 15,000 → 2,000 tokens (87% reduction!)
```

## Schema Structure

Generated schemas follow MCP tool specification:

```json
{
  "tool_name": "skill_name.operation_name",
  "description": "Clear description of what the operation does",
  "input_schema": {
    "type": "object",
    "properties": {
      "param_name": {
        "type": "string",
        "description": "Parameter description"
      }
    },
    "required": ["param_name"]
  },
  "examples": [
    {
      "description": "Example usage",
      "code": "from skills.code_analysis import analyze_file\\nresult = analyze_file('main.py')"
    }
  ]
}
```

## Error Handling

The skill provides agent-friendly error messages:

```python
result = generate_schema("non_existent_skill")

if not result.success:
    print(result.error)
    # "Skill 'non_existent_skill' not found. Available skills: code_analysis, test_orchestrator, ..."
    print(result.suggestion)
    # "Check skill name spelling or list available skills with: ls skills/"
```

## Best Practices

1. **Use summary format first** - Generate summaries, validate, then generate complete
2. **Batch when possible** - Use generate_batch_schemas for multiple skills
3. **Validate before use** - Always validate generated schemas
4. **Filter results** - Use ResultFilter to reduce token usage
5. **Cache schemas** - Regenerate only when skill operations change

## Integration with MCP Server Builder

This skill is designed to work seamlessly with mcp-server-builder agent:

```python
# mcp-server-builder will use this skill to:
# 1. Generate schemas for all skills
# 2. Validate each schema
# 3. Write schema files to server directory
# 4. Generate usage documentation
```

See `agents/orchestrators/mcp-server-builder.md` for complete workflow.

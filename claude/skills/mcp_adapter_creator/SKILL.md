---
name: mcp-adapter-creator
description: Create MCP adapter files for skills with token efficiency patterns and usage examples
version: 1.0.0
category: mcp
tags:
  - mcp
  - adapter
  - code-generation
  - automation
activation: manual
tools:
  - Read
  - Write
  - Glob
dependencies: [mcp-schema-generator]
---

# MCP Adapter Creator Skill

## When to Use This Skill

Use mcp-adapter-creator when you need to:
- **Create MCP adapters** - Generate adapter files that expose skills via MCP
- **Batch adapter generation** - Create adapters for multiple skills efficiently
- **Update adapters** - Regenerate adapters when skills change
- **Documentation generation** - Generate usage examples and documentation

**Not for:** Manual adapter writing, non-MCP integrations

## Quick Start

```python
from skills.mcp_adapter_creator import create_adapter, create_batch_adapters

# 1. Create adapter for a single skill
result = create_adapter("code_analysis", response_format="complete")

if result.success:
    adapter_path = result.data['adapter_path']
    print(f"Adapter created at: {adapter_path}")

# 2. Batch creation
result = create_batch_adapters([
    {"name": "code_analysis"},
    {"name": "test_orchestrator"},
])

if result.success:
    print(f"Created {result.data['total_adapters']} adapters")
```

## Operations

### create_adapter(skill_name, operations=None, response_format="summary")
Create MCP adapter for a skill.

**Returns:** Adapter code and metadata (summary) or complete adapter with examples (complete)

### create_batch_adapters(skills, response_format="summary")
Create adapters for multiple skills.

**Returns:** List of created adapters with metadata

See **reference.md** for complete specifications.

## Token Efficiency

| Operation | Format | Token Usage | Use When |
|-----------|--------|-------------|----------|
| create_adapter | summary | 300-600 | Quick adapter metadata |
| create_adapter | complete | 3000-8000 | Full adapter with code |
| create_batch_adapters | summary | 1000-3000 | Multiple adapters, metadata |
| create_batch_adapters | complete | 20000+ | Full adapters for all skills |

## Adapter Structure

Generated adapters follow MCP best practices:

```python
"""
MCP Adapter for {skill_name} skill.

Exposes {skill_name} operations via MCP with local filtering.
Enables 98.7% token reduction by processing data locally.
"""

OPERATIONS = {
    "operation_name": {
        "description": "...",
        "parameters": {...},
        "returns": "...",
        "example": '''
from skills.{skill_name} import operation_name
from skills.common.filters import ResultFilter

result = operation_name(params)
filtered = ResultFilter.limit(result, 10)
        '''
    }
}
```

## Integration

Works seamlessly with mcp-server-builder agent:

```python
# mcp-server-builder will use this skill to:
# 1. Generate adapters for all skills
# 2. Write adapter files to server directory
# 3. Configure imports and exports
```

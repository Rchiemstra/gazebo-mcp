---
name: {{SKILL_NAME}}
version: 0.1.0
description: {{SKILL_DESCRIPTION}}
category: {{SKILL_CATEGORY}}
author: {{AUTHOR_NAME}}
created: {{CREATED_DATE}}
operations:
{{OPERATIONS_YAML}}
dependencies: []
tags: []
---

# {{SKILL_NAME}} Skill

## Overview

{{DETAILED_OVERVIEW}}

## Purpose

This skill provides operations for {{SKILL_PURPOSE}}.

## Operations

{{OPERATIONS_DOCUMENTATION}}

## Dependencies

This skill has no external dependencies.

## Integration with Agents

Agents can invoke this skill using:

```
Skill({{SKILL_NAME}}) with query: "natural language query describing what you need"
```

### Example Agent Usage

```markdown
I'll use the {{SKILL_NAME}} skill to {{EXAMPLE_USAGE}}.

Skill({{SKILL_NAME}}) with query: "{{EXAMPLE_QUERY}}"
```

## Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| `VALIDATION_ERROR` | Invalid input parameters | Review parameter requirements and types |
| `OPERATION_ERROR` | General operation failure | Check logs for detailed error information |
| `FILE_NOT_FOUND` | Required file/directory missing | Verify file paths and existence |

## Performance

- Target operation duration: < 200ms
- Maximum operation duration: < 2000ms
- All operations track execution time

## Testing

### Run Demo
```bash
python skills/{{SKILL_NAME}}/demo.py
```

### Run Tests
```bash
pytest skills/{{SKILL_NAME}}/tests/
```

## Development

### Adding New Operations

1. Define operation in `skill.md` frontmatter
2. Implement operation in `operations.py`
3. Export operation in `__init__.py`
4. Add tests in `tests/` directory
5. Update README.md with usage examples

### Code Style

- Use Black for formatting: `black skills/{{SKILL_NAME}}/`
- Use Flake8 for linting: `flake8 skills/{{SKILL_NAME}}/`
- Follow PEP 8 style guide

## Changelog

### 0.1.0 ({{CREATED_DATE}})
- Initial implementation
{{CHANGELOG_OPERATIONS}}

## Contributing

When contributing to this skill:
- Follow the standardized OperationResult format
- Include comprehensive error handling
- Track operation duration
- Add tests for new operations
- Update documentation

## License

[Add license information]

## Support

For issues or questions:
- GitHub Issues: [Link to issues]
- Documentation: `docs/SKILLS_SYSTEM_OVERVIEW.md`

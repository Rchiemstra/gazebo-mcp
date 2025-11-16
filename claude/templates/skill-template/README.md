# {{SKILL_NAME}} Skill

{{SKILL_DESCRIPTION}}

## Features

{{FEATURES_LIST}}

## Installation

This skill is part of the Claude Code skills system and requires no additional installation.

## Usage

### From Python

```python
from skills.{{SKILL_NAME}} import {{OPERATION_NAME_EXAMPLE}}

# Example usage
result = {{OPERATION_NAME_EXAMPLE}}(
    param1="value1",
    param2="value2"
)

if result.success:
    print(f"Success! Result: {result.data}")
    print(f"Duration: {result.duration:.3f}s")
else:
    print(f"Error: {result.error} (Code: {result.error_code})")
```

### From Agents

Agents can invoke this skill using natural language queries:

```markdown
Skill({{SKILL_NAME}}) with query: "{{EXAMPLE_AGENT_QUERY}}"
```

## Operations

{{OPERATIONS_TABLE}}

## Examples

### Example 1: {{EXAMPLE_1_TITLE}}

```python
{{EXAMPLE_1_CODE}}
```

### Example 2: {{EXAMPLE_2_TITLE}}

```python
{{EXAMPLE_2_CODE}}
```

## Error Handling

All operations return an `OperationResult` object with standardized error codes:

| Error Code | Description | How to Handle |
|------------|-------------|---------------|
| `VALIDATION_ERROR` | Invalid input parameters | Check parameter types and values |
| `OPERATION_ERROR` | General operation failure | Check logs for details |
| `FILE_NOT_FOUND` | Required file missing | Verify file paths exist |

Example error handling:

```python
result = {{OPERATION_NAME_EXAMPLE}}(param="value")

if not result.success:
    if result.error_code == "VALIDATION_ERROR":
        print("Please check your input parameters")
    elif result.error_code == "FILE_NOT_FOUND":
        print(f"File not found: {result.error}")
    else:
        print(f"Unexpected error: {result.error}")
```

## Performance

- **Target Duration:** < 200ms per operation
- **Maximum Duration:** < 2000ms per operation
- All operations track execution time in `result.duration`

## Testing

Run the demonstration:
```bash
python skills/{{SKILL_NAME}}/demo.py
```

Run unit tests:
```bash
pytest skills/{{SKILL_NAME}}/tests/ -v
```

## Development

### Project Structure

```
{{SKILL_NAME}}/
├── skill.md              # Skill metadata and documentation
├── operations.py         # Standardized operations interface
├── __init__.py           # Package exports
├── README.md             # This file
├── demo.py               # Usage demonstration
├── core/                 # Core implementation modules
│   ├── __init__.py
│   └── [implementation modules]
└── tests/                # Unit tests
    ├── __init__.py
    └── test_operations.py
```

### Adding New Operations

1. Define operation in `skill.md` frontmatter
2. Implement function in `operations.py`
3. Export in `__init__.py`
4. Add tests in `tests/`
5. Update this README

### Code Style

- **Formatter:** Black (`black skills/{{SKILL_NAME}}/`)
- **Linter:** Flake8 (`flake8 skills/{{SKILL_NAME}}/`)
- **Style Guide:** PEP 8

## Dependencies

{{DEPENDENCIES_LIST}}

## Contributing

Contributions are welcome! Please:
1. Follow the standardized `OperationResult` format
2. Include comprehensive error handling
3. Add tests for new operations
4. Update documentation

## Changelog

See `skill.md` for detailed changelog.

## License

{{LICENSE_INFO}}

## Support

- **Documentation:** `/docs/SKILLS_SYSTEM_OVERVIEW.md`
- **Issues:** [GitHub Issues]
- **Questions:** [GitHub Discussions]

## Related Skills

{{RELATED_SKILLS_LIST}}

## Author

{{AUTHOR_NAME}} - {{CREATED_DATE}}

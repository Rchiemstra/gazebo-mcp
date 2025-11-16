# MCP Server Builder Examples

This directory contains comprehensive examples for using the MCP Server Builder system to create production-ready MCP servers following Anthropic best practices.

## Overview

The MCP Server Builder system consists of:
- **3 Skills**: Schema generator, adapter creator, security validator
- **2 Agents**: Server architect (design), server builder (implementation)

## Examples

### 1. Generate MCP Schemas (`01_generate_schemas.py`)

Learn how to generate MCP tool schemas from existing skills:
- Basic schema generation
- Complete schemas with all details
- Batch generation for multiple skills
- Token efficiency patterns
- Writing schemas to files

**Run:** `python examples/mcp_builder/01_generate_schemas.py`

### 2. Create MCP Adapters (`02_create_adapters.py`)

Learn how to create MCP adapter files:
- Basic adapter creation
- View generated adapter code
- Batch adapter creation
- Specific operations only
- Save adapters to custom directory
- Analyze adapter structure

**Run:** `python examples/mcp_builder/02_create_adapters.py`

### 3. Validate Security (`03_validate_security.py`)

Learn how to validate MCP server security:
- Validate existing servers
- Detailed security reports
- Validate sandbox configuration
- Compare configurations
- Filter security issues by severity
- Security checklists

**Run:** `python examples/mcp_builder/03_validate_security.py`

## Quick Start

```python
# 1. Generate schemas for your skills
from skills.mcp_schema_generator import generate_batch_schemas

result = generate_batch_schemas(["code_analysis", "test_orchestrator"])

# 2. Create adapters
from skills.mcp_adapter_creator import create_batch_adapters

skills = [{"name": "code_analysis"}, {"name": "test_orchestrator"}]
result = create_batch_adapters(skills)

# 3. Validate security
from skills.mcp_security_validator import validate_server_security

result = validate_server_security("mcp/servers/my-server")
print(f"Security Score: {result.data['security_score']}/100")
```

## Complete Workflow

For the complete end-to-end workflow of creating an MCP server:

1. **Design Phase** - Use `mcp-server-architect` agent to analyze and plan
2. **Implementation Phase** - Use `mcp-server-builder` orchestrator to build
3. **Validation Phase** - Ensure security score >= 90/100
4. **Deployment** - Deploy to Claude Desktop

See `docs/MCP_BUILDER_IMPLEMENTATION_PLAN.md` for detailed documentation.

## Expected Results

When following these examples, you should achieve:
- ✅ Valid MCP schemas for all operations
- ✅ Token-efficient adapters (98.7% reduction)
- ✅ Security score >= 90/100
- ✅ Production-ready MCP server

## Token Efficiency

All examples demonstrate token efficiency patterns:
- Use `response_format="summary"` for quick checks
- Use `response_format="complete"` only when needed
- Filter results locally with `ResultFilter`
- Batch operations for multiple skills

## Security Best Practices

Examples follow Anthropic's security best practices:
- Filesystem isolation (workspace + /tmp only)
- Network filtering (allowed domains only)
- Resource limits (CPU, memory, processes)
- Code validation (AST-based)
- No sensitive data in errors

## Troubleshooting

**Schema generation fails:**
- Ensure skill has `SKILL.md` with YAML frontmatter
- Ensure `operations.py` has public functions
- Check skill name spelling

**Adapter creation fails:**
- Ensure `mcp_schema_generator` skill is available
- Check schema validation passes
- Verify skill exists

**Security validation shows low score:**
- Add security configuration to `config.py`
- Configure filesystem isolation
- Set up network filtering
- Define resource limits

## Next Steps

After running these examples:
1. Try with your own custom skills
2. Create a complete MCP server using the orchestrator
3. Deploy to Claude Desktop
4. Test with real workloads
5. Monitor token efficiency gains

## Documentation

- **Implementation Plan**: `docs/MCP_BUILDER_IMPLEMENTATION_PLAN.md`
- **Skills Documentation**: `skills/mcp_*/SKILL.md`
- **Agents Documentation**: `agents/mcp-server-*.md`

## Support

For issues or questions:
- Review the implementation plan
- Check skill SKILL.md files
- Run tests: `pytest skills/mcp_*/tests/`
- See integration tests: `tests/integration/test_mcp_builder_workflow.py`

---
name: mcp-security-validator
description: Validate MCP server security configuration following Anthropic best practices for sandboxing and isolation
version: 1.0.0
category: mcp
tags:
  - mcp
  - security
  - validation
  - sandboxing
activation: manual
tools:
  - Read
  - Glob
dependencies: []
---

# MCP Security Validator Skill

## When to Use This Skill

Use mcp-security-validator when you need to:
- **Validate MCP server security** - Check security configuration and compliance
- **Audit sandbox configuration** - Verify filesystem and network isolation
- **Check resource limits** - Validate CPU, memory, and process limits
- **Security scoring** - Get security score and recommendations

**Not for:** Application security audits, vulnerability scanning

## Quick Start

```python
from skills.mcp_security_validator import validate_server_security, validate_sandbox_config

# 1. Validate complete MCP server
result = validate_server_security("mcp/servers/my-mcp-server/")

if result.success:
    score = result.data['security_score']
    print(f"Security Score: {score}/100")

    # Filter to critical issues only
    from skills.common.filters import ResultFilter
    critical = ResultFilter.filter_by_field(
        result.data['issues'],
        "severity",
        "critical"
    )

# 2. Validate sandbox config
config = {...}
result = validate_sandbox_config(config)
```

## Operations

### validate_server_security(server_path, response_format="summary")
Validate complete MCP server security.

**Returns:** Security score, issues, and recommendations

### validate_sandbox_config(config)
Validate sandbox configuration dict.

**Returns:** Validation results with specific checks

## Security Checks

1. **Filesystem Isolation** - Workspace/tmp access only, sensitive paths blocked
2. **Network Filtering** - Allowed domains configured, default deny
3. **Resource Limits** - CPU, memory, process limits set
4. **Code Validation** - AST validation, dangerous functions blocked
5. **Error Handling** - Proper exceptions, no sensitive data in errors

## Security Score

- 90-100: Excellent - Production ready
- 70-89: Good - Minor improvements needed
- 50-69: Fair - Security issues to address
- 0-49: Poor - Critical issues, not production ready

## Integration

Works with mcp-server-builder to ensure security compliance.

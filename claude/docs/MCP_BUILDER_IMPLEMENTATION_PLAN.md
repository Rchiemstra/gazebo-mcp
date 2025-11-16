# MCP Server Builder Implementation Plan
**Agents and Skills for Creating MCP Servers Following Best Practices**

**Date:** 2025-11-11
**Branch:** `claude/mcp-agents-skills-plan-011CV2JKiWVYdGSwuXXGvXsk`
**Status:** Ready for Implementation

---

## Executive Summary

This plan implements a comprehensive system for creating MCP (Model Context Protocol) servers following Anthropic's best practices. The system provides:

1. **3 specialized skills** for MCP server components
2. **2 coordinating agents** for MCP server architecture and building
3. **Complete testing and documentation**

**Key Goals:**
- Enable developers to create production-ready MCP servers efficiently
- Enforce Anthropic's MCP best practices automatically
- Provide comprehensive validation and security checks
- Generate complete, maintainable server code

**Expected Benefits:**
- ✅ 80% faster MCP server creation
- ✅ 100% adherence to security best practices
- ✅ Reduced errors through automated validation
- ✅ Consistent server architecture across projects

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [MCP Best Practices Summary](#mcp-best-practices-summary)
3. [Skills Implementation](#skills-implementation)
4. [Agents Implementation](#agents-implementation)
5. [Testing Strategy](#testing-strategy)
6. [Documentation](#documentation)
7. [Implementation Timeline](#implementation-timeline)

---

## Architecture Overview

### System Components

```
MCP Server Builder System
│
├── Skills (Python Code)
│   ├── mcp_schema_generator     - Generate MCP tool schemas
│   ├── mcp_adapter_creator      - Create skill adapters for MCP
│   └── mcp_security_validator   - Validate MCP server security
│
└── Agents (Coordination)
    ├── mcp-server-architect     - Design MCP server architecture
    └── mcp-server-builder       - Orchestrate server creation
```

### Workflow

```
User Request: "Create MCP server for my skills"
    ↓
mcp-server-architect (Design Phase)
    ├─→ Analyzes existing skills
    ├─→ Plans server architecture
    ├─→ Identifies security requirements
    └─→ Creates implementation plan
    ↓
mcp-server-builder (Implementation Phase)
    ├─→ Generates schemas (mcp_schema_generator)
    ├─→ Creates adapters (mcp_adapter_creator)
    ├─→ Validates security (mcp_security_validator)
    └─→ Assembles complete server
    ↓
Complete MCP Server
    ├── server.py (main server)
    ├── adapters/ (skill adapters)
    ├── schema/ (MCP schemas)
    ├── tests/ (comprehensive tests)
    └── README.md (documentation)
```

---

## MCP Best Practices Summary

### Core Principles (from Anthropic)

1. **Token Efficiency**
   - Enable 98.7% token reduction through local filtering
   - Return only filtered results to model
   - Use ResultFilter for data processing

2. **Security**
   - Sandboxed code execution
   - Filesystem isolation (workspace + /tmp only)
   - Network filtering (allowed domains only)
   - Resource limits (CPU, memory, time)
   - AST validation for dangerous operations

3. **Progressive Disclosure**
   - Minimal tool descriptions upfront
   - Load details on-demand
   - Filesystem-based tool discovery

4. **Code Execution Pattern**
   - Skills as importable Python modules
   - Agents generate code that filters locally
   - State persistence between calls

5. **Desktop Extension Packaging**
   - .mcpb packages for one-click install
   - Automatic security updates
   - OS keychain integration

### Security Requirements

**Filesystem Isolation:**
- ✅ Allow: workspace directory, /tmp
- ❌ Block: /root, SSH keys, ~/.aws, system files
- 🔒 Read-only: /usr, /lib, system libraries

**Network Isolation:**
- ✅ Allow: api.anthropic.com, pypi.org, github.com
- ❌ Block: All other domains
- 📝 Log all requests for audit

**Resource Limits:**
- ⏱️ CPU time: 30 seconds max
- 💾 Memory: 512 MB max
- 🔢 Processes: 10 max

**Code Validation:**
- ❌ Block: eval(), exec(), __import__()
- ❌ Block: Unauthorized imports
- ✅ Allow: Skills imports, common stdlib

---

## Skills Implementation

### 1. mcp_schema_generator

**Purpose:** Generate MCP tool schemas from skill operations

**Location:** `skills/mcp_schema_generator/`

**Operations:**

#### generate_schema(skill_name: str, response_format: str = "summary") -> OperationResult
Generate MCP schema for a skill.

**Parameters:**
- `skill_name`: Name of skill (e.g., "code_analysis")
- `response_format`: "summary" | "detailed" | "complete"

**Returns:**
```python
{
    "success": true,
    "data": {
        "tool_name": "code_analysis.analyze_codebase",
        "description": "Analyze entire codebase...",
        "input_schema": {
            "type": "object",
            "properties": {...},
            "required": [...]
        },
        "examples": [...]
    }
}
```

#### validate_schema(schema: dict) -> OperationResult
Validate MCP schema structure.

**Parameters:**
- `schema`: MCP schema dictionary

**Returns:**
```python
{
    "success": true,
    "data": {
        "valid": true,
        "errors": [],
        "warnings": ["Consider adding example usage"]
    }
}
```

#### generate_batch_schemas(skill_names: List[str]) -> OperationResult
Generate schemas for multiple skills.

**Features:**
- ✅ Parses skill SKILL.md for metadata
- ✅ Extracts operations from operations.py
- ✅ Generates JSON schemas automatically
- ✅ Validates parameter types
- ✅ Creates usage examples
- ✅ Supports response_format filtering

**Example Usage:**
```python
from skills.mcp_schema_generator import generate_schema
from skills.common.filters import ResultFilter

# Generate schema for code_analysis skill
result = generate_schema("code_analysis", response_format="complete")

if result.success:
    schema = result.data
    print(f"Tool: {schema['tool_name']}")
    print(f"Parameters: {list(schema['input_schema']['properties'].keys())}")
```

---

### 2. mcp_adapter_creator

**Purpose:** Create MCP adapter files for skills

**Location:** `skills/mcp_adapter_creator/`

**Operations:**

#### create_adapter(skill_name: str, operations: List[str] = None) -> OperationResult
Create MCP adapter for a skill.

**Parameters:**
- `skill_name`: Name of skill
- `operations`: Optional list of operations to include (default: all)

**Returns:**
```python
{
    "success": true,
    "data": {
        "adapter_path": "mcp/servers/skills-mcp/adapters/code_analysis.py",
        "operations_count": 5,
        "example_code": "...",
        "documentation": "..."
    }
}
```

#### create_batch_adapters(skills: List[dict]) -> OperationResult
Create adapters for multiple skills.

**Features:**
- ✅ Generates adapter.py files
- ✅ Imports skill operations correctly
- ✅ Adds token efficiency documentation
- ✅ Creates usage examples
- ✅ Handles error cases
- ✅ Validates skill exists

**Example Usage:**
```python
from skills.mcp_adapter_creator import create_adapter

# Create adapter for test_orchestrator skill
result = create_adapter(
    skill_name="test_orchestrator",
    operations=["generate_tests", "analyze_coverage"]
)

if result.success:
    print(f"Adapter created at: {result.data['adapter_path']}")
    print(f"Operations: {result.data['operations_count']}")
```

**Adapter Template:**
```python
"""
MCP Adapter for {skill_name} skill.

Exposes {skill_name} operations via MCP with local filtering.
Enables 98.7% token reduction by processing data locally.

Example usage in agent-generated code:
    from skills.{skill_name} import {main_operation}
    from skills.common.filters import ResultFilter

    # Execute operation
    result = {main_operation}(params)

    # Filter locally (98.7% token savings!)
    filtered = ResultFilter.limit(result, 5)
"""

OPERATIONS = {
    "{operation_name}": {
        "description": "...",
        "parameters": {...},
        "returns": "...",
        "example": '''
from skills.{skill_name} import {operation_name}
from skills.common.filters import ResultFilter

# Example usage
result = {operation_name}(params)
filtered = ResultFilter.limit(result, 10)
        '''
    }
}
```

---

### 3. mcp_security_validator

**Purpose:** Validate MCP server security configuration

**Location:** `skills/mcp_security_validator/`

**Operations:**

#### validate_server_security(server_path: str) -> OperationResult
Validate security configuration of MCP server.

**Parameters:**
- `server_path`: Path to MCP server directory

**Returns:**
```python
{
    "success": true,
    "data": {
        "security_score": 95,
        "checks_passed": 18,
        "checks_failed": 1,
        "issues": [
            {
                "severity": "medium",
                "issue": "Network filtering not configured",
                "recommendation": "Add allowed_domains configuration",
                "file": "server.py:45"
            }
        ],
        "recommendations": [...]
    }
}
```

#### validate_sandbox_config(config: dict) -> OperationResult
Validate sandbox configuration.

**Security Checks:**

1. **Filesystem Isolation**
   - ✅ Workspace directory properly configured
   - ✅ /tmp access enabled
   - ❌ No access to sensitive paths (/root, ~/.ssh, ~/.aws)
   - ✅ System paths read-only

2. **Network Filtering**
   - ✅ Allowed domains configured
   - ✅ Default deny policy
   - ✅ Logging enabled for audit

3. **Resource Limits**
   - ✅ CPU timeout set (≤ 30s)
   - ✅ Memory limit set (≤ 512MB)
   - ✅ Process limit set (≤ 10)

4. **Code Validation**
   - ✅ AST validation enabled
   - ✅ Dangerous functions blocked (eval, exec)
   - ✅ Import whitelist configured

5. **Error Handling**
   - ✅ Proper exception handling
   - ✅ Agent-friendly error messages
   - ✅ No sensitive data in errors

**Example Usage:**
```python
from skills.mcp_security_validator import validate_server_security
from skills.common.filters import ResultFilter

# Validate MCP server security
result = validate_server_security("mcp/servers/my-mcp-server/")

if result.success:
    score = result.data['security_score']
    issues = result.data['issues']

    print(f"Security Score: {score}/100")

    # Filter to high-severity issues only
    critical = ResultFilter.filter_by_field(
        issues, "severity", "critical"
    )

    if critical:
        print(f"CRITICAL ISSUES: {len(critical)}")
        for issue in critical:
            print(f"  - {issue['issue']} ({issue['file']})")
```

---

## Agents Implementation

### 1. mcp-server-architect

**Purpose:** Design MCP server architecture following best practices

**Type:** Planning Agent (uses Think tool)

**Location:** `agents/mcp-server-architect.md`

**Mission:**
Analyze requirements and design MCP server architecture following Anthropic's best practices. Provide detailed implementation plan with security considerations.

**Workflow:**

#### Phase 1: Requirements Analysis
**Goal:** Understand what skills need MCP server

**Actions:**
1. **Discover skills**
   ```python
   from skills.code_search import find_skills
   skills = find_skills()
   ```

2. **Analyze each skill**
   - Read SKILL.md metadata
   - Identify operations
   - Check token efficiency patterns
   - Determine if MCP-suitable

3. **Use Think tool for analysis**
   ```python
   think(reasoning='''
   Analyzing skills for MCP server creation.

   Skills found: code_analysis, test_orchestrator, learning_analytics

   code_analysis:
   - 3 operations: analyze_codebase, analyze_file, generate_dependency_graph
   - Returns large datasets (10K+ files)
   - Perfect MCP candidate (98% token savings potential)

   test_orchestrator:
   - 2 operations: generate_tests, analyze_coverage
   - Returns medium datasets (100-1000 tests)
   - Good MCP candidate (90% token savings)

   learning_analytics:
   - 4 operations: analyze_student, get_learning_history, etc.
   - Returns large historical data
   - Excellent MCP candidate (99% token savings)

   Decision: Create MCP server with all 3 skills
   Priority: code_analysis (highest impact)
   ''', decision="Create MCP server with 3 skills", confidence=0.95)
   ```

**Expected Output:**
- List of skills to include
- Priority order
- Expected token savings
- Initial architecture sketch

**Decision Point:** Confirm skill selection with user

---

#### Phase 2: Architecture Design
**Goal:** Design complete MCP server structure

**Actions:**
1. **Plan directory structure**
   ```
   mcp/servers/{server_name}/
   ├── server.py               # Main MCP server
   ├── adapters/               # Skill adapters
   │   ├── __init__.py
   │   ├── code_analysis.py
   │   ├── test_orchestrator.py
   │   └── learning_analytics.py
   ├── schema/                 # MCP schemas
   │   └── tools.json
   ├── tests/                  # Comprehensive tests
   │   ├── test_server.py
   │   ├── test_adapters.py
   │   └── test_security.py
   ├── README.md               # Documentation
   └── config.py               # Configuration
   ```

2. **Design security configuration**
   ```python
   security_config = {
       "filesystem": {
           "allowed_paths": ["workspace", "/tmp"],
           "blocked_paths": ["/root", "~/.ssh", "~/.aws"],
           "system_readonly": True
       },
       "network": {
           "allowed_domains": [
               "api.anthropic.com",
               "pypi.org",
               "github.com"
           ],
           "default_policy": "deny",
           "log_requests": True
       },
       "resources": {
           "cpu_timeout": 30,
           "memory_limit_mb": 512,
           "max_processes": 10
       }
   }
   ```

3. **Use Think tool for design decisions**
   ```python
   think(reasoning='''
   Designing security configuration.

   Question: Should we allow network access to PyPI?

   Analysis:
   - Skills may need to install dependencies
   - PyPI is trusted, official Python repository
   - Can be isolated to specific endpoints
   - Risk: Supply chain attacks (low if we validate packages)

   Question: Should we use filesystem-based or JSON-RPC protocol?

   Analysis:
   - Filesystem: Better progressive disclosure, natural navigation
   - JSON-RPC: More standard, better tooling
   - Anthropic recommends filesystem for Claude Desktop

   Decision: Use filesystem-based + JSON-RPC fallback
   Allow PyPI with package validation
   ''', decision="Filesystem-based protocol with PyPI allowed", confidence=0.85)
   ```

**Expected Output:**
- Complete directory structure
- Security configuration
- Protocol selection
- Integration patterns

**Decision Point:** Review architecture with user

---

#### Phase 3: Implementation Planning
**Goal:** Create detailed implementation plan

**Actions:**
1. **Generate task breakdown**
   - Schema generation tasks
   - Adapter creation tasks
   - Security validation tasks
   - Testing tasks
   - Documentation tasks

2. **Identify dependencies**
   - Skills → Adapters
   - Adapters → Schemas
   - Schemas → Server
   - Server → Tests

3. **Estimate effort and risks**
   ```python
   think(reasoning='''
   Planning implementation.

   Tasks:
   1. Generate schemas for 3 skills (2 hours)
   2. Create adapters for 3 skills (3 hours)
   3. Implement main server (4 hours)
   4. Configure security (2 hours)
   5. Write tests (3 hours)
   6. Documentation (2 hours)
   Total: 16 hours

   Risks:
   - Schema complexity for code_analysis (HIGH)
     Mitigation: Generate incrementally, validate each operation

   - Security configuration on different OS (MEDIUM)
     Mitigation: Use platform-specific sandboxing (bwrap/seatbelt)

   - Integration testing complexity (MEDIUM)
     Mitigation: Use existing MCP server as reference

   Decision: Implement in phases, validate security first
   ''', decision="Phased implementation, security-first", confidence=0.9)
   ```

**Expected Output:**
- Task list with dependencies
- Effort estimates
- Risk mitigation plan
- Implementation phases

**Decision Point:** Approve implementation plan

---

### 2. mcp-server-builder

**Purpose:** Orchestrate MCP server creation using skills

**Type:** Orchestrator Agent (coordinates workers/skills)

**Location:** `agents/orchestrators/mcp-server-builder.md`

**Mission:**
Build complete MCP server by coordinating schema generation, adapter creation, security validation, and testing. Ensures 100% adherence to best practices.

**Required Skills:**
- `mcp_schema_generator` (required) - Generate MCP schemas
- `mcp_adapter_creator` (required) - Create skill adapters
- `mcp_security_validator` (required) - Validate security
- `code_analysis` (optional) - Analyze existing skills
- `doc_generator` (optional) - Generate documentation

**Workflow:**

#### Phase 1: Setup & Validation
**Goal:** Validate requirements and setup project structure

**Actions:**
1. **Verify skills exist**
   ```python
   try:
       from skills.mcp_schema_generator import generate_schema
       from skills.mcp_adapter_creator import create_adapter
       from skills.mcp_security_validator import validate_server_security
   except ImportError as e:
       raise MissingSkillError(f"Required skill not found: {e}")
   ```

2. **Load architecture plan**
   - Read plan from mcp-server-architect
   - Validate completeness
   - Confirm user approval

3. **Create directory structure**
   ```python
   from pathlib import Path

   server_dir = Path("mcp/servers/my-mcp-server")
   server_dir.mkdir(parents=True, exist_ok=True)
   (server_dir / "adapters").mkdir(exist_ok=True)
   (server_dir / "schema").mkdir(exist_ok=True)
   (server_dir / "tests").mkdir(exist_ok=True)
   ```

**Expected Output:**
- ✅ Skills verified
- ✅ Architecture loaded
- ✅ Directories created
- ✅ Ready for generation

**Decision Point:** Continue to generation?

---

#### Phase 2: Schema Generation
**Goal:** Generate MCP schemas for all skills

**Actions:**
1. **Generate schemas in parallel** (if using multi-agent)
   ```python
   from skills.mcp_schema_generator import generate_batch_schemas

   skills_to_process = [
       "code_analysis",
       "test_orchestrator",
       "learning_analytics"
   ]

   # Generate all schemas
   result = generate_batch_schemas(skills_to_process)

   if result.success:
       schemas = result.data['schemas']
       print(f"Generated {len(schemas)} schemas")
   ```

2. **Validate each schema**
   ```python
   from skills.mcp_schema_generator import validate_schema

   for schema in schemas:
       validation = validate_schema(schema)
       if not validation.data['valid']:
           print(f"Schema validation failed: {validation.data['errors']}")
   ```

3. **Write schema files**
   ```python
   import json

   for schema in schemas:
       schema_path = server_dir / "schema" / f"{schema['tool_name']}.json"
       with open(schema_path, 'w') as f:
           json.dump(schema, f, indent=2)
   ```

**Expected Output:**
- ✅ All schemas generated
- ✅ All schemas validated
- ✅ Schema files written
- 📊 Token efficiency metrics

**Decision Point:** Review schemas before proceeding?

---

#### Phase 3: Adapter Creation
**Goal:** Create MCP adapters for all skills

**Actions:**
1. **Generate adapters**
   ```python
   from skills.mcp_adapter_creator import create_batch_adapters

   skills_config = [
       {
           "name": "code_analysis",
           "operations": ["analyze_codebase", "analyze_file", "generate_dependency_graph"]
       },
       {
           "name": "test_orchestrator",
           "operations": ["generate_tests", "analyze_coverage"]
       },
       {
           "name": "learning_analytics",
           "operations": ["analyze_student", "get_learning_history"]
       }
   ]

   result = create_batch_adapters(skills_config)

   if result.success:
       adapters = result.data['adapters']
       print(f"Created {len(adapters)} adapters")

       # Write adapter files
       for adapter in adapters:
           adapter_path = server_dir / "adapters" / f"{adapter['skill_name']}.py"
           with open(adapter_path, 'w') as f:
               f.write(adapter['code'])
   ```

2. **Generate __init__.py for adapters**
   ```python
   init_content = '''"""MCP adapters for skills."""

   from . import code_analysis
   from . import test_orchestrator
   from . import learning_analytics

   __all__ = [
       "code_analysis",
       "test_orchestrator",
       "learning_analytics"
   ]
   '''

   with open(server_dir / "adapters" / "__init__.py", 'w') as f:
       f.write(init_content)
   ```

**Expected Output:**
- ✅ All adapters created
- ✅ Adapter files written
- ✅ Imports configured
- 📝 Usage examples generated

---

#### Phase 4: Server Implementation
**Goal:** Create main MCP server file

**Actions:**
1. **Generate server.py from template**
   ```python
   from skills.mcp_adapter_creator import generate_server_template

   server_code = generate_server_template(
       server_name="my-mcp-server",
       skills=skills_config,
       security_config=security_config
   )

   with open(server_dir / "server.py", 'w') as f:
       f.write(server_code)
   ```

2. **Generate config.py**
   ```python
   config_code = f'''"""Configuration for MCP server."""

   import os
   from pathlib import Path

   # Workspace configuration
   WORKSPACE_DIR = os.getenv("WORKSPACE_DIR", os.getcwd())

   # Security configuration
   ALLOWED_PATHS = [WORKSPACE_DIR, "/tmp"]
   BLOCKED_PATHS = ["/root", str(Path.home() / ".ssh"), str(Path.home() / ".aws")]

   ALLOWED_DOMAINS = [
       "api.anthropic.com",
       "pypi.org",
       "github.com"
   ]

   # Resource limits
   CPU_TIMEOUT = 30  # seconds
   MEMORY_LIMIT_MB = 512
   MAX_PROCESSES = 10
   '''

   with open(server_dir / "config.py", 'w') as f:
       f.write(config_code)
   ```

**Expected Output:**
- ✅ server.py created
- ✅ config.py created
- ✅ Entry points configured
- 🔧 Ready for testing

---

#### Phase 5: Security Validation
**Goal:** Validate server security configuration

**Actions:**
1. **Run comprehensive security validation**
   ```python
   from skills.mcp_security_validator import validate_server_security
   from skills.common.filters import ResultFilter

   # Validate security
   result = validate_server_security(str(server_dir))

   if result.success:
       score = result.data['security_score']
       issues = result.data['issues']

       print(f"Security Score: {score}/100")

       # Filter to critical/high issues only
       critical = ResultFilter.filter_by_field(
           issues, "severity", "critical"
       )
       high = ResultFilter.filter_by_field(
           issues, "severity", "high"
       )

       blocking_issues = critical + high

       if blocking_issues:
           print(f"BLOCKING ISSUES: {len(blocking_issues)}")
           for issue in blocking_issues:
               print(f"  [{issue['severity'].upper()}] {issue['issue']}")
               print(f"  File: {issue['file']}")
               print(f"  Fix: {issue['recommendation']}")

           # Stop if critical issues found
           if critical:
               raise SecurityError("Critical security issues must be fixed")
   ```

2. **Apply recommended fixes**
   ```python
   # Auto-fix common issues
   for issue in issues:
       if issue.get('auto_fix_available'):
           apply_security_fix(issue)
   ```

**Expected Output:**
- ✅ Security score ≥ 90/100
- ✅ No critical issues
- ⚠️ Warnings documented
- 🔐 Security audit complete

**Decision Point:** Abort if critical issues found

---

#### Phase 6: Testing
**Goal:** Generate and run comprehensive tests

**Actions:**
1. **Generate test files**
   ```python
   # Generate test_server.py
   test_server_code = '''"""Tests for MCP server."""

   import pytest
   from pathlib import Path
   import json

   from server import MCPServer


   def test_server_initialization():
       """Test server initializes correctly."""
       server = MCPServer()
       assert server is not None
       assert server.workspace_dir is not None


   def test_skill_imports():
       """Test skills can be imported."""
       from adapters import code_analysis, test_orchestrator, learning_analytics
       assert code_analysis is not None


   def test_code_execution():
       """Test code execution with filtering."""
       server = MCPServer()

       code = """
from skills.code_analysis import analyze_file
from skills.common.filters import ResultFilter

result = analyze_file("test_file.py")
result = ResultFilter.limit([result], 1)
"""

       response = server.execute_code(code)
       assert response.success
   '''

   with open(server_dir / "tests" / "test_server.py", 'w') as f:
       f.write(test_server_code)
   ```

2. **Run tests**
   ```bash
   cd mcp/servers/my-mcp-server
   pytest tests/ -v
   ```

**Expected Output:**
- ✅ All tests pass
- 📊 Test coverage ≥ 80%
- 🧪 Integration tests pass
- ✅ Security tests pass

---

#### Phase 7: Documentation
**Goal:** Generate complete documentation

**Actions:**
1. **Generate README.md**
   ```python
   from skills.doc_generator import generate_readme

   readme = generate_readme(
       project_name="My MCP Server",
       description="MCP server exposing code analysis, test orchestration, and learning analytics skills",
       skills=skills_config,
       installation_steps=[...],
       usage_examples=[...],
       security_notes=[...]
   )

   with open(server_dir / "README.md", 'w') as f:
       f.write(readme)
   ```

2. **Generate usage examples**
   ```python
   examples_dir = server_dir / "examples"
   examples_dir.mkdir(exist_ok=True)

   # Generate example for each skill
   for skill_config in skills_config:
       example_code = generate_skill_example(skill_config)
       example_path = examples_dir / f"{skill_config['name']}_example.py"
       with open(example_path, 'w') as f:
           f.write(example_code)
   ```

**Expected Output:**
- ✅ README.md complete
- ✅ Usage examples generated
- ✅ API documentation created
- 📚 Ready for users

---

**Final Output:**
Complete, production-ready MCP server with:
- ✅ All schemas generated and validated
- ✅ All adapters created and tested
- ✅ Security score ≥ 90/100
- ✅ All tests passing (coverage ≥ 80%)
- ✅ Complete documentation
- 📦 Ready for deployment

---

## Testing Strategy

### Unit Tests

**Location:** `skills/mcp_schema_generator/tests/`, etc.

**Coverage:**
- Schema generation for all skill types
- Adapter creation with various configurations
- Security validation checks
- Error handling
- Edge cases

**Example Test:**
```python
# tests/skills/mcp_schema_generator/test_schema_generation.py

import pytest
from skills.mcp_schema_generator import generate_schema, validate_schema

def test_generate_schema_basic():
    """Test basic schema generation."""
    result = generate_schema("code_analysis")

    assert result.success
    assert "tool_name" in result.data
    assert "input_schema" in result.data
    assert result.data['tool_name'] == "code_analysis.analyze_codebase"

def test_generate_schema_with_operations():
    """Test schema generation for specific operations."""
    result = generate_schema(
        "code_analysis",
        operations=["analyze_file"]
    )

    assert result.success
    assert len(result.data['operations']) == 1

def test_schema_validation():
    """Test schema validation."""
    valid_schema = {
        "tool_name": "test.operation",
        "description": "Test operation",
        "input_schema": {
            "type": "object",
            "properties": {
                "param": {"type": "string"}
            },
            "required": ["param"]
        }
    }

    result = validate_schema(valid_schema)
    assert result.success
    assert result.data['valid'] is True

def test_schema_validation_invalid():
    """Test schema validation catches errors."""
    invalid_schema = {
        "tool_name": "test.operation",
        # Missing required fields
    }

    result = validate_schema(invalid_schema)
    assert result.success
    assert result.data['valid'] is False
    assert len(result.data['errors']) > 0
```

### Integration Tests

**Location:** `tests/integration/test_mcp_builder.py`

**Tests:**
- Complete MCP server creation workflow
- Multi-skill server generation
- Security validation integration
- End-to-end server execution

**Example Test:**
```python
# tests/integration/test_mcp_builder_workflow.py

import pytest
import tempfile
from pathlib import Path

def test_complete_mcp_server_creation():
    """Test complete MCP server creation workflow."""
    # Use mcp-server-architect to design
    # Use mcp-server-builder to implement
    # Validate result

    with tempfile.TemporaryDirectory() as tmpdir:
        server_dir = Path(tmpdir) / "test-mcp-server"

        # Run builder
        from agents.mcp_server_builder import build_mcp_server

        result = build_mcp_server(
            server_dir=server_dir,
            skills=["code_analysis", "test_orchestrator"],
            security_config={...}
        )

        # Validate structure
        assert (server_dir / "server.py").exists()
        assert (server_dir / "adapters" / "code_analysis.py").exists()
        assert (server_dir / "schema").exists()
        assert (server_dir / "tests").exists()
        assert (server_dir / "README.md").exists()

        # Validate security
        from skills.mcp_security_validator import validate_server_security
        security = validate_server_security(str(server_dir))
        assert security.success
        assert security.data['security_score'] >= 90

        # Run tests
        import subprocess
        test_result = subprocess.run(
            ["pytest", str(server_dir / "tests"), "-v"],
            capture_output=True
        )
        assert test_result.returncode == 0
```

### Security Tests

**Location:** `tests/security/test_mcp_security.py`

**Tests:**
- Filesystem isolation
- Network filtering
- Resource limits
- Code validation
- Input sanitization

---

## Documentation

### 1. Skills Documentation

Each skill needs complete SKILL.md:

**Example:** `skills/mcp_schema_generator/SKILL.md`
```markdown
---
name: mcp-schema-generator
description: Generate MCP tool schemas from skill operations following Anthropic best practices
version: 1.0.0
category: mcp
tags:
  - mcp
  - schema
  - code-generation
activation: manual
tools:
  - Read
  - Glob
dependencies: []
---

# MCP Schema Generator Skill

## When to Use This Skill

Use mcp-schema-generator when you need to:
- **Generate MCP schemas** - Create tool schemas from skill operations
- **Validate schemas** - Check schema structure and completeness
- **Batch generation** - Generate schemas for multiple skills
- **Update schemas** - Regenerate schemas when skills change

**Not for:** Manual schema writing, non-MCP tools

## Quick Start

```python
from skills.mcp_schema_generator import generate_schema
from skills.common.filters import ResultFilter

# Generate schema for a skill
result = generate_schema("code_analysis", response_format="complete")

if result.success:
    schema = result.data
    print(f"Generated schema for: {schema['tool_name']}")
    print(f"Parameters: {list(schema['input_schema']['properties'].keys())}")
```

[... rest of SKILL.md ...]
```

### 2. Agents Documentation

Each agent needs complete .md file:

**Example:** `agents/mcp-server-architect.md`
```markdown
---
name: mcp-server-architect
description: Design MCP server architecture following Anthropic best practices
tools:
  - Read
  - Write
  - Glob
  - think
model: sonnet
activation: manual
---

# MCP Server Architect Agent

## Your Mission

You are the MCP Server Architect. Your job is to analyze requirements and design complete MCP server architecture following Anthropic's best practices for token efficiency, security, and progressive disclosure.

[... rest of agent definition ...]
```

### 3. Usage Guide

**Location:** `docs/MCP_BUILDER_GUIDE.md`

**Contents:**
- Getting started
- Creating your first MCP server
- Best practices
- Security considerations
- Troubleshooting
- Examples

---

## Implementation Timeline

### Week 1: Skills Implementation
**Days 1-2: mcp_schema_generator**
- [ ] Create skill structure
- [ ] Implement generate_schema()
- [ ] Implement validate_schema()
- [ ] Implement generate_batch_schemas()
- [ ] Write unit tests
- [ ] Create SKILL.md

**Days 3-4: mcp_adapter_creator**
- [ ] Create skill structure
- [ ] Implement create_adapter()
- [ ] Implement create_batch_adapters()
- [ ] Create adapter templates
- [ ] Write unit tests
- [ ] Create SKILL.md

**Days 5-7: mcp_security_validator**
- [ ] Create skill structure
- [ ] Implement validate_server_security()
- [ ] Implement validate_sandbox_config()
- [ ] Create security checklist
- [ ] Write unit tests
- [ ] Create SKILL.md

### Week 2: Agents Implementation
**Days 1-3: mcp-server-architect**
- [ ] Create agent definition
- [ ] Implement Phase 1: Requirements Analysis
- [ ] Implement Phase 2: Architecture Design
- [ ] Implement Phase 3: Implementation Planning
- [ ] Integrate Think tool
- [ ] Test with various scenarios

**Days 4-7: mcp-server-builder**
- [ ] Create orchestrator definition
- [ ] Implement Phase 1: Setup & Validation
- [ ] Implement Phase 2: Schema Generation
- [ ] Implement Phase 3: Adapter Creation
- [ ] Implement Phase 4: Server Implementation
- [ ] Implement Phase 5: Security Validation
- [ ] Implement Phase 6: Testing
- [ ] Implement Phase 7: Documentation
- [ ] Integration testing

### Week 3: Testing & Documentation
**Days 1-2: Testing**
- [ ] Write integration tests
- [ ] Write security tests
- [ ] Run comprehensive test suite
- [ ] Fix any issues
- [ ] Achieve 80%+ coverage

**Days 3-5: Documentation**
- [ ] Write MCP_BUILDER_GUIDE.md
- [ ] Create usage examples
- [ ] Update CLAUDE.md
- [ ] Update README.md
- [ ] Create video tutorials (optional)

**Days 6-7: Polish**
- [ ] Code review
- [ ] Performance optimization
- [ ] User testing
- [ ] Final fixes

### Week 4: Deployment & Validation
**Days 1-2: Deployment**
- [ ] Commit all changes
- [ ] Create pull request
- [ ] Deploy to staging
- [ ] Run smoke tests

**Days 3-5: Validation**
- [ ] Create 3 real MCP servers using the system
- [ ] Validate security scores
- [ ] Measure token efficiency gains
- [ ] Collect user feedback

**Days 6-7: Iteration**
- [ ] Address feedback
- [ ] Fix any issues
- [ ] Final documentation updates
- [ ] Deploy to production

---

## Success Criteria

### Functional Requirements
- ✅ Generate valid MCP schemas for any skill
- ✅ Create complete, working MCP adapters
- ✅ Validate security configuration (score ≥ 90)
- ✅ Build complete MCP server in < 10 minutes
- ✅ 100% test pass rate
- ✅ 80%+ test coverage

### Quality Requirements
- ✅ Code follows Python best practices
- ✅ Complete documentation for all components
- ✅ Agent-friendly error messages
- ✅ Progressive disclosure pattern
- ✅ Token efficiency (response_format support)

### Security Requirements
- ✅ Filesystem isolation enforced
- ✅ Network filtering configured
- ✅ Resource limits set
- ✅ Code validation enabled
- ✅ Security audit passes

### Performance Requirements
- ✅ Schema generation < 5s per skill
- ✅ Adapter creation < 10s per skill
- ✅ Security validation < 30s
- ✅ Complete server build < 10 minutes
- ✅ Token usage reduction ≥ 95% for filtered operations

---

## Next Steps

1. **Review this plan** with team
2. **Approve timeline** and resource allocation
3. **Create Git branch** for implementation
4. **Start Week 1: Skills Implementation**
5. **Daily standups** to track progress
6. **Weekly demos** to show progress

---

**Status:** ✅ Ready for Implementation
**Expected Timeline:** 4 weeks
**Expected Impact:**
- 80% faster MCP server creation
- 100% security compliance
- 95%+ token efficiency for all operations

**Created:** 2025-11-11
**Author:** Claude Code Learning System
**Version:** 1.0.0

# Skills Integration Architecture

**Version:** 1.0
**Date:** 2025-10-25
**Status:** Design Complete

---

## Overview

This document defines how agents interact with skills to perform specialized tasks. Skills are invoked through a standardized protocol that ensures consistent behavior and easy extensibility.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         AGENT LAYER                          │
│  (learning-coordinator, plan-generation-mentor, etc.)        │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    SKILL INTEGRATION LAYER                   │
│  ┌───────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Skill Registry│  │ Skill Loader │  │ Skill Invoker   │  │
│  └───────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        SKILLS LAYER                          │
│  ┌──────────────┐  ┌─────────────────┐  ┌───────────────┐  │
│  │code-analysis │  │test-orchestrator│  │session-state  │  │
│  └──────────────┘  └─────────────────┘  └───────────────┘  │
│  ┌──────────────┐  ┌─────────────────┐                      │
│  │learning-plan │  │learning-analytics│  ...more skills     │
│  │-manager      │  │                 │                      │
│  └──────────────┘  └─────────────────┘                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. Skill Registry

**Purpose:** Discover and catalog all available skills

**Responsibilities:**
- Scan skills directory
- Parse skill.md definitions
- Maintain skill metadata
- Validate skill compatibility
- Handle skill dependencies

**API:**
```python
class SkillRegistry:
    def discover_skills(self, skills_dir: str) -> List[SkillMetadata]
    def get_skill(self, skill_name: str) -> Optional[SkillMetadata]
    def list_skills(self, category: Optional[str] = None) -> List[str]
    def validate_skill(self, skill_name: str) -> ValidationResult
```

### 2. Skill Loader

**Purpose:** Load and initialize skills on demand

**Responsibilities:**
- Dynamic skill loading
- Dependency injection
- Configuration management
- Error handling
- Caching

**API:**
```python
class SkillLoader:
    def load_skill(self, skill_name: str) -> SkillInstance
    def reload_skill(self, skill_name: str) -> SkillInstance
    def unload_skill(self, skill_name: str) -> None
    def get_loaded_skills(self) -> List[str]
```

### 3. Skill Invoker

**Purpose:** Execute skill operations with standardized protocol

**Responsibilities:**
- Request/response handling
- Parameter validation
- Error handling
- Timeout management
- Result formatting

**API:**
```python
class SkillInvoker:
    def invoke(self, skill_name: str, operation: str, params: Dict) -> SkillResult
    async def invoke_async(self, skill_name: str, operation: str, params: Dict) -> SkillResult
    def invoke_batch(self, requests: List[SkillRequest]) -> List[SkillResult]
```

---

## Skill Definition Format

### skill.md Structure

```yaml
---
name: skill-name
description: Brief description of what the skill does
version: 1.0.0
author: optional
tools:
  - Read
  - Glob
  - Grep
  - Bash
activation: manual  # or automatic
dependencies:
  - other-skill-name  # optional
category: testing  # optional
tags:
  - python
  - testing
---

# Skill Documentation

Detailed description of the skill...

## Operations

### operation_name

Description of operation

**Input:**
```json
{
  "param1": "value",
  "param2": 123
}
```

**Output:**
```json
{
  "result": "value"
}
```
```

---

## Request/Response Protocol

### Request Format

```python
@dataclass
class SkillRequest:
    """Request to invoke a skill."""
    skill_name: str
    operation: str
    parameters: Dict[str, Any]
    context: Optional[Dict[str, Any]] = None
    timeout: int = 60
    request_id: Optional[str] = None
```

**Example:**
```python
request = SkillRequest(
    skill_name="test-orchestrator",
    operation="generate_tests",
    parameters={
        "source_file": "src/services/payment.py",
        "target_coverage": 80.0
    },
    context={
        "project_type": "python",
        "framework": "pytest"
    }
)
```

### Response Format

```python
@dataclass
class SkillResult:
    """Result from skill invocation."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    duration: float = 0.0
    metadata: Optional[Dict[str, Any]] = None
```

**Success Example:**
```python
result = SkillResult(
    success=True,
    data={
        "tests_generated": 17,
        "completeness_score": 0.768,
        "test_file": "test_payment.py",
        "quality_score": 84.4
    },
    duration=2.3,
    metadata={
        "skill_version": "0.2.0",
        "generator": "EnhancedTestGenerator"
    }
)
```

**Error Example:**
```python
result = SkillResult(
    success=False,
    error="Source file not found: payment.py",
    error_code="FILE_NOT_FOUND",
    duration=0.1
)
```

---

## Agent Integration Patterns

### Pattern 1: Direct Invocation

```python
from skills.integration import SkillInvoker

# Agent code
invoker = SkillInvoker()

result = invoker.invoke(
    skill_name="test-orchestrator",
    operation="generate_tests",
    params={"source_file": "payment.py"}
)

if result.success:
    print(f"Generated {result.data['tests_generated']} tests")
else:
    print(f"Error: {result.error}")
```

### Pattern 2: Async Invocation

```python
# For long-running operations
result = await invoker.invoke_async(
    skill_name="code-analysis",
    operation="analyze_codebase",
    params={"path": "src/"}
)
```

### Pattern 3: Batch Invocation

```python
# Invoke multiple skills in parallel
requests = [
    SkillRequest("test-orchestrator", "generate_tests", {"file": "payment.py"}),
    SkillRequest("code-analysis", "analyze_file", {"file": "payment.py"}),
    SkillRequest("session-state", "get_student", {"student_id": "alex_2025"})
]

results = invoker.invoke_batch(requests)
```

### Pattern 4: Skill Chaining

```python
# spec-to-implementation orchestrates multiple skills
class SpecToImplementation:
    def implement_feature(self, requirement: str):
        # Step 1: Analyze codebase
        analysis = invoker.invoke(
            "code-analysis",
            "analyze_codebase",
            {"path": "src/"}
        )

        # Step 2: Generate specification
        spec = self.generate_spec(requirement, analysis.data)

        # Step 3: Generate code
        code = self.generate_code(spec)

        # Step 4: Generate tests
        tests = invoker.invoke(
            "test-orchestrator",
            "generate_tests",
            {"source_code": code}
        )

        # Step 5: Create PR
        pr = invoker.invoke(
            "pr-review-assistant",
            "create_pr",
            {"changes": code, "tests": tests.data}
        )

        return pr.data
```

---

## Error Handling

### Error Codes

```python
class SkillError:
    # Client errors (4xx)
    SKILL_NOT_FOUND = "SKILL_NOT_FOUND"
    INVALID_OPERATION = "INVALID_OPERATION"
    INVALID_PARAMETERS = "INVALID_PARAMETERS"
    VALIDATION_ERROR = "VALIDATION_ERROR"

    # Server errors (5xx)
    SKILL_ERROR = "SKILL_ERROR"
    TIMEOUT = "TIMEOUT"
    DEPENDENCY_ERROR = "DEPENDENCY_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"
```

### Error Handling Pattern

```python
result = invoker.invoke("test-orchestrator", "generate_tests", params)

if not result.success:
    if result.error_code == SkillError.SKILL_NOT_FOUND:
        # Skill not installed
        print("Please install test-orchestrator skill")
    elif result.error_code == SkillError.TIMEOUT:
        # Operation took too long
        print("Test generation timed out, try with smaller file")
    elif result.error_code == SkillError.VALIDATION_ERROR:
        # Invalid parameters
        print(f"Invalid parameters: {result.error}")
    else:
        # Generic error
        print(f"Skill error: {result.error}")
```

---

## Configuration

### Skill Configuration File

**`skills/config.yaml`**
```yaml
registry:
  skills_directory: "skills/"
  auto_discover: true
  cache_enabled: true

loader:
  lazy_loading: true
  max_concurrent: 5
  reload_on_change: false

invoker:
  default_timeout: 60
  max_retries: 3
  enable_metrics: true

skills:
  test-orchestrator:
    enabled: true
    config:
      target_coverage: 80.0
      framework: "pytest"

  code-analysis:
    enabled: true
    config:
      languages: ["python", "javascript"]
```

---

## Skill Discovery

### Automatic Discovery

```python
# At startup
registry = SkillRegistry()
skills = registry.discover_skills("skills/")

print(f"Discovered {len(skills)} skills:")
for skill in skills:
    print(f"  - {skill.name}: {skill.description}")
```

**Output:**
```
Discovered 6 skills:
  - test-orchestrator: Intelligent test generation and coverage analysis
  - code-analysis: Deep static code analysis and pattern detection
  - session-state: Student profile and learning history management
  - learning-analytics: Learning velocity and struggle detection
  - learning-plan-manager: Learning plan creation and tracking
  - interactive-diagram: Mermaid diagram generation
```

---

## Metrics and Monitoring

### Skill Metrics

```python
@dataclass
class SkillMetrics:
    """Metrics for skill usage."""
    skill_name: str
    total_invocations: int
    successful_invocations: int
    failed_invocations: int
    avg_duration: float
    max_duration: float
    min_duration: float
    error_rate: float
```

### Monitoring

```python
# Get metrics
metrics = invoker.get_metrics("test-orchestrator")

print(f"Test Orchestrator Metrics:")
print(f"  Invocations: {metrics.total_invocations}")
print(f"  Success rate: {(1 - metrics.error_rate) * 100:.1f}%")
print(f"  Avg duration: {metrics.avg_duration:.2f}s")
```

---

## Security Considerations

### Sandboxing

- Skills run in isolated environments
- Limited file system access
- No network access by default (unless specified in tools)
- Resource limits (CPU, memory, time)

### Input Validation

- All parameters validated against schema
- Type checking enforced
- Size limits on inputs
- Path traversal prevention

### Output Sanitization

- No sensitive data in responses
- Error messages don't leak system info
- Results are structured and typed

---

## Testing Integration

### Unit Testing Skills

```python
import unittest
from skills.integration import SkillInvoker

class TestSkillIntegration(unittest.TestCase):
    def setUp(self):
        self.invoker = SkillInvoker()

    def test_test_orchestrator_generates_tests(self):
        result = self.invoker.invoke(
            "test-orchestrator",
            "generate_tests",
            {"source_file": "examples/sample_payment.py"}
        )

        self.assertTrue(result.success)
        self.assertIn("tests_generated", result.data)
        self.assertGreater(result.data["tests_generated"], 0)
```

---

## Migration Path

### For Existing Skills

1. **Add skill.md** if not present
2. **Standardize operations** to follow protocol
3. **Return SkillResult** format
4. **Add error handling**
5. **Register with registry**

### For New Skills

1. **Use skill template** (provided)
2. **Follow naming conventions**
3. **Document all operations**
4. **Include examples**
5. **Add tests**

---

## Best Practices

### Skill Design

✅ **DO:**
- Keep skills focused (single responsibility)
- Provide clear, structured output
- Handle errors gracefully
- Document all operations
- Include usage examples
- Support async operations for long tasks

❌ **DON'T:**
- Make skills too generic
- Return unstructured data
- Raise exceptions without context
- Assume file paths
- Block indefinitely

### Agent Integration

✅ **DO:**
- Check result.success before using data
- Handle timeouts appropriately
- Log skill invocations
- Use batch operations when possible
- Cache results when appropriate

❌ **DON'T:**
- Ignore errors
- Make assumptions about skill availability
- Hardcode skill parameters
- Invoke skills unnecessarily

---

## Example: Complete Integration

See `skills/integration/examples/agent_skill_demo.py` for complete working example.

---

**Version:** 1.0
**Status:** ✅ Ready for Implementation
**Next Steps:**
1. Implement SkillRegistry
2. Implement SkillLoader
3. Implement SkillInvoker
4. Create example integrations
5. Add monitoring and metrics

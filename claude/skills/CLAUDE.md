# Skills Directory Guide

This directory contains reusable skill modules that provide specialized capabilities through standardized interfaces.

---

## 📋 What Are Skills?

Skills are Python modules that provide:
- **Reusable functionality** - Common operations packaged for easy reuse
- **Standardized interfaces** - Consistent patterns across all skills
- **Agent-friendly design** - Optimized for AI agent invocation
- **Progressive disclosure** - Summary first, details on demand
- **Token efficiency** - Configurable response formats to save context

---

## 🔍 Using Metadata for Navigation

**Skills have YAML frontmatter** in their SKILL.md files:
```yaml
---
name: test-orchestrator
category: testing
tools: [Read, Write, Bash]
dependencies: []
---
```

**Quick skill discovery:**
```bash
# Find skills by category
grep "category: testing" skills/*/SKILL.md

# Find skills using specific tools
grep "tools:.*Bash" skills/*/SKILL.md

# Find skills with no dependencies
grep "dependencies: \[\]" skills/*/SKILL.md
```

**Progressive disclosure pattern:**
1. Load SKILL.md first (~200-500 tokens) - Quick overview
2. Load reference.md on demand - Complete API
3. Load examples.md as needed - Usage patterns

---

## 📁 Directory Structure

Each skill follows this structure:

```
skills/skill_name/
├── SKILL.md              # Progressive disclosure entry point (load first)
├── reference.md          # Detailed documentation (load on demand)
├── examples.md           # Usage examples (load on demand)
├── __init__.py          # Public API exports
├── operations.py        # Agent-friendly interface (NEW!)
├── core/                # Implementation modules
│   ├── *.py            # Core logic
└── tests/              # Unit tests
    └── test_*.py
```

### Key Files

**SKILL.md** (Progressive Disclosure)
- Name and description (always loaded)
- When to use this skill
- Quick start guide
- Operation list (brief)
- Link to reference.md for details

**operations.py** (Agent-Friendly Interface)
- High-level functions for agent invocation
- `response_format` parameter (summary/concise/detailed)
- Agent-friendly error messages
- Token efficiency guidance
- Returns `OperationResult` with success status

**reference.md** (Detailed Documentation)
- Complete operation specifications
- Parameter descriptions
- Return value details
- Error handling
- Advanced usage

**examples.md** (Usage Examples)
- Real-world scenarios
- Code examples
- Common patterns
- Integration examples

---

## 🎯 Available Skills

### Analysis & Quality
- **code_analysis** - AST parsing, complexity metrics, dependency graphs
- **code_search** - Find definitions, usages, patterns in codebase
- **test_orchestrator** - Test generation, execution, coverage analysis
- **pr_review_assistant** - Automated pull request review
- **spec_to_implementation** - Transform specs into code

### Learning & Teaching
- **learning_plan_manager** - Parse and manage learning plans
- **learning_analytics** - Velocity tracking, struggle detection
- **session_state** - Student profiles and progress tracking
- **interactive_diagram** - Generate Mermaid diagrams

### Development Tools
- **git_workflow_assistant** - Git operations, branch management
- **doc_generator** - Documentation generation
- **refactor_assistant** - Code refactoring guidance
- **dependency_guardian** - Dependency security scanning
- **skill_evaluator** - Skill effectiveness evaluation

### Infrastructure
- **execution** - Safe code execution
- **common** - Shared utilities (filters, types, etc.)
- **integration** - Skill composition and coordination

---

## 🚀 Using Skills

### Pattern 1: Direct Import (Recommended)

```python
# Import the agent-friendly interface
from skills.test_orchestrator.operations import generate_tests

# Use with response_format for token efficiency
result = generate_tests(
    source_file="src/payment.py",
    response_format="concise"  # Default: summary only
)

if result.success:
    print(f"Generated {result.data['tests_generated']} tests")
    print(f"Test file: {result.data['test_file']}")
else:
    print(f"Error: {result.error}")
    print(f"Suggestions: {result.suggestions}")
```

### Pattern 2: Progressive Disclosure

```python
# Step 1: Start with summary
from skills.code_analysis.operations import analyze_codebase

result = analyze_codebase(
    path="src/",
    response_format="summary"  # Just overview
)
# Returns: ~500 tokens (file counts, complexity overview)

# Step 2: Filter locally (zero tokens!)
from skills.common.filters import ResultFilter

# Get detailed data only when needed
result = analyze_codebase(
    path="src/",
    response_format="filtered"  # Optimized for filtering
)
# Returns: ~2000 tokens (all data, structured)

# Filter locally (runs in your code, no agent tokens!)
nav_files = ResultFilter.search(
    result.data["files"],
    "navigation",
    ["path", "name"]
)
top_5 = ResultFilter.top_n_by_field(nav_files, "complexity", 5)
# Agent receives only 5 files (~500 tokens)
# Savings: 49,500 tokens (99%)!
```

### Pattern 3: Error Recovery

```python
from skills.test_orchestrator.operations import generate_tests

result = generate_tests("nonexistent.py")

if not result.success:
    # Agent-friendly error with guidance
    print(f"Error: {result.error}")
    # "Cannot find source file: nonexistent.py"

    print("Suggestions:")
    for suggestion in result.suggestions:
        print(f"  - {suggestion}")
    # - Check if the file path is correct
    # - Use Glob('**/*.py') to find Python files
    # - Verify the file exists with Bash('ls -la src/')

    if result.example_fix:
        print(f"Example: {result.example_fix}")
        # generate_tests('src/services/payment.py')
```

---

## 💡 Token Efficiency Patterns

### Use response_format Parameter

All modernized skills support `response_format`:

```python
# ❌ Inefficient - always returns everything
result = analyze_codebase("src/")  # 50,000 tokens

# ✅ Efficient - returns summary first
result = analyze_codebase("src/", response_format="summary")  # 500 tokens
# Then get details only for specific files

# ✅ Most efficient - filter locally
result = analyze_codebase("src/", response_format="filtered")  # 2,000 tokens
filtered = ResultFilter.search(result.data["files"], "auth")  # 0 tokens (local)
# Agent sees only filtered results
```

### Common Response Formats

| Format | Purpose | Token Usage | When to Use |
|--------|---------|-------------|-------------|
| `summary` | Overview only | 200-1000 | Quick check, planning |
| `concise` | Key data, no details | 500-2000 | Most common case |
| `filtered` | For local filtering | 2000-5000 | Large datasets |
| `detailed` | Everything | 5000+ | Rare, specific needs |

### ResultFilter for Local Filtering

```python
from skills.common.filters import ResultFilter

# After getting data with response_format="filtered"
files = result.data["files"]

# All these run locally (0 tokens to agent!)
limited = ResultFilter.limit(files, 10)
searched = ResultFilter.search(files, "navigation", ["path"])
top_n = ResultFilter.top_n_by_field(files, "complexity", 5)
filtered = ResultFilter.filter_by_field(files, "language", "python")
summary = ResultFilter.summarize(files)  # Condensed summary
```

**Token Savings:**
- Before: 50,000 tokens (all files)
- After: 500 tokens (5 filtered files)
- **Savings: 99%**

---

## 🔐 Security & Safety

### Safe Skill Usage

Before using a new skill, check:

1. **SKILL.md `tools` list** - What access does it need?
   ```yaml
   tools:
     - Read    # File reading
     - Write   # File creation
     - Bash    # Command execution
   ```

2. **Dependencies** - Does it call external services?
3. **Source code** - Review if using Bash or network access

### Red Flags

⚠️ Audit carefully if skill:
- Uses `Bash` without clear need
- Accesses network (WebFetch)
- Requests sensitive data access
- Has obfuscated code
- Lacks clear documentation
- No SKILL.md or operations.py

### Safe Patterns

✅ Good skills have:
- Minimal tool usage
- Clear documentation in SKILL.md
- No network access (unless clearly needed)
- Sandboxed execution
- Well-defined operations
- Agent-friendly error messages
- Token efficiency features

---

## 📊 Skill Development Status

### ✅ Modernized (Week 1)
- **test_orchestrator** - response_format, better errors
- **code_analysis** - operations.py, 3 formats
- **learning_plan_manager** - operations.py, 3 formats

### 🔄 In Progress (Week 2)
- **test_orchestrator** - Add SKILL.md, reference.md, examples.md
- **code_analysis** - Add SKILL.md, reference.md, examples.md

### 📅 Planned
- All remaining 21 skills

---

## 🛠️ Creating New Skills

### Minimal Skill Structure

```
skills/my_skill/
├── SKILL.md           # Required: Progressive disclosure
├── __init__.py        # Required: Public API
└── operations.py      # Recommended: Agent-friendly interface
```

### SKILL.md Template

```yaml
---
name: my-skill
description: Brief description (one sentence)
version: 1.0.0
category: analysis|learning|development|infrastructure
tags:
  - relevant
  - tags
activation: manual
tools:
  - Read
  - Write
---

# My Skill

## When to Use This Skill

Use my-skill when you need to:
- Specific use case 1
- Specific use case 2

## Quick Start

See reference.md for detailed docs.
See examples.md for usage examples.

## Operations

- `operation_name` - Brief description

See reference.md for details.
```

### operations.py Template

```python
"""Agent-friendly interface for my_skill."""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class OperationResult:
    """Standardized result format."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    suggestions: Optional[List[str]] = None
    example_fix: Optional[str] = None


def my_operation(
    param: str,
    response_format: str = "concise"
) -> OperationResult:
    """
    Do something useful.

    Args:
        param: Description
        response_format: "summary" | "concise" | "detailed"
            - "summary": Overview only (< 500 tokens)
            - "concise": Key data without details (< 2000 tokens)
            - "detailed": Full results (5000+ tokens)

    Returns:
        OperationResult with success status and data/error
    """
    try:
        # Implementation
        result = _do_work(param)

        # Format based on response_format
        if response_format == "summary":
            return OperationResult(
                success=True,
                data={
                    "count": len(result),
                    "summary": "Brief overview"
                }
            )
        elif response_format == "concise":
            return OperationResult(
                success=True,
                data={
                    "items": [item["name"] for item in result],
                    "count": len(result)
                }
            )
        else:  # detailed
            return OperationResult(
                success=True,
                data={"items": result}
            )

    except FileNotFoundError as e:
        return OperationResult(
            success=False,
            error=f"Cannot find file: {param}",
            error_code="FILE_NOT_FOUND",
            suggestions=[
                "Check if the file path is correct",
                "Use Glob('**/*') to find files",
            ],
            example_fix="my_operation('correct/path.py')"
        )
```

---

## 📚 Integration Patterns

### Skill Composition

```python
# Combine skills for complex workflows
from skills.code_analysis.operations import analyze_file
from skills.test_orchestrator.operations import generate_tests

# 1. Analyze source file
analysis = analyze_file("payment.py", response_format="summary")

# 2. Generate tests based on analysis
if analysis.success:
    tests = generate_tests(
        "payment.py",
        target_coverage=analysis.data["complexity"] > 10 ? 90 : 80
    )
```

### Use with Agents

Skills are designed for agent invocation:

```python
# Agents can discover skills via SKILL.md
# Then invoke via operations.py

# Agent reads: skills/test_orchestrator/SKILL.md
# Learns: "Use when you need to generate tests"

# Agent imports and calls:
from skills.test_orchestrator.operations import generate_tests

result = generate_tests("payment.py")  # Defaults to concise

# Agent understands errors:
if not result.success:
    # Sees: suggestions, example_fix
    # Can retry with corrected parameters
```

---

## 🧪 Testing Skills

### Run Skill Tests

```bash
# Test specific skill
pytest skills/test_orchestrator/tests/ -v

# Test all skills
pytest skills/*/tests/ -v

# Test with coverage
pytest skills/test_orchestrator/tests/ --cov=skills.test_orchestrator
```

### Test Your Code Using Skills

```bash
# Use test_orchestrator to test your code
python -c "
from skills.test_orchestrator.operations import generate_tests
result = generate_tests('myfile.py')
print(result.data['test_file'])
"

# Then run the generated tests
pytest path/to/generated/test_file.py
```

---

## 📖 Related Documentation

- `../CLAUDE.md` - Project navigation guide
- `../docs/SANDBOXING_GUIDE.md` - Security configuration
- `INTEGRATION_ARCHITECTURE.md` - Skill composition patterns
- `../docs/ANTHROPIC_BEST_PRACTICES_IMPLEMENTATION_PLAN.md` - Improvement roadmap

---

## 🎯 Quick Reference

### Find the Right Skill

**Code Analysis:**
- Structure & complexity → `code_analysis`
- Find definitions → `code_search`
- Refactoring → `refactor_assistant`

**Testing:**
- Generate tests → `test_orchestrator`
- Review code → `pr_review_assistant`

**Learning:**
- Manage plans → `learning_plan_manager`
- Track progress → `learning_analytics`
- Track sessions → `session_state`

**Development:**
- Git operations → `git_workflow_assistant`
- Documentation → `doc_generator`
- Dependencies → `dependency_guardian`

**Visualization:**
- Diagrams → `interactive_diagram`
- Data viz → `data_visualization`

### Response Format Quick Guide

```python
# Planning / Quick check
response_format="summary"      # 200-1000 tokens

# Normal usage
response_format="concise"      # 500-2000 tokens (default)

# Large datasets with filtering
response_format="filtered"     # 2000-5000 tokens
# + ResultFilter.search/top_n

# Rare: need everything
response_format="detailed"     # 5000+ tokens
```

### Error Handling

```python
result = skill_operation(...)

if not result.success:
    print(result.error)          # Human-readable error
    print(result.error_code)     # Machine-readable code
    print(result.suggestions)    # How to fix
    print(result.example_fix)    # Corrected example
```

---

## 🚀 Getting Started

### New to Skills?

1. **Read a SKILL.md file** (e.g., `test_orchestrator/SKILL.md`)
2. **Try an example** from `examples.md`
3. **Check operations.py** for available functions
4. **Use response_format** to control output size

### Building a Workflow?

1. **Check available skills** (list above)
2. **Read SKILL.md files** to understand capabilities
3. **Start with summary format** to explore
4. **Combine skills** for complex tasks
5. **Filter locally** for efficiency

### Contributing?

1. **Follow the structure** (SKILL.md, operations.py, etc.)
2. **Add response_format** parameter
3. **Use agent-friendly errors** (suggestions, examples)
4. **Write tests** in tests/ directory
5. **Document in reference.md** and examples.md

---

**Remember:** Skills are building blocks for intelligent workflows. Use progressive disclosure and local filtering for maximum efficiency! 🚀

*Last Updated: 2025-11-07*

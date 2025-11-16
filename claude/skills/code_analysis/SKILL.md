---
name: code-analysis
description: Deep static code analysis providing AST parsing, complexity metrics, dependency graphs, and pattern detection. Goes far beyond basic grep/find.
version: 1.0.0
category: analysis
tags:
  - python
  - ast
  - complexity
  - dependencies
  - patterns
  - architecture
activation: manual
tools:
  - Read
  - Glob
dependencies: []
---

# Code Analysis Skill

## When to Use This Skill

Use code-analysis when you need to:
- **Analyze codebase structure** - Understand architecture, entry points, and organization
- **Measure complexity** - Calculate cyclomatic complexity and identify complex functions
- **Map dependencies** - Find imports, usage patterns, and integration points
- **Detect patterns** - Identify design patterns (Singleton, Factory, Observer, etc.)
- **Find integration points** - Locate APIs, database access, external services
- **Understand relationships** - See how files, classes, and functions connect

**Not for:** Simple file/text search (use Grep for that)

## Quick Start

```python
from skills.code_analysis.operations import analyze_codebase, analyze_file
from skills.common.filters import ResultFilter

# 1. Analyze entire codebase (summary format for efficiency)
result = analyze_codebase("src/")
print(f"Found {result.data['total_files']} files")
print(f"Entry points: {result.data['entry_points']}")

# 2. Filter locally for efficiency (95-99% token savings!)
result = analyze_codebase("src/", response_format="filtered")
nav_files = ResultFilter.search(result.data["files"], "navigation", ["path"])
complex = ResultFilter.top_n_by_field(nav_files, "complexity", 5)

# 3. Analyze specific file
details = analyze_file("src/auth.py", response_format="detailed")
print(f"Classes: {[c['name'] for c in details.data['classes']]}")
```

For detailed documentation, see **reference.md**.
For usage examples, see **examples.md**.

## Operations

### analyze_codebase(root_path, response_format="summary")
Analyze entire codebase for structure, patterns, and integration points.

**Returns:** File counts, entry points, pattern summary (summary) or full file details (detailed/filtered)

### analyze_file(file_path, response_format="summary")
Analyze single Python file for entities, complexity, and dependencies.

**Returns:** Entity counts and names (summary) or full details with AST info (detailed)

See **reference.md** for complete parameter specifications and response formats.

## Token Efficiency

This skill provides **extreme token savings** for large codebases:

| Operation | Format | Token Usage | Use When |
|-----------|--------|-------------|----------|
| analyze_codebase | summary | 500-1000 | Quick overview |
| analyze_codebase | filtered | 2000-10000 | Large codebase + filtering |
| analyze_codebase | detailed | 50000+ | Small codebase only |
| analyze_file | summary | 200-500 | Quick file check |
| analyze_file | detailed | 2000-5000 | Deep file analysis |

**Critical:** For codebases with >100 files, ALWAYS use summary or filtered format!

## Example Workflow: The 99% Token Reduction Pattern

```python
from skills.code_analysis.operations import analyze_codebase
from skills.common.filters import ResultFilter

# ❌ INEFFICIENT: Returns all 1000 files (50,000 tokens)
result = analyze_codebase("large_project/", response_format="detailed")
# Agent receives 50,000 tokens of file data

# ✅ EFFICIENT: Filter locally (99% reduction!)
result = analyze_codebase("large_project/", response_format="filtered")
# Returns: 2000 tokens (all files, structured for filtering)

# Filter IN YOUR CODE (not in agent context!)
auth_files = ResultFilter.search(result.data["files"], "auth", ["path", "name"])
# Returns: ~10 files

top_complex = ResultFilter.top_n_by_field(auth_files, "complexity", 3)
# Returns: ~3 files

# Agent receives only 3 files (~150 tokens)
# Savings: 49,850 tokens (99.7%)!
```

## Pattern Detection

Automatically detects design patterns:

- **Singleton Pattern** - Single instance classes
- **Factory Pattern** - Object creation patterns
- **Observer Pattern** - Event/listener systems
- **Decorator Pattern** - Function/class wrapping
- **Strategy Pattern** - Algorithm encapsulation
- **Repository Pattern** - Data access abstraction

```python
result = analyze_codebase("src/")
print(result.data['patterns_summary'])
# {
#   "singleton": 3,
#   "factory": 5,
#   "observer": 2,
#   ...
# }
```

## Integration Point Detection

Finds external connections:

- **API Endpoints** - REST, GraphQL, RPC
- **Database Access** - SQL, ORM, NoSQL
- **Message Queues** - RabbitMQ, Kafka, Redis
- **File I/O** - File operations
- **Network Calls** - HTTP, WebSocket
- **External Services** - Third-party APIs

```python
result = analyze_codebase("src/", response_format="summary")
print(f"Found {result.data['integration_points_count']} integration points")
```

## Error Handling

All operations return `OperationResult` with agent-friendly errors:

```python
result = analyze_codebase("nonexistent/")

if not result.success:
    print(result.error)       # "Directory not found: nonexistent/"
    print(result.error_code)  # "DIR_NOT_FOUND"

    # Actionable suggestions
    for suggestion in result.suggestions:
        print(f"  - {suggestion}")
    # - Check if the path is correct
    # - Use Glob('**/') to find directories
    # - Verify directory exists with Bash('ls -la')

    # Example fix
    print(result.example_fix)
    # analyze_codebase('src/')
```

## Integration

**With Architecture Review:**
```python
# Understand system structure
analysis = analyze_codebase("src/", response_format="summary")
print(f"Entry points: {analysis.data['entry_points']}")
print(f"Patterns: {analysis.data['patterns_summary']}")
```

**With Refactoring:**
```python
# Find high-complexity files
result = analyze_codebase("src/", response_format="filtered")
complex_files = ResultFilter.top_n_by_field(
    result.data["files"],
    "avg_complexity",
    10
)
# Focus refactoring on these 10 files
```

**With Test Generation:**
```python
# Find untested complex code
analysis = analyze_file("payment.py", response_format="detailed")
complex_functions = [
    func for func in analysis.data['functions']
    if func['complexity'] > 10
]
# Generate tests for complex functions first
```

## Comparison with Basic Tools

| Task | Grep/Find | code-analysis |
|------|-----------|---------------|
| Find files | ✓ | ✓ |
| Search text | ✓ | ✗ (use Grep) |
| Complexity metrics | ✗ | ✓ |
| Dependency graph | ✗ | ✓ |
| Pattern detection | ✗ | ✓ |
| AST parsing | ✗ | ✓ |
| Integration points | ✗ | ✓ |

**Rule of thumb:**
- **Grep:** Find specific text/code snippets
- **code-analysis:** Understand structure, complexity, relationships

## Next Steps

- **Read reference.md** for complete API documentation
- **Read examples.md** for real-world usage patterns
- **Try with your codebase** - Start with summary format
- **Combine with ResultFilter** for massive token savings
- **Use with refactor_assistant** for targeted improvements

---

*Last Updated: 2025-11-07*

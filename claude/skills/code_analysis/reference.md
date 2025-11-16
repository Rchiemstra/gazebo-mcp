# Code Analysis - API Reference

Complete documentation for all code_analysis operations.

---

## Overview

Code Analysis provides deep static analysis of Python codebases using AST (Abstract Syntax Tree) parsing. It goes far beyond simple text search to understand code structure, complexity, dependencies, and architectural patterns.

---

## Operations

### analyze_codebase

Analyze entire codebase for structure, patterns, and integration points.

#### Signature

```python
def analyze_codebase(
    root_path: str,
    response_format: str = "summary",
    include_patterns: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None,
    max_files: Optional[int] = None,
    **kwargs
) -> OperationResult
```

#### Parameters

**root_path** (str, required)
- Root directory to analyze
- Can be relative or absolute path
- Must exist and be a directory

**response_format** (str, optional, default="summary")
- Controls the detail level of the response
- Options:
  - `"summary"` - Overview only (500-1000 tokens) - **DEFAULT**
  - `"filtered"` - Structured for ResultFilter (2000-10000 tokens) - **FOR LARGE CODEBASES**
  - `"detailed"` - All file details (50000+ tokens) - **AVOID FOR LARGE CODEBASES**

**include_patterns** (List[str], optional, default=["**/*.py"])
- Glob patterns for files to include
- Examples: `["**/*.py"]`, `["src/**/*.py", "tests/**/*.py"]`

**exclude_patterns** (List[str], optional, default=[])
- Glob patterns for files to exclude
- Examples: `["**/test_*.py"]`, `["**/__pycache__/**"]`

**max_files** (int, optional, default=None)
- Maximum number of files to analyze
- Useful for very large codebases
- Processes first N matching files

#### Returns

**OperationResult** with the following data structure:

**Summary format (DEFAULT):**
```python
{
    "success": True,
    "data": {
        "root_path": "src/",
        "total_files": 145,
        "total_lines": 12450,
        "entry_points": ["main.py", "app.py", "cli.py"],
        "patterns_summary": {
            "singleton": 3,
            "factory": 5,
            "observer": 2,
            "decorator": 8,
            "strategy": 1
        },
        "integration_points_count": 23,
        "avg_complexity": 4.2,
        "efficiency_tip": "Analysis complete! Found 145 files...",
        "next_step": "Use response_format='filtered' + ResultFilter for large datasets"
    }
}
```

**Filtered format (FOR LOCAL FILTERING):**
```python
{
    "success": True,
    "data": {
        "root_path": "src/",
        "total_files": 145,
        "files": [
            {
                "path": "src/services/payment.py",
                "total_lines": 234,
                "total_entities": 15,
                "avg_complexity": 5.2,
                "max_complexity": 12,
                "imports_count": 8,
                "classes_count": 3,
                "functions_count": 12,
                "has_patterns": ["singleton", "factory"],
                "has_integration_points": ["database", "api"],
                # Minimal data - optimized for filtering
            },
            # ... all 145 files with minimal data
        ],
        "efficiency_tip": "Use ResultFilter.search/top_n/filter to process locally"
    }
}
```

**Detailed format (AVOID FOR LARGE CODEBASES):**
```python
{
    "success": True,
    "data": {
        "root_path": "src/",
        "total_files": 145,
        "files": [
            {
                "path": "src/services/payment.py",
                "total_lines": 234,
                "entities": [
                    {
                        "type": "class",
                        "name": "PaymentProcessor",
                        "line_number": 15,
                        "base_classes": ["ABC"],
                        "methods": [...],
                        "complexity": 8,
                        # Full AST details
                    },
                    {
                        "type": "function",
                        "name": "process_payment",
                        "line_number": 45,
                        "parameters": [...],
                        "returns": "PaymentResult",
                        "complexity": 12,
                        "dependencies": [...],
                        # Full AST details
                    }
                ],
                "imports": ["typing", "datetime", "decimal"],
                "patterns": [
                    {
                        "type": "singleton",
                        "class": "PaymentProcessor",
                        "confidence": 0.95
                    }
                ],
                "integration_points": [
                    {
                        "type": "database",
                        "line": 78,
                        "details": "PostgreSQL via SQLAlchemy"
                    }
                ]
            },
            # ... all 145 files with FULL details
            # ⚠️ Can be 50,000+ tokens!
        ]
    }
}
```

#### Error Handling

**DIR_NOT_FOUND:**
```python
{
    "success": False,
    "error": "Directory not found: nonexistent/",
    "error_code": "DIR_NOT_FOUND",
    "suggestions": [
        "Check if the path is correct",
        "Use Glob('**/') to find directories",
        "Verify directory exists with Bash('ls -la')"
    ],
    "example_fix": "analyze_codebase('src/')"
}
```

**NO_PYTHON_FILES:**
```python
{
    "success": False,
    "error": "No Python files found in: data/",
    "error_code": "NO_PYTHON_FILES",
    "suggestions": [
        "Check if directory contains .py files",
        "Adjust include_patterns if needed",
        "Verify file extensions"
    ],
    "example_fix": "analyze_codebase('src/', include_patterns=['**/*.py'])"
}
```

#### Token Efficiency

| Codebase Size | Summary | Filtered | Detailed |
|---------------|---------|----------|----------|
| 10 files | 500 | 1,000 | 5,000 |
| 100 files | 800 | 5,000 | 50,000 |
| 1000 files | 1,000 | 20,000 | 500,000 |

**Critical Guidelines:**
- **< 10 files:** Any format OK
- **10-100 files:** Use summary or filtered
- **> 100 files:** ALWAYS use filtered + ResultFilter
- **Never use detailed for > 50 files**

#### Best Practices

**Pattern 1: Overview First**
```python
# Start with summary to understand scope
result = analyze_codebase("src/")
print(f"Found {result.data['total_files']} files")

# Decide next steps based on size
if result.data['total_files'] > 100:
    # Use filtered format + ResultFilter
    result = analyze_codebase("src/", response_format="filtered")
    # Then filter locally
```

**Pattern 2: Progressive Refinement**
```python
# 1. Get summary
summary = analyze_codebase("src/")

# 2. Get filtered data
filtered = analyze_codebase("src/", response_format="filtered")

# 3. Filter locally
from skills.common.filters import ResultFilter
target_files = ResultFilter.search(filtered.data["files"], "payment")

# 4. Analyze specific files in detail
for file_path in target_files[:5]:  # Top 5 only
    details = analyze_file(file_path, response_format="detailed")
    # Work with details
```

---

### analyze_file

Analyze single Python file for entities, complexity, and dependencies.

#### Signature

```python
def analyze_file(
    file_path: str,
    response_format: str = "summary",
    **kwargs
) -> OperationResult
```

#### Parameters

**file_path** (str, required)
- Path to Python file to analyze
- Must exist and be valid Python code

**response_format** (str, optional, default="summary")
- Controls the detail level of the response
- Options:
  - `"summary"` - Counts and names only (200-500 tokens)
  - `"detailed"` - Full AST analysis (2000-5000 tokens)

#### Returns

**OperationResult** with the following data structure:

**Summary format:**
```python
{
    "success": True,
    "data": {
        "file_path": "src/payment.py",
        "total_lines": 234,
        "total_entities": 15,
        "classes_count": 3,
        "functions_count": 12,
        "class_names": ["PaymentProcessor", "CardValidator", "Receipt"],
        "function_names": ["process_payment", "validate_card", ...],
        "avg_complexity": 5.2,
        "max_complexity": 12,
        "most_complex": "process_payment",
        "imports": ["typing", "datetime", "decimal"],
        "efficiency_tip": "For full details: analyze_file(..., response_format='detailed')"
    }
}
```

**Detailed format:**
```python
{
    "success": True,
    "data": {
        "file_path": "src/payment.py",
        "total_lines": 234,
        "total_entities": 15,
        "classes": [
            {
                "name": "PaymentProcessor",
                "line_number": 15,
                "base_classes": ["ABC"],
                "docstring": "Processes payment transactions...",
                "methods": [
                    {
                        "name": "process",
                        "line_number": 25,
                        "parameters": ["amount", "card"],
                        "returns": "PaymentResult",
                        "complexity": 8,
                        "docstring": "Process a payment..."
                    },
                    # ... more methods
                ],
                "attributes": ["_instance", "logger"],
                "decorators": ["singleton"],
                "patterns": ["singleton"]
            },
            # ... more classes
        ],
        "functions": [
            {
                "name": "process_payment",
                "line_number": 145,
                "parameters": [
                    {"name": "amount", "type": "Decimal", "default": None},
                    {"name": "card", "type": "CreditCard", "default": None}
                ],
                "returns": "PaymentResult",
                "raises": ["ValueError", "PaymentError"],
                "complexity": 12,
                "docstring": "Process payment transaction...",
                "decorators": ["retry", "log_errors"],
                "calls": ["validate_card", "charge_card", "create_receipt"],
                "dependencies": ["CreditCard", "PaymentResult", "Receipt"]
            },
            # ... more functions
        ],
        "imports": [
            {"module": "typing", "names": ["Dict", "Optional"]},
            {"module": "decimal", "names": ["Decimal"]},
            {"module": ".models", "names": ["CreditCard", "PaymentResult"]}
        ],
        "dependency_graph": {
            "process_payment": ["validate_card", "charge_card"],
            "validate_card": [],
            "charge_card": ["create_receipt"]
        },
        "patterns_detected": [
            {
                "type": "singleton",
                "class": "PaymentProcessor",
                "line": 15,
                "confidence": 0.95
            }
        ],
        "integration_points": [
            {
                "type": "database",
                "line": 78,
                "method": "store_transaction",
                "details": "SQLAlchemy ORM"
            },
            {
                "type": "api",
                "line": 92,
                "method": "charge_card",
                "details": "Stripe API"
            }
        ]
    }
}
```

#### Error Handling

**FILE_NOT_FOUND:**
```python
{
    "success": False,
    "error": "File not found: src/nonexistent.py",
    "error_code": "FILE_NOT_FOUND",
    "suggestions": [
        "Check if the file path is correct",
        "Use Glob('**/*.py') to find Python files",
        "Verify file exists with Bash('ls -la src/')"
    ],
    "example_fix": "analyze_file('src/services/payment.py')"
}
```

**SYNTAX_ERROR:**
```python
{
    "success": False,
    "error": "Python syntax error in payment.py at line 45: invalid syntax",
    "error_code": "SYNTAX_ERROR",
    "suggestions": [
        "Fix syntax errors before analysis",
        "Run: python -m py_compile payment.py",
        "Check for missing colons, parentheses, or quotes"
    ],
    "example_fix": "Fix syntax, then: analyze_file('payment.py')"
}
```

#### Token Efficiency

- **Summary format:** 200-500 tokens (recommended default)
- **Detailed format:** 2000-5000 tokens (when needed)
- **Savings:** Up to 90% with summary

**Best Practice:**
1. Start with summary to understand file
2. Use detailed only when you need AST details
3. For large files (>500 lines), prefer summary

---

## Data Structures

### Entity Types

Code entities detected by analysis:

- **class** - Class definitions
- **function** - Function/method definitions
- **import** - Import statements
- **attribute** - Class attributes
- **decorator** - Decorators (@decorator)

### Pattern Types

Design patterns automatically detected:

- **singleton** - Single instance pattern
- **factory** - Object creation pattern
- **observer** - Event/listener pattern
- **decorator** - Function/class wrapping
- **strategy** - Algorithm encapsulation
- **repository** - Data access abstraction
- **adapter** - Interface adaptation
- **facade** - Simplified interface

### Integration Point Types

External connections detected:

- **api** - REST/GraphQL/RPC endpoints
- **database** - SQL/ORM/NoSQL access
- **message_queue** - RabbitMQ/Kafka/Redis
- **file_io** - File operations
- **network** - HTTP/WebSocket calls
- **cache** - Cache systems
- **external_service** - Third-party APIs

### Complexity Metrics

- **Cyclomatic Complexity** - Number of decision points
- **Cognitive Complexity** - Mental effort to understand
- **Average Complexity** - Mean across all functions
- **Max Complexity** - Highest single function complexity

**Interpretation:**
- 1-5: Low complexity (good)
- 6-10: Moderate complexity (acceptable)
- 11-20: High complexity (consider refactoring)
- 20+: Very high complexity (refactor recommended)

---

## Common Workflows

### Workflow 1: Understanding New Codebase

```python
from skills.code_analysis.operations import analyze_codebase, analyze_file

# Step 1: Get overview
overview = analyze_codebase("src/")
print(f"Files: {overview.data['total_files']}")
print(f"Entry points: {overview.data['entry_points']}")
print(f"Patterns: {overview.data['patterns_summary']}")
print(f"Integrations: {overview.data['integration_points_count']}")

# Step 2: Examine entry points
for entry_point in overview.data['entry_points'][:3]:
    details = analyze_file(f"src/{entry_point}", response_format="detailed")
    print(f"\nEntry: {entry_point}")
    print(f"  Classes: {[c['name'] for c in details.data['classes']]}")
    print(f"  Main functions: {[f['name'] for f in details.data['functions']]}")

# Step 3: Find integration points
result = analyze_codebase("src/", response_format="filtered")
from skills.common.filters import ResultFilter
api_files = [
    f for f in result.data["files"]
    if "api" in f.get("has_integration_points", [])
]
print(f"\nAPI integration files: {len(api_files)}")
```

### Workflow 2: Finding Refactoring Targets

```python
from skills.code_analysis.operations import analyze_codebase
from skills.common.filters import ResultFilter

# Get all files
result = analyze_codebase("src/", response_format="filtered")

# Find high-complexity files
complex_files = ResultFilter.top_n_by_field(
    result.data["files"],
    "avg_complexity",
    10
)

print("Top 10 complex files to refactor:")
for file_data in complex_files:
    print(f"  {file_data['path']}: {file_data['avg_complexity']:.1f}")

# Analyze most complex in detail
most_complex = complex_files[0]
details = analyze_file(most_complex['path'], response_format="detailed")

print(f"\nMost complex functions in {most_complex['path']}:")
for func in sorted(details.data['functions'], key=lambda f: f['complexity'], reverse=True)[:5]:
    print(f"  {func['name']}: complexity {func['complexity']}")
```

### Workflow 3: Dependency Analysis

```python
from skills.code_analysis.operations import analyze_file

# Analyze file
result = analyze_file("src/services/order.py", response_format="detailed")

# Show import structure
print("Imports:")
for imp in result.data['imports']:
    print(f"  from {imp['module']} import {', '.join(imp['names'])}")

# Show function dependencies
print("\nDependency Graph:")
for func, deps in result.data['dependency_graph'].items():
    print(f"  {func} → {', '.join(deps) if deps else 'no dependencies'}")

# Find circular dependencies
# (implement logic to detect cycles)
```

### Workflow 4: Pattern Detection

```python
from skills.code_analysis.operations import analyze_codebase
from skills.common.filters import ResultFilter

# Find all singleton implementations
result = analyze_codebase("src/", response_format="filtered")
singleton_files = [
    f for f in result.data["files"]
    if "singleton" in f.get("has_patterns", [])
]

print(f"Found {len(singleton_files)} files with Singleton pattern")

# Examine each singleton
for file_data in singleton_files:
    details = analyze_file(file_data['path'], response_format="detailed")
    for pattern in details.data['patterns_detected']:
        if pattern['type'] == 'singleton':
            print(f"\n{file_data['path']}:")
            print(f"  Class: {pattern['class']}")
            print(f"  Line: {pattern['line']}")
            print(f"  Confidence: {pattern['confidence']:.1%}")
```

---

## Performance Notes

### Execution Time

| Operation | Small (<10 files) | Medium (10-100) | Large (100+) |
|-----------|-------------------|-----------------|--------------|
| analyze_codebase | < 1s | 1-5s | 5-30s |
| analyze_file | < 0.1s | < 0.1s | < 0.1s |

### Memory Usage

- **Summary format:** Low (< 10 MB)
- **Filtered format:** Moderate (10-50 MB)
- **Detailed format:** High (50-500 MB)

### Recommended Limits

- **analyze_codebase:** < 1000 files (use max_files parameter)
- **analyze_file:** < 5000 lines per file

---

## ResultFilter Integration

### Why Use ResultFilter?

For large codebases (>100 files), filtering locally saves 95-99% tokens:

```python
# Without filtering: 50,000 tokens
result = analyze_codebase("large_project/", response_format="detailed")

# With filtering: 500 tokens (99% savings!)
result = analyze_codebase("large_project/", response_format="filtered")
filtered = ResultFilter.search(result.data["files"], "payment")
# Only 10 files sent to agent instead of 1000
```

### Common ResultFilter Operations

```python
from skills.common.filters import ResultFilter

# Search by keyword
payments = ResultFilter.search(files, "payment", ["path", "name"])

# Top N by field
complex = ResultFilter.top_n_by_field(files, "avg_complexity", 10)

# Filter by field value
python_files = ResultFilter.filter_by_field(files, "language", "python")

# Combine filters
result = ResultFilter.search(files, "auth")
result = ResultFilter.top_n_by_field(result, "complexity", 5)
# Top 5 complex auth files
```

---

## Related Skills

- **code_search** - Find specific code patterns and usage
- **refactor_assistant** - Refactor based on complexity analysis
- **test_orchestrator** - Generate tests for complex functions
- **doc_generator** - Generate docs from AST analysis

---

## Dependencies

### Required

- Python 3.8+
- AST standard library

### Optional

- **networkx** - For dependency graph visualization
- **graphviz** - For graph rendering

---

*Last Updated: 2025-11-07*

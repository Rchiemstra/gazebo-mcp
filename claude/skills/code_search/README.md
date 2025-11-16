# Code Search

Intelligent code search system with AST-based indexing that understands code structure, semantics, and relationships. Goes beyond simple text search to find definitions, usages, and patterns across entire codebases.

## Overview

Code Search transforms how developers navigate and understand code by using Abstract Syntax Tree (AST) parsing to index and search Python code. Instead of grep-style text matching, it understands functions, classes, variables, imports, and their relationships.

## Features

### 🔍 Symbol Search
- **AST-Based Indexing**: Understands code structure, not just text
- **Multiple Symbol Types**: Functions, classes, methods, variables, constants
- **Fuzzy Matching**: Find symbols even with approximate names
- **Wildcard Support**: Use glob patterns like `process_*` or `*Handler`
- **Relevance Scoring**: Results ranked by match quality
- **Context-Aware**: Shows surrounding code and documentation

### 📍 Definition Finding
- **Jump to Definition**: Instantly locate where symbols are defined
- **Import Resolution**: Follows import statements to find definitions
- **Module Path Resolution**: Resolves relative and absolute imports
- **Full Context**: Returns complete source code with signatures
- **Inheritance Tracking**: Finds base class definitions
- **Method Overrides**: Identifies overridden methods

### 🔗 Usage Finding
- **Find All References**: Locate every usage of a symbol
- **Usage Types**: Distinguishes calls, references, imports, assignments
- **Call Hierarchies**: Shows where functions are called from
- **Context Tracking**: Identifies parent functions and classes
- **Import Tracking**: Finds all files that import a symbol
- **Attribute Access**: Tracks object attribute usage

### 🎯 Pattern Matching
- **Regex Support**: Search with regular expressions
- **Structural Patterns**: Match code patterns, not just text
- **Anti-Pattern Detection**: Find problematic code patterns
- **Code Clone Detection**: Locate similar code blocks
- **Convention Checking**: Find naming pattern violations

### ⚡ Performance
- **Fast Indexing**: AST caching for quick searches
- **Incremental Updates**: Only re-index changed files
- **Parallel Processing**: Multi-threaded for large projects
- **Memory Efficient**: Lazy loading of source files
- **Smart Caching**: Import resolution caching

## Installation

No external dependencies - uses Python standard library!

```bash
cd skills/code_search
python demo.py  # Run the demonstration
```

## Quick Start

### Search for Symbols

```python
from code_search import search_symbol

# Search for a function
results = search_symbol(
    project_path='./myproject',
    symbol_name='process_data',
    symbol_type='function',
    exact_match=True
)

print(f"Found {results['total_matches']} matches")
for match in results['matches']:
    print(f"{match['file_path']}:{match['line_number']}")
    print(f"  {match['signature']}")
    print(f"  Relevance: {match['relevance_score']:.2f}")
```

### Find Definition

```python
from code_search import find_definition

# Find where a symbol is defined
result = find_definition(
    project_path='./myproject',
    symbol_name='DataProcessor',
    file_context='./myproject/main.py'  # Optional: helps with imports
)

if result['found']:
    definition = result['definition']
    print(f"Defined at {definition['file_path']}:{definition['line_number']}")
    print(f"Type: {definition['definition_type']}")
    print(f"\n{definition['source_code']}")
```

### Find All Usages

```python
from code_search import find_usages

# Find all places where a symbol is used
result = find_usages(
    project_path='./myproject',
    symbol_name='calculate_metrics'
)

print(f"Found {result['total_usages']} usages")

# Group by usage type
for usage_type, count in result['usage_counts'].items():
    print(f"  {usage_type}: {count}")

# Show each usage
for usage in result['usages']:
    print(f"\n{usage['file_path']}:{usage['line_number']}")
    print(f"  Type: {usage['usage_type']}")
    if usage['parent_function']:
        print(f"  In: {usage['parent_function']}")
```

### Search with Patterns

```python
from code_search import search_pattern

# Find all test functions
result = search_pattern(
    project_path='./myproject',
    pattern=r'def test_\w+\(.*\):'
)

print(f"Found {result['total_matches']} test functions")
for match in result['matches']:
    print(f"  {match['file_path']}:{match['line_number']}")
    print(f"    {match['matched_code']}")
```

## API Reference

### search_symbol

Search for symbols in a project.

```python
search_symbol(
    project_path: str,
    symbol_name: str,
    symbol_type: str = "all",
    exact_match: bool = False,
    include_private: bool = False
) -> Dict[str, Any]
```

**Parameters:**
- `project_path`: Path to project root directory
- `symbol_name`: Symbol name to search for (supports wildcards)
- `symbol_type`: Filter by type - 'function', 'class', 'variable', 'method', 'all'
- `exact_match`: If True, match exact name only; if False, allow fuzzy/wildcard matching
- `include_private`: Include symbols starting with '_'

**Returns:**
```python
{
    'matches': [
        {
            'file_path': str,
            'line_number': int,
            'symbol_name': str,
            'symbol_type': str,
            'context': str,          # Surrounding code
            'signature': str,        # Function/class signature
            'relevance_score': float,  # 0.0 to 1.0
            'docstring': str         # If available
        }
    ],
    'total_matches': int,
    'index_stats': {
        'files_indexed': int,
        'symbols_indexed': int,
        'functions': int,
        'classes': int,
        'methods': int
    }
}
```

**Examples:**
```python
# Exact match
results = search_symbol(
    project_path='.',
    symbol_name='User',
    symbol_type='class',
    exact_match=True
)

# Wildcard search
results = search_symbol(
    project_path='.',
    symbol_name='*Handler',
    symbol_type='class'
)

# Fuzzy search
results = search_symbol(
    project_path='.',
    symbol_name='proces',  # Will match 'process', 'processor', etc.
    symbol_type='function'
)

# Find all symbols
results = search_symbol(
    project_path='.',
    symbol_name='*',
    symbol_type='all'
)
```

### find_definition

Find the definition of a symbol.

```python
find_definition(
    project_path: str,
    symbol_name: str,
    file_context: Optional[str] = None
) -> Dict[str, Any]
```

**Parameters:**
- `project_path`: Path to project root
- `symbol_name`: Name of symbol to find
- `file_context`: Optional file where symbol is used (helps resolve imports)

**Returns:**
```python
{
    'found': bool,
    'definition': {
        'file_path': str,
        'line_number': int,
        'symbol_name': str,
        'definition_type': str,  # 'function', 'class', 'method', 'variable'
        'source_code': str,       # Complete definition
        'signature': str,         # Function/class signature
        'docstring': str,         # If available
        'parent_class': str       # For methods
    } if found else None
}
```

**Examples:**
```python
# Find class definition
result = find_definition(
    project_path='./myproject',
    symbol_name='UserManager'
)

# Find with import context
result = find_definition(
    project_path='./myproject',
    symbol_name='process_data',
    file_context='./myproject/handlers/user_handler.py'
)

if result['found']:
    print(result['definition']['source_code'])
```

### find_usages

Find all usages/references of a symbol.

```python
find_usages(
    project_path: str,
    symbol_name: str,
    definition_file: Optional[str] = None
) -> Dict[str, Any]
```

**Parameters:**
- `project_path`: Path to project root
- `symbol_name`: Symbol to find usages of
- `definition_file`: Optional file containing the definition

**Returns:**
```python
{
    'usages': [
        {
            'file_path': str,
            'line_number': int,
            'column': int,
            'context': str,          # Surrounding code
            'usage_type': str,       # 'call', 'reference', 'import', 'assignment', etc.
            'parent_function': str,  # Function containing this usage
            'parent_class': str      # Class containing this usage
        }
    ],
    'total_usages': int,
    'usage_counts': {
        'call': int,
        'reference': int,
        'import': int,
        ...
    },
    'symbol_name': str
}
```

**Examples:**
```python
# Find all function calls
result = find_usages(
    project_path='.',
    symbol_name='send_email'
)

for usage in result['usages']:
    if usage['usage_type'] == 'call':
        print(f"Called in {usage['parent_function']}")

# Analyze usage patterns
print(f"Total usages: {result['total_usages']}")
for usage_type, count in result['usage_counts'].items():
    print(f"  {usage_type}: {count}")
```

### search_pattern

Search for code patterns using regex.

```python
search_pattern(
    project_path: str,
    pattern: str,
    language: str = "python"
) -> Dict[str, Any]
```

**Parameters:**
- `project_path`: Path to project root
- `pattern`: Regular expression pattern
- `language`: Programming language (currently only 'python')

**Returns:**
```python
{
    'matches': [
        {
            'file_path': str,
            'line_number': int,
            'matched_code': str,     # The matching line
            'context': str,           # Surrounding lines
            'similarity_score': float
        }
    ],
    'total_matches': int,
    'pattern': str
}
```

**Examples:**
```python
# Find all async functions
result = search_pattern(
    project_path='.',
    pattern=r'async def \w+\('
)

# Find bare except clauses
result = search_pattern(
    project_path='.',
    pattern=r'except\s*:'
)

# Find print statements (debugging code)
result = search_pattern(
    project_path='.',
    pattern=r'print\('
)
```

## Use Cases

### 1. Code Navigation

Quickly navigate large codebases:

```python
# Find where a class is defined
definition = find_definition(
    project_path='.',
    symbol_name='PaymentProcessor'
)

# Jump to definition
print(f"Go to: {definition['definition']['file_path']}:{definition['definition']['line_number']}")
```

### 2. Refactoring Safety

Find all usages before renaming:

```python
# Before renaming 'old_function' to 'new_function'
usages = find_usages(
    project_path='.',
    symbol_name='old_function'
)

print(f"Found {usages['total_usages']} usages to update:")
for usage in usages['usages']:
    print(f"  {usage['file_path']}:{usage['line_number']}")

# Now safe to rename knowing all locations
```

### 3. Code Understanding

Understand how code is used:

```python
# How is this utility function used?
usages = find_usages(
    project_path='.',
    symbol_name='format_currency'
)

# Group by calling context
callers = set()
for usage in usages['usages']:
    if usage['parent_function']:
        callers.add(usage['parent_function'])

print(f"Called from {len(callers)} different functions")
```

### 4. Finding Unused Code

Identify potentially unused functions:

```python
# Get all functions
all_functions = search_symbol(
    project_path='.',
    symbol_name='*',
    symbol_type='function'
)

# Check each for usages
unused = []
for func in all_functions['matches']:
    usages = find_usages(
        project_path='.',
        symbol_name=func['symbol_name']
    )

    # Exclude the definition itself
    if usages['total_usages'] <= 1:
        unused.append(func['symbol_name'])

print(f"Potentially unused functions: {unused}")
```

### 5. Test Coverage Analysis

Find functions without tests:

```python
# Find all test functions
tests = search_pattern(
    project_path='.',
    pattern=r'def test_\w+\('
)

test_names = {match['matched_code'] for match in tests['matches']}

# Find all source functions
functions = search_symbol(
    project_path='./src',
    symbol_name='*',
    symbol_type='function'
)

# Check if tested
for func in functions['matches']:
    test_name = f"test_{func['symbol_name']}"
    if not any(test_name in t for t in test_names):
        print(f"No test for: {func['symbol_name']}")
```

### 6. Dependency Impact Analysis

Assess impact of removing a dependency:

```python
# Find all usages of a module
usages = find_usages(
    project_path='.',
    symbol_name='requests'  # external dependency
)

print(f"Module 'requests' is used in {len(set(u['file_path'] for u in usages['usages']))} files")

# List affected files
for usage in usages['usages']:
    if usage['usage_type'] == 'import':
        print(f"  Imported in: {usage['file_path']}")
```

### 7. Architecture Analysis

Understand module relationships:

```python
# Find all imports of a core module
usages = find_usages(
    project_path='.',
    symbol_name='core'
)

import_locations = [u for u in usages['usages'] if u['usage_type'] == 'import']

print(f"Core module imported by {len(import_locations)} files:")
for location in import_locations:
    print(f"  {location['file_path']}")
```

## Integration with Other Skills

### With refactor-assistant

Safe refactoring workflow:

```python
from code_search import find_usages, find_definition
from refactor_assistant import refactor_code

# 1. Find all usages
usages = find_usages(
    project_path='.',
    symbol_name='old_function_name'
)

print(f"Will affect {usages['total_usages']} locations")

# 2. Review each usage
for usage in usages['usages']:
    print(f"{usage['file_path']}:{usage['line_number']}")
    print(f"  Context: {usage['context']}")

# 3. Proceed with refactoring
refactor_result = refactor_code(
    file_path='core.py',
    refactoring_type='rename',
    old_name='old_function_name',
    new_name='new_function_name'
)

# 4. Verify all usages updated
new_usages = find_usages(
    project_path='.',
    symbol_name='old_function_name'
)

if new_usages['total_usages'] == 0:
    print("✅ All usages successfully renamed")
```

### With test-orchestrator

Generate tests for untested code:

```python
from code_search import search_symbol
from test_orchestrator import generate_tests

# Find all functions
functions = search_symbol(
    project_path='./src',
    symbol_name='*',
    symbol_type='function',
    include_private=False
)

for func in functions['matches']:
    # Check if test exists
    test_file = func['file_path'].replace('src/', 'tests/test_')

    if not Path(test_file).exists():
        print(f"Generating tests for {func['symbol_name']}")
        generate_tests(
            source_file=func['file_path'],
            target_function=func['symbol_name']
        )
```

### With doc-generator

Document undocumented code:

```python
from code_search import search_symbol
from doc_generator import generate_docstrings

# Find functions without docstrings
functions = search_symbol(
    project_path='.',
    symbol_name='*',
    symbol_type='function'
)

for func in functions['matches']:
    if not func['docstring']:
        print(f"Generating docstring for {func['symbol_name']}")
        generate_docstrings(
            file_path=func['file_path'],
            style='google'
        )
```

### With pr-review-assistant

Review code changes:

```python
from code_search import find_usages
from pr_review_assistant import review_pull_request

# For each changed function, check its impact
pr_changes = {'modified': ['api/handlers.py']}

# Find what functions changed
# ... (extract changed functions)

for func_name in changed_functions:
    usages = find_usages(
        project_path='.',
        symbol_name=func_name
    )

    if usages['total_usages'] > 50:
        print(f"⚠️  {func_name} is heavily used ({usages['total_usages']} places)")
        print("Consider extra testing")
```

## Advanced Usage

### Custom Search Filters

```python
from code_search.core.search_engine import CodeSearchEngine

# Create custom search engine
engine = CodeSearchEngine()
engine.index_project('./myproject')

# Custom filtering
matches = engine.search(
    symbol_name='*',
    symbol_type='function',
    exact_match=False,
    include_private=False
)

# Filter by additional criteria
public_async = [
    m for m in matches
    if m.symbol_name.startswith('async ')
    and not m.is_private
]
```

### Batch Processing

```python
from concurrent.futures import ThreadPoolExecutor
from code_search import find_usages

symbols_to_check = ['function1', 'function2', 'function3']

def check_usage(symbol):
    result = find_usages(
        project_path='.',
        symbol_name=symbol
    )
    return symbol, result['total_usages']

# Process in parallel
with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(check_usage, symbols_to_check)

for symbol, count in results:
    print(f"{symbol}: {count} usages")
```

### Building a Call Graph

```python
from code_search import search_symbol, find_usages

def build_call_graph(project_path):
    """Build a call graph of all functions."""
    # Get all functions
    functions = search_symbol(
        project_path=project_path,
        symbol_name='*',
        symbol_type='function'
    )

    graph = {}
    for func in functions['matches']:
        # Find what this function calls
        # (simplified - would need AST analysis of function body)
        usages = find_usages(
            project_path=project_path,
            symbol_name=func['symbol_name']
        )

        graph[func['symbol_name']] = {
            'defined_in': func['file_path'],
            'called_from': [
                u['parent_function']
                for u in usages['usages']
                if u['usage_type'] == 'call' and u['parent_function']
            ]
        }

    return graph

# Usage
graph = build_call_graph('.')
for func, info in graph.items():
    callers = len(set(info['called_from']))
    print(f"{func}: called from {callers} places")
```

## Best Practices

### 1. Use Exact Match for Known Symbols

```python
# Fast and precise
result = search_symbol(
    project_path='.',
    symbol_name='UserManager',
    exact_match=True
)
```

### 2. Provide File Context for Imports

```python
# Helps resolve imports correctly
definition = find_definition(
    project_path='.',
    symbol_name='process_data',
    file_context='./src/handlers/user.py'
)
```

### 3. Filter by Symbol Type

```python
# More focused results
classes = search_symbol(
    project_path='.',
    symbol_name='*Manager',
    symbol_type='class'  # Only classes
)
```

### 4. Exclude Private Symbols

```python
# Only public API
public_functions = search_symbol(
    project_path='./src',
    symbol_name='*',
    symbol_type='function',
    include_private=False
)
```

### 5. Cache Index for Multiple Searches

```python
from code_search.core.search_engine import CodeSearchEngine

# Index once
engine = CodeSearchEngine()
engine.index_project('./myproject')

# Search many times
for symbol in ['User', 'Product', 'Order']:
    matches = engine.search(symbol, exact_match=True)
    print(f"{symbol}: {len(matches)} matches")
```

## Demo

Run the comprehensive demo:

```bash
cd skills/code_search
python demo.py
```

The demo demonstrates:
- Symbol search with different filters
- Wildcard and fuzzy matching
- Definition finding with import resolution
- Usage tracking with context
- Pattern matching with regex
- Performance metrics
- Integration examples

## Limitations

### Current Implementation

- **Python Only**: Currently only supports Python code
- **AST-Based**: Limited to syntactically valid Python files
- **Import Resolution**: Basic module resolution (doesn't handle all edge cases)
- **No Type Analysis**: Doesn't use type hints for semantic understanding
- **Single Project**: Doesn't index across multiple projects
- **No Persistence**: Index is rebuilt on each run

### Recommended Approach

1. **Index Once**: For large projects, build index once and cache
2. **Incremental Updates**: Only re-index changed files
3. **Verify Results**: Always verify critical refactoring results
4. **Combine Tools**: Use with IDE features for best experience

## Future Enhancements

Planned improvements:

- **Multi-Language Support**: JavaScript, TypeScript, Java, Go, Rust
- **Persistent Index**: Save and load index from disk
- **Incremental Indexing**: Track file changes and update incrementally
- **Type-Aware Search**: Use type hints for semantic search
- **Cross-Project Search**: Index and search across multiple projects
- **LSP Integration**: Language Server Protocol support for IDE integration
- **Semantic Search**: Use embeddings for semantic code search
- **Code Clone Detection**: Find duplicate or similar code blocks

## Troubleshooting

### "No matches found but I know the symbol exists"

- Check symbol name spelling
- Try fuzzy search (`exact_match=False`)
- Verify file is not in skip directories (venv, __pycache__, etc.)
- Check for syntax errors in the file

### "Import resolution not working"

- Ensure `__init__.py` files exist in packages
- Provide `file_context` parameter to help resolution
- Check module structure matches import statement

### "Too many results"

- Use `exact_match=True` for precise matching
- Filter by `symbol_type`
- Exclude private symbols with `include_private=False`

### "Search is slow"

- Cache the search engine instance for multiple searches
- Use specific symbol types instead of 'all'
- Consider excluding large vendor directories

## Contributing

Suggestions for improvement:

1. Add incremental indexing for file changes
2. Implement persistent index storage
3. Add support for more languages
4. Improve import resolution edge cases
5. Add semantic search capabilities

## Related Skills

- **refactor-assistant**: Safe refactoring with usage tracking
- **test-orchestrator**: Find untested code
- **doc-generator**: Document undocumented symbols
- **dependency-guardian**: Analyze dependency usage

## License

Part of Claude Code Skills framework.

## Support

- Run demo: `python demo.py`
- Check examples: See `examples/` directory
- Review source: Read code in `core/` modules

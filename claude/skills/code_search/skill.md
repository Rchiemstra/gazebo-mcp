---
name: code-search
version: 0.1.0
description: Intelligent code search with AST-based indexing and semantic understanding
category: developer-productivity
author: Claude Code Skills
tools:
  - Read
  - Glob
  - Grep
dependencies: []
tags: [search, code-navigation, ast, indexing, symbols, references]
operations:
  search_symbol: "Find symbols (functions, classes, variables) in codebase"
  search_pattern: "Search for code patterns in codebase"
  find_definition: "Find the definition of a symbol"
  find_usages: "Find all usages of a symbol"
---

# Code Search

## Overview

Code Search is an intelligent code search system that goes beyond simple text search by understanding code structure, semantics, and relationships. It uses AST-based indexing to find definitions, usages, and patterns across entire codebases.

## Capabilities

### 🔍 Symbol Search
- Find function definitions
- Locate class declarations
- Search for variables and constants
- Discover imports and dependencies
- Support for wildcards and regex

### 📍 Definition Finder
- Jump to definition from any usage
- Find all definitions of a symbol
- Resolve imports and aliases
- Track inheritance chains
- Identify overridden methods

### 🔗 Usage Finder
- Find all usages of a function
- Locate all references to a class
- Track variable usage patterns
- Identify callers of a method
- Analyze import usage

### 🎯 Pattern Matching
- Search for code patterns
- Find similar code blocks
- Detect anti-patterns
- Match AST structures
- Structural search and replace

### 📊 Code Analytics
- Symbol frequency analysis
- Dependency graphs
- Call hierarchies
- Unused code detection
- Complexity metrics

## Operations

### search_symbol
Find symbols (functions, classes, variables) in codebase.

**Input:**
```python
{
    'project_path': str,        # Path to project root
    'symbol_name': str,         # Symbol to search for
    'symbol_type': str,         # 'function', 'class', 'variable', 'all'
    'exact_match': bool         # Exact match or fuzzy search
}
```

**Output:**
```python
{
    'matches': [
        {
            'file_path': str,
            'line_number': int,
            'symbol_name': str,
            'symbol_type': str,
            'context': str,
            'signature': str
        }
    ],
    'total_matches': int
}
```

### find_definition
Find the definition of a symbol.

**Input:**
```python
{
    'project_path': str,        # Path to project root
    'symbol_name': str,         # Symbol to find
    'file_context': str         # Optional: file where symbol is used
}
```

**Output:**
```python
{
    'definition': {
        'file_path': str,
        'line_number': int,
        'symbol_name': str,
        'definition_type': str,
        'source_code': str
    },
    'found': bool
}
```

### find_usages
Find all usages/references of a symbol.

**Input:**
```python
{
    'project_path': str,        # Path to project root
    'symbol_name': str,         # Symbol to find usages of
    'definition_file': str      # File containing definition
}
```

**Output:**
```python
{
    'usages': [
        {
            'file_path': str,
            'line_number': int,
            'context': str,
            'usage_type': str  # 'call', 'reference', 'import'
        }
    ],
    'total_usages': int
}
```

### search_pattern
Search for code patterns using AST matching.

**Input:**
```python
{
    'project_path': str,        # Path to project root
    'pattern': str,             # Code pattern to match
    'language': str             # 'python', 'javascript', etc.
}
```

**Output:**
```python
{
    'matches': [
        {
            'file_path': str,
            'line_number': int,
            'matched_code': str,
            'similarity_score': float
        }
    ]
}
```

## Integration

Works seamlessly with other skills:
- **refactor-assistant**: Find all usages before refactoring
- **test-orchestrator**: Locate test coverage gaps
- **doc-generator**: Find undocumented symbols
- **dependency-guardian**: Analyze dependency usage

## Usage Example

```python
from code_search import search_symbol, find_definition, find_usages

# Search for a function
results = search_symbol(
    project_path='./myproject',
    symbol_name='process_data',
    symbol_type='function',
    exact_match=False
)

print(f"Found {results['total_matches']} matches")
for match in results['matches']:
    print(f"  {match['file_path']}:{match['line_number']} - {match['signature']}")

# Find definition
definition = find_definition(
    project_path='./myproject',
    symbol_name='DataProcessor'
)

if definition['found']:
    print(f"Definition: {definition['definition']['file_path']}:{definition['definition']['line_number']}")

# Find all usages
usages = find_usages(
    project_path='./myproject',
    symbol_name='calculate_metrics',
    definition_file='analytics.py'
)

print(f"Found {usages['total_usages']} usages")
```

## Performance

- **Fast indexing**: AST caching for quick searches
- **Incremental updates**: Only re-index changed files
- **Parallel processing**: Multi-threaded indexing
- **Memory efficient**: Lazy loading of source files

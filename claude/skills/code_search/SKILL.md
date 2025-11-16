---
name: code-search
description: Intelligent code search with AST-based indexing and semantic understanding for finding symbols, patterns, and usages
version: 0.1.0
category: analysis
tags:
  - code-search
  - ast
  - symbols
  - patterns
activation: manual
tools:
  - Read
  - Glob
  - Grep
dependencies: []
---

# Code Search

Intelligent code search providing symbol search, pattern matching, definition finding, and usage tracking across codebases.

---

## When to Use This Skill

Use code-search when you need to:

- **Find symbols** - Locate functions, classes, variables
- **Search patterns** - Find code patterns (AST, regex, text)
- **Find definitions** - Jump to symbol definitions
- **Find usages** - Track where symbols are used
- **Navigate codebases** - Understand code structure

**Don't use for:**
- Simple grep searches (use Grep tool directly)
- Full-text search (use search engines)

---

## Quick Start

```python
from skills.code_search.operations import search_symbol

result = search_symbol(
    project_path=".",
    symbol_name="PaymentProcessor",
    symbol_type="class"
)

if result.success:
    for match in result.data['matches']:
        print(f"{match['file']}:{match['line']}")
```

---

## Operations

### search_symbol
Find symbols (functions, classes, variables) in codebase.

### search_pattern
Search for code patterns (AST, regex, or text).

### find_definition
Find the definition of a symbol.

### find_usages
Find all usages of a symbol.

---

## Search Types

- **Symbol Search** - Functions, classes, variables
- **AST Pattern Search** - Structural code patterns
- **Regex Search** - Pattern matching
- **Text Search** - Simple text search

---

*Last Updated: 2025-11-08*

# Code Search - API Reference

## Operations

### search_symbol

```python
def search_symbol(
    project_path: str,
    symbol_name: str,
    symbol_type: str = "all",
    exact_match: bool = False
) -> OperationResult
```

Returns: List of symbol matches with file, line, context

### search_pattern

```python
def search_pattern(
    project_path: str,
    pattern: str,
    pattern_type: str = "ast"
) -> OperationResult
```

Returns: List of pattern matches

### find_definition

```python
def find_definition(
    project_path: str,
    symbol_name: str
) -> OperationResult
```

Returns: Definition location

### find_usages

```python
def find_usages(
    project_path: str,
    symbol_name: str
) -> OperationResult
```

Returns: List of usage locations

---

*Last Updated: 2025-11-08*

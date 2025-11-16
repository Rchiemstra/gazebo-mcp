# Code Search - Usage Examples

## Example 1: Find Class Definition

```python
from skills.code_search.operations import search_symbol

result = search_symbol(".", "PaymentProcessor", symbol_type="class")
```

## Example 2: Find Function Usages

```python
from skills.code_search.operations import find_usages

result = find_usages(".", "process_payment")
```

## Example 3: AST Pattern Search

```python
from skills.code_search.operations import search_pattern

result = search_pattern(".", "for ... in ...: if ...", pattern_type="ast")
```

## Example 4: Find Definition

```python
from skills.code_search.operations import find_definition

result = find_definition(".", "User")
```

## Example 5: Fuzzy Symbol Search

```python
result = search_symbol(".", "payment", exact_match=False)
```

---

*Last Updated: 2025-11-08*

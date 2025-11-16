# Spec to Implementation - Usage Examples

## Example 1: Implement from Specification

```python
from skills.spec_to_implementation.operations import implement_from_spec

result = implement_from_spec(
    spec_file="specs/user_api.md",
    output_dir="src/api",
    include_tests=True,
    include_docs=True
)
```

## Example 2: Analyze Specification

```python
from skills.spec_to_implementation.operations import analyze_spec

result = analyze_spec("specs/payment_system.md")

if result.success:
    print(f"Completeness: {result.data['completeness_score']}%")
```

---

*Last Updated: 2025-11-08*

# Doc Generator - Usage Examples

## Example 1: Generate Google-Style Docstrings

```python
from skills.doc_generator.operations import generate_docstrings

result = generate_docstrings("src/payment.py", style="google")

if result.success:
    print(f"✅ Documented {result.data['functions_documented']} functions")
    print(f"Coverage: {result.data['coverage_percent']}%")
```

## Example 2: Generate Project README

```python
from skills.doc_generator.operations import generate_readme

result = generate_readme(
    project_path=".",
    include_api=True,
    include_examples=True
)

if result.success:
    print(f"✅ README generated: {result.data['readme_path']}")
    print(f"Sections: {result.data['sections_generated']}")
```

## Example 3: Documentation Quality Check

```python
from skills.doc_generator.operations import analyze_documentation

result = analyze_documentation(".")

if result.success:
    data = result.data
    print(f"Coverage: {data['coverage_percent']}%")
    print(f"Quality Score: {data['quality_score']}/100")

    if data['coverage_percent'] < 80:
        print("⚠️  Needs improvement")
        for issue in data['issues']:
            print(f"  - {issue['file']}: {issue['issue']}")
```

## Example 4: Pre-commit Documentation Check

```python
# .git/hooks/pre-commit
from skills.doc_generator.operations import analyze_documentation

result = analyze_documentation(".")

if result.data['coverage_percent'] < 70:
    print("❌ Documentation coverage too low")
    exit(1)
```

## Example 5: Different Docstring Styles

```python
styles = ["google", "numpy", "sphinx"]

for style in styles:
    result = generate_docstrings(f"src/{style}_module.py", style=style)
    print(f"{style}: {result.data['functions_documented']} functions")
```

## Example 6: README with Examples

```python
result = generate_readme(
    ".",
    include_api=True,
    include_examples=True
)
```

## Example 7: Minimal README

```python
result = generate_readme(
    ".",
    include_api=False,
    include_examples=False
)
```

## Example 8: Bulk Documentation

```python
import glob

files = glob.glob("src/**/*.py", recursive=True)

for file in files:
    result = generate_docstrings(file, style="google")
    print(f"{file}: {result.data['coverage_percent']}%")
```

## Example 9: Documentation Report

```python
analysis = analyze_documentation(".")
docstrings = generate_docstrings("src/main.py", style="google")
readme = generate_readme(".")

print(f"Project Documentation Status:")
print(f"  Coverage: {analysis.data['coverage_percent']}%")
print(f"  Quality: {analysis.data['quality_score']}/100")
print(f"  README: {'✅' if readme.success else '❌'}")
```

---

*Last Updated: 2025-11-08*

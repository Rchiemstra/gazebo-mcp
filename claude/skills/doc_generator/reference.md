# Doc Generator - API Reference

Complete documentation for all doc_generator operations.

---

## Operations

### generate_docstrings

Generate comprehensive docstrings for Python code.

#### Signature

```python
def generate_docstrings(
    file_path: str,
    style: str = "google",
    include_examples: bool = False,
    **kwargs
) -> OperationResult
```

#### Parameters

- **file_path** (str): Path to Python file
- **style** (str): Docstring style - "google", "numpy", or "sphinx"
- **include_examples** (bool): Include usage examples in docstrings

#### Returns

```python
{
    "success": True,
    "data": {
        "file_path": "src/payment.py",
        "functions_documented": 12,
        "classes_documented": 3,
        "coverage_percent": 85.0,
        "docstrings_generated": 15,
        "style_used": "google",
        "preview": "def process_payment(...):\n    \"\"\"Process payment transaction...\"\"\""
    }
}
```

---

### generate_readme

Generate comprehensive README.md from project analysis.

#### Signature

```python
def generate_readme(
    project_path: str,
    include_api: bool = True,
    include_examples: bool = True,
    **kwargs
) -> OperationResult
```

#### Parameters

- **project_path** (str): Path to project root
- **include_api** (bool): Include API reference section
- **include_examples** (bool): Include usage examples

#### Returns

```python
{
    "success": True,
    "data": {
        "readme_path": "README.md",
        "sections_generated": 8,
        "total_lines": 156,
        "api_functions": 25,
        "examples_included": 5
    }
}
```

---

### analyze_documentation

Analyze documentation coverage and quality.

#### Signature

```python
def analyze_documentation(
    project_path: str,
    **kwargs
) -> OperationResult
```

#### Returns

```python
{
    "success": True,
    "data": {
        "total_files": 45,
        "documented_files": 38,
        "coverage_percent": 84.4,
        "missing_docstrings": 23,
        "quality_score": 78,
        "issues": [
            {"file": "api.py", "issue": "Missing return documentation"}
        ]
    }
}
```

---

*Last Updated: 2025-11-08*

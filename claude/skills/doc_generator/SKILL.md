---
name: doc-generator
description: Automated documentation generation from code analysis, including docstrings, READMEs, and documentation coverage analysis
version: 0.1.0
category: development
tags:
  - documentation
  - docstrings
  - readme
  - code-analysis
  - automation
activation: manual
tools:
  - Read
  - Write
dependencies: []
---

# Doc Generator

Automated documentation generation that creates comprehensive docstrings, README files, and analyzes documentation coverage across projects.

---

## When to Use This Skill

Use doc-generator when you need to:

- **Generate docstrings** - Add comprehensive documentation to Python code
- **Create README files** - Auto-generate project documentation
- **Analyze documentation** - Assess documentation coverage and quality
- **Standardize docs** - Ensure consistent documentation style
- **Save time** - Automate repetitive documentation tasks

**Don't use for:**
- Writing prose documentation (use manual editing)
- Non-Python docstrings (currently Python-focused)
- Complex documentation websites (use Sphinx/MkDocs directly)

---

## Quick Start

```python
from skills.doc_generator.operations import generate_docstrings

# Generate docstrings for a Python file
result = generate_docstrings(
    file_path="src/payment.py",
    style="google"
)

if result.success:
    print(f"Generated docstrings for {result.data['functions_documented']} functions")
    print(f"Coverage: {result.data['coverage_percent']}%")
```

---

## Operations

### generate_docstrings
Generate comprehensive docstrings for Python code.

**Returns:** Generated docstrings with coverage metrics

### generate_readme
Generate comprehensive README.md from project analysis.

**Returns:** Complete README with project info, API docs, examples

### analyze_documentation
Analyze existing documentation coverage and quality.

**Returns:** Coverage metrics, missing docs, quality scores

---

## Docstring Styles

Supports 3 major Python docstring conventions:

**Google Style:**
```python
def function(arg1: str, arg2: int) -> bool:
    """Summary line.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Description of return value

    Raises:
        ValueError: When validation fails
    """
```

**NumPy Style:**
```python
def function(arg1, arg2):
    """Summary line.

    Parameters
    ----------
    arg1 : str
        Description of arg1
    arg2 : int
        Description of arg2

    Returns
    -------
    bool
        Description of return value
    """
```

**Sphinx Style:**
```python
def function(arg1, arg2):
    """Summary line.

    :param arg1: Description of arg1
    :type arg1: str
    :param arg2: Description of arg2
    :type arg2: int
    :return: Description of return value
    :rtype: bool
    """
```

---

## README Sections

Auto-generated READMEs include:

- **Project Title & Description**
- **Installation** - Setup instructions
- **Quick Start** - Basic usage example
- **Features** - Key capabilities
- **API Reference** - Public API documentation (optional)
- **Examples** - Usage examples (optional)
- **Contributing** - Contribution guidelines
- **License** - License information

---

## Token Efficiency

**Uses Read and Write tools** - Moderate token usage

**Tip:** Control output size with parameters:
```python
# Minimal: ~500 tokens
generate_readme(project_path=".", include_api=False, include_examples=False)

# Full: ~2000 tokens
generate_readme(project_path=".", include_api=True, include_examples=True)
```

---

## Security

**Safety Level:** Low (uses Read and Write)

**Safe because:**
- Read-only analysis operations
- Write only creates documentation files
- No code execution
- No external network calls

**Audit focus:**
- File write operations
- Paths being documented

See `../SECURITY.md` for details.

---

## Documentation

**For complete API reference:** See `reference.md`
- Full operation signatures
- All parameters and return values
- Docstring style specifications
- README section templates
- Error codes and handling

**For usage examples:** See `examples.md`
- 9 real-world scenarios
- Different docstring styles
- README generation workflows
- Documentation quality gates

---

## Common Patterns

### Pattern 1: Add Docstrings to File
```python
# Generate Google-style docstrings
result = generate_docstrings("src/api.py", style="google")

# Review and apply changes
```

### Pattern 2: Generate Project README
```python
# Full README with API and examples
result = generate_readme(".", include_api=True, include_examples=True)

# Saves to README.md
```

### Pattern 3: Documentation Quality Check
```python
# Analyze current documentation
result = analyze_documentation(".")

if result.data['coverage_percent'] < 80:
    print("Documentation needs improvement")
```

---

## Related Skills

- **code_analysis** - Analyze code structure for documentation
- **test_orchestrator** - Document test suites
- **pr_review_assistant** - Check documentation in PRs

---

## Quick Reference

**Generate docstrings:**
```python
generate_docstrings(file_path, style="google", include_examples=False)
```

**Generate README:**
```python
generate_readme(project_path, include_api=True, include_examples=True)
```

**Analyze documentation:**
```python
analyze_documentation(project_path)
```

---

*Last Updated: 2025-11-08*

---
name: doc-generator
version: 0.1.0
description: Automated documentation generation from code analysis
category: developer-productivity
author: Claude Code Skills
tools:
  - Read
  - Write
  - Glob
dependencies: []
tags: [documentation, docstrings, readme, api-docs, automation]
operations:
  generate_docstrings: "Generate comprehensive docstrings for Python code"
  generate_readme: "Generate comprehensive README.md from project analysis"
  analyze_documentation: "Analyze existing documentation coverage and quality"
---

# Doc Generator

## Overview

Doc Generator is an automated documentation generation system that analyzes code and produces comprehensive, well-structured documentation including docstrings, README files, API documentation, and usage examples.

## Capabilities

### 🔍 Code Analysis
- Extracts functions, classes, and modules
- Identifies parameters, return types, and exceptions
- Detects usage patterns and examples
- Analyzes code complexity and behavior

### 📝 Docstring Generation
- Google, NumPy, and Sphinx style support
- Comprehensive parameter documentation
- Return type and exception documentation
- Usage examples and code snippets

### 📚 README Generation
- Project overview and features
- Installation instructions
- Quick start guides
- API reference
- Usage examples
- Contributing guidelines

### 📖 API Documentation
- Module-level documentation
- Class hierarchy documentation
- Function/method documentation
- Type hints and signatures

## Operations

### generate_docstrings
Generate comprehensive docstrings for Python code.

**Input:**
```python
{
    'file_path': str,           # Path to Python file
    'style': str,               # 'google', 'numpy', or 'sphinx'
    'include_examples': bool    # Include usage examples
}
```

**Output:**
```python
{
    'original_code': str,
    'documented_code': str,
    'docstrings_added': int,
    'coverage_before': float,
    'coverage_after': float
}
```

### generate_readme
Generate comprehensive README.md from project analysis.

**Input:**
```python
{
    'project_path': str,        # Path to project root
    'include_api': bool,        # Include API reference
    'include_examples': bool    # Include usage examples
}
```

**Output:**
```python
{
    'readme_content': str,
    'sections_generated': list,
    'examples_found': int
}
```

### analyze_documentation
Analyze existing documentation coverage and quality.

**Input:**
```python
{
    'project_path': str         # Path to project root
}
```

**Output:**
```python
{
    'coverage_score': float,
    'missing_docstrings': list,
    'quality_issues': list,
    'recommendations': list
}
```

## Integration

Works seamlessly with other skills:
- **test-orchestrator**: Document test patterns
- **refactor-assistant**: Update docs during refactoring
- **pr-review-assistant**: Validate documentation updates

## Usage Example

```python
from doc_generator import generate_docstrings, generate_readme

# Generate docstrings for a file
result = generate_docstrings(
    file_path='myproject/core.py',
    style='google',
    include_examples=True
)

print(f"Added {result['docstrings_added']} docstrings")
print(f"Coverage: {result['coverage_before']:.1f}% -> {result['coverage_after']:.1f}%")

# Generate project README
readme = generate_readme(
    project_path='myproject/',
    include_api=True,
    include_examples=True
)

print(readme['readme_content'])
```

## Quality Metrics

- Documentation coverage percentage
- Docstring completeness score
- Example code quality
- Documentation freshness
- API reference completeness

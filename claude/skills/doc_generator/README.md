# Doc Generator

Automated documentation generation system that analyzes code and produces comprehensive, well-structured documentation including docstrings, README files, and API documentation.

## Overview

Doc Generator transforms undocumented or poorly documented code into professional, comprehensive documentation. It analyzes Python code, identifies missing documentation, generates high-quality docstrings in multiple styles, and creates complete README files for projects.

## Features

### 📊 Documentation Analysis
- **Coverage Calculation**: Measures documentation coverage percentage
- **Quality Assessment**: Evaluates docstring completeness and quality
- **Issue Detection**: Identifies missing docstrings, incomplete parameters, missing return values
- **Multi-dimensional Scoring**: Separate coverage and quality scores
- **Detailed Reports**: Line-by-line issue tracking with suggestions

### 📝 Docstring Generation
- **Multiple Styles**: Google, NumPy, and Sphinx docstring formats
- **Intelligent Generation**: Infers descriptions from function/parameter names
- **Type Hint Integration**: Uses type annotations in docstrings
- **Exception Documentation**: Automatically documents raised exceptions
- **Usage Examples**: Optional code examples in docstrings
- **Parameter Inference**: Smart parameter descriptions based on naming patterns

### 📚 README Generation
- **Project Analysis**: Extracts metadata from setup.py, pyproject.toml, __init__.py
- **Comprehensive Sections**: Overview, features, installation, quick start, API reference, testing, contributing, license
- **Dependency Detection**: Automatically lists project dependencies
- **Example Extraction**: Finds and includes code examples
- **CI/CD Detection**: Identifies testing and CI configuration
- **Module Documentation**: Documents project structure

## Installation

No external dependencies required!

```bash
# The skill is self-contained and uses Python standard library
cd skills/doc_generator
python demo.py  # Run the demonstration
```

## Quick Start

### Analyze Documentation Coverage

```python
from doc_generator import analyze_documentation

# Analyze project documentation
result = analyze_documentation('path/to/project')

print(f"Coverage: {result['coverage_score']:.1f}%")
print(f"Quality: {result['quality_score']:.1f}%")
print(f"Missing docstrings: {len(result['missing_docstrings'])}")

# Review issues
for issue in result['quality_issues']:
    print(f"{issue['severity']}: {issue['description']}")
    print(f"  Location: {issue['location']}:{issue['line_number']}")
    print(f"  Suggestion: {issue['suggestion']}")
```

### Generate Docstrings

```python
from doc_generator import generate_docstrings

# Generate Google-style docstrings
result = generate_docstrings(
    file_path='mymodule.py',
    style='google',
    include_examples=True
)

print(f"Added {result['docstrings_added']} docstrings")
print(f"Coverage: {result['coverage_before']:.1f}% → {result['coverage_after']:.1f}%")

# Save documented code
with open('mymodule_documented.py', 'w') as f:
    f.write(result['documented_code'])
```

### Generate README

```python
from doc_generator import generate_readme

# Generate comprehensive README
result = generate_readme(
    project_path='path/to/project',
    include_api=True,
    include_examples=True
)

print(f"Generated {len(result['sections_generated'])} sections")

# Save README
with open('README.md', 'w') as f:
    f.write(result['readme_content'])
```

## API Reference

### analyze_documentation

Analyzes documentation coverage and quality for a project.

```python
analyze_documentation(project_path: str) -> Dict[str, Any]
```

**Parameters:**
- `project_path`: Path to project root directory

**Returns:**
```python
{
    'coverage_score': float,        # 0-100 percentage
    'quality_score': float,         # 0-100 percentage
    'statistics': {
        'modules_analyzed': int,
        'functions_analyzed': int,
        'classes_analyzed': int,
        'documented_functions': int,
        'documented_classes': int,
    },
    'missing_docstrings': [str],    # List of undocumented items
    'quality_issues': [
        {
            'type': str,            # Issue type
            'severity': str,        # 'high', 'medium', 'low'
            'location': str,        # File::function
            'line_number': int,
            'description': str,
            'suggestion': str
        }
    ],
    'recommendations': [str]         # Actionable recommendations
}
```

**Example:**
```python
result = analyze_documentation('./myproject')

if result['coverage_score'] < 80:
    print("Documentation coverage too low!")
    for item in result['missing_docstrings'][:10]:
        print(f"  Missing: {item}")
```

### generate_docstrings

Generates comprehensive docstrings for a Python file.

```python
generate_docstrings(
    file_path: str,
    style: str = "google",
    include_examples: bool = False
) -> Dict[str, Any]
```

**Parameters:**
- `file_path`: Path to Python file
- `style`: Docstring style - 'google', 'numpy', or 'sphinx'
- `include_examples`: Whether to include usage examples

**Returns:**
```python
{
    'original_code': str,           # Original source
    'documented_code': str,         # With docstrings
    'docstrings_added': int,        # New docstrings
    'docstrings_updated': int,      # Modified docstrings
    'coverage_before': float,       # Before percentage
    'coverage_after': float,        # After percentage
    'generated': [
        {
            'target': str,          # Function/class name
            'line_number': int,
            'original': str,        # Original docstring or None
            'generated': str,       # Generated docstring
            'style': str            # Style used
        }
    ]
}
```

**Example:**
```python
# Generate NumPy-style docstrings with examples
result = generate_docstrings(
    file_path='analytics.py',
    style='numpy',
    include_examples=True
)

# Apply changes
if result['coverage_after'] > result['coverage_before']:
    with open('analytics.py', 'w') as f:
        f.write(result['documented_code'])
    print(f"Improved coverage by {result['coverage_after'] - result['coverage_before']:.1f}%")
```

### generate_readme

Generates comprehensive README.md for a project.

```python
generate_readme(
    project_path: str,
    include_api: bool = True,
    include_examples: bool = True
) -> Dict[str, Any]
```

**Parameters:**
- `project_path`: Path to project root
- `include_api`: Include API reference section
- `include_examples`: Include usage examples

**Returns:**
```python
{
    'readme_content': str,          # Complete README markdown
    'sections_generated': [str],    # Section titles
    'project_info': {
        'name': str,
        'description': str,
        'version': str,
        'dependencies': int
    }
}
```

**Example:**
```python
result = generate_readme(
    project_path='./myproject',
    include_api=True,
    include_examples=True
)

with open('README.md', 'w') as f:
    f.write(result['readme_content'])

print(f"Created README with sections: {', '.join(result['sections_generated'])}")
```

## Docstring Styles

### Google Style

```python
def calculate_metrics(data: list, metric_type: str = 'mean') -> float:
    """Calculate metrics.

    Args:
        data (list): Data to process
        metric_type (str): Metric type

    Returns:
        float: Float result

    Raises:
        ValueError: If input value is invalid

    Example:
        >>> calculate_metrics(data=[1, 2, 3], metric_type='mean')
    """
```

### NumPy Style

```python
def calculate_metrics(data: list, metric_type: str = 'mean') -> float:
    """Calculate metrics.

    Parameters
    ----------
    data : list
        Data to process
    metric_type : str
        Metric type

    Returns
    -------
    float
        Float result

    Raises
    ------
    ValueError
        If input value is invalid
    """
```

### Sphinx Style

```python
def calculate_metrics(data: list, metric_type: str = 'mean') -> float:
    """Calculate metrics.

    :param data: Data to process
    :type data: list
    :param metric_type: Metric type
    :type metric_type: str

    :returns: Float result
    :rtype: float

    :raises ValueError: If input value is invalid
    """
```

## Documentation Quality Scoring

### Coverage Score (0-100)

Percentage of items with docstrings:

- Module-level docstrings
- Function docstrings
- Class docstrings
- Method docstrings

**Formula:**
```
coverage_score = (documented_items / total_items) * 100
```

### Quality Score (0-100)

Based on detected issues:

- **High severity issues**: -5 points each
- **Medium severity issues**: -2 points each
- **Low severity issues**: -1 point each

**Issues detected:**
- Missing docstrings
- Incomplete parameter documentation
- Missing return value documentation
- Missing exception documentation
- Docstrings that are too short

## Use Cases

### 1. Legacy Code Documentation

Add comprehensive documentation to undocumented legacy code:

```python
# Analyze coverage
analysis = analyze_documentation('./legacy_code')
print(f"Current coverage: {analysis['coverage_score']:.1f}%")

# Generate docstrings
for file in analysis['module_info']:
    result = generate_docstrings(
        file_path=file.file_path,
        style='google',
        include_examples=True
    )
    # Save updated file
    with open(file.file_path, 'w') as f:
        f.write(result['documented_code'])

# Verify improvement
new_analysis = analyze_documentation('./legacy_code')
print(f"New coverage: {new_analysis['coverage_score']:.1f}%")
```

### 2. New Project Bootstrap

Create complete documentation for new projects:

```python
# Generate README
readme = generate_readme(
    project_path='./new_project',
    include_api=True,
    include_examples=True
)

with open('./new_project/README.md', 'w') as f:
    f.write(readme['readme_content'])

# Add docstrings to all code
for python_file in Path('./new_project').rglob('*.py'):
    result = generate_docstrings(
        file_path=str(python_file),
        style='google',
        include_examples=True
    )
    with open(python_file, 'w') as f:
        f.write(result['documented_code'])
```

### 3. CI/CD Quality Gate

Enforce documentation standards in CI/CD:

```python
#!/usr/bin/env python3
"""Documentation quality gate for CI/CD."""

import sys
from doc_generator import analyze_documentation

# Analyze project
result = analyze_documentation('.')

print(f"Documentation Coverage: {result['coverage_score']:.1f}%")
print(f"Documentation Quality: {result['quality_score']:.1f}%")

# Define thresholds
COVERAGE_THRESHOLD = 80.0
QUALITY_THRESHOLD = 85.0

# Check thresholds
if result['coverage_score'] < COVERAGE_THRESHOLD:
    print(f"❌ Coverage {result['coverage_score']:.1f}% below threshold {COVERAGE_THRESHOLD}%")
    sys.exit(1)

if result['quality_score'] < QUALITY_THRESHOLD:
    print(f"❌ Quality {result['quality_score']:.1f}% below threshold {QUALITY_THRESHOLD}%")
    sys.exit(1)

print("✅ Documentation quality gate passed")
sys.exit(0)
```

### 4. Pre-commit Hook

Auto-generate docstrings before commit:

```python
#!/usr/bin/env python3
"""Pre-commit hook to ensure documentation."""

import subprocess
from pathlib import Path
from doc_generator import generate_docstrings

# Get staged Python files
result = subprocess.run(
    ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACMR', '*.py'],
    capture_output=True,
    text=True
)

staged_files = result.stdout.strip().split('\n')

for file_path in staged_files:
    if not file_path or not file_path.endswith('.py'):
        continue

    # Generate docstrings
    result = generate_docstrings(
        file_path=file_path,
        style='google',
        include_examples=False
    )

    # Only update if coverage improved
    if result['coverage_after'] > result['coverage_before']:
        with open(file_path, 'w') as f:
            f.write(result['documented_code'])

        # Re-stage the file
        subprocess.run(['git', 'add', file_path])
        print(f"📝 Added docstrings to {file_path}")
```

### 5. Documentation Audit

Regular documentation quality audits:

```python
from doc_generator import analyze_documentation
import json
from datetime import datetime

# Run audit
result = analyze_documentation('.')

# Create audit report
audit_report = {
    'timestamp': datetime.now().isoformat(),
    'coverage_score': result['coverage_score'],
    'quality_score': result['quality_score'],
    'statistics': result['statistics'],
    'issue_count': len(result['quality_issues']),
    'missing_count': len(result['missing_docstrings'])
}

# Save report
with open(f"audit_{datetime.now().strftime('%Y%m%d')}.json", 'w') as f:
    json.dump(audit_report, f, indent=2)

# Track trends
print(f"Coverage: {result['coverage_score']:.1f}%")
print(f"Quality: {result['quality_score']:.1f}%")
print(f"Issues: {len(result['quality_issues'])}")
```

## Integration with Other Skills

### With test-orchestrator

```python
from test_orchestrator import generate_tests
from doc_generator import generate_docstrings

# Generate tests
test_result = generate_tests(source_file='mymodule.py')

# Document the generated tests
doc_result = generate_docstrings(
    file_path=test_result['test_file_path'],
    style='google',
    include_examples=False
)

# Complete test suite with documentation
```

### With refactor-assistant

```python
from refactor_assistant import refactor_code
from doc_generator import generate_docstrings

# Refactor code
refactor_result = refactor_code('legacy.py')

# Update documentation to match refactored code
doc_result = generate_docstrings(
    file_path='legacy.py',
    style='google',
    include_examples=True
)

# Code and docs stay in sync
```

### With pr-review-assistant

```python
from pr_review_assistant import review_pull_request
from doc_generator import analyze_documentation

# Review PR
pr_result = review_pull_request(pr_changes)

# Check documentation for changed files
for file in pr_changes['added'] + pr_changes['modified']:
    if file.endswith('.py'):
        doc_result = analyze_documentation(file)

        # Add documentation check to PR review
        if doc_result['coverage_score'] < 80:
            pr_result['issues'].append({
                'file': file,
                'severity': 'major',
                'description': f"Documentation coverage {doc_result['coverage_score']:.1f}% below 80%",
                'suggestion': "Add docstrings to new/modified functions and classes"
            })
```

### With dependency-guardian

```python
from dependency_guardian import analyze_dependencies
from doc_generator import generate_readme

# Analyze dependencies
dep_result = analyze_dependencies('.')

# Generate README with up-to-date dependency info
readme_result = generate_readme(
    project_path='.',
    include_api=True,
    include_examples=True
)

# README automatically includes current dependencies
```

## Advanced Usage

### Custom Documentation Standards

```python
from doc_generator.core.doc_analyzer import DocumentationAnalyzer

class CustomAnalyzer(DocumentationAnalyzer):
    """Custom analyzer with stricter standards."""

    def _assess_docstring_quality(self, docstring, parameters, return_type, raises):
        """Override to enforce custom standards."""
        # Require docstrings > 100 characters
        if not docstring or len(docstring) < 100:
            return DocQuality.POOR

        # All parameters must be documented
        if parameters and not all(p in docstring.lower() for p in parameters):
            return DocQuality.FAIR

        # Must include examples
        if 'example' not in docstring.lower():
            return DocQuality.GOOD

        return DocQuality.EXCELLENT

# Use custom analyzer
analyzer = CustomAnalyzer()
result = analyzer.analyze_project('.')
```

### Batch Processing

```python
from pathlib import Path
from doc_generator import generate_docstrings
import concurrent.futures

def process_file(file_path):
    """Process single file."""
    result = generate_docstrings(
        file_path=str(file_path),
        style='google',
        include_examples=True
    )

    if result['docstrings_added'] > 0:
        with open(file_path, 'w') as f:
            f.write(result['documented_code'])

    return file_path, result['docstrings_added']

# Process all Python files in parallel
python_files = list(Path('.').rglob('*.py'))

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(process_file, python_files)

# Summary
total_added = sum(count for _, count in results)
print(f"Added {total_added} docstrings across {len(python_files)} files")
```

### Integration with Documentation Generators

```python
from doc_generator import generate_docstrings, analyze_documentation
import subprocess

# Generate docstrings
for file in Path('src').rglob('*.py'):
    generate_docstrings(str(file), style='sphinx')  # Sphinx style for Sphinx docs

# Generate Sphinx documentation
subprocess.run(['sphinx-build', '-b', 'html', 'docs/source', 'docs/build'])

# Or generate pdoc documentation
subprocess.run(['pdoc', '--html', '--output-dir', 'docs', 'src'])
```

## Best Practices

### 1. Choose the Right Style

- **Google**: Best for general Python projects, most readable
- **NumPy**: Best for scientific/data science projects
- **Sphinx**: Best for projects using Sphinx documentation

### 2. Include Examples Selectively

```python
# Public API: Include examples
generate_docstrings('api.py', include_examples=True)

# Internal modules: Skip examples
generate_docstrings('internal.py', include_examples=False)
```

### 3. Review Generated Docstrings

Always review AI-generated content:

```python
result = generate_docstrings('module.py')

# Review changes
print("Generated docstrings:")
for gen in result['generated']:
    print(f"\n{gen['target']}:")
    print(gen['generated'])

# Accept or reject
response = input("Apply changes? (y/n): ")
if response.lower() == 'y':
    with open('module.py', 'w') as f:
        f.write(result['documented_code'])
```

### 4. Maintain Documentation

```python
# Regular audits
result = analyze_documentation('.')

# Track over time
metrics = {
    'date': datetime.now(),
    'coverage': result['coverage_score'],
    'quality': result['quality_score']
}

# Alert on degradation
if result['coverage_score'] < previous_coverage:
    send_alert("Documentation coverage decreased!")
```

### 5. Combine with Type Hints

Doc-generator works best with type hints:

```python
# Good: Type hints provide rich information
def process_data(
    data: List[Dict[str, Any]],
    config: Config,
    verbose: bool = False
) -> ProcessingResult:
    pass

# Generated docstring will include types from hints
```

## Demo

Run the comprehensive demo:

```bash
cd skills/doc_generator
python demo.py
```

The demo shows:
- Documentation coverage analysis
- Docstring generation in all three styles
- README generation
- Style comparison
- Integration patterns
- Real-world workflows

## Limitations

### Current Implementation

- **Python Only**: Only supports Python code analysis
- **Pattern-Based**: Uses naming patterns for descriptions, not semantic understanding
- **No Context**: Doesn't understand business logic or domain-specific terminology
- **Basic Examples**: Generated examples are simple placeholders
- **No Images**: README generation doesn't include diagrams or screenshots

### Recommended Workflow

1. **Generate**: Use doc-generator for initial documentation
2. **Review**: Manually review all generated content
3. **Enhance**: Add domain-specific details and context
4. **Maintain**: Keep documentation updated with code

## Troubleshooting

### "Coverage shows 0% but files have docstrings"

- Check file paths - doc-generator may be analyzing wrong directory
- Verify files are valid Python (no syntax errors)
- Check that docstrings use triple quotes (`"""`)

### "Generated docstrings are too generic"

- Add type hints to provide more information
- Use descriptive parameter names (e.g., `user_email` vs `data`)
- Manually enhance generated docstrings with domain knowledge

### "README generation missing information"

- Ensure project has setup.py or pyproject.toml
- Add __init__.py with docstrings to modules
- Create examples/ directory with sample code

## Future Enhancements

Planned improvements:

- **Multi-language support**: JavaScript, TypeScript, Java, Go, Rust
- **Semantic understanding**: Use LLMs for context-aware descriptions
- **Domain vocabularies**: Technical term databases for specific domains
- **Documentation testing**: Verify examples actually work
- **Change detection**: Update only outdated documentation
- **Image generation**: Create diagrams and flowcharts
- **Interactive mode**: Guide users through documentation creation

## Contributing

Suggestions for improvement:

1. Add support for more docstring styles (reST, epytext)
2. Improve description generation with better NLP
3. Add support for documentation testing (doctest validation)
4. Create IDE plugins for real-time documentation
5. Add support for other languages

## Related Skills

- **test-orchestrator**: Generate tests for documented code
- **refactor-assistant**: Keep docs in sync during refactoring
- **pr-review-assistant**: Enforce documentation in PRs
- **dependency-guardian**: Document dependencies in README

## License

Part of Claude Code Skills framework.

## Support

- Run demo: `python demo.py`
- Check examples: See `examples/` directory
- Review source: Read docstrings in core modules

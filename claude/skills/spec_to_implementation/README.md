# Spec to Implementation

Meta-skill that orchestrates other skills to automatically transform feature specifications into complete, production-ready code with tests and documentation.

## Overview

Spec to Implementation is a meta-skill that serves as an orchestrator for the entire skills ecosystem. It reads specifications in various formats, analyzes requirements, creates detailed implementation plans, and coordinates multiple skills to generate working code, comprehensive tests, and documentation - all automatically.

This is not just a code generator - it's an intelligent system that understands requirements, makes architectural decisions, and produces production-quality implementations that follow best practices.

## Features

### 📋 Specification Parsing
- **Multiple Formats**: Markdown, YAML, JSON, plain text
- **Smart Extraction**: Automatically identifies requirements, constraints, inputs, outputs
- **Structure Recognition**: Understands headers, lists, code blocks
- **Implicit Requirements**: Extracts requirements from natural language descriptions
- **Metadata Capture**: Dependencies, examples, acceptance criteria

### 🎯 Implementation Planning
- **Task Breakdown**: Decomposes features into implementable tasks
- **Complexity Estimation**: Trivial, Simple, Moderate, Complex, Very Complex
- **Dependency Analysis**: Identifies task dependencies and execution order
- **Risk Identification**: Flags ambiguities, missing criteria, complex areas
- **File Planning**: Determines which files to create or modify

### 🔨 Code Generation
- **Scaffolding**: Creates project structure automatically
- **Implementation**: Generates functions, classes, methods from requirements
- **Error Handling**: Adds appropriate error handling patterns
- **Documentation**: Inline comments and docstrings
- **Conventions**: Follows Python naming and style conventions

### 🧪 Quality Assurance
- **Test Generation**: Creates comprehensive test suites (via test-orchestrator)
- **Documentation**: Adds docstrings and README (via doc-generator)
- **Code Review**: Validates quality (via pr-review-assistant)
- **Refactoring**: Checks for code smells (via refactor-assistant)
- **Dependency Check**: Validates dependencies (via dependency-guardian)

### 🔄 Orchestration
- **Multi-Skill Coordination**: Coordinates 6+ different skills
- **Sequential Execution**: Executes tasks in correct order
- **Error Recovery**: Handles failures gracefully
- **Progress Tracking**: Reports on implementation progress
- **Quality Gates**: Validates against configurable thresholds

## Installation

No external dependencies - uses Python standard library!

```bash
cd skills/spec_to_implementation
python demo.py  # Run the demonstration
```

## Quick Start

### Implement from Specification

```python
from spec_to_implementation import implement_from_spec

# Generate complete implementation
result = implement_from_spec(
    spec_file='specs/user_authentication.md',
    output_dir='src/auth',
    quality_threshold=85.0,
    include_tests=True,
    include_docs=True
)

if result['success']:
    print(f"✅ Created {len(result['files_created'])} files")
    print(f"📊 Quality score: {result['quality_score']}/100")
    print(f"🧪 Tests generated: {result['tests_generated']}")
else:
    print("❌ Implementation failed")
    for error in result['errors']:
        print(f"  {error}")
```

### Analyze Specification First

```python
from spec_to_implementation import analyze_spec

# Analyze without implementing
analysis = analyze_spec(spec_file='specs/payment_processing.md')

print(f"Requirements: {len(analysis['requirements'])}")
print(f"Complexity: {analysis['complexity_estimate']}")
print(f"Risks: {len(analysis['risks'])}")

# Review plan
for task in analysis['implementation_plan']['tasks']:
    print(f"  {task['id']}: {task['description']}")
```

## API Reference

### implement_from_spec

Transform specification into working code.

```python
implement_from_spec(
    spec_file: str,
    output_dir: str,
    project_context: Optional[str] = None,
    quality_threshold: float = 85.0,
    include_tests: bool = True,
    include_docs: bool = True
) -> Dict[str, Any]
```

**Parameters:**
- `spec_file`: Path to specification file (markdown, text, YAML, JSON)
- `output_dir`: Directory where code will be generated
- `project_context`: Optional path to existing project for context
- `quality_threshold`: Minimum quality score (0-100) required for success
- `include_tests`: Whether to generate test files
- `include_docs`: Whether to generate documentation

**Returns:**
```python
{
    'success': bool,                # True if implementation successful
    'files_created': [str],         # List of generated file paths
    'tests_generated': int,         # Number of test files created
    'quality_score': float,         # Overall quality score (0-100)
    'implementation_plan': {
        'title': str,
        'tasks': [dict],
        'complexity': str,
        'total_requirements': int
    },
    'validation_results': {
        'quality_score': float,
        'passed_checks': [str],
        'issues': [str]
    },
    'warnings': [str],              # Non-critical warnings
    'errors': [str]                 # Critical errors
}
```

**Example:**
```python
result = implement_from_spec(
    spec_file='specs/email_validator.md',
    output_dir='src/validators',
    quality_threshold=80.0,
    include_tests=True,
    include_docs=True
)

# Check success
if result['success']:
    # Files created
    for file_path in result['files_created']:
        print(f"Created: {file_path}")

    # Quality metrics
    print(f"Quality: {result['quality_score']}/100")

    # Validation
    for check in result['validation_results']['passed_checks']:
        print(f"✓ {check}")
else:
    # Handle failure
    for error in result['errors']:
        print(f"Error: {error}")
```

### analyze_spec

Analyze specification without implementing.

```python
analyze_spec(
    spec_file: str,
    project_context: Optional[str] = None
) -> Dict[str, Any]
```

**Parameters:**
- `spec_file`: Path to specification file
- `project_context`: Optional path to existing project

**Returns:**
```python
{
    'requirements': [
        {
            'id': str,
            'type': str,          # 'functional', 'non_functional', 'constraint'
            'description': str,
            'priority': str       # 'high', 'medium', 'low'
        }
    ],
    'complexity_estimate': str,   # 'trivial', 'simple', 'moderate', 'complex', 'very_complex'
    'implementation_plan': {
        'title': str,
        'tasks': [
            {
                'id': str,
                'type': str,
                'description': str,
                'complexity': str
            }
        ],
        'files_to_create': [str],
        'estimated_complexity': str
    },
    'risks': [str],
    'dependencies': [str]
}
```

**Example:**
```python
# Analyze before implementing
analysis = analyze_spec('specs/recommendation_engine.md')

# Review complexity
if analysis['complexity_estimate'] == 'very_complex':
    print("⚠️  This is a complex feature")
    print("Consider breaking into smaller specs")

# Review risks
for risk in analysis['risks']:
    print(f"Risk: {risk}")

# Decide whether to proceed
if analysis['complexity_estimate'] in ['simple', 'moderate']:
    result = implement_from_spec('specs/recommendation_engine.md', 'src/')
```

## Specification Format

### Markdown Format (Recommended)

```markdown
# Feature Title

Brief description of the feature.

## Requirements

- Must validate user input
- Should provide helpful error messages
- Must handle edge cases gracefully
- Should support bulk operations
- Must be performant (< 100ms)

## Constraints

- Cannot use external APIs
- Must work offline
- Maximum file size: 10MB

## Inputs

- `data` (list): Data to process
- `options` (dict): Configuration options
- `verbose` (bool): Enable verbose logging

## Outputs

- `result` (dict): Processing results
- `errors` (list): List of errors encountered
- `metadata` (dict): Processing metadata

## Examples

\```python
from feature import process

result = process(data=[1, 2, 3], options={'mode': 'fast'})
print(result['status'])
\```

## Dependencies

- requests>=2.28.0
- pandas>=1.5.0
```

### Plain Text Format

```
Feature: User Authentication

The system must authenticate users securely.
It should support multiple authentication methods.
Users must be able to reset passwords.
The system should log all authentication attempts.
```

## Workflow

### 1. Write Specification

Create detailed specification with:
- Clear title and description
- Specific requirements (use "must", "should")
- Constraints and limitations
- Input/output definitions
- Usage examples
- Dependencies

### 2. Analyze Specification

```python
analysis = analyze_spec('spec.md')
```

Review:
- Number of requirements
- Complexity estimate
- Identified risks
- Implementation tasks

### 3. Generate Implementation

```python
result = implement_from_spec(
    spec_file='spec.md',
    output_dir='src/',
    quality_threshold=85.0
)
```

### 4. Review Generated Code

Check:
- File structure makes sense
- Code implements requirements
- Tests cover functionality
- Documentation is clear

### 5. Refine and Complete

- Add business logic details
- Enhance error handling
- Add edge case handling
- Improve test coverage
- Update documentation

### 6. Validate and Deploy

```python
# Run tests
pytest generated_code/tests/

# Check quality
from pr_review_assistant import review_pull_request
review = review_pull_request(...)

# Deploy
git add generated_code/
git commit -m "Implement feature from spec"
```

## Use Cases

### 1. Rapid Prototyping

Quickly turn ideas into working code:

```python
# Write quick spec
spec = """
# Data Exporter

Export data to CSV, JSON, and Excel formats.

Requirements:
- Support CSV export
- Support JSON export
- Support Excel export
- Handle large datasets (> 1M rows)
"""

# Save and implement
Path('spec.md').write_text(spec)
result = implement_from_spec('spec.md', 'prototypes/data_exporter/')

# Working prototype ready in seconds!
```

### 2. Boilerplate Generation

Generate project templates:

```python
result = implement_from_spec(
    spec_file='templates/rest_api_spec.md',
    output_dir=f'projects/{project_name}/',
    include_tests=True,
    include_docs=True
)

# Complete REST API structure generated
```

### 3. Specification Validation

Test if spec is complete and implementable:

```python
analysis = analyze_spec('draft_spec.md')

# Check for issues
if analysis['risks']:
    print("Specification has issues:")
    for risk in analysis['risks']:
        print(f"  - {risk}")

# Check complexity
if analysis['complexity_estimate'] == 'very_complex':
    print("Consider simplifying or breaking into smaller features")
```

### 4. Learning Tool

Understand how specifications map to code:

```python
# Learn implementation patterns
result = implement_from_spec('learning/sorting_algorithm.md', 'examples/')

# See how requirements become code
for requirement in analysis['requirements']:
    print(f"Requirement: {requirement['description']}")
    # See corresponding code in generated files
```

### 5. Team Standardization

Ensure consistent implementations across team:

```python
# Standard template
TEAM_SPEC_TEMPLATE = """
# {feature_name}

{description}

## Requirements
{requirements}

## Quality Standards
- Test coverage > 80%
- Documentation complete
- No code smells
- Passes code review
"""

# Everyone uses same template
result = implement_from_spec(
    spec_file='team_specs/feature.md',
    quality_threshold=90.0  # Team standard
)
```

## Integration with Skills Ecosystem

Spec to Implementation orchestrates all other skills:

### Code Search Integration

```python
# Before generating, search for similar implementations
from code_search import search_symbol

similar = search_symbol(
    project_path='.',
    symbol_name='*validator*',
    symbol_type='function'
)

# Use patterns from similar code
```

### Test Orchestrator Integration

```python
# Automatically generates tests using test-orchestrator
# Sets target coverage based on quality threshold
# Generates test fixtures and assertions
```

### Doc Generator Integration

```python
# Automatically adds docstrings using doc-generator
# Generates README with API reference
# Keeps docs in sync with code
```

### Refactor Assistant Integration

```python
# Checks generated code for smells
# Suggests improvements
# Can auto-refactor if configured
```

### PR Review Assistant Integration

```python
# Validates generated code meets standards
# Checks for security issues
# Ensures best practices followed
```

### Dependency Guardian Integration

```python
# Validates dependencies from spec
# Checks for vulnerabilities
# Suggests safer alternatives
```

## Advanced Usage

### Custom Code Templates

```python
from spec_to_implementation.core.orchestrator import ImplementationOrchestrator

class CustomOrchestrator(ImplementationOrchestrator):
    def _generate_implementation_code(self, requirement, spec):
        """Override to use custom templates."""
        # Your custom code generation logic
        return custom_template.render(requirement=requirement)

# Use custom orchestrator
orchestrator = CustomOrchestrator()
result = orchestrator.implement(...)
```

### Quality Threshold Configuration

```python
# Strict for production
result = implement_from_spec(
    spec_file='spec.md',
    output_dir='src/',
    quality_threshold=95.0,  # Very strict
    include_tests=True,
    include_docs=True
)

# Relaxed for prototypes
result = implement_from_spec(
    spec_file='spec.md',
    output_dir='prototypes/',
    quality_threshold=60.0,  # Quick and dirty
    include_tests=False,
    include_docs=False
)
```

### Batch Processing

```python
from pathlib import Path

# Implement all specs in directory
specs_dir = Path('specs/')
for spec_file in specs_dir.glob('*.md'):
    print(f"Implementing {spec_file.name}")

    result = implement_from_spec(
        spec_file=str(spec_file),
        output_dir=f'src/{spec_file.stem}/',
        quality_threshold=85.0
    )

    if result['success']:
        print(f"✅ {spec_file.name} implemented")
    else:
        print(f"❌ {spec_file.name} failed")
```

### CI/CD Integration

```yaml
# .github/workflows/implement-specs.yml
name: Auto-implement Specifications

on:
  push:
    paths:
      - 'specs/**.md'

jobs:
  implement:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Implement specifications
        run: |
          for spec in specs/*.md; do
            python -c "
            from spec_to_implementation import implement_from_spec
            result = implement_from_spec(
                spec_file='$spec',
                output_dir='src/',
                quality_threshold=85.0
            )
            if not result['success']:
                exit(1)
            "
          done

      - name: Run tests
        run: pytest

      - name: Create PR
        uses: peter-evans/create-pull-request@v4
        with:
          title: "Auto-implemented from spec"
```

## Best Practices

### 1. Write Clear Specifications

**Good:**
```markdown
## Requirements

- Must validate email format using RFC 5322 standard
- Must check for common typos in domain names
- Must timeout DNS lookups after 2 seconds
- Should suggest corrections for detected typos
```

**Bad:**
```markdown
## Requirements

- Validate emails somehow
- Maybe check typos
- Be fast
```

### 2. Include Examples

```markdown
## Examples

\```python
validator = EmailValidator()
result = validator.validate('user@example.com')

assert result.is_valid == True
assert result.errors == []
\```
```

### 3. Specify Constraints

```markdown
## Constraints

- No external API calls for basic validation
- Must work offline
- Maximum response time: 100ms
- Support Python 3.8+
```

### 4. Define Clear Inputs/Outputs

```markdown
## Inputs

- `email` (str): Email address to validate (required)
- `check_dns` (bool): Whether to verify DNS (default: False)
- `timeout` (int): DNS lookup timeout in seconds (default: 2)

## Outputs

- `is_valid` (bool): Whether email is valid
- `errors` (List[str]): List of validation errors
- `suggestions` (List[str]): Suggested corrections
```

### 5. Review Generated Code

Always review before committing:
- Verify logic correctness
- Add domain-specific details
- Enhance error messages
- Add logging where needed
- Improve test coverage

## Demo

Run the comprehensive demo:

```bash
cd skills/spec_to_implementation
python demo.py
```

The demo shows:
- Specification parsing and analysis
- Implementation plan generation
- Code scaffolding
- Requirement implementation
- Test and documentation generation
- Quality validation
- Complete workflow example

## Limitations

### Current Implementation

- **Python Only**: Currently generates Python code only
- **Template-Based**: Uses basic templates, not advanced AI generation
- **Limited Context**: Doesn't understand complex business logic
- **Basic Validation**: Quality validation is simplified
- **No Interactive Mode**: Can't ask clarifying questions

### Recommended Workflow

1. **Use for Scaffolding**: Great for project structure and boilerplate
2. **Review and Refine**: Always review and enhance generated code
3. **Add Business Logic**: Fill in domain-specific implementation details
4. **Enhance Tests**: Add edge cases and integration tests
5. **Update Docs**: Add examples and usage guides

## Future Enhancements

Planned improvements:

- **Multi-Language Support**: Generate JavaScript, TypeScript, Java, Go
- **AI-Powered Generation**: Use LLMs for smarter code generation
- **Interactive Mode**: Ask clarifying questions about ambiguous requirements
- **Database Schema Generation**: Create database schemas from specs
- **API Generation**: Generate complete REST/GraphQL APIs
- **UI Generation**: Create basic UI from specs
- **Test Data Generation**: Generate realistic test data
- **Performance Optimization**: Auto-optimize generated code

## Troubleshooting

### "No files created"

- Check specification file exists and is readable
- Verify output directory is writable
- Check for errors in `result['errors']`

### "Quality score too low"

- Review `validation_results` for specific issues
- Lower `quality_threshold` for prototypes
- Add more details to specification
- Review generated code and enhance manually

### "Specification parsing failed"

- Check markdown formatting
- Ensure sections have headers (##)
- Use lists for requirements (- or 1.)
- Include clear requirement statements

### "Implementation doesn't match requirements"

- Make requirements more specific
- Add examples to specification
- Include acceptance criteria
- Review and refine generated code manually

## Contributing

Suggestions for improvement:

1. Add support for more programming languages
2. Create specification templates for common patterns
3. Improve code generation templates
4. Add more validation rules
5. Create IDE plugins for specification editing

## Related Skills

- **All Skills**: This meta-skill orchestrates the entire ecosystem
- **test-orchestrator**: Test generation
- **doc-generator**: Documentation generation
- **refactor-assistant**: Code quality checks
- **pr-review-assistant**: Quality validation
- **code-search**: Finding similar implementations
- **dependency-guardian**: Dependency validation

## License

Part of Claude Code Skills framework.

## Support

- Run demo: `python demo.py`
- Example specs: See `examples/` directory
- Review source: Read code in `core/` modules

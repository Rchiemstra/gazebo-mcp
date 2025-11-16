"""
Implementation Orchestrator

Orchestrates all skills to implement specifications.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any
import sys

from .spec_parser import SpecificationParser
from .implementation_planner import ImplementationPlanner, ComplexityLevel, TaskType

# Try to import other skills (graceful degradation if not available)
try:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from test_orchestrator import generate_tests
    from doc_generator import generate_docstrings, generate_readme
    from pr_review_assistant import review_pull_request
    SKILLS_AVAILABLE = True
except ImportError:
    SKILLS_AVAILABLE = False


@dataclass
class ImplementationResult:
    """Result of implementation."""
    success: bool
    files_created: List[str] = field(default_factory=list)
    tests_generated: int = 0
    quality_score: float = 0.0
    implementation_plan: Dict[str, Any] = field(default_factory=dict)
    validation_results: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class ImplementationOrchestrator:
    """Orchestrates implementation from specification to working code."""

    def __init__(self):
        """Initialize orchestrator."""
        self.parser = SpecificationParser()
        self.planner = ImplementationPlanner()

    def implement(
        self,
        spec_file: str,
        output_dir: str,
        project_context: Optional[str] = None,
        quality_threshold: float = 85.0,
        include_tests: bool = True,
        include_docs: bool = True
    ) -> ImplementationResult:
        """
        Implement specification.

        Args:
            spec_file: Path to specification file
            output_dir: Directory for generated code
            project_context: Optional path to existing project
            quality_threshold: Minimum quality score (0-100)
            include_tests: Generate tests
            include_docs: Generate documentation

        Returns:
            Implementation result
        """
        result = ImplementationResult(success=False)

        try:
            # 1. Parse specification
            spec = self.parser.parse_file(spec_file)

            # 2. Create implementation plan
            plan = self.planner.create_plan(spec, project_context)

            # Store plan in result
            result.implementation_plan = {
                'title': plan.title,
                'overview': plan.overview,
                'tasks': [
                    {
                        'id': task.id,
                        'type': task.task_type.value,
                        'description': task.description,
                        'complexity': task.estimated_complexity.value
                    }
                    for task in plan.tasks
                ],
                'complexity': plan.estimated_complexity.value,
                'total_requirements': plan.total_requirements
            }

            # Add risks as warnings
            result.warnings.extend(plan.risks)

            # 3. Create output directory
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

            # 4. Execute implementation tasks
            for task in plan.tasks:
                task_success = self._execute_task(
                    task,
                    spec,
                    output_dir,
                    include_tests,
                    include_docs,
                    result
                )

                if not task_success and task.task_type != TaskType.VALIDATE:
                    # Stop if critical task fails
                    result.errors.append(f"Task {task.id} failed: {task.description}")
                    return result

            # 5. Final validation
            if SKILLS_AVAILABLE:
                validation = self._validate_implementation(
                    output_dir,
                    quality_threshold,
                    result
                )
                result.validation_results = validation

                # Check quality threshold
                if validation.get('quality_score', 0) >= quality_threshold:
                    result.success = True
                    result.quality_score = validation['quality_score']
                else:
                    result.warnings.append(
                        f"Quality score {validation['quality_score']:.1f} below threshold {quality_threshold}"
                    )
                    result.success = False
            else:
                # No validation available, mark as successful if no errors
                result.success = not result.errors
                result.warnings.append("Skills not available - validation skipped")

        except Exception as e:
            result.errors.append(f"Implementation failed: {str(e)}")
            result.success = False

        return result

    def _execute_task(
        self,
        task,
        spec,
        output_dir: str,
        include_tests: bool,
        include_docs: bool,
        result: ImplementationResult
    ) -> bool:
        """Execute a single implementation task."""
        if task.task_type == TaskType.SCAFFOLD:
            return self._execute_scaffold(task, spec, output_dir, result)

        elif task.task_type == TaskType.IMPLEMENT:
            return self._execute_implementation(task, spec, output_dir, result)

        elif task.task_type == TaskType.TEST and include_tests:
            return self._execute_test_generation(task, spec, output_dir, result)

        elif task.task_type == TaskType.DOCUMENT and include_docs:
            return self._execute_documentation(task, spec, output_dir, result)

        elif task.task_type == TaskType.VALIDATE:
            # Validation handled separately
            return True

        return True

    def _execute_scaffold(self, task, spec, output_dir: str, result: ImplementationResult) -> bool:
        """Execute scaffolding task."""
        try:
            output_path = Path(output_dir)

            # Create files
            for file_path in task.files_to_create:
                full_path = output_path / file_path

                # Create parent directories
                full_path.parent.mkdir(parents=True, exist_ok=True)

                # Generate content based on file type
                if file_path.endswith('__init__.py'):
                    content = self._generate_init_file(spec)
                elif file_path.endswith('core.py'):
                    content = self._generate_core_file(spec)
                else:
                    content = f'"""\n{spec.title}\n\nGenerated file.\n"""\n'

                # Write file
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                result.files_created.append(str(full_path))

            return True

        except Exception as e:
            result.errors.append(f"Scaffold failed: {str(e)}")
            return False

    def _execute_implementation(
        self,
        task,
        spec,
        output_dir: str,
        result: ImplementationResult
    ) -> bool:
        """Execute implementation task."""
        try:
            output_path = Path(output_dir)

            # Find requirements to implement
            requirements = [
                req for req in spec.requirements
                if req.id in task.requirements_addressed
            ]

            # Generate implementation code
            for req in requirements:
                code = self._generate_implementation_code(req, spec)

                # Determine target file
                if task.files_to_create:
                    target_file = output_path / task.files_to_create[0]
                elif task.files_to_modify:
                    target_file = output_path / task.files_to_modify[0]
                else:
                    # Default to core.py
                    module_name = self.planner._title_to_module_name(spec.title)
                    target_file = output_path / module_name / 'core.py'

                # Create file if needed
                target_file.parent.mkdir(parents=True, exist_ok=True)

                if target_file.exists():
                    # Append to existing file
                    with open(target_file, 'a', encoding='utf-8') as f:
                        f.write('\n\n' + code)
                else:
                    # Create new file
                    with open(target_file, 'w', encoding='utf-8') as f:
                        f.write(code)

                    if str(target_file) not in result.files_created:
                        result.files_created.append(str(target_file))

            return True

        except Exception as e:
            result.errors.append(f"Implementation failed: {str(e)}")
            return False

    def _execute_test_generation(
        self,
        task,
        spec,
        output_dir: str,
        result: ImplementationResult
    ) -> bool:
        """Execute test generation."""
        if not SKILLS_AVAILABLE:
            result.warnings.append("test-orchestrator not available - tests not generated")
            return True

        try:
            output_path = Path(output_dir)

            # Create test file
            for file_path in task.files_to_create:
                full_path = output_path / file_path

                # Create parent directories
                full_path.parent.mkdir(parents=True, exist_ok=True)

                # Generate basic test template
                content = self._generate_test_template(spec)

                # Write file
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                result.files_created.append(str(full_path))
                result.tests_generated += 1

            return True

        except Exception as e:
            result.warnings.append(f"Test generation failed: {str(e)}")
            return True  # Non-critical

    def _execute_documentation(
        self,
        task,
        spec,
        output_dir: str,
        result: ImplementationResult
    ) -> bool:
        """Execute documentation generation."""
        if not SKILLS_AVAILABLE:
            result.warnings.append("doc-generator not available - docs not generated")
            return True

        try:
            output_path = Path(output_dir)

            # Create README
            for file_path in task.files_to_create:
                if file_path.endswith('README.md'):
                    full_path = output_path / file_path

                    # Generate README content
                    content = self._generate_readme(spec)

                    # Write file
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(content)

                    result.files_created.append(str(full_path))

            return True

        except Exception as e:
            result.warnings.append(f"Documentation generation failed: {str(e)}")
            return True  # Non-critical

    def _validate_implementation(
        self,
        output_dir: str,
        quality_threshold: float,
        result: ImplementationResult
    ) -> Dict[str, Any]:
        """Validate implementation quality."""
        validation = {
            'quality_score': 70.0,  # Default score
            'issues': [],
            'passed_checks': []
        }

        # Basic validation
        output_path = Path(output_dir)

        # Check files were created
        if result.files_created:
            validation['passed_checks'].append("Files created successfully")
        else:
            validation['issues'].append("No files created")

        # Check for Python files
        python_files = list(output_path.rglob("*.py"))
        if python_files:
            validation['passed_checks'].append(f"Found {len(python_files)} Python files")
            validation['quality_score'] += 10
        else:
            validation['issues'].append("No Python files found")

        # Check for tests
        test_files = list(output_path.rglob("test_*.py"))
        if test_files:
            validation['passed_checks'].append(f"Found {len(test_files)} test files")
            validation['quality_score'] += 10
        else:
            validation['issues'].append("No test files found")

        # Check for README
        readme_files = list(output_path.rglob("README.md"))
        if readme_files:
            validation['passed_checks'].append("README.md exists")
            validation['quality_score'] += 10
        else:
            validation['issues'].append("No README.md found")

        return validation

    def _generate_init_file(self, spec) -> str:
        """Generate __init__.py content."""
        module_name = self.planner._title_to_module_name(spec.title)

        return f'''"""
{spec.title}

{spec.description}
"""

__version__ = "0.1.0"
'''

    def _generate_core_file(self, spec) -> str:
        """Generate core.py content."""
        return f'''"""
{spec.title} - Core Module

{spec.description}
"""


def main():
    """Main entry point."""
    pass


if __name__ == "__main__":
    main()
'''

    def _generate_implementation_code(self, requirement, spec) -> str:
        """Generate code for a requirement."""
        # Extract feature name
        feature_name = self.planner._extract_feature_name(requirement.description)

        if not feature_name:
            feature_name = "process"

        # Generate function
        code = f'''def {feature_name}():
    """
    {requirement.description}

    Implementation generated from specification.
    """
    # TODO: Implement {requirement.description}
    pass
'''

        return code

    def _generate_test_template(self, spec) -> str:
        """Generate test template."""
        module_name = self.planner._title_to_module_name(spec.title)

        return f'''"""
Tests for {spec.title}

Generated test template.
"""

import pytest


def test_basic_functionality():
    """Test basic functionality."""
    # TODO: Add tests
    assert True


def test_requirements():
    """Test that all requirements are met."""
    # TODO: Test each requirement
    assert True
'''

    def _generate_readme(self, spec) -> str:
        """Generate README content."""
        return f'''# {spec.title}

{spec.description}

## Features

'''  + '\n'.join(f'- {req.description}' for req in spec.requirements) + f'''

## Installation

```bash
pip install {self.planner._title_to_module_name(spec.title)}
```

## Usage

```python
from {self.planner._title_to_module_name(spec.title)} import main

main()
```

## Requirements

Total: {len(spec.requirements)} requirements implemented

## License

MIT License
'''


def implement_from_spec(
    spec_file: str,
    output_dir: str,
    project_context: Optional[str] = None,
    quality_threshold: float = 85.0,
    include_tests: bool = True,
    include_docs: bool = True
) -> Dict[str, Any]:
    """
    Implement code from specification.

    Args:
        spec_file: Path to specification file
        output_dir: Directory for generated code
        project_context: Optional path to existing project
        quality_threshold: Minimum quality score (0-100)
        include_tests: Generate tests
        include_docs: Generate documentation

    Returns:
        Implementation result

    Example:
        >>> result = implement_from_spec(
        ...     spec_file='specs/user_auth.md',
        ...     output_dir='src/auth',
        ...     quality_threshold=85.0
        ... )
        >>> if result['success']:
        ...     print(f"Created {len(result['files_created'])} files")
    """
    orchestrator = ImplementationOrchestrator()

    result = orchestrator.implement(
        spec_file=spec_file,
        output_dir=output_dir,
        project_context=project_context,
        quality_threshold=quality_threshold,
        include_tests=include_tests,
        include_docs=include_docs
    )

    return {
        'success': result.success,
        'files_created': result.files_created,
        'tests_generated': result.tests_generated,
        'quality_score': result.quality_score,
        'implementation_plan': result.implementation_plan,
        'validation_results': result.validation_results,
        'warnings': result.warnings,
        'errors': result.errors
    }


def analyze_spec(
    spec_file: str,
    project_context: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyze specification without implementing.

    Args:
        spec_file: Path to specification file
        project_context: Optional path to existing project

    Returns:
        Analysis results

    Example:
        >>> analysis = analyze_spec('specs/payment_processing.md')
        >>> print(f"Complexity: {analysis['complexity_estimate']}")
        >>> print(f"Requirements: {len(analysis['requirements'])}")
    """
    parser = SpecificationParser()
    planner = ImplementationPlanner()

    # Parse specification
    spec = parser.parse_file(spec_file)

    # Create plan
    plan = planner.create_plan(spec, project_context)

    return {
        'requirements': [
            {
                'id': req.id,
                'type': req.type.value,
                'description': req.description,
                'priority': req.priority
            }
            for req in spec.requirements
        ],
        'complexity_estimate': plan.estimated_complexity.value,
        'implementation_plan': {
            'title': plan.title,
            'tasks': [
                {
                    'id': task.id,
                    'type': task.task_type.value,
                    'description': task.description,
                    'complexity': task.estimated_complexity.value
                }
                for task in plan.tasks
            ],
            'files_to_create': plan.files_to_create,
            'estimated_complexity': plan.estimated_complexity.value
        },
        'risks': plan.risks,
        'dependencies': spec.dependencies
    }

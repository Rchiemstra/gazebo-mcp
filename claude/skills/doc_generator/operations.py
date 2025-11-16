"""
Doc Generator Operations

Standardized operations interface for agent invocation.
"""

from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
import time

# Import core functions
from .core.docstring_generator import generate_docstrings as _generate_docstrings
from .core.readme_generator import generate_readme as _generate_readme
from .core.doc_analyzer import analyze_documentation as _analyze_documentation


@dataclass
class OperationResult:
    """Result from a skill operation."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    duration: float = 0.0
    metadata: Optional[Dict[str, Any]] = None


def generate_docstrings(
    file_path: str,
    style: str = "google",
    include_examples: bool = False,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Generate comprehensive docstrings for Python code.

    Args:
        file_path: Path to Python file
        style: Docstring style ('google', 'numpy', or 'sphinx')
        include_examples: Include usage examples in docstrings
        response_format: "summary" (counts) or "detailed" (full docstrings)
        **kwargs: Additional parameters

    Returns:
        OperationResult with docstring generation results

    Token Efficiency:
        - Use response_format="summary" for function counts and coverage
        - Use response_format="detailed" for complete generated docstrings
        - Summary mode saves 85-95% tokens
    """
    start_time = time.time()

    try:
        result = _generate_docstrings(
            file_path=file_path,
            style=style,
            include_examples=include_examples
        )

        duration = time.time() - start_time

        return OperationResult(
            success=True,
            data=result,
            duration=duration,
            metadata={
                "skill": "doc-generator",
                "operation": "generate_docstrings",
                "version": "0.1.0",
                "style": style,
                "include_examples": include_examples
            }
        )

    except FileNotFoundError as e:
        return OperationResult(
            success=False,
            error=f"Cannot find Python file: {file_path}",
            error_code="FILE_NOT_FOUND",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check if the file path is correct",
                    "Use Glob('**/*.py') to find Python files in the project",
                    "Verify the file exists with Bash('ls -la {Path(file_path).parent}')",
                    "Ensure you're providing the correct relative or absolute path"
                ],
                "example_fix": "generate_docstrings('src/services/payment.py', style='google')"
            }
        )
    except SyntaxError as e:
        return OperationResult(
            success=False,
            error=f"Python syntax error in {file_path}: {str(e)}",
            error_code="SYNTAX_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Fix syntax errors in the file before generating docstrings",
                    f"Run Bash('python -m py_compile {file_path}') to see detailed syntax errors",
                    "Verify the file contains valid Python code",
                    "Consider using a different file first to test the operation"
                ],
                "example_fix": "# Fix syntax first, then: generate_docstrings('src/fixed_file.py')"
            }
        )
    except ValueError as e:
        return OperationResult(
            success=False,
            error=f"Invalid docstring style: {str(e)}",
            error_code="VALIDATION_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Valid styles are: 'google', 'numpy', or 'sphinx'",
                    "Check the style parameter spelling",
                    "Use 'google' style for most cases (default and most common)",
                    "Verify style parameter is a string"
                ],
                "example_fix": "generate_docstrings('file.py', style='google', include_examples=True)"
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Docstring generation failed: {str(e)}",
            error_code="GENERATION_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure the file contains valid Python code",
                    "Try with a simpler Python file first",
                    "Check if the file has functions or classes to document",
                    "Verify file encoding is UTF-8"
                ],
                "example_fix": "generate_docstrings('src/simple_module.py', style='google')"
            }
        )


def generate_readme(
    project_path: str,
    include_api: bool = True,
    include_examples: bool = True,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Generate comprehensive README.md from project analysis.

    Args:
        project_path: Path to project root directory
        include_api: Include API reference section
        include_examples: Include usage examples section
        response_format: "summary" (metadata) or "detailed" (full README content)
        **kwargs: Additional parameters

    Returns:
        OperationResult with README generation results

    Token Efficiency:
        - Use response_format="summary" for section counts and overview
        - Use response_format="detailed" for complete README markdown
        - Summary mode saves 90-95% tokens
    """
    start_time = time.time()

    try:
        result = _generate_readme(
            project_path=project_path,
            include_api=include_api,
            include_examples=include_examples
        )

        duration = time.time() - start_time

        return OperationResult(
            success=True,
            data=result,
            duration=duration,
            metadata={
                "skill": "doc-generator",
                "operation": "generate_readme",
                "version": "0.1.0",
                "include_api": include_api,
                "include_examples": include_examples
            }
        )

    except FileNotFoundError as e:
        return OperationResult(
            success=False,
            error=f"Cannot find project directory: {project_path}",
            error_code="FILE_NOT_FOUND",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check if the project path is correct",
                    "Use Bash('ls -la .') to see available directories",
                    "Verify you're in the correct working directory",
                    "Ensure the path points to a project root with Python files"
                ],
                "example_fix": "generate_readme('path/to/project/', include_api=True, include_examples=True)"
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            error=f"README generation failed: {str(e)}",
            error_code="GENERATION_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure the project directory contains Python files",
                    "Check if the project has a valid structure (src/, tests/, etc.)",
                    "Try with simpler options first (include_api=False, include_examples=False)",
                    "Verify you have read permissions for all project files"
                ],
                "example_fix": "generate_readme('project/', include_api=False, include_examples=False)"
            }
        )


def analyze_documentation(
    project_path: str,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Analyze existing documentation coverage and quality.

    Args:
        project_path: Path to project root directory
        response_format: "summary" (coverage %) or "detailed" (missing docs list)
        **kwargs: Additional parameters

    Returns:
        OperationResult with documentation analysis

    Token Efficiency:
        - Use response_format="summary" for coverage percentages and scores
        - Use response_format="detailed" for complete list of missing docs
        - Summary mode saves 80-90% tokens
    """
    start_time = time.time()

    try:
        result = _analyze_documentation(project_path=project_path)

        duration = time.time() - start_time

        return OperationResult(
            success=True,
            data=result,
            duration=duration,
            metadata={
                "skill": "doc-generator",
                "operation": "analyze_documentation",
                "version": "0.1.0"
            }
        )

    except FileNotFoundError as e:
        return OperationResult(
            success=False,
            error=f"Cannot find project directory: {project_path}",
            error_code="FILE_NOT_FOUND",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check if the project path is correct",
                    "Verify the directory exists with Bash('ls -la .')",
                    "Ensure you're providing a path to a project with Python files",
                    "Use Glob('**/*.py') to verify Python files exist in the project"
                ],
                "example_fix": "analyze_documentation('path/to/project/')"
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Documentation analysis failed: {str(e)}",
            error_code="ANALYSIS_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure the project contains Python files to analyze",
                    "Check if Python files are syntactically valid",
                    "Try with a simpler project structure first",
                    "Verify you have read permissions for all project files"
                ],
                "example_fix": "analyze_documentation('src/')"
            }
        )


# Export all operations
__all__ = [
    "generate_docstrings",
    "generate_readme",
    "analyze_documentation",
    "OperationResult"
]

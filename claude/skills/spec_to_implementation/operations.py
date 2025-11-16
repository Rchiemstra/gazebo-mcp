"""
Spec to Implementation Operations

Standardized operations interface for agent invocation.
"""

from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
import time

# Import core functions
from .core.orchestrator import (
    implement_from_spec as _implement_from_spec,
    analyze_spec as _analyze_spec
)


@dataclass
class OperationResult:
    """Result from a skill operation."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    duration: float = 0.0
    metadata: Optional[Dict[str, Any]] = None


def implement_from_spec(
    spec_file: str,
    output_dir: str,
    project_context: Optional[str] = None,
    quality_threshold: float = 85.0,
    include_tests: bool = True,
    include_docs: bool = True,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Transform a specification into working, tested code.

    Args:
        spec_file: Path to specification file
        output_dir: Directory for generated code
        project_context: Optional path to existing project for context
        quality_threshold: Minimum quality score (0-100, default: 85.0)
        include_tests: Generate tests using test-orchestrator (default: True)
        include_docs: Generate documentation (default: True)
        response_format: "summary" (file counts) or "detailed" (full implementation report)
        **kwargs: Additional parameters

    Returns:
        OperationResult with implementation results

    Token Efficiency:
        - Use response_format="summary" for file counts and quality score
        - Use response_format="detailed" for complete implementation details
        - Summary mode saves 85-95% tokens
        include_docs: Generate documentation (default: True)
        **kwargs: Additional parameters

    Returns:
        OperationResult with implementation results
    """
    start_time = time.time()

    try:
        result = _implement_from_spec(
            spec_file=spec_file,
            output_dir=output_dir,
            project_context=project_context,
            quality_threshold=quality_threshold,
            include_tests=include_tests,
            include_docs=include_docs
        )

        duration = time.time() - start_time

        return OperationResult(
            success=result.get('success', False),
            data=result,
            duration=duration,
            metadata={
                "skill": "spec-to-implementation",
                "operation": "implement_from_spec",
                "version": "0.1.0",
                "quality_threshold": quality_threshold,
                "include_tests": include_tests,
                "include_docs": include_docs
            }
        )

    except FileNotFoundError as e:
        return OperationResult(
            success=False,
            error=f"Cannot find specification file: {spec_file}",
            error_code="FILE_NOT_FOUND",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check if the spec_file path is correct",
                    "Use Glob('**/*.md') to find markdown specification files",
                    "Verify the specification file exists with Bash('ls -la {Path(spec_file).parent}')",
                    "Ensure the file is in markdown format (.md extension)"
                ],
                "example_fix": "implement_from_spec('specs/feature.md', 'output/', include_tests=True)"
            }
        )
    except ValueError as e:
        return OperationResult(
            success=False,
            error=f"Invalid specification or parameters: {str(e)}",
            error_code="VALIDATION_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check if the specification file has required sections",
                    "Verify quality_threshold is between 0 and 100",
                    "Ensure output_dir is a valid directory path",
                    "Try analyze_spec first to validate the specification"
                ],
                "example_fix": "implement_from_spec('spec.md', 'output/', quality_threshold=85.0)"
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Implementation failed: {str(e)}",
            error_code="IMPLEMENTATION_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure the specification is in valid markdown format",
                    "Try with simpler options first (include_tests=False, include_docs=False)",
                    "Check if project_context (if provided) is a valid project path",
                    "Verify output_dir is writable with Bash('ls -la {output_dir}')"
                ],
                "example_fix": "implement_from_spec('spec.md', 'out/', include_tests=False, include_docs=False)"
            }
        )


def analyze_spec(
    spec_file: str,
    project_context: Optional[str] = None,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Analyze a specification without implementing it.

    Args:
        spec_file: Path to specification file
        project_context: Optional path to existing project for context
        response_format: "summary" (overview) or "detailed" (full analysis)
        **kwargs: Additional parameters

    Returns:
        OperationResult with specification analysis

    Token Efficiency:
        - Use response_format="summary" for validation results and complexity
        - Use response_format="detailed" for complete gap analysis
        - Summary mode saves 80-90% tokens

    Returns:
        OperationResult with analysis results
    """
    start_time = time.time()

    try:
        result = _analyze_spec(
            spec_file=spec_file,
            project_context=project_context
        )

        duration = time.time() - start_time

        return OperationResult(
            success=True,
            data=result,
            duration=duration,
            metadata={
                "skill": "spec-to-implementation",
                "operation": "analyze_spec",
                "version": "0.1.0"
            }
        )

    except FileNotFoundError as e:
        return OperationResult(
            success=False,
            error=f"Cannot find specification file: {spec_file}",
            error_code="FILE_NOT_FOUND",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check if the spec_file path is correct",
                    "Use Glob('**/*.md') to find markdown files",
                    "Verify the file exists with Bash('ls -la {Path(spec_file).parent}')",
                    "Ensure the specification is in markdown format"
                ],
                "example_fix": "analyze_spec('specs/api-feature.md', project_context='src/')"
            }
        )
    except ValueError as e:
        return OperationResult(
            success=False,
            error=f"Invalid specification format: {str(e)}",
            error_code="VALIDATION_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure the specification is in valid markdown format",
                    "Check if the spec has required sections (Description, Requirements, etc.)",
                    "Verify the file content is readable and properly formatted",
                    "Try with a simpler specification file first"
                ],
                "example_fix": "analyze_spec('specs/simple-feature.md')"
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Specification analysis failed: {str(e)}",
            error_code="ANALYSIS_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check if the specification file is readable",
                    "Verify project_context (if provided) is a valid directory",
                    "Ensure the specification follows standard markdown structure",
                    "Try without project_context first"
                ],
                "example_fix": "analyze_spec('spec.md')"
            }
        )


# Export all operations
__all__ = [
    "implement_from_spec",
    "analyze_spec",
    "OperationResult"
]

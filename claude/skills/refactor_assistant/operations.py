"""
Refactor Assistant Operations

Standardized operations interface for agent invocation.
"""

from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
import time

# Import core functions
from .core.smell_detector import detect_code_smells as _detect_code_smells
from .core.refactoring_engine import (
    suggest_refactorings as _suggest_refactorings,
    apply_refactoring as _apply_refactoring
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


def detect_code_smells(
    file_path: str,
    severity_threshold: str = "low",
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Detect code smells and refactoring opportunities in a file.

    Args:
        file_path: Path to file to analyze
        severity_threshold: Minimum severity (low, medium, high, critical)
        response_format: "summary" (counts only) or "detailed" (full smell list)
        **kwargs: Additional parameters

    Returns:
        OperationResult with detected code smells

    Token Efficiency:
        - Use response_format="summary" for counts and high-level overview
        - Use response_format="detailed" when you need all smell details
        - For files with many smells (>10), summary mode saves 85-90% tokens
    """
    start_time = time.time()

    try:
        result = _detect_code_smells(file_path, severity_threshold)

        duration = time.time() - start_time

        # Build response based on format
        if response_format == "summary":
            data = {
                "file_path": result.get('file_path'),
                "total_smells": len(result.get('smells', [])),
                "by_severity": {
                    "critical": len([s for s in result.get('smells', []) if s.get('severity') == 'critical']),
                    "high": len([s for s in result.get('smells', []) if s.get('severity') == 'high']),
                    "medium": len([s for s in result.get('smells', []) if s.get('severity') == 'medium']),
                    "low": len([s for s in result.get('smells', []) if s.get('severity') == 'low'])
                },
                "by_type": {},
                "metrics": result.get('metrics', {}),
                "efficiency_tip": (
                    f"Found {len(result.get('smells', []))} code smells. "
                    f"Using summary mode for efficiency. For full smell details:\n"
                    f"detect_code_smells('{file_path}', response_format='detailed')"
                )
            }
            # Count by type
            for smell in result.get('smells', []):
                smell_type = smell.get('type')
                data["by_type"][smell_type] = data["by_type"].get(smell_type, 0) + 1
        else:
            # Detailed format - include everything
            data = result

        return OperationResult(
            success=True,
            data=data,
            duration=duration,
            metadata={
                "skill": "refactor-assistant",
                "operation": "detect_code_smells",
                "version": "0.1.0",
                "severity_threshold": severity_threshold,
                "response_format": response_format
            }
        )

    except FileNotFoundError:
        return OperationResult(
            success=False,
            error=f"Cannot find file: {file_path}",
            error_code="FILE_NOT_FOUND",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check if the file path is correct",
                    "Use Glob('**/*.py') to find Python files",
                    f"Verify the file exists with Bash('ls -la {Path(file_path).parent}')"
                ],
                "example_fix": "detect_code_smells('src/legacy/old_code.py')"
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
                    "Fix syntax errors in the file before analyzing",
                    f"Run: Bash('python -m py_compile {file_path}') to see detailed syntax errors",
                    "Consider using detect_code_smells on a different file first"
                ],
                "example_fix": "# Fix syntax errors first, then: detect_code_smells('src/fixed_file.py')"
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Code smell detection failed: {str(e)}",
            error_code="DETECTION_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check if the file is a valid Python file",
                    "Try with a simpler file first to verify the operation works",
                    "Check the file encoding (should be UTF-8)"
                ],
                "example_fix": "detect_code_smells('src/simple_module.py', severity_threshold='medium')"
            }
        )


def suggest_refactorings(
    file_path: str,
    max_suggestions: int = 10,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Suggest specific refactorings for code.

    Args:
        file_path: Path to file to analyze
        max_suggestions: Maximum number of suggestions
        response_format: "summary" (overview) or "detailed" (full suggestions)
        **kwargs: Additional parameters

    Returns:
        OperationResult with refactoring suggestions

    Token Efficiency:
        - Use response_format="summary" for counts and types overview
        - Use response_format="detailed" for complete refactoring details
        - Summary mode saves 80-90% tokens for files with many suggestions
    """
    start_time = time.time()

    try:
        result = _suggest_refactorings(file_path, max_suggestions)

        duration = time.time() - start_time

        # Build response based on format
        if response_format == "summary":
            suggestions = result.get('suggestions', [])
            data = {
                "file_path": result.get('file_path'),
                "total_suggestions": len(suggestions),
                "by_type": {},
                "top_priority": suggestions[0] if suggestions else None,
                "efficiency_tip": (
                    f"Found {len(suggestions)} refactoring suggestions. "
                    f"Using summary mode for efficiency. For full suggestions:\n"
                    f"suggest_refactorings('{file_path}', response_format='detailed')"
                )
            }
            # Count by type
            for suggestion in suggestions:
                ref_type = suggestion.get('type')
                data["by_type"][ref_type] = data["by_type"].get(ref_type, 0) + 1
        else:
            # Detailed format - include everything
            data = result

        return OperationResult(
            success=True,
            data=data,
            duration=duration,
            metadata={
                "skill": "refactor-assistant",
                "operation": "suggest_refactorings",
                "version": "0.1.0",
                "max_suggestions": max_suggestions,
                "response_format": response_format
            }
        )

    except FileNotFoundError:
        return OperationResult(
            success=False,
            error=f"Cannot find file: {file_path}",
            error_code="FILE_NOT_FOUND",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check if the file path is correct",
                    "Use Glob('**/*.py') to find Python files",
                    "Verify the file exists before requesting refactorings"
                ],
                "example_fix": "suggest_refactorings('src/services/payment.py', max_suggestions=5)"
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
                    "Fix syntax errors before requesting refactoring suggestions",
                    "Syntax errors must be resolved manually first",
                    "Consider using detect_code_smells to identify all issues"
                ],
                "example_fix": "# Fix syntax first, then: suggest_refactorings('src/fixed_file.py')"
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Refactoring suggestion failed: {str(e)}",
            error_code="SUGGESTION_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check if the file contains valid Python code",
                    "Try reducing max_suggestions if the file is very large",
                    "Ensure the file is readable and properly formatted"
                ],
                "example_fix": "suggest_refactorings('src/module.py', max_suggestions=3)"
            }
        )


def apply_refactoring(
    file_path: str,
    refactoring_type: str,
    location: Dict[str, Any],
    parameters: Dict[str, Any],
    run_tests: bool = False,
    **kwargs
) -> OperationResult:
    """
    Apply a refactoring transformation to code.

    Args:
        file_path: Path to file to refactor
        refactoring_type: Type of refactoring (extract_method, rename_symbol, etc.)
        location: Location information (start_line, end_line, etc.)
        parameters: Refactoring-specific parameters
        run_tests: Whether to run tests after refactoring
        **kwargs: Additional parameters

    Returns:
        OperationResult with refactoring results
    """
    start_time = time.time()

    try:
        result = _apply_refactoring(
            file_path=file_path,
            refactoring_type=refactoring_type,
            location=location,
            parameters=parameters,
            run_tests=run_tests
        )

        duration = time.time() - start_time

        return OperationResult(
            success=result.get('success', False),
            data=result,
            duration=duration,
            metadata={
                "skill": "refactor-assistant",
                "operation": "apply_refactoring",
                "version": "0.1.0",
                "refactoring_type": refactoring_type,
                "tests_run": run_tests
            }
        )

    except FileNotFoundError:
        return OperationResult(
            success=False,
            error=f"Cannot find file: {file_path}",
            error_code="FILE_NOT_FOUND",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check if the file path is correct",
                    "Ensure the file exists before applying refactorings",
                    "Use suggest_refactorings first to identify available refactorings"
                ],
                "example_fix": "apply_refactoring('src/module.py', 'extract_method', {...}, {...})"
            }
        )
    except ValueError as e:
        return OperationResult(
            success=False,
            error=f"Invalid refactoring parameters: {str(e)}",
            error_code="VALIDATION_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check the refactoring_type is valid (extract_method, rename_symbol, etc.)",
                    "Verify location dict has required fields (start_line, end_line)",
                    "Ensure parameters dict contains refactoring-specific values",
                    "Use suggest_refactorings to get valid refactoring suggestions first"
                ],
                "example_fix": "apply_refactoring('file.py', 'extract_method', {'start_line': 10, 'end_line': 15}, {'new_name': 'calculate'})"
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Refactoring failed: {str(e)}",
            error_code="REFACTORING_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure the code at the specified location is refactorable",
                    "Check if the file has been modified since suggesting refactorings",
                    "Try with a smaller/simpler refactoring first",
                    "Set run_tests=False if tests are failing"
                ],
                "example_fix": "apply_refactoring('file.py', 'rename_variable', {'line': 10}, {'old_name': 'x', 'new_name': 'count'}, run_tests=False)"
            }
        )


def analyze_complexity(
    file_path: str,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Analyze code complexity metrics.

    Args:
        file_path: Path to file to analyze
        response_format: "summary" (metrics only) or "detailed" (with all issues)
        **kwargs: Additional parameters

    Returns:
        OperationResult with complexity analysis

    Token Efficiency:
        - Use response_format="summary" for high-level metrics
        - Use response_format="detailed" for all complexity issues
        - Summary mode saves 85-90% tokens for complex files
    """
    start_time = time.time()

    try:
        # Use code smell detection to get complexity metrics
        result = _detect_code_smells(file_path, severity_threshold="low")

        # Extract complexity-related issues
        complexity_issues = [
            smell for smell in result.get('smells', [])
            if smell['type'] in ['complex_function', 'cognitive_complexity', 'deep_nesting']
        ]

        # Build response based on format
        if response_format == "summary":
            complexity_data = {
                "file_path": result.get('file_path'),
                "metrics": result.get('metrics', {}),
                "total_complexity_issues": len(complexity_issues),
                "issue_types": {},
                "efficiency_tip": (
                    f"Found {len(complexity_issues)} complexity issues. "
                    f"Using summary mode for efficiency. For full details:\n"
                    f"analyze_complexity('{file_path}', response_format='detailed')"
                )
            }
            # Count by type
            for issue in complexity_issues:
                issue_type = issue.get('type')
                complexity_data["issue_types"][issue_type] = complexity_data["issue_types"].get(issue_type, 0) + 1
        else:
            # Detailed format - include all issues and recommendations
            complexity_data = {
                "file_path": result.get('file_path'),
                "metrics": result.get('metrics', {}),
                "complexity_issues": complexity_issues,
                "total_complexity_issues": len(complexity_issues),
                "recommendations": [
                    smell['suggestion'] for smell in complexity_issues
                ]
            }

        duration = time.time() - start_time

        return OperationResult(
            success=True,
            data=complexity_data,
            duration=duration,
            metadata={
                "skill": "refactor-assistant",
                "operation": "analyze_complexity",
                "version": "0.1.0",
                "response_format": response_format
            }
        )

    except FileNotFoundError:
        return OperationResult(
            success=False,
            error=f"Cannot find file: {file_path}",
            error_code="FILE_NOT_FOUND",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check if the file path is correct",
                    "Use Glob('**/*.py') to find Python files in the project",
                    "Verify the file exists before analyzing complexity"
                ],
                "example_fix": "analyze_complexity('src/services/payment.py')"
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Complexity analysis failed: {str(e)}",
            error_code="ANALYSIS_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure the file contains valid Python code",
                    "Check if the file is too large or has unusual structure",
                    "Try analyzing a simpler file first to verify the operation works"
                ],
                "example_fix": "analyze_complexity('src/simple_module.py')"
            }
        )


# Export all operations
__all__ = [
    "detect_code_smells",
    "suggest_refactorings",
    "apply_refactoring",
    "analyze_complexity",
    "OperationResult"
]

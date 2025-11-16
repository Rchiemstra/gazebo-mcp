"""
Verification Skill Operations

Agent-friendly interface for code, output, and test validation.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import time

from .core.code_validator import CodeValidator
from .core.output_validator import OutputValidator
from .core.test_validator import TestValidator


@dataclass
class OperationResult:
    """Result from a skill operation."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    duration: float = 0.0
    metadata: Optional[Dict[str, Any]] = None


def validate_code(
    code: str,
    check_style: bool = True,
    check_security: bool = True,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Validate Python code for syntax, style, and security.

    Args:
        code: Python code to validate
        check_style: Whether to check style issues
        check_security: Whether to check security issues
        response_format: "summary" (issues only) or "detailed" (with metrics)

    Returns:
        OperationResult with validation results

    Token Efficiency:
        - Use response_format="summary" for just validity and issue count
        - Use response_format="detailed" for all issues and metrics
        - Summary mode saves 70-80% tokens
    """
    start_time = time.time()

    try:
        validator = CodeValidator()
        result = validator.validate(code, check_style=check_style, check_security=check_security)

        duration = time.time() - start_time

        # Format response based on response_format
        data = {
            "is_valid": result.is_valid,
            "issue_count": len(result.issues),
            "error_count": sum(1 for issue in result.issues if issue.severity == 'error'),
            "warning_count": sum(1 for issue in result.issues if issue.severity == 'warning')
        }

        if response_format == "detailed":
            data.update({
                "issues": [
                    {
                        "severity": issue.severity,
                        "category": issue.category,
                        "message": issue.message,
                        "line": issue.line,
                        "suggestion": issue.suggestion
                    }
                    for issue in result.issues
                ],
                "metrics": result.metrics
            })
        else:  # summary
            # Just show first 3 issues
            if result.issues:
                data["top_issues"] = [
                    f"{issue.severity.upper()}: {issue.message}"
                    for issue in result.issues[:3]
                ]
            data["efficiency_tip"] = (
                f"Code validation complete! Found {len(result.issues)} issues.\n"
                f"For full issue list and metrics:\n"
                f"validate_code(code, response_format='detailed')"
            )

        return OperationResult(
            success=True,
            data=data,
            duration=duration,
            metadata={
                "skill": "verification",
                "operation": "validate_code",
                "version": "1.0.0"
            }
        )

    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Code validation failed: {str(e)}",
            error_code="VALIDATION_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure the code parameter contains valid Python code",
                    "Check if the code is a string, not bytes or other type",
                    "Try with simpler code first to verify the skill is working"
                ],
                "example_fix": "validate_code('def hello():\\n    print(\"Hello world\")')"
            }
        )


def validate_output(
    expected: str,
    actual: str,
    match_type: str = "exact",
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Validate program output against expected results.

    Args:
        expected: Expected output
        actual: Actual output
        match_type: "exact", "contains", "regex", "json", or "lines"
        response_format: "summary" (match result only) or "detailed" (with differences)

    Returns:
        OperationResult with validation results

    Token Efficiency:
        - Use response_format="summary" for just match result and similarity
        - Use response_format="detailed" for full difference analysis
        - Summary mode saves 80-90% tokens for large outputs
    """
    start_time = time.time()

    try:
        validator = OutputValidator()

        # Choose validation method based on match_type
        if match_type == "exact":
            result = validator.validate_exact(expected, actual)
        elif match_type == "contains":
            result = validator.validate_contains(expected, actual)
        elif match_type == "regex":
            result = validator.validate_regex(expected, actual)
        elif match_type == "json":
            result = validator.validate_json(expected, actual)
        elif match_type == "lines":
            expected_lines = expected.strip().split('\n')
            result = validator.validate_lines(expected_lines, actual)
        else:
            return OperationResult(
                success=False,
                error=f"Invalid match_type: {match_type}",
                error_code="INVALID_MATCH_TYPE",
                duration=time.time() - start_time,
                metadata={
                    "suggestions": [
                        "Valid match_type values: 'exact', 'contains', 'regex', 'json', 'lines'",
                        "Use 'exact' for exact string match",
                        "Use 'contains' to check if actual contains expected",
                        "Use 'regex' for pattern matching"
                    ],
                    "example_fix": "validate_output('Hello', 'Hello world', match_type='contains')"
                }
            )

        duration = time.time() - start_time

        data = {
            "is_match": result.is_match,
            "similarity_score": result.similarity_score,
            "match_type": match_type
        }

        if response_format == "detailed":
            data.update({
                "differences": result.differences,
                "details": result.details
            })
        else:  # summary
            if not result.is_match:
                data["difference_count"] = len(result.differences)
                data["efficiency_tip"] = (
                    f"Output validation complete! Match: {result.is_match}.\n"
                    f"For full difference details:\n"
                    f"validate_output(expected, actual, match_type='{match_type}', response_format='detailed')"
                )

        return OperationResult(
            success=True,
            data=data,
            duration=duration,
            metadata={
                "skill": "verification",
                "operation": "validate_output",
                "version": "1.0.0"
            }
        )

    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Output validation failed: {str(e)}",
            error_code="VALIDATION_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure expected and actual are strings",
                    "Check that match_type is one of: exact, contains, regex, json, lines",
                    "For JSON validation, ensure inputs are valid JSON",
                    "For regex validation, ensure pattern is valid"
                ],
                "example_fix": "validate_output('expected output', 'actual output', match_type='exact')"
            }
        )


def validate_tests(
    test_code: str,
    source_code: Optional[str] = None,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Validate test code quality and coverage.

    Args:
        test_code: Test code to validate
        source_code: Optional source code being tested (for coverage analysis)
        response_format: "summary" (overview only) or "detailed" (with all issues)

    Returns:
        OperationResult with validation results

    Token Efficiency:
        - Use response_format="summary" for test count and validity
        - Use response_format="detailed" for all issues and suggestions
        - Summary mode saves 75-85% tokens
    """
    start_time = time.time()

    try:
        validator = TestValidator()
        result = validator.validate_tests(test_code, source_code)

        duration = time.time() - start_time

        data = {
            "is_valid": result.is_valid,
            "test_count": result.test_count,
            "issue_count": len(result.issues)
        }

        if source_code:
            data["coverage_ratio"] = result.metrics.get('coverage_ratio', 0.0)
            data["functions_covered"] = len(result.coverage_functions)

        if response_format == "detailed":
            data.update({
                "issues": result.issues,
                "metrics": result.metrics,
                "covered_functions": list(result.coverage_functions)
            })

            # Add suggestions for missing tests
            if source_code:
                suggestions = validator.suggest_missing_tests(source_code, test_code)
                data["suggestions_for_improvement"] = suggestions[:5]  # Top 5

        else:  # summary
            if result.issues:
                data["top_issues"] = result.issues[:3]
            data["efficiency_tip"] = (
                f"Test validation complete! Found {result.test_count} tests.\n"
                f"For full issues and improvement suggestions:\n"
                f"validate_tests(test_code, source_code, response_format='detailed')"
            )

        return OperationResult(
            success=True,
            data=data,
            duration=duration,
            metadata={
                "skill": "verification",
                "operation": "validate_tests",
                "version": "1.0.0"
            }
        )

    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Test validation failed: {str(e)}",
            error_code="VALIDATION_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure test_code contains valid Python test functions",
                    "Test functions should start with 'test_'",
                    "If providing source_code, ensure it's valid Python",
                    "Check that test_code and source_code are strings"
                ],
                "example_fix": "validate_tests('def test_example():\\n    assert True')"
            }
        )

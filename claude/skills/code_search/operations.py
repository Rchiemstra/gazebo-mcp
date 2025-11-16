"""
Code Search Operations

Standardized operations interface for agent invocation.
"""

from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
import time

# Import core functions
from .core.search_engine import search_symbol as _search_symbol
from .core.search_engine import search_pattern as _search_pattern
from .core.definition_finder import find_definition as _find_definition
from .core.usage_finder import find_usages as _find_usages


@dataclass
class OperationResult:
    """Result from a skill operation."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    duration: float = 0.0
    metadata: Optional[Dict[str, Any]] = None


def search_symbol(
    project_path: str,
    symbol_name: str,
    symbol_type: str = "all",
    exact_match: bool = False,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Find symbols (functions, classes, variables) in codebase.

    Args:
        project_path: Path to project root
        symbol_name: Symbol to search for
        symbol_type: Type of symbol ('function', 'class', 'variable', 'all')
        exact_match: Exact match or fuzzy search
        response_format: "summary" (counts & files) or "detailed" (full symbol info)
        **kwargs: Additional parameters

    Returns:
        OperationResult with symbol search results

    Token Efficiency:
        - Use response_format="summary" for file locations and counts
        - Use response_format="detailed" for complete symbol definitions
        - Summary mode saves 80-90% tokens
    """
    start_time = time.time()

    try:
        result = _search_symbol(
            project_path=project_path,
            symbol_name=symbol_name,
            symbol_type=symbol_type,
            exact_match=exact_match
        )

        duration = time.time() - start_time

        return OperationResult(
            success=True,
            data=result,
            duration=duration,
            metadata={
                "skill": "code-search",
                "operation": "search_symbol",
                "version": "0.1.0",
                "symbol_type": symbol_type,
                "exact_match": exact_match
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
                    "Verify the directory contains Python files",
                    "Ensure project_path points to a valid project root"
                ],
                "example_fix": "search_symbol('src/', 'UserAuth', symbol_type='class')"
            }
        )
    except ValueError as e:
        return OperationResult(
            success=False,
            error=f"Invalid symbol type: {str(e)}",
            error_code="VALIDATION_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Valid symbol_type values: 'function', 'class', 'variable', or 'all'",
                    "Check the symbol_type parameter spelling",
                    "Use 'all' to search for any symbol type",
                    "Verify symbol_name is a non-empty string"
                ],
                "example_fix": "search_symbol('src/', 'authenticate', symbol_type='function')"
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Symbol search failed: {str(e)}",
            error_code="SEARCH_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure the project contains Python files to search",
                    "Try with a different symbol_name that you know exists",
                    "Check if Python files are syntactically valid",
                    "Use Glob('**/*.py') to verify Python files exist"
                ],
                "example_fix": "search_symbol('project/', 'MyClass', symbol_type='class', exact_match=False)"
            }
        )


def search_pattern(
    project_path: str,
    pattern: str,
    pattern_type: str = "ast",
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Search for code patterns in codebase.

    Args:
        project_path: Path to project root
        pattern: Pattern to search for
        pattern_type: Type of pattern ('ast', 'regex', 'text')
        response_format: "summary" (counts only) or "detailed" (full matches)
        **kwargs: Additional parameters

    Returns:
        OperationResult with pattern search results

    Token Efficiency:
        - Use response_format="summary" for match counts and overview
        - Use response_format="detailed" when you need all match locations
        - Summary mode saves 80-90% tokens for large codebases
    """
    start_time = time.time()

    try:
        result = _search_pattern(
            project_path=project_path,
            pattern=pattern,
            pattern_type=pattern_type
        )

        duration = time.time() - start_time

        return OperationResult(
            success=True,
            data=result,
            duration=duration,
            metadata={
                "skill": "code-search",
                "operation": "search_pattern",
                "version": "0.1.0",
                "pattern_type": pattern_type
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
                    "Ensure the directory contains code files to search",
                    "Use Glob('**/*.py') to see available Python files"
                ],
                "example_fix": "search_pattern('src/', 'def.*login', pattern_type='regex')"
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Pattern search failed: {str(e)}",
            error_code="SEARCH_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure the pattern is valid for the pattern_type",
                    "Valid pattern_type values: 'ast', 'regex', 'text'",
                    "For regex patterns, verify the regex syntax is correct",
                    "Try with pattern_type='text' for simpler text search"
                ],
                "example_fix": "search_pattern('src/', 'UserAuth', pattern_type='text')"
            }
        )


def find_definition(
    project_path: str,
    symbol_name: str,
    file_context: Optional[str] = None,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Find the definition of a symbol.

    Args:
        project_path: Path to project root
        symbol_name: Symbol to find definition for
        file_context: Optional file where symbol is used (for context)
        response_format: "summary" (location only) or "detailed" (with code snippet)
        **kwargs: Additional parameters

    Returns:
        OperationResult with symbol definition

    Token Efficiency:
        - Use response_format="summary" for just file path and line number
        - Use response_format="detailed" when you need the code snippet
        - Summary mode saves 70-80% tokens
    """
    start_time = time.time()

    try:
        result = _find_definition(
            project_path=project_path,
            symbol_name=symbol_name,
            file_context=file_context
        )

        duration = time.time() - start_time

        return OperationResult(
            success=True,
            data=result,
            duration=duration,
            metadata={
                "skill": "code-search",
                "operation": "find_definition",
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
                    "Verify the directory exists",
                    "Ensure file_context (if provided) is a valid file path",
                    "Use Glob('**/*.py') to find Python files in the project"
                ],
                "example_fix": "find_definition('src/', 'UserAuth', file_context='src/auth/login.py')"
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Definition search failed: {str(e)}",
            error_code="SEARCH_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure symbol_name exists in the project",
                    "Try search_symbol first to verify the symbol exists",
                    "Check if Python files are syntactically valid",
                    "Verify symbol_name is spelled correctly"
                ],
                "example_fix": "find_definition('project/', 'authenticate')"
            }
        )


def find_usages(
    project_path: str,
    symbol_name: str,
    file_path: Optional[str] = None,
    response_format: str = "summary",
    include_tests: bool = True,
    **kwargs
) -> OperationResult:
    """
    Find all usages of a symbol.

    Args:
        project_path: Path to project root
        symbol_name: Symbol to find usages for
        file_path: Optional specific file to search in
        response_format: "summary" (usage count) or "detailed" (all locations)
        include_tests: Include test files in search
        **kwargs: Additional parameters

    Returns:
        OperationResult with symbol usages

    Token Efficiency:
        - Use response_format="summary" for usage counts per file
        - Use response_format="detailed" when you need all line numbers
        - Summary mode saves 85-90% tokens for widely-used symbols
    """
    start_time = time.time()

    try:
        result = _find_usages(
            project_path=project_path,
            symbol_name=symbol_name,
            definition_file=file_path
        )

        duration = time.time() - start_time

        return OperationResult(
            success=True,
            data=result,
            duration=duration,
            metadata={
                "skill": "code-search",
                "operation": "find_usages",
                "version": "0.1.0",
                "include_tests": include_tests
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
                    "Ensure file_path (if provided) is a valid file",
                    "Use Glob('**/*.py') to see available Python files"
                ],
                "example_fix": "find_usages('src/', 'authenticate', include_tests=True)"
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Usage search failed: {str(e)}",
            error_code="SEARCH_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure symbol_name exists in the project",
                    "Try find_definition first to verify the symbol exists",
                    "Check if Python files are syntactically valid",
                    "Try with include_tests=False to search only production code"
                ],
                "example_fix": "find_usages('project/', 'UserAuth', file_path='src/models.py')"
            }
        )


# Export all operations
__all__ = [
    "search_symbol",
    "search_pattern",
    "find_definition",
    "find_usages",
    "OperationResult"
]

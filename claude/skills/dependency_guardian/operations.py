"""
Dependency Guardian Operations

Standardized operations interface for agent invocation.
"""

from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
import time

# Import core functions
from .core.dependency_analyzer import analyze_dependencies as _analyze_dependencies
from .core.vulnerability_scanner import check_vulnerabilities as _check_vulnerabilities
from .core.update_checker import check_updates as _check_updates


@dataclass
class OperationResult:
    """Result from a skill operation."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    duration: float = 0.0
    metadata: Optional[Dict[str, Any]] = None


def analyze_dependencies(
    project_path: str,
    ecosystem: Optional[str] = None,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Analyze all dependencies in a project.

    Args:
        project_path: Path to project directory
        ecosystem: Specific ecosystem to analyze (python, npm, auto)
        response_format: "summary" (counts only) or "detailed" (full dependency tree)
        **kwargs: Additional parameters

    Returns:
        OperationResult with dependency analysis

    Token Efficiency:
        - Use response_format="summary" for high-level overview
        - Use response_format="detailed" for complete dependency tree
        - Summary mode saves 85-95% tokens for projects with many dependencies
    """
    start_time = time.time()

    try:
        result = _analyze_dependencies(project_path, ecosystem)

        duration = time.time() - start_time

        # Build response based on format
        if response_format == "summary":
            dependencies = result.get('dependencies', [])
            data = {
                "project_path": result.get('project_path'),
                "ecosystem": result.get('ecosystem'),
                "total_dependencies": len(dependencies),
                "direct_dependencies": len([d for d in dependencies if d.get('direct', False)]),
                "transitive_dependencies": len([d for d in dependencies if not d.get('direct', False)]),
                "dependency_types": {},
                "efficiency_tip": (
                    f"Found {len(dependencies)} dependencies. "
                    f"Using summary mode for efficiency. For full dependency tree:\n"
                    f"analyze_dependencies('{project_path}', response_format='detailed')"
                )
            }
            # Count by type
            for dep in dependencies:
                dep_type = dep.get('type', 'runtime')
                data["dependency_types"][dep_type] = data["dependency_types"].get(dep_type, 0) + 1
        else:
            # Detailed format - include everything
            data = result

        return OperationResult(
            success=True,
            data=data,
            duration=duration,
            metadata={
                "skill": "dependency-guardian",
                "operation": "analyze_dependencies",
                "version": "0.1.0",
                "ecosystem": ecosystem or "auto",
                "response_format": response_format
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
                    "Ensure the path contains dependency files (requirements.txt, package.json)"
                ],
                "example_fix": "analyze_dependencies('path/to/project/', ecosystem='python')"
            }
        )
    except ValueError as e:
        return OperationResult(
            success=False,
            error=f"Invalid project or ecosystem: {str(e)}",
            error_code="VALIDATION_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Valid ecosystems are: 'python', 'npm', or 'auto' (auto-detect)",
                    "Ensure the project directory contains dependency files",
                    "For Python: requires requirements.txt or setup.py",
                    "For Node.js: requires package.json"
                ],
                "example_fix": "analyze_dependencies('project/', ecosystem='auto')"
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Dependency analysis failed: {str(e)}",
            error_code="ANALYSIS_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check if dependency files are valid and not corrupted",
                    "Verify network connection for fetching dependency data",
                    "Try with a simpler project first to verify the operation works",
                    "Ensure dependency files follow proper format (valid JSON/requirements syntax)"
                ],
                "example_fix": "analyze_dependencies('path/to/simple-project/', ecosystem='python')"
            }
        )


def check_vulnerabilities(
    project_path: str,
    ecosystem: Optional[str] = None,
    include_low: bool = True,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Check dependencies for known security vulnerabilities.

    Args:
        project_path: Path to project directory
        ecosystem: Specific ecosystem to check (python, npm, auto)
        include_low: Include low severity vulnerabilities (default: True)
        response_format: "summary" (counts by severity) or "detailed" (full CVE details)
        **kwargs: Additional parameters

    Returns:
        OperationResult with vulnerability scan results

    Token Efficiency:
        - Use response_format="summary" for vulnerability counts
        - Use response_format="detailed" for complete CVE information
        - Summary mode saves 90-95% tokens for projects with many vulnerabilities
    """
    start_time = time.time()

    try:
        result = _check_vulnerabilities(project_path, ecosystem, include_low)

        duration = time.time() - start_time

        # Build response based on format
        if response_format == "summary":
            vulnerabilities = result.get('vulnerabilities', [])
            data = {
                "project_path": result.get('project_path'),
                "total_vulnerabilities": len(vulnerabilities),
                "by_severity": {
                    "critical": len([v for v in vulnerabilities if v.get('severity') == 'critical']),
                    "high": len([v for v in vulnerabilities if v.get('severity') == 'high']),
                    "medium": len([v for v in vulnerabilities if v.get('severity') == 'medium']),
                    "low": len([v for v in vulnerabilities if v.get('severity') == 'low'])
                },
                "affected_packages": len(set([v.get('package') for v in vulnerabilities])),
                "has_critical": any(v.get('severity') == 'critical' for v in vulnerabilities),
                "efficiency_tip": (
                    f"Found {len(vulnerabilities)} vulnerabilities. "
                    f"Using summary mode for efficiency. For full CVE details:\n"
                    f"check_vulnerabilities('{project_path}', response_format='detailed')"
                )
            }
        else:
            # Detailed format - include everything
            data = result

        return OperationResult(
            success=True,
            data=data,
            duration=duration,
            metadata={
                "skill": "dependency-guardian",
                "operation": "check_vulnerabilities",
                "version": "0.1.0",
                "ecosystem": ecosystem or "auto",
                "include_low": include_low,
                "response_format": response_format
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
                    "Ensure the project has dependency files (requirements.txt, package.json)",
                    "Use Bash('find . -name requirements.txt') to locate dependency files",
                    "Verify you're in the correct working directory"
                ],
                "example_fix": "check_vulnerabilities('path/to/project/', ecosystem='python')"
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Vulnerability check failed: {str(e)}",
            error_code="SCAN_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Verify network connection for vulnerability database access",
                    "Check if dependency files are parseable",
                    "Try running analyze_dependencies first to verify project setup",
                    "Ensure you have permissions to access the project directory"
                ],
                "example_fix": "check_vulnerabilities('project/', ecosystem='auto', include_low=False)"
            }
        )


def check_updates(
    project_path: str,
    ecosystem: Optional[str] = None,
    include_major: bool = False,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Check for available updates to dependencies.

    Args:
        project_path: Path to project directory
        ecosystem: Specific ecosystem to check (python, npm, auto)
        include_major: Include major version updates (default: False)
        response_format: "summary" (counts by type) or "detailed" (all update details)
        **kwargs: Additional parameters

    Returns:
        OperationResult with update check results

    Token Efficiency:
        - Use response_format="summary" for update counts
        - Use response_format="detailed" for all version details
        - Summary mode saves 85-90% tokens for projects with many updates
    """
    start_time = time.time()

    try:
        result = _check_updates(project_path, ecosystem, include_major)

        duration = time.time() - start_time

        # Build response based on format
        if response_format == "summary":
            updates = result.get('updates', [])
            data = {
                "project_path": result.get('project_path'),
                "total_updates": len(updates),
                "by_type": {
                    "major": len([u for u in updates if u.get('update_type') == 'major']),
                    "minor": len([u for u in updates if u.get('update_type') == 'minor']),
                    "patch": len([u for u in updates if u.get('update_type') == 'patch'])
                },
                "security_updates": len([u for u in updates if u.get('security', False)]),
                "efficiency_tip": (
                    f"Found {len(updates)} available updates. "
                    f"Using summary mode for efficiency. For all version details:\n"
                    f"check_updates('{project_path}', response_format='detailed')"
                )
            }
        else:
            # Detailed format - include everything
            data = result

        return OperationResult(
            success=True,
            data=data,
            duration=duration,
            metadata={
                "skill": "dependency-guardian",
                "operation": "check_updates",
                "version": "0.1.0",
                "ecosystem": ecosystem or "auto",
                "include_major": include_major,
                "response_format": response_format
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
                    "Ensure dependency files exist (requirements.txt, package.json)",
                    "Use Glob('**/package.json') to find Node.js projects",
                    "Use Glob('**/requirements.txt') to find Python projects"
                ],
                "example_fix": "check_updates('path/to/project/', ecosystem='auto')"
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Update check failed: {str(e)}",
            error_code="CHECK_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Verify network connection for checking package registries",
                    "Check if dependency files are properly formatted",
                    "Try with include_major=False to check only minor/patch updates",
                    "Ensure you have access to package registries (PyPI, npm)"
                ],
                "example_fix": "check_updates('project/', ecosystem='python', include_major=False)"
            }
        )


# Export all operations
__all__ = [
    "analyze_dependencies",
    "check_vulnerabilities",
    "check_updates",
    "OperationResult"
]

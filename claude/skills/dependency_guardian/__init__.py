"""
Dependency Guardian Skill

Monitors and manages project dependencies.
"""

# Import core functions for direct use
from .core.dependency_analyzer import analyze_dependencies as _analyze_dependencies_core
from .core.vulnerability_scanner import check_vulnerabilities as _check_vulnerabilities_core
from .core.update_checker import check_updates as _check_updates_core

# Import operations for agent invocation
from .operations import (
    analyze_dependencies,
    check_vulnerabilities,
    check_updates,
    OperationResult
)

__all__ = [
    # Core functions (for backward compatibility)
    "_analyze_dependencies_core",
    "_check_vulnerabilities_core",
    "_check_updates_core",
    # Operations
    "analyze_dependencies",
    "check_vulnerabilities",
    "check_updates",
    "OperationResult"
]

__version__ = "0.1.0"

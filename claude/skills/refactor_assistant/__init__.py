"""
Refactor Assistant Skill

Intelligently refactors code to improve quality and maintainability.
"""

# Import core functions for direct use
from .core.smell_detector import detect_code_smells as _detect_code_smells_core
from .core.refactoring_engine import suggest_refactorings as _suggest_refactorings_core
from .core.refactoring_engine import apply_refactoring as _apply_refactoring_core

# Import operations for agent invocation
from .operations import (
    detect_code_smells,
    suggest_refactorings,
    apply_refactoring,
    analyze_complexity,
    OperationResult
)

__all__ = [
    # Core functions (for backward compatibility)
    "_detect_code_smells_core",
    "_suggest_refactorings_core",
    "_apply_refactoring_core",
    # Operations
    "detect_code_smells",
    "suggest_refactorings",
    "apply_refactoring",
    "analyze_complexity",
    "OperationResult"
]

__version__ = "0.1.0"

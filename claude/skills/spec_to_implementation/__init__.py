"""
Spec to Implementation Skill

Meta-skill that orchestrates other skills to transform specifications
into working, tested, documented code.
"""

# Import core functions for direct use
from .core.orchestrator import implement_from_spec as _implement_from_spec_core
from .core.orchestrator import analyze_spec as _analyze_spec_core

# Import operations for agent invocation
from .operations import (
    implement_from_spec,
    analyze_spec,
    OperationResult
)

__all__ = [
    # Core functions (for backward compatibility)
    "_implement_from_spec_core",
    "_analyze_spec_core",
    # Operations
    "implement_from_spec",
    "analyze_spec",
    "OperationResult"
]

__version__ = "0.1.0"

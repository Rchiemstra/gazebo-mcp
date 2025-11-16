"""
Code Search Skill

Intelligent code search with AST-based indexing and semantic understanding.
"""

# Import core functions for direct use
from .core.search_engine import search_symbol as _search_symbol_core
from .core.search_engine import search_pattern as _search_pattern_core
from .core.definition_finder import find_definition as _find_definition_core
from .core.usage_finder import find_usages as _find_usages_core

# Import operations for agent invocation
from .operations import (
    search_symbol,
    search_pattern,
    find_definition,
    find_usages,
    OperationResult
)

__all__ = [
    # Core functions (for backward compatibility)
    "_search_symbol_core",
    "_search_pattern_core",
    "_find_definition_core",
    "_find_usages_core",
    # Operations
    "search_symbol",
    "search_pattern",
    "find_definition",
    "find_usages",
    "OperationResult"
]

__version__ = "0.1.0"

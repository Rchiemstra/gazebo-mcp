"""
Doc Generator Skill

Automated documentation generation from code analysis.
"""

# Import core functions for direct use
from .core.docstring_generator import generate_docstrings as _generate_docstrings_core
from .core.readme_generator import generate_readme as _generate_readme_core
from .core.doc_analyzer import analyze_documentation as _analyze_documentation_core

# Import operations for agent invocation
from .operations import (
    generate_docstrings,
    generate_readme,
    analyze_documentation,
    OperationResult
)

__all__ = [
    # Core functions (for backward compatibility)
    "_generate_docstrings_core",
    "_generate_readme_core",
    "_analyze_documentation_core",
    # Operations
    "generate_docstrings",
    "generate_readme",
    "analyze_documentation",
    "OperationResult"
]

__version__ = "0.1.0"

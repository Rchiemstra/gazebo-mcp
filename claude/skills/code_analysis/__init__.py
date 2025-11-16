"""
Code Analysis Skill

Provides deep static code analysis for Python codebases.
Includes AST parsing, complexity metrics, pattern detection, and integration point identification.
"""

from .models import (
    NodeType,
    DesignPattern,
    CodeSmell,
    ComplexityMetrics,
    CodeEntity,
    FileAnalysis,
    DependencyEdge,
    DependencyGraph,
    IntegrationPoint,
    CodebaseAnalysis,
)
from .python_analyzer import PythonAnalyzer
from .pattern_detector import PatternDetector
from .code_analyzer import CodeAnalyzer

# Import operations for agent invocation
from .operations import analyze_codebase, analyze_codebase_parallel, analyze_file, OperationResult

__all__ = [
    # Enums
    "NodeType",
    "DesignPattern",
    "CodeSmell",
    # Models
    "ComplexityMetrics",
    "CodeEntity",
    "FileAnalysis",
    "DependencyEdge",
    "DependencyGraph",
    "IntegrationPoint",
    "CodebaseAnalysis",
    # Main classes
    "PythonAnalyzer",
    "PatternDetector",
    "CodeAnalyzer",
    # Operations (agent-friendly interface)
    "analyze_codebase",
    "analyze_codebase_parallel",
    "analyze_file",
    "OperationResult",
]

__version__ = "0.1.0"

"""
Test Orchestrator Skill

Intelligent test generation, execution, and coverage analysis.
"""

from .core.analyzer import CodeAnalyzer
from .core.test_generator import TestGenerator
from .core.coverage_analyzer import CoverageAnalyzer

# Import operations for agent invocation
from .operations import (
    analyze_file,
    analyze_files_parallel,
    generate_tests,
    generate_tests_parallel,
    analyze_coverage,
    OperationResult
)

__all__ = [
    # Core components
    "CodeAnalyzer",
    "TestGenerator",
    "CoverageAnalyzer",
    # Operations
    "analyze_file",
    "analyze_files_parallel",
    "generate_tests",
    "generate_tests_parallel",
    "analyze_coverage",
    "OperationResult"
]
__version__ = "0.1.0"

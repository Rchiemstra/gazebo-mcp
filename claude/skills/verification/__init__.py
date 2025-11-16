"""
Verification Skill

Validates code, output, and tests to ensure quality and correctness.
"""

from .operations import (
    validate_code,
    validate_output,
    validate_tests,
    OperationResult
)

__all__ = [
    'validate_code',
    'validate_output',
    'validate_tests',
    'OperationResult'
]

__version__ = '1.0.0'

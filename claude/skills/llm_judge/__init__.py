"""
LLM-as-Judge Skill

Evaluates teaching quality and student understanding for learning-first workflows.
"""

from .operations import (
    evaluate_teaching,
    check_understanding,
    OperationResult
)

__all__ = [
    'evaluate_teaching',
    'check_understanding',
    'OperationResult'
]

__version__ = '1.0.0'

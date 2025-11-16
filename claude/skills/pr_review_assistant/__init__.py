"""
PR Review Assistant Skill

Automated pull request review system.
"""

# Import core functions for direct use
from .core.pr_analyzer import review_pull_request as _review_pull_request_core
from .core.comment_generator import generate_review_comment as _generate_review_comment_core

# Import operations for agent invocation
from .operations import (
    review_pull_request,
    generate_review_comment,
    analyze_change_impact,
    check_pr_quality,
    OperationResult
)

__all__ = [
    # Core functions (for backward compatibility)
    "_review_pull_request_core",
    "_generate_review_comment_core",
    # Operations
    "review_pull_request",
    "generate_review_comment",
    "analyze_change_impact",
    "check_pr_quality",
    "OperationResult"
]

__version__ = "0.1.0"

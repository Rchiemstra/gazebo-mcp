"""
Git Workflow Assistant Skill

Intelligent git workflow automation including commit messages, branch management,
and PR creation.
"""

# Import core functions for direct use
from .core.change_analyzer import analyze_changes as _analyze_changes_core
from .core.commit_generator import generate_commit_message as _generate_commit_message_core
from .core.branch_manager import suggest_branch_name as _suggest_branch_name_core
from .core.pr_generator import create_pull_request as _create_pull_request_core

# Import operations for agent invocation
from .operations import (
    analyze_changes,
    generate_commit_message,
    suggest_branch_name,
    create_pull_request,
    OperationResult
)

__all__ = [
    # Core functions (for backward compatibility)
    "_analyze_changes_core",
    "_generate_commit_message_core",
    "_suggest_branch_name_core",
    "_create_pull_request_core",
    # Operations
    "analyze_changes",
    "generate_commit_message",
    "suggest_branch_name",
    "create_pull_request",
    "OperationResult"
]

__version__ = "0.1.0"

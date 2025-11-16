"""
Context Manager Skill

Manages context usage and optimization for long-horizon tasks.
Provides compaction, note-taking, and context analysis capabilities.
"""

from .operations import (
    analyze_context_usage,
    create_notes,
    compact_conversation,
    analyze_available_skills,
    OperationResult
)

__all__ = [
    # Operations
    "analyze_context_usage",
    "create_notes",
    "compact_conversation",
    "analyze_available_skills",
    "OperationResult"
]

__version__ = "0.1.0"

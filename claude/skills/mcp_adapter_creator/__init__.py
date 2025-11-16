"""
MCP Adapter Creator Skill.

Creates MCP adapter files for skills following Anthropic best practices.
"""

from .operations import (
    create_adapter,
    create_batch_adapters,
    OperationResult,
    ErrorCodes
)

__version__ = "1.0.0"
__all__ = [
    "create_adapter",
    "create_batch_adapters",
    "OperationResult",
    "ErrorCodes"
]

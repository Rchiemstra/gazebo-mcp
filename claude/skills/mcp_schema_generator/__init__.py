"""
MCP Schema Generator Skill.

Generates MCP tool schemas from skill operations following Anthropic best practices.
"""

from .operations import (
    generate_schema,
    validate_schema,
    generate_batch_schemas,
    OperationResult,
    ErrorCodes,
    MCPSchema
)

__version__ = "1.0.0"
__all__ = [
    "generate_schema",
    "validate_schema",
    "generate_batch_schemas",
    "OperationResult",
    "ErrorCodes",
    "MCPSchema"
]

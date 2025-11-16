"""
{{SKILL_NAME}} Skill Operations

{{SKILL_DESCRIPTION}}

This module provides standardized operations that can be invoked by agents.

Author: {{AUTHOR_NAME}}
Created: {{CREATED_DATE}}
Version: 0.1.0
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, List
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class OperationResult:
    """
    Standardized result object for all skill operations.

    This dataclass ensures consistent return values across all operations,
    making it easy for agents to handle results programmatically.

    Attributes:
        success (bool): Whether the operation completed successfully
        data (Optional[Dict[str, Any]]): Operation-specific result data
        error (Optional[str]): Human-readable error message if operation failed
        error_code (Optional[str]): Standardized error code for programmatic handling
        duration (float): Operation execution time in seconds
        metadata (Optional[Dict[str, Any]]): Additional operation metadata
            (skill name, version, operation name, warnings, etc.)
    """
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    duration: float = 0.0
    metadata: Optional[Dict[str, Any]] = None


class ErrorCodes:
    """
    Standard error codes used across all operations.

    Use these codes for consistent error handling across the skill.
    """
    VALIDATION_ERROR = "VALIDATION_ERROR"      # Invalid input parameters
    OPERATION_ERROR = "OPERATION_ERROR"        # General operation failure
    FILE_NOT_FOUND = "FILE_NOT_FOUND"          # File or directory not found
    PERMISSION_DENIED = "PERMISSION_DENIED"    # Insufficient permissions
    TIMEOUT = "TIMEOUT"                        # Operation exceeded time limit
    DEPENDENCY_ERROR = "DEPENDENCY_ERROR"      # Missing required dependency
    PARSE_ERROR = "PARSE_ERROR"                # Parsing failed
    NETWORK_ERROR = "NETWORK_ERROR"            # Network request failed


{{OPERATIONS_FUNCTIONS}}


# Internal helper functions (prefix with underscore)
def _validate_input(param: Any, param_name: str) -> None:
    """
    Validate input parameter.

    Args:
        param: Parameter to validate
        param_name: Name of parameter for error messages

    Raises:
        ValueError: If parameter is invalid
    """
    if param is None or (isinstance(param, str) and not param.strip()):
        raise ValueError(f"{param_name} is required and cannot be empty")


def _build_metadata(operation_name: str, **kwargs) -> Dict[str, Any]:
    """
    Build metadata dictionary for operation result.

    Args:
        operation_name: Name of the operation
        **kwargs: Additional metadata fields

    Returns:
        Dict containing skill metadata
    """
    metadata = {
        "skill": "{{SKILL_NAME}}",
        "version": "0.1.0",
        "operation": operation_name,
    }
    metadata.update(kwargs)
    return metadata

"""
MCP Adapter Creator Operations.

Creates MCP adapter files for skills following Anthropic best practices.
"""

import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class OperationResult:
    """Result from an operation."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    duration: float = 0.0
    metadata: Optional[Dict[str, Any]] = None


class ErrorCodes:
    """Standard error codes."""
    VALIDATION_ERROR = "VALIDATION_ERROR"
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    OPERATION_ERROR = "OPERATION_ERROR"


def _get_project_root() -> Path:
    """Get project root directory."""
    return Path(__file__).parents[2]


def _generate_adapter_template(skill_name: str, operations: List[Dict[str, Any]]) -> str:
    """
    Generate adapter template code.

    Args:
        skill_name: Name of skill
        operations: List of operations with metadata

    Returns:
        Adapter code as string
    """
    operations_dict = {}
    for op in operations:
        operations_dict[op['name']] = {
            'description': op.get('description', f"{op['name']} operation"),
            'parameters': op.get('parameters', {}),
            'returns': op.get('returns', 'Operation result'),
            'example': f'''
from skills.{skill_name} import {op['name']}
from skills.common.filters import ResultFilter

# Execute operation
result = {op['name']}(params)

# Filter locally (98.7% token savings!)
filtered = ResultFilter.limit(result.data, 10)
'''
        }

    import json
    operations_json = json.dumps(operations_dict, indent=4)

    adapter_code = f'''"""
MCP Adapter for {skill_name} skill.

Exposes {skill_name} operations via MCP with local filtering.
Enables 98.7% token reduction by processing data locally.

Example usage in agent-generated code:
    from skills.{skill_name} import {{operation_name}}
    from skills.common.filters import ResultFilter

    # Execute operation
    result = {{operation_name}}(params)

    # Filter locally (token efficiency!)
    filtered = ResultFilter.limit(result, 10)
"""

# This adapter file documents the available operations from {skill_name} skill.
# The actual imports happen in the sandboxed code execution environment.

OPERATIONS = {operations_json}


def get_operation_docs() -> dict:
    """Get documentation for all operations."""
    return OPERATIONS
'''

    return adapter_code


def create_adapter(
    skill_name: str,
    operations: Optional[List[str]] = None,
    output_path: Optional[str] = None,
    response_format: str = "summary"
) -> OperationResult:
    """
    Create MCP adapter for a skill.

    Args:
        skill_name: Name of skill (e.g., "code_analysis")
        operations: Optional list of specific operations to include
        output_path: Optional output path for adapter file
        response_format: "summary" for metadata only, "complete" for full code

    Returns:
        OperationResult with adapter data

    Example:
        result = create_adapter("code_analysis", response_format="complete")
        if result.success:
            print(f"Adapter: {result.data['adapter_path']}")
    """
    start_time = time.time()

    try:
        # Get project root
        project_root = _get_project_root()
        skills_dir = project_root / "skills"
        skill_path = skills_dir / skill_name

        if not skill_path.exists():
            skill_path = skills_dir / skill_name.replace('-', '_')

        if not skill_path.exists():
            available = [p.name for p in skills_dir.iterdir() if p.is_dir() and not p.name.startswith('.')]
            return OperationResult(
                success=False,
                error=f"Skill '{skill_name}' not found. Available: {', '.join(sorted(available))}",
                error_code=ErrorCodes.FILE_NOT_FOUND,
                duration=time.time() - start_time
            )

        # Use mcp_schema_generator to get operations
        try:
            from skills.mcp_schema_generator import generate_schema

            schema_result = generate_schema(skill_name, response_format="complete")
            if not schema_result.success:
                return OperationResult(
                    success=False,
                    error=f"Failed to get schema: {schema_result.error}",
                    error_code=ErrorCodes.OPERATION_ERROR,
                    duration=time.time() - start_time
                )

            # Extract operations from schema
            skill_operations = []
            for schema in schema_result.data.get('schemas', []):
                op_name = schema['tool_name'].split('.')[-1]
                if operations is None or op_name in operations:
                    skill_operations.append({
                        'name': op_name,
                        'description': schema['description'],
                        'parameters': schema['input_schema'].get('properties', {}),
                        'returns': 'OperationResult'
                    })

            if not skill_operations:
                return OperationResult(
                    success=False,
                    error=f"No operations found for skill '{skill_name}'",
                    error_code=ErrorCodes.VALIDATION_ERROR,
                    duration=time.time() - start_time
                )

            # Generate adapter code
            adapter_code = _generate_adapter_template(skill_name, skill_operations)

            # Determine output path
            if output_path is None:
                mcp_adapters_dir = project_root / "mcp" / "servers" / "skills-mcp" / "adapters"
                mcp_adapters_dir.mkdir(parents=True, exist_ok=True)
                output_path = str(mcp_adapters_dir / f"{skill_name}.py")

            # Prepare response
            if response_format == "summary":
                data = {
                    'skill_name': skill_name,
                    'adapter_path': output_path,
                    'operations_count': len(skill_operations),
                    'operations': [op['name'] for op in skill_operations]
                }
            else:  # complete
                data = {
                    'skill_name': skill_name,
                    'adapter_path': output_path,
                    'adapter_code': adapter_code,
                    'operations_count': len(skill_operations),
                    'operations': skill_operations
                }

            return OperationResult(
                success=True,
                data=data,
                duration=time.time() - start_time,
                metadata={
                    'skill': skill_name,
                    'format': response_format
                }
            )

        except ImportError:
            return OperationResult(
                success=False,
                error="mcp_schema_generator skill not found. Install required dependency.",
                error_code=ErrorCodes.OPERATION_ERROR,
                duration=time.time() - start_time
            )

    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Failed to create adapter: {str(e)}",
            error_code=ErrorCodes.OPERATION_ERROR,
            duration=time.time() - start_time
        )


def create_batch_adapters(
    skills: List[Dict[str, Any]],
    output_dir: Optional[str] = None,
    response_format: str = "summary"
) -> OperationResult:
    """
    Create adapters for multiple skills.

    Args:
        skills: List of skill configs [{{"name": "skill_name", "operations": [...]}}]
        output_dir: Optional output directory
        response_format: "summary" or "complete"

    Returns:
        OperationResult with batch creation results

    Example:
        result = create_batch_adapters([
            {{"name": "code_analysis"}},
            {{"name": "test_orchestrator"}}
        ])
    """
    start_time = time.time()

    try:
        adapters = []
        failed = []

        for skill_config in skills:
            skill_name = skill_config['name']
            operations = skill_config.get('operations')

            result = create_adapter(
                skill_name=skill_name,
                operations=operations,
                output_path=None,
                response_format="complete"
            )

            if result.success:
                adapters.append(result.data)
            else:
                failed.append({
                    'skill': skill_name,
                    'error': result.error
                })

        # Prepare response
        if response_format == "summary":
            data = {
                'total_skills': len(skills),
                'successful': len(adapters),
                'failed': len(failed),
                'total_adapters': len(adapters),
                'failed_skills': failed
            }
        else:  # complete
            data = {
                'adapters': adapters,
                'total_adapters': len(adapters),
                'failed_skills': failed
            }

        return OperationResult(
            success=True,
            data=data,
            duration=time.time() - start_time
        )

    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Failed to create batch adapters: {str(e)}",
            error_code=ErrorCodes.OPERATION_ERROR,
            duration=time.time() - start_time
        )

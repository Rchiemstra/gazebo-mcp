"""
MCP Schema Generator Operations.

Generates MCP tool schemas from skill operations following Anthropic best practices.
"""

import ast
import time
import yaml
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict

# Define locally following the pattern from other skills
class ErrorCodes:
    """Standard error codes."""
    VALIDATION_ERROR = "VALIDATION_ERROR"
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    OPERATION_ERROR = "OPERATION_ERROR"


@dataclass
class OperationResult:
    """Result from an operation."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    duration: float = 0.0
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class MCPSchema:
    """MCP tool schema structure."""
    tool_name: str
    description: str
    input_schema: Dict[str, Any]
    examples: List[Dict[str, str]]
    warnings: List[str] = None

    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []


def _get_project_root() -> Path:
    """Get project root directory."""
    return Path(__file__).parents[2]


def _read_skill_metadata(skill_path: Path) -> Optional[Dict[str, Any]]:
    """
    Read skill metadata from SKILL.md YAML frontmatter.

    Args:
        skill_path: Path to skill directory

    Returns:
        Dict with metadata or None if not found
    """
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        skill_md = skill_path / "skill.md"

    if not skill_md.exists():
        return None

    try:
        with open(skill_md, 'r') as f:
            content = f.read()

        # Extract YAML frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1].strip()
                metadata = yaml.safe_load(frontmatter)
                return metadata

    except Exception:
        pass

    return None


def _extract_operations_from_file(file_path: Path) -> List[Dict[str, Any]]:
    """
    Extract operations from operations.py using AST parsing.

    Args:
        file_path: Path to operations.py

    Returns:
        List of operation definitions
    """
    if not file_path.exists():
        return []

    operations = []

    try:
        with open(file_path, 'r') as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Skip private functions
                if node.name.startswith('_'):
                    continue

                # Extract docstring
                docstring = ast.get_docstring(node) or ""

                # Extract parameters
                params = []
                required_params = []

                for arg in node.args.args:
                    # Skip 'self' parameter
                    if arg.arg == 'self':
                        continue

                    param_type = "string"  # Default
                    param_desc = ""

                    # Try to extract type from annotation
                    if arg.annotation:
                        if isinstance(arg.annotation, ast.Name):
                            type_name = arg.annotation.id
                            if type_name in ['int', 'float']:
                                param_type = "number"
                            elif type_name == 'bool':
                                param_type = "boolean"
                            elif type_name in ['List', 'list']:
                                param_type = "array"
                            elif type_name in ['Dict', 'dict']:
                                param_type = "object"

                    params.append({
                        'name': arg.arg,
                        'type': param_type,
                        'description': param_desc
                    })

                    # Check if parameter has default value
                    num_defaults = len(node.args.defaults)
                    num_args = len(node.args.args) - 1  # Exclude self
                    param_index = node.args.args.index(arg) - 1  # Account for self

                    if param_index < (num_args - num_defaults):
                        required_params.append(arg.arg)

                operations.append({
                    'name': node.name,
                    'docstring': docstring,
                    'parameters': params,
                    'required': required_params
                })

    except Exception:
        pass

    return operations


def _generate_example_code(skill_name: str, operation_name: str, parameters: List[Dict]) -> str:
    """
    Generate example code for an operation.

    Args:
        skill_name: Skill name
        operation_name: Operation name
        parameters: List of parameters

    Returns:
        Example code string
    """
    # Build example parameters
    example_params = []
    for param in parameters:
        if param['name'] in ['response_format', 'options']:
            continue  # Skip these common params in examples

        if param['type'] == 'string':
            example_params.append(f'"{param["name"]}_value"')
        elif param['type'] == 'number':
            example_params.append('10')
        elif param['type'] == 'boolean':
            example_params.append('True')
        elif param['type'] == 'array':
            example_params.append('[]')
        elif param['type'] == 'object':
            example_params.append('{}')
        else:
            example_params.append('None')

    params_str = ', '.join(example_params)

    return f"""from skills.{skill_name} import {operation_name}
from skills.common.filters import ResultFilter

# Execute operation
result = {operation_name}({params_str})

if result.success:
    # Filter results locally (token efficiency!)
    filtered = ResultFilter.limit(result.data, 10)
    print(filtered)
"""


def generate_schema(
    skill_name: str,
    operations: Optional[List[str]] = None,
    response_format: str = "summary"
) -> OperationResult:
    """
    Generate MCP schema for a skill.

    Args:
        skill_name: Name of skill (e.g., "code_analysis")
        operations: Optional list of specific operations to include
        response_format: "summary" for metadata only, "complete" for full schema

    Returns:
        OperationResult with:
            - success: bool
            - data: Dict with schema(s)
            - error: str if failed

    Example:
        result = generate_schema("code_analysis", response_format="complete")
        if result.success:
            schema = result.data
            print(schema['tool_name'])
    """
    start_time = time.time()

    try:
        # Get project root
        project_root = _get_project_root()
        skills_dir = project_root / "skills"

        # Find skill directory
        skill_path = skills_dir / skill_name
        if not skill_path.exists():
            # Try with underscores
            skill_path = skills_dir / skill_name.replace('-', '_')

        if not skill_path.exists():
            # List available skills
            available = [p.name for p in skills_dir.iterdir() if p.is_dir() and not p.name.startswith('.')]
            return OperationResult(
                success=False,
                error=f"Skill '{skill_name}' not found. Available skills: {', '.join(sorted(available))}",
                error_code=ErrorCodes.VALIDATION_ERROR,
                duration=time.time() - start_time
            )

        # Read skill metadata
        metadata = _read_skill_metadata(skill_path)
        if not metadata:
            return OperationResult(
                success=False,
                error=f"Could not read metadata for skill '{skill_name}'. Ensure skill has SKILL.md with YAML frontmatter",
                error_code=ErrorCodes.FILE_NOT_FOUND,
                duration=time.time() - start_time
            )

        # Extract operations from operations.py
        operations_file = skill_path / "operations.py"
        extracted_operations = _extract_operations_from_file(operations_file)

        if not extracted_operations:
            return OperationResult(
                success=False,
                error=f"No operations found in {skill_name}/operations.py. Ensure operations.py contains public functions",
                error_code=ErrorCodes.VALIDATION_ERROR,
                duration=time.time() - start_time
            )

        # Filter to requested operations
        if operations:
            extracted_operations = [
                op for op in extracted_operations
                if op['name'] in operations
            ]

        # Generate schemas
        schemas = []
        warnings = []

        for op in extracted_operations:
            # Build input schema
            properties = {}
            required = []

            for param in op['parameters']:
                properties[param['name']] = {
                    'type': param['type'],
                    'description': param.get('description', f"Parameter {param['name']}")
                }

            required = op.get('required', [])

            # Generate schema
            schema = MCPSchema(
                tool_name=f"{skill_name}.{op['name']}",
                description=op['docstring'].split('\n')[0] if op['docstring'] else f"{op['name']} operation",
                input_schema={
                    'type': 'object',
                    'properties': properties,
                    'required': required
                },
                examples=[
                    {
                        'description': f"Basic usage of {op['name']}",
                        'code': _generate_example_code(skill_name, op['name'], op['parameters'])
                    }
                ],
                warnings=[]
            )

            # Add warnings for common issues
            if not op['docstring']:
                schema.warnings.append(f"Operation {op['name']} missing docstring")

            if not required:
                schema.warnings.append(f"Operation {op['name']} has no required parameters")

            schemas.append(schema)

        # Prepare response based on format
        if response_format == "summary":
            data = {
                'skill_name': skill_name,
                'operations_count': len(schemas),
                'operations': [s.tool_name for s in schemas],
                'has_warnings': any(s.warnings for s in schemas)
            }
        else:  # complete
            data = {
                'skill_name': skill_name,
                'skill_description': metadata.get('description', ''),
                'schemas': [asdict(s) for s in schemas],
                'operations_count': len(schemas)
            }

        return OperationResult(
            success=True,
            data=data,
            duration=time.time() - start_time,
            metadata={
                'skill': skill_name,
                'format': response_format,
                'operations': len(schemas)
            }
        )

    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Failed to generate schema: {str(e)}",
            error_code=ErrorCodes.OPERATION_ERROR,
            duration=time.time() - start_time
        )


def validate_schema(schema: Dict[str, Any]) -> OperationResult:
    """
    Validate MCP schema structure and completeness.

    Args:
        schema: MCP schema dictionary to validate

    Returns:
        OperationResult with:
            - success: bool
            - data: Dict with validation results
                - valid: bool
                - errors: List[str]
                - warnings: List[str]

    Example:
        schema = {...}
        result = validate_schema(schema)
        if result.success and result.data['valid']:
            print("Schema is valid!")
    """
    start_time = time.time()

    try:
        errors = []
        warnings = []

        # Check required top-level fields
        required_fields = ['tool_name', 'description', 'input_schema']
        for field in required_fields:
            if field not in schema:
                errors.append(f"Missing required field: {field}")

        # Validate tool_name format
        if 'tool_name' in schema:
            if '.' not in schema['tool_name']:
                warnings.append("tool_name should follow 'skill_name.operation_name' format")

        # Validate description
        if 'description' in schema:
            if len(schema['description']) < 10:
                warnings.append("description is too short (< 10 characters)")
            if len(schema['description']) > 500:
                warnings.append("description is very long (> 500 characters)")

        # Validate input_schema
        if 'input_schema' in schema:
            input_schema = schema['input_schema']

            if not isinstance(input_schema, dict):
                errors.append("input_schema must be a dictionary")
            else:
                # Check schema structure
                if 'type' not in input_schema:
                    errors.append("input_schema missing 'type' field")
                elif input_schema['type'] != 'object':
                    warnings.append("input_schema type should typically be 'object'")

                if 'properties' not in input_schema:
                    warnings.append("input_schema missing 'properties' field")

                # Validate properties
                if 'properties' in input_schema:
                    props = input_schema['properties']
                    if not isinstance(props, dict):
                        errors.append("input_schema properties must be a dictionary")
                    else:
                        for prop_name, prop_def in props.items():
                            if 'type' not in prop_def:
                                errors.append(f"Property '{prop_name}' missing 'type' field")
                            if 'description' not in prop_def:
                                warnings.append(f"Property '{prop_name}' missing 'description' field")

        # Check for examples
        if 'examples' not in schema:
            warnings.append("Schema missing 'examples' field")
        elif not schema['examples']:
            warnings.append("Schema has empty 'examples' list")

        valid = len(errors) == 0

        return OperationResult(
            success=True,
            data={
                'valid': valid,
                'errors': errors,
                'warnings': warnings,
                'score': max(0, 100 - (len(errors) * 20) - (len(warnings) * 5))
            },
            duration=time.time() - start_time
        )

    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Failed to validate schema: {str(e)}",
            error_code=ErrorCodes.VALIDATION_ERROR,
            duration=time.time() - start_time
        )


def generate_batch_schemas(
    skill_names: List[str],
    response_format: str = "summary"
) -> OperationResult:
    """
    Generate schemas for multiple skills.

    Args:
        skill_names: List of skill names
        response_format: "summary" or "complete"

    Returns:
        OperationResult with:
            - success: bool
            - data: Dict with schemas and metadata

    Example:
        result = generate_batch_schemas(["code_analysis", "test_orchestrator"])
        if result.success:
            print(f"Generated {result.data['total_schemas']} schemas")
    """
    start_time = time.time()

    try:
        schemas = []
        failed = []

        for skill_name in skill_names:
            result = generate_schema(skill_name, response_format="complete")
            if result.success:
                schemas.extend(result.data.get('schemas', []))
            else:
                failed.append({
                    'skill': skill_name,
                    'error': result.error
                })

        # Prepare response
        if response_format == "summary":
            data = {
                'total_skills': len(skill_names),
                'successful': len(skill_names) - len(failed),
                'failed': len(failed),
                'total_schemas': len(schemas),
                'failed_skills': failed
            }
        else:  # complete
            data = {
                'schemas': schemas,
                'total_schemas': len(schemas),
                'failed_skills': failed,
                'metadata': {
                    'total_skills': len(skill_names),
                    'successful': len(skill_names) - len(failed)
                }
            }

        return OperationResult(
            success=True,
            data=data,
            duration=time.time() - start_time,
            metadata={
                'format': response_format,
                'skills': len(skill_names)
            }
        )

    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Failed to generate batch schemas: {str(e)}",
            error_code=ErrorCodes.OPERATION_ERROR,
            duration=time.time() - start_time
        )

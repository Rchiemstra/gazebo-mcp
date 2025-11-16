"""
Docstring Generator

Generates comprehensive docstrings for Python code.
"""

import ast
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Dict, Optional, Any


class DocstringStyle(Enum):
    """Supported docstring styles."""
    GOOGLE = "google"
    NUMPY = "numpy"
    SPHINX = "sphinx"


@dataclass
class GeneratedDocstring:
    """A generated docstring."""
    target: str  # Function or class name
    line_number: int
    original_docstring: Optional[str]
    generated_docstring: str
    style: DocstringStyle


@dataclass
class DocstringResult:
    """Results of docstring generation."""
    original_code: str
    documented_code: str
    docstrings_added: int
    docstrings_updated: int
    coverage_before: float
    coverage_after: float
    generated_docstrings: List[GeneratedDocstring]


class DocstringGenerator:
    """Generates comprehensive docstrings for Python code."""

    def __init__(self, style: str = "google"):
        """
        Initialize docstring generator.

        Args:
            style: Docstring style ('google', 'numpy', or 'sphinx')
        """
        self.style = DocstringStyle(style.lower())
        self.generated: List[GeneratedDocstring] = []

    def generate_for_file(
        self,
        file_path: str,
        include_examples: bool = False
    ) -> DocstringResult:
        """
        Generate docstrings for all functions and classes in a file.

        Args:
            file_path: Path to Python file
            include_examples: Whether to include usage examples

        Returns:
            Results with original and documented code
        """
        # Read original code
        with open(file_path, 'r', encoding='utf-8') as f:
            original_code = f.read()

        # Parse AST
        try:
            tree = ast.parse(original_code)
        except SyntaxError:
            return DocstringResult(
                original_code=original_code,
                documented_code=original_code,
                docstrings_added=0,
                docstrings_updated=0,
                coverage_before=0.0,
                coverage_after=0.0,
                generated_docstrings=[]
            )

        # Calculate coverage before
        coverage_before = self._calculate_coverage(tree)

        # Generate docstrings
        self._process_tree(tree, include_examples)

        # Generate new code
        documented_code = ast.unparse(tree)

        # Calculate coverage after
        coverage_after = self._calculate_coverage(tree)

        # Count additions and updates
        added = sum(1 for d in self.generated if d.original_docstring is None)
        updated = sum(1 for d in self.generated if d.original_docstring is not None)

        return DocstringResult(
            original_code=original_code,
            documented_code=documented_code,
            docstrings_added=added,
            docstrings_updated=updated,
            coverage_before=coverage_before,
            coverage_after=coverage_after,
            generated_docstrings=self.generated.copy()
        )

    def _process_tree(self, tree: ast.AST, include_examples: bool):
        """Process AST tree and add docstrings."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self._add_function_docstring(node, include_examples)
            elif isinstance(node, ast.ClassDef):
                self._add_class_docstring(node)

    def _add_function_docstring(
        self,
        node: ast.FunctionDef,
        include_examples: bool
    ):
        """Add or update function docstring."""
        existing_docstring = ast.get_docstring(node)

        # Skip if already has good docstring
        if existing_docstring and len(existing_docstring) > 50:
            return

        # Extract function information
        params = self._extract_parameters(node)
        return_type = self._extract_return_type(node)
        raises = self._extract_raises(node)

        # Generate docstring
        docstring = self._generate_function_docstring(
            node.name,
            params,
            return_type,
            raises,
            include_examples
        )

        # Create docstring node
        docstring_node = ast.Expr(value=ast.Constant(value=docstring))

        # Insert docstring
        if node.body and isinstance(node.body[0], ast.Expr) and \
           isinstance(node.body[0].value, ast.Constant):
            # Replace existing docstring
            node.body[0] = docstring_node
        else:
            # Insert new docstring
            node.body.insert(0, docstring_node)

        # Track generation
        self.generated.append(GeneratedDocstring(
            target=node.name,
            line_number=node.lineno,
            original_docstring=existing_docstring,
            generated_docstring=docstring,
            style=self.style
        ))

    def _add_class_docstring(self, node: ast.ClassDef):
        """Add or update class docstring."""
        existing_docstring = ast.get_docstring(node)

        # Skip if already has good docstring
        if existing_docstring and len(existing_docstring) > 50:
            return

        # Extract class information
        attributes = self._extract_attributes(node)
        methods = self._extract_methods(node)
        base_classes = [ast.unparse(base) for base in node.bases]

        # Generate docstring
        docstring = self._generate_class_docstring(
            node.name,
            attributes,
            methods,
            base_classes
        )

        # Create docstring node
        docstring_node = ast.Expr(value=ast.Constant(value=docstring))

        # Insert docstring
        if node.body and isinstance(node.body[0], ast.Expr) and \
           isinstance(node.body[0].value, ast.Constant):
            # Replace existing docstring
            node.body[0] = docstring_node
        else:
            # Insert new docstring
            node.body.insert(0, docstring_node)

        # Track generation
        self.generated.append(GeneratedDocstring(
            target=node.name,
            line_number=node.lineno,
            original_docstring=existing_docstring,
            generated_docstring=docstring,
            style=self.style
        ))

    def _generate_function_docstring(
        self,
        name: str,
        params: List[Dict[str, Any]],
        return_type: Optional[str],
        raises: List[str],
        include_examples: bool
    ) -> str:
        """Generate function docstring based on style."""
        if self.style == DocstringStyle.GOOGLE:
            return self._generate_google_function(
                name, params, return_type, raises, include_examples
            )
        elif self.style == DocstringStyle.NUMPY:
            return self._generate_numpy_function(
                name, params, return_type, raises, include_examples
            )
        else:  # SPHINX
            return self._generate_sphinx_function(
                name, params, return_type, raises, include_examples
            )

    def _generate_google_function(
        self,
        name: str,
        params: List[Dict[str, Any]],
        return_type: Optional[str],
        raises: List[str],
        include_examples: bool
    ) -> str:
        """Generate Google-style docstring for function."""
        lines = [self._generate_function_description(name)]
        lines.append("")

        # Parameters
        if params:
            lines.append("Args:")
            for param in params:
                param_name = param['name']
                param_type = param.get('type', 'Any')
                param_desc = self._generate_param_description(param_name)
                lines.append(f"    {param_name} ({param_type}): {param_desc}")
            lines.append("")

        # Returns
        if return_type:
            lines.append("Returns:")
            return_desc = self._generate_return_description(name, return_type)
            lines.append(f"    {return_type}: {return_desc}")
            lines.append("")

        # Raises
        if raises:
            lines.append("Raises:")
            for exc in raises:
                exc_desc = self._generate_exception_description(exc)
                lines.append(f"    {exc}: {exc_desc}")
            lines.append("")

        # Examples
        if include_examples:
            example = self._generate_example(name, params)
            if example:
                lines.append("Example:")
                lines.append(f"    >>> {example}")
                lines.append("")

        return "\n".join(lines).rstrip()

    def _generate_numpy_function(
        self,
        name: str,
        params: List[Dict[str, Any]],
        return_type: Optional[str],
        raises: List[str],
        include_examples: bool
    ) -> str:
        """Generate NumPy-style docstring for function."""
        lines = [self._generate_function_description(name)]
        lines.append("")

        # Parameters
        if params:
            lines.append("Parameters")
            lines.append("----------")
            for param in params:
                param_name = param['name']
                param_type = param.get('type', 'Any')
                param_desc = self._generate_param_description(param_name)
                lines.append(f"{param_name} : {param_type}")
                lines.append(f"    {param_desc}")
            lines.append("")

        # Returns
        if return_type:
            lines.append("Returns")
            lines.append("-------")
            return_desc = self._generate_return_description(name, return_type)
            lines.append(f"{return_type}")
            lines.append(f"    {return_desc}")
            lines.append("")

        # Raises
        if raises:
            lines.append("Raises")
            lines.append("------")
            for exc in raises:
                exc_desc = self._generate_exception_description(exc)
                lines.append(f"{exc}")
                lines.append(f"    {exc_desc}")
            lines.append("")

        # Examples
        if include_examples:
            example = self._generate_example(name, params)
            if example:
                lines.append("Examples")
                lines.append("--------")
                lines.append(f">>> {example}")
                lines.append("")

        return "\n".join(lines).rstrip()

    def _generate_sphinx_function(
        self,
        name: str,
        params: List[Dict[str, Any]],
        return_type: Optional[str],
        raises: List[str],
        include_examples: bool
    ) -> str:
        """Generate Sphinx-style docstring for function."""
        lines = [self._generate_function_description(name)]
        lines.append("")

        # Parameters
        for param in params:
            param_name = param['name']
            param_type = param.get('type', 'Any')
            param_desc = self._generate_param_description(param_name)
            lines.append(f":param {param_name}: {param_desc}")
            lines.append(f":type {param_name}: {param_type}")

        if params:
            lines.append("")

        # Returns
        if return_type:
            return_desc = self._generate_return_description(name, return_type)
            lines.append(f":returns: {return_desc}")
            lines.append(f":rtype: {return_type}")
            lines.append("")

        # Raises
        for exc in raises:
            exc_desc = self._generate_exception_description(exc)
            lines.append(f":raises {exc}: {exc_desc}")

        if raises:
            lines.append("")

        return "\n".join(lines).rstrip()

    def _generate_class_docstring(
        self,
        name: str,
        attributes: List[str],
        methods: List[str],
        base_classes: List[str]
    ) -> str:
        """Generate class docstring."""
        lines = [self._generate_class_description(name)]
        lines.append("")

        # Base classes
        if base_classes:
            bases = ", ".join(base_classes)
            lines.append(f"Inherits from: {bases}")
            lines.append("")

        # Attributes
        if attributes and self.style == DocstringStyle.GOOGLE:
            lines.append("Attributes:")
            for attr in attributes:
                attr_desc = self._generate_attribute_description(attr)
                lines.append(f"    {attr}: {attr_desc}")
            lines.append("")
        elif attributes and self.style == DocstringStyle.NUMPY:
            lines.append("Attributes")
            lines.append("----------")
            for attr in attributes:
                attr_desc = self._generate_attribute_description(attr)
                lines.append(f"{attr} : type")
                lines.append(f"    {attr_desc}")
            lines.append("")

        return "\n".join(lines).rstrip()

    def _generate_function_description(self, name: str) -> str:
        """Generate function description from name."""
        # Convert snake_case or camelCase to words
        words = []
        current_word = []

        for i, char in enumerate(name):
            if char == '_':
                if current_word:
                    words.append(''.join(current_word))
                    current_word = []
            elif char.isupper() and i > 0:
                if current_word:
                    words.append(''.join(current_word))
                current_word = [char.lower()]
            else:
                current_word.append(char.lower())

        if current_word:
            words.append(''.join(current_word))

        if not words:
            return "TODO: Add description"

        # Generate description
        description = ' '.join(words).capitalize()
        return f"{description}."

    def _generate_class_description(self, name: str) -> str:
        """Generate class description from name."""
        description = self._generate_function_description(name)
        return f"{description[:-1]} class."

    def _generate_param_description(self, param_name: str) -> str:
        """Generate parameter description from name."""
        if param_name in ('self', 'cls'):
            return ""

        # Common parameter patterns
        descriptions = {
            'id': 'Unique identifier',
            'name': 'Name identifier',
            'path': 'File or directory path',
            'file_path': 'Path to file',
            'dir_path': 'Path to directory',
            'url': 'URL address',
            'data': 'Data to process',
            'value': 'Value to use',
            'count': 'Number of items',
            'index': 'Index position',
            'key': 'Dictionary key',
            'timeout': 'Timeout in seconds',
            'verbose': 'Enable verbose output',
            'debug': 'Enable debug mode',
        }

        if param_name in descriptions:
            return descriptions[param_name]

        # Generate from name
        description = self._generate_function_description(param_name)
        return description[:-1]  # Remove period

    def _generate_return_description(self, func_name: str, return_type: str) -> str:
        """Generate return value description."""
        type_descriptions = {
            'bool': 'True if successful, False otherwise',
            'int': 'Integer result',
            'float': 'Float result',
            'str': 'String result',
            'list': 'List of results',
            'dict': 'Dictionary with results',
            'None': 'None',
        }

        if return_type in type_descriptions:
            return type_descriptions[return_type]

        return f"Result of {func_name} operation"

    def _generate_attribute_description(self, attr_name: str) -> str:
        """Generate attribute description from name."""
        return self._generate_param_description(attr_name)

    def _generate_exception_description(self, exc_name: str) -> str:
        """Generate exception description."""
        descriptions = {
            'ValueError': 'If input value is invalid',
            'TypeError': 'If input type is incorrect',
            'FileNotFoundError': 'If file does not exist',
            'KeyError': 'If key is not found',
            'IndexError': 'If index is out of range',
            'IOError': 'If I/O operation fails',
            'RuntimeError': 'If operation fails at runtime',
        }

        return descriptions.get(exc_name, 'If operation fails')

    def _generate_example(self, func_name: str, params: List[Dict[str, Any]]) -> str:
        """Generate usage example."""
        if not params:
            return f"{func_name}()"

        # Generate example parameters
        example_params = []
        for param in params[:3]:  # Max 3 params in example
            if param['name'] in ('self', 'cls'):
                continue

            param_name = param['name']
            param_type = param.get('type', 'Any')

            # Generate example value
            example_value = self._get_example_value(param_name, param_type)
            example_params.append(f"{param_name}={example_value}")

        params_str = ", ".join(example_params)
        return f"{func_name}({params_str})"

    def _get_example_value(self, param_name: str, param_type: str) -> str:
        """Get example value for parameter."""
        # Type-based examples
        if 'str' in param_type.lower():
            if 'path' in param_name:
                return "'/path/to/file'"
            elif 'name' in param_name:
                return "'example'"
            return "'value'"
        elif 'int' in param_type.lower():
            return '42'
        elif 'float' in param_type.lower():
            return '3.14'
        elif 'bool' in param_type.lower():
            return 'True'
        elif 'list' in param_type.lower():
            return '[]'
        elif 'dict' in param_type.lower():
            return '{}'

        return 'None'

    def _extract_parameters(self, node: ast.FunctionDef) -> List[Dict[str, Any]]:
        """Extract function parameters."""
        params = []

        for arg in node.args.args:
            param_type = 'Any'
            if arg.annotation:
                param_type = ast.unparse(arg.annotation)

            params.append({
                'name': arg.arg,
                'type': param_type
            })

        return params

    def _extract_return_type(self, node: ast.FunctionDef) -> Optional[str]:
        """Extract return type annotation."""
        if node.returns:
            return ast.unparse(node.returns)
        return None

    def _extract_raises(self, node: ast.FunctionDef) -> List[str]:
        """Extract exceptions that function raises."""
        raises = []

        for item in ast.walk(node):
            if isinstance(item, ast.Raise):
                if item.exc:
                    if isinstance(item.exc, ast.Call):
                        if isinstance(item.exc.func, ast.Name):
                            raises.append(item.exc.func.id)
                    elif isinstance(item.exc, ast.Name):
                        raises.append(item.exc.id)

        return list(set(raises))

    def _extract_attributes(self, node: ast.ClassDef) -> List[str]:
        """Extract class attributes."""
        attributes = []

        for item in node.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                attributes.append(item.target.id)
            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        attributes.append(target.id)

        return attributes

    def _extract_methods(self, node: ast.ClassDef) -> List[str]:
        """Extract class methods."""
        methods = []

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append(item.name)

        return methods

    def _calculate_coverage(self, tree: ast.AST) -> float:
        """Calculate documentation coverage percentage."""
        total = 0
        documented = 0

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                total += 1
                if ast.get_docstring(node):
                    documented += 1

        if total == 0:
            return 100.0

        return (documented / total) * 100


def generate_docstrings(
    file_path: str,
    style: str = "google",
    include_examples: bool = False
) -> Dict[str, Any]:
    """
    Generate comprehensive docstrings for a Python file.

    Args:
        file_path: Path to Python file
        style: Docstring style ('google', 'numpy', or 'sphinx')
        include_examples: Whether to include usage examples in docstrings

    Returns:
        Dictionary containing:
        - original_code: Original source code
        - documented_code: Source code with generated docstrings
        - docstrings_added: Number of new docstrings added
        - docstrings_updated: Number of existing docstrings updated
        - coverage_before: Documentation coverage before (%)
        - coverage_after: Documentation coverage after (%)
        - generated: List of generated docstrings

    Example:
        >>> result = generate_docstrings(
        ...     file_path='mymodule.py',
        ...     style='google',
        ...     include_examples=True
        ... )
        >>> print(f"Added {result['docstrings_added']} docstrings")
    """
    generator = DocstringGenerator(style)
    result = generator.generate_for_file(file_path, include_examples)

    return {
        'original_code': result.original_code,
        'documented_code': result.documented_code,
        'docstrings_added': result.docstrings_added,
        'docstrings_updated': result.docstrings_updated,
        'coverage_before': result.coverage_before,
        'coverage_after': result.coverage_after,
        'generated': [
            {
                'target': d.target,
                'line_number': d.line_number,
                'original': d.original_docstring,
                'generated': d.generated_docstring,
                'style': d.style.value
            }
            for d in result.generated_docstrings
        ]
    }

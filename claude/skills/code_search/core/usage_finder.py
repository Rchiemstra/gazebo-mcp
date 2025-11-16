"""
Usage Finder

Finds all usages/references of symbols in Python code.
"""

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Optional


@dataclass
class Usage:
    """A symbol usage/reference."""
    file_path: str
    line_number: int
    column: int
    context: str
    usage_type: str  # 'call', 'reference', 'import', 'attribute', 'assignment'
    parent_function: Optional[str] = None
    parent_class: Optional[str] = None


class UsageFinder:
    """Finds all usages/references of symbols across a codebase."""

    def __init__(self, project_path: str):
        """
        Initialize usage finder.

        Args:
            project_path: Path to project root
        """
        self.project_path = Path(project_path)

    def find(
        self,
        symbol_name: str,
        definition_file: Optional[str] = None
    ) -> List[Usage]:
        """
        Find all usages of a symbol.

        Args:
            symbol_name: Name of symbol to find usages of
            definition_file: Optional file containing the definition

        Returns:
            List of usages
        """
        usages = []

        # Search all Python files
        python_files = list(self.project_path.rglob("*.py"))
        python_files = [f for f in python_files if not self._should_skip(f)]

        for file_path in python_files:
            file_usages = self._find_in_file(symbol_name, str(file_path))
            usages.extend(file_usages)

        return usages

    def _find_in_file(
        self,
        symbol_name: str,
        file_path: str
    ) -> List[Usage]:
        """Find usages in a specific file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
        except Exception:
            return []

        try:
            tree = ast.parse(source)
        except SyntaxError:
            return []

        usages = []

        # Walk the AST and find all references
        for node in ast.walk(tree):
            node_usages = self._check_node(node, symbol_name, file_path, source)
            usages.extend(node_usages)

        return usages

    def _check_node(
        self,
        node: ast.AST,
        symbol_name: str,
        file_path: str,
        source: str
    ) -> List[Usage]:
        """Check if node contains usage of symbol."""
        usages = []

        # Function call
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == symbol_name:
                usage = self._create_usage(
                    node, 'call', file_path, source, symbol_name
                )
                usages.append(usage)
            elif isinstance(node.func, ast.Attribute):
                if node.func.attr == symbol_name:
                    usage = self._create_usage(
                        node, 'call', file_path, source, symbol_name
                    )
                    usages.append(usage)

        # Name reference
        elif isinstance(node, ast.Name):
            if node.id == symbol_name:
                # Determine usage type based on context
                usage_type = self._determine_usage_type(node)
                usage = self._create_usage(
                    node, usage_type, file_path, source, symbol_name
                )
                usages.append(usage)

        # Attribute access
        elif isinstance(node, ast.Attribute):
            if node.attr == symbol_name:
                usage = self._create_usage(
                    node, 'attribute', file_path, source, symbol_name
                )
                usages.append(usage)

        # Import statement
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == symbol_name or alias.asname == symbol_name:
                    usage = self._create_usage(
                        node, 'import', file_path, source, symbol_name
                    )
                    usages.append(usage)

        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == symbol_name or alias.asname == symbol_name:
                    usage = self._create_usage(
                        node, 'import', file_path, source, symbol_name
                    )
                    usages.append(usage)

        # Class instantiation
        elif isinstance(node, ast.ClassDef):
            # Check base classes
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id == symbol_name:
                    usage = self._create_usage(
                        node, 'inheritance', file_path, source, symbol_name
                    )
                    usages.append(usage)

        return usages

    def _determine_usage_type(self, node: ast.Name) -> str:
        """Determine the type of name usage."""
        # Check if it's in a store context (assignment)
        if isinstance(node.ctx, ast.Store):
            return 'assignment'
        # Load context (reading the value)
        elif isinstance(node.ctx, ast.Load):
            return 'reference'
        # Del context (deletion)
        elif isinstance(node.ctx, ast.Del):
            return 'deletion'
        else:
            return 'reference'

    def _create_usage(
        self,
        node: ast.AST,
        usage_type: str,
        file_path: str,
        source: str,
        symbol_name: str
    ) -> Usage:
        """Create usage record."""
        line_number = node.lineno
        column = node.col_offset

        # Get context (surrounding lines)
        lines = source.splitlines()
        context_start = max(0, line_number - 2)
        context_end = min(len(lines), line_number + 2)
        context = '\n'.join(lines[context_start:context_end])

        # Find parent function/class
        parent_function = self._find_parent_function(node, source)
        parent_class = self._find_parent_class(node, source)

        return Usage(
            file_path=file_path,
            line_number=line_number,
            column=column,
            context=context,
            usage_type=usage_type,
            parent_function=parent_function,
            parent_class=parent_class
        )

    def _find_parent_function(self, node: ast.AST, source: str) -> Optional[str]:
        """Find the parent function containing this node."""
        # This is a simplified version - in production would use proper scope tracking
        try:
            tree = ast.parse(source)
            for func_node in ast.walk(tree):
                if isinstance(func_node, ast.FunctionDef):
                    if self._node_in_function(node, func_node):
                        return func_node.name
        except:
            pass
        return None

    def _find_parent_class(self, node: ast.AST, source: str) -> Optional[str]:
        """Find the parent class containing this node."""
        try:
            tree = ast.parse(source)
            for class_node in ast.walk(tree):
                if isinstance(class_node, ast.ClassDef):
                    if self._node_in_class(node, class_node):
                        return class_node.name
        except:
            pass
        return None

    def _node_in_function(self, node: ast.AST, func_node: ast.FunctionDef) -> bool:
        """Check if node is inside function."""
        if not hasattr(node, 'lineno') or not hasattr(func_node, 'lineno'):
            return False

        return (func_node.lineno <= node.lineno <=
                (func_node.end_lineno or func_node.lineno))

    def _node_in_class(self, node: ast.AST, class_node: ast.ClassDef) -> bool:
        """Check if node is inside class."""
        if not hasattr(node, 'lineno') or not hasattr(class_node, 'lineno'):
            return False

        return (class_node.lineno <= node.lineno <=
                (class_node.end_lineno or class_node.lineno))

    def _should_skip(self, file_path: Path) -> bool:
        """Check if file should be skipped."""
        skip_dirs = {'__pycache__', '.git', 'venv', 'env', 'node_modules', '.tox'}
        return any(skip_dir in file_path.parts for skip_dir in skip_dirs)


def find_usages(
    project_path: str,
    symbol_name: str,
    definition_file: Optional[str] = None
) -> Dict[str, Any]:
    """
    Find all usages/references of a symbol.

    Args:
        project_path: Path to project root
        symbol_name: Symbol name to find usages of
        definition_file: Optional file containing definition

    Returns:
        Dictionary with usage information

    Example:
        >>> result = find_usages(
        ...     project_path='./myproject',
        ...     symbol_name='process_data',
        ...     definition_file='./myproject/core.py'
        ... )
        >>> print(f"Found {result['total_usages']} usages")
        >>> for usage in result['usages']:
        ...     print(f"  {usage['file_path']}:{usage['line_number']} ({usage['usage_type']})")
    """
    finder = UsageFinder(project_path)
    usages = finder.find(symbol_name, definition_file)

    # Group usages by type
    usage_counts = {}
    for usage in usages:
        usage_counts[usage.usage_type] = usage_counts.get(usage.usage_type, 0) + 1

    return {
        'usages': [
            {
                'file_path': u.file_path,
                'line_number': u.line_number,
                'column': u.column,
                'context': u.context,
                'usage_type': u.usage_type,
                'parent_function': u.parent_function,
                'parent_class': u.parent_class
            }
            for u in usages
        ],
        'total_usages': len(usages),
        'usage_counts': usage_counts,
        'symbol_name': symbol_name
    }

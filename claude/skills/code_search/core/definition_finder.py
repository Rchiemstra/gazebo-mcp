"""
Definition Finder

Finds definitions of symbols in Python code.
"""

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple


@dataclass
class Definition:
    """A symbol definition."""
    file_path: str
    line_number: int
    symbol_name: str
    definition_type: str
    source_code: str
    signature: str
    docstring: Optional[str] = None
    parent_class: Optional[str] = None


class DefinitionFinder:
    """Finds definitions of symbols across a codebase."""

    def __init__(self, project_path: str):
        """
        Initialize definition finder.

        Args:
            project_path: Path to project root
        """
        self.project_path = Path(project_path)
        self._import_cache: Dict[str, str] = {}

    def find(
        self,
        symbol_name: str,
        file_context: Optional[str] = None
    ) -> Optional[Definition]:
        """
        Find the definition of a symbol.

        Args:
            symbol_name: Name of symbol to find
            file_context: Optional file where symbol is used (helps with imports)

        Returns:
            Definition if found, None otherwise
        """
        # If file context provided, check imports first
        if file_context:
            imported_def = self._find_in_imports(symbol_name, file_context)
            if imported_def:
                return imported_def

        # Search all Python files
        python_files = list(self.project_path.rglob("*.py"))
        python_files = [f for f in python_files if not self._should_skip(f)]

        for file_path in python_files:
            definition = self._find_in_file(symbol_name, str(file_path))
            if definition:
                return definition

        return None

    def _find_in_file(
        self,
        symbol_name: str,
        file_path: str
    ) -> Optional[Definition]:
        """Find definition in a specific file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
        except Exception:
            return None

        try:
            tree = ast.parse(source)
        except SyntaxError:
            return None

        # Search for definition in AST
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name == symbol_name:
                    return self._create_function_definition(node, file_path, source)

            elif isinstance(node, ast.ClassDef):
                if node.name == symbol_name:
                    return self._create_class_definition(node, file_path, source)

                # Check methods
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        if item.name == symbol_name:
                            return self._create_method_definition(
                                item, node.name, file_path, source
                            )

            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == symbol_name:
                        return self._create_variable_definition(
                            target, node, file_path, source
                        )

            elif isinstance(node, ast.AnnAssign):
                if isinstance(node.target, ast.Name) and node.target.id == symbol_name:
                    return self._create_variable_definition(
                        node.target, node, file_path, source
                    )

        return None

    def _find_in_imports(
        self,
        symbol_name: str,
        file_context: str
    ) -> Optional[Definition]:
        """Find definition by following imports."""
        try:
            with open(file_context, 'r', encoding='utf-8') as f:
                source = f.read()
        except Exception:
            return None

        try:
            tree = ast.parse(source)
        except SyntaxError:
            return None

        # Find import statements
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                # from module import symbol
                if node.module:
                    for alias in node.names:
                        imported_name = alias.asname if alias.asname else alias.name
                        if imported_name == symbol_name:
                            # Resolve module path
                            module_file = self._resolve_module(node.module, file_context)
                            if module_file:
                                return self._find_in_file(alias.name, module_file)

            elif isinstance(node, ast.Import):
                # import module
                for alias in node.names:
                    if alias.name == symbol_name or alias.asname == symbol_name:
                        module_file = self._resolve_module(alias.name, file_context)
                        if module_file:
                            return self._find_in_file(symbol_name, module_file)

        return None

    def _resolve_module(self, module_name: str, from_file: str) -> Optional[str]:
        """Resolve module name to file path."""
        # Check cache
        cache_key = f"{module_name}:{from_file}"
        if cache_key in self._import_cache:
            return self._import_cache[cache_key]

        # Convert module name to path
        parts = module_name.split('.')
        current_dir = Path(from_file).parent

        # Try relative import
        for i in range(len(parts) + 1):
            if i < len(parts):
                # Try as package
                potential_path = current_dir / '/'.join(parts[:i+1]) / '__init__.py'
                if potential_path.exists():
                    self._import_cache[cache_key] = str(potential_path)
                    return str(potential_path)

                # Try as module file
                potential_path = current_dir / f"{'/'.join(parts[:i+1])}.py"
                if potential_path.exists():
                    self._import_cache[cache_key] = str(potential_path)
                    return str(potential_path)

        # Try from project root
        for i in range(len(parts) + 1):
            if i < len(parts):
                # Try as package
                potential_path = self.project_path / '/'.join(parts[:i+1]) / '__init__.py'
                if potential_path.exists():
                    self._import_cache[cache_key] = str(potential_path)
                    return str(potential_path)

                # Try as module file
                potential_path = self.project_path / f"{'/'.join(parts[:i+1])}.py"
                if potential_path.exists():
                    self._import_cache[cache_key] = str(potential_path)
                    return str(potential_path)

        return None

    def _create_function_definition(
        self,
        node: ast.FunctionDef,
        file_path: str,
        source: str
    ) -> Definition:
        """Create definition for a function."""
        # Get signature
        args = []
        for arg in node.args.args:
            arg_str = arg.arg
            if arg.annotation:
                arg_str += f": {ast.unparse(arg.annotation)}"
            args.append(arg_str)

        return_type = ""
        if node.returns:
            return_type = f" -> {ast.unparse(node.returns)}"

        signature = f"def {node.name}({', '.join(args)}){return_type}"

        # Get source code
        lines = source.splitlines()
        source_code = '\n'.join(lines[node.lineno - 1:node.end_lineno])

        # Get docstring
        docstring = ast.get_docstring(node)

        return Definition(
            file_path=file_path,
            line_number=node.lineno,
            symbol_name=node.name,
            definition_type='function',
            source_code=source_code,
            signature=signature,
            docstring=docstring
        )

    def _create_class_definition(
        self,
        node: ast.ClassDef,
        file_path: str,
        source: str
    ) -> Definition:
        """Create definition for a class."""
        # Get base classes
        bases = [ast.unparse(base) for base in node.bases]
        bases_str = f"({', '.join(bases)})" if bases else ""

        signature = f"class {node.name}{bases_str}"

        # Get source code
        lines = source.splitlines()
        source_code = '\n'.join(lines[node.lineno - 1:node.end_lineno])

        # Get docstring
        docstring = ast.get_docstring(node)

        return Definition(
            file_path=file_path,
            line_number=node.lineno,
            symbol_name=node.name,
            definition_type='class',
            source_code=source_code,
            signature=signature,
            docstring=docstring
        )

    def _create_method_definition(
        self,
        node: ast.FunctionDef,
        parent_class: str,
        file_path: str,
        source: str
    ) -> Definition:
        """Create definition for a method."""
        definition = self._create_function_definition(node, file_path, source)
        definition.definition_type = 'method'
        definition.parent_class = parent_class
        return definition

    def _create_variable_definition(
        self,
        target: ast.Name,
        node: ast.AST,
        file_path: str,
        source: str
    ) -> Definition:
        """Create definition for a variable."""
        lines = source.splitlines()
        source_code = lines[node.lineno - 1]

        signature = target.id

        return Definition(
            file_path=file_path,
            line_number=node.lineno,
            symbol_name=target.id,
            definition_type='variable',
            source_code=source_code,
            signature=signature
        )

    def _should_skip(self, file_path: Path) -> bool:
        """Check if file should be skipped."""
        skip_dirs = {'__pycache__', '.git', 'venv', 'env', 'node_modules', '.tox'}
        return any(skip_dir in file_path.parts for skip_dir in skip_dirs)


def find_definition(
    project_path: str,
    symbol_name: str,
    file_context: Optional[str] = None
) -> Dict[str, Any]:
    """
    Find the definition of a symbol.

    Args:
        project_path: Path to project root
        symbol_name: Name of symbol to find
        file_context: Optional file where symbol is used

    Returns:
        Dictionary with definition information

    Example:
        >>> result = find_definition(
        ...     project_path='./myproject',
        ...     symbol_name='DataProcessor',
        ...     file_context='./myproject/main.py'
        ... )
        >>> if result['found']:
        ...     print(f"Defined at {result['definition']['file_path']}:{result['definition']['line_number']}")
    """
    finder = DefinitionFinder(project_path)
    definition = finder.find(symbol_name, file_context)

    if definition:
        return {
            'found': True,
            'definition': {
                'file_path': definition.file_path,
                'line_number': definition.line_number,
                'symbol_name': definition.symbol_name,
                'definition_type': definition.definition_type,
                'source_code': definition.source_code,
                'signature': definition.signature,
                'docstring': definition.docstring,
                'parent_class': definition.parent_class
            }
        }
    else:
        return {
            'found': False,
            'definition': None
        }

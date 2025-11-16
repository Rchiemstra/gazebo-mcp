"""
Search Engine

AST-based code search with intelligent indexing.
"""

import ast
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Dict, Optional, Any, Set
import fnmatch


class SymbolType(Enum):
    """Type of code symbol."""
    FUNCTION = "function"
    CLASS = "class"
    VARIABLE = "variable"
    CONSTANT = "constant"
    IMPORT = "import"
    METHOD = "method"
    ATTRIBUTE = "attribute"
    PARAMETER = "parameter"


@dataclass
class Symbol:
    """A code symbol (function, class, variable, etc)."""
    name: str
    symbol_type: SymbolType
    file_path: str
    line_number: int
    end_line_number: int
    column: int
    signature: str
    context: str
    docstring: Optional[str] = None
    parent: Optional[str] = None  # Parent class for methods
    decorators: List[str] = field(default_factory=list)
    is_private: bool = False
    is_async: bool = False


@dataclass
class SearchMatch:
    """A search result match."""
    file_path: str
    line_number: int
    symbol_name: str
    symbol_type: str
    context: str
    signature: str
    relevance_score: float = 1.0
    docstring: Optional[str] = None


@dataclass
class CodeIndex:
    """Index of code symbols."""
    symbols: List[Symbol] = field(default_factory=list)
    file_hashes: Dict[str, str] = field(default_factory=dict)
    indexed_at: Optional[str] = None


class CodeSearchEngine:
    """
    Intelligent code search engine with AST-based indexing.

    Indexes Python code by parsing AST and extracting symbols
    (functions, classes, variables, etc) for fast searching.
    """

    def __init__(self):
        """Initialize search engine."""
        self.index: CodeIndex = CodeIndex()
        self._symbol_map: Dict[str, List[Symbol]] = {}

    def index_project(self, project_path: str) -> Dict[str, Any]:
        """
        Index all Python files in a project.

        Args:
            project_path: Path to project root

        Returns:
            Indexing statistics
        """
        project_dir = Path(project_path)

        # Find all Python files
        python_files = list(project_dir.rglob("*.py"))
        python_files = [f for f in python_files if not self._should_skip(f)]

        # Index each file
        total_symbols = 0
        for file_path in python_files:
            symbols = self._index_file(str(file_path))
            total_symbols += len(symbols)
            self.index.symbols.extend(symbols)

            # Add to symbol map for fast lookup
            for symbol in symbols:
                if symbol.name not in self._symbol_map:
                    self._symbol_map[symbol.name] = []
                self._symbol_map[symbol.name].append(symbol)

        return {
            'files_indexed': len(python_files),
            'symbols_indexed': total_symbols,
            'functions': sum(1 for s in self.index.symbols if s.symbol_type == SymbolType.FUNCTION),
            'classes': sum(1 for s in self.index.symbols if s.symbol_type == SymbolType.CLASS),
            'methods': sum(1 for s in self.index.symbols if s.symbol_type == SymbolType.METHOD),
        }

    def _index_file(self, file_path: str) -> List[Symbol]:
        """Index a single Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
        except Exception:
            return []

        try:
            tree = ast.parse(source)
        except SyntaxError:
            return []

        symbols = []

        # Extract module-level symbols
        for node in tree.body:
            symbols.extend(self._extract_symbols(node, file_path, source, None))

        return symbols

    def _extract_symbols(
        self,
        node: ast.AST,
        file_path: str,
        source: str,
        parent: Optional[str]
    ) -> List[Symbol]:
        """Extract symbols from AST node."""
        symbols = []

        if isinstance(node, ast.FunctionDef):
            symbol = self._create_function_symbol(node, file_path, source, parent)
            symbols.append(symbol)

            # Extract nested functions
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    symbols.extend(
                        self._extract_symbols(item, file_path, source, node.name)
                    )

        elif isinstance(node, ast.AsyncFunctionDef):
            symbol = self._create_function_symbol(node, file_path, source, parent, is_async=True)
            symbols.append(symbol)

        elif isinstance(node, ast.ClassDef):
            symbol = self._create_class_symbol(node, file_path, source)
            symbols.append(symbol)

            # Extract methods and nested classes
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    method_symbol = self._create_function_symbol(
                        item, file_path, source, node.name
                    )
                    method_symbol.symbol_type = SymbolType.METHOD
                    symbols.append(method_symbol)
                elif isinstance(item, ast.ClassDef):
                    symbols.extend(
                        self._extract_symbols(item, file_path, source, node.name)
                    )

        elif isinstance(node, ast.Assign):
            # Extract global/class variables
            for target in node.targets:
                if isinstance(target, ast.Name):
                    symbol = self._create_variable_symbol(
                        target, node, file_path, source, parent
                    )
                    symbols.append(symbol)

        elif isinstance(node, ast.AnnAssign):
            # Annotated assignment
            if isinstance(node.target, ast.Name):
                symbol = self._create_variable_symbol(
                    node.target, node, file_path, source, parent
                )
                symbols.append(symbol)

        return symbols

    def _create_function_symbol(
        self,
        node: ast.FunctionDef,
        file_path: str,
        source: str,
        parent: Optional[str],
        is_async: bool = False
    ) -> Symbol:
        """Create symbol for a function."""
        name = node.name
        line_number = node.lineno
        end_line_number = node.end_lineno or line_number
        column = node.col_offset

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

        signature = f"{'async ' if is_async else ''}def {name}({', '.join(args)}){return_type}"

        # Get context (surrounding lines)
        context = self._get_context(source, line_number, end_line_number)

        # Get docstring
        docstring = ast.get_docstring(node)

        # Get decorators
        decorators = [ast.unparse(d) for d in node.decorator_list]

        # Check if private
        is_private = name.startswith('_') and not name.startswith('__')

        return Symbol(
            name=name,
            symbol_type=SymbolType.FUNCTION,
            file_path=file_path,
            line_number=line_number,
            end_line_number=end_line_number,
            column=column,
            signature=signature,
            context=context,
            docstring=docstring,
            parent=parent,
            decorators=decorators,
            is_private=is_private,
            is_async=is_async
        )

    def _create_class_symbol(
        self,
        node: ast.ClassDef,
        file_path: str,
        source: str
    ) -> Symbol:
        """Create symbol for a class."""
        name = node.name
        line_number = node.lineno
        end_line_number = node.end_lineno or line_number
        column = node.col_offset

        # Get base classes
        bases = [ast.unparse(base) for base in node.bases]
        bases_str = f"({', '.join(bases)})" if bases else ""

        signature = f"class {name}{bases_str}"

        # Get context
        context = self._get_context(source, line_number, end_line_number)

        # Get docstring
        docstring = ast.get_docstring(node)

        # Get decorators
        decorators = [ast.unparse(d) for d in node.decorator_list]

        return Symbol(
            name=name,
            symbol_type=SymbolType.CLASS,
            file_path=file_path,
            line_number=line_number,
            end_line_number=end_line_number,
            column=column,
            signature=signature,
            context=context,
            docstring=docstring,
            decorators=decorators,
            is_private=name.startswith('_')
        )

    def _create_variable_symbol(
        self,
        target: ast.Name,
        node: ast.AST,
        file_path: str,
        source: str,
        parent: Optional[str]
    ) -> Symbol:
        """Create symbol for a variable."""
        name = target.id
        line_number = node.lineno
        end_line_number = node.end_lineno or line_number
        column = node.col_offset

        # Determine if constant (all caps)
        is_constant = name.isupper()

        signature = name
        context = self._get_context(source, line_number, line_number)

        return Symbol(
            name=name,
            symbol_type=SymbolType.CONSTANT if is_constant else SymbolType.VARIABLE,
            file_path=file_path,
            line_number=line_number,
            end_line_number=end_line_number,
            column=column,
            signature=signature,
            context=context,
            parent=parent,
            is_private=name.startswith('_')
        )

    def _get_context(self, source: str, start_line: int, end_line: int) -> str:
        """Get source code context around a line."""
        lines = source.splitlines()

        # Get a few lines before and after
        context_start = max(0, start_line - 2)
        context_end = min(len(lines), end_line + 2)

        context_lines = lines[context_start:context_end]
        return '\n'.join(context_lines)

    def search(
        self,
        symbol_name: str,
        symbol_type: Optional[str] = None,
        exact_match: bool = False,
        include_private: bool = False
    ) -> List[SearchMatch]:
        """
        Search for symbols in the index.

        Args:
            symbol_name: Symbol name to search for
            symbol_type: Optional symbol type filter
            exact_match: If True, match exact name only
            include_private: Include private symbols (_name)

        Returns:
            List of search matches
        """
        matches = []

        # Determine search method
        if exact_match:
            # Exact match - use symbol map for fast lookup
            if symbol_name in self._symbol_map:
                symbols = self._symbol_map[symbol_name]
            else:
                symbols = []
        else:
            # Fuzzy search - check all symbols
            symbols = self.index.symbols

        # Filter and score matches
        for symbol in symbols:
            # Skip if type doesn't match
            if symbol_type and symbol.symbol_type.value != symbol_type:
                continue

            # Skip private if not included
            if not include_private and symbol.is_private:
                continue

            # Check name match
            if exact_match:
                if symbol.name == symbol_name:
                    score = 1.0
                else:
                    continue
            else:
                score = self._calculate_relevance(symbol.name, symbol_name)
                if score < 0.3:  # Threshold for fuzzy match
                    continue

            # Create match
            match = SearchMatch(
                file_path=symbol.file_path,
                line_number=symbol.line_number,
                symbol_name=symbol.name,
                symbol_type=symbol.symbol_type.value,
                context=symbol.context,
                signature=symbol.signature,
                relevance_score=score,
                docstring=symbol.docstring
            )
            matches.append(match)

        # Sort by relevance
        matches.sort(key=lambda m: m.relevance_score, reverse=True)

        return matches

    def _calculate_relevance(self, symbol_name: str, search_term: str) -> float:
        """
        Calculate relevance score between symbol name and search term.

        Args:
            symbol_name: Name of the symbol
            search_term: Search term

        Returns:
            Relevance score (0.0 to 1.0)
        """
        symbol_lower = symbol_name.lower()
        search_lower = search_term.lower()

        # Exact match
        if symbol_lower == search_lower:
            return 1.0

        # Starts with
        if symbol_lower.startswith(search_lower):
            return 0.9

        # Contains
        if search_lower in symbol_lower:
            return 0.7

        # Wildcard/glob match
        if fnmatch.fnmatch(symbol_lower, search_lower):
            return 0.8

        # Substring ratio
        matching_chars = sum(1 for c in search_lower if c in symbol_lower)
        ratio = matching_chars / len(search_lower)

        return ratio * 0.6

    def _should_skip(self, file_path: Path) -> bool:
        """Check if file should be skipped."""
        skip_dirs = {'__pycache__', '.git', 'venv', 'env', 'node_modules', '.tox', 'build', 'dist'}
        return any(skip_dir in file_path.parts for skip_dir in skip_dirs)


def search_symbol(
    project_path: str,
    symbol_name: str,
    symbol_type: str = "all",
    exact_match: bool = False,
    include_private: bool = False
) -> Dict[str, Any]:
    """
    Search for symbols in a project.

    Args:
        project_path: Path to project root
        symbol_name: Symbol name to search for
        symbol_type: Type filter ('function', 'class', 'variable', 'all')
        exact_match: If True, match exact name only
        include_private: Include private symbols

    Returns:
        Dictionary with search results

    Example:
        >>> results = search_symbol(
        ...     project_path='./myproject',
        ...     symbol_name='process_*',
        ...     symbol_type='function'
        ... )
        >>> for match in results['matches']:
        ...     print(f"{match['file_path']}:{match['line_number']}")
    """
    # Create search engine and index project
    engine = CodeSearchEngine()
    index_stats = engine.index_project(project_path)

    # Perform search
    symbol_type_filter = None if symbol_type == "all" else symbol_type
    matches = engine.search(
        symbol_name=symbol_name,
        symbol_type=symbol_type_filter,
        exact_match=exact_match,
        include_private=include_private
    )

    return {
        'matches': [
            {
                'file_path': m.file_path,
                'line_number': m.line_number,
                'symbol_name': m.symbol_name,
                'symbol_type': m.symbol_type,
                'context': m.context,
                'signature': m.signature,
                'relevance_score': m.relevance_score,
                'docstring': m.docstring
            }
            for m in matches
        ],
        'total_matches': len(matches),
        'index_stats': index_stats
    }


def search_pattern(
    project_path: str,
    pattern: str,
    language: str = "python"
) -> Dict[str, Any]:
    """
    Search for code patterns using regex.

    Args:
        project_path: Path to project root
        pattern: Regex pattern to search for
        language: Programming language (currently only 'python')

    Returns:
        Dictionary with pattern matches

    Example:
        >>> results = search_pattern(
        ...     project_path='./myproject',
        ...     pattern=r'def\s+test_\w+\(.*\):'
        ... )
        >>> print(f"Found {results['total_matches']} test functions")
    """
    project_dir = Path(project_path)
    python_files = list(project_dir.rglob("*.py"))

    matches = []
    regex = re.compile(pattern)

    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            for line_num, line in enumerate(content.splitlines(), 1):
                if regex.search(line):
                    # Get context
                    lines = content.splitlines()
                    start = max(0, line_num - 2)
                    end = min(len(lines), line_num + 2)
                    context = '\n'.join(lines[start:end])

                    matches.append({
                        'file_path': str(file_path),
                        'line_number': line_num,
                        'matched_code': line,
                        'context': context,
                        'similarity_score': 1.0
                    })

        except Exception:
            continue

    return {
        'matches': matches,
        'total_matches': len(matches),
        'pattern': pattern
    }

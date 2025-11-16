"""
Code Analyzer for Test Orchestrator

Analyzes Python source code to extract functions, parameters,
return types, exceptions, and edge cases for test generation.
"""

import ast
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Set, Any


@dataclass
class FunctionInfo:
    """Information about a function for test generation."""
    name: str
    params: List[str]
    returns: Optional[str] = None
    raises: List[str] = field(default_factory=list)
    docstring: Optional[str] = None
    is_async: bool = False
    complexity: int = 0
    edge_cases: List[str] = field(default_factory=list)
    dependencies: Set[str] = field(default_factory=set)
    line_number: int = 0


@dataclass
class ClassInfo:
    """Information about a class for test generation."""
    name: str
    methods: List[FunctionInfo]
    base_classes: List[str] = field(default_factory=list)
    line_number: int = 0


@dataclass
class AnalysisResult:
    """Result of code analysis."""
    file_path: str
    functions: List[FunctionInfo]
    classes: List[ClassInfo]
    imports: Set[str]
    total_functions: int
    total_complexity: int


class CodeAnalyzer:
    """Analyzes Python source code for test generation."""

    def analyze_file(self, file_path: str) -> AnalysisResult:
        """
        Analyze a Python file and extract information for test generation.

        Args:
            file_path: Path to Python source file

        Returns:
            AnalysisResult with extracted information
        """
        with open(file_path, 'r') as f:
            source = f.read()

        tree = ast.parse(source)

        functions = []
        classes = []
        imports = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module)

        # Analyze module-level functions
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                func_info = self._analyze_function(node)
                functions.append(func_info)
            elif isinstance(node, ast.ClassDef):
                class_info = self._analyze_class(node)
                classes.append(class_info)

        total_complexity = sum(f.complexity for f in functions)
        for cls in classes:
            total_complexity += sum(m.complexity for m in cls.methods)

        total_functions = len(functions) + sum(len(cls.methods) for cls in classes)

        return AnalysisResult(
            file_path=file_path,
            functions=functions,
            classes=classes,
            imports=imports,
            total_functions=total_functions,
            total_complexity=total_complexity
        )

    def _analyze_function(self, node: ast.FunctionDef) -> FunctionInfo:
        """Analyze a function definition."""
        params = [arg.arg for arg in node.args.args if arg.arg != 'self']

        # Extract return type annotation
        returns = None
        if node.returns:
            returns = ast.unparse(node.returns)

        # Extract docstring
        docstring = ast.get_docstring(node)

        # Find raised exceptions
        raises = self._find_exceptions(node)

        # Calculate complexity
        complexity = self._calculate_complexity(node)

        # Detect edge cases
        edge_cases = self._detect_edge_cases(node, params)

        # Find dependencies (external calls)
        dependencies = self._find_dependencies(node)

        return FunctionInfo(
            name=node.name,
            params=params,
            returns=returns,
            raises=raises,
            docstring=docstring,
            is_async=isinstance(node, ast.AsyncFunctionDef),
            complexity=complexity,
            edge_cases=edge_cases,
            dependencies=dependencies,
            line_number=node.lineno
        )

    def _analyze_class(self, node: ast.ClassDef) -> ClassInfo:
        """Analyze a class definition."""
        methods = []
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                method_info = self._analyze_function(item)
                methods.append(method_info)

        base_classes = [ast.unparse(base) for base in node.bases]

        return ClassInfo(
            name=node.name,
            methods=methods,
            base_classes=base_classes,
            line_number=node.lineno
        )

    def _find_exceptions(self, node: ast.FunctionDef) -> List[str]:
        """Find exceptions that can be raised by a function."""
        exceptions = []
        for child in ast.walk(node):
            if isinstance(child, ast.Raise):
                if child.exc:
                    if isinstance(child.exc, ast.Call):
                        if isinstance(child.exc.func, ast.Name):
                            exceptions.append(child.exc.func.id)
                    elif isinstance(child.exc, ast.Name):
                        exceptions.append(child.exc.id)
        return list(set(exceptions))

    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity."""
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            # Add 1 for each decision point
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1

        return complexity

    def _detect_edge_cases(self, node: ast.FunctionDef, params: List[str]) -> List[str]:
        """Detect potential edge cases to test."""
        edge_cases = []

        # Check for None checks
        for child in ast.walk(node):
            if isinstance(child, ast.Compare):
                if any(isinstance(op, (ast.Is, ast.IsNot)) for op in child.ops):
                    for comparator in child.comparators:
                        if isinstance(comparator, ast.Constant) and comparator.value is None:
                            edge_cases.append("null_check")

        # Check for empty collection checks
        for child in ast.walk(node):
            if isinstance(child, ast.UnaryOp) and isinstance(child.op, ast.Not):
                edge_cases.append("empty_collection")

        # Check for numeric comparisons
        for child in ast.walk(node):
            if isinstance(child, ast.Compare):
                if any(isinstance(op, (ast.Gt, ast.Lt, ast.GtE, ast.LtE)) for op in child.ops):
                    edge_cases.append("boundary_condition")

        # Check for exception handling
        for child in ast.walk(node):
            if isinstance(child, ast.ExceptHandler):
                edge_cases.append("exception_handling")

        # Check for list/dict operations
        for child in ast.walk(node):
            if isinstance(child, ast.Subscript):
                edge_cases.append("indexing")

        return list(set(edge_cases))

    def _find_dependencies(self, node: ast.FunctionDef) -> Set[str]:
        """Find external dependencies (function calls, class instantiations)."""
        dependencies = set()

        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    # Simple function call
                    dependencies.add(child.func.id)
                elif isinstance(child.func, ast.Attribute):
                    # Method call or module function
                    if isinstance(child.func.value, ast.Name):
                        dependencies.add(child.func.value.id)

        return dependencies


def analyze_python_file(file_path: str) -> AnalysisResult:
    """
    Convenience function to analyze a Python file.

    Args:
        file_path: Path to Python source file

    Returns:
        AnalysisResult with analysis information
    """
    analyzer = CodeAnalyzer()
    return analyzer.analyze_file(file_path)

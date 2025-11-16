"""
Python AST Analyzer

Analyzes Python source files using the ast module.
"""

import ast
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple

from .models import (
    FileAnalysis,
    CodeEntity,
    NodeType,
    ComplexityMetrics,
    DesignPattern,
    CodeSmell,
)


class PythonAnalyzer:
    """Analyzes Python source files using AST"""

    def analyze_file(self, file_path: Path) -> FileAnalysis:
        """
        Analyze a Python file.

        Args:
            file_path: Path to .py file

        Returns:
            FileAnalysis with all extracted information
        """
        try:
            content = file_path.read_text(encoding="utf-8")
            tree = ast.parse(content, filename=str(file_path))
        except (SyntaxError, UnicodeDecodeError) as e:
            # Handle malformed Python files gracefully
            return FileAnalysis(
                file_path=str(file_path),
                is_test_file=self._is_test_file(file_path),
                is_init_file=file_path.name == "__init__.py",
            )

        # Extract entities
        classes = self._extract_classes(tree, str(file_path))
        functions = self._extract_functions(tree, str(file_path))

        # Extract imports
        imports, from_imports = self._extract_imports(tree)

        # Count lines
        lines = content.split("\n")
        total_lines = len(lines)
        code_lines = sum(
            1 for line in lines if line.strip() and not line.strip().startswith("#")
        )
        comment_lines = sum(1 for line in lines if line.strip().startswith("#"))

        # Create analysis
        analysis = FileAnalysis(
            file_path=str(file_path),
            classes=classes,
            functions=functions,
            imports=imports,
            from_imports=from_imports,
            total_lines=total_lines,
            code_lines=code_lines,
            comment_lines=comment_lines,
            is_test_file=self._is_test_file(file_path),
            is_init_file=file_path.name == "__init__.py",
        )

        # Detect code smells
        analysis.smells = self._detect_smells(analysis)

        # Note: Pattern detection done by PatternDetector separately

        return analysis

    def _extract_classes(self, tree: ast.AST, file_path: str) -> List[CodeEntity]:
        """Extract all class definitions"""
        classes = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                entity = CodeEntity(
                    name=node.name,
                    entity_type=NodeType.CLASS,
                    file_path=file_path,
                    line_start=node.lineno,
                    line_end=node.end_lineno or node.lineno,
                    docstring=ast.get_docstring(node),
                    decorators=self._get_decorators(node),
                    is_public=not node.name.startswith("_"),
                )

                # Extract methods
                methods = []
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        methods.append(item.name)

                entity.calls = methods  # Store method names
                classes.append(entity)

        return classes

    def _extract_functions(self, tree: ast.AST, file_path: str) -> List[CodeEntity]:
        """Extract all function definitions (module-level only)"""
        functions = []

        for node in tree.body:  # Only top-level
            if isinstance(node, ast.FunctionDef):
                entity = self._create_function_entity(
                    node, file_path, NodeType.FUNCTION
                )
                functions.append(entity)
            elif isinstance(node, ast.AsyncFunctionDef):
                entity = self._create_function_entity(
                    node, file_path, NodeType.ASYNC_FUNCTION
                )
                functions.append(entity)

        return functions

    def _create_function_entity(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
        file_path: str,
        entity_type: NodeType,
    ) -> CodeEntity:
        """Create a CodeEntity from a function AST node"""
        # Extract parameters
        params = [arg.arg for arg in node.args.args]

        # Calculate complexity
        complexity = self._calculate_complexity(node)

        # Extract function calls
        calls = self._extract_calls(node)

        return CodeEntity(
            name=node.name,
            entity_type=entity_type,
            file_path=file_path,
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            docstring=ast.get_docstring(node),
            decorators=self._get_decorators(node),
            parameters=params,
            complexity=complexity,
            calls=calls,
            is_public=not node.name.startswith("_"),
        )

    def _calculate_complexity(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> ComplexityMetrics:
        """Calculate cyclomatic complexity and other metrics"""
        complexity = 1  # Base complexity
        max_depth = 0
        num_branches = 0

        # Track nesting depth
        depth_stack = []

        for child in ast.walk(node):
            # Each decision point adds 1
            if isinstance(child, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                complexity += 1
                num_branches += 1

            # Boolean operators
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1

        # Calculate max nesting depth (simplified)
        # For a more accurate implementation, would need to traverse tree structure
        max_depth = self._calculate_nesting_depth(node)

        lines = (node.end_lineno - node.lineno + 1) if node.end_lineno else 1

        return ComplexityMetrics(
            cyclomatic_complexity=complexity,
            lines_of_code=lines,
            max_nesting_depth=max_depth,
            num_branches=num_branches,
        )

    def _calculate_nesting_depth(self, node: ast.AST) -> int:
        """Calculate maximum nesting depth"""

        def get_depth(node, current_depth=0):
            max_depth = current_depth

            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.If, ast.For, ast.While, ast.With)):
                    child_depth = get_depth(child, current_depth + 1)
                    max_depth = max(max_depth, child_depth)
                else:
                    child_depth = get_depth(child, current_depth)
                    max_depth = max(max_depth, child_depth)

            return max_depth

        return get_depth(node)

    def _extract_calls(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> List[str]:
        """Extract function/method calls made by this function"""
        calls = []

        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    calls.append(child.func.id)
                elif isinstance(child.func, ast.Attribute):
                    calls.append(child.func.attr)

        return list(set(calls))  # Unique calls

    def _extract_imports(
        self, tree: ast.AST
    ) -> Tuple[List[str], Dict[str, List[str]]]:
        """Extract import statements"""
        imports = []
        from_imports = {}

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)

            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                names = [alias.name for alias in node.names]

                if module in from_imports:
                    from_imports[module].extend(names)
                else:
                    from_imports[module] = names

        return imports, from_imports

    def _get_decorators(self, node) -> List[str]:
        """Extract decorator names"""
        decorators = []

        for dec in node.decorator_list:
            if isinstance(dec, ast.Name):
                decorators.append(dec.id)
            elif isinstance(dec, ast.Call) and isinstance(dec.func, ast.Name):
                decorators.append(dec.func.id)

        return decorators

    def _is_test_file(self, file_path: Path) -> bool:
        """Check if file is a test file"""
        return (
            file_path.name.startswith("test_")
            or file_path.name.endswith("_test.py")
            or "test" in file_path.parts
        )

    def _detect_smells(self, analysis: FileAnalysis) -> List[Dict[str, Any]]:
        """Detect code smells"""
        smells = []

        # Check all functions for smells
        for func in analysis.functions:
            # Long function
            if func.complexity and func.complexity.lines_of_code > 50:
                smells.append(
                    {
                        "smell": CodeSmell.LONG_FUNCTION,
                        "location": f"{analysis.file_path}:{func.line_start}",
                        "name": func.name,
                        "metric": func.complexity.lines_of_code,
                        "description": f"Function has {func.complexity.lines_of_code} lines (recommend < 50)",
                    }
                )

            # Complex function
            if func.complexity and func.complexity.cyclomatic_complexity > 10:
                smells.append(
                    {
                        "smell": CodeSmell.COMPLEX_FUNCTION,
                        "location": f"{analysis.file_path}:{func.line_start}",
                        "name": func.name,
                        "metric": func.complexity.cyclomatic_complexity,
                        "description": f"Function has complexity {func.complexity.cyclomatic_complexity} (recommend < 10)",
                    }
                )

            # Too many parameters
            if len(func.parameters) > 5:
                smells.append(
                    {
                        "smell": CodeSmell.TOO_MANY_PARAMETERS,
                        "location": f"{analysis.file_path}:{func.line_start}",
                        "name": func.name,
                        "metric": len(func.parameters),
                        "description": f"Function has {len(func.parameters)} parameters (recommend < 5)",
                    }
                )

            # Deep nesting
            if func.complexity and func.complexity.max_nesting_depth > 4:
                smells.append(
                    {
                        "smell": CodeSmell.DEEP_NESTING,
                        "location": f"{analysis.file_path}:{func.line_start}",
                        "name": func.name,
                        "metric": func.complexity.max_nesting_depth,
                        "description": f"Function has nesting depth {func.complexity.max_nesting_depth} (recommend < 4)",
                    }
                )

        return smells

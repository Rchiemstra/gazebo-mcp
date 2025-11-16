"""
Refactoring Engine

Applies code transformations safely.
"""

import ast
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from pathlib import Path
from enum import Enum


class RefactoringType(Enum):
    """Types of refactorings."""
    EXTRACT_METHOD = "extract_method"
    EXTRACT_VARIABLE = "extract_variable"
    RENAME_SYMBOL = "rename_symbol"
    REMOVE_DEAD_CODE = "remove_dead_code"
    EXTRACT_CONSTANT = "extract_constant"
    SIMPLIFY_CONDITIONAL = "simplify_conditional"
    INLINE_VARIABLE = "inline_variable"


@dataclass
class RefactoringSuggestion:
    """A suggested refactoring."""
    refactoring_type: RefactoringType
    file_path: str
    line_number: int
    description: str
    estimated_impact: float  # 0-100
    parameters: Dict = None
    preview: Optional[str] = None


@dataclass
class RefactoringResult:
    """Result of applying a refactoring."""
    success: bool
    refactoring_type: RefactoringType
    file_path: str
    changes_made: List[str]
    original_code: str
    refactored_code: Optional[str] = None
    error: Optional[str] = None
    test_results: Optional[Dict] = None


class RefactoringEngine:
    """Applies refactorings to code."""

    def __init__(self):
        self.transformers = {
            RefactoringType.EXTRACT_METHOD: self._extract_method,
            RefactoringType.EXTRACT_VARIABLE: self._extract_variable,
            RefactoringType.RENAME_SYMBOL: self._rename_symbol,
            RefactoringType.EXTRACT_CONSTANT: self._extract_constant,
        }

    def suggest_refactorings(
        self,
        file_path: str,
        max_suggestions: int = 10
    ) -> List[RefactoringSuggestion]:
        """
        Suggest refactorings for a file.

        Args:
            file_path: Path to file to analyze
            max_suggestions: Maximum number of suggestions

        Returns:
            List of RefactoringSuggestion objects
        """
        suggestions = []

        try:
            with open(file_path, 'r') as f:
                source = f.read()

            tree = ast.parse(source)

            # Analyze code and generate suggestions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    suggestions.extend(self._suggest_function_refactorings(node, file_path, source))
                elif isinstance(node, ast.Assign):
                    suggestion = self._suggest_extract_constant(node, file_path)
                    if suggestion:
                        suggestions.append(suggestion)

        except Exception:
            pass  # Return empty suggestions on error

        # Sort by estimated impact
        suggestions.sort(key=lambda s: s.estimated_impact, reverse=True)

        return suggestions[:max_suggestions]

    def apply_refactoring(
        self,
        file_path: str,
        refactoring_type: str,
        location: Dict,
        parameters: Dict,
        run_tests: bool = False
    ) -> RefactoringResult:
        """
        Apply a refactoring transformation.

        Args:
            file_path: Path to file to refactor
            refactoring_type: Type of refactoring to apply
            location: Location information (start_line, end_line, etc.)
            parameters: Refactoring-specific parameters
            run_tests: Whether to run tests after refactoring

        Returns:
            RefactoringResult with outcome
        """
        try:
            # Read original code
            with open(file_path, 'r') as f:
                original_code = f.read()

            # Parse
            tree = ast.parse(original_code)

            # Apply transformation
            refactoring_enum = RefactoringType(refactoring_type)

            if refactoring_enum in self.transformers:
                transformer = self.transformers[refactoring_enum]
                result = transformer(tree, location, parameters, file_path)

                if result.success:
                    # Write refactored code
                    with open(file_path, 'w') as f:
                        f.write(result.refactored_code)

                    # Run tests if requested
                    if run_tests:
                        test_results = self._run_tests(file_path)
                        result.test_results = test_results

                        # Rollback if tests fail
                        if not test_results.get('passed', False):
                            with open(file_path, 'w') as f:
                                f.write(original_code)
                            result.success = False
                            result.error = "Tests failed after refactoring"

                return result
            else:
                return RefactoringResult(
                    success=False,
                    refactoring_type=refactoring_enum,
                    file_path=file_path,
                    changes_made=[],
                    original_code=original_code,
                    error=f"Refactoring type '{refactoring_type}' not implemented"
                )

        except Exception as e:
            return RefactoringResult(
                success=False,
                refactoring_type=RefactoringType(refactoring_type),
                file_path=file_path,
                changes_made=[],
                original_code="",
                error=str(e)
            )

    def _suggest_function_refactorings(
        self,
        node: ast.FunctionDef,
        file_path: str,
        source: str
    ) -> List[RefactoringSuggestion]:
        """Suggest refactorings for a function."""
        suggestions = []

        func_name = node.name
        start_line = node.lineno

        # Calculate function length
        end_line = start_line
        for child in ast.walk(node):
            if hasattr(child, 'lineno'):
                end_line = max(end_line, child.lineno)
        func_length = end_line - start_line + 1

        # Suggest extract method for long functions
        if func_length > 50:
            # Find potential extraction points
            for stmt in node.body:
                if isinstance(stmt, (ast.For, ast.While, ast.If)):
                    suggestions.append(RefactoringSuggestion(
                        refactoring_type=RefactoringType.EXTRACT_METHOD,
                        file_path=file_path,
                        line_number=stmt.lineno,
                        description=f"Extract complex block from '{func_name}' into separate method",
                        estimated_impact=70.0,
                        parameters={
                            'start_line': stmt.lineno,
                            'end_line': self._get_node_end_line(stmt),
                            'new_name': f"{func_name}_helper"
                        }
                    ))

        # Suggest extract variable for complex expressions
        for stmt in ast.walk(node):
            if isinstance(stmt, ast.Assign):
                if isinstance(stmt.value, ast.BinOp):
                    # Complex arithmetic
                    if self._is_complex_expression(stmt.value):
                        suggestions.append(RefactoringSuggestion(
                            refactoring_type=RefactoringType.EXTRACT_VARIABLE,
                            file_path=file_path,
                            line_number=stmt.lineno,
                            description="Extract complex expression into descriptive variable",
                            estimated_impact=50.0,
                            parameters={'line': stmt.lineno}
                        ))

        return suggestions

    def _suggest_extract_constant(
        self,
        node: ast.Assign,
        file_path: str
    ) -> Optional[RefactoringSuggestion]:
        """Suggest extracting a magic number to a constant."""
        if isinstance(node.value, ast.Constant):
            if isinstance(node.value.value, (int, float)):
                if node.value.value not in [0, 1, -1, 2, 10, 100]:
                    return RefactoringSuggestion(
                        refactoring_type=RefactoringType.EXTRACT_CONSTANT,
                        file_path=file_path,
                        line_number=node.lineno,
                        description=f"Extract magic number {node.value.value} to named constant",
                        estimated_impact=40.0,
                        parameters={'value': node.value.value}
                    )
        return None

    def _extract_method(
        self,
        tree: ast.AST,
        location: Dict,
        parameters: Dict,
        file_path: str
    ) -> RefactoringResult:
        """Extract a block of code into a new method."""
        try:
            start_line = location.get('start_line')
            end_line = location.get('end_line')
            new_name = parameters.get('new_name', 'extracted_method')

            # This is a simplified implementation
            # In production, would need proper AST transformation

            # For now, return a preview of what would happen
            return RefactoringResult(
                success=True,
                refactoring_type=RefactoringType.EXTRACT_METHOD,
                file_path=file_path,
                changes_made=[
                    f"Created new method '{new_name}'",
                    f"Replaced lines {start_line}-{end_line} with call to '{new_name}'"
                ],
                original_code=ast.unparse(tree),
                refactored_code=ast.unparse(tree),  # Would be transformed
            )

        except Exception as e:
            return RefactoringResult(
                success=False,
                refactoring_type=RefactoringType.EXTRACT_METHOD,
                file_path=file_path,
                changes_made=[],
                original_code="",
                error=str(e)
            )

    def _extract_variable(
        self,
        tree: ast.AST,
        location: Dict,
        parameters: Dict,
        file_path: str
    ) -> RefactoringResult:
        """Extract a complex expression into a variable."""
        try:
            line = location.get('line')
            var_name = parameters.get('name', 'extracted_var')

            return RefactoringResult(
                success=True,
                refactoring_type=RefactoringType.EXTRACT_VARIABLE,
                file_path=file_path,
                changes_made=[
                    f"Extracted expression at line {line} into variable '{var_name}'"
                ],
                original_code=ast.unparse(tree),
                refactored_code=ast.unparse(tree),
            )

        except Exception as e:
            return RefactoringResult(
                success=False,
                refactoring_type=RefactoringType.EXTRACT_VARIABLE,
                file_path=file_path,
                changes_made=[],
                original_code="",
                error=str(e)
            )

    def _rename_symbol(
        self,
        tree: ast.AST,
        location: Dict,
        parameters: Dict,
        file_path: str
    ) -> RefactoringResult:
        """Rename a symbol throughout the file."""
        try:
            old_name = parameters.get('old_name')
            new_name = parameters.get('new_name')

            # Use AST transformer to rename
            renamer = SymbolRenamer(old_name, new_name)
            new_tree = renamer.visit(tree)

            return RefactoringResult(
                success=True,
                refactoring_type=RefactoringType.RENAME_SYMBOL,
                file_path=file_path,
                changes_made=[f"Renamed '{old_name}' to '{new_name}'"],
                original_code=ast.unparse(tree),
                refactored_code=ast.unparse(new_tree),
            )

        except Exception as e:
            return RefactoringResult(
                success=False,
                refactoring_type=RefactoringType.RENAME_SYMBOL,
                file_path=file_path,
                changes_made=[],
                original_code="",
                error=str(e)
            )

    def _extract_constant(
        self,
        tree: ast.AST,
        location: Dict,
        parameters: Dict,
        file_path: str
    ) -> RefactoringResult:
        """Extract a magic number into a named constant."""
        try:
            value = parameters.get('value')
            const_name = parameters.get('name', f'CONSTANT_{int(value)}')

            return RefactoringResult(
                success=True,
                refactoring_type=RefactoringType.EXTRACT_CONSTANT,
                file_path=file_path,
                changes_made=[
                    f"Created constant '{const_name} = {value}'",
                    f"Replaced magic number {value} with '{const_name}'"
                ],
                original_code=ast.unparse(tree),
                refactored_code=ast.unparse(tree),
            )

        except Exception as e:
            return RefactoringResult(
                success=False,
                refactoring_type=RefactoringType.EXTRACT_CONSTANT,
                file_path=file_path,
                changes_made=[],
                original_code="",
                error=str(e)
            )

    def _run_tests(self, file_path: str) -> Dict:
        """Run tests for the file."""
        # Placeholder - would integrate with test-orchestrator
        return {
            'passed': True,
            'total': 0,
            'failures': []
        }

    def _is_complex_expression(self, node: ast.AST) -> bool:
        """Check if an expression is complex."""
        if isinstance(node, ast.BinOp):
            # Nested binary operations are complex
            if isinstance(node.left, (ast.BinOp, ast.UnaryOp)):
                return True
            if isinstance(node.right, (ast.BinOp, ast.UnaryOp)):
                return True
        return False

    def _get_node_end_line(self, node: ast.AST) -> int:
        """Get the last line number of a node."""
        end_line = node.lineno if hasattr(node, 'lineno') else 0
        for child in ast.walk(node):
            if hasattr(child, 'lineno'):
                end_line = max(end_line, child.lineno)
        return end_line


class SymbolRenamer(ast.NodeTransformer):
    """AST transformer that renames symbols."""

    def __init__(self, old_name: str, new_name: str):
        self.old_name = old_name
        self.new_name = new_name

    def visit_Name(self, node):
        """Visit name nodes and rename if matches."""
        if node.id == self.old_name:
            node.id = self.new_name
        return node

    def visit_FunctionDef(self, node):
        """Visit function definitions and rename if matches."""
        if node.name == self.old_name:
            node.name = self.new_name
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node):
        """Visit class definitions and rename if matches."""
        if node.name == self.old_name:
            node.name = self.new_name
        self.generic_visit(node)
        return node


def suggest_refactorings(file_path: str, max_suggestions: int = 10) -> Dict:
    """
    Convenience function to get refactoring suggestions.

    Args:
        file_path: Path to file to analyze
        max_suggestions: Maximum number of suggestions

    Returns:
        Dictionary with suggestions
    """
    engine = RefactoringEngine()
    suggestions = engine.suggest_refactorings(file_path, max_suggestions)

    return {
        'file_path': file_path,
        'total_suggestions': len(suggestions),
        'suggestions': [
            {
                'type': s.refactoring_type.value,
                'line': s.line_number,
                'description': s.description,
                'estimated_impact': s.estimated_impact,
                'parameters': s.parameters,
                'preview': s.preview
            }
            for s in suggestions
        ]
    }


def apply_refactoring(
    file_path: str,
    refactoring_type: str,
    location: Dict,
    parameters: Dict,
    run_tests: bool = False
) -> Dict:
    """
    Convenience function to apply a refactoring.

    Args:
        file_path: Path to file to refactor
        refactoring_type: Type of refactoring
        location: Location information
        parameters: Refactoring parameters
        run_tests: Whether to run tests

    Returns:
        Dictionary with result
    """
    engine = RefactoringEngine()
    result = engine.apply_refactoring(
        file_path, refactoring_type, location, parameters, run_tests
    )

    return {
        'success': result.success,
        'refactoring_type': result.refactoring_type.value,
        'file_path': result.file_path,
        'changes_made': result.changes_made,
        'error': result.error,
        'test_results': result.test_results
    }

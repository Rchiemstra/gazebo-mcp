"""
Code Analyzer

AST-based code analysis for complexity, maintainability, and quality metrics.
"""

import ast
import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
from collections import defaultdict


class CodeAnalyzer:
    """
    Analyzes Python code using AST parsing.

    Provides metrics for complexity, maintainability, and code quality.
    """

    def analyze_skill(self, skill_name: str) -> Dict[str, Any]:
        """
        Analyze all code files for a skill.

        Args:
            skill_name: Name of the skill to analyze

        Returns:
            Analysis results
        """
        # Construct skill path
        skill_path = Path(f"skills/{skill_name}")

        if not skill_path.exists():
            return {
                'success': False,
                'error': f'Skill directory not found: {skill_path}'
            }

        # Find all Python files
        python_files = list(skill_path.rglob("*.py"))

        if not python_files:
            return {
                'success': False,
                'error': f'No Python files found in {skill_path}'
            }

        # Analyze each file
        file_analyses = []
        total_metrics = {
            'total_lines': 0,
            'total_functions': 0,
            'total_classes': 0,
            'total_complexity': 0,
            'max_complexity': 0
        }

        for file_path in python_files:
            # Skip test files and __pycache__
            if '__pycache__' in str(file_path) or file_path.name.startswith('test_'):
                continue

            analysis = self.analyze_file(str(file_path))
            if analysis['success']:
                file_analyses.append(analysis)

                # Aggregate metrics
                total_metrics['total_lines'] += analysis['metrics']['lines_of_code']
                total_metrics['total_functions'] += analysis['metrics']['num_functions']
                total_metrics['total_classes'] += analysis['metrics']['num_classes']
                total_metrics['total_complexity'] += analysis['metrics']['total_complexity']
                total_metrics['max_complexity'] = max(
                    total_metrics['max_complexity'],
                    analysis['metrics']['max_complexity']
                )

        # Calculate overall scores
        avg_complexity = (
            total_metrics['total_complexity'] / total_metrics['total_functions']
            if total_metrics['total_functions'] > 0 else 0
        )

        # Complexity score (inverted - lower is better)
        # 1-5: Excellent, 6-10: Good, 11-20: Fair, 21+: Poor
        if avg_complexity <= 5:
            complexity_score = 100
        elif avg_complexity <= 10:
            complexity_score = 80
        elif avg_complexity <= 20:
            complexity_score = 60
        else:
            complexity_score = max(0, 60 - (avg_complexity - 20) * 2)

        # Maintainability index (simplified)
        # Based on: lines per file, complexity, comments
        avg_lines_per_file = total_metrics['total_lines'] / len(file_analyses) if file_analyses else 0

        if avg_lines_per_file < 200 and avg_complexity < 10:
            maintainability = 90
        elif avg_lines_per_file < 400 and avg_complexity < 15:
            maintainability = 75
        elif avg_lines_per_file < 600 and avg_complexity < 20:
            maintainability = 60
        else:
            maintainability = 45

        return {
            'success': True,
            'skill_name': skill_name,
            'files_analyzed': len(file_analyses),
            'total_metrics': total_metrics,
            'average_complexity': avg_complexity,
            'complexity_score': complexity_score,
            'maintainability_index': maintainability,
            'file_analyses': file_analyses,
            'issues': self._identify_code_issues(file_analyses, avg_complexity)
        }

    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze a single Python file.

        Args:
            file_path: Path to the Python file

        Returns:
            File analysis results
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()

            tree = ast.parse(source, filename=file_path)

            # Collect metrics
            visitor = CodeMetricsVisitor()
            visitor.visit(tree)

            # Calculate complexity
            complexities = [func['complexity'] for func in visitor.functions]
            total_complexity = sum(complexities)
            max_complexity = max(complexities) if complexities else 0
            avg_complexity = total_complexity / len(complexities) if complexities else 0

            return {
                'success': True,
                'file_path': file_path,
                'metrics': {
                    'lines_of_code': len(source.splitlines()),
                    'num_functions': len(visitor.functions),
                    'num_classes': len(visitor.classes),
                    'num_imports': len(visitor.imports),
                    'total_complexity': total_complexity,
                    'max_complexity': max_complexity,
                    'avg_complexity': avg_complexity
                },
                'functions': visitor.functions,
                'classes': visitor.classes,
                'imports': visitor.imports,
                'issues': []
            }

        except SyntaxError as e:
            return {
                'success': False,
                'file_path': file_path,
                'error': f'Syntax error: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'file_path': file_path,
                'error': f'Analysis error: {str(e)}'
            }

    def _identify_code_issues(
        self,
        file_analyses: List[Dict[str, Any]],
        avg_complexity: float
    ) -> List[Dict[str, Any]]:
        """Identify code issues from analysis results."""
        issues = []

        # High complexity functions
        for analysis in file_analyses:
            if not analysis.get('success'):
                continue

            for func in analysis.get('functions', []):
                if func['complexity'] > 15:
                    issues.append({
                        'type': 'high_complexity',
                        'severity': 'high' if func['complexity'] > 25 else 'medium',
                        'file': analysis['file_path'],
                        'function': func['name'],
                        'complexity': func['complexity'],
                        'recommendation': f"Refactor {func['name']} to reduce complexity from {func['complexity']} to below 15"
                    })

        # Large files
        for analysis in file_analyses:
            if not analysis.get('success'):
                continue

            loc = analysis['metrics']['lines_of_code']
            if loc > 500:
                issues.append({
                    'type': 'large_file',
                    'severity': 'medium' if loc < 1000 else 'high',
                    'file': analysis['file_path'],
                    'lines': loc,
                    'recommendation': f"Consider splitting {Path(analysis['file_path']).name} ({loc} lines) into smaller modules"
                })

        # Classes with many methods
        for analysis in file_analyses:
            if not analysis.get('success'):
                continue

            for cls in analysis.get('classes', []):
                if cls['num_methods'] > 15:
                    issues.append({
                        'type': 'large_class',
                        'severity': 'medium',
                        'file': analysis['file_path'],
                        'class': cls['name'],
                        'methods': cls['num_methods'],
                        'recommendation': f"Consider breaking down {cls['name']} ({cls['num_methods']} methods) into smaller, focused classes"
                    })

        return issues


class CodeMetricsVisitor(ast.NodeVisitor):
    """AST visitor for collecting code metrics."""

    def __init__(self):
        self.functions = []
        self.classes = []
        self.imports = []
        self.current_class = None

    def visit_FunctionDef(self, node):
        """Visit function definition."""
        complexity = self._calculate_complexity(node)

        func_info = {
            'name': node.name,
            'lineno': node.lineno,
            'complexity': complexity,
            'num_args': len(node.args.args),
            'is_method': self.current_class is not None,
            'class_name': self.current_class
        }

        self.functions.append(func_info)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        """Visit async function definition."""
        self.visit_FunctionDef(node)

    def visit_ClassDef(self, node):
        """Visit class definition."""
        # Count methods
        methods = [n for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]

        class_info = {
            'name': node.name,
            'lineno': node.lineno,
            'num_methods': len(methods),
            'num_attributes': len([n for n in node.body if isinstance(n, ast.AnnAssign)])
        }

        self.classes.append(class_info)

        # Visit methods
        old_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = old_class

    def visit_Import(self, node):
        """Visit import statement."""
        for alias in node.names:
            self.imports.append({
                'type': 'import',
                'module': alias.name,
                'alias': alias.asname
            })
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """Visit from...import statement."""
        for alias in node.names:
            self.imports.append({
                'type': 'from_import',
                'module': node.module,
                'name': alias.name,
                'alias': alias.asname
            })
        self.generic_visit(node)

    def _calculate_complexity(self, node):
        """
        Calculate cyclomatic complexity for a function.

        Simplified McCabe complexity:
        - Start with 1
        - +1 for each: if, elif, for, while, except, and, or
        - +1 for each boolean operator in conditions
        """
        complexity = 1

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1

        return complexity


def get_code_metrics(skill_name: str) -> Dict[str, Any]:
    """
    Convenience function to get code metrics for a skill.

    Args:
        skill_name: Name of the skill

    Returns:
        Code analysis results
    """
    analyzer = CodeAnalyzer()
    return analyzer.analyze_skill(skill_name)

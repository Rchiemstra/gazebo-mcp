"""
Code Smell Detector

Identifies code smells and refactoring opportunities.
"""

import ast
import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from pathlib import Path
from enum import Enum


class SmellSeverity(Enum):
    """Severity levels for code smells."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SmellType(Enum):
    """Types of code smells."""
    LONG_FUNCTION = "long_function"
    LONG_PARAMETER_LIST = "long_parameter_list"
    COMPLEX_FUNCTION = "complex_function"
    DUPLICATE_CODE = "duplicate_code"
    MAGIC_NUMBER = "magic_number"
    DEEP_NESTING = "deep_nesting"
    DEAD_CODE = "dead_code"
    GOD_CLASS = "god_class"
    LONG_CLASS = "long_class"
    POOR_NAMING = "poor_naming"
    MUTABLE_DEFAULT = "mutable_default"
    BROAD_EXCEPTION = "broad_exception"
    EMPTY_EXCEPT = "empty_except"
    TOO_MANY_RETURNS = "too_many_returns"
    COGNITIVE_COMPLEXITY = "cognitive_complexity"


@dataclass
class CodeSmell:
    """Represents a detected code smell."""
    smell_type: SmellType
    severity: SmellSeverity
    file_path: str
    line_number: int
    function_name: Optional[str]
    class_name: Optional[str]
    description: str
    suggestion: str
    metrics: Dict = field(default_factory=dict)


@dataclass
class SmellAnalysis:
    """Results of code smell detection."""
    file_path: str
    total_smells: int
    critical: int
    high: int
    medium: int
    low: int
    smells: List[CodeSmell] = field(default_factory=list)
    metrics: Dict = field(default_factory=dict)


class SmellDetector:
    """Detects code smells in source code."""

    # Thresholds for detection
    MAX_FUNCTION_LENGTH = 50
    MAX_PARAMETERS = 5
    MAX_COMPLEXITY = 10
    MAX_NESTING_DEPTH = 4
    MAX_CLASS_LENGTH = 200
    MAX_CLASS_METHODS = 20
    MAX_RETURNS = 5

    def __init__(self):
        self.detectors = {
            'python': self._detect_python_smells,
        }

    def detect_smells(
        self,
        file_path: str,
        severity_threshold: str = "low"
    ) -> SmellAnalysis:
        """
        Detect code smells in a file.

        Args:
            file_path: Path to file to analyze
            severity_threshold: Minimum severity to report

        Returns:
            SmellAnalysis with detected smells
        """
        file_path = Path(file_path)

        if not file_path.exists():
            return SmellAnalysis(
                file_path=str(file_path),
                total_smells=0,
                critical=0,
                high=0,
                medium=0,
                low=0
            )

        # Detect language
        if file_path.suffix == '.py':
            language = 'python'
        else:
            language = 'unknown'

        if language in self.detectors:
            return self.detectors[language](file_path, severity_threshold)
        else:
            return SmellAnalysis(
                file_path=str(file_path),
                total_smells=0,
                critical=0,
                high=0,
                medium=0,
                low=0
            )

    def _detect_python_smells(
        self,
        file_path: Path,
        severity_threshold: str
    ) -> SmellAnalysis:
        """Detect smells in Python code."""
        smells = []

        try:
            with open(file_path, 'r') as f:
                source = f.read()

            tree = ast.parse(source)

            # Visit all nodes
            for node in ast.walk(tree):
                # Function smells
                if isinstance(node, ast.FunctionDef):
                    smells.extend(self._check_function_smells(node, file_path))

                # Class smells
                elif isinstance(node, ast.ClassDef):
                    smells.extend(self._check_class_smells(node, file_path))

                # Exception handling smells
                elif isinstance(node, ast.ExceptHandler):
                    smells.extend(self._check_exception_smells(node, file_path))

                # Magic numbers
                elif isinstance(node, ast.Constant):
                    smell = self._check_magic_number(node, file_path)
                    if smell:
                        smells.append(smell)

            # Check for duplicate code
            smells.extend(self._check_duplicate_code(source, file_path))

        except Exception:
            pass  # Return empty smells on parse error

        # Filter by severity
        threshold_order = ['low', 'medium', 'high', 'critical']
        threshold_index = threshold_order.index(severity_threshold)

        filtered_smells = [
            s for s in smells
            if threshold_order.index(s.severity.value) >= threshold_index
        ]

        # Count by severity
        severity_counts = {
            'critical': sum(1 for s in filtered_smells if s.severity == SmellSeverity.CRITICAL),
            'high': sum(1 for s in filtered_smells if s.severity == SmellSeverity.HIGH),
            'medium': sum(1 for s in filtered_smells if s.severity == SmellSeverity.MEDIUM),
            'low': sum(1 for s in filtered_smells if s.severity == SmellSeverity.LOW),
        }

        # Calculate metrics
        metrics = {
            'total_lines': len(source.split('\n')),
            'total_functions': sum(1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)),
            'total_classes': sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef)),
        }

        return SmellAnalysis(
            file_path=str(file_path),
            total_smells=len(filtered_smells),
            critical=severity_counts['critical'],
            high=severity_counts['high'],
            medium=severity_counts['medium'],
            low=severity_counts['low'],
            smells=filtered_smells,
            metrics=metrics
        )

    def _check_function_smells(
        self,
        node: ast.FunctionDef,
        file_path: Path
    ) -> List[CodeSmell]:
        """Check for function-related smells."""
        smells = []

        # Get function info
        func_name = node.name
        start_line = node.lineno
        num_params = len(node.args.args)

        # Calculate function length
        end_line = start_line
        for child in ast.walk(node):
            if hasattr(child, 'lineno'):
                end_line = max(end_line, child.lineno)
        func_length = end_line - start_line + 1

        # Calculate complexity
        complexity = self._calculate_complexity(node)

        # Calculate nesting depth
        max_depth = self._calculate_max_nesting(node)

        # Count returns
        num_returns = sum(1 for n in ast.walk(node) if isinstance(n, ast.Return))

        # Long function
        if func_length > self.MAX_FUNCTION_LENGTH:
            severity = SmellSeverity.HIGH if func_length > self.MAX_FUNCTION_LENGTH * 2 else SmellSeverity.MEDIUM
            smells.append(CodeSmell(
                smell_type=SmellType.LONG_FUNCTION,
                severity=severity,
                file_path=str(file_path),
                line_number=start_line,
                function_name=func_name,
                class_name=None,
                description=f"Function '{func_name}' is {func_length} lines long (threshold: {self.MAX_FUNCTION_LENGTH})",
                suggestion="Consider extracting methods to break down this function",
                metrics={'length': func_length, 'threshold': self.MAX_FUNCTION_LENGTH}
            ))

        # Long parameter list
        if num_params > self.MAX_PARAMETERS:
            smells.append(CodeSmell(
                smell_type=SmellType.LONG_PARAMETER_LIST,
                severity=SmellSeverity.MEDIUM,
                file_path=str(file_path),
                line_number=start_line,
                function_name=func_name,
                class_name=None,
                description=f"Function '{func_name}' has {num_params} parameters (threshold: {self.MAX_PARAMETERS})",
                suggestion="Consider using a parameter object or breaking up the function",
                metrics={'params': num_params, 'threshold': self.MAX_PARAMETERS}
            ))

        # High complexity
        if complexity > self.MAX_COMPLEXITY:
            severity = SmellSeverity.HIGH if complexity > self.MAX_COMPLEXITY * 2 else SmellSeverity.MEDIUM
            smells.append(CodeSmell(
                smell_type=SmellType.COMPLEX_FUNCTION,
                severity=severity,
                file_path=str(file_path),
                line_number=start_line,
                function_name=func_name,
                class_name=None,
                description=f"Function '{func_name}' has complexity {complexity} (threshold: {self.MAX_COMPLEXITY})",
                suggestion="Simplify conditionals and extract complex logic into separate functions",
                metrics={'complexity': complexity, 'threshold': self.MAX_COMPLEXITY}
            ))

        # Deep nesting
        if max_depth > self.MAX_NESTING_DEPTH:
            smells.append(CodeSmell(
                smell_type=SmellType.DEEP_NESTING,
                severity=SmellSeverity.MEDIUM,
                file_path=str(file_path),
                line_number=start_line,
                function_name=func_name,
                class_name=None,
                description=f"Function '{func_name}' has nesting depth {max_depth} (threshold: {self.MAX_NESTING_DEPTH})",
                suggestion="Use early returns or extract nested logic into separate functions",
                metrics={'depth': max_depth, 'threshold': self.MAX_NESTING_DEPTH}
            ))

        # Too many returns
        if num_returns > self.MAX_RETURNS:
            smells.append(CodeSmell(
                smell_type=SmellType.TOO_MANY_RETURNS,
                severity=SmellSeverity.LOW,
                file_path=str(file_path),
                line_number=start_line,
                function_name=func_name,
                class_name=None,
                description=f"Function '{func_name}' has {num_returns} return statements",
                suggestion="Consider consolidating return logic",
                metrics={'returns': num_returns}
            ))

        # Check for mutable default arguments
        for default in node.args.defaults:
            if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                smells.append(CodeSmell(
                    smell_type=SmellType.MUTABLE_DEFAULT,
                    severity=SmellSeverity.HIGH,
                    file_path=str(file_path),
                    line_number=start_line,
                    function_name=func_name,
                    class_name=None,
                    description=f"Function '{func_name}' has mutable default argument",
                    suggestion="Use None as default and initialize inside function",
                    metrics={}
                ))

        # Poor naming
        if len(func_name) <= 2 and func_name not in ['_', '__']:
            smells.append(CodeSmell(
                smell_type=SmellType.POOR_NAMING,
                severity=SmellSeverity.LOW,
                file_path=str(file_path),
                line_number=start_line,
                function_name=func_name,
                class_name=None,
                description=f"Function name '{func_name}' is too short",
                suggestion="Use descriptive names that explain the function's purpose",
                metrics={'name_length': len(func_name)}
            ))

        return smells

    def _check_class_smells(
        self,
        node: ast.ClassDef,
        file_path: Path
    ) -> List[CodeSmell]:
        """Check for class-related smells."""
        smells = []

        class_name = node.name
        start_line = node.lineno

        # Calculate class length
        end_line = start_line
        for child in ast.walk(node):
            if hasattr(child, 'lineno'):
                end_line = max(end_line, child.lineno)
        class_length = end_line - start_line + 1

        # Count methods
        methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
        num_methods = len(methods)

        # God class (too many methods)
        if num_methods > self.MAX_CLASS_METHODS:
            smells.append(CodeSmell(
                smell_type=SmellType.GOD_CLASS,
                severity=SmellSeverity.HIGH,
                file_path=str(file_path),
                line_number=start_line,
                function_name=None,
                class_name=class_name,
                description=f"Class '{class_name}' has {num_methods} methods (threshold: {self.MAX_CLASS_METHODS})",
                suggestion="Consider breaking this class into smaller, focused classes",
                metrics={'methods': num_methods, 'threshold': self.MAX_CLASS_METHODS}
            ))

        # Long class
        if class_length > self.MAX_CLASS_LENGTH:
            smells.append(CodeSmell(
                smell_type=SmellType.LONG_CLASS,
                severity=SmellSeverity.MEDIUM,
                file_path=str(file_path),
                line_number=start_line,
                function_name=None,
                class_name=class_name,
                description=f"Class '{class_name}' is {class_length} lines long",
                suggestion="Extract related functionality into separate classes",
                metrics={'length': class_length}
            ))

        return smells

    def _check_exception_smells(
        self,
        node: ast.ExceptHandler,
        file_path: Path
    ) -> List[CodeSmell]:
        """Check for exception handling smells."""
        smells = []

        line_number = node.lineno

        # Broad exception catch
        if node.type is None:
            smells.append(CodeSmell(
                smell_type=SmellType.BROAD_EXCEPTION,
                severity=SmellSeverity.MEDIUM,
                file_path=str(file_path),
                line_number=line_number,
                function_name=None,
                class_name=None,
                description="Catching all exceptions with bare 'except:'",
                suggestion="Catch specific exceptions instead of using bare except",
                metrics={}
            ))
        elif isinstance(node.type, ast.Name) and node.type.id == 'Exception':
            smells.append(CodeSmell(
                smell_type=SmellType.BROAD_EXCEPTION,
                severity=SmellSeverity.LOW,
                file_path=str(file_path),
                line_number=line_number,
                function_name=None,
                class_name=None,
                description="Catching broad 'Exception' type",
                suggestion="Catch more specific exception types",
                metrics={}
            ))

        # Empty except block
        if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
            smells.append(CodeSmell(
                smell_type=SmellType.EMPTY_EXCEPT,
                severity=SmellSeverity.HIGH,
                file_path=str(file_path),
                line_number=line_number,
                function_name=None,
                class_name=None,
                description="Empty except block silently ignores errors",
                suggestion="Log the error or handle it appropriately",
                metrics={}
            ))

        return smells

    def _check_magic_number(
        self,
        node: ast.Constant,
        file_path: Path
    ) -> Optional[CodeSmell]:
        """Check for magic numbers."""
        # Only check numeric constants
        if not isinstance(node.value, (int, float)):
            return None

        # Skip common values
        if node.value in [0, 1, -1, 2, 10, 100, 1000]:
            return None

        # Check if it's in a comparison or arithmetic operation
        # This is a simplified check
        return CodeSmell(
            smell_type=SmellType.MAGIC_NUMBER,
            severity=SmellSeverity.LOW,
            file_path=str(file_path),
            line_number=node.lineno,
            function_name=None,
            class_name=None,
            description=f"Magic number {node.value} found",
            suggestion="Extract to a named constant",
            metrics={'value': node.value}
        )

    def _check_duplicate_code(
        self,
        source: str,
        file_path: Path
    ) -> List[CodeSmell]:
        """Check for duplicate code blocks."""
        smells = []
        lines = source.split('\n')

        # Simple duplicate detection: look for identical line sequences
        min_duplicate_length = 5
        seen_sequences = {}

        for i in range(len(lines) - min_duplicate_length):
            # Get sequence of lines (normalized)
            sequence = []
            for j in range(min_duplicate_length):
                line = lines[i + j].strip()
                if line and not line.startswith('#'):
                    sequence.append(line)

            if len(sequence) >= min_duplicate_length:
                seq_key = tuple(sequence)
                if seq_key in seen_sequences:
                    # Found duplicate
                    smells.append(CodeSmell(
                        smell_type=SmellType.DUPLICATE_CODE,
                        severity=SmellSeverity.MEDIUM,
                        file_path=str(file_path),
                        line_number=i + 1,
                        function_name=None,
                        class_name=None,
                        description=f"Duplicate code block starting at line {i + 1}",
                        suggestion="Extract common code into a shared function",
                        metrics={'first_occurrence': seen_sequences[seq_key]}
                    ))
                else:
                    seen_sequences[seq_key] = i + 1

        return smells

    def _calculate_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity."""
        complexity = 1

        for child in ast.walk(node):
            # Each decision point adds 1
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                # And/Or operations
                complexity += len(child.values) - 1

        return complexity

    def _calculate_max_nesting(self, node: ast.AST, current_depth: int = 0) -> int:
        """Calculate maximum nesting depth."""
        max_depth = current_depth

        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.With)):
                child_depth = self._calculate_max_nesting(child, current_depth + 1)
                max_depth = max(max_depth, child_depth)
            else:
                child_depth = self._calculate_max_nesting(child, current_depth)
                max_depth = max(max_depth, child_depth)

        return max_depth


def detect_code_smells(file_path: str, severity_threshold: str = "low") -> Dict:
    """
    Convenience function to detect code smells.

    Args:
        file_path: Path to file to analyze
        severity_threshold: Minimum severity (low, medium, high, critical)

    Returns:
        Dictionary with analysis results
    """
    detector = SmellDetector()
    result = detector.detect_smells(file_path, severity_threshold)

    return {
        'file_path': result.file_path,
        'total_smells': result.total_smells,
        'by_severity': {
            'critical': result.critical,
            'high': result.high,
            'medium': result.medium,
            'low': result.low,
        },
        'smells': [
            {
                'type': smell.smell_type.value,
                'severity': smell.severity.value,
                'line': smell.line_number,
                'function': smell.function_name,
                'class': smell.class_name,
                'description': smell.description,
                'suggestion': smell.suggestion,
                'metrics': smell.metrics
            }
            for smell in result.smells
        ],
        'metrics': result.metrics
    }

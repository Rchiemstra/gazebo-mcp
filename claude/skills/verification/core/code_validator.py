"""
Code Validator

Validates Python code for syntax, style, security, and completeness.
"""

import ast
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class ValidationIssue:
    """Represents a validation issue"""
    severity: str  # 'error', 'warning', 'info'
    category: str  # 'syntax', 'style', 'security', 'completeness'
    message: str
    line: Optional[int] = None
    suggestion: Optional[str] = None


@dataclass
class CodeValidationResult:
    """Result of code validation"""
    is_valid: bool
    issues: List[ValidationIssue] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)


class CodeValidator:
    """Validates Python code quality"""

    def __init__(self):
        self.security_patterns = [
            (r'eval\s*\(', 'Avoid eval() - security risk'),
            (r'exec\s*\(', 'Avoid exec() - security risk'),
            (r'__import__\s*\(', 'Avoid __import__() - use import statement'),
            (r'open\([^)]*[\'"]w[\'"]', 'File write detected - ensure proper permissions'),
        ]

    def validate(self, code: str, check_style: bool = True, check_security: bool = True) -> CodeValidationResult:
        """
        Validate Python code.

        Args:
            code: Python code to validate
            check_style: Whether to check style issues
            check_security: Whether to check security issues

        Returns:
            CodeValidationResult with issues and metrics
        """
        issues = []

        # 1. Syntax validation
        syntax_issues = self._check_syntax(code)
        issues.extend(syntax_issues)

        # If syntax errors, stop here
        if any(issue.severity == 'error' for issue in syntax_issues):
            return CodeValidationResult(is_valid=False, issues=issues)

        # 2. Parse AST for deeper analysis
        try:
            tree = ast.parse(code)

            # 3. Style checks
            if check_style:
                style_issues = self._check_style(code, tree)
                issues.extend(style_issues)

            # 4. Security checks
            if check_security:
                security_issues = self._check_security(code, tree)
                issues.extend(security_issues)

            # 5. Calculate metrics
            metrics = self._calculate_metrics(code, tree)

        except SyntaxError as e:
            # Should have been caught earlier, but just in case
            issues.append(ValidationIssue(
                severity='error',
                category='syntax',
                message=f"Syntax error: {e.msg}",
                line=e.lineno if hasattr(e, 'lineno') else None
            ))
            return CodeValidationResult(is_valid=False, issues=issues)

        # Determine if valid (no errors, warnings are okay)
        has_errors = any(issue.severity == 'error' for issue in issues)

        return CodeValidationResult(
            is_valid=not has_errors,
            issues=issues,
            metrics=metrics
        )

    def _check_syntax(self, code: str) -> List[ValidationIssue]:
        """Check for syntax errors"""
        issues = []

        try:
            ast.parse(code)
        except SyntaxError as e:
            issues.append(ValidationIssue(
                severity='error',
                category='syntax',
                message=f"Syntax error: {e.msg}",
                line=e.lineno if hasattr(e, 'lineno') else None,
                suggestion="Fix syntax error before proceeding"
            ))
        except Exception as e:
            issues.append(ValidationIssue(
                severity='error',
                category='syntax',
                message=f"Parse error: {str(e)}",
                suggestion="Ensure code is valid Python"
            ))

        return issues

    def _check_style(self, code: str, tree: ast.AST) -> List[ValidationIssue]:
        """Check for style issues"""
        issues = []

        # Check for very long lines (> 120 characters)
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                issues.append(ValidationIssue(
                    severity='warning',
                    category='style',
                    message=f"Line {i} is too long ({len(line)} > 120 characters)",
                    line=i,
                    suggestion="Break long lines for readability"
                ))

        # Check for missing docstrings in functions/classes
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if not ast.get_docstring(node):
                    issues.append(ValidationIssue(
                        severity='info',
                        category='style',
                        message=f"{node.__class__.__name__} '{node.name}' missing docstring",
                        line=node.lineno,
                        suggestion="Add docstring to describe purpose"
                    ))

        return issues

    def _check_security(self, code: str, tree: ast.AST) -> List[ValidationIssue]:
        """Check for security issues"""
        issues = []

        # Pattern-based security checks
        for pattern, message in self.security_patterns:
            if re.search(pattern, code):
                issues.append(ValidationIssue(
                    severity='warning',
                    category='security',
                    message=message,
                    suggestion="Review security implications"
                ))

        # AST-based security checks
        for node in ast.walk(tree):
            # Check for bare except
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                issues.append(ValidationIssue(
                    severity='warning',
                    category='security',
                    message="Bare except clause catches all exceptions",
                    line=node.lineno,
                    suggestion="Catch specific exceptions instead of bare 'except:'"
                ))

        return issues

    def _calculate_metrics(self, code: str, tree: ast.AST) -> Dict[str, Any]:
        """Calculate code metrics"""
        metrics = {
            'total_lines': len(code.split('\n')),
            'non_empty_lines': len([line for line in code.split('\n') if line.strip()]),
            'functions': 0,
            'classes': 0,
            'imports': 0,
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                metrics['functions'] += 1
            elif isinstance(node, ast.ClassDef):
                metrics['classes'] += 1
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                metrics['imports'] += 1

        return metrics

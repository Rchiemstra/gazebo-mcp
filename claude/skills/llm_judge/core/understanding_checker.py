"""
Student Understanding Checker

Analyzes student code and responses to identify knowledge gaps,
misconceptions, and suggest areas for review.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Set
import ast
import re


@dataclass
class KnowledgeGap:
    """A knowledge gap identified in student work."""
    concept: str
    severity: str  # "critical", "moderate", "minor"
    evidence: str
    suggestion: str


@dataclass
class UnderstandingResult:
    """Result of understanding check."""
    demonstrates_understanding: bool
    confidence_level: float  # 0.0 to 1.0
    knowledge_gaps: List[KnowledgeGap]
    demonstrated_concepts: List[str]
    recommended_review: List[str]
    next_learning_steps: List[str]
    metrics: Dict[str, Any]


class UnderstandingChecker:
    """Checks student understanding through code analysis."""

    def check_code_understanding(
        self,
        student_code: str,
        expected_concepts: Optional[List[str]] = None,
        learning_context: Optional[Dict[str, Any]] = None
    ) -> UnderstandingResult:
        """
        Analyze student code to assess understanding.

        Args:
            student_code: Student's code to analyze
            expected_concepts: Concepts student should demonstrate
                - "functions", "classes", "loops", "conditionals"
                - "error_handling", "typing", "docstrings"
                - "list_comprehension", "generators", "decorators"
            learning_context: Optional context
                - level: "beginner", "intermediate", "advanced"
                - previous_attempts: int
                - known_struggles: List[str]

        Returns:
            UnderstandingResult with analysis
        """
        expected = expected_concepts or []
        context = learning_context or {}
        level = context.get("level", "beginner")

        knowledge_gaps = []
        demonstrated = []
        metrics = {
            "total_lines": len(student_code.splitlines()),
            "functions_defined": 0,
            "classes_defined": 0,
            "has_docstrings": False,
            "has_type_hints": False,
            "has_error_handling": False,
            "complexity_indicators": []
        }

        # Try to parse the code
        try:
            tree = ast.parse(student_code)
            self._analyze_ast(tree, metrics, demonstrated, knowledge_gaps, expected)
        except SyntaxError as e:
            knowledge_gaps.append(KnowledgeGap(
                concept="syntax",
                severity="critical",
                evidence=f"Syntax error at line {e.lineno}: {e.msg}",
                suggestion="Review Python syntax basics - ensure proper indentation and structure"
            ))
            # Can't continue AST analysis with syntax errors
            return self._build_result(False, 0.0, knowledge_gaps, demonstrated, metrics, level)

        # Analyze patterns and anti-patterns
        self._check_code_patterns(student_code, knowledge_gaps, demonstrated, level)

        # Check for expected concepts
        self._check_expected_concepts(expected, demonstrated, knowledge_gaps, level)

        # Calculate confidence level
        confidence = self._calculate_confidence(metrics, knowledge_gaps, demonstrated, expected)

        # Determine if understanding is demonstrated
        critical_gaps = [g for g in knowledge_gaps if g.severity == "critical"]
        demonstrates_understanding = len(critical_gaps) == 0 and confidence >= 0.6

        return self._build_result(
            demonstrates_understanding,
            confidence,
            knowledge_gaps,
            demonstrated,
            metrics,
            level
        )

    def _analyze_ast(
        self,
        tree: ast.AST,
        metrics: Dict[str, Any],
        demonstrated: List[str],
        knowledge_gaps: List[KnowledgeGap],
        expected: List[str]
    ):
        """Analyze AST to extract metrics and concepts."""
        for node in ast.walk(tree):
            # Functions
            if isinstance(node, ast.FunctionDef):
                metrics["functions_defined"] += 1
                demonstrated.append("functions")

                # Check for docstrings
                if ast.get_docstring(node):
                    metrics["has_docstrings"] = True
                    demonstrated.append("docstrings")

                # Check for type hints
                if node.returns or any(arg.annotation for arg in node.args.args):
                    metrics["has_type_hints"] = True
                    demonstrated.append("typing")

                # Check for decorators
                if node.decorator_list:
                    demonstrated.append("decorators")

            # Classes
            elif isinstance(node, ast.ClassDef):
                metrics["classes_defined"] += 1
                demonstrated.append("classes")

            # Error handling
            elif isinstance(node, ast.Try):
                metrics["has_error_handling"] = True
                demonstrated.append("error_handling")

                # Check for bare except (anti-pattern)
                for handler in node.handlers:
                    if handler.type is None:
                        knowledge_gaps.append(KnowledgeGap(
                            concept="error_handling",
                            severity="moderate",
                            evidence="Using bare 'except:' clause",
                            suggestion="Catch specific exceptions (e.g., 'except ValueError:') for better error handling"
                        ))

            # Loops
            elif isinstance(node, (ast.For, ast.While)):
                demonstrated.append("loops")

            # Conditionals
            elif isinstance(node, ast.If):
                demonstrated.append("conditionals")

            # List comprehensions
            elif isinstance(node, ast.ListComp):
                demonstrated.append("list_comprehension")
                metrics["complexity_indicators"].append("comprehension")

            # Generators
            elif isinstance(node, ast.GeneratorExp):
                demonstrated.append("generators")
                metrics["complexity_indicators"].append("generator")

        # Remove duplicates
        demonstrated[:] = list(set(demonstrated))

    def _check_code_patterns(
        self,
        code: str,
        knowledge_gaps: List[KnowledgeGap],
        demonstrated: List[str],
        level: str
    ):
        """Check for common patterns and anti-patterns."""
        # Check for common anti-patterns
        if re.search(r'eval\(', code):
            knowledge_gaps.append(KnowledgeGap(
                concept="security",
                severity="critical",
                evidence="Using eval() function",
                suggestion="Avoid eval() - it's a security risk. Use safer alternatives like ast.literal_eval() for data"
            ))

        if re.search(r'exec\(', code):
            knowledge_gaps.append(KnowledgeGap(
                concept="security",
                severity="critical",
                evidence="Using exec() function",
                suggestion="Avoid exec() - it's dangerous. Refactor to use normal function calls"
            ))

        # Check for global variables (intermediate+ level)
        if level in ["intermediate", "advanced"]:
            if re.search(r'^\s*global\s+\w+', code, re.MULTILINE):
                knowledge_gaps.append(KnowledgeGap(
                    concept="code_organization",
                    severity="moderate",
                    evidence="Using global variables",
                    suggestion="Consider using function parameters or class attributes instead of globals"
                ))

        # Check for magic numbers
        numbers = re.findall(r'\b\d+\b', code)
        if len([n for n in numbers if n not in ['0', '1', '2']]) > 3:
            knowledge_gaps.append(KnowledgeGap(
                concept="code_readability",
                severity="minor",
                evidence="Multiple magic numbers found",
                suggestion="Consider using named constants for important numbers (e.g., MAX_RETRIES = 3)"
            ))

    def _check_expected_concepts(
        self,
        expected: List[str],
        demonstrated: List[str],
        knowledge_gaps: List[KnowledgeGap],
        level: str
    ):
        """Check if expected concepts were demonstrated."""
        missing = set(expected) - set(demonstrated)

        for concept in missing:
            severity = "critical" if level == "beginner" else "moderate"

            suggestions = {
                "functions": "Break your code into reusable functions",
                "classes": "Consider using a class to organize related data and methods",
                "loops": "Use loops (for/while) to handle repetitive tasks",
                "conditionals": "Add conditional logic (if/else) to handle different cases",
                "error_handling": "Add try/except blocks to handle potential errors",
                "docstrings": "Add docstrings to explain what your functions do",
                "typing": "Add type hints to make your code more maintainable",
                "list_comprehension": "Consider using list comprehensions for cleaner list processing",
            }

            knowledge_gaps.append(KnowledgeGap(
                concept=concept,
                severity=severity,
                evidence=f"Expected to see '{concept}' but not found in code",
                suggestion=suggestions.get(concept, f"Review the '{concept}' concept")
            ))

    def _calculate_confidence(
        self,
        metrics: Dict[str, Any],
        knowledge_gaps: List[KnowledgeGap],
        demonstrated: List[str],
        expected: List[str]
    ) -> float:
        """Calculate confidence in student understanding (0.0 to 1.0)."""
        score = 0.5  # Start neutral

        # Positive indicators
        if metrics["functions_defined"] > 0:
            score += 0.10
        if metrics["classes_defined"] > 0:
            score += 0.10
        if metrics["has_docstrings"]:
            score += 0.10
        if metrics["has_type_hints"]:
            score += 0.10
        if metrics["has_error_handling"]:
            score += 0.10

        # Demonstrated expected concepts
        if expected:
            coverage = len(set(demonstrated) & set(expected)) / len(expected)
            score += coverage * 0.30

        # Negative indicators
        for gap in knowledge_gaps:
            if gap.severity == "critical":
                score -= 0.25
            elif gap.severity == "moderate":
                score -= 0.10
            elif gap.severity == "minor":
                score -= 0.05

        return max(0.0, min(1.0, score))

    def _build_result(
        self,
        demonstrates_understanding: bool,
        confidence: float,
        knowledge_gaps: List[KnowledgeGap],
        demonstrated: List[str],
        metrics: Dict[str, Any],
        level: str
    ) -> UnderstandingResult:
        """Build final understanding result."""
        # Generate recommended review topics
        recommended_review = []
        for gap in knowledge_gaps:
            if gap.severity in ["critical", "moderate"]:
                recommended_review.append(gap.concept)

        # Remove duplicates
        recommended_review = list(set(recommended_review))

        # Generate next learning steps
        next_steps = []
        if not demonstrates_understanding:
            # Focus on critical gaps first
            critical_gaps = [g for g in knowledge_gaps if g.severity == "critical"]
            if critical_gaps:
                next_steps.append(f"Review: {critical_gaps[0].concept}")
                next_steps.append(critical_gaps[0].suggestion)
            else:
                moderate_gaps = [g for g in knowledge_gaps if g.severity == "moderate"]
                if moderate_gaps:
                    next_steps.append(f"Improve: {moderate_gaps[0].concept}")
                    next_steps.append(moderate_gaps[0].suggestion)
        else:
            # Suggest advancement
            if level == "beginner" and confidence > 0.8:
                next_steps.append("Ready to explore intermediate concepts")
                next_steps.append("Consider learning about: classes, error handling, type hints")
            elif level == "intermediate" and confidence > 0.8:
                next_steps.append("Ready for advanced topics")
                next_steps.append("Consider learning about: decorators, context managers, metaclasses")
            else:
                next_steps.append("Continue practicing current concepts to build fluency")

        return UnderstandingResult(
            demonstrates_understanding=demonstrates_understanding,
            confidence_level=confidence,
            knowledge_gaps=knowledge_gaps,
            demonstrated_concepts=demonstrated,
            recommended_review=recommended_review,
            next_learning_steps=next_steps[:3],  # Top 3
            metrics=metrics
        )

"""
Pattern Detector

Detects design patterns in Python code.
"""

import ast
from typing import List

from .models import FileAnalysis, DesignPattern


class PatternDetector:
    """Detects design patterns in Python code"""

    def detect_patterns(self, analysis: FileAnalysis, tree: ast.AST) -> List[DesignPattern]:
        """
        Detect design patterns in a file.

        Args:
            analysis: FileAnalysis object
            tree: AST tree of the file

        Returns:
            List of detected patterns
        """
        patterns = []

        # Singleton pattern
        if self._has_singleton(analysis, tree):
            patterns.append(DesignPattern.SINGLETON)

        # Factory pattern
        if self._has_factory(analysis):
            patterns.append(DesignPattern.FACTORY)

        # Strategy pattern
        if self._has_strategy(analysis):
            patterns.append(DesignPattern.STRATEGY)

        # Decorator pattern (not Python @decorators)
        if self._has_decorator_pattern(analysis):
            patterns.append(DesignPattern.DECORATOR)

        # Observer pattern
        if self._has_observer(analysis):
            patterns.append(DesignPattern.OBSERVER)

        return patterns

    def _has_singleton(self, analysis: FileAnalysis, tree: ast.AST) -> bool:
        """Detect singleton pattern"""
        for cls in analysis.classes:
            # Check for __new__ override or _instance class variable
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == cls.name:
                    # Look for __new__ method
                    has_new = any(
                        isinstance(item, ast.FunctionDef) and item.name == "__new__"
                        for item in node.body
                    )

                    # Look for _instance variable
                    has_instance = any(
                        isinstance(item, ast.Assign)
                        and any(
                            isinstance(target, ast.Name)
                            and target.id == "_instance"
                            for target in item.targets
                        )
                        for item in node.body
                    )

                    if has_new or has_instance:
                        return True

        return False

    def _has_factory(self, analysis: FileAnalysis) -> bool:
        """Detect factory pattern"""
        # Look for classes or functions with "Factory" in name
        has_factory_class = any("Factory" in cls.name for cls in analysis.classes)

        # Look for create_* methods
        has_create_method = any(
            "create" in func.name.lower() or "make" in func.name.lower()
            for func in analysis.functions
        )

        return has_factory_class or has_create_method

    def _has_strategy(self, analysis: FileAnalysis) -> bool:
        """Detect strategy pattern"""
        # Look for multiple classes with similar method names
        if len(analysis.classes) < 2:
            return False

        # Check if classes have common method signatures
        class_methods = {}
        for cls in analysis.classes:
            class_methods[cls.name] = set(cls.calls)  # Methods

        # If multiple classes share common method names, might be strategies
        if len(class_methods) >= 2:
            method_sets = list(class_methods.values())
            common_methods = set.intersection(*method_sets)

            # If 2+ common methods, likely strategy pattern
            if len(common_methods) >= 2:
                return True

        return False

    def _has_decorator_pattern(self, analysis: FileAnalysis) -> bool:
        """Detect decorator pattern (wrapper classes)"""
        for cls in analysis.classes:
            # Look for "Decorator" or "Wrapper" in name
            if "Decorator" in cls.name or "Wrapper" in cls.name:
                return True

            # Look for classes that take another object in __init__
            # (This is a heuristic - would need deeper AST analysis)
            if "wrapped" in str(cls.calls).lower():
                return True

        return False

    def _has_observer(self, analysis: FileAnalysis) -> bool:
        """Detect observer pattern"""
        # Look for subscribe/notify/update methods
        observer_keywords = [
            "subscribe",
            "notify",
            "update",
            "attach",
            "detach",
            "observer",
        ]

        for func in analysis.functions:
            if any(keyword in func.name.lower() for keyword in observer_keywords):
                return True

        for cls in analysis.classes:
            if any(
                keyword in method.lower()
                for keyword in observer_keywords
                for method in cls.calls
            ):
                return True

        return False

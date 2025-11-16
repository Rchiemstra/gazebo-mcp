"""
Dynamic model selection based on task complexity.

Automatically selects the appropriate Claude model (Haiku, Sonnet, Opus) based on:
- Task complexity indicators
- File size and count
- Code complexity metrics
- Operation type

This optimizes for both cost and performance by using:
- Haiku (fast, cheap) for simple, well-defined tasks
- Sonnet (balanced) for moderate complexity
- Opus (powerful, expensive) for complex, ambiguous tasks
"""

from enum import Enum
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import re


class ClaudeModel(str, Enum):
    """Available Claude models with their characteristics."""

    HAIKU = "claude-haiku-4-5-20251001"  # Fast, cheap, simple tasks
    SONNET = "claude-sonnet-4-5-20250929"  # Balanced, most use cases
    OPUS = "claude-opus-4-5-20250929"  # Powerful, complex tasks

    @property
    def cost_tier(self) -> int:
        """Cost tier (1=cheapest, 3=most expensive)."""
        return {
            ClaudeModel.HAIKU: 1,
            ClaudeModel.SONNET: 2,
            ClaudeModel.OPUS: 3,
        }[self]

    @property
    def capability_tier(self) -> int:
        """Capability tier (1=basic, 3=advanced)."""
        return {
            ClaudeModel.HAIKU: 1,
            ClaudeModel.SONNET: 2,
            ClaudeModel.OPUS: 3,
        }[self]


class TaskComplexity(str, Enum):
    """Task complexity levels."""

    SIMPLE = "simple"  # Well-defined, straightforward tasks
    MODERATE = "moderate"  # Standard development tasks
    COMPLEX = "complex"  # Ambiguous, multi-faceted tasks


@dataclass
class ComplexityFactors:
    """Factors that contribute to task complexity."""

    # File/data factors
    file_count: int = 0
    total_lines: int = 0
    avg_file_size: int = 0

    # Code complexity factors
    avg_cyclomatic_complexity: float = 0.0
    max_cyclomatic_complexity: int = 0
    num_functions: int = 0
    num_classes: int = 0

    # Task factors
    requires_creativity: bool = False
    requires_architecture: bool = False
    requires_refactoring: bool = False
    is_debugging: bool = False
    is_code_generation: bool = False
    is_analysis_only: bool = False

    # Ambiguity factors
    has_unclear_requirements: bool = False
    requires_decision_making: bool = False
    involves_tradeoffs: bool = False

    # Workload factors
    parallel_operations: int = 0
    estimated_duration_minutes: int = 0


class ModelSelector:
    """
    Intelligently select Claude model based on task complexity.

    Usage:
        # Enabled (default)
        selector = ModelSelector(enabled=True)
        model = selector.select_for_operation("verify_lint")
        # Returns: ClaudeModel.HAIKU (optimized for simple task)

        # Disabled (always use default)
        selector = ModelSelector(enabled=False, default_model=ClaudeModel.SONNET)
        model = selector.select_for_operation("verify_lint")
        # Returns: ClaudeModel.SONNET (ignores complexity, uses default)

        # Complex task with factors
        factors = ComplexityFactors(
            file_count=50,
            avg_cyclomatic_complexity=15.0,
            requires_architecture=True
        )
        model = selector.select_from_factors(factors)
        # Returns: ClaudeModel.SONNET or OPUS
    """

    # Operation complexity mappings
    SIMPLE_OPERATIONS = {
        "verify_lint", "verify_build", "format_code",
        "run_tests", "list_files", "read_file",
        "simple_search", "basic_analysis"
    }

    MODERATE_OPERATIONS = {
        "verify_all", "analyze_file", "analyze_codebase",
        "generate_tests", "refactor_function", "add_documentation",
        "fix_bug", "implement_feature", "code_review"
    }

    COMPLEX_OPERATIONS = {
        "design_architecture", "major_refactor", "debug_complex_issue",
        "optimize_performance", "design_api", "implement_pattern",
        "cross_language_integration", "system_design"
    }

    def __init__(
        self,
        enabled: bool = True,
        default_model: ClaudeModel = ClaudeModel.SONNET,
        cost_conscious: bool = True,
        prefer_quality: bool = False
    ):
        """
        Initialize model selector.

        Args:
            enabled: Enable dynamic model selection (if False, always uses default_model)
            default_model: Default model when complexity is unclear or when disabled
            cost_conscious: Prefer cheaper models when possible
            prefer_quality: Prefer higher-tier models for borderline cases
        """
        self.enabled = enabled
        self.default_model = default_model
        self.cost_conscious = cost_conscious
        self.prefer_quality = prefer_quality

    def select_for_operation(
        self,
        operation: str,
        override_factors: Optional[ComplexityFactors] = None
    ) -> ClaudeModel:
        """
        Select model for a named operation.

        Args:
            operation: Operation name (e.g., "verify_lint", "analyze_codebase")
            override_factors: Optional complexity factors to override default assessment

        Returns:
            Appropriate Claude model for the operation
        """
        # If dynamic selection disabled, always use default
        if not self.enabled:
            return self.default_model

        # Check operation complexity
        if operation in self.SIMPLE_OPERATIONS:
            base_complexity = TaskComplexity.SIMPLE
        elif operation in self.MODERATE_OPERATIONS:
            base_complexity = TaskComplexity.MODERATE
        elif operation in self.COMPLEX_OPERATIONS:
            base_complexity = TaskComplexity.COMPLEX
        else:
            # Unknown operation - use default
            return self.default_model

        # If override factors provided, use them
        if override_factors:
            return self.select_from_factors(override_factors)

        # Map base complexity to model
        return self._complexity_to_model(base_complexity)

    def select_from_factors(self, factors: ComplexityFactors) -> ClaudeModel:
        """
        Select model based on detailed complexity factors.

        Args:
            factors: Complexity factors for the task

        Returns:
            Appropriate Claude model
        """
        # If dynamic selection disabled, always use default
        if not self.enabled:
            return self.default_model

        complexity = self._assess_complexity(factors)
        return self._complexity_to_model(complexity)

    def select_for_codebase(
        self,
        file_count: int,
        total_lines: int,
        avg_complexity: float = 0.0,
        operation_type: str = "analysis"
    ) -> ClaudeModel:
        """
        Select model for codebase operations.

        Args:
            file_count: Number of files to analyze
            total_lines: Total lines of code
            avg_complexity: Average cyclomatic complexity
            operation_type: Type of operation (analysis, refactor, etc.)

        Returns:
            Appropriate Claude model
        """
        factors = ComplexityFactors(
            file_count=file_count,
            total_lines=total_lines,
            avg_file_size=total_lines // max(file_count, 1),
            avg_cyclomatic_complexity=avg_complexity,
            is_analysis_only="analysis" in operation_type.lower(),
            requires_refactoring="refactor" in operation_type.lower(),
            requires_architecture="design" in operation_type.lower() or "architecture" in operation_type.lower()
        )

        return self.select_from_factors(factors)

    def select_for_prompt(self, prompt: str) -> ClaudeModel:
        """
        Select model based on prompt text analysis.

        Analyzes the prompt for complexity indicators:
        - Keywords suggesting complexity
        - Length and structure
        - Ambiguity markers

        Args:
            prompt: The task prompt/description

        Returns:
            Appropriate Claude model
        """
        factors = self._analyze_prompt(prompt)
        return self.select_from_factors(factors)

    def _assess_complexity(self, factors: ComplexityFactors) -> TaskComplexity:
        """Assess overall task complexity from factors."""
        score = 0

        # File/data complexity (0-3 points)
        if factors.file_count > 50 or factors.total_lines > 10000:
            score += 3
        elif factors.file_count > 20 or factors.total_lines > 5000:
            score += 2
        elif factors.file_count > 5 or factors.total_lines > 1000:
            score += 1

        # Code complexity (0-3 points)
        if factors.avg_cyclomatic_complexity > 15 or factors.max_cyclomatic_complexity > 30:
            score += 3
        elif factors.avg_cyclomatic_complexity > 10 or factors.max_cyclomatic_complexity > 20:
            score += 2
        elif factors.avg_cyclomatic_complexity > 5 or factors.max_cyclomatic_complexity > 10:
            score += 1

        # Task type complexity (0-4 points)
        if factors.requires_architecture or factors.requires_creativity:
            score += 2
        if factors.is_debugging and factors.has_unclear_requirements:
            score += 2
        elif factors.is_code_generation:
            score += 1

        # Ambiguity (0-3 points)
        if factors.has_unclear_requirements:
            score += 1
        if factors.requires_decision_making:
            score += 1
        if factors.involves_tradeoffs:
            score += 1

        # Workload (0-2 points)
        if factors.parallel_operations > 10 or factors.estimated_duration_minutes > 30:
            score += 2
        elif factors.parallel_operations > 5 or factors.estimated_duration_minutes > 15:
            score += 1

        # Bonuses
        if factors.is_analysis_only:
            score -= 1  # Analysis is simpler than generation

        # Map score to complexity
        # Total possible: 15 points
        if score <= 3:
            return TaskComplexity.SIMPLE
        elif score <= 8:
            return TaskComplexity.MODERATE
        else:
            return TaskComplexity.COMPLEX

    def _complexity_to_model(self, complexity: TaskComplexity) -> ClaudeModel:
        """Map complexity level to Claude model."""
        if complexity == TaskComplexity.SIMPLE:
            return ClaudeModel.HAIKU
        elif complexity == TaskComplexity.MODERATE:
            return ClaudeModel.SONNET
        else:  # TaskComplexity.COMPLEX
            # Use Opus for complex tasks only if not cost-conscious
            # or if prefer_quality is set
            if self.prefer_quality and not self.cost_conscious:
                return ClaudeModel.OPUS
            else:
                # Sonnet can handle most complex tasks well
                return ClaudeModel.SONNET

    def _analyze_prompt(self, prompt: str) -> ComplexityFactors:
        """Analyze prompt text for complexity indicators."""
        prompt_lower = prompt.lower()

        # Keywords indicating complexity
        creativity_keywords = ["design", "create", "architect", "invent", "innovative"]
        architecture_keywords = ["architecture", "system design", "structure", "organize"]
        refactor_keywords = ["refactor", "restructure", "reorganize", "improve"]
        debug_keywords = ["debug", "fix", "troubleshoot", "diagnose", "issue"]
        unclear_keywords = ["maybe", "possibly", "unclear", "not sure", "might"]
        decision_keywords = ["decide", "choose", "which", "better", "best approach"]
        tradeoff_keywords = ["tradeoff", "trade-off", "balance", "pros and cons"]

        factors = ComplexityFactors(
            requires_creativity=any(kw in prompt_lower for kw in creativity_keywords),
            requires_architecture=any(kw in prompt_lower for kw in architecture_keywords),
            requires_refactoring=any(kw in prompt_lower for kw in refactor_keywords),
            is_debugging=any(kw in prompt_lower for kw in debug_keywords),
            has_unclear_requirements=any(kw in prompt_lower for kw in unclear_keywords),
            requires_decision_making=any(kw in prompt_lower for kw in decision_keywords),
            involves_tradeoffs=any(kw in prompt_lower for kw in tradeoff_keywords),
        )

        # Estimate complexity from prompt length and structure
        word_count = len(prompt.split())
        if word_count > 100:
            factors.estimated_duration_minutes = 30
        elif word_count > 50:
            factors.estimated_duration_minutes = 15
        else:
            factors.estimated_duration_minutes = 5

        # Check for code generation indicators
        code_indicators = ["implement", "write", "generate", "create code"]
        factors.is_code_generation = any(ind in prompt_lower for ind in code_indicators)

        # Check for analysis-only
        analysis_indicators = ["analyze", "explain", "describe", "understand", "review"]
        action_indicators = ["implement", "write", "fix", "create", "build"]
        if any(ind in prompt_lower for ind in analysis_indicators) and \
           not any(ind in prompt_lower for ind in action_indicators):
            factors.is_analysis_only = True

        return factors

    def explain_selection(
        self,
        model: ClaudeModel,
        factors: Optional[ComplexityFactors] = None
    ) -> str:
        """
        Explain why a particular model was selected.

        Args:
            model: The selected model
            factors: Optional complexity factors used for selection

        Returns:
            Human-readable explanation
        """
        explanation = f"Selected {model.value} "

        if model == ClaudeModel.HAIKU:
            explanation += "(fast, cost-effective for simple tasks)\n"
        elif model == ClaudeModel.SONNET:
            explanation += "(balanced for most use cases)\n"
        else:  # OPUS
            explanation += "(powerful for complex tasks)\n"

        if factors:
            complexity = self._assess_complexity(factors)
            explanation += f"Assessed complexity: {complexity.value}\n"

            # Highlight key factors
            key_factors = []
            if factors.file_count > 20:
                key_factors.append(f"{factors.file_count} files")
            if factors.avg_cyclomatic_complexity > 10:
                key_factors.append(f"avg complexity {factors.avg_cyclomatic_complexity:.1f}")
            if factors.requires_architecture:
                key_factors.append("architecture required")
            if factors.has_unclear_requirements:
                key_factors.append("unclear requirements")

            if key_factors:
                explanation += "Key factors: " + ", ".join(key_factors)

        return explanation


# Convenience functions
def select_model_for_operation(operation: str) -> ClaudeModel:
    """Quick model selection for operation name."""
    selector = ModelSelector()
    return selector.select_for_operation(operation)


def select_model_for_codebase(file_count: int, total_lines: int) -> ClaudeModel:
    """Quick model selection for codebase size."""
    selector = ModelSelector()
    return selector.select_for_codebase(file_count, total_lines)


def select_model_for_prompt(prompt: str) -> ClaudeModel:
    """Quick model selection from prompt analysis."""
    selector = ModelSelector()
    return selector.select_for_prompt(prompt)

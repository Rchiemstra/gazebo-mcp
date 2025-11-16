"""
Improvement Engine

AI-powered improvement suggestion engine using specialized agents.
"""

import json
from typing import Dict, Any, List, Optional
from pathlib import Path

from skills.skill_evaluator.core.models import (
    ImprovementSuggestion,
    ImprovementCategory,
    ImprovementSeverity,
    SkillEvaluationMetrics
)
from skills.skill_evaluator.core.history_tracker import ExecutionHistoryTracker


class ImprovementEngine:
    """
    AI-powered improvement suggestion engine.

    Uses specialized agents via Task tool to analyze skills and generate
    intelligent, context-aware improvement suggestions.
    """

    def __init__(self, history_tracker: ExecutionHistoryTracker):
        """
        Initialize the improvement engine.

        Args:
            history_tracker: ExecutionHistoryTracker for accessing execution data
        """
        self.history_tracker = history_tracker

    def generate_suggestions(
        self,
        skill_name: str,
        metrics: SkillEvaluationMetrics,
        focus_areas: Optional[List[str]] = None,
        use_ai_agents: bool = True
    ) -> List[ImprovementSuggestion]:
        """
        Generate comprehensive improvement suggestions.

        Args:
            skill_name: Name of the skill
            metrics: Current evaluation metrics
            focus_areas: Specific areas to focus on (None for all)
            use_ai_agents: Whether to use AI agents for analysis

        Returns:
            List of improvement suggestions
        """
        suggestions = []

        # Start with basic metric-based suggestions
        suggestions.extend(self._generate_metric_based_suggestions(metrics))

        # Add failure pattern suggestions
        failed_records = self.history_tracker.get_failed_executions(skill_name, limit=50)
        if failed_records:
            suggestions.extend(self._analyze_failure_patterns(failed_records))

        # If AI agents enabled and we have code to analyze
        if use_ai_agents:
            # Note: In a real implementation, we would use Task tool here
            # For Phase 3, we'll simulate AI agent suggestions based on metrics
            ai_suggestions = self._simulate_ai_agent_analysis(skill_name, metrics)
            suggestions.extend(ai_suggestions)

        # Deduplicate and prioritize
        suggestions = self._deduplicate_suggestions(suggestions)
        suggestions = self._prioritize_suggestions(suggestions, metrics)

        return suggestions

    def _generate_metric_based_suggestions(
        self,
        metrics: SkillEvaluationMetrics
    ) -> List[ImprovementSuggestion]:
        """Generate suggestions based on evaluation metrics."""
        suggestions = []

        # Performance suggestions
        if metrics.performance_scores.performance_score < 70:
            suggestions.append(ImprovementSuggestion(
                category=ImprovementCategory.PERFORMANCE.value,
                severity=ImprovementSeverity.HIGH.value if metrics.performance_scores.performance_score < 50 else ImprovementSeverity.MEDIUM.value,
                description="Optimize execution performance to reduce latency",
                expected_impact="Reduce average execution time by 30-50%",
                confidence=0.75,
                can_auto_apply=False
            ))

        # Regression handling
        if metrics.performance_scores.has_regression:
            severity = ImprovementSeverity.CRITICAL.value
            if metrics.performance_scores.regression_details:
                degradation = metrics.performance_scores.regression_details.get('degradation_percent', 0)
                if degradation > 100:
                    severity = ImprovementSeverity.CRITICAL.value
                elif degradation > 50:
                    severity = ImprovementSeverity.HIGH.value
                else:
                    severity = ImprovementSeverity.MEDIUM.value

            suggestions.append(ImprovementSuggestion(
                category=ImprovementCategory.PERFORMANCE.value,
                severity=severity,
                description="Fix performance regression detected in recent executions",
                expected_impact="Restore performance to baseline levels",
                confidence=0.90,
                can_auto_apply=False
            ))

        # Reliability suggestions
        if metrics.reliability_scores.reliability_score < 80:
            suggestions.append(ImprovementSuggestion(
                category=ImprovementCategory.RELIABILITY.value,
                severity=ImprovementSeverity.HIGH.value if metrics.reliability_scores.error_rate > 30 else ImprovementSeverity.MEDIUM.value,
                description=f"Improve reliability - current error rate: {metrics.reliability_scores.error_rate:.1f}%",
                expected_impact="Reduce error rate by 40-60%",
                confidence=0.80,
                can_auto_apply=False
            ))

        # Error handling quality
        if metrics.reliability_scores.error_handling_quality < 70:
            suggestions.append(ImprovementSuggestion(
                category=ImprovementCategory.QUALITY.value,
                severity=ImprovementSeverity.MEDIUM.value,
                description="Improve error messages to be more descriptive and actionable",
                expected_impact="Better debuggability and faster issue resolution",
                confidence=0.65,
                can_auto_apply=False
            ))

        # Code quality suggestions
        if metrics.code_quality_scores.complexity_score > 70:
            suggestions.append(ImprovementSuggestion(
                category=ImprovementCategory.MAINTAINABILITY.value,
                severity=ImprovementSeverity.MEDIUM.value,
                description="Refactor complex code to improve maintainability",
                expected_impact="Reduce complexity by 30-40%, improve long-term maintainability",
                confidence=0.70,
                can_auto_apply=False
            ))

        # Test coverage
        if metrics.code_quality_scores.test_coverage < 60:
            suggestions.append(ImprovementSuggestion(
                category=ImprovementCategory.QUALITY.value,
                severity=ImprovementSeverity.MEDIUM.value,
                description=f"Increase test coverage from {metrics.code_quality_scores.test_coverage:.0f}% to at least 80%",
                expected_impact="Catch more bugs before production, improve confidence in changes",
                confidence=0.85,
                can_auto_apply=False
            ))

        # Documentation
        if metrics.code_quality_scores.documentation_score < 70:
            suggestions.append(ImprovementSuggestion(
                category=ImprovementCategory.DOCUMENTATION.value,
                severity=ImprovementSeverity.LOW.value,
                description="Improve documentation coverage and quality",
                expected_impact="Better developer experience and faster onboarding",
                confidence=0.70,
                can_auto_apply=False
            ))

        return suggestions

    def _analyze_failure_patterns(
        self,
        failed_records: List
    ) -> List[ImprovementSuggestion]:
        """Analyze failure patterns and generate suggestions."""
        suggestions = []

        if not failed_records:
            return suggestions

        # Group by error code
        error_groups = {}
        for record in failed_records:
            if record.error_code:
                if record.error_code not in error_groups:
                    error_groups[record.error_code] = []
                error_groups[record.error_code].append(record)

        # Generate suggestions for common errors
        for error_code, records in error_groups.items():
            if len(records) >= 3:  # At least 3 occurrences
                percentage = (len(records) / len(failed_records)) * 100

                suggestions.append(ImprovementSuggestion(
                    category=ImprovementCategory.RELIABILITY.value,
                    severity=ImprovementSeverity.HIGH.value if percentage > 50 else ImprovementSeverity.MEDIUM.value,
                    description=f"Address recurring error: {error_code} ({len(records)} occurrences, {percentage:.0f}% of failures)",
                    expected_impact="Reduce error rate significantly",
                    confidence=0.85,
                    can_auto_apply=False
                ))

        return suggestions

    def _simulate_ai_agent_analysis(
        self,
        skill_name: str,
        metrics: SkillEvaluationMetrics
    ) -> List[ImprovementSuggestion]:
        """
        Simulate AI agent analysis.

        Note: In a real implementation, this would use Task tool to invoke:
        - Explore agent for code understanding
        - code-architecture-mentor for design advice
        - debugging-detective for failure analysis
        - python-best-practices for optimizations

        For Phase 3, we simulate intelligent suggestions based on metrics.
        """
        suggestions = []

        # Simulate architecture mentor suggestions
        if metrics.code_quality_scores.complexity_score > 60:
            suggestions.append(ImprovementSuggestion(
                category=ImprovementCategory.MAINTAINABILITY.value,
                severity=ImprovementSeverity.MEDIUM.value,
                description="Consider applying Single Responsibility Principle to reduce coupling",
                location=f"skills/{skill_name}/operations.py",
                expected_impact="Improve maintainability and testability",
                confidence=0.75,
                can_auto_apply=False,
                metadata={
                    'agent': 'code-architecture-mentor',
                    'pattern': 'single_responsibility'
                }
            ))

        # Simulate performance optimization suggestions
        if metrics.performance_scores.performance_score < 80:
            suggestions.append(ImprovementSuggestion(
                category=ImprovementCategory.PERFORMANCE.value,
                severity=ImprovementSeverity.MEDIUM.value,
                description="Add caching for expensive computations to improve response time",
                location=f"skills/{skill_name}/core/",
                expected_impact="30-40% reduction in execution time for repeated operations",
                confidence=0.70,
                can_auto_apply=False,
                metadata={
                    'agent': 'python-best-practices',
                    'technique': 'caching'
                }
            ))

        # Simulate debugging detective suggestions for reliability issues
        if metrics.reliability_scores.error_rate > 15:
            suggestions.append(ImprovementSuggestion(
                category=ImprovementCategory.RELIABILITY.value,
                severity=ImprovementSeverity.HIGH.value,
                description="Add defensive error handling with proper exception hierarchy",
                location=f"skills/{skill_name}/operations.py",
                expected_impact="Reduce error rate by 40-50%",
                confidence=0.80,
                can_auto_apply=False,
                metadata={
                    'agent': 'debugging-detective',
                    'approach': 'defensive_programming'
                }
            ))

        # Simulate code quality suggestions
        if metrics.code_quality_scores.maintainability_index < 70:
            suggestions.append(ImprovementSuggestion(
                category=ImprovementCategory.MAINTAINABILITY.value,
                severity=ImprovementSeverity.MEDIUM.value,
                description="Extract complex logic into smaller, well-named helper functions",
                location=f"skills/{skill_name}/core/",
                expected_impact="Improve code readability and reduce bug density",
                confidence=0.75,
                can_auto_apply=False,
                metadata={
                    'agent': 'python-best-practices',
                    'refactoring': 'extract_function'
                }
            ))

        return suggestions

    def _deduplicate_suggestions(
        self,
        suggestions: List[ImprovementSuggestion]
    ) -> List[ImprovementSuggestion]:
        """Remove duplicate or very similar suggestions."""
        seen = set()
        unique = []

        for suggestion in suggestions:
            # Create a key based on category and description (simplified)
            key = (suggestion.category, suggestion.description[:50])

            if key not in seen:
                seen.add(key)
                unique.append(suggestion)

        return unique

    def _prioritize_suggestions(
        self,
        suggestions: List[ImprovementSuggestion],
        metrics: SkillEvaluationMetrics
    ) -> List[ImprovementSuggestion]:
        """Prioritize suggestions based on impact and current state."""

        # Define priority scores
        severity_scores = {
            ImprovementSeverity.CRITICAL.value: 100,
            ImprovementSeverity.HIGH.value: 75,
            ImprovementSeverity.MEDIUM.value: 50,
            ImprovementSeverity.LOW.value: 25
        }

        category_weights = {
            ImprovementCategory.PERFORMANCE.value: 1.2 if metrics.performance_scores.performance_score < 70 else 1.0,
            ImprovementCategory.RELIABILITY.value: 1.3 if metrics.reliability_scores.reliability_score < 80 else 1.0,
            ImprovementCategory.QUALITY.value: 1.0,
            ImprovementCategory.MAINTAINABILITY.value: 0.9,
            ImprovementCategory.SECURITY.value: 1.5,
            ImprovementCategory.DOCUMENTATION.value: 0.8
        }

        # Calculate priority score for each suggestion
        def calculate_priority(suggestion: ImprovementSuggestion) -> float:
            base_score = severity_scores.get(suggestion.severity, 50)
            category_weight = category_weights.get(suggestion.category, 1.0)
            confidence_boost = suggestion.confidence * 20  # Up to 20 point boost

            return base_score * category_weight + confidence_boost

        # Sort by priority (descending)
        suggestions.sort(key=calculate_priority, reverse=True)

        return suggestions

    def generate_action_plan(
        self,
        suggestions: List[ImprovementSuggestion],
        max_items: int = 5
    ) -> Dict[str, Any]:
        """
        Generate an actionable implementation plan.

        Args:
            suggestions: List of improvement suggestions
            max_items: Maximum items in the plan

        Returns:
            Structured action plan
        """
        if not suggestions:
            return {
                'has_plan': False,
                'message': 'No improvements needed - skill is performing well'
            }

        # Take top N suggestions
        top_suggestions = suggestions[:max_items]

        # Group by category
        by_category = {}
        for suggestion in top_suggestions:
            category = suggestion.category
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(suggestion)

        # Create phased plan
        phases = []

        # Phase 1: Critical and High severity
        critical_high = [s for s in top_suggestions if s.severity in [
            ImprovementSeverity.CRITICAL.value,
            ImprovementSeverity.HIGH.value
        ]]

        if critical_high:
            phases.append({
                'phase': 1,
                'name': 'Critical Fixes',
                'description': 'Address critical and high-priority issues',
                'items': [
                    {
                        'description': s.description,
                        'category': s.category,
                        'severity': s.severity,
                        'expected_impact': s.expected_impact
                    }
                    for s in critical_high
                ],
                'estimated_effort': 'High',
                'timeline': '1-2 weeks'
            })

        # Phase 2: Medium severity
        medium = [s for s in top_suggestions if s.severity == ImprovementSeverity.MEDIUM.value]

        if medium:
            phases.append({
                'phase': 2,
                'name': 'Performance & Quality Improvements',
                'description': 'Enhance performance and code quality',
                'items': [
                    {
                        'description': s.description,
                        'category': s.category,
                        'severity': s.severity,
                        'expected_impact': s.expected_impact
                    }
                    for s in medium
                ],
                'estimated_effort': 'Medium',
                'timeline': '1 week'
            })

        # Phase 3: Low severity
        low = [s for s in top_suggestions if s.severity == ImprovementSeverity.LOW.value]

        if low:
            phases.append({
                'phase': 3,
                'name': 'Polish & Documentation',
                'description': 'Final touches and documentation',
                'items': [
                    {
                        'description': s.description,
                        'category': s.category,
                        'severity': s.severity,
                        'expected_impact': s.expected_impact
                    }
                    for s in low
                ],
                'estimated_effort': 'Low',
                'timeline': '2-3 days'
            })

        return {
            'has_plan': True,
            'total_suggestions': len(suggestions),
            'plan_items': len(top_suggestions),
            'phases': phases,
            'by_category': {
                category: len(items)
                for category, items in by_category.items()
            },
            'estimated_total_effort': self._estimate_total_effort(top_suggestions)
        }

    def _estimate_total_effort(self, suggestions: List[ImprovementSuggestion]) -> str:
        """Estimate total implementation effort."""
        critical_high_count = sum(
            1 for s in suggestions
            if s.severity in [ImprovementSeverity.CRITICAL.value, ImprovementSeverity.HIGH.value]
        )

        if critical_high_count >= 3:
            return 'High (2-3 weeks)'
        elif critical_high_count >= 1:
            return 'Medium (1-2 weeks)'
        else:
            return 'Low (3-5 days)'

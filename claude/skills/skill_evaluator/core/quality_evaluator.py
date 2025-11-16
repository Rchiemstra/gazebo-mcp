"""
Quality Evaluator

Evaluates skill quality across multiple dimensions.
"""

import statistics
from typing import Dict, Any, List, Optional
from collections import Counter

from skills.skill_evaluator.core.models import (
    SkillEvaluationMetrics,
    QualityScores,
    PerformanceScores,
    ReliabilityScores,
    CodeQualityScores,
    HealthTrend,
    ImprovementSuggestion,
    ImprovementCategory,
    ImprovementSeverity
)
from skills.skill_evaluator.core.history_tracker import ExecutionHistoryTracker
from skills.skill_evaluator.core.code_analyzer import CodeAnalyzer


class QualityEvaluator:
    """
    Evaluates skill quality across multiple dimensions.

    Analyzes execution history, code patterns, and performance to generate
    comprehensive quality metrics and improvement suggestions.
    """

    def __init__(self, history_tracker: ExecutionHistoryTracker):
        """
        Initialize the quality evaluator.

        Args:
            history_tracker: ExecutionHistoryTracker for accessing execution data
        """
        self.history_tracker = history_tracker
        self.code_analyzer = CodeAnalyzer()

    def evaluate(
        self,
        skill_name: str,
        execution_samples: int = 100,
        include_code_analysis: bool = True,
        time_period_days: Optional[int] = None
    ) -> SkillEvaluationMetrics:
        """
        Perform comprehensive quality evaluation.

        Args:
            skill_name: Name of the skill to evaluate
            execution_samples: Number of recent executions to analyze
            include_code_analysis: Whether to perform code analysis
            time_period_days: Limit analysis to recent days (None for all)

        Returns:
            SkillEvaluationMetrics with complete evaluation
        """
        # Get execution data
        stats = self.history_tracker.get_execution_stats(
            skill_name,
            time_period_days=time_period_days
        )

        since = None
        if time_period_days:
            import time
            from datetime import datetime, timedelta
            since = (datetime.now() - timedelta(days=time_period_days)).timestamp()

        records = self.history_tracker.get_recent_executions(
            skill_name,
            limit=execution_samples,
            since=since
        )

        # Initialize metrics
        metrics = SkillEvaluationMetrics(
            skill_name=skill_name,
            execution_samples_analyzed=len(records),
            time_period_days=time_period_days or 0
        )

        if not records:
            # No data available
            metrics.weaknesses.append("No execution data available for analysis")
            return metrics

        # Evaluate each dimension
        metrics.quality_scores = self._evaluate_quality(records, stats)
        metrics.performance_scores = self._evaluate_performance(records, stats, skill_name)
        metrics.reliability_scores = self._evaluate_reliability(records, stats)

        # Code quality evaluation (basic for Phase 1)
        if include_code_analysis:
            metrics.code_quality_scores = self._evaluate_code_quality(skill_name)

        # Calculate overall health
        metrics.calculate_overall_health()

        # Determine trend
        metrics.health_trend = self._determine_trend(skill_name, time_period_days or 7)

        # Identify strengths and weaknesses
        metrics.strengths = self._identify_strengths(metrics)
        metrics.weaknesses = self._identify_weaknesses(metrics)

        # Generate improvement opportunities
        metrics.improvement_opportunities = self._generate_improvements(metrics, records, stats)

        # Identify priority fixes
        metrics.priority_fixes = self._identify_priority_fixes(metrics)

        return metrics

    def _evaluate_quality(
        self,
        records: List,
        stats: Dict[str, Any]
    ) -> QualityScores:
        """Evaluate quality dimension."""
        scores = QualityScores()

        # Output quality based on success patterns
        successful = [r for r in records if r.success]
        if successful:
            # Check for consistent outputs
            consistent_count = 0
            for i in range(min(10, len(successful) - 1)):
                if successful[i].operation == successful[i + 1].operation:
                    consistent_count += 1

            scores.consistency_score = min(100, (consistent_count / 10) * 100) if successful else 0

            # Correctness approximated by success rate
            scores.correctness_score = stats['success_rate']

            # Output quality: penalize if warnings are common
            warnings_count = sum(len(r.warnings) for r in records if hasattr(r, 'warnings') and r.warnings)
            warnings_ratio = warnings_count / len(records) if records else 0
            scores.output_quality_score = max(0, 100 - (warnings_ratio * 50))

        # Completeness: check if operations provide all expected data
        complete_results = sum(1 for r in successful if r.result_data)
        scores.completeness_score = (complete_results / len(successful) * 100) if successful else 0

        return scores

    def _evaluate_performance(
        self,
        records: List,
        stats: Dict[str, Any],
        skill_name: str
    ) -> PerformanceScores:
        """Evaluate performance dimension."""
        scores = PerformanceScores()

        if not records:
            return scores

        # Get baseline for comparison
        baseline = self.history_tracker.get_performance_baseline(skill_name, days=7)

        # Calculate performance score based on duration
        durations = [r.duration for r in records if r.success]
        if durations:
            scores.avg_duration = statistics.mean(durations)

            # Performance score: lower duration is better
            # Score 100 for <1s, decreasing to 0 at 60s
            avg_duration = scores.avg_duration
            if avg_duration < 1:
                scores.performance_score = 100
            elif avg_duration < 60:
                scores.performance_score = max(0, 100 - (avg_duration / 60 * 100))
            else:
                scores.performance_score = max(0, 20 - (avg_duration / 600 * 20))

        # Check for regression
        if baseline and len(durations) > 10:
            current_avg = statistics.mean(durations[-10:])
            baseline_avg = baseline['avg_duration']

            if current_avg > baseline_avg * 1.3:  # 30% degradation
                scores.has_regression = True
                scores.regression_details = {
                    'current_avg': current_avg,
                    'baseline_avg': baseline_avg,
                    'degradation_percent': ((current_avg - baseline_avg) / baseline_avg) * 100
                }
                scores.duration_trend = HealthTrend.DECLINING.value
            elif current_avg < baseline_avg * 0.8:  # 20% improvement
                scores.duration_trend = HealthTrend.IMPROVING.value
            else:
                scores.duration_trend = HealthTrend.STABLE.value

        # Resource efficiency (placeholder for Phase 1)
        # In Phase 2, we'll add CPU/memory analysis
        scores.resource_efficiency = 80  # Default moderate score

        return scores

    def _evaluate_reliability(
        self,
        records: List,
        stats: Dict[str, Any]
    ) -> ReliabilityScores:
        """Evaluate reliability dimension."""
        scores = ReliabilityScores()

        scores.success_rate = stats['success_rate']
        scores.error_rate = stats['error_rate']

        # Reliability score based on success rate
        scores.reliability_score = stats['success_rate']

        # Error handling quality: check for informative error messages
        failed = [r for r in records if not r.success]
        if failed:
            with_error_msg = sum(1 for r in failed if r.error and len(r.error) > 10)
            with_error_code = sum(1 for r in failed if r.error_code)

            error_msg_ratio = with_error_msg / len(failed)
            error_code_ratio = with_error_code / len(failed)

            scores.error_handling_quality = (error_msg_ratio * 50 + error_code_ratio * 50)
        else:
            scores.error_handling_quality = 100  # No failures to judge

        # Recovery capability: check for successful retries after failures
        # (simplified for Phase 1)
        scores.recovery_capability = 70  # Default moderate score

        return scores

    def _evaluate_code_quality(self, skill_name: str) -> CodeQualityScores:
        """
        Evaluate code quality dimension using AST analysis (Phase 3).
        """
        scores = CodeQualityScores()

        try:
            # Use CodeAnalyzer for real analysis
            analysis = self.code_analyzer.analyze_skill(skill_name)

            if analysis.get('success'):
                # Use actual metrics from code analysis
                scores.complexity_score = 100 - analysis['complexity_score']  # Invert so higher is better for overall score
                scores.maintainability_index = analysis['maintainability_index']

                # Code quality score based on complexity and maintainability
                scores.code_quality_score = (scores.maintainability_index + analysis['complexity_score']) / 2

                # Test coverage (estimate based on presence of test files)
                # In a real implementation, would use coverage.py
                scores.test_coverage = 60  # Default estimate

                # Documentation score (estimate based on docstrings)
                # In a real implementation, would analyze docstring coverage
                scores.documentation_score = 70  # Default estimate

            else:
                # Fall back to defaults if analysis fails
                scores.code_quality_score = 75
                scores.maintainability_index = 75
                scores.complexity_score = 30
                scores.test_coverage = 60
                scores.documentation_score = 70

        except Exception:
            # Fall back to defaults on any error
            scores.code_quality_score = 75
            scores.maintainability_index = 75
            scores.complexity_score = 30
            scores.test_coverage = 60
            scores.documentation_score = 70

        return scores

    def _determine_trend(self, skill_name: str, days: int) -> str:
        """Determine health trend."""
        try:
            # Compare current period with previous period
            current_stats = self.history_tracker.get_execution_stats(
                skill_name,
                time_period_days=days
            )

            previous_stats = self.history_tracker.get_execution_stats(
                skill_name,
                time_period_days=days * 2
            )

            if current_stats['total_executions'] < 10:
                return HealthTrend.UNKNOWN.value

            # Trend based on error rate change
            error_delta = current_stats['error_rate'] - previous_stats['error_rate']

            if error_delta < -10:
                return HealthTrend.IMPROVING.value
            elif error_delta > 10:
                return HealthTrend.DECLINING.value
            else:
                return HealthTrend.STABLE.value

        except Exception:
            return HealthTrend.UNKNOWN.value

    def _identify_strengths(self, metrics: SkillEvaluationMetrics) -> List[str]:
        """Identify skill strengths."""
        strengths = []

        # Check each dimension
        if metrics.quality_scores.overall_score() >= 80:
            strengths.append("High output quality and consistency")

        if metrics.performance_scores.performance_score >= 80:
            strengths.append("Excellent performance with low latency")

        if metrics.reliability_scores.reliability_score >= 90:
            strengths.append("Highly reliable with low error rate")

        if metrics.reliability_scores.error_handling_quality >= 80:
            strengths.append("Good error handling with informative messages")

        if not metrics.performance_scores.has_regression:
            strengths.append("Stable performance with no recent regressions")

        if metrics.health_trend == HealthTrend.IMPROVING.value:
            strengths.append("Improving health trend over time")

        return strengths if strengths else ["Skill is operational"]

    def _identify_weaknesses(self, metrics: SkillEvaluationMetrics) -> List[str]:
        """Identify skill weaknesses."""
        weaknesses = []

        # Check each dimension
        if metrics.quality_scores.overall_score() < 60:
            weaknesses.append("Low output quality or consistency issues")

        if metrics.performance_scores.performance_score < 60:
            weaknesses.append("Performance concerns with slow execution times")

        if metrics.performance_scores.has_regression:
            weaknesses.append("Performance regression detected")

        if metrics.reliability_scores.reliability_score < 80:
            weaknesses.append("Reliability issues with elevated error rate")

        if metrics.reliability_scores.error_handling_quality < 60:
            weaknesses.append("Poor error handling with unclear error messages")

        if metrics.code_quality_scores.complexity_score > 70:
            weaknesses.append("High code complexity affecting maintainability")

        if metrics.code_quality_scores.test_coverage < 50:
            weaknesses.append("Insufficient test coverage")

        if metrics.health_trend == HealthTrend.DECLINING.value:
            weaknesses.append("Declining health trend requires attention")

        return weaknesses if weaknesses else []

    def _generate_improvements(
        self,
        metrics: SkillEvaluationMetrics,
        records: List,
        stats: Dict[str, Any]
    ) -> List[ImprovementSuggestion]:
        """Generate improvement suggestions."""
        suggestions = []

        # Performance improvements
        if metrics.performance_scores.performance_score < 70:
            suggestions.append(ImprovementSuggestion(
                category=ImprovementCategory.PERFORMANCE.value,
                severity=ImprovementSeverity.HIGH.value if metrics.performance_scores.performance_score < 50 else ImprovementSeverity.MEDIUM.value,
                description="Optimize execution performance to reduce latency",
                expected_impact="Reduce average execution time by 30-50%",
                confidence=0.7,
                can_auto_apply=False
            ))

        # Regression fix
        if metrics.performance_scores.has_regression:
            suggestions.append(ImprovementSuggestion(
                category=ImprovementCategory.PERFORMANCE.value,
                severity=ImprovementSeverity.CRITICAL.value,
                description="Fix performance regression",
                expected_impact=f"Restore performance to baseline levels",
                confidence=0.9,
                can_auto_apply=False
            ))

        # Reliability improvements
        if metrics.reliability_scores.reliability_score < 80:
            # Analyze common errors
            top_errors = Counter([r.error_code for r in records if not r.success and r.error_code])
            if top_errors:
                most_common_error = top_errors.most_common(1)[0]
                suggestions.append(ImprovementSuggestion(
                    category=ImprovementCategory.RELIABILITY.value,
                    severity=ImprovementSeverity.HIGH.value,
                    description=f"Address common error: {most_common_error[0]} ({most_common_error[1]} occurrences)",
                    expected_impact="Reduce error rate by 40-60%",
                    confidence=0.8,
                    can_auto_apply=False
                ))

        # Error handling improvements
        if metrics.reliability_scores.error_handling_quality < 70:
            suggestions.append(ImprovementSuggestion(
                category=ImprovementCategory.QUALITY.value,
                severity=ImprovementSeverity.MEDIUM.value,
                description="Improve error messages to be more descriptive and actionable",
                expected_impact="Better debuggability and user experience",
                confidence=0.6,
                can_auto_apply=False
            ))

        # Code quality improvements
        if metrics.code_quality_scores.complexity_score > 70:
            suggestions.append(ImprovementSuggestion(
                category=ImprovementCategory.MAINTAINABILITY.value,
                severity=ImprovementSeverity.MEDIUM.value,
                description="Refactor complex code to improve maintainability",
                expected_impact="Reduce complexity by 30-40%, improve maintainability",
                confidence=0.7,
                can_auto_apply=False
            ))

        # Test coverage improvements
        if metrics.code_quality_scores.test_coverage < 60:
            suggestions.append(ImprovementSuggestion(
                category=ImprovementCategory.QUALITY.value,
                severity=ImprovementSeverity.MEDIUM.value,
                description="Increase test coverage to improve reliability",
                expected_impact="Catch more bugs, improve confidence in changes",
                confidence=0.8,
                can_auto_apply=False
            ))

        return suggestions

    def _identify_priority_fixes(self, metrics: SkillEvaluationMetrics) -> List[str]:
        """Identify priority fixes based on severity."""
        fixes = []

        # Critical and high severity improvements
        critical_improvements = [
            s for s in metrics.improvement_opportunities
            if s.severity in [ImprovementSeverity.CRITICAL.value, ImprovementSeverity.HIGH.value]
        ]

        for imp in critical_improvements:
            fixes.append(f"[{imp.severity.upper()}] {imp.description}")

        # Add critical weaknesses
        if metrics.overall_health_score < 50:
            fixes.insert(0, "CRITICAL: Overall health score below 50 - immediate attention required")

        if metrics.performance_scores.has_regression:
            fixes.insert(0, "CRITICAL: Performance regression detected")

        if metrics.reliability_scores.error_rate > 30:
            fixes.insert(0, "CRITICAL: Error rate exceeds 30%")

        return fixes

"""
Performance Analyzer

Advanced performance analysis with regression detection and bottleneck identification.
"""

import statistics
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict

from skills.skill_evaluator.core.models import (
    ImprovementSuggestion,
    ImprovementCategory,
    ImprovementSeverity,
    HealthTrend
)
from skills.skill_evaluator.core.history_tracker import ExecutionHistoryTracker


class PerformanceAnalyzer:
    """
    Advanced performance analysis with statistical methods.

    Detects regressions, identifies bottlenecks, and provides
    optimization recommendations.
    """

    def __init__(self, history_tracker: ExecutionHistoryTracker):
        """
        Initialize the performance analyzer.

        Args:
            history_tracker: ExecutionHistoryTracker for accessing execution data
        """
        self.history_tracker = history_tracker

    def analyze(
        self,
        skill_name: str,
        baseline_period_days: int = 7,
        regression_threshold: float = 0.3,
        operation: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Perform comprehensive performance analysis.

        Args:
            skill_name: Name of the skill to analyze
            baseline_period_days: Days for baseline period
            regression_threshold: Threshold for regression (0-1, e.g., 0.3 = 30%)
            operation: Specific operation to analyze (None for all)

        Returns:
            Dictionary containing analysis results
        """
        # Get baseline and current performance
        baseline = self.history_tracker.get_performance_baseline(
            skill_name,
            operation=operation,
            days=baseline_period_days
        )

        if not baseline or baseline['sample_size'] < 10:
            return {
                'has_data': False,
                'error': 'Insufficient baseline data for analysis',
                'recommendation': f'Need at least 10 executions in the last {baseline_period_days} days'
            }

        # Get current performance (last 24 hours)
        current_stats = self.history_tracker.get_execution_stats(
            skill_name,
            time_period_days=1
        )

        # Get recent executions for detailed analysis
        since = (datetime.now() - timedelta(days=1)).timestamp()
        recent_records = self.history_tracker.get_recent_executions(
            skill_name,
            limit=1000,
            since=since
        )

        if operation:
            recent_records = [r for r in recent_records if r.operation == operation]

        if not recent_records:
            return {
                'has_data': False,
                'error': 'No recent executions found',
                'recommendation': 'Execute the skill to generate performance data'
            }

        # Detect regression
        regression_analysis = self._detect_regression(
            baseline,
            current_stats,
            recent_records,
            regression_threshold
        )

        # Identify bottlenecks
        bottlenecks = self._identify_bottlenecks(
            recent_records,
            baseline
        )

        # Analyze performance distribution
        distribution = self._analyze_distribution(recent_records)

        # Generate optimization suggestions
        suggestions = self._generate_optimization_suggestions(
            regression_analysis,
            bottlenecks,
            distribution,
            baseline
        )

        # Calculate overall performance score
        performance_score = self._calculate_performance_score(
            current_stats,
            baseline,
            regression_analysis
        )

        return {
            'has_data': True,
            'skill_name': skill_name,
            'operation': operation,
            'performance_score': performance_score,
            'baseline_period_days': baseline_period_days,
            'baseline_metrics': baseline,
            'current_metrics': {
                'avg_duration': current_stats['avg_duration'],
                'min_duration': current_stats['min_duration'],
                'max_duration': current_stats['max_duration'],
                'success_rate': current_stats['success_rate'],
                'sample_size': current_stats['total_executions']
            },
            'regression_analysis': regression_analysis,
            'bottlenecks': bottlenecks,
            'distribution': distribution,
            'optimization_suggestions': suggestions,
            'trend': self._determine_performance_trend(regression_analysis)
        }

    def _detect_regression(
        self,
        baseline: Dict[str, Any],
        current_stats: Dict[str, Any],
        recent_records: List,
        threshold: float
    ) -> Dict[str, Any]:
        """Detect performance regression with statistical analysis."""
        # Extract durations from recent successful executions
        recent_successful = [r for r in recent_records if r.success]

        if len(recent_successful) < 5:
            return {
                'has_regression': False,
                'confidence': 0.0,
                'reason': 'Insufficient recent data for regression detection'
            }

        recent_durations = [r.duration for r in recent_successful]
        current_avg = statistics.mean(recent_durations)
        current_median = statistics.median(recent_durations)
        current_stdev = statistics.stdev(recent_durations) if len(recent_durations) > 1 else 0

        baseline_avg = baseline['avg_duration']
        baseline_median = baseline['median_duration']

        # Calculate degradation
        avg_degradation = (current_avg - baseline_avg) / baseline_avg if baseline_avg > 0 else 0
        median_degradation = (current_median - baseline_median) / baseline_median if baseline_median > 0 else 0

        # Check if regression exceeds threshold
        has_regression = avg_degradation > threshold

        # Calculate confidence based on consistency
        # Higher confidence if both avg and median show degradation
        confidence = 0.0
        if has_regression:
            if median_degradation > threshold * 0.8:
                confidence = min(1.0, 0.7 + (avg_degradation / threshold) * 0.3)
            else:
                confidence = min(1.0, 0.5 + (avg_degradation / threshold) * 0.3)

        # Determine severity
        if avg_degradation > threshold * 2:
            severity = ImprovementSeverity.CRITICAL.value
        elif avg_degradation > threshold * 1.5:
            severity = ImprovementSeverity.HIGH.value
        elif avg_degradation > threshold:
            severity = ImprovementSeverity.MEDIUM.value
        else:
            severity = ImprovementSeverity.LOW.value

        return {
            'has_regression': has_regression,
            'confidence': confidence,
            'severity': severity if has_regression else None,
            'baseline_avg': baseline_avg,
            'current_avg': current_avg,
            'baseline_median': baseline_median,
            'current_median': current_median,
            'avg_degradation_percent': avg_degradation * 100,
            'median_degradation_percent': median_degradation * 100,
            'current_stdev': current_stdev,
            'sample_size': len(recent_successful),
            'threshold_percent': threshold * 100
        }

    def _identify_bottlenecks(
        self,
        recent_records: List,
        baseline: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Identify performance bottlenecks."""
        bottlenecks = []

        successful_records = [r for r in recent_records if r.success]
        if not successful_records:
            return bottlenecks

        durations = [r.duration for r in successful_records]
        avg_duration = statistics.mean(durations)
        p95_duration = sorted(durations)[int(len(durations) * 0.95)] if len(durations) > 0 else 0
        max_duration = max(durations)

        # Bottleneck 1: High variance in execution times
        if len(durations) > 1:
            stdev = statistics.stdev(durations)
            coefficient_of_variation = stdev / avg_duration if avg_duration > 0 else 0

            if coefficient_of_variation > 0.5:  # More than 50% variation
                bottlenecks.append({
                    'type': 'high_variance',
                    'severity': 'medium',
                    'description': f'High variance in execution times (CV: {coefficient_of_variation:.2f})',
                    'impact': 'Unpredictable performance',
                    'recommendation': 'Investigate inconsistent operations or external dependencies'
                })

        # Bottleneck 2: Long tail latency
        if p95_duration > avg_duration * 2:
            bottlenecks.append({
                'type': 'long_tail_latency',
                'severity': 'high',
                'description': f'P95 latency ({p95_duration:.2f}s) significantly higher than average ({avg_duration:.2f}s)',
                'impact': 'Poor worst-case performance',
                'recommendation': 'Profile slowest executions to identify edge cases'
            })

        # Bottleneck 3: Consistently slow operations
        if avg_duration > 30:  # More than 30 seconds
            bottlenecks.append({
                'type': 'slow_execution',
                'severity': 'high',
                'description': f'Average execution time is {avg_duration:.2f}s',
                'impact': 'Poor user experience',
                'recommendation': 'Consider breaking down into smaller operations or adding caching'
            })

        # Bottleneck 4: Resource-heavy operations
        # Check if we have resource profiling data
        resource_heavy = []
        for record in successful_records[-10:]:  # Check last 10
            if record.metadata and 'performance_profile' in record.metadata:
                profile = record.metadata['performance_profile']
                if profile.get('memory_delta_mb', 0) > 100:
                    resource_heavy.append('memory')
                if profile.get('cpu_usage_percent', 0) > 80:
                    resource_heavy.append('cpu')

        if resource_heavy:
            bottlenecks.append({
                'type': 'resource_intensive',
                'severity': 'medium',
                'description': f'High resource usage detected: {", ".join(set(resource_heavy))}',
                'impact': 'May impact system performance',
                'recommendation': 'Optimize resource usage or implement resource pooling'
            })

        # Bottleneck 5: Operation-specific slowness
        operation_stats = defaultdict(list)
        for record in successful_records:
            operation_stats[record.operation].append(record.duration)

        for operation, durations in operation_stats.items():
            if len(durations) >= 5:
                op_avg = statistics.mean(durations)
                if op_avg > avg_duration * 1.5:
                    bottlenecks.append({
                        'type': 'slow_operation',
                        'severity': 'medium',
                        'description': f'Operation "{operation}" is {(op_avg / avg_duration - 1) * 100:.0f}% slower than average',
                        'impact': f'Affects {len(durations)} executions',
                        'recommendation': f'Optimize the "{operation}" operation specifically'
                    })

        return bottlenecks

    def _analyze_distribution(self, recent_records: List) -> Dict[str, Any]:
        """Analyze performance distribution."""
        successful = [r for r in recent_records if r.success]

        if not successful:
            return {'has_data': False}

        durations = sorted([r.duration for r in successful])

        return {
            'has_data': True,
            'count': len(durations),
            'min': min(durations),
            'max': max(durations),
            'mean': statistics.mean(durations),
            'median': statistics.median(durations),
            'stdev': statistics.stdev(durations) if len(durations) > 1 else 0,
            'p25': durations[int(len(durations) * 0.25)],
            'p50': durations[int(len(durations) * 0.50)],
            'p75': durations[int(len(durations) * 0.75)],
            'p90': durations[int(len(durations) * 0.90)],
            'p95': durations[int(len(durations) * 0.95)],
            'p99': durations[int(len(durations) * 0.99)] if len(durations) >= 100 else durations[-1]
        }

    def _generate_optimization_suggestions(
        self,
        regression_analysis: Dict[str, Any],
        bottlenecks: List[Dict[str, Any]],
        distribution: Dict[str, Any],
        baseline: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate optimization suggestions based on analysis."""
        suggestions = []

        # Suggestion for regression
        if regression_analysis.get('has_regression'):
            suggestions.append({
                'id': 'fix_regression',
                'category': ImprovementCategory.PERFORMANCE.value,
                'severity': regression_analysis.get('severity', ImprovementSeverity.HIGH.value),
                'description': f'Fix performance regression ({regression_analysis["avg_degradation_percent"]:.1f}% slower)',
                'expected_impact': f'Restore performance to baseline ({baseline["avg_duration"]:.2f}s)',
                'confidence': regression_analysis['confidence'],
                'priority': 'critical' if regression_analysis['confidence'] > 0.8 else 'high',
                'actions': [
                    'Profile recent changes to identify performance impact',
                    'Compare current implementation with baseline version',
                    'Check for new dependencies or external service calls',
                    'Review database queries or I/O operations'
                ]
            })

        # Suggestions for bottlenecks
        for bottleneck in bottlenecks:
            if bottleneck['type'] == 'high_variance':
                suggestions.append({
                    'id': 'reduce_variance',
                    'category': ImprovementCategory.PERFORMANCE.value,
                    'severity': ImprovementSeverity.MEDIUM.value,
                    'description': 'Reduce execution time variance for consistent performance',
                    'expected_impact': 'More predictable performance',
                    'confidence': 0.7,
                    'priority': 'medium',
                    'actions': [
                        'Identify operations with inconsistent timing',
                        'Add connection pooling for external services',
                        'Implement request coalescing for repeated operations',
                        'Add timeouts to prevent hanging operations'
                    ]
                })

            elif bottleneck['type'] == 'long_tail_latency':
                suggestions.append({
                    'id': 'optimize_p95',
                    'category': ImprovementCategory.PERFORMANCE.value,
                    'severity': ImprovementSeverity.HIGH.value,
                    'description': 'Optimize worst-case performance (P95 latency)',
                    'expected_impact': 'Better worst-case user experience',
                    'confidence': 0.8,
                    'priority': 'high',
                    'actions': [
                        'Profile the slowest 5% of executions',
                        'Identify and handle edge cases more efficiently',
                        'Add early termination for expensive operations',
                        'Implement progressive enhancement'
                    ]
                })

            elif bottleneck['type'] == 'slow_execution':
                suggestions.append({
                    'id': 'reduce_duration',
                    'category': ImprovementCategory.PERFORMANCE.value,
                    'severity': ImprovementSeverity.HIGH.value,
                    'description': 'Reduce overall execution time',
                    'expected_impact': '30-50% reduction in execution time',
                    'confidence': 0.6,
                    'priority': 'high',
                    'actions': [
                        'Break down into smaller, composable operations',
                        'Add caching for expensive computations',
                        'Parallelize independent operations',
                        'Optimize data structures and algorithms'
                    ]
                })

        # Suggestion based on distribution
        if distribution.get('has_data'):
            # If P95 is much higher than median, suggest optimization
            p95 = distribution.get('p95', 0)
            median = distribution.get('median', 0)

            if median > 0 and p95 > median * 3:
                suggestions.append({
                    'id': 'optimize_outliers',
                    'category': ImprovementCategory.PERFORMANCE.value,
                    'severity': ImprovementSeverity.MEDIUM.value,
                    'description': 'Optimize performance outliers',
                    'expected_impact': 'More consistent performance across all executions',
                    'confidence': 0.7,
                    'priority': 'medium',
                    'actions': [
                        'Add performance monitoring to identify outliers',
                        'Implement circuit breakers for failing dependencies',
                        'Add request throttling to prevent overload',
                        'Cache frequently accessed data'
                    ]
                })

        return suggestions

    def _calculate_performance_score(
        self,
        current_stats: Dict[str, Any],
        baseline: Dict[str, Any],
        regression_analysis: Dict[str, Any]
    ) -> float:
        """
        Calculate overall performance score (0-100).

        Factors:
        - Absolute performance (speed)
        - Relative to baseline
        - Success rate
        - Consistency
        """
        # Base score from absolute performance (0-100)
        avg_duration = current_stats['avg_duration']
        if avg_duration < 1:
            speed_score = 100
        elif avg_duration < 5:
            speed_score = 90 - (avg_duration - 1) * 5
        elif avg_duration < 30:
            speed_score = 70 - (avg_duration - 5) * 2
        else:
            speed_score = max(0, 30 - (avg_duration - 30) * 0.5)

        # Relative performance score (compare to baseline)
        if not regression_analysis.get('has_regression'):
            relative_score = 100
        else:
            degradation = regression_analysis['avg_degradation_percent']
            relative_score = max(0, 100 - degradation)

        # Success rate score
        success_score = current_stats['success_rate']

        # Weighted combination
        performance_score = (
            speed_score * 0.4 +
            relative_score * 0.4 +
            success_score * 0.2
        )

        return round(performance_score, 2)

    def _determine_performance_trend(
        self,
        regression_analysis: Dict[str, Any]
    ) -> str:
        """Determine performance trend."""
        if not regression_analysis.get('has_regression'):
            # Check if improving
            degradation = regression_analysis.get('avg_degradation_percent', 0)
            if degradation < -10:  # 10% improvement
                return HealthTrend.IMPROVING.value
            elif degradation < 10:  # Within 10% of baseline
                return HealthTrend.STABLE.value
            else:
                return HealthTrend.DECLINING.value
        else:
            return HealthTrend.DECLINING.value

    def compare_periods(
        self,
        skill_name: str,
        period1_days: int,
        period2_days: int,
        operation: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Compare performance between two time periods.

        Args:
            skill_name: Name of the skill
            period1_days: Recent period (e.g., last 7 days)
            period2_days: Older period (e.g., 7-14 days ago)
            operation: Specific operation to compare

        Returns:
            Comparison results
        """
        # Get stats for period 1 (recent)
        period1_stats = self.history_tracker.get_execution_stats(
            skill_name,
            time_period_days=period1_days
        )

        # Get stats for period 2 (need to calculate from older records)
        since_period2 = (datetime.now() - timedelta(days=period2_days)).timestamp()
        until_period2 = (datetime.now() - timedelta(days=period1_days)).timestamp()

        all_records = self.history_tracker.get_recent_executions(
            skill_name,
            limit=10000,
            since=since_period2
        )

        period2_records = [
            r for r in all_records
            if r.timestamp <= until_period2
        ]

        if operation:
            period2_records = [r for r in period2_records if r.operation == operation]

        if not period2_records:
            return {
                'has_data': False,
                'error': f'No data available for period 2 ({period1_days}-{period2_days} days ago)'
            }

        # Calculate period 2 stats
        period2_successful = [r for r in period2_records if r.success]
        period2_failed = [r for r in period2_records if not r.success]

        period2_avg = statistics.mean([r.duration for r in period2_successful]) if period2_successful else 0

        # Calculate changes
        duration_change = ((period1_stats['avg_duration'] - period2_avg) / period2_avg * 100) if period2_avg > 0 else 0
        error_rate_change = period1_stats['error_rate'] - (len(period2_failed) / len(period2_records) * 100 if period2_records else 0)

        return {
            'has_data': True,
            'skill_name': skill_name,
            'operation': operation,
            'period1': {
                'days': period1_days,
                'avg_duration': period1_stats['avg_duration'],
                'error_rate': period1_stats['error_rate'],
                'total_executions': period1_stats['total_executions']
            },
            'period2': {
                'days': f'{period1_days}-{period2_days}',
                'avg_duration': period2_avg,
                'error_rate': len(period2_failed) / len(period2_records) * 100 if period2_records else 0,
                'total_executions': len(period2_records)
            },
            'changes': {
                'duration_change_percent': duration_change,
                'error_rate_change_percent': error_rate_change,
                'trend': 'improving' if duration_change < -10 and error_rate_change < -5 else
                        'declining' if duration_change > 10 or error_rate_change > 5 else
                        'stable'
            }
        }

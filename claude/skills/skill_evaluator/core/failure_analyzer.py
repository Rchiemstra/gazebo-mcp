"""
Failure Pattern Analyzer

Analyzes failure patterns and error clustering for root cause identification.
"""

from typing import Dict, Any, List
from collections import Counter, defaultdict
from datetime import datetime, timedelta

from skills.skill_evaluator.core.models import ImprovementSuggestion, ImprovementCategory, ImprovementSeverity


class FailurePatternAnalyzer:
    """
    Analyzes failure patterns to identify root causes and suggest fixes.
    """

    def analyze_failures(self, failed_records: List) -> Dict[str, Any]:
        """
        Analyze failure patterns from execution records.

        Args:
            failed_records: List of failed ExecutionRecords

        Returns:
            Analysis results with patterns and suggestions
        """
        if not failed_records:
            return {
                'has_failures': False,
                'patterns': [],
                'suggestions': []
            }

        patterns = []

        # Pattern 1: Error code clustering
        error_patterns = self._analyze_error_codes(failed_records)
        patterns.extend(error_patterns)

        # Pattern 2: Temporal clustering
        temporal_patterns = self._analyze_temporal_clustering(failed_records)
        patterns.extend(temporal_patterns)

        # Pattern 3: Operation-specific failures
        operation_patterns = self._analyze_operation_failures(failed_records)
        patterns.extend(operation_patterns)

        # Generate suggestions based on patterns
        suggestions = self._generate_failure_suggestions(patterns, failed_records)

        return {
            'has_failures': True,
            'total_failures': len(failed_records),
            'patterns': patterns,
            'pattern_count': len(patterns),
            'suggestions': suggestions
        }

    def _analyze_error_codes(self, failed_records: List) -> List[Dict[str, Any]]:
        """Analyze error code patterns."""
        patterns = []

        # Count error codes
        error_counter = Counter(r.error_code for r in failed_records if r.error_code)

        for error_code, count in error_counter.most_common(5):
            percentage = (count / len(failed_records)) * 100

            # Get sample error messages
            samples = [
                r.error for r in failed_records
                if r.error_code == error_code and r.error
            ][:3]

            patterns.append({
                'type': 'error_code_clustering',
                'error_code': error_code,
                'occurrences': count,
                'percentage': percentage,
                'severity': 'high' if percentage > 50 else 'medium' if percentage > 25 else 'low',
                'sample_messages': samples,
                'description': f"Error {error_code} accounts for {percentage:.1f}% of failures ({count} occurrences)"
            })

        return patterns

    def _analyze_temporal_clustering(self, failed_records: List) -> List[Dict[str, Any]]:
        """Analyze temporal clustering of failures."""
        patterns = []

        if len(failed_records) < 3:
            return patterns

        # Sort by timestamp
        sorted_records = sorted(failed_records, key=lambda r: r.timestamp)

        # Calculate time gaps between failures
        time_gaps = []
        for i in range(len(sorted_records) - 1):
            gap = sorted_records[i + 1].timestamp - sorted_records[i].timestamp
            time_gaps.append(gap)

        if not time_gaps:
            return patterns

        # Check for clustering (median gap < 1 hour)
        import statistics
        median_gap = statistics.median(time_gaps)

        if median_gap < 3600:  # 1 hour
            patterns.append({
                'type': 'temporal_clustering',
                'median_gap_seconds': median_gap,
                'median_gap_minutes': median_gap / 60,
                'severity': 'high',
                'description': f'Failures occur in temporal clusters (median gap: {median_gap/60:.1f} minutes)',
                'implication': 'Suggests cascading failures or dependency issues'
            })

        return patterns

    def _analyze_operation_failures(self, failed_records: List) -> List[Dict[str, Any]]:
        """Analyze operation-specific failure patterns."""
        patterns = []

        # Group by operation
        operation_failures = defaultdict(list)
        for record in failed_records:
            operation_failures[record.operation].append(record)

        # Find operations with high failure rates
        for operation, records in operation_failures.items():
            if len(records) >= 3:  # At least 3 failures
                percentage = (len(records) / len(failed_records)) * 100

                patterns.append({
                    'type': 'operation_specific',
                    'operation': operation,
                    'failure_count': len(records),
                    'percentage': percentage,
                    'severity': 'high' if percentage > 50 else 'medium',
                    'description': f"Operation '{operation}' has {len(records)} failures ({percentage:.1f}% of all failures)"
                })

        return patterns

    def _generate_failure_suggestions(
        self,
        patterns: List[Dict[str, Any]],
        failed_records: List
    ) -> List[ImprovementSuggestion]:
        """Generate improvement suggestions based on failure patterns."""
        suggestions = []

        for pattern in patterns:
            if pattern['type'] == 'error_code_clustering':
                if pattern['percentage'] > 50:
                    suggestions.append(ImprovementSuggestion(
                        category=ImprovementCategory.RELIABILITY.value,
                        severity=ImprovementSeverity.CRITICAL.value,
                        description=f"Fix recurring error: {pattern['error_code']} ({pattern['occurrences']} occurrences)",
                        expected_impact=f"Eliminate {pattern['percentage']:.0f}% of failures",
                        confidence=0.90,
                        can_auto_apply=False,
                        metadata={'error_code': pattern['error_code'], 'samples': pattern['sample_messages']}
                    ))

            elif pattern['type'] == 'temporal_clustering':
                suggestions.append(ImprovementSuggestion(
                    category=ImprovementCategory.RELIABILITY.value,
                    severity=ImprovementSeverity.HIGH.value,
                    description="Investigate cascading failures and add circuit breakers",
                    expected_impact="Prevent failure cascades and improve system stability",
                    confidence=0.75,
                    can_auto_apply=False,
                    metadata={'pattern': 'temporal_clustering', 'median_gap_minutes': pattern['median_gap_minutes']}
                ))

            elif pattern['type'] == 'operation_specific':
                suggestions.append(ImprovementSuggestion(
                    category=ImprovementCategory.RELIABILITY.value,
                    severity=ImprovementSeverity.HIGH.value,
                    description=f"Fix reliability issues in '{pattern['operation']}' operation",
                    expected_impact=f"Reduce overall failures by {pattern['percentage']:.0f}%",
                    confidence=0.85,
                    can_auto_apply=False,
                    metadata={'operation': pattern['operation'], 'failure_count': pattern['failure_count']}
                ))

        return suggestions

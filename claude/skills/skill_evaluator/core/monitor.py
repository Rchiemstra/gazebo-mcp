"""
Execution Monitor

Monitors skill executions and provides pre/post execution analysis.
"""

import time
import psutil
import os
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from skills.skill_evaluator.core.models import (
    ExecutionContext,
    ExecutionRecord,
    HealthTrend
)
from skills.skill_evaluator.core.history_tracker import ExecutionHistoryTracker


class ExecutionMonitor:
    """
    Monitors skill executions with pre/post execution checks.

    Collects metrics, detects anomalies, and provides recommendations.
    """

    def __init__(self, history_tracker: ExecutionHistoryTracker):
        """
        Initialize the execution monitor.

        Args:
            history_tracker: ExecutionHistoryTracker instance for accessing history
        """
        self.history_tracker = history_tracker
        self._active_executions: Dict[str, Dict[str, Any]] = {}

    def pre_execution_check(
        self,
        skill_name: str,
        operation: str,
        parameters: Dict[str, Any]
    ) -> ExecutionContext:
        """
        Perform pre-execution checks and setup monitoring.

        Args:
            skill_name: Name of the skill
            operation: Operation to execute
            parameters: Operation parameters

        Returns:
            ExecutionContext with monitoring setup
        """
        context = ExecutionContext(
            skill_name=skill_name,
            operation=operation,
            parameters=parameters
        )

        # Store initial resource state
        process = psutil.Process(os.getpid())
        self._active_executions[context.execution_id] = {
            'context': context,
            'start_time': time.time(),
            'start_cpu_percent': process.cpu_percent(),
            'start_memory_mb': process.memory_info().rss / 1024 / 1024,
            'start_io_counters': process.io_counters() if hasattr(process, 'io_counters') else None
        }

        return context

    def post_execution_analysis(
        self,
        execution_id: str,
        success: bool,
        result_data: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
        error_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Perform post-execution analysis.

        Args:
            execution_id: Execution ID from pre_execution_check
            success: Whether execution was successful
            result_data: Result data from execution
            error: Error message if failed
            error_code: Error code if failed

        Returns:
            Analysis results including warnings and recommendations
        """
        if execution_id not in self._active_executions:
            return {
                'warnings': ['Execution context not found'],
                'recommendations': [],
                'performance_profile': None
            }

        exec_data = self._active_executions.pop(execution_id)
        context = exec_data['context']
        duration = time.time() - exec_data['start_time']

        # Collect final resource state
        process = psutil.Process(os.getpid())
        end_cpu_percent = process.cpu_percent()
        end_memory_mb = process.memory_info().rss / 1024 / 1024
        end_io_counters = process.io_counters() if hasattr(process, 'io_counters') else None

        # Calculate resource usage
        cpu_usage = end_cpu_percent - exec_data['start_cpu_percent']
        memory_delta = end_memory_mb - exec_data['start_memory_mb']

        performance_profile = {
            'duration': duration,
            'cpu_usage_percent': max(0, cpu_usage),  # Can be negative due to sampling
            'memory_delta_mb': memory_delta,
            'memory_end_mb': end_memory_mb
        }

        # Add I/O if available
        if exec_data['start_io_counters'] and end_io_counters:
            io_read_delta = end_io_counters.read_bytes - exec_data['start_io_counters'].read_bytes
            io_write_delta = end_io_counters.write_bytes - exec_data['start_io_counters'].write_bytes
            performance_profile['io_read_mb'] = io_read_delta / 1024 / 1024
            performance_profile['io_write_mb'] = io_write_delta / 1024 / 1024

        # Create execution record
        record = ExecutionRecord(
            execution_id=execution_id,
            skill_name=context.skill_name,
            operation=context.operation,
            parameters=context.parameters,
            success=success,
            duration=duration,
            timestamp=exec_data['start_time'],
            error=error,
            error_code=error_code,
            result_data=result_data,
            metadata={'performance_profile': performance_profile}
        )

        # Save to history
        self.history_tracker.record_execution(record)

        # Generate warnings and recommendations
        warnings = []
        recommendations = []

        # Get historical baseline for comparison
        baseline = self.history_tracker.get_performance_baseline(
            context.skill_name,
            operation=context.operation,
            days=7
        )

        if baseline:
            # Check for performance degradation
            if duration > baseline['p95_duration'] * 1.5:
                warnings.append(
                    f"Performance degradation detected: {duration:.2f}s vs "
                    f"baseline P95 {baseline['p95_duration']:.2f}s"
                )
                recommendations.append(
                    "Consider profiling this operation to identify bottlenecks"
                )

            # Check for increased error rate
            stats = self.history_tracker.get_execution_stats(
                context.skill_name,
                time_period_days=1
            )
            if stats['error_rate'] > 15.0:
                warnings.append(
                    f"Elevated error rate: {stats['error_rate']:.1f}% in last 24h"
                )
                recommendations.append(
                    "Investigate recent failures to identify common patterns"
                )

        # Check for resource anomalies
        if memory_delta > 100:  # More than 100MB increase
            warnings.append(
                f"High memory usage: +{memory_delta:.1f}MB during execution"
            )
            recommendations.append(
                "Check for memory leaks or inefficient data structures"
            )

        if duration > 60:  # More than 1 minute
            warnings.append(
                f"Long execution time: {duration:.1f}s"
            )
            recommendations.append(
                "Consider breaking down the operation or adding progress indicators"
            )

        # Check for failure patterns
        if not success:
            recent_failures = self.history_tracker.get_failed_executions(
                context.skill_name,
                limit=10,
                error_code=error_code
            )
            if len(recent_failures) >= 3:
                warnings.append(
                    f"Repeated failures with error code: {error_code} "
                    f"({len(recent_failures)} in recent history)"
                )
                recommendations.append(
                    "This error pattern requires investigation and fixing"
                )

        return {
            'execution_id': execution_id,
            'warnings': warnings,
            'recommendations': recommendations,
            'performance_profile': performance_profile,
            'baseline_comparison': baseline,
            'record': record
        }

    def get_monitoring_summary(
        self,
        skill_name: str,
        time_period_days: int = 7
    ) -> Dict[str, Any]:
        """
        Get a monitoring summary for a skill.

        Args:
            skill_name: Name of the skill
            time_period_days: Time period to analyze

        Returns:
            Monitoring summary with key metrics and trends
        """
        stats = self.history_tracker.get_execution_stats(
            skill_name,
            time_period_days=time_period_days
        )

        if stats['total_executions'] == 0:
            return {
                'skill_name': skill_name,
                'status': 'no_data',
                'message': 'No execution data available'
            }

        # Determine health status
        health_status = 'healthy'
        if stats['error_rate'] > 20:
            health_status = 'critical'
        elif stats['error_rate'] > 10:
            health_status = 'warning'

        # Get trend
        trend = self._calculate_trend(skill_name, time_period_days)

        # Get top errors
        top_errors = sorted(
            stats['errors_by_code'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        return {
            'skill_name': skill_name,
            'health_status': health_status,
            'trend': trend,
            'time_period_days': time_period_days,
            'total_executions': stats['total_executions'],
            'success_rate': stats['success_rate'],
            'error_rate': stats['error_rate'],
            'avg_duration': stats['avg_duration'],
            'top_errors': [
                {'error_code': code, 'count': count}
                for code, count in top_errors
            ],
            'operations': stats['operations_breakdown'],
            'last_execution': datetime.fromtimestamp(
                stats['last_execution']
            ).isoformat() if stats.get('last_execution') else None
        }

    def check_quality_gates(
        self,
        skill_name: str,
        thresholds: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Check if skill meets quality gate thresholds.

        Args:
            skill_name: Name of the skill
            thresholds: Custom thresholds (uses defaults if None)

        Returns:
            Quality gate check results
        """
        # Default thresholds
        if thresholds is None:
            thresholds = {
                'max_error_rate': 20.0,  # Max 20% error rate
                'min_success_rate': 80.0,  # Min 80% success rate
                'max_avg_duration': 30.0,  # Max 30s average duration
                'max_p95_duration': 60.0   # Max 60s P95 duration
            }

        stats = self.history_tracker.get_execution_stats(skill_name, time_period_days=1)
        baseline = self.history_tracker.get_performance_baseline(skill_name, days=1)

        gates = {}
        passed = True

        # Check error rate
        if stats['error_rate'] > thresholds['max_error_rate']:
            gates['error_rate'] = {
                'passed': False,
                'value': stats['error_rate'],
                'threshold': thresholds['max_error_rate'],
                'message': f"Error rate {stats['error_rate']:.1f}% exceeds threshold {thresholds['max_error_rate']:.1f}%"
            }
            passed = False
        else:
            gates['error_rate'] = {
                'passed': True,
                'value': stats['error_rate'],
                'threshold': thresholds['max_error_rate']
            }

        # Check success rate
        if stats['success_rate'] < thresholds['min_success_rate']:
            gates['success_rate'] = {
                'passed': False,
                'value': stats['success_rate'],
                'threshold': thresholds['min_success_rate'],
                'message': f"Success rate {stats['success_rate']:.1f}% below threshold {thresholds['min_success_rate']:.1f}%"
            }
            passed = False
        else:
            gates['success_rate'] = {
                'passed': True,
                'value': stats['success_rate'],
                'threshold': thresholds['min_success_rate']
            }

        # Check average duration
        if stats['avg_duration'] > thresholds['max_avg_duration']:
            gates['avg_duration'] = {
                'passed': False,
                'value': stats['avg_duration'],
                'threshold': thresholds['max_avg_duration'],
                'message': f"Average duration {stats['avg_duration']:.2f}s exceeds threshold {thresholds['max_avg_duration']:.2f}s"
            }
            passed = False
        else:
            gates['avg_duration'] = {
                'passed': True,
                'value': stats['avg_duration'],
                'threshold': thresholds['max_avg_duration']
            }

        # Check P95 duration if baseline available
        if baseline and baseline['p95_duration'] > thresholds['max_p95_duration']:
            gates['p95_duration'] = {
                'passed': False,
                'value': baseline['p95_duration'],
                'threshold': thresholds['max_p95_duration'],
                'message': f"P95 duration {baseline['p95_duration']:.2f}s exceeds threshold {thresholds['max_p95_duration']:.2f}s"
            }
            passed = False
        elif baseline:
            gates['p95_duration'] = {
                'passed': True,
                'value': baseline['p95_duration'],
                'threshold': thresholds['max_p95_duration']
            }

        return {
            'skill_name': skill_name,
            'overall_passed': passed,
            'gates': gates,
            'timestamp': time.time()
        }

    def _calculate_trend(
        self,
        skill_name: str,
        time_period_days: int
    ) -> str:
        """Calculate health trend for a skill."""
        try:
            # Get stats for current period and previous period
            current_stats = self.history_tracker.get_execution_stats(
                skill_name,
                time_period_days=time_period_days
            )

            previous_stats = self.history_tracker.get_execution_stats(
                skill_name,
                time_period_days=time_period_days * 2
            )

            if current_stats['total_executions'] < 10:
                return HealthTrend.UNKNOWN.value

            # Compare error rates
            current_error_rate = current_stats['error_rate']
            previous_error_rate = previous_stats['error_rate']

            # Compare performance
            current_duration = current_stats['avg_duration']
            previous_duration = previous_stats['avg_duration']

            # Calculate trend
            error_rate_delta = current_error_rate - previous_error_rate
            duration_delta_percent = (
                (current_duration - previous_duration) / previous_duration * 100
                if previous_duration > 0 else 0
            )

            # Improving if error rate decreased and performance improved
            if error_rate_delta < -5 or duration_delta_percent < -20:
                return HealthTrend.IMPROVING.value
            # Declining if error rate increased or performance degraded
            elif error_rate_delta > 5 or duration_delta_percent > 30:
                return HealthTrend.DECLINING.value
            else:
                return HealthTrend.STABLE.value

        except Exception:
            return HealthTrend.UNKNOWN.value

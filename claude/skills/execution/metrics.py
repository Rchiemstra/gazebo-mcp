"""
Efficiency metrics for code execution pattern.

Tracks token savings and performance gains from MCP code execution.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class EfficiencyMetrics:
    """Track token savings from a single code execution."""
    operation: str
    tokens_without_filtering: int
    tokens_with_filtering: int
    savings_percent: float
    duration: float
    timestamp: datetime = field(default_factory=datetime.now)


class EfficiencyTracker:
    """
    Track efficiency gains from code execution pattern.

    Example:
        tracker = EfficiencyTracker()

        # Record execution
        tracker.record_execution(
            operation="code_analysis",
            full_result_size=50_000,  # tokens if unfiltered
            filtered_result_size=500,  # tokens after filtering
            duration=2.3
        )

        # Get summary
        summary = tracker.get_summary()
        print(f"Average savings: {summary['average_savings_percent']}%")
    """

    def __init__(self):
        self.metrics: List[EfficiencyMetrics] = []

    def record_execution(
        self,
        operation: str,
        full_result_size: int,
        filtered_result_size: int,
        duration: float
    ):
        """
        Record an execution with filtering.

        Args:
            operation: Name of operation
            full_result_size: Token count without filtering
            filtered_result_size: Token count with filtering
            duration: Execution duration in seconds
        """
        tokens_saved = full_result_size - filtered_result_size
        savings_percent = (tokens_saved / full_result_size * 100) if full_result_size > 0 else 0

        self.metrics.append(EfficiencyMetrics(
            operation=operation,
            tokens_without_filtering=full_result_size,
            tokens_with_filtering=filtered_result_size,
            savings_percent=savings_percent,
            duration=duration
        ))

    def get_summary(self) -> Dict[str, Any]:
        """
        Get efficiency summary across all operations.

        Returns:
            Summary dict with aggregated metrics
        """
        if not self.metrics:
            return {
                "total_operations": 0,
                "tokens_without_filtering": 0,
                "tokens_with_filtering": 0,
                "total_tokens_saved": 0,
                "average_savings_percent": 0,
                "total_duration": 0
            }

        total_without = sum(m.tokens_without_filtering for m in self.metrics)
        total_with = sum(m.tokens_with_filtering for m in self.metrics)
        total_saved = total_without - total_with
        avg_savings = (total_saved / total_without * 100) if total_without > 0 else 0

        return {
            "total_operations": len(self.metrics),
            "tokens_without_filtering": total_without,
            "tokens_with_filtering": total_with,
            "total_tokens_saved": total_saved,
            "average_savings_percent": round(avg_savings, 2),
            "total_duration": sum(m.duration for m in self.metrics),
            "operations": [
                {
                    "operation": m.operation,
                    "savings": f"{m.savings_percent:.1f}%",
                    "tokens_saved": m.tokens_without_filtering - m.tokens_with_filtering
                }
                for m in self.metrics
            ]
        }

    def get_operation_stats(self, operation: str) -> Optional[Dict[str, Any]]:
        """
        Get stats for a specific operation.

        Args:
            operation: Operation name

        Returns:
            Stats dict or None if operation not found
        """
        op_metrics = [m for m in self.metrics if m.operation == operation]

        if not op_metrics:
            return None

        total_without = sum(m.tokens_without_filtering for m in op_metrics)
        total_with = sum(m.tokens_with_filtering for m in op_metrics)
        avg_savings = ((total_without - total_with) / total_without * 100) if total_without > 0 else 0

        return {
            "operation": operation,
            "executions": len(op_metrics),
            "total_tokens_without_filtering": total_without,
            "total_tokens_with_filtering": total_with,
            "total_tokens_saved": total_without - total_with,
            "average_savings_percent": round(avg_savings, 2),
            "average_duration": sum(m.duration for m in op_metrics) / len(op_metrics)
        }

    def clear(self):
        """Clear all metrics."""
        self.metrics.clear()

    def export_csv(self, filepath: str):
        """
        Export metrics to CSV file.

        Args:
            filepath: Path to CSV file
        """
        import csv

        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                "Operation",
                "Tokens Without Filtering",
                "Tokens With Filtering",
                "Tokens Saved",
                "Savings %",
                "Duration (s)",
                "Timestamp"
            ])

            for m in self.metrics:
                writer.writerow([
                    m.operation,
                    m.tokens_without_filtering,
                    m.tokens_with_filtering,
                    m.tokens_without_filtering - m.tokens_with_filtering,
                    f"{m.savings_percent:.2f}",
                    f"{m.duration:.3f}",
                    m.timestamp.isoformat()
                ])


# Global tracker instance
_global_tracker = EfficiencyTracker()


def get_global_tracker() -> EfficiencyTracker:
    """Get the global efficiency tracker instance."""
    return _global_tracker


def record_efficiency(
    operation: str,
    full_result_size: int,
    filtered_result_size: int,
    duration: float
):
    """
    Convenience function to record to global tracker.

    Args:
        operation: Name of operation
        full_result_size: Token count without filtering
        filtered_result_size: Token count with filtering
        duration: Execution duration in seconds
    """
    _global_tracker.record_execution(
        operation,
        full_result_size,
        filtered_result_size,
        duration
    )


def get_efficiency_summary() -> Dict[str, Any]:
    """Get summary from global tracker."""
    return _global_tracker.get_summary()

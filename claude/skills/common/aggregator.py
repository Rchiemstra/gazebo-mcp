"""
Result Aggregator Module

Provides utilities for aggregating results from parallel operations
with token-efficient summarization and error collection.

Part of Phase 1: Foundation (Parallel Execution Plan)
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from collections import defaultdict
import time


@dataclass
class OperationResult:
    """
    Standardized result from a skill operation.

    This is the common result type used across all skills for consistency.
    """
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    duration: float = 0.0
    metadata: Optional[Dict[str, Any]] = None


class ResultAggregator:
    """
    Aggregate results from parallel operations with token-efficient summarization.

    Features:
    - Collect results from multiple parallel tasks
    - Track success/failure counts
    - Aggregate errors by type
    - Calculate timing statistics
    - Generate token-efficient summaries

    Token Optimization:
    - Aggregates data locally (no LLM calls)
    - Provides summary vs detailed output modes
    - Filters and groups data efficiently

    Example:
        aggregator = ResultAggregator()

        # Add results as they complete
        for result in parallel_results:
            aggregator.add_result(f"task_{i}", result)

        # Get summary (token-efficient)
        summary = aggregator.get_summary()

        # Or get full operation result
        op_result = aggregator.to_operation_result()
    """

    def __init__(self):
        """Initialize result aggregator."""
        self.results: Dict[str, Any] = {}
        self.errors: Dict[str, str] = {}
        self.success_count = 0
        self.failure_count = 0
        self.total_duration = 0.0
        self.start_time = time.time()
        self.errors_by_type: Dict[str, List[str]] = defaultdict(list)

    def add_result(
        self,
        task_name: str,
        result: Any,
        duration: Optional[float] = None
    ) -> None:
        """
        Add a result from a parallel task.

        Args:
            task_name: Identifier for the task
            result: Result value (can be OperationResult or any value)
            duration: Task duration in seconds (optional)
        """
        # Handle OperationResult objects
        if isinstance(result, OperationResult):
            if result.success:
                self.results[task_name] = result.data
                self.success_count += 1
            else:
                self.errors[task_name] = result.error
                self.failure_count += 1
                if result.error_code:
                    self.errors_by_type[result.error_code].append(task_name)

            if result.duration:
                self.total_duration += result.duration
        else:
            # Handle raw results
            self.results[task_name] = result
            self.success_count += 1

        if duration:
            self.total_duration += duration

    def add_error(
        self,
        task_name: str,
        error: str,
        error_type: Optional[str] = None
    ) -> None:
        """
        Add an error from a failed task.

        Args:
            task_name: Identifier for the task
            error: Error message
            error_type: Optional error classification
        """
        self.errors[task_name] = error
        self.failure_count += 1

        if error_type:
            self.errors_by_type[error_type].append(task_name)

    def get_summary(self) -> Dict[str, Any]:
        """
        Get a token-efficient summary of results.

        This provides high-level statistics without including
        all result data, saving tokens when only counts are needed.

        Returns:
            Summary dictionary with counts and statistics
        """
        elapsed_time = time.time() - self.start_time

        summary = {
            "total_tasks": self.success_count + self.failure_count,
            "successful": self.success_count,
            "failed": self.failure_count,
            "success_rate": self._calculate_success_rate(),
            "total_duration": round(self.total_duration, 2),
            "wall_clock_time": round(elapsed_time, 2),
            "speedup": round(self.total_duration / elapsed_time, 2) if elapsed_time > 0 else 0,
        }

        # Add error summary if there are errors
        if self.errors:
            summary["errors"] = {
                "count": len(self.errors),
                "by_type": {
                    error_type: len(tasks)
                    for error_type, tasks in self.errors_by_type.items()
                },
                "failed_tasks": list(self.errors.keys())
            }

        return summary

    def get_detailed_results(self) -> Dict[str, Any]:
        """
        Get detailed results including all task data.

        Use this when you need the actual result data, not just statistics.
        Note: This can consume more tokens than get_summary().

        Returns:
            Detailed results dictionary
        """
        return {
            "summary": self.get_summary(),
            "results": self.results,
            "errors": self.errors,
            "errors_by_type": dict(self.errors_by_type)
        }

    def to_operation_result(
        self,
        response_format: str = "summary",
        metadata: Optional[Dict[str, Any]] = None
    ) -> OperationResult:
        """
        Convert aggregated results to OperationResult.

        Args:
            response_format: "summary" or "detailed"
            metadata: Optional metadata to include

        Returns:
            OperationResult with aggregated data
        """
        success = self.failure_count == 0

        if response_format == "summary":
            data = self.get_summary()
        else:
            data = self.get_detailed_results()

        error_msg = None
        if not success:
            error_msg = f"{self.failure_count} of {self.success_count + self.failure_count} tasks failed"

        return OperationResult(
            success=success,
            data=data,
            error=error_msg,
            error_code="PARTIAL_FAILURE" if self.failure_count > 0 else None,
            duration=time.time() - self.start_time,
            metadata=metadata
        )

    def _calculate_success_rate(self) -> float:
        """Calculate success rate as a percentage."""
        total = self.success_count + self.failure_count
        if total == 0:
            return 0.0
        return round((self.success_count / total) * 100, 1)

    def get_failed_tasks(self) -> List[str]:
        """Get list of failed task names."""
        return list(self.errors.keys())

    def get_successful_tasks(self) -> List[str]:
        """Get list of successful task names."""
        return list(self.results.keys())

    def has_failures(self) -> bool:
        """Check if any tasks failed."""
        return self.failure_count > 0

    def get_errors_by_type(self, error_type: str) -> List[str]:
        """Get list of tasks that failed with a specific error type."""
        return self.errors_by_type.get(error_type, [])


def merge_aggregators(aggregators: List[ResultAggregator]) -> ResultAggregator:
    """
    Merge multiple ResultAggregator instances into one.

    Useful when you have nested parallel operations and want to
    combine results into a single summary.

    Args:
        aggregators: List of ResultAggregator instances to merge

    Returns:
        New ResultAggregator with combined results
    """
    merged = ResultAggregator()

    for agg in aggregators:
        # Merge results
        merged.results.update(agg.results)
        merged.errors.update(agg.errors)

        # Update counts
        merged.success_count += agg.success_count
        merged.failure_count += agg.failure_count
        merged.total_duration += agg.total_duration

        # Merge errors by type
        for error_type, tasks in agg.errors_by_type.items():
            merged.errors_by_type[error_type].extend(tasks)

    # Use earliest start time
    merged.start_time = min(agg.start_time for agg in aggregators)

    return merged


def aggregate_operation_results(
    results: List[OperationResult],
    response_format: str = "summary"
) -> OperationResult:
    """
    Aggregate multiple OperationResult objects into one.

    This is a convenience function for quickly aggregating
    results from parallel operations.

    Args:
        results: List of OperationResult objects
        response_format: "summary" or "detailed"

    Returns:
        Single OperationResult with aggregated data
    """
    aggregator = ResultAggregator()

    for i, result in enumerate(results):
        aggregator.add_result(f"task_{i}", result)

    return aggregator.to_operation_result(response_format=response_format)

"""
Tests for Result Aggregator

Tests the result aggregation infrastructure for parallel operations.
"""

import pytest
import time
from skills.common.aggregator import (
    ResultAggregator,
    OperationResult,
    merge_aggregators,
    aggregate_operation_results
)


class TestResultAggregator:
    """Test cases for ResultAggregator."""

    def test_basic_aggregation(self):
        """Test basic result aggregation."""
        aggregator = ResultAggregator()

        # Add some successful results
        aggregator.add_result("task1", {"data": "result1"})
        aggregator.add_result("task2", {"data": "result2"})
        aggregator.add_result("task3", {"data": "result3"})

        assert aggregator.success_count == 3
        assert aggregator.failure_count == 0
        assert len(aggregator.results) == 3

    def test_aggregation_with_errors(self):
        """Test aggregation with some failures."""
        aggregator = ResultAggregator()

        # Add mix of successes and failures
        aggregator.add_result("task1", {"data": "result1"})
        aggregator.add_error("task2", "Task failed", "ValueError")
        aggregator.add_result("task3", {"data": "result3"})
        aggregator.add_error("task4", "Another failure", "RuntimeError")

        assert aggregator.success_count == 2
        assert aggregator.failure_count == 2
        assert len(aggregator.errors) == 2
        assert aggregator.has_failures()

    def test_operation_result_aggregation(self):
        """Test aggregating OperationResult objects."""
        aggregator = ResultAggregator()

        # Create operation results
        op1 = OperationResult(success=True, data={"value": 1}, duration=0.1)
        op2 = OperationResult(success=True, data={"value": 2}, duration=0.2)
        op3 = OperationResult(
            success=False,
            error="Failed",
            error_code="ERROR_CODE",
            duration=0.3
        )

        # Add them
        aggregator.add_result("op1", op1)
        aggregator.add_result("op2", op2)
        aggregator.add_result("op3", op3)

        assert aggregator.success_count == 2
        assert aggregator.failure_count == 1
        assert aggregator.total_duration == pytest.approx(0.6, rel=0.01)

    def test_get_summary(self):
        """Test getting token-efficient summary."""
        aggregator = ResultAggregator()

        aggregator.add_result("task1", {"data": "result1"})
        aggregator.add_result("task2", {"data": "result2"})
        aggregator.add_error("task3", "Failed", "ValueError")

        summary = aggregator.get_summary()

        assert summary["total_tasks"] == 3
        assert summary["successful"] == 2
        assert summary["failed"] == 1
        assert summary["success_rate"] == pytest.approx(66.7, rel=0.1)
        assert "errors" in summary
        assert summary["errors"]["count"] == 1
        assert "ValueError" in summary["errors"]["by_type"]

    def test_get_detailed_results(self):
        """Test getting detailed results."""
        aggregator = ResultAggregator()

        aggregator.add_result("task1", {"data": "result1"})
        aggregator.add_result("task2", {"data": "result2"})
        aggregator.add_error("task3", "Failed", "ValueError")

        detailed = aggregator.get_detailed_results()

        assert "summary" in detailed
        assert "results" in detailed
        assert "errors" in detailed
        assert "errors_by_type" in detailed
        assert len(detailed["results"]) == 2
        assert len(detailed["errors"]) == 1

    def test_to_operation_result_summary(self):
        """Test converting to OperationResult with summary format."""
        aggregator = ResultAggregator()

        aggregator.add_result("task1", {"data": "result1"})
        aggregator.add_result("task2", {"data": "result2"})

        op_result = aggregator.to_operation_result(response_format="summary")

        assert op_result.success is True
        assert "total_tasks" in op_result.data
        assert op_result.data["successful"] == 2
        assert op_result.error is None

    def test_to_operation_result_detailed(self):
        """Test converting to OperationResult with detailed format."""
        aggregator = ResultAggregator()

        aggregator.add_result("task1", {"data": "result1"})
        aggregator.add_error("task2", "Failed")

        op_result = aggregator.to_operation_result(response_format="detailed")

        assert op_result.success is False  # Has failures
        assert "summary" in op_result.data
        assert "results" in op_result.data
        assert "errors" in op_result.data
        assert op_result.error is not None
        assert "1 of 2 tasks failed" in op_result.error

    def test_errors_by_type_tracking(self):
        """Test error tracking by type."""
        aggregator = ResultAggregator()

        aggregator.add_error("task1", "Error 1", "ValueError")
        aggregator.add_error("task2", "Error 2", "ValueError")
        aggregator.add_error("task3", "Error 3", "RuntimeError")

        # Get errors of specific type
        value_errors = aggregator.get_errors_by_type("ValueError")
        runtime_errors = aggregator.get_errors_by_type("RuntimeError")

        assert len(value_errors) == 2
        assert len(runtime_errors) == 1
        assert "task1" in value_errors
        assert "task2" in value_errors
        assert "task3" in runtime_errors

    def test_success_rate_calculation(self):
        """Test success rate calculation."""
        aggregator = ResultAggregator()

        # 0% success
        aggregator.add_error("task1", "Failed")
        aggregator.add_error("task2", "Failed")
        assert aggregator._calculate_success_rate() == 0.0

        # Reset
        aggregator = ResultAggregator()

        # 100% success
        aggregator.add_result("task1", "result")
        aggregator.add_result("task2", "result")
        assert aggregator._calculate_success_rate() == 100.0

        # 50% success
        aggregator.add_error("task3", "Failed")
        aggregator.add_error("task4", "Failed")
        assert aggregator._calculate_success_rate() == 50.0

    def test_failed_and_successful_task_lists(self):
        """Test getting lists of failed and successful tasks."""
        aggregator = ResultAggregator()

        aggregator.add_result("task1", "result1")
        aggregator.add_result("task2", "result2")
        aggregator.add_error("task3", "Failed")
        aggregator.add_result("task4", "result4")
        aggregator.add_error("task5", "Failed")

        successful = aggregator.get_successful_tasks()
        failed = aggregator.get_failed_tasks()

        assert len(successful) == 3
        assert len(failed) == 2
        assert "task1" in successful
        assert "task2" in successful
        assert "task4" in successful
        assert "task3" in failed
        assert "task5" in failed


class TestMergeAggregators:
    """Test cases for merging multiple aggregators."""

    def test_merge_two_aggregators(self):
        """Test merging two aggregators."""
        agg1 = ResultAggregator()
        agg1.add_result("task1", "result1")
        agg1.add_result("task2", "result2")

        agg2 = ResultAggregator()
        agg2.add_result("task3", "result3")
        agg2.add_error("task4", "Failed", "ValueError")

        merged = merge_aggregators([agg1, agg2])

        assert merged.success_count == 3
        assert merged.failure_count == 1
        assert len(merged.results) == 3
        assert len(merged.errors) == 1

    def test_merge_preserves_error_types(self):
        """Test that merging preserves error type tracking."""
        agg1 = ResultAggregator()
        agg1.add_error("task1", "Error 1", "ValueError")

        agg2 = ResultAggregator()
        agg2.add_error("task2", "Error 2", "ValueError")
        agg2.add_error("task3", "Error 3", "RuntimeError")

        merged = merge_aggregators([agg1, agg2])

        value_errors = merged.get_errors_by_type("ValueError")
        runtime_errors = merged.get_errors_by_type("RuntimeError")

        assert len(value_errors) == 2
        assert len(runtime_errors) == 1

    def test_merge_empty_aggregators(self):
        """Test merging empty aggregators."""
        agg1 = ResultAggregator()
        agg2 = ResultAggregator()

        merged = merge_aggregators([agg1, agg2])

        assert merged.success_count == 0
        assert merged.failure_count == 0
        assert len(merged.results) == 0
        assert len(merged.errors) == 0


class TestAggregateOperationResults:
    """Test convenience function for aggregating OperationResults."""

    def test_aggregate_operation_results(self):
        """Test aggregating multiple OperationResult objects."""
        results = [
            OperationResult(success=True, data={"value": 1}),
            OperationResult(success=True, data={"value": 2}),
            OperationResult(success=False, error="Failed"),
        ]

        aggregated = aggregate_operation_results(results, response_format="summary")

        assert aggregated.success is False  # Has failures
        assert aggregated.data["successful"] == 2
        assert aggregated.data["failed"] == 1

    def test_aggregate_all_successful(self):
        """Test aggregating all successful results."""
        results = [
            OperationResult(success=True, data={"value": i})
            for i in range(5)
        ]

        aggregated = aggregate_operation_results(results, response_format="summary")

        assert aggregated.success is True
        assert aggregated.data["successful"] == 5
        assert aggregated.data["failed"] == 0
        assert aggregated.data["success_rate"] == 100.0

    def test_aggregate_all_failed(self):
        """Test aggregating all failed results."""
        results = [
            OperationResult(success=False, error=f"Error {i}")
            for i in range(3)
        ]

        aggregated = aggregate_operation_results(results, response_format="summary")

        assert aggregated.success is False
        assert aggregated.data["successful"] == 0
        assert aggregated.data["failed"] == 3
        assert aggregated.data["success_rate"] == 0.0


class TestPerformanceMetrics:
    """Test performance metric calculations."""

    def test_speedup_calculation(self):
        """Test speedup calculation in summary."""
        aggregator = ResultAggregator()

        # Simulate tasks that took 1s each but ran in 0.25s wall clock
        time.sleep(0.25)  # Simulate wall clock time

        # Add results with durations
        for i in range(4):
            op_result = OperationResult(
                success=True,
                data={"value": i},
                duration=1.0  # Each task took 1s
            )
            aggregator.add_result(f"task{i}", op_result)

        summary = aggregator.get_summary()

        # Total duration should be 4s (4 tasks × 1s)
        assert summary["total_duration"] == pytest.approx(4.0, rel=0.01)

        # Wall clock time should be ~0.25s
        assert summary["wall_clock_time"] >= 0.25

        # Speedup should be ~16x (4s / 0.25s)
        assert summary["speedup"] > 10  # At least 10x speedup

    def test_empty_aggregator_summary(self):
        """Test summary with no results."""
        aggregator = ResultAggregator()
        summary = aggregator.get_summary()

        assert summary["total_tasks"] == 0
        assert summary["successful"] == 0
        assert summary["failed"] == 0
        assert summary["success_rate"] == 0.0
        assert summary["speedup"] == 0

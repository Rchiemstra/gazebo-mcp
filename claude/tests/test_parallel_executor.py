"""
Tests for ParallelExecutor

Tests the parallel execution infrastructure including thread, process,
and async execution modes.
"""

import pytest
import asyncio
import time
from skills.common.parallel_executor import (
    ParallelExecutor,
    ExecutorType,
    TaskResult,
    get_optimal_worker_count
)


# Test helper functions
def simple_add(a: int, b: int) -> int:
    """Simple function for testing."""
    return a + b


def slow_operation(duration: float = 0.1) -> str:
    """Simulate a slow operation."""
    time.sleep(duration)
    return f"completed after {duration}s"


def failing_operation():
    """Function that always fails."""
    raise ValueError("This operation always fails")


async def async_add(a: int, b: int) -> int:
    """Async version of add for testing."""
    await asyncio.sleep(0.01)  # Simulate some async work
    return a + b


async def async_failing():
    """Async function that fails."""
    await asyncio.sleep(0.01)
    raise RuntimeError("Async operation failed")


class TestParallelExecutor:
    """Test cases for ParallelExecutor."""

    def test_thread_executor_basic(self):
        """Test basic thread pool execution."""
        executor = ParallelExecutor(max_workers=2, executor_type=ExecutorType.THREAD)

        tasks = [
            (simple_add, (1, 2), {}),
            (simple_add, (3, 4), {}),
            (simple_add, (5, 6), {}),
        ]

        results = executor.execute(tasks)

        assert len(results) == 3
        assert all(r.success for r in results)
        assert results[0].result == 3
        assert results[1].result == 7
        assert results[2].result == 11

    def test_thread_executor_with_errors(self):
        """Test thread execution with some failures."""
        executor = ParallelExecutor(max_workers=2, executor_type=ExecutorType.THREAD)

        tasks = [
            (simple_add, (1, 2), {}),
            (failing_operation, (), {}),
            (simple_add, (5, 6), {}),
        ]

        results = executor.execute(tasks, fail_fast=False)

        assert len(results) == 3
        assert results[0].success is True
        assert results[1].success is False
        assert results[2].success is True
        assert "always fails" in results[1].error

    def test_thread_executor_fail_fast(self):
        """Test fail-fast mode stops on first error."""
        executor = ParallelExecutor(max_workers=2, executor_type=ExecutorType.THREAD)

        tasks = [
            (failing_operation, (), {}),
            (slow_operation, (1.0,), {}),  # Should be cancelled
            (simple_add, (1, 2), {}),
        ]

        results = executor.execute(tasks, fail_fast=True)

        # Should have at least one failure
        assert any(not r.success for r in results)

    def test_async_executor_basic(self):
        """Test basic async execution."""
        executor = ParallelExecutor(max_workers=2, executor_type=ExecutorType.ASYNC)

        tasks = [
            (async_add, (1, 2), {}),
            (async_add, (3, 4), {}),
            (async_add, (5, 6), {}),
        ]

        results = executor.execute(tasks)

        assert len(results) == 3
        assert all(r.success for r in results)
        assert results[0].result == 3
        assert results[1].result == 7
        assert results[2].result == 11

    def test_async_executor_with_errors(self):
        """Test async execution with failures."""
        executor = ParallelExecutor(max_workers=2, executor_type=ExecutorType.ASYNC)

        tasks = [
            (async_add, (1, 2), {}),
            (async_failing, (), {}),
            (async_add, (5, 6), {}),
        ]

        results = executor.execute(tasks, fail_fast=False)

        assert len(results) == 3
        assert results[0].success is True
        assert results[1].success is False
        assert results[2].success is True

    def test_async_executor_with_timeout(self):
        """Test async execution with timeout."""
        async def slow_async():
            await asyncio.sleep(2.0)
            return "done"

        executor = ParallelExecutor(
            max_workers=2,
            executor_type=ExecutorType.ASYNC,
            timeout=0.5
        )

        tasks = [(slow_async, (), {})]
        results = executor.execute(tasks)

        assert len(results) == 1
        assert results[0].success is False
        assert "timed out" in results[0].error.lower()

    def test_shared_context_execution(self):
        """Test execution with shared context to optimize tokens."""
        def process_with_context(item, shared_context=None):
            """Process item using shared context."""
            if shared_context is None:
                raise ValueError("Expected shared context")
            return f"{item}:{shared_context['value']}"

        def create_shared_context():
            """Create shared context once."""
            return {"value": "shared_data"}

        executor = ParallelExecutor(max_workers=2, executor_type=ExecutorType.THREAD)

        tasks = [
            (process_with_context, ("item1",), {}),
            (process_with_context, ("item2",), {}),
            (process_with_context, ("item3",), {}),
        ]

        shared_context, results = executor.execute_with_shared_context(
            tasks,
            create_shared_context
        )

        assert shared_context == {"value": "shared_data"}
        assert len(results) == 3
        assert all(r.success for r in results)
        assert results[0].result == "item1:shared_data"
        assert results[1].result == "item2:shared_data"
        assert results[2].result == "item3:shared_data"

    def test_task_result_ordering(self):
        """Test that results maintain task order."""
        executor = ParallelExecutor(max_workers=4, executor_type=ExecutorType.THREAD)

        tasks = [
            (simple_add, (i, i), {})
            for i in range(10)
        ]

        results = executor.execute(tasks)

        assert len(results) == 10
        for i, result in enumerate(results):
            assert result.task_id == i
            assert result.result == i + i

    def test_get_optimal_worker_count(self):
        """Test worker count calculation."""
        # I/O-bound should use more workers
        io_workers = get_optimal_worker_count("io")
        assert io_workers > 0

        # CPU-bound should match CPU count roughly
        cpu_workers = get_optimal_worker_count("cpu")
        assert cpu_workers > 0

        # With memory constraint
        constrained = get_optimal_worker_count("io", available_memory_gb=2.0)
        assert constrained > 0
        assert constrained <= 10  # Reasonable limit


class TestTaskResult:
    """Test cases for TaskResult dataclass."""

    def test_task_result_creation(self):
        """Test creating task results."""
        result = TaskResult(
            task_id=0,
            success=True,
            result=42,
            duration=1.5
        )

        assert result.task_id == 0
        assert result.success is True
        assert result.result == 42
        assert result.duration == 1.5
        assert result.error is None

    def test_task_result_with_error(self):
        """Test task result with error."""
        result = TaskResult(
            task_id=1,
            success=False,
            error="Something went wrong",
            error_type="ValueError"
        )

        assert result.task_id == 1
        assert result.success is False
        assert result.error == "Something went wrong"
        assert result.error_type == "ValueError"
        assert result.result is None


class TestPerformance:
    """Performance tests for parallel execution."""

    def test_parallel_speedup(self):
        """Test that parallel execution is faster than sequential."""
        num_tasks = 8
        sleep_duration = 0.1

        # Sequential execution
        start = time.time()
        for _ in range(num_tasks):
            slow_operation(sleep_duration)
        sequential_time = time.time() - start

        # Parallel execution
        executor = ParallelExecutor(max_workers=4, executor_type=ExecutorType.THREAD)
        tasks = [(slow_operation, (sleep_duration,), {}) for _ in range(num_tasks)]

        start = time.time()
        results = executor.execute(tasks)
        parallel_time = time.time() - start

        # Parallel should be significantly faster (at least 2x with 4 workers)
        assert parallel_time < sequential_time / 1.5
        assert len(results) == num_tasks
        assert all(r.success for r in results)

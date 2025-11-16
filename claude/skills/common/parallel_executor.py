"""
Parallel Executor Module

Provides infrastructure for executing tasks in parallel using threads,
processes, or async coroutines with proper error handling and resource management.

Part of Phase 1: Foundation (Parallel Execution Plan)
"""

import asyncio
import multiprocessing
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Tuple, Union
from enum import Enum


class ExecutorType(Enum):
    """Type of executor to use for parallel execution."""
    THREAD = "thread"      # I/O-bound operations
    PROCESS = "process"    # CPU-bound operations
    ASYNC = "async"        # Async coroutines


@dataclass
class TaskResult:
    """Result from a single parallel task."""
    task_id: int
    success: bool
    result: Any = None
    error: Optional[str] = None
    error_type: Optional[str] = None
    duration: float = 0.0


class ParallelExecutor:
    """
    Execute tasks in parallel with configurable execution strategy.

    Supports:
    - Thread pool for I/O-bound operations
    - Process pool for CPU-bound operations
    - Async execution for coroutines
    - Automatic error handling and aggregation
    - Resource limits and timeout support

    Token Optimization:
    - Use shared_context to avoid copying context to each task
    - Aggregate results locally before returning
    - Support for fail-fast or fail-soft error handling

    Example:
        executor = ParallelExecutor(max_workers=4)

        # Execute functions in parallel
        tasks = [
            (analyze_file, ("file1.py",)),
            (analyze_file, ("file2.py",)),
            (analyze_file, ("file3.py",)),
        ]
        results = executor.execute(tasks)
    """

    def __init__(
        self,
        max_workers: Optional[int] = None,
        executor_type: ExecutorType = ExecutorType.THREAD,
        timeout: Optional[float] = None
    ):
        """
        Initialize parallel executor.

        Args:
            max_workers: Maximum concurrent workers (default: CPU count)
            executor_type: Type of executor (THREAD, PROCESS, or ASYNC)
            timeout: Global timeout in seconds (default: None)
        """
        self.max_workers = max_workers or multiprocessing.cpu_count()
        self.executor_type = executor_type
        self.timeout = timeout
        self._shared_context_cache = {}

    def execute(
        self,
        tasks: List[Tuple[Callable, Tuple, dict]],
        fail_fast: bool = False
    ) -> List[TaskResult]:
        """
        Execute tasks in parallel.

        Args:
            tasks: List of (function, args, kwargs) tuples
            fail_fast: If True, stop on first error (default: False)

        Returns:
            List of TaskResult objects
        """
        if self.executor_type == ExecutorType.ASYNC:
            return asyncio.run(self._execute_async(tasks, fail_fast))
        elif self.executor_type == ExecutorType.THREAD:
            return self._execute_threaded(tasks, fail_fast)
        elif self.executor_type == ExecutorType.PROCESS:
            return self._execute_process(tasks, fail_fast)
        else:
            raise ValueError(f"Unknown executor type: {self.executor_type}")

    def _execute_threaded(
        self,
        tasks: List[Tuple[Callable, Tuple, dict]],
        fail_fast: bool
    ) -> List[TaskResult]:
        """Execute tasks using thread pool."""
        results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_id = {}
            for task_id, (func, args, kwargs) in enumerate(tasks):
                future = executor.submit(self._execute_task, func, args, kwargs)
                future_to_id[future] = task_id

            # Collect results as they complete
            for future in as_completed(future_to_id, timeout=self.timeout):
                task_id = future_to_id[future]
                try:
                    result = future.result()
                    results.append(TaskResult(
                        task_id=task_id,
                        success=True,
                        result=result,
                        duration=0.0  # TODO: Track actual duration
                    ))
                except Exception as e:
                    results.append(TaskResult(
                        task_id=task_id,
                        success=False,
                        error=str(e),
                        error_type=type(e).__name__
                    ))

                    if fail_fast:
                        # Cancel remaining tasks
                        for f in future_to_id:
                            f.cancel()
                        break

        # Sort results by task_id to maintain order
        results.sort(key=lambda r: r.task_id)
        return results

    def _execute_process(
        self,
        tasks: List[Tuple[Callable, Tuple, dict]],
        fail_fast: bool
    ) -> List[TaskResult]:
        """Execute tasks using process pool."""
        results = []

        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_id = {}
            for task_id, (func, args, kwargs) in enumerate(tasks):
                future = executor.submit(self._execute_task, func, args, kwargs)
                future_to_id[future] = task_id

            # Collect results as they complete
            for future in as_completed(future_to_id, timeout=self.timeout):
                task_id = future_to_id[future]
                try:
                    result = future.result()
                    results.append(TaskResult(
                        task_id=task_id,
                        success=True,
                        result=result
                    ))
                except Exception as e:
                    results.append(TaskResult(
                        task_id=task_id,
                        success=False,
                        error=str(e),
                        error_type=type(e).__name__
                    ))

                    if fail_fast:
                        # Cancel remaining tasks
                        for f in future_to_id:
                            f.cancel()
                        break

        # Sort results by task_id to maintain order
        results.sort(key=lambda r: r.task_id)
        return results

    async def _execute_async(
        self,
        tasks: List[Tuple[Callable, Tuple, dict]],
        fail_fast: bool
    ) -> List[TaskResult]:
        """Execute tasks using async coroutines."""
        results = []

        async def execute_task_async(task_id, func, args, kwargs):
            """Execute a single async task."""
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                return TaskResult(
                    task_id=task_id,
                    success=True,
                    result=result,
                    duration=duration
                )
            except Exception as e:
                duration = time.time() - start_time
                return TaskResult(
                    task_id=task_id,
                    success=False,
                    error=str(e),
                    error_type=type(e).__name__,
                    duration=duration
                )

        # Create coroutines for all tasks
        coroutines = [
            execute_task_async(task_id, func, args, kwargs)
            for task_id, (func, args, kwargs) in enumerate(tasks)
        ]

        # Execute with timeout if specified
        if self.timeout:
            try:
                results = await asyncio.wait_for(
                    asyncio.gather(*coroutines, return_exceptions=not fail_fast),
                    timeout=self.timeout
                )
            except asyncio.TimeoutError:
                # Return partial results with timeout errors
                results = [
                    TaskResult(
                        task_id=i,
                        success=False,
                        error="Operation timed out",
                        error_type="TimeoutError"
                    )
                    for i in range(len(tasks))
                ]
        else:
            results = await asyncio.gather(*coroutines, return_exceptions=not fail_fast)

        # Handle exception results if not fail_fast
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append(TaskResult(
                    task_id=i,
                    success=False,
                    error=str(result),
                    error_type=type(result).__name__
                ))
            elif isinstance(result, TaskResult):
                processed_results.append(result)
            else:
                processed_results.append(TaskResult(
                    task_id=i,
                    success=True,
                    result=result
                ))

        return processed_results

    @staticmethod
    def _execute_task(func: Callable, args: Tuple, kwargs: dict) -> Any:
        """Execute a single task with error handling."""
        return func(*args, **kwargs)

    def execute_with_shared_context(
        self,
        tasks: List[Tuple[Callable, Tuple, dict]],
        shared_context_fn: Callable[[], Any],
        fail_fast: bool = False
    ) -> Tuple[Any, List[TaskResult]]:
        """
        Execute tasks with a shared context to optimize token usage.

        The shared context is generated once and can be referenced by all tasks,
        avoiding redundant token consumption.

        Args:
            tasks: List of (function, args, kwargs) tuples
            shared_context_fn: Function to generate shared context
            fail_fast: If True, stop on first error

        Returns:
            Tuple of (shared_context, results)
        """
        # Generate shared context once
        shared_context = shared_context_fn()

        # Add shared context to each task's kwargs
        tasks_with_context = []
        for func, args, kwargs in tasks:
            kwargs_with_context = dict(kwargs)
            kwargs_with_context['shared_context'] = shared_context
            tasks_with_context.append((func, args, kwargs_with_context))

        # Execute tasks
        results = self.execute(tasks_with_context, fail_fast=fail_fast)

        return shared_context, results


def get_optimal_worker_count(
    operation_type: str = "io",
    available_memory_gb: Optional[float] = None
) -> int:
    """
    Determine optimal worker count based on operation type and system resources.

    Args:
        operation_type: "io" for I/O-bound, "cpu" for CPU-bound
        available_memory_gb: Available memory in GB (optional, will detect if None)

    Returns:
        Recommended worker count
    """
    cpu_count = multiprocessing.cpu_count()

    if operation_type == "io":
        # I/O-bound: Can use more workers than CPUs
        base_workers = cpu_count * 2
    else:
        # CPU-bound: Match CPU count
        base_workers = cpu_count

    # Adjust based on available memory if provided
    if available_memory_gb is not None:
        # Assume each worker needs ~500MB
        max_workers_by_memory = int(available_memory_gb * 2)
        return min(base_workers, max_workers_by_memory)

    return base_workers

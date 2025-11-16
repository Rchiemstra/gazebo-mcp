"""
Performance benchmarking suite for parallel execution.

Provides comprehensive benchmarks to measure and validate
performance improvements from parallel execution.

Usage:
    python tests/benchmark_parallel_execution.py
    python tests/benchmark_parallel_execution.py --save-results benchmarks/results.json
"""

import time
import tempfile
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, asdict

from skills.code_analysis import analyze_codebase, analyze_codebase_parallel
from skills.test_orchestrator import (
    analyze_file,
    analyze_files_parallel,
    generate_tests,
    generate_tests_parallel
)
from skills.common import ParallelExecutor, ExecutorType


@dataclass
class BenchmarkResult:
    """Result from a benchmark run."""
    name: str
    operation: str
    input_size: int
    sequential_time: float
    parallel_time: float
    speedup: float
    improvement_pct: float
    metadata: Dict[str, Any]

    def to_dict(self):
        return asdict(self)


class PerformanceBenchmark:
    """Performance benchmarking suite."""

    def __init__(self):
        self.results: List[BenchmarkResult] = []

    def create_test_files(self, tmp_dir: Path, count: int) -> List[Path]:
        """Create test Python files for benchmarking."""
        files = []
        for i in range(count):
            file_path = tmp_dir / f"test_module_{i}.py"
            file_path.write_text(f'''
"""Test module {i}."""

def function_{i}_add(a, b):
    """Add two numbers with offset {i}."""
    return a + b + {i}

def function_{i}_multiply(a, b):
    """Multiply two numbers with factor {i}."""
    return a * b * {i}

def function_{i}_complex(x, y, z):
    """Complex calculation {i}."""
    result = 0
    for i in range(x):
        for j in range(y):
            result += i * j + z
    return result

class TestClass{i}:
    """Test class {i}."""

    def __init__(self):
        self.value = {i}

    def method_{i}(self):
        """Method {i}."""
        return self.value * {i}

    def complex_method(self, x):
        """Complex method."""
        if x > 0:
            return self.value * x
        else:
            return self.value / (x - 1) if x != 1 else 0
''')
            files.append(file_path)
        return files

    def benchmark_code_analysis(self, file_count: int) -> BenchmarkResult:
        """Benchmark code analysis with varying file counts."""
        print(f"\n{'='*60}")
        print(f"Benchmarking Code Analysis: {file_count} files")
        print(f"{'='*60}")

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            files = self.create_test_files(tmp_path, file_count)

            # Sequential analysis
            print("Running sequential analysis...")
            start = time.time()
            seq_result = analyze_codebase(
                str(tmp_path),
                response_format="summary"
            )
            sequential_time = time.time() - start

            assert seq_result.success, "Sequential analysis failed"
            print(f"  Sequential: {sequential_time:.2f}s")

            # Parallel analysis
            print("Running parallel analysis...")
            start = time.time()
            par_result = analyze_codebase_parallel(
                str(tmp_path),
                response_format="summary"
            )
            parallel_time = time.time() - start

            assert par_result.success, "Parallel analysis failed"
            print(f"  Parallel:   {parallel_time:.2f}s")

            speedup = sequential_time / parallel_time
            improvement = ((sequential_time - parallel_time) / sequential_time) * 100

            print(f"  Speedup:    {speedup:.2f}x")
            print(f"  Improvement: {improvement:.1f}%")

            result = BenchmarkResult(
                name=f"code_analysis_{file_count}_files",
                operation="analyze_codebase",
                input_size=file_count,
                sequential_time=sequential_time,
                parallel_time=parallel_time,
                speedup=speedup,
                improvement_pct=improvement,
                metadata={
                    "total_files": seq_result.data["total_files"],
                    "total_lines": seq_result.data["total_lines"]
                }
            )

            self.results.append(result)
            return result

    def benchmark_batch_file_analysis(self, file_count: int) -> BenchmarkResult:
        """Benchmark batch file analysis."""
        print(f"\n{'='*60}")
        print(f"Benchmarking Batch File Analysis: {file_count} files")
        print(f"{'='*60}")

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            files = self.create_test_files(tmp_path, file_count)
            file_paths = [str(f) for f in files]

            # Sequential analysis
            print("Running sequential analysis...")
            start = time.time()
            seq_results = []
            for file_path in file_paths:
                result = analyze_file(file_path, response_format="summary")
                if result.success:
                    seq_results.append(result)
            sequential_time = time.time() - start

            print(f"  Sequential: {sequential_time:.2f}s")

            # Parallel analysis
            print("Running parallel analysis...")
            start = time.time()
            par_result = analyze_files_parallel(
                file_paths,
                response_format="summary"
            )
            parallel_time = time.time() - start

            assert par_result.success, "Parallel analysis failed"
            print(f"  Parallel:   {parallel_time:.2f}s")

            speedup = sequential_time / parallel_time
            improvement = ((sequential_time - parallel_time) / sequential_time) * 100

            print(f"  Speedup:    {speedup:.2f}x")
            print(f"  Improvement: {improvement:.1f}%")

            result = BenchmarkResult(
                name=f"batch_analysis_{file_count}_files",
                operation="analyze_files_parallel",
                input_size=file_count,
                sequential_time=sequential_time,
                parallel_time=parallel_time,
                speedup=speedup,
                improvement_pct=improvement,
                metadata={
                    "successful": par_result.data["analyzed_successfully"],
                    "total_functions": par_result.data["total_functions"]
                }
            )

            self.results.append(result)
            return result

    def benchmark_test_generation(self, file_count: int) -> BenchmarkResult:
        """Benchmark test generation."""
        print(f"\n{'='*60}")
        print(f"Benchmarking Test Generation: {file_count} files")
        print(f"{'='*60}")

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            files = self.create_test_files(tmp_path, file_count)
            file_paths = [str(f) for f in files]

            # Sequential test generation
            print("Running sequential test generation...")
            start = time.time()
            seq_results = []
            for file_path in file_paths:
                result = generate_tests(
                    file_path,
                    target_coverage=80.0,
                    response_format="concise"
                )
                if result.success:
                    seq_results.append(result)
            sequential_time = time.time() - start

            print(f"  Sequential: {sequential_time:.2f}s")

            # Parallel test generation
            print("Running parallel test generation...")
            start = time.time()
            par_result = generate_tests_parallel(
                file_paths,
                target_coverage=80.0,
                response_format="concise"
            )
            parallel_time = time.time() - start

            assert par_result.success, "Parallel test generation failed"
            print(f"  Parallel:   {parallel_time:.2f}s")

            speedup = sequential_time / parallel_time
            improvement = ((sequential_time - parallel_time) / sequential_time) * 100

            print(f"  Speedup:    {speedup:.2f}x")
            print(f"  Improvement: {improvement:.1f}%")

            result = BenchmarkResult(
                name=f"test_generation_{file_count}_files",
                operation="generate_tests_parallel",
                input_size=file_count,
                sequential_time=sequential_time,
                parallel_time=parallel_time,
                speedup=speedup,
                improvement_pct=improvement,
                metadata={
                    "successful": par_result.data["successful"],
                    "total_tests": par_result.data["total_tests"]
                }
            )

            self.results.append(result)
            return result

    def benchmark_parallel_executor(self, task_count: int, task_duration: float) -> BenchmarkResult:
        """Benchmark raw ParallelExecutor performance."""
        print(f"\n{'='*60}")
        print(f"Benchmarking ParallelExecutor: {task_count} tasks @ {task_duration}s each")
        print(f"{'='*60}")

        def slow_task(i):
            """Simulate slow task."""
            time.sleep(task_duration)
            return i * 2

        # Sequential execution
        print("Running sequential execution...")
        start = time.time()
        seq_results = [slow_task(i) for i in range(task_count)]
        sequential_time = time.time() - start

        print(f"  Sequential: {sequential_time:.2f}s")

        # Parallel execution
        print("Running parallel execution...")
        executor = ParallelExecutor(
            max_workers=task_count,
            executor_type=ExecutorType.THREAD
        )

        tasks = [(slow_task, (i,), {}) for i in range(task_count)]

        start = time.time()
        par_results = executor.execute(tasks, fail_fast=False)
        parallel_time = time.time() - start

        assert all(r.success for r in par_results)
        print(f"  Parallel:   {parallel_time:.2f}s")

        speedup = sequential_time / parallel_time
        improvement = ((sequential_time - parallel_time) / sequential_time) * 100

        print(f"  Speedup:    {speedup:.2f}x")
        print(f"  Improvement: {improvement:.1f}%")

        result = BenchmarkResult(
            name=f"parallel_executor_{task_count}_tasks",
            operation="ParallelExecutor.execute",
            input_size=task_count,
            sequential_time=sequential_time,
            parallel_time=parallel_time,
            speedup=speedup,
            improvement_pct=improvement,
            metadata={
                "task_duration": task_duration,
                "max_workers": task_count
            }
        )

        self.results.append(result)
        return result

    def run_comprehensive_suite(self):
        """Run comprehensive benchmark suite."""
        print("\n" + "="*70)
        print(" " * 15 + "PARALLEL EXECUTION BENCHMARK SUITE")
        print("="*70)

        # Code analysis benchmarks
        print("\n--- CODE ANALYSIS BENCHMARKS ---")
        self.benchmark_code_analysis(10)   # Small
        self.benchmark_code_analysis(20)   # Medium (threshold)
        self.benchmark_code_analysis(50)   # Large
        self.benchmark_code_analysis(100)  # Very large

        # Batch analysis benchmarks
        print("\n--- BATCH ANALYSIS BENCHMARKS ---")
        self.benchmark_batch_file_analysis(5)   # Small
        self.benchmark_batch_file_analysis(10)  # Medium
        self.benchmark_batch_file_analysis(20)  # Large

        # Test generation benchmarks
        print("\n--- TEST GENERATION BENCHMARKS ---")
        self.benchmark_test_generation(3)   # Small
        self.benchmark_test_generation(5)   # Medium
        self.benchmark_test_generation(10)  # Large

        # Raw executor benchmarks
        print("\n--- PARALLEL EXECUTOR BENCHMARKS ---")
        self.benchmark_parallel_executor(4, 0.5)   # 4 tasks, 0.5s each
        self.benchmark_parallel_executor(8, 0.3)   # 8 tasks, 0.3s each
        self.benchmark_parallel_executor(10, 0.2)  # 10 tasks, 0.2s each

    def print_summary(self):
        """Print benchmark summary."""
        print("\n" + "="*70)
        print(" " * 25 + "BENCHMARK SUMMARY")
        print("="*70)

        print(f"\n{'Operation':<40} {'Files':<8} {'Speedup':<10} {'Improvement'}")
        print("-" * 70)

        for result in self.results:
            print(
                f"{result.operation:<40} "
                f"{result.input_size:<8} "
                f"{result.speedup:<10.2f}x "
                f"{result.improvement_pct:>6.1f}%"
            )

        # Calculate average speedup
        avg_speedup = sum(r.speedup for r in self.results) / len(self.results)
        avg_improvement = sum(r.improvement_pct for r in self.results) / len(self.results)

        print("-" * 70)
        print(
            f"{'AVERAGE':<40} "
            f"{'':<8} "
            f"{avg_speedup:<10.2f}x "
            f"{avg_improvement:>6.1f}%"
        )
        print("="*70)

    def save_results(self, output_file: str):
        """Save results to JSON file."""
        results_dict = {
            "benchmark_run": time.strftime("%Y-%m-%d %H:%M:%S"),
            "results": [r.to_dict() for r in self.results],
            "summary": {
                "total_benchmarks": len(self.results),
                "average_speedup": sum(r.speedup for r in self.results) / len(self.results),
                "average_improvement_pct": sum(r.improvement_pct for r in self.results) / len(self.results),
                "best_speedup": max(self.results, key=lambda r: r.speedup).to_dict(),
                "operations_tested": list(set(r.operation for r in self.results))
            }
        }

        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(results_dict, f, indent=2)

        print(f"\nResults saved to: {output_file}")


def main():
    """Run benchmarks from command line."""
    parser = argparse.ArgumentParser(description="Benchmark parallel execution performance")
    parser.add_argument(
        "--save-results",
        type=str,
        help="Save results to JSON file",
        default=None
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run quick benchmark suite (fewer iterations)"
    )

    args = parser.parse_args()

    benchmark = PerformanceBenchmark()

    if args.quick:
        print("\nRunning QUICK benchmark suite...")
        benchmark.benchmark_code_analysis(20)
        benchmark.benchmark_batch_file_analysis(10)
        benchmark.benchmark_test_generation(5)
        benchmark.benchmark_parallel_executor(4, 0.5)
    else:
        print("\nRunning COMPREHENSIVE benchmark suite...")
        benchmark.run_comprehensive_suite()

    benchmark.print_summary()

    if args.save_results:
        benchmark.save_results(args.save_results)

    return 0


if __name__ == "__main__":
    exit(main())

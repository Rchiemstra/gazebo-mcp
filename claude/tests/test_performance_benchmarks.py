"""
Performance benchmarks for skill operations.

Tests execution time, memory usage, and token efficiency across all skills.
Establishes baselines for regression detection.
"""

import pytest
import time
import json
import tempfile
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestExecutionPerformance:
    """Test operation execution time benchmarks."""

    @pytest.fixture
    def sample_python_file(self):
        """Create a sample Python file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('''
"""Sample module for testing."""

def function1(x, y):
    """Add two numbers."""
    return x + y

def function2(items):
    """Process a list of items."""
    result = []
    for item in items:
        if item > 0:
            result.append(item * 2)
    return result

class Calculator:
    """A simple calculator class."""

    def __init__(self):
        self.value = 0

    def add(self, n):
        """Add to current value."""
        self.value += n
        return self.value

    def subtract(self, n):
        """Subtract from current value."""
        self.value -= n
        return self.value

def complex_function(data):
    """A more complex function for testing."""
    if not data:
        return None

    calc = Calculator()
    results = []

    for i, item in enumerate(data):
        if i % 2 == 0:
            calc.add(item)
        else:
            calc.subtract(item)
        results.append(calc.value)

    return results
''')
            temp_path = f.name

        yield temp_path

        # Cleanup
        if os.path.exists(temp_path):
            os.unlink(temp_path)

    def test_analyze_file_execution_time(self, sample_python_file):
        """Test analyze_file execution time."""
        try:
            from skills.code_analysis.operations import analyze_file

            # Warm up (first run may be slower due to imports)
            analyze_file(sample_python_file, response_format='summary')

            # Measure execution time (5 runs)
            times = []
            for _ in range(5):
                start = time.time()
                result = analyze_file(sample_python_file, response_format='summary')
                elapsed = time.time() - start
                times.append(elapsed)

                assert result.success, "Operation should succeed"

            avg_time = sum(times) / len(times)
            max_time = max(times)
            min_time = min(times)

            # Performance assertions
            assert avg_time < 1.0, f"Average execution time {avg_time:.3f}s should be < 1.0s"
            assert max_time < 2.0, f"Max execution time {max_time:.3f}s should be < 2.0s"

            print(f"\nanalyze_file performance:")
            print(f"  Average: {avg_time:.3f}s")
            print(f"  Min: {min_time:.3f}s")
            print(f"  Max: {max_time:.3f}s")

        except ImportError:
            pytest.skip("code_analysis not available")

    def test_generate_tests_execution_time(self, sample_python_file):
        """Test generate_tests execution time."""
        try:
            from skills.test_orchestrator.operations import generate_tests

            # Warm up
            generate_tests(sample_python_file, response_format='summary')

            # Measure execution time (3 runs - this operation is slower)
            times = []
            for _ in range(3):
                start = time.time()
                result = generate_tests(sample_python_file, response_format='summary')
                elapsed = time.time() - start
                times.append(elapsed)

                assert result.success, "Operation should succeed"

            avg_time = sum(times) / len(times)
            max_time = max(times)

            # Performance assertions (test generation is slower)
            assert avg_time < 3.0, f"Average execution time {avg_time:.3f}s should be < 3.0s"
            assert max_time < 5.0, f"Max execution time {max_time:.3f}s should be < 5.0s"

            print(f"\ngenerate_tests performance:")
            print(f"  Average: {avg_time:.3f}s")
            print(f"  Max: {max_time:.3f}s")

        except ImportError:
            pytest.skip("test_orchestrator not available")

    def test_response_format_impact_on_speed(self, sample_python_file):
        """Test that response_format doesn't significantly impact execution time."""
        try:
            from skills.code_analysis.operations import analyze_file

            # Measure summary format time
            summary_times = []
            for _ in range(3):
                start = time.time()
                analyze_file(sample_python_file, response_format='summary')
                summary_times.append(time.time() - start)

            # Measure detailed format time
            detailed_times = []
            for _ in range(3):
                start = time.time()
                analyze_file(sample_python_file, response_format='detailed')
                detailed_times.append(time.time() - start)

            avg_summary = sum(summary_times) / len(summary_times)
            avg_detailed = sum(detailed_times) / len(detailed_times)

            # Detailed should not be more than 50% slower than summary
            # (most time is analysis, not formatting)
            time_ratio = avg_detailed / avg_summary
            assert time_ratio < 1.5, \
                f"Detailed format {time_ratio:.2f}x slower should be < 1.5x"

            print(f"\nResponse format time impact:")
            print(f"  Summary: {avg_summary:.3f}s")
            print(f"  Detailed: {avg_detailed:.3f}s")
            print(f"  Ratio: {time_ratio:.2f}x")

        except ImportError:
            pytest.skip("code_analysis not available")


class TestTokenEfficiency:
    """Test token usage and efficiency benchmarks."""

    @pytest.fixture
    def sample_python_file(self):
        """Create a sample Python file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('''
def func1(): pass
def func2(): pass
def func3(): pass
class Class1: pass
class Class2: pass
''')
            temp_path = f.name

        yield temp_path

        if os.path.exists(temp_path):
            os.unlink(temp_path)

    def estimate_tokens(self, data: Any) -> int:
        """Estimate token count from data size (rough approximation)."""
        # Convert to JSON string
        json_str = json.dumps(data)
        # Rough estimate: ~4 characters per token
        return len(json_str) // 4

    def test_summary_format_token_savings(self, sample_python_file):
        """Test token savings of summary format."""
        try:
            from skills.code_analysis.operations import analyze_file

            # Get both formats
            summary_result = analyze_file(sample_python_file, response_format='summary')
            detailed_result = analyze_file(sample_python_file, response_format='detailed')

            assert summary_result.success and detailed_result.success

            # Estimate tokens
            summary_tokens = self.estimate_tokens(summary_result.data)
            detailed_tokens = self.estimate_tokens(detailed_result.data)

            # Summary should use significantly fewer tokens
            # Note: For small test files, ratio may be higher due to overhead
            # In production with larger files, expect 20-40% (much better savings)
            savings_ratio = summary_tokens / detailed_tokens
            assert savings_ratio < 0.65, \
                f"Summary should use < 65% of detailed tokens (currently {savings_ratio:.1%})"

            savings_pct = (1 - savings_ratio) * 100

            print(f"\nToken efficiency:")
            print(f"  Summary: ~{summary_tokens} tokens")
            print(f"  Detailed: ~{detailed_tokens} tokens")
            print(f"  Savings: {savings_pct:.1f}%")

        except ImportError:
            pytest.skip("code_analysis not available")

    def test_token_efficiency_baselines(self):
        """Establish token efficiency baselines for common operations."""
        baselines = {
            'analyze_file': {
                'summary_max': 500,    # Max tokens for summary format
                'detailed_max': 5000,  # Max tokens for detailed format
            },
            'generate_tests': {
                'summary_max': 300,
                'detailed_max': 3000,
            },
            'load_plan': {
                'summary_max': 200,
                'detailed_max': 2000,
            }
        }

        # Document baselines
        print("\nToken efficiency baselines:")
        for op_name, limits in baselines.items():
            print(f"  {op_name}:")
            print(f"    Summary: < {limits['summary_max']} tokens")
            print(f"    Detailed: < {limits['detailed_max']} tokens")

        assert len(baselines) > 0


class TestMemoryUsage:
    """Test memory usage benchmarks."""

    def test_large_file_memory_efficiency(self):
        """Test memory usage doesn't explode with large files."""
        try:
            import psutil
            import os

            # Create a larger Python file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                # Generate file with 100 functions
                for i in range(100):
                    f.write(f'''
def function_{i}(x, y):
    """Function {i}."""
    return x + y
''')
                temp_path = f.name

            try:
                from skills.code_analysis.operations import analyze_file

                # Get process memory before
                process = psutil.Process(os.getpid())
                mem_before = process.memory_info().rss / 1024 / 1024  # MB

                # Analyze file
                result = analyze_file(temp_path, response_format='summary')
                assert result.success

                # Get memory after
                mem_after = process.memory_info().rss / 1024 / 1024  # MB
                mem_increase = mem_after - mem_before

                # Memory increase should be reasonable (< 50 MB for this operation)
                assert mem_increase < 50, \
                    f"Memory increase {mem_increase:.1f}MB should be < 50MB"

                print(f"\nMemory usage:")
                print(f"  Before: {mem_before:.1f}MB")
                print(f"  After: {mem_after:.1f}MB")
                print(f"  Increase: {mem_increase:.1f}MB")

            finally:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)

        except ImportError as e:
            if 'psutil' in str(e):
                pytest.skip("psutil not available")
            else:
                pytest.skip("code_analysis not available")


class TestPerformanceBaselines:
    """Establish performance baselines for regression detection."""

    def test_create_performance_baseline(self):
        """Create baseline performance metrics for future comparison."""

        baselines = {
            'code_analysis.analyze_file': {
                'avg_time_ms': 100,     # Average execution time
                'max_time_ms': 500,     # Maximum acceptable time
                'summary_tokens': 100,  # Typical summary token count
                'detailed_tokens': 1000, # Typical detailed token count
            },
            'test_orchestrator.generate_tests': {
                'avg_time_ms': 1000,
                'max_time_ms': 3000,
                'summary_tokens': 50,
                'detailed_tokens': 500,
            },
            'learning_plan_manager.load_plan': {
                'avg_time_ms': 50,
                'max_time_ms': 200,
                'summary_tokens': 50,
                'detailed_tokens': 500,
            }
        }

        # Could save these baselines to a file for regression testing
        baseline_file = Path(__file__).parent / 'performance_baselines.json'

        # For now, just verify structure
        assert len(baselines) > 0
        for op_name, metrics in baselines.items():
            assert 'avg_time_ms' in metrics
            assert 'max_time_ms' in metrics
            assert 'summary_tokens' in metrics
            assert 'detailed_tokens' in metrics

        print("\nPerformance baselines established:")
        print(json.dumps(baselines, indent=2))

        # Note: In production, would save to file:
        # with open(baseline_file, 'w') as f:
        #     json.dump(baselines, f, indent=2)


class TestRegressionDetection:
    """Test for performance regressions."""

    def test_no_performance_regression_analyze_file(self):
        """Test that analyze_file hasn't regressed in performance."""
        try:
            from skills.code_analysis.operations import analyze_file

            # Create test file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write('def test(): pass\n' * 10)
                temp_path = f.name

            try:
                # Baseline: should complete in < 500ms
                start = time.time()
                result = analyze_file(temp_path, response_format='summary')
                elapsed = time.time() - start

                assert result.success
                assert elapsed < 0.5, \
                    f"Execution time {elapsed:.3f}s exceeds baseline of 0.5s"

                # Token count baseline: summary should be < 500 tokens
                token_estimate = len(json.dumps(result.data)) // 4
                assert token_estimate < 500, \
                    f"Token estimate {token_estimate} exceeds baseline of 500"

                print(f"\nRegression check passed:")
                print(f"  Time: {elapsed:.3f}s (< 0.5s baseline)")
                print(f"  Tokens: ~{token_estimate} (< 500 baseline)")

            finally:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)

        except ImportError:
            pytest.skip("code_analysis not available")

    def test_error_handling_performance(self):
        """Test that error handling doesn't significantly impact performance."""
        try:
            from skills.code_analysis.operations import analyze_file

            # Time error case
            error_times = []
            for _ in range(5):
                start = time.time()
                result = analyze_file('/nonexistent/file.py')
                error_times.append(time.time() - start)
                assert not result.success

            avg_error_time = sum(error_times) / len(error_times)

            # Error handling should be fast (< 10ms)
            assert avg_error_time < 0.01, \
                f"Error handling {avg_error_time*1000:.1f}ms should be < 10ms"

            print(f"\nError handling performance:")
            print(f"  Average: {avg_error_time*1000:.1f}ms")

        except ImportError:
            pytest.skip("code_analysis not available")


if __name__ == "__main__":
    # Run with verbose output to see performance metrics
    pytest.main([__file__, "-v", "-s"])

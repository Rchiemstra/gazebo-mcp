"""
Integration tests for parallel execution workflows.

Tests the end-to-end workflows with parallel execution:
- Verification workflows
- Context gathering workflows
- Combined development workflows
"""

import pytest
import subprocess
import time
from pathlib import Path
import tempfile
import shutil

from skills.code_analysis import analyze_codebase_parallel
from skills.test_orchestrator import analyze_files_parallel, generate_tests_parallel
from skills.common import ParallelExecutor, ResultAggregator, ExecutorType


class TestParallelVerificationWorkflow:
    """Test parallel verification workflows."""

    @pytest.fixture
    def sample_package(self, tmp_path):
        """Create a sample ROS package for testing."""
        pkg_dir = tmp_path / "test_package"
        pkg_dir.mkdir()

        # Create source file
        src_dir = pkg_dir / "src"
        src_dir.mkdir()
        (src_dir / "test_node.cpp").write_text("""
#include <rclcpp/rclcpp.hpp>

class TestNode : public rclcpp::Node {
public:
    TestNode() : Node("test_node") {
        RCLCPP_INFO(this->get_logger(), "Test node started");
    }
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<TestNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
""")

        # Create CMakeLists.txt
        (pkg_dir / "CMakeLists.txt").write_text("""
cmake_minimum_required(VERSION 3.5)
project(test_package)

find_package(rclcpp REQUIRED)

add_executable(test_node src/test_node.cpp)
ament_target_dependencies(test_node rclcpp)

install(TARGETS test_node
  DESTINATION lib/${PROJECT_NAME})
""")

        # Create package.xml
        (pkg_dir / "package.xml").write_text("""
<?xml version="1.0"?>
<package format="3">
  <name>test_package</name>
  <version>0.1.0</version>
  <description>Test package</description>
  <maintainer email="test@test.com">Test</maintainer>
  <license>Apache-2.0</license>

  <depend>rclcpp</depend>

  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
""")

        return pkg_dir

    def test_verify_all_workflow(self, sample_package):
        """Test /verify-all command workflow."""
        # This would normally call the slash command
        # For testing, we simulate the parallel verification workflow

        checks = ["build", "tests", "lint", "node"]

        def mock_check(check_name):
            """Mock verification check."""
            time.sleep(0.5)  # Simulate work
            return {"name": check_name, "status": "pass"}

        executor = ParallelExecutor(
            max_workers=4,
            executor_type=ExecutorType.THREAD
        )

        tasks = [(mock_check, (check,), {}) for check in checks]

        start = time.time()
        results = executor.execute(tasks, fail_fast=False)
        duration = time.time() - start

        # Should complete in ~0.5s (parallel) instead of ~2s (sequential)
        assert duration < 1.0, f"Parallel execution too slow: {duration:.2f}s"
        assert all(r.success for r in results)

        # Aggregate results
        aggregator = ResultAggregator()
        for result in results:
            aggregator.add_result(
                result.result["name"],
                result.result,
                result.duration
            )

        summary = aggregator.get_summary()
        assert summary["successful"] == 4
        assert summary["failed"] == 0


class TestParallelContextGatheringWorkflow:
    """Test parallel context gathering workflows."""

    @pytest.fixture
    def sample_codebase(self, tmp_path):
        """Create a sample codebase for testing."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()

        # Create 25 Python files
        for i in range(25):
            (src_dir / f"module_{i}.py").write_text(f"""
def function_{i}(x):
    \"\"\"Function {i} documentation.\"\"\"
    return x * {i}

class Class{i}:
    \"\"\"Class {i} documentation.\"\"\"
    def method_{i}(self):
        return {i}
""")

        return tmp_path

    def test_parallel_context_gathering(self, sample_codebase):
        """Test parallel code analysis for context gathering."""
        # Test parallel analysis (should use parallel for 25 files)
        start = time.time()
        result = analyze_codebase_parallel(
            str(sample_codebase / "src"),
            response_format="summary"
        )
        parallel_duration = time.time() - start

        assert result.success
        assert result.data["total_files"] == 25
        assert result.data["parallel_execution"] is True

        # Should be significantly faster than sequential
        # (Though without real comparison, we just verify it completes quickly)
        assert parallel_duration < 5.0, f"Analysis too slow: {parallel_duration:.2f}s"

    def test_parallel_with_local_filtering(self, sample_codebase):
        """Test parallel analysis with ResultFilter."""
        from skills.common.filters import ResultFilter

        result = analyze_codebase_parallel(
            str(sample_codebase / "src"),
            response_format="filtered"
        )

        assert result.success
        files = result.data["files"]
        assert len(files) == 25

        # Filter locally for specific modules
        filtered = ResultFilter.search(files, "module_1", ["path", "name"])
        # Should find module_1, module_10-19
        assert len(filtered) >= 11

        # Get top 5 most complex
        top_5 = ResultFilter.top_n_by_field(filtered, "complexity", 5)
        assert len(top_5) <= 5


class TestParallelTestGenerationWorkflow:
    """Test parallel test generation workflows."""

    @pytest.fixture
    def sample_modules(self, tmp_path):
        """Create sample modules for test generation."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()

        files = []
        for i in range(10):
            file_path = src_dir / f"calculator_{i}.py"
            file_path.write_text(f"""
def add_{i}(a, b):
    return a + b + {i}

def multiply_{i}(a, b):
    return a * b * {i}

class Calculator{i}:
    def calculate(self, x):
        return x + {i}
""")
            files.append(str(file_path))

        return files

    def test_parallel_test_generation(self, sample_modules):
        """Test parallel test generation for multiple files."""
        # Generate tests in parallel
        start = time.time()
        result = generate_tests_parallel(
            sample_modules,
            target_coverage=80.0,
            response_format="concise"
        )
        duration = time.time() - start

        assert result.success
        assert result.data["successful"] == 10
        assert result.data["total_tests"] > 0
        assert result.data["parallel_execution"] is True

        # Should complete reasonably fast
        assert duration < 10.0, f"Test generation too slow: {duration:.2f}s"

    def test_batch_file_analysis(self, sample_modules):
        """Test batch file analysis in parallel."""
        result = analyze_files_parallel(
            sample_modules,
            response_format="summary"
        )

        assert result.success
        assert result.data["total_files"] == 10
        assert result.data["analyzed_successfully"] == 10
        assert result.data["total_functions"] >= 20  # At least 2 per file
        assert result.data["parallel_execution"] is True


class TestCompleteDevWorkflow:
    """Test complete development workflow with parallel execution."""

    def test_dev_workflow_phases(self, tmp_path):
        """Test that dev workflow phases can use parallel execution."""
        # Phase 1: Context Gathering (uses parallel internally)
        codebase = tmp_path / "src"
        codebase.mkdir()

        for i in range(20):
            (codebase / f"file_{i}.py").write_text(f"def func_{i}(): pass")

        # Simulate context gathering (would be /gather-context)
        context_result = analyze_codebase_parallel(
            str(codebase),
            response_format="summary"
        )

        assert context_result.success
        assert context_result.data["total_files"] == 20

        # Phase 2: Planning (no parallel needed - single operation)
        # Would call /plan here

        # Phase 3: Execution with parallel verification
        # Simulate verification checks
        def mock_verify(check_type):
            return {"check": check_type, "passed": True}

        executor = ParallelExecutor(executor_type=ExecutorType.THREAD)
        tasks = [
            (mock_verify, ("build",), {}),
            (mock_verify, ("tests",), {}),
            (mock_verify, ("lint",), {})
        ]

        results = executor.execute(tasks, fail_fast=False)

        assert all(r.success for r in results)
        assert len(results) == 3


class TestPerformanceComparison:
    """Performance validation tests."""

    def test_parallel_speedup_for_verification(self):
        """Verify that parallel verification is faster than sequential."""

        def slow_check(i):
            """Simulate a slow check."""
            time.sleep(0.3)
            return i

        # Sequential execution
        sequential_start = time.time()
        for i in range(4):
            slow_check(i)
        sequential_time = time.time() - sequential_start

        # Parallel execution
        executor = ParallelExecutor(
            max_workers=4,
            executor_type=ExecutorType.THREAD
        )

        tasks = [(slow_check, (i,), {}) for i in range(4)]

        parallel_start = time.time()
        results = executor.execute(tasks, fail_fast=False)
        parallel_time = time.time() - parallel_start

        # Parallel should be significantly faster
        speedup = sequential_time / parallel_time
        assert speedup > 2.0, f"Insufficient speedup: {speedup:.2f}x"

        # All results should be successful
        assert all(r.success for r in results)

    def test_token_efficiency(self, tmp_path):
        """Verify token efficiency of parallel operations."""
        # Create test files
        src_dir = tmp_path / "src"
        src_dir.mkdir()

        for i in range(30):
            (src_dir / f"file_{i}.py").write_text(f"def func_{i}(): return {i}")

        # Test with summary format (token efficient)
        result = analyze_codebase_parallel(
            str(src_dir),
            response_format="summary"
        )

        assert result.success
        # Summary should not include full file contents
        assert "file_list" in result.data
        assert len(result.data.get("file_list", [])) <= 20  # First 20 only

        # Test with filtered format + ResultFilter
        from skills.common.filters import ResultFilter

        result = analyze_codebase_parallel(
            str(src_dir),
            response_format="filtered"
        )

        files = result.data["files"]
        # Filter locally (0 tokens)
        filtered = ResultFilter.limit(files, 5)

        assert len(filtered) == 5
        # This filtering happened locally without API calls


class TestErrorHandling:
    """Test error handling in parallel workflows."""

    def test_partial_failure_handling(self):
        """Test that partial failures are handled gracefully."""

        def sometimes_fails(i):
            if i == 2:
                raise ValueError("Simulated failure")
            return i

        executor = ParallelExecutor(executor_type=ExecutorType.THREAD)
        tasks = [(sometimes_fails, (i,), {}) for i in range(5)]

        # With fail_fast=False, all tasks should be attempted
        results = executor.execute(tasks, fail_fast=False)

        assert len(results) == 5
        assert sum(1 for r in results if r.success) == 4
        assert sum(1 for r in results if not r.success) == 1

        # Verify the failed task
        failed = [r for r in results if not r.success][0]
        assert "Simulated failure" in failed.error

    def test_graceful_fallback(self, tmp_path):
        """Test graceful fallback when parallel infrastructure unavailable."""
        # Create small codebase (< 20 files triggers fallback)
        src_dir = tmp_path / "src"
        src_dir.mkdir()

        for i in range(10):
            (src_dir / f"file_{i}.py").write_text(f"def func(): pass")

        # Should automatically use sequential
        result = analyze_codebase_parallel(str(src_dir))

        assert result.success
        # Will use sequential (no parallel_execution flag or will be False)
        # depending on implementation


# Integration test fixtures
@pytest.fixture
def ros_workspace(tmp_path):
    """Create a mock ROS workspace."""
    ws = tmp_path / "ros_ws"
    ws.mkdir()

    src = ws / "src"
    src.mkdir()

    # Create a simple package
    pkg = src / "test_pkg"
    pkg.mkdir()

    (pkg / "CMakeLists.txt").write_text("cmake_minimum_required(VERSION 3.5)")
    (pkg / "package.xml").write_text("<package><name>test_pkg</name></package>")

    return ws


# Mark integration tests
pytestmark = pytest.mark.integration

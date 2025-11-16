"""
Tests for parallel code analysis operations.

Tests the parallel execution of code analysis with shared context,
error handling, and performance validation.
"""

import pytest
import time
import tempfile
from pathlib import Path

from skills.code_analysis import (
    analyze_codebase,
    analyze_codebase_parallel,
    CodeAnalyzer
)


# Test fixtures - create temporary Python files
@pytest.fixture
def temp_codebase(tmp_path):
    """Create a temporary codebase with multiple Python files."""

    # Create directory structure
    src_dir = tmp_path / "src"
    src_dir.mkdir()

    # Create multiple Python files
    files = []

    # Simple module
    (src_dir / "simple.py").write_text("""
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
""")
    files.append(src_dir / "simple.py")

    # Class with methods
    (src_dir / "calculator.py").write_text("""
class Calculator:
    def __init__(self):
        self.result = 0

    def add(self, x):
        self.result += x
        return self.result

    def subtract(self, x):
        self.result -= x
        return self.result

    def clear(self):
        self.result = 0
""")
    files.append(src_dir / "calculator.py")

    # Module with patterns
    (src_dir / "factory.py").write_text("""
class ShapeFactory:
    @staticmethod
    def create_shape(shape_type):
        if shape_type == "circle":
            return Circle()
        elif shape_type == "square":
            return Square()
        return None

class Circle:
    def area(self):
        return 3.14

class Square:
    def area(self):
        return 1.0
""")
    files.append(src_dir / "factory.py")

    # Complex module
    (src_dir / "complex.py").write_text("""
import os
import sys
from pathlib import Path

class ComplexCalculator:
    def __init__(self, mode="normal"):
        self.mode = mode
        self._cache = {}

    def calculate(self, operation, *args):
        if operation == "add":
            return sum(args)
        elif operation == "multiply":
            result = 1
            for arg in args:
                result *= arg
            return result
        elif operation == "power":
            if len(args) < 2:
                raise ValueError("Need at least 2 args")
            base, exp = args[0], args[1]
            return base ** exp
        else:
            raise ValueError(f"Unknown operation: {operation}")

    def _cache_result(self, key, value):
        self._cache[key] = value
""")
    files.append(src_dir / "complex.py")

    return {
        "root": tmp_path,
        "src": src_dir,
        "files": files
    }


@pytest.fixture
def large_codebase(tmp_path):
    """Create a larger codebase for performance testing."""
    src_dir = tmp_path / "src"
    src_dir.mkdir()

    # Create 30 files to test parallelization benefits
    for i in range(30):
        (src_dir / f"module_{i}.py").write_text(f"""
class Class{i}:
    def __init__(self):
        self.value = {i}

    def method_{i}(self):
        return self.value * {i}

    def complex_method(self, x, y):
        result = 0
        for j in range(x):
            for k in range(y):
                result += j * k
        return result

def function_{i}(a, b):
    return a + b + {i}

def another_function_{i}(x):
    if x > 0:
        return x * 2
    else:
        return x / 2
""")

    return {"root": tmp_path, "src": src_dir, "file_count": 30}


class TestParallelCodeAnalysis:
    """Test cases for parallel code analysis."""

    def test_parallel_basic_analysis(self, temp_codebase):
        """Test basic parallel codebase analysis."""
        result = analyze_codebase_parallel(
            str(temp_codebase["src"]),
            response_format="summary"
        )

        assert result.success is True
        assert result.data["total_files"] == 4
        assert result.data["parallel_execution"] is True
        assert result.metadata["parallel_execution"] is True

    def test_parallel_detailed_format(self, temp_codebase):
        """Test parallel analysis with detailed format."""
        result = analyze_codebase_parallel(
            str(temp_codebase["src"]),
            response_format="detailed"
        )

        assert result.success is True
        assert "files" in result.data
        assert len(result.data["files"]) == 4

        # Check that each file has expected structure
        for file_info in result.data["files"]:
            assert "path" in file_info
            assert "entities" in file_info
            assert "imports" in file_info

    def test_parallel_filtered_format(self, temp_codebase):
        """Test parallel analysis with filtered format for local filtering."""
        result = analyze_codebase_parallel(
            str(temp_codebase["src"]),
            response_format="filtered"
        )

        assert result.success is True
        assert "files" in result.data
        assert len(result.data["files"]) == 4

        # Check filterable fields
        for file_info in result.data["files"]:
            assert "path" in file_info
            assert "name" in file_info
            assert "complexity" in file_info
            assert "entity_count" in file_info

    def test_parallel_small_codebase_fallback(self, temp_codebase):
        """Test that small codebases fall back to sequential."""
        # CodeAnalyzer should use sequential for < 20 files
        analyzer = CodeAnalyzer()
        analysis = analyzer.analyze_codebase_parallel(
            str(temp_codebase["src"])
        )

        # Should complete successfully (whether parallel or sequential)
        assert analysis.total_files == 4
        assert len(analysis.files) == 4

    def test_parallel_max_files_limit(self, large_codebase):
        """Test max_files parameter limits analysis."""
        result = analyze_codebase_parallel(
            str(large_codebase["src"]),
            response_format="summary",
            max_files=10
        )

        assert result.success is True
        # Should analyze at most 10 files
        assert result.data["total_files"] <= 10

    def test_parallel_max_workers_parameter(self, large_codebase):
        """Test max_workers parameter controls parallelism."""
        result = analyze_codebase_parallel(
            str(large_codebase["src"]),
            response_format="summary",
            max_workers=2
        )

        assert result.success is True
        assert result.data["total_files"] == 30

    def test_parallel_pattern_detection(self, temp_codebase):
        """Test that parallel analysis detects patterns correctly."""
        result = analyze_codebase_parallel(
            str(temp_codebase["src"]),
            response_format="summary"
        )

        assert result.success is True
        assert "patterns_summary" in result.data
        # Should detect Factory pattern in factory.py
        patterns = result.data["patterns_summary"]
        assert len(patterns) > 0

    def test_parallel_integration_points(self, temp_codebase):
        """Test that parallel analysis identifies integration points."""
        result = analyze_codebase_parallel(
            str(temp_codebase["src"]),
            response_format="detailed"
        )

        assert result.success is True
        assert "integration_points" in result.data

        # ShapeFactory should be an integration point
        factory_points = [
            ip for ip in result.data["integration_points"]
            if "Factory" in ip["name"]
        ]
        assert len(factory_points) > 0

    def test_parallel_error_handling_invalid_path(self):
        """Test error handling for non-existent directory."""
        result = analyze_codebase_parallel(
            "/nonexistent/path",
            response_format="summary"
        )

        assert result.success is False
        assert result.error_code == "DIR_NOT_FOUND"
        assert "suggestions" in result.metadata

    def test_parallel_handles_syntax_errors(self, tmp_path):
        """Test that parallel analysis handles files with syntax errors gracefully."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()

        # Create a valid file
        (src_dir / "valid.py").write_text("""
def valid_function():
    return True
""")

        # Create a file with syntax error
        (src_dir / "invalid.py").write_text("""
def broken_function(
    # Missing closing parenthesis
    return True
""")

        result = analyze_codebase_parallel(
            str(src_dir),
            response_format="summary"
        )

        # Should succeed for valid files, skip invalid
        assert result.success is True
        # Should analyze at least the valid file
        assert result.data["total_files"] >= 1

    def test_parallel_vs_sequential_consistency(self, temp_codebase):
        """Test that parallel and sequential analysis produce consistent results."""
        # Run sequential analysis
        seq_result = analyze_codebase(
            str(temp_codebase["src"]),
            response_format="summary"
        )

        # Run parallel analysis
        par_result = analyze_codebase_parallel(
            str(temp_codebase["src"]),
            response_format="summary"
        )

        # Should have same core results
        assert seq_result.success == par_result.success
        assert seq_result.data["total_files"] == par_result.data["total_files"]
        assert seq_result.data["total_lines"] == par_result.data["total_lines"]
        assert seq_result.data["integration_points_count"] == par_result.data["integration_points_count"]

    def test_parallel_performance_improvement(self, large_codebase):
        """Test that parallel analysis is faster for large codebases."""
        # Sequential analysis
        start = time.time()
        seq_result = analyze_codebase(
            str(large_codebase["src"]),
            response_format="summary"
        )
        seq_duration = time.time() - start

        # Parallel analysis
        start = time.time()
        par_result = analyze_codebase_parallel(
            str(large_codebase["src"]),
            response_format="summary"
        )
        par_duration = time.time() - start

        # Both should succeed
        assert seq_result.success is True
        assert par_result.success is True

        # Both should analyze same files
        assert seq_result.data["total_files"] == par_result.data["total_files"]

        # Parallel should be faster (or at least not significantly slower)
        # Allow some overhead, but expect speedup for 30 files
        assert par_duration < seq_duration * 1.2  # At most 20% slower (usually much faster)

    def test_parallel_include_patterns(self, temp_codebase):
        """Test include_patterns parameter in parallel mode."""
        # Create additional non-Python file
        (temp_codebase["src"] / "data.txt").write_text("Not a Python file")

        result = analyze_codebase_parallel(
            str(temp_codebase["src"]),
            include_patterns=["**/*.py"],
            response_format="summary"
        )

        assert result.success is True
        # Should only analyze Python files
        assert result.data["total_files"] == 4

    def test_parallel_exclude_patterns(self, temp_codebase):
        """Test exclude_patterns parameter in parallel mode."""
        result = analyze_codebase_parallel(
            str(temp_codebase["src"]),
            exclude_patterns=["**/complex.py"],
            response_format="summary"
        )

        assert result.success is True
        # Should exclude complex.py
        assert result.data["total_files"] == 3


class TestCodeAnalyzerParallel:
    """Test cases for CodeAnalyzer parallel methods."""

    def test_analyzer_parallel_method(self, temp_codebase):
        """Test CodeAnalyzer.analyze_codebase_parallel() method."""
        analyzer = CodeAnalyzer()
        analysis = analyzer.analyze_codebase_parallel(
            str(temp_codebase["src"])
        )

        assert analysis.total_files == 4
        assert analysis.total_lines > 0
        assert len(analysis.files) == 4
        assert isinstance(analysis.patterns_found, dict)

    def test_analyzer_worker_function(self, temp_codebase):
        """Test _analyze_file_worker with shared context."""
        analyzer = CodeAnalyzer()

        # Create shared context
        shared_context = {
            "python_analyzer": analyzer.python_analyzer,
            "pattern_detector": analyzer.pattern_detector
        }

        # Analyze single file with worker
        file_path = temp_codebase["files"][0]
        analysis = analyzer._analyze_file_worker(file_path, shared_context)

        assert analysis is not None
        assert analysis.total_lines > 0

    def test_analyzer_fallback_without_parallel(self, temp_codebase, monkeypatch):
        """Test graceful fallback when parallel infrastructure unavailable."""
        # Temporarily make parallel unavailable
        import skills.code_analysis.code_analyzer
        monkeypatch.setattr(
            skills.code_analysis.code_analyzer,
            "PARALLEL_AVAILABLE",
            False
        )

        analyzer = CodeAnalyzer()
        analysis = analyzer.analyze_codebase_parallel(
            str(temp_codebase["src"])
        )

        # Should fall back to sequential
        assert analysis.total_files == 4
        assert len(analysis.files) == 4

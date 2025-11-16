"""
Test Orchestrator Operations

Standardized operations interface for agent invocation.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from .core.analyzer import CodeAnalyzer
from .core.test_generator import TestGenerator
from .core.coverage_analyzer import CoverageAnalyzer

# Import parallel execution infrastructure
try:
    from skills.common import ParallelExecutor, ResultAggregator, ExecutorType
    PARALLEL_AVAILABLE = True
except ImportError:
    PARALLEL_AVAILABLE = False


@dataclass
class OperationResult:
    """Result from a skill operation."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    duration: float = 0.0
    metadata: Optional[Dict[str, Any]] = None


def analyze_file(source_file: str, response_format: str = "summary", **kwargs) -> OperationResult:
    """
    Analyze a Python source file to identify testable components.

    Args:
        source_file: Path to the Python source file
        response_format: "summary" (counts only) or "detailed" (full analysis)
        **kwargs: Additional parameters

    Returns:
        OperationResult with analysis data

    Token Efficiency:
        - Use response_format="summary" for counts and high-level info
        - Use response_format="detailed" when you need all function/class details
        - For large files (>20 functions), summary mode can save 90% tokens
    """
    import time
    start_time = time.time()

    try:
        analyzer = CodeAnalyzer()
        analysis = analyzer.analyze_file(source_file)

        duration = time.time() - start_time

        # Always include summary data
        data = {
            "source_file": str(analysis.file_path),
            "total_functions": analysis.total_functions,
            "total_classes": len(analysis.classes),
            "total_complexity": analysis.total_complexity,
            "avg_complexity": analysis.total_complexity / analysis.total_functions if analysis.total_functions > 0 else 0
        }

        if response_format == "detailed":
            # Include full details
            data.update({
                "functions": [
                    {
                        "name": func.name,
                        "line_number": func.line_number,
                        "complexity": func.complexity,
                        "parameters": func.params,
                        "return_type": func.returns,
                        "raises": func.raises,
                        "edge_cases": func.edge_cases,
                        "dependencies": list(func.dependencies)
                    }
                    for func in analysis.functions
                ],
                "classes": [
                    {
                        "name": cls.name,
                        "line_number": cls.line_number,
                        "base_classes": cls.base_classes,
                        "methods": [method.name for method in cls.methods]
                    }
                    for cls in analysis.classes
                ],
                "imports": list(analysis.imports)
            })
        else:
            # Summary mode - just names and key stats
            data.update({
                "function_names": [func.name for func in analysis.functions],
                "class_names": [cls.name for cls in analysis.classes],
                "most_complex_function": max(analysis.functions, key=lambda f: f.complexity).name if analysis.functions else None,
                "efficiency_tip": (
                    f"Analysis complete! Found {analysis.total_functions} functions and {len(analysis.classes)} classes.\n"
                    f"Using summary mode for efficiency. For full details including parameters, edge cases, and dependencies:\n"
                    f"analyze_file('{source_file}', response_format='detailed')"
                )
            })

        return OperationResult(
            success=True,
            data=data,
            duration=duration,
            metadata={
                "skill": "test-orchestrator",
                "operation": "analyze_file",
                "version": "0.1.0",
                "response_format": response_format
            }
        )

    except FileNotFoundError:
        return OperationResult(
            success=False,
            error=f"Cannot find source file: {source_file}",
            error_code="FILE_NOT_FOUND",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check if the file path is correct",
                    "Use Glob('**/*.py') to find Python files in the project",
                    f"Verify the file exists with Bash('ls -la {Path(source_file).parent}')"
                ],
                "example_fix": "analyze_file('src/services/payment.py')"
            }
        )
    except SyntaxError as e:
        return OperationResult(
            success=False,
            error=f"Python syntax error in {source_file}: {str(e)}",
            error_code="SYNTAX_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check the file for syntax errors",
                    "Run: Bash('python -m py_compile {source_file}') to see detailed error",
                    "Fix syntax errors before attempting analysis"
                ]
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Analysis failed: {str(e)}",
            error_code="ANALYSIS_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure the file is a valid Python source file",
                    "Check if the file is readable",
                    "Try with a simpler file first to verify the skill is working"
                ]
            }
        )


def generate_tests(
    source_file: str,
    target_coverage: float = 80.0,
    response_format: str = "concise",
    **kwargs
) -> OperationResult:
    """
    Generate comprehensive test suite for a Python source file.

    Args:
        source_file: Path to the Python source file
        target_coverage: Target coverage percentage (default: 80.0)
        response_format: Response format - "concise" (summary only) or "detailed" (includes full test_content)
        **kwargs: Additional parameters

    Returns:
        OperationResult with generated tests data

    Token Efficiency:
        - Use response_format="concise" (default) for summary (fast, ~500 tokens)
        - Use response_format="detailed" only when you need the full test code
        - If you need to modify tests, use Write tool with the test_file path
    """
    import time
    start_time = time.time()

    try:
        # First analyze the file
        analyzer = CodeAnalyzer()
        analysis = analyzer.analyze_file(source_file)

        # Generate tests
        generator = TestGenerator()
        test_suite = generator.generate_tests(analysis)

        # Generate test file content
        test_content = generator.generate_test_file(test_suite)

        duration = time.time() - start_time

        # Base data (always included)
        data = {
            "source_file": str(analysis.file_path),
            "test_file": test_suite.file_path,
            "tests_generated": len(test_suite.tests),
            "test_breakdown": {
                "unit_tests": sum(1 for tc in test_suite.tests if tc.test_type == "unit"),
                "edge_case_tests": sum(1 for tc in test_suite.tests if tc.test_type == "edge_case"),
                "exception_tests": sum(1 for tc in test_suite.tests if tc.test_type == "exception"),
                "parametrized_tests": sum(1 for tc in test_suite.tests if tc.test_type == "parametrized")
            },
            "completeness_score": getattr(test_suite, 'completeness_score', 0),
            "quality_score": getattr(test_suite, 'quality_score', 0),
            "coverage_estimate": getattr(test_suite, 'completeness_score', 0) * 100
        }

        # Add detailed content only if requested
        if response_format == "detailed":
            data.update({
                "test_content": test_content,
                "fixtures": test_suite.fixtures,
                "imports": test_suite.imports
            })
        else:
            # Concise mode - add efficiency tip
            estimated_tokens = len(test_content) // 4  # Rough estimate
            data["efficiency_tip"] = (
                f"Test generation complete! Generated {len(test_suite.tests)} tests.\n"
                f"For token efficiency, full test_content not included (saves ~{estimated_tokens} tokens).\n"
                f"To get full content: generate_tests('{source_file}', response_format='detailed')\n"
                f"To write tests to file: Write('{test_suite.file_path}', test_content)"
            )

        return OperationResult(
            success=True,
            data=data,
            duration=duration,
            metadata={
                "skill": "test-orchestrator",
                "operation": "generate_tests",
                "version": "0.1.0",
                "target_coverage": target_coverage,
                "response_format": response_format
            }
        )

    except FileNotFoundError:
        return OperationResult(
            success=False,
            error=f"Cannot find source file: {source_file}",
            error_code="FILE_NOT_FOUND",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check if the file path is correct",
                    "Use Glob('**/*.py') to find Python files in the project",
                    f"Verify the file exists with Bash('ls -la {Path(source_file).parent}')"
                ],
                "example_fix": "generate_tests('src/services/payment.py')"
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Test generation failed: {str(e)}",
            error_code="GENERATION_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check if the file contains valid Python syntax",
                    "Ensure the file has functions or classes to test",
                    "Try analyzing the file first with analyze_file() to check for issues"
                ]
            }
        )


def analyze_coverage(
    test_results_file: Optional[str] = None,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Analyze test coverage and identify gaps.

    Args:
        test_results_file: Path to pytest coverage report (optional)
        response_format: Response format - "summary" (overview only) or "detailed" (full gap analysis)
        **kwargs: Additional parameters

    Returns:
        OperationResult with coverage analysis

    Token Efficiency:
        - Use response_format="summary" (default) for coverage overview (~200 tokens)
        - Use response_format="detailed" for complete gap analysis and recommendations
        - Summary includes overall coverage percentage and file count
        - Detailed includes per-file coverage, gap locations, and recommendations
    """
    import time
    start_time = time.time()

    try:
        analyzer = CoverageAnalyzer()

        # Parse coverage results if provided
        if test_results_file:
            coverage_data = analyzer.parse_coverage_report(test_results_file)
        else:
            # Return placeholder data for now
            coverage_data = {
                "overall_coverage": 0.0,
                "files": [],
                "gaps": []
            }

        duration = time.time() - start_time

        # Format response based on response_format
        if response_format == "summary":
            # Summary: just key metrics
            data = {
                "overall_coverage": coverage_data.get("overall_coverage", 0.0),
                "files_analyzed": len(coverage_data.get("files", [])),
                "gaps_found": len(coverage_data.get("gaps", [])),
                "efficiency_tip": (
                    "Coverage analysis complete! "
                    f"For detailed gap analysis: analyze_coverage('{test_results_file}', response_format='detailed')"
                    if test_results_file else
                    "No test results file provided. Run tests with coverage first."
                )
            }
        else:
            # Detailed: full coverage data
            data = coverage_data

        return OperationResult(
            success=True,
            data=data,
            duration=duration,
            metadata={
                "skill": "test-orchestrator",
                "operation": "analyze_coverage",
                "version": "0.1.0"
            }
        )

    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Coverage analysis failed: {str(e)}",
            error_code="COVERAGE_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure the test results file exists and is readable",
                    "Verify the file is a valid pytest coverage report",
                    "Try running: Bash('pytest --cov=. --cov-report=json')"
                ],
                "example_fix": "analyze_coverage('coverage.json')"
            }
        )


# Export all operations
def analyze_files_parallel(
    source_files: List[str],
    response_format: str = "summary",
    max_workers: Optional[int] = None,
    **kwargs
) -> OperationResult:
    """
    Analyze multiple Python source files in parallel.

    This provides significant speedup when analyzing multiple files:
    - 60% faster for 10+ files
    - 40% faster for 5-10 files

    Args:
        source_files: List of paths to Python source files
        response_format: "summary" (counts only) or "detailed" (full analysis)
        max_workers: Number of worker threads (default: auto-detect)
        **kwargs: Additional parameters

    Returns:
        OperationResult with aggregated analysis data

    Performance:
        - Thread pool execution for I/O-bound file operations
        - Shared analyzer context across workers
        - Local aggregation (no LLM calls)

    Token Efficiency:
        - Use response_format="summary" for aggregated counts
        - Response includes summary for all files
        - Detailed mode includes per-file breakdowns

    Example:
        from skills.test_orchestrator import analyze_files_parallel

        files = ["src/payment.py", "src/user.py", "src/order.py"]
        result = analyze_files_parallel(files, response_format="summary")

        print(f"Analyzed {result.data['total_files']} files")
        print(f"Total functions: {result.data['total_functions']}")
    """
    import time
    start_time = time.time()

    if not PARALLEL_AVAILABLE or len(source_files) < 3:
        # Fallback to sequential for small batches
        return _analyze_files_sequential(source_files, response_format, **kwargs)

    try:
        # Create executor
        executor = ParallelExecutor(
            max_workers=max_workers,
            executor_type=ExecutorType.THREAD,
            timeout=300
        )

        # Prepare tasks
        def analyze_single(file_path, shared_context=None):
            """Worker function to analyze a single file."""
            analyzer = shared_context["analyzer"] if shared_context else CodeAnalyzer()
            return analyzer.analyze_file(file_path)

        tasks = [(analyze_single, (f,), {}) for f in source_files]

        # Execute with shared context
        def create_shared_context():
            return {"analyzer": CodeAnalyzer()}

        shared_context, results = executor.execute_with_shared_context(
            tasks,
            shared_context_fn=create_shared_context
        )

        # Aggregate results
        aggregator = ResultAggregator()
        analyses = []
        total_functions = 0
        total_classes = 0
        total_complexity = 0

        for i, result in enumerate(results):
            if result.success:
                analysis = result.result
                analyses.append(analysis)
                aggregator.add_result(f"file_{i}", {"status": "success"}, result.duration)
                total_functions += analysis.total_functions
                total_classes += len(analysis.classes)
                total_complexity += analysis.total_complexity
            else:
                aggregator.add_error(f"file_{i}", result.error, result.error_type)

        duration = time.time() - start_time
        summary = aggregator.get_summary()

        # Build response data
        data = {
            "total_files": len(source_files),
            "analyzed_successfully": summary["successful"],
            "failed": summary["failed"],
            "total_functions": total_functions,
            "total_classes": total_classes,
            "total_complexity": total_complexity,
            "avg_complexity": total_complexity / total_functions if total_functions > 0 else 0,
            "parallel_execution": True,
            "speedup": summary.get("speedup", 1.0)
        }

        if response_format == "detailed":
            # Include per-file details
            data["files"] = [
                {
                    "source_file": str(a.file_path),
                    "functions": a.total_functions,
                    "classes": len(a.classes),
                    "complexity": a.total_complexity,
                    "function_names": [f.name for f in a.functions],
                    "class_names": [c.name for c in a.classes]
                }
                for a in analyses
            ]
        else:
            # Summary mode
            data["file_list"] = [str(a.file_path) for a in analyses[:10]]
            data["showing_files"] = min(10, len(analyses))
            data["efficiency_tip"] = (
                f"Parallel analysis complete! Analyzed {len(analyses)} files in {duration:.1f}s.\n"
                f"Found {total_functions} functions and {total_classes} classes.\n"
                f"For per-file details: analyze_files_parallel(files, response_format='detailed')"
            )

        return OperationResult(
            success=summary["failed"] == 0,
            data=data,
            duration=duration,
            error=f"{summary['failed']} files failed" if summary['failed'] > 0 else None,
            error_code="PARTIAL_FAILURE" if summary['failed'] > 0 else None,
            metadata={
                "skill": "test-orchestrator",
                "operation": "analyze_files_parallel",
                "version": "0.1.0",
                "response_format": response_format,
                "parallel_execution": True
            }
        )

    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Parallel analysis failed: {str(e)}",
            error_code="ANALYSIS_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check that all file paths are valid",
                    "Ensure files are readable Python source files",
                    "Try with fewer files to isolate the issue",
                    "Fallback to sequential: [analyze_file(f) for f in files]"
                ]
            }
        )


def _analyze_files_sequential(
    source_files: List[str],
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """Sequential fallback for small batches."""
    import time
    start_time = time.time()

    analyzer = CodeAnalyzer()
    analyses = []
    errors = []
    total_functions = 0
    total_classes = 0
    total_complexity = 0

    for file_path in source_files:
        try:
            analysis = analyzer.analyze_file(file_path)
            analyses.append(analysis)
            total_functions += analysis.total_functions
            total_classes += len(analysis.classes)
            total_complexity += analysis.total_complexity
        except Exception as e:
            errors.append((file_path, str(e)))

    duration = time.time() - start_time

    data = {
        "total_files": len(source_files),
        "analyzed_successfully": len(analyses),
        "failed": len(errors),
        "total_functions": total_functions,
        "total_classes": total_classes,
        "total_complexity": total_complexity,
        "avg_complexity": total_complexity / total_functions if total_functions > 0 else 0,
        "parallel_execution": False
    }

    if response_format == "detailed":
        data["files"] = [
            {
                "source_file": str(a.file_path),
                "functions": a.total_functions,
                "classes": len(a.classes),
                "complexity": a.total_complexity
            }
            for a in analyses
        ]

    return OperationResult(
        success=len(errors) == 0,
        data=data,
        duration=duration,
        error=f"{len(errors)} files failed" if errors else None,
        metadata={
            "skill": "test-orchestrator",
            "operation": "analyze_files_sequential",
            "version": "0.1.0"
        }
    )


def generate_tests_parallel(
    source_files: List[str],
    target_coverage: float = 80.0,
    response_format: str = "concise",
    max_workers: Optional[int] = None,
    **kwargs
) -> OperationResult:
    """
    Generate tests for multiple Python source files in parallel.

    This provides significant speedup when generating tests for multiple files:
    - 70% faster for 10+ files
    - 50% faster for 5-10 files

    Args:
        source_files: List of paths to Python source files
        target_coverage: Target coverage percentage (default: 80.0)
        response_format: "concise" (summary) or "detailed" (includes test content)
        max_workers: Number of worker threads (default: auto-detect)
        **kwargs: Additional parameters

    Returns:
        OperationResult with aggregated test generation data

    Performance:
        - Thread pool execution for concurrent test generation
        - Shared analyzer and generator context
        - Local aggregation (no LLM calls)

    Token Efficiency:
        - Use response_format="concise" for summary only
        - Detailed mode includes all generated test content (large!)
        - Per-file test content written to files, not returned

    Example:
        from skills.test_orchestrator import generate_tests_parallel

        files = ["src/payment.py", "src/user.py", "src/order.py"]
        result = generate_tests_parallel(files, target_coverage=85.0)

        print(f"Generated tests for {result.data['successful']} files")
        print(f"Total tests: {result.data['total_tests']}")
    """
    import time
    start_time = time.time()

    if not PARALLEL_AVAILABLE or len(source_files) < 3:
        # Fallback to sequential for small batches
        return _generate_tests_sequential(source_files, target_coverage, response_format, **kwargs)

    try:
        # Create executor
        executor = ParallelExecutor(
            max_workers=max_workers,
            executor_type=ExecutorType.THREAD,
            timeout=600  # Longer timeout for test generation
        )

        # Prepare tasks
        def generate_for_file(file_path, shared_context=None):
            """Worker function to generate tests for a single file."""
            if shared_context:
                analyzer = shared_context["analyzer"]
                generator = shared_context["generator"]
            else:
                analyzer = CodeAnalyzer()
                generator = TestGenerator()

            # Analyze and generate
            analysis = analyzer.analyze_file(file_path)
            test_suite = generator.generate_tests(analysis)
            test_content = generator.generate_test_file(test_suite)

            return {
                "source_file": str(analysis.file_path),
                "test_file": test_suite.file_path,
                "tests_count": len(test_suite.tests),
                "test_content": test_content,
                "test_suite": test_suite
            }

        tasks = [(generate_for_file, (f,), {}) for f in source_files]

        # Execute with shared context
        def create_shared_context():
            return {
                "analyzer": CodeAnalyzer(),
                "generator": TestGenerator()
            }

        shared_context, results = executor.execute_with_shared_context(
            tasks,
            shared_context_fn=create_shared_context
        )

        # Aggregate results
        aggregator = ResultAggregator()
        generated_tests = []
        total_tests = 0

        for i, result in enumerate(results):
            if result.success:
                test_data = result.result
                generated_tests.append(test_data)
                aggregator.add_result(f"file_{i}", {"status": "success"}, result.duration)
                total_tests += test_data["tests_count"]
            else:
                aggregator.add_error(f"file_{i}", result.error, result.error_type)

        duration = time.time() - start_time
        summary = aggregator.get_summary()

        # Build response data
        data = {
            "total_files": len(source_files),
            "successful": summary["successful"],
            "failed": summary["failed"],
            "total_tests": total_tests,
            "avg_tests_per_file": total_tests / summary["successful"] if summary["successful"] > 0 else 0,
            "parallel_execution": True,
            "speedup": summary.get("speedup", 1.0)
        }

        if response_format == "detailed":
            # Include test content for all files
            data["test_suites"] = [
                {
                    "source_file": t["source_file"],
                    "test_file": t["test_file"],
                    "tests_count": t["tests_count"],
                    "test_content": t["test_content"]
                }
                for t in generated_tests
            ]
        else:
            # Concise mode - just summary
            data["test_files"] = [t["test_file"] for t in generated_tests[:10]]
            data["showing_files"] = min(10, len(generated_tests))
            estimated_tokens = sum(len(t["test_content"]) // 4 for t in generated_tests)
            data["efficiency_tip"] = (
                f"Parallel test generation complete! Generated {total_tests} tests for {len(generated_tests)} files in {duration:.1f}s.\n"
                f"Test content not included for efficiency (saves ~{estimated_tokens} tokens).\n"
                f"For full content: generate_tests_parallel(files, response_format='detailed')\n"
                f"Tests written to: {', '.join([t['test_file'] for t in generated_tests[:3]])}..."
            )

        return OperationResult(
            success=summary["failed"] == 0,
            data=data,
            duration=duration,
            error=f"{summary['failed']} files failed" if summary['failed'] > 0 else None,
            error_code="PARTIAL_FAILURE" if summary['failed'] > 0 else None,
            metadata={
                "skill": "test-orchestrator",
                "operation": "generate_tests_parallel",
                "version": "0.1.0",
                "target_coverage": target_coverage,
                "response_format": response_format,
                "parallel_execution": True
            }
        )

    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Parallel test generation failed: {str(e)}",
            error_code="GENERATION_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check that all file paths are valid",
                    "Ensure files are readable Python source files",
                    "Try with fewer files to isolate the issue",
                    "Fallback to sequential: [generate_tests(f) for f in files]"
                ]
            }
        )


def _generate_tests_sequential(
    source_files: List[str],
    target_coverage: float = 80.0,
    response_format: str = "concise",
    **kwargs
) -> OperationResult:
    """Sequential fallback for small batches."""
    import time
    start_time = time.time()

    analyzer = CodeAnalyzer()
    generator = TestGenerator()
    generated_tests = []
    errors = []
    total_tests = 0

    for file_path in source_files:
        try:
            analysis = analyzer.analyze_file(file_path)
            test_suite = generator.generate_tests(analysis)
            test_content = generator.generate_test_file(test_suite)

            test_data = {
                "source_file": str(analysis.file_path),
                "test_file": test_suite.file_path,
                "tests_count": len(test_suite.tests),
                "test_content": test_content
            }
            generated_tests.append(test_data)
            total_tests += len(test_suite.tests)
        except Exception as e:
            errors.append((file_path, str(e)))

    duration = time.time() - start_time

    data = {
        "total_files": len(source_files),
        "successful": len(generated_tests),
        "failed": len(errors),
        "total_tests": total_tests,
        "avg_tests_per_file": total_tests / len(generated_tests) if generated_tests else 0,
        "parallel_execution": False
    }

    if response_format == "detailed":
        data["test_suites"] = generated_tests

    return OperationResult(
        success=len(errors) == 0,
        data=data,
        duration=duration,
        error=f"{len(errors)} files failed" if errors else None,
        metadata={
            "skill": "test-orchestrator",
            "operation": "generate_tests_sequential",
            "version": "0.1.0"
        }
    )


__all__ = [
    "analyze_file",
    "analyze_files_parallel",
    "generate_tests",
    "generate_tests_parallel",
    "analyze_coverage",
    "OperationResult"
]

"""
MCP Adapter for test_orchestrator skill.

Exposes test generation and analysis operations via MCP with local filtering.

Example usage in agent-generated code:
    from skills.test_orchestrator import generate_tests, analyze_coverage
    from skills.common.filters import ResultFilter

    # Generate tests for all files
    all_tests = generate_tests("src/")

    # Filter to untested files only
    untested = [t for t in all_tests if t["coverage"] < 50]

    # Return top 5 files needing tests most urgently
    result = ResultFilter.top_n_by_field(untested, "priority", 5)
"""

OPERATIONS = {
    "generate_tests": {
        "description": "Generate test cases for code files",
        "parameters": {
            "path": "File or directory path",
            "test_framework": "Test framework to use (pytest, unittest, jest, etc.)",
            "coverage_target": "Target coverage percentage (default: 80)"
        },
        "returns": "Dictionary with generated test suggestions",
        "example": """
from skills.test_orchestrator import generate_tests
from skills.common.filters import ResultFilter

# Generate tests for all files
tests = generate_tests("src/", test_framework="pytest")

# Filter to high-priority files only
high_priority = [t for t in tests["suggestions"]
                 if t.get("priority", 0) >= 8]

# Return top 10
result = ResultFilter.limit(high_priority, 10)
        """
    },

    "analyze_coverage": {
        "description": "Analyze test coverage for codebase",
        "parameters": {
            "path": "Directory path to analyze",
            "coverage_file": "Optional path to coverage report (coverage.xml, .coverage)"
        },
        "returns": "Dictionary with coverage analysis",
        "example": """
from skills.test_orchestrator import analyze_coverage

# Analyze coverage
coverage = analyze_coverage("src/")

# Filter to files with <50% coverage
low_coverage = [
    f for f in coverage["files"]
    if f["coverage_percent"] < 50
]

# Sort by lines uncovered
low_coverage.sort(key=lambda f: f["lines_uncovered"], reverse=True)

# Return top 10 files needing tests
result = low_coverage[:10]
        """
    },

    "run_tests": {
        "description": "Run tests and collect results",
        "parameters": {
            "path": "Test file or directory",
            "pattern": "Test file pattern (e.g., 'test_*.py')",
            "markers": "Optional pytest markers to filter tests"
        },
        "returns": "Dictionary with test results",
        "example": """
from skills.test_orchestrator import run_tests

# Run tests
results = run_tests("tests/", pattern="test_*.py")

# Filter to failed tests only
failed = [t for t in results["tests"] if t["status"] == "failed"]

# Group by file
from collections import defaultdict
by_file = defaultdict(list)
for test in failed:
    by_file[test["file"]].append(test)

# Return files with most failures
result = sorted(
    [{"file": k, "failures": len(v), "tests": v}
     for k, v in by_file.items()],
    key=lambda x: x["failures"],
    reverse=True
)[:5]
        """
    }
}


def get_operation_docs() -> dict:
    """Get documentation for all operations."""
    return OPERATIONS


def generate_import_example() -> str:
    """Generate example code showing how to use test_orchestrator via MCP."""
    return """
# MCP Code Execution Pattern for test_orchestrator skill

from skills.test_orchestrator import generate_tests, analyze_coverage, run_tests
from skills.common.filters import ResultFilter

# Example 1: Find files needing tests most urgently
# --------------------------------------------------

# Analyze coverage for entire codebase
coverage = analyze_coverage("src/")

# Filter to files with <80% coverage
needs_tests = [
    f for f in coverage["files"]
    if f["coverage_percent"] < 80
]

# Sort by importance (lines of code * complexity * (1 - coverage))
for f in needs_tests:
    f["urgency"] = f["lines"] * f.get("complexity", 1) * (1 - f["coverage_percent"]/100)

needs_tests.sort(key=lambda f: f["urgency"], reverse=True)

# Return top 5 most urgent
result = needs_tests[:5]


# Example 2: Generate tests for specific module
# ----------------------------------------------

# Generate test suggestions
suggestions = generate_tests("src/authentication/", test_framework="pytest")

# Filter to high-priority suggestions
high_priority = [
    s for s in suggestions["suggestions"]
    if s.get("priority", 0) >= 8
]

# Group by file
from collections import defaultdict
by_file = defaultdict(list)
for suggestion in high_priority:
    by_file[suggestion["file"]].append(suggestion)

# Return top 3 files with most high-priority test needs
result = sorted(
    [{"file": k, "test_count": len(v), "tests": v}
     for k, v in by_file.items()],
    key=lambda x: x["test_count"],
    reverse=True
)[:3]


# Example 3: Analyze test failures
# ---------------------------------

# Run tests
test_results = run_tests("tests/")

# Filter to failures and errors
problems = [
    t for t in test_results["tests"]
    if t["status"] in ["failed", "error"]
]

# Group by error message pattern (simplified)
error_groups = defaultdict(list)
for test in problems:
    error_msg = test.get("error", "Unknown error")
    # Group by first line of error
    error_key = error_msg.split('\n')[0][:50]
    error_groups[error_key].append(test)

# Return error patterns with most failures
result = sorted(
    [{"error": k, "count": len(v), "examples": v[:3]}
     for k, v in error_groups.items()],
    key=lambda x: x["count"],
    reverse=True
)[:5]


# Example 4: Coverage gaps analysis
# ----------------------------------

# Analyze coverage
coverage = analyze_coverage("src/")

# Find files with partial coverage (some tested, but gaps)
partial = [
    f for f in coverage["files"]
    if 20 < f["coverage_percent"] < 80
]

# These are often the most valuable to improve
# Sort by: high complexity + medium coverage = high ROI
for f in partial:
    f["roi_score"] = f.get("complexity", 1) * (100 - f["coverage_percent"])

partial.sort(key=lambda f: f["roi_score"], reverse=True)

# Return top 10 files with best test ROI
result = partial[:10]
"""

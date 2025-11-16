"""
MCP Adapter for code_analysis skill.

Exposes code analysis operations via MCP with local filtering.
Enables 98.7% token reduction by processing data locally.

Example usage in agent-generated code:
    from skills.code_analysis import analyze_codebase, analyze_file
    from skills.common.filters import ResultFilter

    # Analyze entire codebase (could be 10,000 files)
    files = analyze_codebase("src/")

    # Filter locally - only navigation-related
    nav_files = ResultFilter.search(files, "navigation", ["path", "name"])

    # Get top 5 most complex
    result = ResultFilter.top_n_by_field(nav_files, "complexity", 5)

    # Returns only 5 files (~500 tokens) instead of 10,000 (~150,000 tokens)!
"""

# This adapter file documents the available operations from code_analysis skill.
# The actual imports happen in the sandboxed code execution environment.

OPERATIONS = {
    "analyze_codebase": {
        "description": "Analyze entire codebase for complexity, dependencies, and structure",
        "parameters": {
            "path": "Directory path to analyze",
            "file_types": "Optional list of file extensions to include (e.g., ['.py', '.js'])",
            "exclude_patterns": "Optional list of patterns to exclude (e.g., ['node_modules', '__pycache__'])"
        },
        "returns": "Dictionary with 'files' list containing analysis for each file",
        "example": """
from skills.code_analysis import analyze_codebase
from skills.common.filters import ResultFilter

# Analyze Python files only
result = analyze_codebase("src/", file_types=[".py"])

# Filter to high-complexity files
complex_files = ResultFilter.filter_by_threshold(
    result["files"],
    "complexity",
    min_value=10
)

# Return top 10 most complex
top_complex = ResultFilter.top_n_by_field(complex_files, "complexity", 10)
        """
    },

    "analyze_file": {
        "description": "Analyze a single file for complexity, functions, classes, imports",
        "parameters": {
            "file_path": "Path to file to analyze"
        },
        "returns": "Dictionary with file analysis details",
        "example": """
from skills.code_analysis import analyze_file

# Analyze specific file
result = analyze_file("src/main.py")

# Access analysis
print(f"Complexity: {result['complexity']}")
print(f"Functions: {len(result['functions'])}")
print(f"Classes: {len(result['classes'])}")
        """
    },

    "generate_dependency_graph": {
        "description": "Generate dependency graph for codebase",
        "parameters": {
            "path": "Directory path to analyze"
        },
        "returns": "Dictionary with nodes and edges for dependency graph",
        "example": """
from skills.code_analysis import generate_dependency_graph

# Generate graph
graph = generate_dependency_graph("src/")

# Filter to show only core modules
core_nodes = [n for n in graph["nodes"] if "core" in n["path"]]
core_edges = [e for e in graph["edges"]
              if e["source"] in [n["id"] for n in core_nodes]]

result = {"nodes": core_nodes, "edges": core_edges}
        """
    }
}


def get_operation_docs() -> dict:
    """Get documentation for all operations."""
    return OPERATIONS


def generate_import_example() -> str:
    """Generate example code showing how to use code_analysis via MCP."""
    return """
# MCP Code Execution Pattern for code_analysis skill

from skills.code_analysis import analyze_codebase, analyze_file
from skills.common.filters import ResultFilter

# Example 1: Find navigation-related files (98.7% token reduction)
# -----------------------------------------------------------------

# Analyze entire codebase (could be 10,000 files = 150,000 tokens)
all_files = analyze_codebase("src/")

# Filter locally to navigation-related files
nav_files = ResultFilter.search(all_files["files"], "navigation", ["path", "name"])

# Get top 5 most complex
top_nav = ResultFilter.top_n_by_field(nav_files, "complexity", 5)

# Result: Only 5 files returned (~500 tokens) = 99.7% reduction!


# Example 2: Find high-complexity files for refactoring
# ------------------------------------------------------

# Analyze codebase
all_files = analyze_codebase("src/", file_types=[".py"])

# Filter to files with complexity > 15
complex_files = [
    f for f in all_files["files"]
    if f.get("complexity", 0) > 15
]

# Sort by complexity
complex_files.sort(key=lambda f: f["complexity"], reverse=True)

# Return top 10
result = complex_files[:10]


# Example 3: Analyze specific files in detail
# --------------------------------------------

# First, find files of interest
files = analyze_codebase("src/skills/")
auth_files = ResultFilter.search(files["files"], "auth", ["path"])

# Then analyze top 3 in detail
detailed = []
for file_info in auth_files[:3]:
    detail = analyze_file(file_info["path"])
    detailed.append(detail)

result = detailed


# Example 4: Dependency analysis
# -------------------------------

from skills.code_analysis import generate_dependency_graph

# Generate full graph
graph = generate_dependency_graph("src/")

# Filter to show only circular dependencies
circular = [
    edge for edge in graph["edges"]
    if edge.get("circular", False)
]

result = {
    "circular_count": len(circular),
    "circular_dependencies": circular[:10]  # Top 10 only
}
"""

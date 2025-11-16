"""
Data models for code analysis.

Pydantic models representing code structure, metrics, and analysis results.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class NodeType(str, Enum):
    """Code entity types"""

    CLASS = "class"
    FUNCTION = "function"
    METHOD = "method"
    ASYNC_FUNCTION = "async_function"
    ASYNC_METHOD = "async_method"


class DesignPattern(str, Enum):
    """Detected design patterns"""

    SINGLETON = "singleton"
    FACTORY = "factory"
    STRATEGY = "strategy"
    DECORATOR = "decorator"
    OBSERVER = "observer"


class CodeSmell(str, Enum):
    """Common code smells"""

    LONG_FUNCTION = "long_function"
    TOO_MANY_PARAMETERS = "too_many_parameters"
    COMPLEX_FUNCTION = "complex_function"
    DEEP_NESTING = "deep_nesting"
    MUTABLE_DEFAULT_ARG = "mutable_default_arg"  # Python-specific


class ComplexityMetrics(BaseModel):
    """Code complexity metrics"""

    cyclomatic_complexity: int = Field(ge=1, description="McCabe complexity")
    lines_of_code: int = Field(ge=0)
    max_nesting_depth: int = Field(ge=0)
    num_branches: int = Field(ge=0, description="Number of if/for/while statements")


class CodeEntity(BaseModel):
    """Represents a code entity (class, function, etc.)"""

    name: str
    entity_type: NodeType
    file_path: str
    line_start: int
    line_end: int
    docstring: Optional[str] = None
    decorators: List[str] = Field(default_factory=list)
    parameters: List[str] = Field(default_factory=list)
    complexity: Optional[ComplexityMetrics] = None
    calls: List[str] = Field(
        default_factory=list, description="Functions/methods called"
    )
    is_public: bool = True


class FileAnalysis(BaseModel):
    """Analysis of a single Python file"""

    file_path: str
    classes: List[CodeEntity] = Field(default_factory=list)
    functions: List[CodeEntity] = Field(default_factory=list)
    imports: List[str] = Field(default_factory=list)
    from_imports: Dict[str, List[str]] = Field(
        default_factory=dict, description="module -> [names]"
    )
    patterns: List[DesignPattern] = Field(default_factory=list)
    smells: List[Dict[str, Any]] = Field(default_factory=list)
    total_lines: int = 0
    code_lines: int = 0
    comment_lines: int = 0
    is_test_file: bool = False
    is_init_file: bool = False


class DependencyEdge(BaseModel):
    """A dependency relationship"""

    from_file: str
    to_file: str
    import_type: str  # "import" or "from_import"
    imported_names: List[str] = Field(default_factory=list)


class DependencyGraph(BaseModel):
    """Import dependency graph"""

    edges: List[DependencyEdge] = Field(default_factory=list)

    def get_dependencies(self, file_path: str) -> List[str]:
        """Get all files this file depends on"""
        return [edge.to_file for edge in self.edges if edge.from_file == file_path]

    def get_dependents(self, file_path: str) -> List[str]:
        """Get all files that depend on this file"""
        return [edge.from_file for edge in self.edges if edge.to_file == file_path]

    def find_circular_dependencies(self) -> List[List[str]]:
        """Detect circular dependency chains"""
        cycles = []
        visited = set()

        def dfs(node, path):
            if node in path:
                cycle_start = path.index(node)
                cycle = path[cycle_start:]
                if cycle not in cycles and len(cycle) > 1:
                    cycles.append(cycle)
                return

            if node in visited:
                return

            visited.add(node)
            path.append(node)

            for dep in self.get_dependencies(node):
                dfs(dep, path.copy())

        all_files = set(e.from_file for e in self.edges) | set(
            e.to_file for e in self.edges
        )
        for file in all_files:
            dfs(file, [])

        return cycles


class IntegrationPoint(BaseModel):
    """Identified integration point"""

    name: str
    file_path: str
    line_number: int
    entity_type: str  # "class", "function", "method"
    reason: str  # Why this is a good integration point
    pattern: Optional[str] = None  # Related pattern if detected
    example_usage: Optional[str] = None


class CodebaseAnalysis(BaseModel):
    """Complete codebase analysis"""

    root_path: str
    total_files: int = 0
    total_lines: int = 0
    files: List[FileAnalysis] = Field(default_factory=list)
    dependency_graph: DependencyGraph = Field(default_factory=DependencyGraph)
    patterns_found: Dict[DesignPattern, List[str]] = Field(
        default_factory=dict, description="Pattern -> [file_paths]"
    )
    integration_points: List[IntegrationPoint] = Field(default_factory=list)
    entry_points: List[str] = Field(default_factory=list)

    def find_related_files(self, file_path: str, max_depth: int = 2) -> List[str]:
        """Find files related through dependencies (BFS)"""
        if max_depth <= 0:
            return []

        visited = {file_path}
        queue = [(file_path, 0)]
        related = []

        while queue:
            current, depth = queue.pop(0)

            if depth >= max_depth:
                continue

            # Get dependencies and dependents
            deps = self.dependency_graph.get_dependencies(current)
            dependents = self.dependency_graph.get_dependents(current)

            for next_file in deps + dependents:
                if next_file not in visited:
                    visited.add(next_file)
                    related.append(next_file)
                    queue.append((next_file, depth + 1))

        return related

    def suggest_integration_for_feature(
        self, feature_description: str
    ) -> List[IntegrationPoint]:
        """Suggest where to integrate a new feature"""
        # Simple keyword matching
        keywords = feature_description.lower().split()
        suggestions = []

        for point in self.integration_points:
            # Check if integration point matches feature keywords
            point_text = (point.name + " " + point.reason).lower()
            if any(keyword in point_text for keyword in keywords):
                suggestions.append(point)

        return suggestions[:5]  # Top 5

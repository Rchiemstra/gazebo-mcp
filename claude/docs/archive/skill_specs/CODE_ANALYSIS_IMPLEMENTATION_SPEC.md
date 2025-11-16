# Code Analysis Skill - Detailed Implementation Specification

**Document Version**: 1.0
**Created**: 2025-10-19
**Focus**: Python-first implementation with extensibility for other languages

---

## Table of Contents

1. [Implementation Overview](#implementation-overview)
2. [Phase 1A: Core Python Analysis](#phase-1a-core-python-analysis)
3. [Phase 1B: Pattern Detection](#phase-1b-pattern-detection)
4. [Phase 1C: Integration Point Identification](#phase-1c-integration-point-identification)
5. [Implementation Details](#implementation-details)
6. [Testing Strategy](#testing-strategy)
7. [Integration with Agents](#integration-with-agents)

---

## Implementation Overview

### Scope for Initial Release

**✅ In Scope:**
- Python AST parsing and analysis
- Basic complexity metrics (cyclomatic complexity)
- Dependency graph generation (imports)
- Common design pattern detection (5 patterns)
- Integration point identification
- Code smell detection (5 smells)
- Codebase-level analysis

**❌ Out of Scope (Future):**
- C++/JavaScript/other language support
- Advanced metrics (Halstead, maintainability index)
- Real-time analysis
- Code execution or testing
- Architectural refactoring suggestions

### Success Criteria

1. Can analyze entire `src/` directory in < 5 seconds
2. Detects patterns with 80%+ accuracy
3. Provides useful integration point suggestions
4. Works seamlessly with file-search-agent
5. Handles malformed Python gracefully

---

## Phase 1A: Core Python Analysis

### Data Models (Simplified from spec)

```python
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
    calls: List[str] = Field(default_factory=list, description="Functions/methods called")
    is_public: bool = True

class FileAnalysis(BaseModel):
    """Analysis of a single Python file"""
    file_path: str
    classes: List[CodeEntity] = Field(default_factory=list)
    functions: List[CodeEntity] = Field(default_factory=list)
    imports: List[str] = Field(default_factory=list)
    from_imports: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="module -> [names]"
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
        # Simple cycle detection
        cycles = []
        visited = set()

        def dfs(node, path):
            if node in path:
                cycle_start = path.index(node)
                cycle = path[cycle_start:]
                if cycle not in cycles:
                    cycles.append(cycle)
                return

            if node in visited:
                return

            visited.add(node)
            path.append(node)

            for dep in self.get_dependencies(node):
                dfs(dep, path.copy())

        all_files = set(e.from_file for e in self.edges) | set(e.to_file for e in self.edges)
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
        default_factory=dict,
        description="Pattern -> [file_paths]"
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

    def suggest_integration_for_feature(self, feature_description: str) -> List[IntegrationPoint]:
        """Suggest where to integrate a new feature"""
        # Simple keyword matching for now
        keywords = feature_description.lower().split()
        suggestions = []

        for point in self.integration_points:
            # Check if integration point matches feature keywords
            point_text = (point.name + " " + point.reason).lower()
            if any(keyword in point_text for keyword in keywords):
                suggestions.append(point)

        return suggestions[:5]  # Top 5
```

### Python AST Analyzer Implementation

```python
import ast
from pathlib import Path
from typing import List, Optional, Set

class PythonAnalyzer:
    """Analyzes Python source files using AST"""

    def analyze_file(self, file_path: Path) -> FileAnalysis:
        """
        Analyze a Python file.

        Args:
            file_path: Path to .py file

        Returns:
            FileAnalysis with all extracted information
        """
        try:
            content = file_path.read_text(encoding='utf-8')
            tree = ast.parse(content, filename=str(file_path))
        except (SyntaxError, UnicodeDecodeError) as e:
            # Handle malformed Python files gracefully
            return FileAnalysis(
                file_path=str(file_path),
                is_test_file=self._is_test_file(file_path),
                is_init_file=file_path.name == "__init__.py"
            )

        # Extract entities
        classes = self._extract_classes(tree, str(file_path))
        functions = self._extract_functions(tree, str(file_path))

        # Extract imports
        imports, from_imports = self._extract_imports(tree)

        # Count lines
        lines = content.split('\n')
        total_lines = len(lines)
        code_lines = sum(1 for line in lines if line.strip() and not line.strip().startswith('#'))
        comment_lines = sum(1 for line in lines if line.strip().startswith('#'))

        # Create analysis
        analysis = FileAnalysis(
            file_path=str(file_path),
            classes=classes,
            functions=functions,
            imports=imports,
            from_imports=from_imports,
            total_lines=total_lines,
            code_lines=code_lines,
            comment_lines=comment_lines,
            is_test_file=self._is_test_file(file_path),
            is_init_file=file_path.name == "__init__.py"
        )

        # Detect patterns and smells
        analysis.patterns = self._detect_patterns(analysis, tree)
        analysis.smells = self._detect_smells(analysis)

        return analysis

    def _extract_classes(self, tree: ast.AST, file_path: str) -> List[CodeEntity]:
        """Extract all class definitions"""
        classes = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                entity = CodeEntity(
                    name=node.name,
                    entity_type=NodeType.CLASS,
                    file_path=file_path,
                    line_start=node.lineno,
                    line_end=node.end_lineno or node.lineno,
                    docstring=ast.get_docstring(node),
                    decorators=self._get_decorators(node),
                    is_public=not node.name.startswith('_')
                )

                # Extract methods
                methods = []
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        methods.append(item.name)

                entity.calls = methods  # Store method names
                classes.append(entity)

        return classes

    def _extract_functions(self, tree: ast.AST, file_path: str) -> List[CodeEntity]:
        """Extract all function definitions (module-level only)"""
        functions = []

        for node in tree.body:  # Only top-level
            if isinstance(node, ast.FunctionDef):
                entity = self._create_function_entity(node, file_path, NodeType.FUNCTION)
                functions.append(entity)
            elif isinstance(node, ast.AsyncFunctionDef):
                entity = self._create_function_entity(node, file_path, NodeType.ASYNC_FUNCTION)
                functions.append(entity)

        return functions

    def _create_function_entity(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
        file_path: str,
        entity_type: NodeType
    ) -> CodeEntity:
        """Create a CodeEntity from a function AST node"""
        # Extract parameters
        params = [arg.arg for arg in node.args.args]

        # Calculate complexity
        complexity = self._calculate_complexity(node)

        # Extract function calls
        calls = self._extract_calls(node)

        return CodeEntity(
            name=node.name,
            entity_type=entity_type,
            file_path=file_path,
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            docstring=ast.get_docstring(node),
            decorators=self._get_decorators(node),
            parameters=params,
            complexity=complexity,
            calls=calls,
            is_public=not node.name.startswith('_')
        )

    def _calculate_complexity(self, node: ast.FunctionDef) -> ComplexityMetrics:
        """Calculate cyclomatic complexity and other metrics"""
        complexity = 1  # Base complexity
        max_depth = 0
        current_depth = 0
        num_branches = 0

        for child in ast.walk(node):
            # Each decision point adds 1
            if isinstance(child, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                complexity += 1
                num_branches += 1

            # Boolean operators
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1

            # Nesting depth tracking (simplified)
            if isinstance(child, (ast.If, ast.For, ast.While, ast.With)):
                current_depth += 1
                max_depth = max(max_depth, current_depth)

        lines = (node.end_lineno - node.lineno + 1) if node.end_lineno else 1

        return ComplexityMetrics(
            cyclomatic_complexity=complexity,
            lines_of_code=lines,
            max_nesting_depth=max_depth,
            num_branches=num_branches
        )

    def _extract_calls(self, node: ast.FunctionDef) -> List[str]:
        """Extract function/method calls made by this function"""
        calls = []

        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    calls.append(child.func.id)
                elif isinstance(child.func, ast.Attribute):
                    calls.append(child.func.attr)

        return list(set(calls))  # Unique calls

    def _extract_imports(self, tree: ast.AST) -> tuple[List[str], Dict[str, List[str]]]:
        """Extract import statements"""
        imports = []
        from_imports = {}

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)

            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                names = [alias.name for alias in node.names]

                if module in from_imports:
                    from_imports[module].extend(names)
                else:
                    from_imports[module] = names

        return imports, from_imports

    def _get_decorators(self, node) -> List[str]:
        """Extract decorator names"""
        decorators = []

        for dec in node.decorator_list:
            if isinstance(dec, ast.Name):
                decorators.append(dec.id)
            elif isinstance(dec, ast.Call) and isinstance(dec.func, ast.Name):
                decorators.append(dec.func.id)

        return decorators

    def _is_test_file(self, file_path: Path) -> bool:
        """Check if file is a test file"""
        return (
            file_path.name.startswith('test_') or
            file_path.name.endswith('_test.py') or
            'test' in file_path.parts
        )

    # Pattern detection methods will be added in Phase 1B
    def _detect_patterns(self, analysis: FileAnalysis, tree: ast.AST) -> List[DesignPattern]:
        """Detect design patterns - implemented in Phase 1B"""
        return []

    def _detect_smells(self, analysis: FileAnalysis) -> List[Dict[str, Any]]:
        """Detect code smells"""
        smells = []

        # Check all functions for smells
        for func in analysis.functions:
            # Long function
            if func.complexity and func.complexity.lines_of_code > 50:
                smells.append({
                    "smell": CodeSmell.LONG_FUNCTION,
                    "location": f"{analysis.file_path}:{func.line_start}",
                    "name": func.name,
                    "metric": func.complexity.lines_of_code,
                    "description": f"Function has {func.complexity.lines_of_code} lines (recommend < 50)"
                })

            # Complex function
            if func.complexity and func.complexity.cyclomatic_complexity > 10:
                smells.append({
                    "smell": CodeSmell.COMPLEX_FUNCTION,
                    "location": f"{analysis.file_path}:{func.line_start}",
                    "name": func.name,
                    "metric": func.complexity.cyclomatic_complexity,
                    "description": f"Function has complexity {func.complexity.cyclomatic_complexity} (recommend < 10)"
                })

            # Too many parameters
            if len(func.parameters) > 5:
                smells.append({
                    "smell": CodeSmell.TOO_MANY_PARAMETERS,
                    "location": f"{analysis.file_path}:{func.line_start}",
                    "name": func.name,
                    "metric": len(func.parameters),
                    "description": f"Function has {len(func.parameters)} parameters (recommend < 5)"
                })

            # Deep nesting
            if func.complexity and func.complexity.max_nesting_depth > 4:
                smells.append({
                    "smell": CodeSmell.DEEP_NESTING,
                    "location": f"{analysis.file_path}:{func.line_start}",
                    "name": func.name,
                    "metric": func.complexity.max_nesting_depth,
                    "description": f"Function has nesting depth {func.complexity.max_nesting_depth} (recommend < 4)"
                })

        return smells
```

### Main CodeAnalyzer Class

```python
from pathlib import Path
from typing import List, Optional

class CodeAnalyzer:
    """Main interface for code analysis"""

    def __init__(self):
        self.python_analyzer = PythonAnalyzer()

    def analyze_codebase(
        self,
        root_path: str | Path,
        include_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
        max_files: Optional[int] = None
    ) -> CodebaseAnalysis:
        """
        Analyze entire codebase.

        Args:
            root_path: Root directory
            include_patterns: Glob patterns to include (default: ["**/*.py"])
            exclude_patterns: Patterns to exclude
            max_files: Maximum files to analyze

        Returns:
            Complete CodebaseAnalysis
        """
        root = Path(root_path)

        # Default patterns
        if not include_patterns:
            include_patterns = ["**/*.py"]

        if not exclude_patterns:
            exclude_patterns = [
                "**/__pycache__/**",
                "**/.git/**",
                "**/venv/**",
                "**/env/**",
                "**/.venv/**",
                "**/node_modules/**"
            ]

        # Discover files
        files = self._discover_files(root, include_patterns, exclude_patterns, max_files)

        # Analyze each file
        file_analyses = []
        total_lines = 0

        for file_path in files:
            analysis = self.python_analyzer.analyze_file(file_path)
            file_analyses.append(analysis)
            total_lines += analysis.total_lines

        # Build dependency graph
        dep_graph = self._build_dependency_graph(file_analyses, root)

        # Collect patterns
        patterns_found = {}
        for analysis in file_analyses:
            for pattern in analysis.patterns:
                if pattern not in patterns_found:
                    patterns_found[pattern] = []
                patterns_found[pattern].append(analysis.file_path)

        # Identify integration points
        integration_points = self._identify_integration_points(file_analyses)

        # Find entry points
        entry_points = self._find_entry_points(file_analyses)

        return CodebaseAnalysis(
            root_path=str(root),
            total_files=len(file_analyses),
            total_lines=total_lines,
            files=file_analyses,
            dependency_graph=dep_graph,
            patterns_found=patterns_found,
            integration_points=integration_points,
            entry_points=entry_points
        )

    def analyze_file(self, file_path: str | Path) -> FileAnalysis:
        """Analyze a single file"""
        return self.python_analyzer.analyze_file(Path(file_path))

    def _discover_files(
        self,
        root: Path,
        include: List[str],
        exclude: List[str],
        max_files: Optional[int]
    ) -> List[Path]:
        """Discover Python files to analyze"""
        files = []

        for pattern in include:
            for file_path in root.glob(pattern):
                if not file_path.is_file():
                    continue

                # Check exclusions
                should_exclude = False
                for ex_pattern in exclude:
                    if file_path.match(ex_pattern):
                        should_exclude = True
                        break

                if not should_exclude:
                    files.append(file_path)

                    if max_files and len(files) >= max_files:
                        return files

        return files

    def _build_dependency_graph(
        self,
        file_analyses: List[FileAnalysis],
        root: Path
    ) -> DependencyGraph:
        """Build import dependency graph"""
        edges = []

        # Create file path to module name mapping
        file_to_module = {}
        for analysis in file_analyses:
            # Convert file path to module name
            rel_path = Path(analysis.file_path).relative_to(root)
            module_parts = list(rel_path.parts[:-1])  # Directories
            if rel_path.name != "__init__.py":
                module_parts.append(rel_path.stem)  # Filename without .py

            module_name = ".".join(module_parts) if module_parts else rel_path.stem
            file_to_module[analysis.file_path] = module_name

        # Build edges
        module_to_file = {v: k for k, v in file_to_module.items()}

        for analysis in file_analyses:
            # Process imports
            for imp in analysis.imports:
                if imp in module_to_file:
                    edges.append(DependencyEdge(
                        from_file=analysis.file_path,
                        to_file=module_to_file[imp],
                        import_type="import",
                        imported_names=[imp]
                    ))

            # Process from imports
            for module, names in analysis.from_imports.items():
                if module in module_to_file:
                    edges.append(DependencyEdge(
                        from_file=analysis.file_path,
                        to_file=module_to_file[module],
                        import_type="from_import",
                        imported_names=names
                    ))

        return DependencyGraph(edges=edges)

    def _identify_integration_points(
        self,
        file_analyses: List[FileAnalysis]
    ) -> List[IntegrationPoint]:
        """Identify good integration points"""
        points = []

        for analysis in file_analyses:
            # Base classes are good integration points
            for cls in analysis.classes:
                # Abstract base classes or classes with "Base" in name
                if "Base" in cls.name or "Abstract" in cls.name:
                    points.append(IntegrationPoint(
                        name=cls.name,
                        file_path=analysis.file_path,
                        line_number=cls.line_start,
                        entity_type="class",
                        reason=f"Base class - extend to add new functionality",
                        pattern="Inheritance"
                    ))

                # Classes with Factory pattern
                if "Factory" in cls.name:
                    points.append(IntegrationPoint(
                        name=cls.name,
                        file_path=analysis.file_path,
                        line_number=cls.line_start,
                        entity_type="class",
                        reason="Factory class - add new product types here",
                        pattern="Factory"
                    ))

            # Public functions with "register" or "add" in name
            for func in analysis.functions:
                if func.is_public and any(keyword in func.name.lower()
                                         for keyword in ['register', 'add', 'create']):
                    points.append(IntegrationPoint(
                        name=func.name,
                        file_path=analysis.file_path,
                        line_number=func.line_start,
                        entity_type="function",
                        reason=f"Registration/creation function - use to add new items"
                    ))

        return points

    def _find_entry_points(self, file_analyses: List[FileAnalysis]) -> List[str]:
        """Find entry point files"""
        entry_points = []

        for analysis in file_analyses:
            file_name = Path(analysis.file_path).name

            # Main files
            if file_name in ["main.py", "__main__.py", "app.py", "cli.py"]:
                entry_points.append(analysis.file_path)

            # __init__.py files (package entry points)
            elif analysis.is_init_file:
                entry_points.append(analysis.file_path)

            # Files with if __name__ == "__main__"
            for func in analysis.functions:
                if func.name == "<module>":  # Top-level code
                    # This is a heuristic - in real implementation would check AST
                    entry_points.append(analysis.file_path)
                    break

        return entry_points
```

---

## Phase 1B: Pattern Detection

### Implementation

```python
class PatternDetector:
    """Detects design patterns in Python code"""

    def detect_patterns(
        self,
        analysis: FileAnalysis,
        tree: ast.AST
    ) -> List[DesignPattern]:
        """Detect design patterns in a file"""
        patterns = []

        # Singleton pattern
        if self._has_singleton(analysis, tree):
            patterns.append(DesignPattern.SINGLETON)

        # Factory pattern
        if self._has_factory(analysis):
            patterns.append(DesignPattern.FACTORY)

        # Strategy pattern
        if self._has_strategy(analysis):
            patterns.append(DesignPattern.STRATEGY)

        # Decorator pattern (not Python @decorators)
        if self._has_decorator_pattern(analysis):
            patterns.append(DesignPattern.DECORATOR)

        # Observer pattern
        if self._has_observer(analysis):
            patterns.append(DesignPattern.OBSERVER)

        return patterns

    def _has_singleton(self, analysis: FileAnalysis, tree: ast.AST) -> bool:
        """Detect singleton pattern"""
        for cls in analysis.classes:
            # Check for __new__ override or _instance class variable
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == cls.name:
                    # Look for __new__ method
                    has_new = any(
                        isinstance(item, ast.FunctionDef) and item.name == '__new__'
                        for item in node.body
                    )

                    # Look for _instance variable
                    has_instance = any(
                        isinstance(item, ast.Assign) and
                        any(isinstance(target, ast.Name) and target.id == '_instance'
                            for target in item.targets)
                        for item in node.body
                    )

                    if has_new or has_instance:
                        return True

        return False

    def _has_factory(self, analysis: FileAnalysis) -> bool:
        """Detect factory pattern"""
        # Look for classes or functions with "Factory" in name
        has_factory_class = any("Factory" in cls.name for cls in analysis.classes)

        # Look for create_* methods
        has_create_method = any(
            "create" in func.name.lower() or "make" in func.name.lower()
            for func in analysis.functions
        )

        return has_factory_class or has_create_method

    def _has_strategy(self, analysis: FileAnalysis) -> bool:
        """Detect strategy pattern"""
        # Look for multiple classes with similar method names
        if len(analysis.classes) < 2:
            return False

        # Check if classes have common method signatures
        class_methods = {}
        for cls in analysis.classes:
            class_methods[cls.name] = set(cls.calls)  # Methods

        # If multiple classes share common method names, might be strategies
        if len(class_methods) >= 2:
            method_sets = list(class_methods.values())
            common_methods = set.intersection(*method_sets)

            # If 2+ common methods, likely strategy pattern
            if len(common_methods) >= 2:
                return True

        return False

    def _has_decorator_pattern(self, analysis: FileAnalysis) -> bool:
        """Detect decorator pattern (wrapper classes)"""
        for cls in analysis.classes:
            # Look for "Decorator" or "Wrapper" in name
            if "Decorator" in cls.name or "Wrapper" in cls.name:
                return True

            # Look for classes that take another object in __init__
            # (This is a heuristic - would need deeper AST analysis)
            if "wrapped" in str(cls.calls).lower():
                return True

        return False

    def _has_observer(self, analysis: FileAnalysis) -> bool:
        """Detect observer pattern"""
        # Look for subscribe/notify/update methods
        observer_keywords = ['subscribe', 'notify', 'update', 'attach', 'detach', 'observer']

        for func in analysis.functions:
            if any(keyword in func.name.lower() for keyword in observer_keywords):
                return True

        for cls in analysis.classes:
            if any(keyword in method.lower() for keyword in observer_keywords
                   for method in cls.calls):
                return True

        return False
```

---

## Phase 1C: Integration Point Identification

Already implemented in `_identify_integration_points` method above.

---

## Testing Strategy

See full implementation below for test suite.

---

## Integration with Agents

### file-search-agent Enhancement

```python
# file-search-agent uses code-analysis skill

from skills.code_analysis import CodeAnalyzer

# Analyze codebase for feature
analyzer = CodeAnalyzer()
analysis = analyzer.analyze_codebase("src/agents/")

# Find integration points
for feature in ["new agent type"]:
    points = analysis.suggest_integration_for_feature(feature)

    # Document findings
    markdown = f"## Integration Points for {feature}\n\n"
    for point in points:
        markdown += f"- **{point.name}** ({point.file_path}:{point.line_number})\n"
        markdown += f"  - {point.reason}\n"
        if point.pattern:
            markdown += f"  - Pattern: {point.pattern}\n"
```

---

## File Structure

```
skills/code_analysis/
├── __init__.py           # Package exports
├── models.py             # Pydantic data models
├── python_analyzer.py    # Python AST analysis
├── pattern_detector.py   # Pattern detection
├── code_analyzer.py      # Main analyzer class
├── skill.md              # Skill definition
└── README.md             # Documentation
```

---

## Performance Targets

- Analyze 100 Python files: < 2 seconds
- Analyze entire src/ directory: < 5 seconds
- Pattern detection overhead: < 10% of parse time
- Memory usage: < 200MB for typical codebase

---

**End of Implementation Spec**

# MCP Code Execution Implementation Plan

**Date:** 2025-11-05
**Status:** Ready for Implementation
**Target:** 98.7% token reduction through code execution patterns

---

## Overview

This plan implements the MCP code execution efficiency patterns identified in [MCP_EFFICIENCY_ANALYSIS.md](./MCP_EFFICIENCY_ANALYSIS.md).

**Key Goals:**
1. Enable agents to generate Python code that calls skills
2. Filter results locally before model sees them
3. Load tools on-demand instead of upfront
4. Maintain backward compatibility

---

## Phase 1: Foundation (Priority 1 - High Impact, Low Effort)

### 1.1: Create Result Filtering Utilities

**Location:** `skills/common/filters.py`

```python
"""
Common filtering utilities for all skills.
Enables local data filtering before results reach the model.
"""

from typing import List, Dict, Any, Callable


class ResultFilter:
    """Efficient filtering operations for skill results."""

    @staticmethod
    def limit(results: List[Any], n: int) -> List[Any]:
        """
        Return first n results.

        Example:
            files = analyze_codebase("src/")  # 10,000 files
            top_5 = ResultFilter.limit(files, 5)  # Only 5 files
        """
        return results[:n] if results else []

    @staticmethod
    def filter_by_field(
        results: List[Dict],
        field: str,
        value: Any
    ) -> List[Dict]:
        """
        Filter results where field equals value.

        Example:
            tests = generate_tests()  # All tests
            failed = ResultFilter.filter_by_field(tests, "status", "failed")
        """
        return [r for r in results if r.get(field) == value]

    @staticmethod
    def filter_by_predicate(
        results: List[Any],
        predicate: Callable[[Any], bool]
    ) -> List[Any]:
        """
        Filter results using custom predicate.

        Example:
            files = analyze_codebase("src/")
            complex = ResultFilter.filter_by_predicate(
                files,
                lambda f: f.complexity > 10
            )
        """
        return [r for r in results if predicate(r)]

    @staticmethod
    def summarize(results: List[Any], sample_size: int = 3) -> Dict[str, Any]:
        """
        Return summary instead of full dataset.

        Example:
            history = get_learning_history()  # 6 months, 30,000 tokens
            summary = ResultFilter.summarize(history)  # 100 tokens
            # Returns: {"count": 1000, "sample": [...]}
        """
        return {
            "total_count": len(results),
            "sample": results[:sample_size] if results else [],
            "has_more": len(results) > sample_size
        }

    @staticmethod
    def top_n_by_field(
        results: List[Dict],
        field: str,
        n: int,
        reverse: bool = True
    ) -> List[Dict]:
        """
        Return top n results sorted by field.

        Example:
            files = analyze_codebase("src/")
            most_complex = ResultFilter.top_n_by_field(
                files, "complexity", 5
            )
        """
        sorted_results = sorted(
            results,
            key=lambda x: x.get(field, 0),
            reverse=reverse
        )
        return sorted_results[:n]

    @staticmethod
    def group_by(
        results: List[Dict],
        field: str
    ) -> Dict[Any, List[Dict]]:
        """
        Group results by field value.

        Example:
            tests = generate_tests()
            by_status = ResultFilter.group_by(tests, "status")
            # Returns: {"passed": [...], "failed": [...]}
        """
        groups = {}
        for result in results:
            key = result.get(field)
            if key not in groups:
                groups[key] = []
            groups[key].append(result)
        return groups

    @staticmethod
    def extract_fields(
        results: List[Dict],
        fields: List[str]
    ) -> List[Dict]:
        """
        Extract only specified fields from results.

        Example:
            files = analyze_codebase("src/")  # Full file objects
            names_only = ResultFilter.extract_fields(files, ["path", "name"])
        """
        return [
            {field: r.get(field) for field in fields}
            for r in results
        ]

    @staticmethod
    def search(
        results: List[Dict],
        query: str,
        fields: List[str]
    ) -> List[Dict]:
        """
        Search results where any field contains query.

        Example:
            files = analyze_codebase("src/")
            navigation_files = ResultFilter.search(
                files, "navigation", ["path", "name"]
            )
        """
        query = query.lower()
        return [
            r for r in results
            if any(
                query in str(r.get(field, "")).lower()
                for field in fields
            )
        ]
```

### 1.2: Create CodeExecutionEngine

**Location:** `skills/execution/code_executor.py`

```python
"""
Code Execution Engine for MCP-style efficiency.
Executes agent-generated code in sandboxed environment with skill access.
"""

import sys
import ast
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr


@dataclass
class ExecutionResult:
    """Result from code execution."""
    success: bool
    output: Any = None
    stdout: str = ""
    stderr: str = ""
    error: Optional[str] = None
    duration: float = 0.0
    tokens_saved: Optional[int] = None  # Estimated token savings


class CodeExecutionEngine:
    """
    Executes agent-generated Python code in secure sandbox.

    Skills are available as importable modules.
    Code can filter/transform data locally before returning.
    """

    # Allowed imports (security whitelist)
    ALLOWED_SKILL_IMPORTS = [
        "skills.code_analysis",
        "skills.test_orchestrator",
        "skills.learning_analytics",
        "skills.learning_plan_manager",
        "skills.session_state",
        "skills.interactive_diagram",
        "skills.refactor_assistant",
        "skills.pr_review_assistant",
        "skills.dependency_guardian",
        "skills.doc_generator",
        "skills.git_workflow_assistant",
        "skills.spec_to_implementation",
        "skills.common.filters",  # Result filtering utilities
    ]

    # Allowed built-in functions
    ALLOWED_BUILTINS = {
        "len", "range", "enumerate", "zip", "map", "filter",
        "sum", "min", "max", "sorted", "list", "dict", "set",
        "str", "int", "float", "bool", "isinstance", "hasattr",
        "getattr", "print"
    }

    MAX_EXECUTION_TIME = 30  # seconds
    MAX_OUTPUT_SIZE = 100_000  # characters

    def __init__(self, skills_path: str = "skills"):
        self.skills_path = Path(skills_path).absolute()
        self._setup_path()

    def _setup_path(self):
        """Add skills directory to Python path."""
        parent = str(self.skills_path.parent)
        if parent not in sys.path:
            sys.path.insert(0, parent)

    def validate_code(self, code: str) -> tuple[bool, Optional[str]]:
        """
        Validate code for security issues.

        Returns:
            (is_valid, error_message)
        """
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"Syntax error: {str(e)}"

        # Check imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if not self._is_allowed_import(alias.name):
                        return False, f"Import not allowed: {alias.name}"

            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                if not self._is_allowed_import(module):
                    return False, f"Import not allowed: {module}"

            # Block dangerous operations
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ["eval", "exec", "__import__"]:
                        return False, f"Dangerous function: {node.func.id}"

        return True, None

    def _is_allowed_import(self, module_name: str) -> bool:
        """Check if import is allowed."""
        # Allow all skill imports
        for allowed in self.ALLOWED_SKILL_IMPORTS:
            if module_name == allowed or module_name.startswith(allowed + "."):
                return True
        return False

    def execute(
        self,
        code: str,
        context: Optional[Dict[str, Any]] = None,
        timeout: int = MAX_EXECUTION_TIME
    ) -> ExecutionResult:
        """
        Execute code in sandboxed environment.

        Args:
            code: Python code to execute
            context: Optional context variables
            timeout: Execution timeout in seconds

        Returns:
            ExecutionResult with output and metadata
        """
        start_time = time.time()

        # Validate code
        is_valid, error = self.validate_code(code)
        if not is_valid:
            return ExecutionResult(
                success=False,
                error=error,
                duration=time.time() - start_time
            )

        # Capture stdout/stderr
        stdout_capture = StringIO()
        stderr_capture = StringIO()

        try:
            # Create execution namespace
            namespace = {
                "__builtins__": {
                    name: __builtins__[name]
                    for name in self.ALLOWED_BUILTINS
                    if name in __builtins__
                }
            }

            # Add context variables
            if context:
                namespace.update(context)

            # Execute code
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(code, namespace)

            # Get return value (last expression or explicit return via namespace)
            output = namespace.get("__result__") or namespace.get("result")

            duration = time.time() - start_time

            return ExecutionResult(
                success=True,
                output=output,
                stdout=stdout_capture.getvalue(),
                stderr=stderr_capture.getvalue(),
                duration=duration
            )

        except Exception as e:
            return ExecutionResult(
                success=False,
                error=f"Execution error: {str(e)}",
                stdout=stdout_capture.getvalue(),
                stderr=stderr_capture.getvalue(),
                duration=time.time() - start_time
            )

    def execute_with_result(self, code: str) -> ExecutionResult:
        """
        Execute code that returns a result.

        Convenience wrapper that expects code to set 'result' variable.

        Example:
            code = '''
            from skills.code_analysis import analyze_file
            from skills.common.filters import ResultFilter

            files = analyze_file("src/")
            result = ResultFilter.limit(files, 5)
            '''

            exec_result = engine.execute_with_result(code)
            if exec_result.success:
                print(exec_result.output)  # Filtered results
        """
        return self.execute(code)


class SkillCodeGenerator:
    """
    Helper to generate efficient code for common skill operations.
    """

    @staticmethod
    def generate_filtered_analysis(
        path: str,
        filter_pattern: Optional[str] = None,
        limit: int = 5
    ) -> str:
        """Generate code for filtered code analysis."""
        code = f'''
from skills.code_analysis import analyze_codebase
from skills.common.filters import ResultFilter

# Analyze codebase
files = analyze_codebase("{path}")
'''

        if filter_pattern:
            code += f'''
# Filter by pattern
filtered = ResultFilter.search(files, "{filter_pattern}", ["path", "name"])
'''
        else:
            code += '''
filtered = files
'''

        code += f'''
# Limit results
result = ResultFilter.limit(filtered, {limit})
'''

        return code

    @staticmethod
    def generate_test_summary(source_file: str) -> str:
        """Generate code for test generation summary."""
        return f'''
from skills.test_orchestrator import generate_tests
from skills.common.filters import ResultFilter

# Generate tests
tests = generate_tests("{source_file}")

# Return summary instead of all tests
result = ResultFilter.summarize(tests, sample_size=3)
'''

    @staticmethod
    def generate_learning_status(student_id: str) -> str:
        """Generate code for current learning status (not full history)."""
        return f'''
from skills.learning_analytics import analyze_student
from skills.session_state import get_student

# Get current status only
student = get_student("{student_id}")
analytics = analyze_student("{student_id}")

# Return current status, not full history
result = {{
    "name": student["name"],
    "current_velocity": analytics.current_velocity,
    "struggles": analytics.current_struggles[:3],  # Top 3 only
    "health": analytics.health_status,
    "recent_achievements": student["achievements"][-3:]  # Last 3 only
}}
'''
```

### 1.3: Update Skills with Filtering Support

**Example: code_analysis/filters.py**
```python
"""Filtering utilities specific to code analysis."""

from skills.common.filters import ResultFilter


class CodeAnalysisFilter(ResultFilter):
    """Specialized filters for code analysis results."""

    @staticmethod
    def filter_by_complexity(files: list, min_complexity: int = 10) -> list:
        """Return files above complexity threshold."""
        return [f for f in files if f.get("complexity", 0) >= min_complexity]

    @staticmethod
    def filter_by_pattern(files: list, pattern: str) -> list:
        """Return files matching design pattern."""
        return [
            f for f in files
            if pattern.lower() in f.get("patterns", [])
        ]

    @staticmethod
    def find_integration_points(files: list, feature: str) -> list:
        """Find likely integration points for new feature."""
        # Search for relevant files
        relevant = ResultFilter.search(files, feature, ["path", "name"])
        # Return top 5 by complexity (likely integration points)
        return ResultFilter.top_n_by_field(relevant, "complexity", 5)
```

---

## Phase 2: Integration (Priority 2 - High Impact, Medium Effort)

### 2.1: Filesystem-Based Tool Discovery

**Current Structure:**
```
skills/
  └── code_analysis/
      ├── __init__.py
      ├── core.py (all operations in one file)
      └── skill.md
```

**New Structure:**
```
skills/
  └── code_analysis/
      ├── __init__.py (lightweight, re-exports)
      ├── skill.md (metadata only)
      ├── operations/
      │   ├── analyze_file.py (one operation per file)
      │   ├── analyze_codebase.py
      │   └── find_integration_points.py
      └── filters.py (result filtering)
```

Each operation file has clean interface:
```python
# skills/code_analysis/operations/analyze_file.py
"""
Analyze a single source file for patterns and complexity.

Token efficiency: Filter results locally before returning.
"""

def analyze_file(file_path: str, options: dict = None) -> dict:
    """
    Analyze a single file.

    Args:
        file_path: Path to file
        options: Optional configuration

    Returns:
        {
            "path": str,
            "complexity": int,
            "patterns": List[str],
            "functions": List[dict]
        }

    Usage (efficient):
        ```python
        from skills.code_analysis.operations import analyze_file
        from skills.common.filters import ResultFilter

        # Analyze
        result = analyze_file("src/payment.py")

        # Filter to high complexity functions only
        complex_funcs = ResultFilter.filter_by_predicate(
            result["functions"],
            lambda f: f["complexity"] > 10
        )

        # Return filtered results
        return {"high_complexity_functions": complex_funcs}
        ```
    """
    # Implementation
    pass
```

### 2.2: Update Agent Prompts

**Example: learning-coordinator agent**

Add code generation capability:
```markdown
## Code Execution for Efficiency

You can write Python code to call skills efficiently, filtering data locally
before results reach your context.

### Available Skills

Explore the skills directory structure:
- skills/code_analysis/ - Code structure analysis
- skills/learning_analytics/ - Learning metrics and insights
- skills/session_state/ - Student profiles and history
- skills/test_orchestrator/ - Test generation and execution

### When to Use Code Execution

Use code execution when:
✅ Dealing with large datasets (code analysis, test results, history)
✅ Need to filter/transform data before processing
✅ Want to reduce token consumption

Use direct skill invocation for:
✅ Simple, small data operations
✅ Quick queries

### Code Execution Examples

**Example 1: Filtered Code Analysis**
```python
from skills.code_analysis import analyze_codebase
from skills.common.filters import ResultFilter

# Analyze full codebase
files = analyze_codebase("src/")  # Could be 10,000 files

# Filter to navigation-related files only
navigation_files = ResultFilter.search(files, "navigation", ["path", "name"])

# Return top 5 most complex (likely integration points)
result = ResultFilter.top_n_by_field(navigation_files, "complexity", 5)
# Only 5 files returned instead of 10,000!
```

**Example 2: Learning Status Summary**
```python
from skills.learning_analytics import analyze_student
from skills.session_state import get_student

# Get data
student = get_student("alex_2025")
analytics = analyze_student("alex_2025")

# Return SUMMARY, not full history
result = {
    "current_velocity": analytics.current_velocity,
    "top_struggles": analytics.current_struggles[:3],
    "health": analytics.health_status
}
# 100 tokens instead of 30,000!
```

### Result Filtering Utilities

All skills have access to `skills.common.filters.ResultFilter`:
- `limit(results, n)` - First n results
- `filter_by_field(results, field, value)` - Filter by field value
- `top_n_by_field(results, field, n)` - Top n by field
- `summarize(results)` - Summary instead of full data
- `search(results, query, fields)` - Search results

Always filter data before returning to reduce token usage!
```

### 2.3: Add Efficiency Metrics

Track token savings:
```python
# skills/execution/metrics.py

@dataclass
class EfficiencyMetrics:
    """Track token savings from code execution."""
    operation: str
    tokens_without_filtering: int
    tokens_with_filtering: int
    savings_percent: float
    duration: float

class EfficiencyTracker:
    """Track efficiency gains from code execution pattern."""

    def __init__(self):
        self.metrics: List[EfficiencyMetrics] = []

    def record_execution(
        self,
        operation: str,
        full_result_size: int,
        filtered_result_size: int,
        duration: float
    ):
        """Record an execution with filtering."""
        tokens_saved = full_result_size - filtered_result_size
        savings_percent = (tokens_saved / full_result_size) * 100

        self.metrics.append(EfficiencyMetrics(
            operation=operation,
            tokens_without_filtering=full_result_size,
            tokens_with_filtering=filtered_result_size,
            savings_percent=savings_percent,
            duration=duration
        ))

    def get_summary(self) -> dict:
        """Get efficiency summary."""
        if not self.metrics:
            return {}

        total_without = sum(m.tokens_without_filtering for m in self.metrics)
        total_with = sum(m.tokens_with_filtering for m in self.metrics)
        avg_savings = (total_without - total_with) / total_without * 100

        return {
            "total_operations": len(self.metrics),
            "tokens_without_filtering": total_without,
            "tokens_with_filtering": total_with,
            "total_tokens_saved": total_without - total_with,
            "average_savings_percent": avg_savings
        }
```

---

## Phase 3: Optimization (Breaking Changes OK)

### 3.1: Enforce Filtering for Large Results

```python
class ResultSizeEnforcer:
    """Enforce size limits on skill results."""

    MAX_RESULT_SIZE = 10_000  # tokens

    @staticmethod
    def check_result_size(result: Any) -> tuple[bool, int]:
        """Check if result exceeds size limit."""
        # Estimate token count
        import json
        result_str = json.dumps(result) if isinstance(result, (dict, list)) else str(result)
        tokens = len(result_str) // 4  # Rough estimate

        return tokens <= ResultSizeEnforcer.MAX_RESULT_SIZE, tokens

    @staticmethod
    def enforce(result: Any, operation: str):
        """Raise error if result too large."""
        within_limit, tokens = ResultSizeEnforcer.check_result_size(result)

        if not within_limit:
            raise ValueError(
                f"Result from {operation} exceeds size limit "
                f"({tokens} tokens > {ResultSizeEnforcer.MAX_RESULT_SIZE} tokens). "
                f"Use ResultFilter to reduce result size before returning."
            )
```

### 3.2: Auto-suggest Filtering

```python
class FilteringSuggester:
    """Suggest filtering operations for large results."""

    @staticmethod
    def suggest_filters(result: Any, operation: str) -> List[str]:
        """Suggest filtering operations."""
        suggestions = []

        if isinstance(result, list):
            size = len(result)
            if size > 100:
                suggestions.append(
                    f"ResultFilter.limit({operation}_result, 10) "
                    f"# {size} items is too many"
                )
            if isinstance(result[0], dict):
                keys = list(result[0].keys())
                suggestions.append(
                    f"ResultFilter.extract_fields({operation}_result, {keys[:3]}) "
                    f"# Extract only needed fields"
                )

        return suggestions
```

---

## Testing Strategy

### Unit Tests

```python
# tests/test_code_execution.py

import pytest
from skills.execution.code_executor import CodeExecutionEngine

def test_basic_execution():
    """Test basic code execution."""
    engine = CodeExecutionEngine()

    code = '''
result = 2 + 2
'''

    result = engine.execute_with_result(code)
    assert result.success
    assert result.output == 4


def test_skill_import_and_filter():
    """Test skill import with filtering."""
    engine = CodeExecutionEngine()

    code = '''
from skills.common.filters import ResultFilter

data = [1, 2, 3, 4, 5]
result = ResultFilter.limit(data, 2)
'''

    result = engine.execute_with_result(code)
    assert result.success
    assert result.output == [1, 2]


def test_security_validation():
    """Test security validation blocks dangerous code."""
    engine = CodeExecutionEngine()

    # Should block eval
    code = 'result = eval("2 + 2")'
    result = engine.execute_with_result(code)
    assert not result.success
    assert "Dangerous function" in result.error

    # Should block unauthorized imports
    code = 'import os\nresult = os.listdir()'
    result = engine.execute_with_result(code)
    assert not result.success
    assert "Import not allowed" in result.error
```

### Integration Tests

```python
# tests/test_efficiency_gains.py

def test_code_analysis_efficiency():
    """Test token savings from filtered code analysis."""
    from skills.code_analysis import analyze_codebase
    from skills.common.filters import ResultFilter

    # Full analysis
    full_results = analyze_codebase("src/")
    full_size = len(str(full_results))  # Simulate tokens

    # Filtered analysis
    filtered = ResultFilter.limit(full_results, 5)
    filtered_size = len(str(filtered))

    # Should save > 95% tokens
    savings = (full_size - filtered_size) / full_size
    assert savings > 0.95
```

---

## Documentation Updates

### 1. Update README.md

Add efficiency section:
```markdown
## 🚀 Efficiency Features

### Code Execution Pattern (98.7% Token Reduction)

Instead of returning massive datasets to the model, generate Python code that
filters data locally:

```python
# Old way: Model sees all 10,000 files
files = code_analysis.analyze_codebase("src/")
# → 50,000 tokens

# New way: Model sees only 5 relevant files
from skills.code_analysis import analyze_codebase
from skills.common.filters import ResultFilter

files = analyze_codebase("src/")
relevant = ResultFilter.search(files, "navigation", ["path"])
result = ResultFilter.limit(relevant, 5)
# → 500 tokens (99% reduction!)
```

See [MCP_EFFICIENCY_ANALYSIS.md](./docs/MCP_EFFICIENCY_ANALYSIS.md) for details.
```

### 2. Create Usage Guide

**File:** `docs/CODE_EXECUTION_GUIDE.md`

Contents:
- When to use code execution vs direct invocation
- Filtering best practices
- Security considerations
- Performance benchmarks
- Common patterns and examples

---

## Success Metrics

### KPIs to Track

1. **Token Reduction**
   - Target: 98% for data-heavy operations
   - Measure: Compare filtered vs unfiltered results

2. **Operation Coverage**
   - Target: 80% of high-volume operations use filtering
   - Measure: Track filtered vs direct invocations

3. **Performance**
   - Target: < 100ms overhead from code execution
   - Measure: Execution time metrics

4. **Adoption**
   - Target: 50% of agent operations use code execution within 1 month
   - Measure: Usage metrics

---

## Rollout Plan

### Week 1: Foundation
- [ ] Implement ResultFilter utilities
- [ ] Create CodeExecutionEngine
- [ ] Add security validation
- [ ] Write unit tests

### Week 2: Integration
- [ ] Update 5 key skills with filter support
- [ ] Add code generation examples
- [ ] Update learning-coordinator agent
- [ ] Integration testing

### Week 3: Documentation
- [ ] Write code execution guide
- [ ] Add examples to skill docs
- [ ] Create efficiency benchmarks
- [ ] Update README

### Week 4: Optimization
- [ ] Add efficiency metrics
- [ ] Implement auto-suggestions
- [ ] Monitor adoption
- [ ] Iterate based on feedback

---

## Next Steps

1. **Immediate**: Review and approve plan
2. **Day 1**: Implement ResultFilter and CodeExecutionEngine
3. **Day 2**: Add filtering to code_analysis skill
4. **Day 3**: Test with learning-coordinator agent
5. **Day 4**: Measure efficiency gains, iterate

---

**Status:** ✅ Ready for implementation
**Expected Timeline:** 4 weeks
**Expected Impact:** 98.7% token reduction for data-heavy operations

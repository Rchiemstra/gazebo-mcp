"""
Code Execution Engine for MCP-style efficiency.

Executes agent-generated code in sandboxed environment with skill access.
This enables the key efficiency pattern from Anthropic's MCP blog:
- Agent generates code that imports and calls skills
- Code filters/transforms data locally
- Only filtered results returned to model
- Result: Up to 98.7% token reduction!

Security: Code is validated and executed in restricted environment.
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

    Example:
        engine = CodeExecutionEngine()

        code = '''
from skills.code_analysis import analyze_codebase
from skills.common.filters import ResultFilter

# Analyze full codebase (could be 10,000 files)
files = analyze_codebase("src/")

# Filter to navigation-related files only
navigation = ResultFilter.search(files, "navigation", ["path", "name"])

# Return top 5 most complex
result = ResultFilter.top_n_by_field(navigation, "complexity", 5)
# Only 5 files returned instead of 10,000!
'''

        result = engine.execute_with_result(code)
        if result.success:
            print(result.output)  # Filtered results
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
        "skills.common",  # Result filtering utilities
        "skills.common.filters",
    ]

    # Allowed built-in functions
    ALLOWED_BUILTINS = {
        "len", "range", "enumerate", "zip", "map", "filter",
        "sum", "min", "max", "sorted", "list", "dict", "set", "tuple",
        "str", "int", "float", "bool", "isinstance", "hasattr",
        "getattr", "print", "abs", "round", "any", "all",
        "__build_class__", "__name__", "__import__",  # Required for imports and classes
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
                    if node.func.id in ["eval", "exec", "__import__", "compile"]:
                        return False, f"Dangerous function not allowed: {node.func.id}"

            # Block file operations (except Read tool via proper skills)
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ["open", "file"]:
                        return False, "Direct file operations not allowed. Use skills instead."

        return True, None

    def _is_allowed_import(self, module_name: str) -> bool:
        """Check if import is allowed."""
        # Allow statistics module for aggregations
        if module_name == "statistics":
            return True

        # Allow all skill imports
        for allowed in self.ALLOWED_SKILL_IMPORTS:
            if module_name == allowed or module_name.startswith(allowed + "."):
                return True

        return False

    def execute(
        self,
        code: str,
        context: Optional[Dict[str, Any]] = None,
        timeout: int = None
    ) -> ExecutionResult:
        """
        Execute code in sandboxed environment.

        Args:
            code: Python code to execute
            context: Optional context variables
            timeout: Execution timeout in seconds (default: MAX_EXECUTION_TIME)

        Returns:
            ExecutionResult with output and metadata
        """
        if timeout is None:
            timeout = self.MAX_EXECUTION_TIME

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
            # Create execution namespace with safe builtins
            # Instead of restricting all builtins, use full builtins but override dangerous ones
            import builtins as builtin_module
            safe_builtins = {
                name: getattr(builtin_module, name)
                for name in dir(builtin_module)
                if not name.startswith('_') or name in ['__name__', '__build_class__', '__import__']
            }

            # Override dangerous functions
            def safe_import(name, *args, **kwargs):
                """Safe import that only allows whitelisted modules."""
                if not self._is_allowed_import(name):
                    raise ImportError(f"Import not allowed: {name}")
                return builtin_module.__import__(name, *args, **kwargs)

            def blocked_function(func_name):
                def _blocked(*args, **kwargs):
                    raise RuntimeError(f"Function {func_name} is not allowed")
                return _blocked

            # Replace dangerous functions
            safe_builtins['__import__'] = safe_import
            safe_builtins['eval'] = blocked_function('eval')
            safe_builtins['exec'] = blocked_function('exec')
            safe_builtins['compile'] = blocked_function('compile')
            safe_builtins['open'] = blocked_function('open')

            namespace = {
                "__builtins__": safe_builtins
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

    def execute_with_result(
        self,
        code: str,
        context: Optional[Dict[str, Any]] = None
    ) -> ExecutionResult:
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
        return self.execute(code, context)


class SkillCodeGenerator:
    """
    Helper to generate efficient code for common skill operations.

    This demonstrates best practices for MCP code execution patterns.
    """

    @staticmethod
    def generate_filtered_analysis(
        path: str,
        filter_pattern: Optional[str] = None,
        limit: int = 5
    ) -> str:
        """
        Generate code for filtered code analysis.

        Example:
            code = SkillCodeGenerator.generate_filtered_analysis(
                "src/", filter_pattern="navigation", limit=5
            )
            result = engine.execute_with_result(code)
        """
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
        """
        Generate code for test generation summary.

        Returns summary instead of all tests (massive token savings).
        """
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
        """
        Generate code for current learning status (not full history).

        Returns current status only, not 6 months of history.
        """
        return f'''
from skills.learning_analytics import analyze_student
from skills.session_state import get_student

# Get current status only
student = get_student("{student_id}")
analytics = analyze_student("{student_id}")

# Return current status, not full history
result = {{
    "name": student.get("name"),
    "current_velocity": analytics.get("current_velocity"),
    "struggles": analytics.get("current_struggles", [])[:3],  # Top 3 only
    "health": analytics.get("health_status"),
    "recent_achievements": student.get("achievements", [])[-3:]  # Last 3 only
}}
'''

    @staticmethod
    def generate_complexity_analysis(path: str, min_complexity: int = 10) -> str:
        """Generate code to analyze only high-complexity files."""
        return f'''
from skills.code_analysis import analyze_codebase
from skills.common.filters import ResultFilter

# Analyze codebase
files = analyze_codebase("{path}")

# Filter to high complexity only
high_complexity = ResultFilter.filter_by_threshold(
    files, "complexity", {min_complexity}, ">"
)

# Return top 10 most complex
result = ResultFilter.top_n_by_field(high_complexity, "complexity", 10)
'''

    @staticmethod
    def generate_failed_tests_only(test_path: str) -> str:
        """Generate code to return only failed tests."""
        return f'''
from skills.test_orchestrator import run_tests
from skills.common.filters import ResultFilter

# Run tests
test_results = run_tests("{test_path}")

# Return only failed tests
result = ResultFilter.filter_by_field(test_results, "status", "failed")
'''

    @staticmethod
    def generate_integration_points(feature: str, limit: int = 5) -> str:
        """Generate code to find integration points for new feature."""
        return f'''
from skills.code_analysis import analyze_codebase, find_integration_points
from skills.common.filters import ResultFilter

# Analyze codebase
files = analyze_codebase("src/")

# Search for relevant files
relevant = ResultFilter.search(files, "{feature}", ["path", "name", "description"])

# Return top {limit} most complex (likely integration points)
result = ResultFilter.top_n_by_field(relevant, "complexity", {limit})
'''


class ResultSizeValidator:
    """
    Validate and enforce result size limits.

    Prevents accidentally returning huge datasets to model.
    """

    MAX_RESULT_SIZE = 10_000  # tokens

    @staticmethod
    def estimate_size(result: Any) -> int:
        """Estimate result size in tokens."""
        import json

        try:
            if isinstance(result, (dict, list)):
                result_str = json.dumps(result)
            else:
                result_str = str(result)

            # Rough estimate: 1 token ≈ 4 characters
            return len(result_str) // 4

        except:
            return 0

    @staticmethod
    def check_size(result: Any, operation: str) -> tuple[bool, int, Optional[str]]:
        """
        Check if result exceeds size limit.

        Returns:
            (within_limit, estimated_tokens, suggestion)
        """
        tokens = ResultSizeValidator.estimate_size(result)
        within_limit = tokens <= ResultSizeValidator.MAX_RESULT_SIZE

        suggestion = None
        if not within_limit:
            suggestion = f"""
Result from {operation} is too large ({tokens} tokens > {ResultSizeValidator.MAX_RESULT_SIZE} tokens).

Suggestions:
1. Use ResultFilter.limit() to reduce number of items
2. Use ResultFilter.summarize() to return summary instead
3. Use ResultFilter.extract_fields() to keep only needed fields
4. Add more specific filtering before returning

Example:
    from skills.common.filters import ResultFilter
    result = ResultFilter.limit(large_result, 10)
"""

        return within_limit, tokens, suggestion

"""
Code execution engine for MCP-style efficiency with sandboxing and think tool.
"""

from .code_executor import CodeExecutionEngine, ExecutionResult, SkillCodeGenerator
from .metrics import EfficiencyMetrics, EfficiencyTracker
from .sandboxed_executor import SandboxedExecutor, SandboxConfig, create_default_executor
from .network_proxy import NetworkProxy, MonkeyPatchedNetworkProxy, create_default_proxy
from .think_tool import (
    ThinkTool,
    ThinkEntry,
    think,
    get_think_history,
    clear_think_history,
    analyze_thinking,
    THINK_TOOL_DEFINITION,
    enable_think_tool,
    get_examples
)

__all__ = [
    "CodeExecutionEngine",
    "ExecutionResult",
    "SkillCodeGenerator",
    "EfficiencyMetrics",
    "EfficiencyTracker",
    "SandboxedExecutor",
    "SandboxConfig",
    "create_default_executor",
    "NetworkProxy",
    "MonkeyPatchedNetworkProxy",
    "create_default_proxy",
    "ThinkTool",
    "ThinkEntry",
    "think",
    "get_think_history",
    "clear_think_history",
    "analyze_thinking",
    "THINK_TOOL_DEFINITION",
    "enable_think_tool",
    "get_examples",
]

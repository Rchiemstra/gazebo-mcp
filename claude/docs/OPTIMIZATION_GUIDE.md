# Optimization Guide

Comprehensive guide to optimizing token usage and performance in Claude Code.

---

## 📋 Overview

This guide covers optimization strategies for:
- Token efficiency (95-99% reduction possible!)
- Response time optimization
- Context window management
- Cost optimization
- Performance patterns

---

## 🎯 Token Efficiency Fundamentals

### The 95-99% Rule

**Problem:** Returning full results wastes tokens
- Full codebase analysis: 50,000 tokens
- Agent receives, processes, filters
- 95% discarded

**Solution:** Progressive disclosure + local filtering
- Summary first: 500 tokens
- Filter locally: 0 tokens (runs in code)
- Details on demand: 2,000 tokens
- **Savings: 95-99%**

### Three-Tier Pattern

```python
# Tier 1: Summary (500 tokens)
result = analyze_codebase("src/", response_format="summary")
# Returns: counts, metrics, overview

# Tier 2: Filtered (2,000 tokens) + Local Filter (0 tokens)
result = analyze_codebase("src/", response_format="filtered")
filtered = ResultFilter.search(result.data, "auth")  # Local!
# Returns: structured data, filter in Python

# Tier 3: Detailed (50,000 tokens)
result = analyze_codebase("src/", response_format="detailed")
# Only use when absolutely necessary
```

---

## 💡 Progressive Disclosure Patterns

### Pattern 1: Summary → Details

**Use When:** Exploring unfamiliar code

```python
# Step 1: Get overview (500 tokens)
from skills.code_analysis.operations import analyze_codebase

summary = analyze_codebase(
    "src/",
    response_format="summary"
)

print(f"Total files: {summary.data['total_files']}")
print(f"Total functions: {summary.data['total_functions']}")
print(f"Avg complexity: {summary.data['avg_complexity']}")

# Step 2: Decide what to explore
if summary.data['avg_complexity'] > 10:
    # Get details for complex files only
    details = analyze_codebase(
        "src/",
        response_format="detailed",
        min_complexity=10  # Filter at source
    )
```

**Token Savings:** 49,500 tokens (99%)

### Pattern 2: Filtered + Local Processing

**Use When:** Working with large datasets

```python
# Step 1: Get structured data (2,000 tokens)
from skills.code_analysis.operations import analyze_codebase
from skills.common.filters import ResultFilter

result = analyze_codebase(
    "src/",
    response_format="filtered"  # Optimized for filtering
)

# Step 2: Filter locally (0 tokens - runs in Python!)
auth_files = ResultFilter.search(
    result.data["files"],
    "auth",
    fields=["path", "name"]
)

# Step 3: Get top items (0 tokens - still local!)
complex_auth = ResultFilter.top_n_by_field(
    auth_files,
    "complexity",
    n=5
)

# Step 4: Only now send to agent (500 tokens)
print(f"Top 5 complex auth files: {complex_auth}")
```

**Token Savings:** 49,500 tokens (99%)

**Key Insight:** Agent only sees 5 filtered files, not all 10,000!

### Pattern 3: Cached Results

**Use When:** Repeated access to same data

```python
# First call: Full analysis (2,000 tokens)
result = analyze_codebase("src/", response_format="filtered")

# Cache results
cache = result.data

# Subsequent filters: (0 tokens each!)
auth_files = ResultFilter.search(cache["files"], "auth")
payment_files = ResultFilter.search(cache["files"], "payment")
api_files = ResultFilter.search(cache["files"], "api")
# All zero tokens - filtering cached data!
```

**Token Savings:** 6,000 tokens (for 3 additional queries)

---

## 🚀 Skill-Specific Optimizations

### Code Analysis Optimization

```python
# ❌ Inefficient (50,000 tokens)
result = analyze_codebase("src/")  # Gets everything
for file in result.data["files"]:
    if "payment" in file["path"]:
        print(file)

# ✅ Efficient (500 tokens)
result = analyze_codebase(
    "src/",
    response_format="filtered",
    path_pattern="*payment*"  # Filter at source
)
# OR
result = analyze_codebase("src/", response_format="filtered")
payment_files = ResultFilter.search(result.data["files"], "payment")
```

### Test Orchestrator Optimization

```python
# ❌ Inefficient (5,000 tokens)
result = generate_tests(
    "payment.py",
    response_format="detailed"  # Full test code
)

# ✅ Efficient (500 tokens)
result = generate_tests(
    "payment.py",
    response_format="summary"  # Just stats
)
# See: 10 tests generated, 90% coverage
# Get details only if needed

# ✅ Most Efficient (1,000 tokens)
result = generate_tests(
    "payment.py",
    response_format="concise"  # Test names + locations
)
# Enough to understand what was generated
```

### Learning Plan Manager Optimization

```python
# ❌ Inefficient (15,000 tokens)
plan = load_plan("navigation-plan.md")
# Loads entire plan with all phases

# ✅ Efficient (1,000 tokens)
plan = load_plan(
    "navigation-plan.md",
    response_format="progress"  # Just current status
)
# See current phase, progress, next steps

# ✅ Most Efficient (500 tokens)
plan = load_plan(
    "navigation-plan.md",
    response_format="summary"  # Overview only
)
# See topic, phases count, overall progress
```

---

## 📊 ResultFilter Mastery

### Filter Operations (All Zero Tokens!)

```python
from skills.common.filters import ResultFilter

# Sample data (assume we have this)
files = analyze_codebase("src/", response_format="filtered").data["files"]

# Search (0 tokens)
auth_files = ResultFilter.search(files, "auth", ["path", "name"])

# Top N (0 tokens)
complex_files = ResultFilter.top_n_by_field(files, "complexity", 10)

# Filter by field (0 tokens)
python_files = ResultFilter.filter_by_field(files, "language", "python")

# Limit (0 tokens)
first_10 = ResultFilter.limit(files, 10)

# Summarize (0 tokens)
summary = ResultFilter.summarize(files)

# Combine filters (0 tokens)
result = ResultFilter.search(files, "payment")
result = ResultFilter.filter_by_field(result, "language", "python")
result = ResultFilter.top_n_by_field(result, "complexity", 5)
# 3 operations, still 0 tokens!
```

### When to Use ResultFilter

**✅ Use ResultFilter When:**
- Working with large datasets (100+ items)
- Need to filter/search results
- Multiple filter operations needed
- Repeated access to same data

**❌ Don't Use ResultFilter When:**
- Dataset is small (<10 items)
- Need agent to interpret results
- Complex logic required (agent better at this)

---

## 🎯 Sub-Agent Optimization

### Pattern: Summarized Returns

When one agent invokes another:

```python
# ❌ Inefficient
def analyze_project():
    """Parent agent."""
    # Sub-agent returns full results (50,000 tokens)
    files = file_search_agent.search("payment")
    # Parent agent receives all 1,000 files
    # Wastes 49,000 tokens

# ✅ Efficient
def analyze_project():
    """Parent agent."""
    # Sub-agent returns summary (1,000 tokens)
    summary = file_search_agent.search(
        "payment",
        return_format="summary"
    )
    # Parent receives:
    # - File count: 45
    # - Top 10 files with notes
    # - Path to full results file
    # Saves 49,000 tokens (98%)
```

**Key Points:**
- Sub-agents return summaries
- Full results saved to files
- Parent can request details if needed
- 95-98% token savings

---

## ⚡ Response Time Optimization

### Parallel Operations

```python
# ❌ Sequential (slow)
result1 = analyze_file("payment.py")  # 2 seconds
result2 = analyze_file("auth.py")     # 2 seconds
result3 = analyze_file("api.py")      # 2 seconds
# Total: 6 seconds

# ✅ Parallel (fast)
import concurrent.futures

files = ["payment.py", "auth.py", "api.py"]

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = list(executor.map(analyze_file, files))
# Total: 2 seconds (3x faster!)
```

### Batch Operations

```python
# ❌ Individual calls
for file in files:
    analyze_file(file)  # 100 API calls

# ✅ Batch call
analyze_files_batch(files)  # 1 API call
```

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def analyze_file_cached(file_path):
    """Cached file analysis."""
    return analyze_file(file_path)

# First call: analyzes file
result1 = analyze_file_cached("payment.py")

# Second call: returns cached (instant!)
result2 = analyze_file_cached("payment.py")
```

---

## 💰 Cost Optimization

### Token Budget Management

```python
class TokenBudget:
    """Track token usage."""

    def __init__(self, budget=100000):
        self.budget = budget
        self.used = 0

    def check(self, operation_cost):
        """Check if operation fits budget."""
        if self.used + operation_cost > self.budget:
            raise ValueError(f"Exceeds budget: {operation_cost} tokens")

    def use(self, cost):
        """Record token usage."""
        self.used += cost

# Usage
budget = TokenBudget(budget=100000)

# Check before expensive operation
if result_format == "detailed":
    budget.check(50000)  # Will raise if exceeds

result = analyze_codebase("src/", response_format="summary")
budget.use(500)  # Record actual usage

print(f"Budget remaining: {budget.budget - budget.used}")
```

### Smart Response Format Selection

```python
def smart_analyze(path, token_budget):
    """Analyze with budget awareness."""

    # Estimate tokens needed
    file_count = len(list(Path(path).rglob("*.py")))

    if file_count < 10:
        # Small project: detailed ok (2,000 tokens)
        return analyze_codebase(path, response_format="detailed")

    elif token_budget > 5000:
        # Large budget: filtered + local filtering (2,000 tokens)
        return analyze_codebase(path, response_format="filtered")

    else:
        # Low budget: summary only (500 tokens)
        return analyze_codebase(path, response_format="summary")
```

---

## 📈 Performance Metrics

### Measure Token Efficiency

```python
def measure_efficiency(operation, *args, **kwargs):
    """Measure token efficiency."""
    import time

    # Baseline: detailed (high tokens)
    start = time.time()
    detailed_result = operation(*args, response_format="detailed")
    detailed_time = time.time() - start
    detailed_tokens = len(str(detailed_result.data))  # Approximate

    # Optimized: summary (low tokens)
    start = time.time()
    summary_result = operation(*args, response_format="summary")
    summary_time = time.time() - start
    summary_tokens = len(str(summary_result.data))  # Approximate

    # Report
    print(f"Detailed: {detailed_tokens} tokens, {detailed_time:.2f}s")
    print(f"Summary: {summary_tokens} tokens, {summary_time:.2f}s")
    print(f"Token reduction: {(1 - summary_tokens/detailed_tokens)*100:.1f}%")
    print(f"Time improvement: {(1 - summary_time/detailed_time)*100:.1f}%")
```

### Track Performance Over Time

```python
import json
from datetime import datetime

class PerformanceTracker:
    """Track performance metrics."""

    def __init__(self, log_file="metrics.jsonl"):
        self.log_file = log_file

    def log(self, operation, tokens_used, duration, metadata=None):
        """Log performance data."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "tokens": tokens_used,
            "duration": duration,
            "metadata": metadata or {}
        }

        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def analyze(self):
        """Analyze performance trends."""
        entries = []
        with open(self.log_file) as f:
            for line in f:
                entries.append(json.loads(line))

        # Compute metrics
        total_tokens = sum(e["tokens"] for e in entries)
        avg_tokens = total_tokens / len(entries)
        total_duration = sum(e["duration"] for e in entries)

        print(f"Total operations: {len(entries)}")
        print(f"Total tokens: {total_tokens:,}")
        print(f"Avg tokens/op: {avg_tokens:.0f}")
        print(f"Total time: {total_duration:.2f}s")
```

---

## 🎓 Optimization Checklist

### Before Each Operation

- [ ] Can I use `response_format="summary"`?
- [ ] Can I filter at the source?
- [ ] Can I use ResultFilter instead?
- [ ] Can I cache the results?
- [ ] Can I run operations in parallel?
- [ ] Am I within my token budget?

### Code Review Checklist

- [ ] All operations use appropriate response_format
- [ ] Large datasets use filtered + ResultFilter
- [ ] Sub-agents return summaries
- [ ] Repeated operations are cached
- [ ] Parallel operations where possible
- [ ] Token usage is measured

### Architecture Checklist

- [ ] Progressive disclosure pattern used
- [ ] Local filtering preferred
- [ ] Agent invocations minimized
- [ ] Results cached when appropriate
- [ ] Performance metrics tracked

---

## 📊 Optimization Impact Summary

| Pattern | Token Savings | Use Case |
|---------|---------------|----------|
| Summary format | 90-95% | Initial exploration |
| Filtered + ResultFilter | 95-99% | Large datasets |
| Sub-agent summarization | 95-98% | Agent coordination |
| Caching | 100% (2nd+ call) | Repeated access |
| Parallel operations | 0% tokens, 3-5x speed | Independent operations |

### Real-World Example

**Before Optimization:**
```python
# Analyze 10,000 files
result = analyze_codebase("src/")  # 50,000 tokens
# Find payment files
payment_files = [f for f in result.data["files"] if "payment" in f["path"]]
# Get top 5 complex
top_5 = sorted(payment_files, key=lambda x: x["complexity"], reverse=True)[:5]

# Total: 50,000 tokens
```

**After Optimization:**
```python
# Analyze 10,000 files
result = analyze_codebase("src/", response_format="filtered")  # 2,000 tokens
# Find payment files (local!)
payment_files = ResultFilter.search(result.data["files"], "payment")  # 0 tokens
# Get top 5 complex (local!)
top_5 = ResultFilter.top_n_by_field(payment_files, "complexity", 5)  # 0 tokens

# Total: 2,000 tokens
# Savings: 48,000 tokens (96%)
```

---

## 📚 Related Documentation

- `../CLAUDE.md` → Token Efficiency Patterns
- `WORKFLOW_GUIDE.md` - Efficient workflows
- `TOOL_ALLOWLISTING_GUIDE.md` - Tool optimization
- `SANDBOXING_GUIDE.md` - Security with efficiency
- `ANTHROPIC_BEST_PRACTICES_IMPLEMENTATION_PLAN.md` - System design

---

## 🎯 Quick Reference

### Response Format Decision Tree

```
Is data > 1000 items?
├─ Yes → Use "filtered" + ResultFilter (99% savings)
└─ No
   ├─ Is this initial exploration?
   │  └─ Yes → Use "summary" (90-95% savings)
   └─ No
      ├─ Need full details?
      │  └─ Yes → Use "detailed" (0% savings, necessary)
      └─ No → Use "concise" (80-90% savings)
```

### Common Optimizations

```python
# Always start with summary
result = operation(response_format="summary")

# Use ResultFilter for large datasets
filtered = ResultFilter.search(data, query)

# Cache repeated operations
@lru_cache
def cached_operation(): ...

# Parallelize independent operations
with ThreadPoolExecutor() as executor:
    results = executor.map(operation, items)

# Track token usage
budget.use(estimated_tokens)
```

---

**Remember:** The best optimization is the operation you don't need to run. Always ask: "Can I do this locally instead?" 🚀

*Last Updated: 2025-11-08*

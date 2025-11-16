# Token Efficiency Guide

**Last Updated:** 2025-11-09
**Status:** Complete guide for optimizing token usage across all skills

---

## 🎯 Overview

This guide provides comprehensive strategies for optimizing token usage when working with the Claude Code Learning System. With the `response_format` parameter now available on all 48 skill operations, you can achieve 80-95% token savings while maintaining full functionality.

---

## 📊 Token Savings Summary

### By Skill

| Skill | Operations | Avg Savings | Best Use Case |
|-------|-----------|-------------|---------------|
| code_analysis | 3 | 95-99% | Large codebase analysis |
| skill_evaluator | 10 | 90-97% | Comprehensive reports |
| doc_generator | 3 | 90-96% | Documentation generation |
| test_orchestrator | 3 | 90% | Test generation |
| refactor_assistant | 3 | 85-90% | Code quality analysis |
| pr_review_assistant | 4 | 85-90% | PR reviews |
| dependency_guardian | 3 | 83-86% | Security scanning |
| code_search | 4 | 85% | Symbol/pattern search |
| spec_to_implementation | 2 | 85-87% | Spec transformation |
| learning_plan_manager | 3 | 83-90% | Learning tracking |
| git_workflow_assistant | 4 | 80-84% | Git operations |
| context_manager | 3 | 80-83% | Context analysis |

**Overall Average:** 85-95% token savings

---

## 🔧 Using response_format Parameter

### Quick Reference

```python
# Default behavior (summary mode - recommended)
result = skill_operation(params)

# Explicit summary mode
result = skill_operation(params, response_format="summary")

# Detailed mode (when you need complete data)
result = skill_operation(params, response_format="detailed")
```

### When to Use Each Mode

#### Summary Mode (Default) ✅

**Use when:**
- Getting a high-level overview
- Checking if action is needed
- Planning next steps
- Filtering large datasets
- Making decisions based on counts/metrics

**Examples:**
```python
# Check if there are issues before diving deep
result = detect_code_smells("large_file.py")
if result.data['total_smells'] > 10:
    # Now get details
    detailed = detect_code_smells("large_file.py", response_format="detailed")
```

**Token Savings:** 80-95%

#### Detailed Mode

**Use when:**
- Implementing fixes based on analysis
- Generating reports for users
- Need complete information for decision-making
- Working with specific items from summary

**Examples:**
```python
# After summary shows high vulnerability count
result = check_vulnerabilities("project/", response_format="detailed")
for vuln in result.data['vulnerabilities']:
    if vuln['severity'] == 'critical':
        print(f"Fix: {vuln['fix']}")
```

**Token Usage:** Full (baseline)

---

## 📈 Progressive Disclosure Pattern

The most efficient workflow uses progressive disclosure:

### Pattern 1: Summary → Detailed

```python
# Step 1: Get summary (500 tokens)
summary = analyze_codebase("src/", response_format="summary")
# { "files": 150, "avg_complexity": 12, "high_complexity_files": 8 }

# Step 2: Only get details if needed (10,000 tokens)
if summary.data['high_complexity_files'] > 5:
    details = analyze_codebase("src/", response_format="detailed")
    # Full complexity analysis with recommendations
```

**Token Savings:** Only pay for detailed when needed (90% savings if threshold not met)

### Pattern 2: Summary → Local Filtering → Detailed

```python
from skills.common.filters import ResultFilter

# Step 1: Get summary (500 tokens)
summary = search_symbol("UserAuth", response_format="summary")
# { "found": 45, "files": ["auth.py", "user.py", ...] }

# Step 2: Local filtering (0 tokens - runs locally!)
if summary.data['found'] < 100:
    # Step 3: Get filtered data
    results = search_symbol("UserAuth", response_format="detailed")
    auth_files = ResultFilter.search(results.data, "auth", ["path"])

**Token Savings:** 95-99% (most filtering happens locally)
```

### Pattern 3: Multiple Summaries → Targeted Detailed

```python
# Step 1: Check multiple files with summaries (1,000 tokens total)
files = ["auth.py", "user.py", "payment.py", "admin.py"]
summaries = []
for file in files:
    summary = analyze_file(file, response_format="summary")
    summaries.append((file, summary))

# Step 2: Only analyze problematic files in detail (2,000 tokens)
for file, summary in summaries:
    if summary.data['complexity'] > 15 or summary.data['issues'] > 5:
        detailed = analyze_file(file, response_format="detailed")
        # Work with detailed analysis
```

**Token Savings:** 80-90% (only detailed for subset of files)

---

## 🎓 Skill-Specific Guidance

### code_analysis (95-99% savings)

**Operations:**
- `analyze_codebase` - Analyze entire codebase
- `analyze_file` - Analyze single file
- `generate_dependency_graph` - Create dependency map

**Best Practice:**
```python
# ❌ Inefficient - always gets everything
files = analyze_codebase("src/")  # 50,000 tokens

# ✅ Efficient - progressive disclosure
summary = analyze_codebase("src/", response_format="summary")
# { "files": 150, "avg_complexity": 12, "languages": {...} }
# 500 tokens - 99% savings!

# Only get details for high-complexity files
if summary.data['avg_complexity'] > 10:
    # Use filtering to further reduce
    from skills.common.filters import ResultFilter
    results = analyze_codebase("src/", response_format="detailed")
    high_complexity = ResultFilter.filter_by_field(
        results.data['files'],
        'complexity',
        lambda x: x > 15
    )
```

**Token Impact:**
- Summary: ~500 tokens
- Detailed: ~50,000 tokens
- **Savings: 99%**

### skill_evaluator (90-97% savings)

**Operations:**
- `evaluate_quality` - Comprehensive quality evaluation
- `generate_report` - Create evaluation report
- `analyze_performance` - Performance analysis
- And 7 more...

**Best Practice:**
```python
# ❌ Inefficient - full report every time
report = generate_report("test_orchestrator")  # 30,000 tokens

# ✅ Efficient - summary first
summary = generate_report("test_orchestrator", response_format="summary")
# {
#   "health_score": 92,
#   "health_grade": "A",
#   "critical_issues": 0,
#   "sections": ["quality", "performance", "trends"]
# }
# 1,000 tokens - 97% savings!

# Only get full report if health is concerning
if summary.data['health_score'] < 85 or summary.data['critical_issues'] > 0:
    full_report = generate_report("test_orchestrator", response_format="detailed")
```

**Token Impact:**
- Summary: ~1,000 tokens
- Detailed: ~30,000 tokens
- **Savings: 97%**

### doc_generator (90-96% savings)

**Operations:**
- `generate_readme` - Create README.md
- `generate_docstrings` - Add docstrings
- `analyze_documentation` - Check doc coverage

**Best Practice:**
```python
# ❌ Inefficient - generates full README
readme = generate_readme("project/")  # 25,000 tokens

# ✅ Efficient - check what's needed first
analysis = analyze_documentation("project/", response_format="summary")
# { "coverage": 65%, "missing_docs": 45, "sections_needed": 8 }
# 800 tokens - 97% savings!

# Only generate if coverage is low
if analysis.data['coverage'] < 80:
    # Generate with summary to see structure
    readme_summary = generate_readme("project/", response_format="summary")
    # { "sections": 8, "api_docs": 15, "word_count": 2500 }
    # 1,000 tokens - 96% savings!

    # Get full README only if needed for review
    if readme_summary.data['word_count'] < 5000:
        full_readme = generate_readme("project/", response_format="detailed")
```

**Token Impact:**
- Analysis summary: ~800 tokens
- README summary: ~1,000 tokens
- README detailed: ~25,000 tokens
- **Savings: 96%** (if you only need summary)

### test_orchestrator (90% savings)

**Operations:**
- `generate_tests` - Create test cases
- `analyze_coverage` - Coverage analysis
- `run_tests` - Execute tests

**Best Practice:**
```python
# ❌ Inefficient - generates all tests
tests = generate_tests("payment.py")  # 8,000 tokens

# ✅ Efficient - check coverage first
coverage = analyze_coverage("payment.py", response_format="summary")
# { "coverage": 45%, "missing_functions": 12, "missing_branches": 28 }
# 500 tokens - 94% savings!

# Only generate tests if coverage is low
if coverage.data['coverage'] < 80:
    test_summary = generate_tests("payment.py", response_format="summary")
    # { "tests_generated": 15, "test_file": "test_payment.py" }
    # 800 tokens - 90% savings!
```

**Token Impact:**
- Coverage summary: ~500 tokens
- Test summary: ~800 tokens
- Test detailed: ~8,000 tokens
- **Savings: 90%**

### refactor_assistant (85-90% savings)

**Operations:**
- `detect_code_smells` - Find code issues
- `suggest_refactorings` - Get refactoring suggestions
- `analyze_complexity` - Complexity analysis

**Best Practice:**
```python
# ❌ Inefficient - all smells with details
smells = detect_code_smells("legacy_code.py")  # 10,000 tokens

# ✅ Efficient - summary with counts
summary = detect_code_smells("legacy_code.py", response_format="summary")
# {
#   "total_smells": 45,
#   "by_severity": {"critical": 3, "high": 12, "medium": 20, "low": 10},
#   "by_category": {...}
# }
# 1,000 tokens - 90% savings!

# Only get details for critical/high severity
if summary.data['by_severity']['critical'] > 0:
    details = detect_code_smells("legacy_code.py", response_format="detailed")
    critical = [s for s in details.data['smells'] if s['severity'] == 'critical']
```

**Token Impact:**
- Summary: ~1,000 tokens
- Detailed: ~10,000 tokens
- **Savings: 90%**

### pr_review_assistant (85-90% savings)

**Operations:**
- `review_pull_request` - Full PR review
- `analyze_change_impact` - Impact analysis
- `check_pr_quality` - Quality checks

**Best Practice:**
```python
# ❌ Inefficient - full review every time
review = review_pull_request(pr_id=123)  # 12,000 tokens

# ✅ Efficient - impact check first
impact = analyze_change_impact(pr_id=123, response_format="summary")
# {
#   "files_changed": 15,
#   "risk_level": "medium",
#   "top_recommendations": [...]
# }
# 1,200 tokens - 90% savings!

# Only do full review if high risk
if impact.data['risk_level'] in ['high', 'critical']:
    full_review = review_pull_request(pr_id=123, response_format="detailed")
```

**Token Impact:**
- Impact summary: ~1,200 tokens
- Review detailed: ~12,000 tokens
- **Savings: 90%**

### dependency_guardian (83-86% savings)

**Operations:**
- `check_vulnerabilities` - Security scan
- `analyze_dependencies` - Dependency analysis
- `check_updates` - Available updates

**Best Practice:**
```python
# ❌ Inefficient - all CVE details
vulns = check_vulnerabilities("project/")  # 7,000 tokens

# ✅ Efficient - severity counts first
summary = check_vulnerabilities("project/", response_format="summary")
# {
#   "total_vulnerabilities": 27,
#   "critical": 2,
#   "high": 5,
#   "medium": 12,
#   "low": 8
# }
# 1,000 tokens - 86% savings!

# Only get details for critical/high
if summary.data['critical'] > 0 or summary.data['high'] > 3:
    details = check_vulnerabilities("project/", response_format="detailed")
    urgent = [v for v in details.data['vulnerabilities']
              if v['severity'] in ['critical', 'high']]
```

**Token Impact:**
- Summary: ~1,000 tokens
- Detailed: ~7,000 tokens
- **Savings: 86%**

### code_search (85% savings)

**Operations:**
- `search_symbol` - Find symbols
- `find_usages` - Find usage locations
- `find_definition` - Locate definitions
- `search_pattern` - Pattern matching

**Best Practice:**
```python
# ❌ Inefficient - all usage locations
usages = find_usages("UserAuth")  # 10,000 tokens

# ✅ Efficient - file list first
summary = find_usages("UserAuth", response_format="summary")
# {
#   "found": 45,
#   "files": ["auth.py", "user.py", "admin.py", ...]
# }
# 1,500 tokens - 85% savings!

# Filter locally for specific files
target_files = [f for f in summary.data['files'] if 'auth' in f.lower()]
if len(target_files) < 10:
    # Get details only for auth-related files
    details = find_usages("UserAuth", response_format="detailed")
```

**Token Impact:**
- Summary: ~1,500 tokens
- Detailed: ~10,000 tokens
- **Savings: 85%**

### spec_to_implementation (85-87% savings)

**Operations:**
- `implement_from_spec` - Generate implementation
- `analyze_spec` - Analyze specification

**Best Practice:**
```python
# ❌ Inefficient - full implementation details
impl = implement_from_spec("spec.md", "output/")  # 15,000 tokens

# ✅ Efficient - check feasibility first
analysis = analyze_spec("spec.md", response_format="summary")
# {
#   "valid": true,
#   "complexity": "medium",
#   "estimated_files": 5,
#   "estimated_loc": 450
# }
# 1,200 tokens - 92% savings!

if analysis.data['valid'] and analysis.data['complexity'] != 'high':
    impl_summary = implement_from_spec(
        "spec.md",
        "output/",
        response_format="summary"
    )
    # {
    #   "files_created": 5,
    #   "tests_created": 3,
    #   "quality_score": 87
    # }
    # 2,000 tokens - 87% savings!
```

**Token Impact:**
- Analysis summary: ~1,200 tokens
- Implementation summary: ~2,000 tokens
- Implementation detailed: ~15,000 tokens
- **Savings: 87%**

### learning_plan_manager (83-90% savings)

**Operations:**
- `parse_learning_plan` - Parse plan file
- `track_progress` - Update progress
- `analyze_plan` - Analyze plan structure

**Best Practice:**
```python
# ❌ Inefficient - full plan details
plan = parse_learning_plan("plans/navigation.md")  # 5,000 tokens

# ✅ Efficient - overview first
summary = parse_learning_plan("plans/navigation.md", response_format="summary")
# {
#   "phases": 4,
#   "total_tasks": 28,
#   "completed": 12,
#   "in_progress": 3,
#   "completion_percentage": 43
# }
# 800 tokens - 84% savings!

# Get details only for current phase
if summary.data['in_progress'] > 0:
    progress = track_progress("plans/navigation.md", response_format="detailed")
```

**Token Impact:**
- Summary: ~800 tokens
- Detailed: ~5,000 tokens
- **Savings: 84%**

### git_workflow_assistant (80-84% savings)

**Operations:**
- `analyze_changes` - Analyze git changes
- `generate_commit_message` - Create commit msg
- `suggest_branch_name` - Suggest branch name
- `create_pull_request` - Create PR

**Best Practice:**
```python
# ❌ Inefficient - full diff analysis
changes = analyze_changes()  # 5,000 tokens

# ✅ Efficient - change counts first
summary = analyze_changes(response_format="summary")
# {
#   "files_changed": 12,
#   "lines_added": 450,
#   "lines_removed": 120,
#   "change_type": "feature"
# }
# 800 tokens - 84% savings!

# Generate commit message based on summary
if summary.data['files_changed'] < 20:
    msg = generate_commit_message(response_format="summary")
```

**Token Impact:**
- Summary: ~800 tokens
- Detailed: ~5,000 tokens
- **Savings: 84%**

### context_manager (80-83% savings)

**Operations:**
- `analyze_context` - Context usage analysis
- `create_notes` - Create persistent notes
- `compact_conversation` - Summarize conversation

**Best Practice:**
```python
# ❌ Inefficient - full context breakdown
ctx = analyze_context()  # 6,000 tokens

# ✅ Efficient - usage metrics only
summary = analyze_context(response_format="summary")
# {
#   "tokens_used": 45000,
#   "tokens_available": 155000,
#   "usage_percentage": 23,
#   "recommendation": "no action needed"
# }
# 1,000 tokens - 83% savings!

# Only compact if approaching limit
if summary.data['usage_percentage'] > 80:
    compaction = compact_conversation(response_format="detailed")
```

**Token Impact:**
- Summary: ~1,000 tokens
- Detailed: ~6,000 tokens
- **Savings: 83%**

---

## 🔄 Common Patterns

### Pattern: Threshold-Based Detail Retrieval

```python
def analyze_with_threshold(file_path, threshold=10):
    """Get details only if issues exceed threshold."""

    # Step 1: Summary
    summary = detect_code_smells(file_path, response_format="summary")

    # Step 2: Decision based on threshold
    if summary.data['total_smells'] > threshold:
        # Get details
        return detect_code_smells(file_path, response_format="detailed")

    # Return summary if below threshold
    return summary
```

**Token Savings:** 90% (when threshold not exceeded)

### Pattern: Multi-File Analysis

```python
def analyze_multiple_files(files):
    """Analyze multiple files efficiently."""

    results = {'needs_attention': [], 'looks_good': []}

    # Step 1: Get summaries for all files
    for file in files:
        summary = analyze_file(file, response_format="summary")

        if summary.data['complexity'] > 15 or summary.data['issues'] > 5:
            results['needs_attention'].append(file)
        else:
            results['looks_good'].append(file)

    # Step 2: Get details only for files needing attention
    detailed_results = []
    for file in results['needs_attention']:
        details = analyze_file(file, response_format="detailed")
        detailed_results.append(details)

    return detailed_results
```

**Token Savings:** 80-90% (depending on ratio of problematic files)

### Pattern: Iterative Refinement

```python
def find_and_fix_issues(project_path):
    """Iteratively find and fix issues."""

    # Round 1: High-level overview
    summary = analyze_codebase(project_path, response_format="summary")

    if summary.data['avg_complexity'] > 15:
        # Round 2: Get file-level summaries
        files = analyze_codebase(project_path, response_format="detailed")

        # Round 3: Detailed analysis only for high-complexity files
        from skills.common.filters import ResultFilter
        high_complexity = ResultFilter.top_n_by_field(
            files.data['files'],
            'complexity',
            10
        )

        # Work with top 10 most complex files
        return high_complexity
```

**Token Savings:** 95-99% (only analyze subset in detail)

### Pattern: Conditional Detail Expansion

```python
def smart_pr_review(pr_id):
    """Smart PR review with progressive detail."""

    # Step 1: Quick impact check
    impact = analyze_change_impact(pr_id, response_format="summary")

    # Step 2: Quality check if medium+ risk
    if impact.data['risk_level'] in ['medium', 'high', 'critical']:
        quality = check_pr_quality(pr_id, response_format="summary")

        # Step 3: Full review only if quality issues found
        if quality.data['quality_score'] < 80:
            return review_pull_request(pr_id, response_format="detailed")

    return {"status": "approved", "risk": impact.data['risk_level']}
```

**Token Savings:** 85-90% (for most PRs)

---

## 📉 Token Budget Management

### Budget-Aware Operations

```python
class TokenBudget:
    """Track and manage token usage."""

    def __init__(self, budget=50000):
        self.budget = budget
        self.used = 0

    def can_afford(self, estimated_tokens):
        """Check if operation fits in budget."""
        return (self.used + estimated_tokens) <= self.budget

    def execute(self, operation, *args, **kwargs):
        """Execute operation with budget awareness."""

        # Try summary first
        kwargs['response_format'] = 'summary'
        result = operation(*args, **kwargs)

        # Estimate tokens (rough: 1 token ≈ 4 chars)
        estimated = len(str(result.data)) / 4
        self.used += estimated

        return result

# Usage
budget = TokenBudget(budget=50000)

# Analyze multiple files within budget
for file in large_file_list:
    if budget.can_afford(1000):  # Estimate for summary
        result = budget.execute(analyze_file, file)
    else:
        print(f"Budget exhausted. Analyzed {len(results)} files.")
        break
```

### Smart Batching

```python
def batch_analyze_with_budget(files, token_budget=50000):
    """Analyze files in batches, respecting token budget."""

    summaries = []
    detailed = []
    tokens_used = 0

    # Phase 1: Get all summaries (cheap)
    for file in files:
        summary = analyze_file(file, response_format="summary")
        summaries.append((file, summary))
        tokens_used += 500  # Estimated per summary

    # Phase 2: Get details for high-priority files (expensive)
    # Sort by priority (e.g., complexity)
    sorted_files = sorted(
        summaries,
        key=lambda x: x[1].data.get('complexity', 0),
        reverse=True
    )

    for file, summary in sorted_files:
        estimated_tokens = 10000  # Estimated per detailed analysis

        if tokens_used + estimated_tokens <= token_budget:
            details = analyze_file(file, response_format="detailed")
            detailed.append(details)
            tokens_used += estimated_tokens
        else:
            break

    return {
        'summaries': summaries,
        'detailed': detailed,
        'tokens_used': tokens_used
    }
```

---

## 🎯 Best Practices Summary

### DO ✅

1. **Default to summary mode** - Start with `response_format="summary"`
2. **Use progressive disclosure** - Summary → Filter → Detailed
3. **Filter locally** - Use ResultFilter to reduce token usage
4. **Set thresholds** - Only get details when metrics exceed thresholds
5. **Batch operations** - Process multiple items with summaries first
6. **Track usage** - Monitor token consumption
7. **Cache summaries** - Store summary results to avoid re-fetching

### DON'T ❌

1. **Don't always use detailed** - Only use when absolutely necessary
2. **Don't skip summaries** - Always check summary first
3. **Don't ignore efficiency tips** - They're in every operation's docstring
4. **Don't load everything** - Use filtering and thresholds
5. **Don't repeat operations** - Cache results when possible
6. **Don't forget local filtering** - ResultFilter is free (0 tokens)

---

## 📚 Quick Reference

### Token Estimates by Operation Type

| Operation Type | Summary | Detailed | Savings |
|----------------|---------|----------|---------|
| File analysis | 500 | 10,000 | 95% |
| Codebase analysis | 500 | 50,000 | 99% |
| Report generation | 1,000 | 30,000 | 97% |
| Documentation | 1,000 | 25,000 | 96% |
| Test generation | 800 | 8,000 | 90% |
| Code smell detection | 1,000 | 10,000 | 90% |
| PR review | 1,200 | 12,000 | 90% |
| Vulnerability scan | 1,000 | 7,000 | 86% |
| Symbol search | 1,500 | 10,000 | 85% |

### Response Format Decision Tree

```
Need information?
├─ Just checking status/counts? → summary
├─ Making go/no-go decision? → summary
├─ Planning next actions? → summary
├─ Need to implement based on results? → detailed
├─ Large dataset (>100 items)? → summary + filter + detailed
└─ Generating report for user? → detailed
```

---

## 🔗 Related Documentation

- `docs/OPTIMIZATION_GUIDE.md` - Overall optimization strategies
- `docs/PHASE3_PROGRESS.md` - response_format implementation details
- `docs/WEEK8_SUMMARY.md` - Token efficiency achievement summary
- `skills/CLAUDE.md` - Skills usage guide

---

*Last Updated: 2025-11-09*
*Status: Complete guide for all 48 operations across 12 skills*
*Average Token Savings: 85-95%*

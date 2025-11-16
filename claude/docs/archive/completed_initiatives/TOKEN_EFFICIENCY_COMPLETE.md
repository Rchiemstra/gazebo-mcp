# Token Efficiency Guide - Complete Reference

**Last Updated:** 2025-11-10
**Status:** Complete guide for creating AND using efficient Claude Code skills
**Applies to:** All skills, agents, and workflow tools

---

## 📖 Table of Contents

### Part 1: Creating Efficient Skills
1. [Core Principles](#part-1-creating-efficient-skills)
2. [Progressive Disclosure Pattern](#progressive-disclosure-pattern)
3. [Model Selection Strategy](#model-selection-strategy)
4. [Skill Structure Template](#skill-structure-template)
5. [Reference Documentation Strategy](#reference-documentation-strategy)

### Part 2: Using Skills Efficiently
6. [Using response_format Parameter](#part-2-using-skills-efficiently)
7. [Progressive Disclosure in Practice](#progressive-disclosure-in-practice)
8. [Skill-Specific Guidance](#skill-specific-guidance)
9. [Common Patterns](#common-patterns)
10. [Token Budget Management](#token-budget-management)

### Part 3: Optimization Techniques
11. [Removing Redundancy](#optimization-techniques)
12. [Compact Templates](#compact-output-templates)
13. [Example Extraction](#example-extraction)
14. [Measurement & Metrics](#measurement--metrics)

### Part 4: Best Practices
15. [Implementation Checklist](#implementation-checklist)
16. [Do's and Don'ts](#best-practices-summary)
17. [Quick Reference](#quick-reference)

---

# Part 1: Creating Efficient Skills

## Core Principles

### Treat Context as a Precious Resource

From Anthropic's "Effective Context Engineering for AI Agents":

> **Context is expensive.** Every token loaded into the prompt costs money and latency. The goal is the **smallest possible set of high-signal tokens** needed to complete the task successfully.

### Quality Over Quantity

- **Concise > Verbose**: Use clear, direct language
- **Essential > Comprehensive**: Include only what's needed for the task
- **On-Demand > Upfront**: Load detailed content only when needed
- **Reuse > Duplicate**: Reference shared knowledge rather than repeating it

### Progressive Loading Philosophy

Load information in tiers:

1. **Tier 1 (Always)**: Core task description and essential instructions
2. **Tier 2 (On-Reference)**: Examples and patterns in separate files
3. **Tier 3 (On-Demand)**: Detailed implementation guides and edge cases

---

## Progressive Disclosure Pattern

### Three-Tier Architecture

**Tier 1: Frontmatter + Core Instructions (Always Loaded)**

```yaml
---
description: Brief 1-sentence description
argument-hint: [arg1] [arg2]
model: claude-haiku-4-5-20251001
category: ros|modbus|verification|workflow
complexity: low|medium|high
requires: ros2, python, cmake
---

You are the [Skill Name]. Your job is [core purpose].

## Task

Input: ${1:-<ask user>}

## Core Instructions

[Essential steps - 10-20 lines max]
```

**Tier 2: Reference Files (Loaded on Reference)**

```markdown
## Examples

**For complete examples**, see: `.claude/[domain]-examples.md`

Quick reference:
- Pattern A: Brief description
- Pattern B: Brief description
```

**Tier 3: Deep Documentation (User-Initiated)**

```markdown
**For comprehensive guides**, see:
- `.claude/[domain]-best-practices.md` - Best practices
- `.claude/error-patterns.md` - Error handling
```

### What to Extract to Reference Files

**Extract if:**
- More than 50 lines of examples
- Repeated across multiple skills
- Implementation details vs. task instructions
- Deep technical reference material

**Keep inline if:**
- Core workflow steps
- Essential validation criteria
- Critical error messages
- Task-specific logic

### Target Metrics

**Skill Size Targets:**
- Simple skills (templates, validation): < 150 lines
- Medium skills (analysis, processing): < 250 lines
- Complex skills (workflows, orchestration): < 400 lines

**Reference File Targets:**
- Example files: 300-700 lines
- Pattern files: 400-800 lines
- Comprehensive guides: 500-1000 lines

**Token Budget per Skill Invocation:**
- Tier 1 (core): 500-2,000 tokens
- Tier 2 (with examples): 2,000-5,000 tokens
- Tier 3 (full context): 5,000-15,000 tokens

---

## Model Selection Strategy

### Model Characteristics

**Haiku 4.5** (`claude-haiku-4-5-20251001`):
- **Speed**: 2-3x faster than Sonnet
- **Cost**: ~1/5 the cost of Sonnet
- **Best for**: Straightforward tasks with clear instructions
- **Token capacity**: 200K input, good for most tasks

**Sonnet 4.5** (`claude-sonnet-4-5-20250929`):
- **Reasoning**: Superior for complex planning and ambiguity
- **Quality**: Better at nuanced understanding
- **Best for**: Complex multi-step workflows, planning, code generation
- **Token capacity**: 200K input

### Selection Matrix

| Task Type | Model | Rationale |
|-----------|-------|-----------|
| Template generation | Haiku | Clear patterns, straightforward output |
| File validation | Haiku | Rule-based checking |
| Build/Test execution | Haiku | Command execution with clear outputs |
| Code analysis | Haiku | Pattern matching and linting |
| Implementation planning | **Sonnet** | Complex reasoning, ambiguity resolution |
| Workflow orchestration | **Sonnet** | Multi-step coordination |
| Context gathering | **Sonnet** | Deep codebase understanding |
| Creating new skills | **Sonnet** | High-quality code generation |

### Best Practice Distribution

In a well-designed system:
- **90-95%** of skills use Haiku - Fast execution tasks
- **5-10%** of skills use Sonnet - Complex reasoning tasks

**Example Sonnet tasks:**
1. Context gathering - Analyzes codebase deeply
2. Implementation planning - Creates detailed plans
3. Complete workflows - Orchestrates multiple steps
4. Skill/agent generation - Creates new tools

---

## Skill Structure Template

```markdown
---
description: [Clear, specific description of what this skill does]
argument-hint: [arg1] [arg2] [optional-arg]
model: claude-haiku-4-5-20251001  # or sonnet for complex reasoning
category: [verification|workflow|ros|modbus|git|analysis]
complexity: [low|medium|high]
requires: [comma-separated list of dependencies]
---

You are the [Skill Name] skill. Your job is to [clear, one-sentence purpose].

## Task

[What needs to be done]: ${1:-<ask user if not provided>}

## Purpose

[2-3 sentences explaining WHY this skill exists and WHEN to use it]

## Process

### 1. [First Step]
[Clear instructions for first action]

### 2. [Second Step]
[Clear instructions for second action]

### 3. [Validation]
[How to verify the action succeeded]

## Output Format

```
[Skill Name]: [target]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[SECTION HEADER]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Status: [✅ SUCCESS | ⚠️ WARNINGS | ❌ FAILED]

[Key metrics or information]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[RECOMMENDATIONS]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Actionable next steps based on results]
```

## Common Issues

### Issue: [Problem Description]

**Symptoms**: [How to recognize it]

**Cause**: [Why it happens]

**Solution**:
```
[Code or commands to fix]
```

## Exit Codes

- **0**: [Success condition]
- **1**: [Warning condition]
- **2**: [Failure condition]

Now [perform the skill's action]!
```

---

## Reference Documentation Strategy

### Shared Knowledge Base

Instead of duplicating content across skills, reference centralized docs:

**Domain-Specific References:**
- `.claude/py-node-examples.md` - Python ROS node examples
- `.claude/cpp-node-examples.md` - C++ ROS node examples
- `.claude/yaml-config-examples.md` - YAML configuration patterns
- `.claude/modbus-handler-examples.md` - Modbus protocol examples

**Cross-Cutting References:**
- `.claude/error-patterns.md` - Error handling across all domains
- `.claude/best-practices.md` - General software engineering practices
- `.claude/ros-patterns.md` - ROS2-specific patterns
- `.claude/modbus-patterns.md` - Modbus integration patterns
- `.claude/cpp-best-practices.md` - Modern C++ guidelines
- `.claude/python-best-practices.md` - Python coding standards
- `.claude/test-strategies.md` - Testing approaches
- `.claude/verification-checklist.md` - Quality verification

### Reference Pattern Template

```markdown
## [Section Name]

**For comprehensive [topic] patterns**, see: `.claude/[reference-file].md`

This includes:
- Pattern A
- Pattern B
- Pattern C

**Quick reference - most common patterns:**
- Brief inline example
- Another brief example
```

### Benefits

1. **DRY Principle**: Update once, applies everywhere
2. **Token Efficiency**: Reference loaded only when needed
3. **Maintainability**: Easier to keep documentation current
4. **Scalability**: Add new patterns without bloating skills

---

# Part 2: Using Skills Efficiently

## response_format Parameter

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

**Token Savings:** 80-95%

**Example:**
```python
# Check if there are issues before diving deep
result = detect_code_smells("large_file.py")
if result.data['total_smells'] > 10:
    # Now get details
    detailed = detect_code_smells("large_file.py", response_format="detailed")
```

#### Detailed Mode

**Use when:**
- Implementing fixes based on analysis
- Generating reports for users
- Need complete information for decision-making
- Working with specific items from summary

**Token Usage:** Full (baseline)

**Example:**
```python
# After summary shows high vulnerability count
result = check_vulnerabilities("project/", response_format="detailed")
for vuln in result.data['vulnerabilities']:
    if vuln['severity'] == 'critical':
        print(f"Fix: {vuln['fix']}")
```

---

## Progressive Disclosure in Practice

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

**Token Savings:** 90% if threshold not met

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
```

**Token Savings:** 95-99% (most filtering happens locally)

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

**Token Savings:** 80-90% (only detailed for subset)

---

## Skill-Specific Guidance

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
    results = analyze_codebase("src/", response_format="detailed")
```

**Token Impact:**
- Summary: ~500 tokens
- Detailed: ~50,000 tokens
- **Savings: 99%**

### skill_evaluator (90-97% savings)

**Best Practice:**
```python
# ❌ Inefficient - full report every time
report = generate_report("test_orchestrator")  # 30,000 tokens

# ✅ Efficient - summary first
summary = generate_report("test_orchestrator", response_format="summary")
# { "health_score": 92, "critical_issues": 0 }
# 1,000 tokens - 97% savings!

if summary.data['health_score'] < 85:
    full_report = generate_report("test_orchestrator", response_format="detailed")
```

**Token Impact:**
- Summary: ~1,000 tokens
- Detailed: ~30,000 tokens
- **Savings: 97%**

### refactor_assistant (85-90% savings)

**Best Practice:**
```python
# ❌ Inefficient - all smells with details
smells = detect_code_smells("legacy_code.py")  # 10,000 tokens

# ✅ Efficient - summary with counts
summary = detect_code_smells("legacy_code.py", response_format="summary")
# { "total_smells": 45, "by_severity": {"critical": 3, "high": 12} }
# 1,000 tokens - 90% savings!

# Only get details for critical/high severity
if summary.data['by_severity']['critical'] > 0:
    details = detect_code_smells("legacy_code.py", response_format="detailed")
```

**Token Impact:**
- Summary: ~1,000 tokens
- Detailed: ~10,000 tokens
- **Savings: 90%**

---

## Common Patterns

### Pattern: Threshold-Based Detail Retrieval

```python
def analyze_with_threshold(file_path, threshold=10):
    """Get details only if issues exceed threshold."""

    # Step 1: Summary
    summary = detect_code_smells(file_path, response_format="summary")

    # Step 2: Decision based on threshold
    if summary.data['total_smells'] > threshold:
        return detect_code_smells(file_path, response_format="detailed")

    return summary
```

**Token Savings:** 90% when threshold not exceeded

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

**Token Savings:** 80-90% depending on ratio

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

        return high_complexity
```

**Token Savings:** 95-99% (only analyze subset in detail)

---

## Token Budget Management

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

for file in large_file_list:
    if budget.can_afford(1000):  # Estimate for summary
        result = budget.execute(analyze_file, file)
    else:
        print(f"Budget exhausted.")
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
    sorted_files = sorted(
        summaries,
        key=lambda x: x[1].data.get('complexity', 0),
        reverse=True
    )

    for file, summary in sorted_files:
        estimated_tokens = 10000

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

# Part 3: Optimization Techniques

## Removing Redundancy

### Extract Common Patterns

**Bad (repeated in every skill):**
```markdown
## Best Practices

1. Use clear variable names
2. Add comments to explain complex logic
3. Follow PEP 8 style guide
[...20 more lines...]
```

**Good (reference shared doc):**
```markdown
## Best Practices

**See**: `.claude/python-best-practices.md` for comprehensive guidelines
```

**Savings:** ~200 tokens per skill × 30 Python skills = ~6,000 tokens

---

## Compact Output Templates

**Bad (verbose template):**
```markdown
## Output

When you complete this task, you should output the following information:

```
Generated File: [filename]

The file contains the following:
- Feature 1: Description of feature 1
[...many more lines...]
```
```

**Good (concise template):**
```markdown
## Output

```
Generated: [filename]
Features: [list]
Next steps: [actions]
```
```

**Savings:** ~150 tokens per skill

---

## Example Extraction

**Achieved reductions:**
- `py-node-template.md`: 427 → 149 lines (-65%)
- `cpp-node-template.md`: 352 → 135 lines (-62%)
- `yaml-config.md`: 436 → 236 lines (-46%)
- `modbus-handler.md`: 261 → 132 lines (-49%)

**Average savings:** ~56% reduction per skill

**Technique:**
1. Identify examples longer than 50 lines
2. Extract to separate reference file
3. Replace with brief inline example + reference
4. Link to full examples file

---

## Measurement & Metrics

### Token Estimation

Rough estimates (varies by content):
- 1 token ≈ 0.75 words
- 1 token ≈ 4 characters
- 100 lines of code ≈ 400-600 tokens
- 100 lines of prose ≈ 600-800 tokens

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

### Measuring Impact

```bash
# Count lines before optimization
wc -l original-skill.md

# Count lines after optimization
wc -l optimized-skill.md

# Calculate reduction percentage
echo "scale=2; (1 - (after/before)) * 100" | bc
```

**Expected Improvements:**
- Skills with examples: 40-60% reduction
- Skills with redundant content: 20-30% reduction
- Already lean skills: 10-15% reduction

**Project-Wide Goal:** 20-30% average reduction

---

# Part 4: Best Practices

## Implementation Checklist

### For New Skills

- [ ] Use appropriate model (Haiku for most, Sonnet for complex)
- [ ] Write concise description (1 sentence in frontmatter)
- [ ] Include only essential instructions
- [ ] Reference existing docs instead of duplicating
- [ ] Extract examples if > 50 lines
- [ ] Use structured formats (lists, tables)
- [ ] Add clear exit codes
- [ ] Test with minimal prompt

### For Existing Skills

- [ ] Identify redundant content
- [ ] Check if examples can be extracted
- [ ] Verify model selection is appropriate
- [ ] Replace duplicated patterns with references
- [ ] Simplify output templates
- [ ] Remove verbose explanations
- [ ] Consolidate similar instructions
- [ ] Measure before/after line count

### For Reference Files

- [ ] Group related content logically
- [ ] Use clear section headers
- [ ] Include table of contents for long files
- [ ] Provide quick reference summaries
- [ ] Keep examples focused and practical
- [ ] Cross-reference related docs

---

## Best Practices Summary

### DO ✅

**For Creating Skills:**
1. ✅ Use Haiku by default - Only use Sonnet for complex reasoning
2. ✅ Extract examples - Move code examples to reference files
3. ✅ Reference shared docs - Link to centralized patterns
4. ✅ Be concise - Every word should add value
5. ✅ Structure information - Use lists, tables, headers
6. ✅ Progressive disclosure - Load details only when needed

**For Using Skills:**
1. ✅ Default to summary mode - Start with `response_format="summary"`
2. ✅ Use progressive disclosure - Summary → Filter → Detailed
3. ✅ Filter locally - Use ResultFilter to reduce token usage
4. ✅ Set thresholds - Only get details when metrics exceed thresholds
5. ✅ Batch operations - Process multiple items with summaries first
6. ✅ Track usage - Monitor token consumption
7. ✅ Cache summaries - Store summary results to avoid re-fetching

### DON'T ❌

**For Creating Skills:**
1. ❌ Don't duplicate - Avoid repeating content across skills
2. ❌ Don't be verbose - Cut unnecessary explanations
3. ❌ Don't inline everything - Extract large examples
4. ❌ Don't use Sonnet unnecessarily - Haiku is faster and cheaper
5. ❌ Don't skip frontmatter - Metadata enables optimization
6. ❌ Don't write prose - Use structured formats

**For Using Skills:**
1. ❌ Don't always use detailed - Only use when absolutely necessary
2. ❌ Don't skip summaries - Always check summary first
3. ❌ Don't ignore efficiency tips - They're in operation docstrings
4. ❌ Don't load everything - Use filtering and thresholds
5. ❌ Don't repeat operations - Cache results when possible
6. ❌ Don't forget local filtering - ResultFilter is free (0 tokens)

---

## Quick Reference

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

### Model Selection Flowchart

```
Does task require complex reasoning?
├─ Yes → Use Sonnet
│   Examples: Planning, context gathering, code generation
└─ No → Does it involve template/pattern application?
    ├─ Yes → Use Haiku
    │   Examples: File generation, validation, testing
    └─ No → Use Haiku (default)
```

### Optimization Decision Tree

```
Is content > 50 lines?
├─ Yes → Can it be extracted?
│   ├─ Yes → Extract to reference file
│   └─ No → Can it be compressed?
│       ├─ Yes → Use tables/lists
│       └─ No → Keep as is
└─ No → Is it duplicated elsewhere?
    ├─ Yes → Move to shared reference
    └─ No → Keep as is
```

### Token Savings Summary

**Overall Average:** 85-95% token savings with progressive disclosure

**By Category:**
- Code analysis: 95-99% savings
- Report generation: 90-97% savings
- Documentation: 90-96% savings
- Test generation: 90% savings
- Refactoring: 85-90% savings
- PR review: 85-90% savings
- Security scanning: 83-86% savings
- Search operations: 85% savings

---

## Related Documentation

**Creating Skills:**
- `docs/TOOL_DESIGN_EXCELLENCE_COMPLETE.md` - Skill design patterns
- `templates/skill-template/` - Skill scaffolding template
- `.claude/CLAUDE.md` - Project overview and skill index

**Using Skills:**
- `docs/OPTIMIZATION_GUIDE.md` - Overall optimization strategies
- `skills/CLAUDE.md` - Skills usage guide
- Individual skill SKILL.md files - Operation-specific guidance

**Best Practices:**
- `.claude/cpp-best-practices.md` - C++ coding guidelines
- `.claude/python-best-practices.md` - Python coding standards
- `.claude/ros-patterns.md` - ROS2-specific patterns
- `.claude/test-strategies.md` - Testing approaches

---

## Maintenance

This guide should be updated when:
- New optimization patterns are discovered
- Token costs or model capabilities change
- New reference files are created
- Project structure evolves
- New skills with novel patterns are added

**Last updated:** 2025-11-10
**Next review:** When adding 10+ new skills or when model capabilities change

---

**Status:** Complete unified guide covering both skill creation and usage
**Average Token Savings:** 85-95% with progressive disclosure
**Skill Reduction:** 40-60% line count reduction with example extraction

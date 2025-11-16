# Token Optimization Guide

Best practices for minimizing token usage while maintaining clarity and functionality in Claude Code skills and agents.

**Created**: 2025-11-10
**Status**: Active
**Applies to**: All 59 skills and agents in this project

---

## Table of Contents

1. [Core Principles](#core-principles)
2. [Progressive Disclosure Pattern](#progressive-disclosure-pattern)
3. [Model Selection Strategy](#model-selection-strategy)
4. [Reference Documentation](#reference-documentation)
5. [Optimization Techniques](#optimization-techniques)
6. [Measurement & Metrics](#measurement--metrics)
7. [Implementation Checklist](#implementation-checklist)

---

## Core Principles

### Treat Context as a Precious Resource

From Anthropic's "Effective Context Engineering for AI Agents":

> **Context is expensive.** Every token loaded into the prompt costs money and latency. The goal is the **smallest possible set of high-signal tokens** needed to complete the task successfully.

### Quality Over Quantity

- **Concise > Verbose**: Use clear, direct language
- **Essential > Comprehensive**: Include only what's needed for the task
- **On-Demand > Upfront**: Load detailed content only when needed
- **Reuse > Duplicate**: Reference shared knowledge rather than repeating it

### Progressive Loading

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

[Essential steps - 10-20 lines]
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

**Extract if**:
- More than 50 lines of examples
- Repeated across multiple skills
- Implementation details vs. task instructions
- Deep technical reference material

**Keep inline if**:
- Core workflow steps
- Essential validation criteria
- Critical error messages
- Task-specific logic

---

## Model Selection Strategy

### Model Characteristics

**Haiku 4.5** (claude-haiku-4-5-20251001):
- **Speed**: 2-3x faster than Sonnet
- **Cost**: ~1/5 the cost of Sonnet
- **Best for**: Straightforward tasks with clear instructions
- **Token capacity**: 200K input, good for most tasks

**Sonnet 4.5** (claude-sonnet-4-5-20250929):
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

### Current Distribution

In this project:
- **55 skills** use Haiku (93%) - Fast execution tasks
- **6 skills** use Sonnet (7%) - Complex reasoning tasks

**Sonnet tasks**:
1. `/gather-context` - Analyzes codebase deeply
2. `/plan` - Creates implementation plans
3. `/dev` - Complete development workflow
4. `/execute` - Workflow execution with verification
5. `/create-skill` - Generates new skills
6. `/create-agent` - Generates new agents

---

## Reference Documentation

### Shared Knowledge Base

Instead of duplicating content across skills, reference centralized docs:

**Domain-Specific References**:
- `.claude/py-node-examples.md` - Python ROS node examples
- `.claude/cpp-node-examples.md` - C++ ROS node examples
- `.claude/yaml-config-examples.md` - YAML configuration patterns
- `.claude/modbus-handler-examples.md` - Modbus protocol examples

**Cross-Cutting References**:
- `.claude/error-patterns.md` - Error handling across all domains
- `.claude/best-practices.md` - General software engineering practices
- `.claude/ros-patterns.md` - ROS2-specific patterns
- `.claude/modbus-patterns.md` - Modbus integration patterns
- `.claude/cpp-best-practices.md` - Modern C++ guidelines
- `.claude/python-best-practices.md` - Python coding standards
- `.claude/test-strategies.md` - Testing approaches
- `.claude/verification-checklist.md` - Quality verification

### Reference Pattern

```markdown
## [Section Name]

**For comprehensive [topic] patterns**, see: `.claude/[reference-file].md`

This includes:
- Pattern A
- Pattern B
- Pattern C

**Quick reference - most common patterns**:
- Brief inline example
- Another brief example
```

### Benefits

1. **DRY Principle**: Update once, applies everywhere
2. **Token Efficiency**: Reference loaded only when needed
3. **Maintainability**: Easier to keep documentation current
4. **Scalability**: Add new patterns without bloating skills

---

## Optimization Techniques

### 1. Remove Redundant Instructions

**Bad** (repeated in every skill):
```markdown
## Best Practices

1. Use clear variable names
2. Add comments to explain complex logic
3. Follow PEP 8 style guide
4. Write unit tests
5. Handle errors gracefully
[...20 more lines...]
```

**Good** (reference shared doc):
```markdown
## Best Practices

**See**: `.claude/python-best-practices.md` for comprehensive guidelines
```

**Savings**: ~200 tokens per skill × 30 Python skills = ~6,000 tokens

### 2. Compact Output Templates

**Bad** (verbose template):
```markdown
## Output

When you complete this task, you should output the following information in the following format:

```
Generated File: [filename]

The file contains the following:
- Feature 1: Description of feature 1
- Feature 2: Description of feature 2
[...many more lines...]
```
```

**Good** (concise template):
```markdown
## Output

```
Generated: [filename]
Features: [list]
Next steps: [actions]
```
```

**Savings**: ~150 tokens per skill

### 3. Example Extraction

See [Progressive Disclosure Pattern](#progressive-disclosure-pattern) above.

**Achieved reductions**:
- `py-node-template.md`: 427 → 149 lines (-65%)
- `cpp-node-template.md`: 352 → 135 lines (-62%)
- `yaml-config.md`: 436 → 236 lines (-46%)
- `modbus-handler.md`: 261 → 132 lines (-49%)

**Average savings**: ~56% reduction per skill

### 4. Eliminate Boilerplate

**Bad**:
```markdown
This skill helps you [do thing]. It is useful when you need to [do thing].
You should use this skill whenever you want to [do thing].

Before using this skill, make sure you understand [thing]. This skill requires
knowledge of [thing] and [thing]. If you don't have [thing], you should first [thing].
```

**Good**:
```markdown
You are the [Name] Skill. You [core purpose].

Requirements: [list]
```

### 5. Structured Brevity

Use tables and lists instead of prose:

**Bad** (prose):
```markdown
The first step is to validate the input. You should check that the input
is not null, that it is the correct type, and that it falls within the
acceptable range of values. The minimum acceptable value is 0 and the
maximum is 100.
```

**Good** (structured):
```markdown
1. Validate input:
   - Not null
   - Correct type
   - Range: 0-100
```

### 6. Eliminate Redundant Examples

**Bad** (showing every variation):
```python
# Example 1: Simple case
def process(x):
    return x * 2

# Example 2: With validation
def process(x):
    if x < 0:
        raise ValueError
    return x * 2

# Example 3: With logging
def process(x):
    logger.info(f"Processing {x}")
    return x * 2

# Example 4: With type hints
def process(x: float) -> float:
    return x * 2
```

**Good** (one comprehensive example):
```python
# Complete example with all features
def process(x: float) -> float:
    """Process input value."""
    if x < 0:
        raise ValueError("x must be non-negative")
    logger.info(f"Processing {x}")
    return x * 2
```

---

## Measurement & Metrics

### Token Estimation

Rough estimates (varies by content):
- 1 token ≈ 0.75 words
- 1 token ≈ 4 characters
- 100 lines of code ≈ 400-600 tokens
- 100 lines of prose ≈ 600-800 tokens

### Target Metrics

**Skill Size Targets**:
- Simple skills (templates, validation): < 150 lines
- Medium skills (analysis, processing): < 250 lines
- Complex skills (workflows, orchestration): < 400 lines

**Reference File Targets**:
- Example files: 300-700 lines
- Pattern files: 400-800 lines
- Comprehensive guides: 500-1000 lines

**Token Budget per Skill Invocation**:
- Tier 1 (core): 500-2,000 tokens
- Tier 2 (with examples): 2,000-5,000 tokens
- Tier 3 (full context): 5,000-15,000 tokens

### Measuring Impact

**Before/After Comparison**:
```bash
# Count lines before optimization
wc -l original-skill.md

# Count lines after optimization
wc -l optimized-skill.md

# Calculate reduction
echo "scale=2; (1 - (after/before)) * 100" | bc
```

**Expected Improvements**:
- Skills with examples: 40-60% reduction
- Skills with redundant content: 20-30% reduction
- Already lean skills: 10-15% reduction

**Project-Wide Goal**: 20-30% average reduction

---

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
- [ ] Update index in CLAUDE.md

---

## Optimization Results

### Phase 1: Progressive Disclosure

**Files optimized**: 4 major skills
**Lines reduced**: 1,476 → 652 (-56% average)
**Reference files created**: 4 (2,352 total lines)

**Details**:
| Skill | Before | After | Reduction | Reference File |
|-------|--------|-------|-----------|----------------|
| py-node-template | 427 | 149 | 65% | py-node-examples.md (392 lines) |
| cpp-node-template | 352 | 135 | 62% | cpp-node-examples.md (573 lines) |
| yaml-config | 436 | 236 | 46% | yaml-config-examples.md (674 lines) |
| modbus-handler | 261 | 132 | 49% | modbus-handler-examples.md (713 lines) |

**Additional documentation**:
- `error-patterns.md` (465 lines)
- `best-practices.md` (556 lines)

### Projected Impact

**Token savings per invocation**:
- Simple skill without examples: 0 tokens (already lean)
- Skill with extracted examples: ~1,500 tokens saved
- Skill referencing shared patterns: ~300 tokens saved

**Estimated project-wide savings**: 20-30% reduction in average token usage

---

## Best Practices Summary

### Do's

✅ **Use Haiku by default** - Only use Sonnet for complex reasoning
✅ **Extract examples** - Move code examples to reference files
✅ **Reference shared docs** - Link to centralized patterns
✅ **Be concise** - Every word should add value
✅ **Structure information** - Use lists, tables, headers
✅ **Measure impact** - Track before/after metrics
✅ **Progressive disclosure** - Load details only when needed

### Don'ts

❌ **Don't duplicate** - Avoid repeating content across skills
❌ **Don't be verbose** - Cut unnecessary explanations
❌ **Don't inline everything** - Extract large examples
❌ **Don't use Sonnet unnecessarily** - Haiku is faster and cheaper
❌ **Don't skip frontmatter** - Metadata enables optimization
❌ **Don't write prose** - Use structured formats
❌ **Don't forget to reference** - Link related documentation

---

## Quick Reference

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

---

## Maintenance

This guide should be updated when:
- New optimization patterns are discovered
- Token costs or model capabilities change
- New reference files are created
- Project structure evolves

**Last updated**: 2025-11-10
**Next review**: When adding 10+ new skills

---

**See also**:
- `.claude/CLAUDE.md` - Project overview
- `docs/IMPLEMENTATION_PLAN.md` - Optimization roadmap
- `docs/PROGRESS_SUMMARY.md` - Completed work

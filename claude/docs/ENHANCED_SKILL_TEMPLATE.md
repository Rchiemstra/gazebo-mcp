# Enhanced SKILL.md Template
**Phase 4 Task 2: Tool Description Refinement**

This template provides the enhanced structure for all SKILL.md files, incorporating Phase 4 improvements for better discoverability, token efficiency documentation, and pitfall prevention.

---

## Template Structure

```markdown
---
name: skill-name
description: One-line description (50 words max)
version: 1.0.0
category: category-name
tags:
  - relevant
  - tags
activation: manual  # or auto
tools:
  - Read
  - Write
dependencies: []
---

# Skill Name

## When to Use This Skill

Use [skill-name] when you need to:
- ✅ **Use case 1** - Brief description
- ✅ **Use case 2** - Brief description
- ✅ **Use case 3** - Brief description

**Not for:** What this skill should NOT be used for

## Quick Start

\```python
from skills.skill_name.operations import main_operation

# Simplest possible usage
result = main_operation(params)
print(result.data)
\```

For detailed documentation, see **reference.md**.
For usage examples, see **examples.md**.

## Operations

### operation_name(params, response_format="summary")
Brief description of what the operation does.

**Parameters:**
- `param1` (type): Description
- `response_format` (str): "summary" | "detailed" | "filtered"

**Returns:** Brief description of return value

See **reference.md** for complete specifications.

## Token Efficiency

This skill provides **[X]% token savings** for [scenario]:

| Operation | Format | Token Usage | Use When |
|-----------|--------|-------------|----------|
| operation | summary | 500-1K | Quick overview |
| operation | filtered | 2-10K | With local filtering |
| operation | detailed | 50K+ | Small datasets only |

**Critical:** For [large scenarios], ALWAYS use summary or filtered format!

## Usage Patterns

### Pattern 1: Basic Usage
**Scenario:** [When to use this pattern]

\```python
from skills.skill_name import operation

# Basic example
result = operation("input")
print(result.data)
\```

**Token Impact:** ~500 tokens

---

### Pattern 2: Intermediate Usage
**Scenario:** [More complex scenario]

\```python
from skills.skill_name import operation
from skills.common.filters import ResultFilter

# Get filtered data
result = operation("input", response_format="filtered")

# Filter locally (95%+ token savings!)
filtered = ResultFilter.search(result.data, "query", ["field1", "field2"])
top_5 = ResultFilter.top_n_by_field(filtered, "score", 5)
\```

**Token Impact:** ~2K tokens (vs 50K without filtering = 96% savings)

---

### Pattern 3: Advanced Usage with Integration
**Scenario:** [Complex integration scenario]

\```python
from skills.skill_name import operation1, operation2
from skills.other_skill import other_operation

# Multi-step workflow
data = operation1("input")
processed = operation2(data.result)
final = other_operation(processed)
\```

**Token Impact:** ~5K tokens
**Integration:** Works with [other-skill], [another-skill]

## Common Pitfalls

### ❌ Pitfall 1: [Description of common mistake]

**Problem:**
\```python
# Bad example
result = operation("large_dataset", response_format="detailed")
# Returns 50,000 tokens!
\```

**Why it's bad:** [Explanation of the issue]

**✅ Solution:**
\```python
# Good example
result = operation("large_dataset", response_format="filtered")
filtered = ResultFilter.limit(result.data, 10)
# Returns only 500 tokens (99% savings)
\```

**Impact:** Saves [X] tokens, [Y]% faster

---

### ❌ Pitfall 2: [Another common mistake]

**Problem:** [Description]

**✅ Solution:** [How to fix]

**Impact:** [Quantified benefit]

---

### ❌ Pitfall 3: [Third common mistake]

**Problem:** [Description]

**✅ Solution:** [How to fix]

**Impact:** [Quantified benefit]

## Progressive Disclosure

This skill follows the progressive disclosure pattern:

1. **Start here: SKILL.md** (this file)
   - Quick overview and common patterns
   - ~200-500 tokens to load
   - Sufficient for 80% of use cases

2. **Need more details: reference.md**
   - Complete API documentation
   - All parameters and return values
   - ~1000-2000 tokens
   - Use when you need exact specifications

3. **Need examples: examples.md**
   - Real-world usage examples
   - Integration patterns
   - ~2000-5000 tokens
   - Use when learning the skill

**Best Practice:** Only load reference.md or examples.md when you actually need them!

## Integration with Other Skills

This skill works well with:
- **[other-skill]** - [How they integrate]
- **[another-skill]** - [How they integrate]

Example integration:
\```python
from skills.skill_name import operation1
from skills.other_skill import operation2

# Combined workflow
data = operation1("input")
result = operation2(data.result)
\```

## Performance Characteristics

- **Speed:** [Fast/Medium/Slow] - [Why]
- **Memory:** [Low/Medium/High] - [Typical usage]
- **Token Efficiency:** [Excellent/Good/Fair] - [Range]
- **Scalability:** Works with [size] datasets

## See Also

- Related skills: [skill1], [skill2]
- Documentation: `docs/GUIDE_NAME.md`
- Examples: `skills/skill_name/examples.md`
```

---

## Enhancement Checklist

When enhancing a SKILL.md file, ensure:

### Required Sections
- [ ] YAML frontmatter with all metadata
- [ ] "When to Use" section with ✅/❌ indicators
- [ ] Quick Start with minimal example
- [ ] Operations listing
- [ ] Token Efficiency table
- [ ] At least 3 usage patterns (basic, intermediate, advanced)
- [ ] At least 3 common pitfalls with solutions
- [ ] Progressive Disclosure section
- [ ] Integration examples
- [ ] See Also links

### Content Quality
- [ ] All code examples are tested and working
- [ ] Token savings are quantified (e.g., "99% savings")
- [ ] Pitfalls include real examples from usage
- [ ] Each pattern shows token impact
- [ ] Progressive disclosure explains when to load each doc

### Formatting
- [ ] Code blocks use proper syntax highlighting
- [ ] Tables are formatted correctly
- [ ] Headers use proper hierarchy
- [ ] Examples show before/after comparisons
- [ ] Emoji indicators (✅/❌) used consistently

---

## Priority Skills for Enhancement

Based on usage frequency and Phase 4 evaluation results:

### High Priority (Enhance First)
1. **code_analysis** - Most used skill, complex API
2. **test_orchestrator** - Critical for testing workflows
3. **code_search** - High usage, simple improvements
4. **pr_review_assistant** - Quality improvements needed (from eval)
5. **git_workflow_assistant** - Common workflows

### Medium Priority
6. **learning_plan_manager** - For student interactions
7. **doc_generator** - Documentation workflows
8. **refactor_assistant** - Code improvement workflows
9. **dependency_guardian** - Security scanning
10. **context_manager** - Context handling

### Lower Priority
11. **llm_judge** - Specialized use
12. **skill_evaluator** - Meta-skill
13. **spec_to_implementation** - Less frequent
14. **verification** - Testing support

---

## Token Savings Examples by Skill

### code_analysis
- **Before:** 50,000 tokens (detailed format)
- **After:** 150 tokens (filtered + local filtering)
- **Savings:** 99.7%

### test_orchestrator
- **Before:** 10,000 tokens (all test results)
- **After:** 500 tokens (summary format)
- **Savings:** 95%

### code_search
- **Before:** 5,000 tokens (all matches)
- **After:** 200 tokens (top 10 results)
- **Savings:** 96%

---

## Implementation Notes

**Estimated Time per Skill:** 30-45 minutes
**Total for 14 Skills:** 7-10 hours

**Approach:**
1. Start with high-priority skills
2. Use this template as baseline
3. Customize patterns to skill specifics
4. Test all code examples
5. Quantify token savings with real data

**Quality Standards:**
- All examples must be copy-pasteable and working
- Token savings must be measured, not estimated
- Pitfalls must be based on real usage issues
- Progressive disclosure must be explained clearly

---

## Next Steps

1. **Immediate:** Enhance 1-2 high-priority skills using this template
2. **Short-term:** Document enhancement process and findings
3. **Long-term:** Systematically enhance remaining skills based on usage data

**Phase 4 Task 2 Status:** Template created ✅
**Next:** Enhance high-priority skills, then move to Task 3 (Orchestrators)

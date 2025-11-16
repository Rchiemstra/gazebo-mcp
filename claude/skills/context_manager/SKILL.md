---
name: context-manager
description: Manages context usage and optimization for long-horizon tasks. Provides context analysis, persistent note-taking, and conversation compaction.
version: 0.1.0
category: infrastructure
tags:
  - context
  - optimization
  - tokens
  - efficiency
  - memory
activation: manual
tools:
  - Read
  - Write
dependencies: []
---

# Context Manager Skill

## When to Use This Skill

Use context-manager when you need to:
- **Monitor context usage** - Track token usage and get optimization recommendations
- **Create persistent notes** - Save important information to disk instead of context
- **Compact conversations** - Summarize completed work to reduce context
- **Optimize long tasks** - Manage context for multi-hour or multi-day projects
- **Prevent context overflow** - Proactively manage approaching token limits

## Quick Start

```python
from skills.context_manager.operations import (
    analyze_context_usage,
    create_notes,
    compact_conversation
)

# 1. Check context usage
analysis = analyze_context_usage(estimated_tokens=50000)
print(f"Usage: {analysis.data['usage_percent']}%")
print(f"Status: {analysis.data['status']}")

# 2. Create persistent notes for important info
notes = create_notes("""
Architectural Decision:
- Using PostgreSQL for primary database
- Redis for caching
- RabbitMQ for async tasks
""")
print(f"Notes saved to: {notes.data['notes_file']}")

# 3. Compact conversation when context gets large
summary = compact_conversation(
    work_completed=["Implemented auth", "Added tests", "Deployed to staging"],
    decisions_made=["Use JWT tokens", "60min session timeout"],
    unresolved_issues=["Performance optimization needed"]
)
print(summary.data['compact_summary'])
```

For detailed documentation, see **reference.md**.
For usage examples, see **examples.md**.

## Operations

### analyze_context_usage(estimated_tokens, max_tokens=200000)
Analyze current context usage and provide optimization recommendations.

**Returns:** Usage metrics, status, and recommendations

### create_notes(notes_content, notes_file=".claude/notes/NOTES.md")
Create or append to persistent notes file.

**Returns:** Notes file path and estimated tokens saved

### compact_conversation(work_completed, decisions_made, unresolved_issues)
Create compact summary of conversation/work for context reduction.

**Returns:** Compact summary preserving critical information

See **reference.md** for complete parameter specifications.

## Token Efficiency

This skill is designed to SAVE tokens on long-horizon tasks:

| Operation | Usage | Savings |
|-----------|-------|---------|
| analyze_context_usage | < 200 tokens | Identifies 80-95% savings opportunities |
| create_notes | < 100 tokens | Saves 1000-5000 tokens per session |
| compact_conversation | 200-500 tokens | Saves 50-80% of conversation history |

**Best Practice:** Use proactively when context usage > 50%

## Context Optimization Strategies

### 1. Progressive Disclosure
Load summary first, details on demand:
```python
# Instead of loading everything
result = analyze_codebase("src/", response_format="detailed")  # 50,000 tokens

# Load progressively
summary = analyze_codebase("src/")  # 500 tokens
# Then get details only for what you need
```

### 2. Local Filtering
Filter data in code, not in agent context:
```python
from skills.common.filters import ResultFilter

# Get all data once
result = analyze_codebase("src/", response_format="filtered")

# Filter locally (0 additional tokens!)
auth_files = ResultFilter.search(result.data["files"], "auth")
# Agent sees only filtered results (99% savings!)
```

### 3. Persistent Notes
Save important info to disk:
```python
# Instead of keeping in context
create_notes("""
Key Decisions:
- Database schema finalized
- API v2 endpoints defined
- Migration plan approved
""")
# Frees up 500-1000 tokens
```

### 4. Conversation Compaction
Summarize completed work:
```python
# Compact verbose history
summary = compact_conversation(
    work_completed=["Task 1", "Task 2", "Task 3"],
    decisions_made=["Decision A", "Decision B"],
    unresolved_issues=["Issue X"]
)
# Reduces 10,000 token conversation to 500 tokens
```

## Example Workflow

```python
# Monitor context throughout long task
analysis = analyze_context_usage(estimated_tokens=80000)

if analysis.data['usage_percent'] > 50:
    print("⚠ Context usage high!")

    # Get optimization recommendations
    detailed = analyze_context_usage(
        estimated_tokens=80000,
        response_format="detailed"
    )

    for rec in detailed.data['recommendations']:
        print(f"  • {rec['description']} (save {rec['potential_savings']})")

    # Save important info to notes
    create_notes("Important architectural decisions made today...")

    # Compact conversation
    summary = compact_conversation(
        work_completed=["Phase 1", "Phase 2"],
        decisions_made=["Use microservices"],
        unresolved_issues=["Performance testing"]
    )

    # Continue with fresh context using summary
```

## Error Handling

All operations return `OperationResult`:

```python
result = create_notes("Important info")

if not result.success:
    print(result.error)       # Clear error message
    print(result.error_code)  # Machine-readable code

    for suggestion in result.suggestions:
        print(f"  - {suggestion}")
```

## Integration

**With Long Tasks:**
```python
# At start of multi-hour task
create_notes("Starting implementation of feature X...")

# Periodically
analysis = analyze_context_usage(estimated_tokens=current_usage)
if analysis.data['priority'] == 'high':
    # Take optimization action
    pass

# At end
compact_conversation(
    work_completed=completed_tasks,
    decisions_made=key_decisions,
    unresolved_issues=remaining_items
)
```

**With Learning Plans:**
```python
# Save learning progress
create_notes(f"""
Learning Session: {date}
- Completed Phase 2
- Key insights: ...
- Next: Phase 3
""")
```

**With Development Workflows:**
```python
# Save architectural decisions
create_notes("""
Architecture Review:
- Microservices: Yes
- Database: PostgreSQL
- Cache: Redis
- Message Queue: RabbitMQ
""")
```

## Notes File Structure

Notes are saved to `.claude/notes/NOTES.md`:

```markdown
# Notes

Persistent notes for context management.

---
**2025-01-15 14:30:00**

Architectural Decision:
- Using PostgreSQL for primary database
- Redis for caching

---
**2025-01-15 16:45:00**

Implementation Progress:
- Auth module complete
- Tests passing
- Ready for review
```

## Next Steps

- **Read reference.md** for complete API documentation
- **Read examples.md** for real-world usage patterns
- **Use proactively** when context > 50%
- **Combine with other skills** using response_format and ResultFilter

---

*Last Updated: 2025-11-08*

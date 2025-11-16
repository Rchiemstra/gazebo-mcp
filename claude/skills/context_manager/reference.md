# Context Manager - API Reference

Complete documentation for all context_manager operations.

---

## Overview

Context Manager provides operations for monitoring and optimizing context usage in long-horizon tasks. It helps prevent context overflow and provides strategies for token efficiency.

---

## Operations

### analyze_context_usage

Analyze current context usage and provide optimization recommendations.

#### Signature

```python
def analyze_context_usage(
    estimated_tokens: int = 0,
    max_tokens: int = 200000,
    response_format: str = "summary",
    **kwargs
) -> OperationResult
```

#### Parameters

**estimated_tokens** (int, optional, default=0)
- Current estimated token count
- Use to check context usage
- Can be approximate

**max_tokens** (int, optional, default=200000)
- Maximum context window size
- Default is Claude's typical context window
- Adjust based on model

**response_format** (str, optional, default="summary")
- `"summary"` - Key metrics and top recommendations (< 200 tokens)
- `"detailed"` - Full analysis with all strategies (< 500 tokens)

#### Returns

**Summary format:**
```python
{
    "success": True,
    "data": {
        "tokens_used": 80000,
        "tokens_max": 200000,
        "tokens_remaining": 120000,
        "usage_percent": 40.0,
        "status": "moderate",  # low | moderate | high | critical
        "priority": "low",  # none | low | medium | high | critical
        "recommendations_count": 2,
        "top_recommendations": [
            "use_summary_format: Use response_format='summary' (save 80-95%)",
            "local_filtering: Use ResultFilter (save 95-99%)"
        ]
    }
}
```

**Detailed format:**
```python
{
    "success": True,
    "data": {
        "tokens_used": 80000,
        "tokens_max": 200000,
        "tokens_remaining": 120000,
        "usage_percent": 40.0,
        "status": "moderate",
        "priority": "low",
        "recommendations_count": 2,
        "recommendations": [
            {
                "type": "use_summary_format",
                "description": "Use response_format='summary' instead of 'detailed'",
                "potential_savings": "80-95%",
                "priority": "high"
            },
            {
                "type": "local_filtering",
                "description": "Use ResultFilter for local data filtering",
                "potential_savings": "95-99%",
                "priority": "high"
            }
        ],
        "optimization_strategies": {
            "progressive_disclosure": "Load summary first, details on demand",
            "local_filtering": "Filter data in code, not in agent context",
            "response_formats": "Use 'summary' or 'concise' formats",
            "result_filter": "Use ResultFilter for 95-99% savings",
            "notes": "Persist important info to disk",
            "compaction": "Summarize completed work"
        },
        "efficiency_metrics": {
            "typical_summary": "200-1000 tokens",
            "typical_detailed": "2000-10000 tokens",
            "typical_savings": "80-95%"
        }
    }
}
```

#### Usage Thresholds

| Usage % | Status | Priority | Action |
|---------|--------|----------|--------|
| 0-25% | low | none | No action needed |
| 25-50% | moderate | low | Start using summary formats |
| 50-75% | high | medium | Use local filtering, create notes |
| 75-100% | critical | high/critical | Compact conversation, clear history |

---

### create_notes

Create or append to persistent notes file for important information.

#### Signature

```python
def create_notes(
    notes_content: str,
    notes_file: str = ".claude/notes/NOTES.md",
    append: bool = True,
    **kwargs
) -> OperationResult
```

#### Parameters

**notes_content** (str, required)
- Content to save to notes
- Markdown formatted
- Can include any important information

**notes_file** (str, optional, default=".claude/notes/NOTES.md")
- Path to notes file
- Created if doesn't exist
- Directory created automatically

**append** (bool, optional, default=True)
- If True, append to existing notes
- If False, overwrite file
- Timestamp added automatically

#### Returns

```python
{
    "success": True,
    "data": {
        "notes_file": ".claude/notes/NOTES.md",
        "action": "appended",  # or "created"
        "content_length": 234,
        "estimated_tokens_saved": 305,
        "message": "Notes appended successfully at .claude/notes/NOTES.md"
    }
}
```

#### Error Handling

**NOTES_ERROR:**
```python
{
    "success": False,
    "error": "Failed to create notes: Permission denied",
    "error_code": "NOTES_ERROR",
    "suggestions": [
        "Check that the notes directory is writable",
        "Verify the file path is valid",
        "Ensure parent directory exists"
    ],
    "example_fix": "create_notes('Important info', notes_file='.claude/notes/NOTES.md')"
}
```

#### Notes File Format

```markdown
# Notes

Persistent notes for context management.

---
**2025-01-15 14:30:00**

First note content here...

---
**2025-01-15 16:45:00**

Second note content here...
```

---

### compact_conversation

Create compact summary of conversation/work for context reduction.

#### Signature

```python
def compact_conversation(
    work_completed: List[str],
    decisions_made: List[str],
    unresolved_issues: List[str],
    response_format: str = "summary",
    **kwargs
) -> OperationResult
```

#### Parameters

**work_completed** (List[str], required)
- List of completed tasks/items
- Be concise but specific
- Example: ["Implemented auth module", "Added unit tests"]

**decisions_made** (List[str], required)
- List of key decisions made
- Architectural or implementation choices
- Example: ["Use PostgreSQL", "JWT for auth"]

**unresolved_issues** (List[str], required)
- List of issues still to address
- Blockers or pending items
- Example: ["Performance optimization needed", "Deploy to prod"]

**response_format** (str, optional, default="summary")
- `"summary"` - Compact summary only
- `"detailed"` - Summary plus recommendations and next steps

#### Returns

**Summary format:**
```python
{
    "success": True,
    "data": {
        "compact_summary": "Completed (3 items):\n  ✓ Task 1\n...",
        "items_completed": 3,
        "items_decided": 2,
        "items_unresolved": 1,
        "total_items": 6,
        "estimated_tokens": 234,
        "usage_tip": "Use this summary to replace verbose conversation history"
    }
}
```

**Detailed format:**
```python
{
    "success": True,
    "data": {
        "compact_summary": "Completed (3 items):\n  ✓ Task 1\n...",
        "items_completed": 3,
        "items_decided": 2,
        "items_unresolved": 1,
        "total_items": 6,
        "estimated_tokens": 234,
        "usage_tip": "Use this summary to replace verbose conversation history",
        "recommendations": [
            "Save this summary with create_notes() for persistence",
            "Clear old conversation history",
            "Continue with fresh context using this summary",
            "Reference specific items by number when needed"
        ],
        "next_steps": [
            "Persist summary to notes if needed",
            "Clear conversation (if supported)",
            "Continue work referencing summary"
        ]
    }
}
```

---

## Common Workflows

### Workflow 1: Proactive Context Monitoring

```python
from skills.context_manager.operations import analyze_context_usage, create_notes

# At regular intervals
def check_context(current_tokens):
    analysis = analyze_context_usage(current_tokens)

    if analysis.data['usage_percent'] > 50:
        print(f"⚠ Context at {analysis.data['usage_percent']}%")

        # Get detailed recommendations
        detailed = analyze_context_usage(
            current_tokens,
            response_format="detailed"
        )

        # Act on top recommendations
        for rec in detailed.data['recommendations']:
            if rec['priority'] == 'high':
                print(f"  ACTION: {rec['description']}")

# Check every major operation
check_context(50000)
check_context(100000)
check_context(150000)
```

### Workflow 2: Long-Horizon Task Management

```python
from skills.context_manager.operations import (
    create_notes,
    compact_conversation,
    analyze_context_usage
)

# Start of task
create_notes("""
Task: Implement Feature X
Started: 2025-01-15
Approach: Microservices architecture
""")

# During task - save decisions
create_notes("""
Decision Log:
- Database: PostgreSQL
- Cache: Redis
- API: REST with JWT
""")

# End of work session
summary = compact_conversation(
    work_completed=[
        "Set up project structure",
        "Implemented auth module",
        "Added database migrations"
    ],
    decisions_made=[
        "Use PostgreSQL for persistence",
        "JWT tokens with 60min expiry",
        "Redis for session storage"
    ],
    unresolved_issues=[
        "Performance testing needed",
        "Deploy to staging environment"
    ]
)

# Save summary
create_notes(f"""
Session Summary:
{summary.data['compact_summary']}
""")

# Check context before continuing
analysis = analyze_context_usage(estimated_tokens=120000)
if analysis.data['usage_percent'] > 75:
    print("Consider starting fresh session with summary")
```

### Workflow 3: Emergency Context Reduction

```python
# When approaching limits
analysis = analyze_context_usage(estimated_tokens=180000)

if analysis.data['status'] == 'critical':
    print("🚨 Critical context usage!")

    # 1. Save all important info
    create_notes("""
    CRITICAL SAVE - Context overflow imminent

    Current State:
    - Feature X: 80% complete
    - Tests: Passing
    - Deploy: Blocked on approval

    Key Decisions:
    - Architecture: Microservices
    - Database: PostgreSQL
    - Cache: Redis

    TODO:
    - Get approval for deployment
    - Run performance tests
    - Update documentation
    """)

    # 2. Create compact summary
    summary = compact_conversation(
        work_completed=["All completed tasks"],
        decisions_made=["All key decisions"],
        unresolved_issues=["All remaining items"]
    )

    # 3. Continue with summary
    print("Context saved. Use summary to continue:")
    print(summary.data['compact_summary'])
```

---

## Best Practices

### 1. Monitor Proactively

```python
# ✅ Good: Check regularly
analysis = analyze_context_usage(current_tokens)
if analysis.data['usage_percent'] > 50:
    # Take action early

# ❌ Bad: Wait until overflow
# Context at 95% - too late!
```

### 2. Use Notes for Important Info

```python
# ✅ Good: Save important decisions
create_notes("Decided to use PostgreSQL for better performance")

# ❌ Bad: Keep everything in context
# Hundreds of lines of conversation history...
```

### 3. Compact Regularly

```python
# ✅ Good: Compact after major milestones
compact_conversation(
    work_completed=["Phase 1", "Phase 2"],
    decisions_made=["Key decisions"],
    unresolved_issues=["Remaining items"]
)

# ❌ Bad: Never compact
# Entire conversation history in context...
```

### 4. Use Response Formats

```python
# ✅ Good: Use summary when possible
result = operation(response_format="summary")

# ❌ Bad: Always use detailed
result = operation(response_format="detailed")  # Wastes 80-95% tokens
```

---

## Token Savings Examples

### Example 1: Using Summary Formats

```python
# Before: Always detailed
result = analyze_codebase("src/", response_format="detailed")
# 50,000 tokens

# After: Summary first
result = analyze_codebase("src/")  # Default: summary
# 500 tokens
# Savings: 49,500 tokens (99%)!
```

### Example 2: Local Filtering

```python
# Before: Return all data
result = analyze_codebase("src/", response_format="detailed")
# Agent receives 50,000 tokens (1000 files)

# After: Filter locally
from skills.common.filters import ResultFilter

result = analyze_codebase("src/", response_format="filtered")
auth_files = ResultFilter.search(result.data["files"], "auth")
# Agent receives only ~50 files (2,500 tokens)
# Savings: 47,500 tokens (95%)!
```

### Example 3: Persistent Notes

```python
# Before: Keep in context
# Conversation includes 5,000 tokens of decisions and notes

# After: Save to notes
create_notes("""
All important decisions and context
""")
# Frees up 5,000 tokens
# Savings: 5,000 tokens (100% of that info)!
```

### Example 4: Conversation Compaction

```python
# Before: Full conversation history
# 20,000 tokens of detailed conversation

# After: Compact summary
summary = compact_conversation(
    work_completed=["10 completed tasks"],
    decisions_made=["5 key decisions"],
    unresolved_issues=["3 remaining items"]
)
# 500 tokens of compact summary
# Savings: 19,500 tokens (97.5%)!
```

---

## Performance Notes

### Token Usage

| Operation | Tokens | Purpose |
|-----------|--------|---------|
| analyze_context_usage (summary) | < 200 | Quick check |
| analyze_context_usage (detailed) | < 500 | Full analysis |
| create_notes | < 100 | Save info |
| compact_conversation (summary) | 200-500 | Create summary |
| compact_conversation (detailed) | 300-700 | With recommendations |

### Execution Time

- All operations: < 0.1s
- Very fast, minimal overhead

---

## Related Skills

- **All skills** - Use context_manager with any skill to optimize token usage
- **ResultFilter** - For local filtering (95-99% savings)

---

## Dependencies

### Required

- Python 3.8+
- Standard library only

### Optional

- None

---

*Last Updated: 2025-11-08*

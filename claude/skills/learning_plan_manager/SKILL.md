---
name: learning-plan-manager
description: Parse, query, update, and manage structured learning plan markdown files. Designed for teaching-first workflows with progress tracking and student journey management.
version: 1.0.0
category: learning
tags:
  - learning
  - education
  - progress-tracking
  - teaching
  - planning
activation: manual
tools:
  - Read
  - Write
dependencies: []
---

# Learning Plan Manager Skill

## When to Use This Skill

Use learning-plan-manager when you need to:
- **Load learning plans** - Parse structured markdown learning plans
- **Track progress** - Get current status, completed tasks, next steps
- **Find plans** - Locate the latest or specific learning plans
- **List plans** - Get overview of all available plans
- **Update progress** - Mark tasks complete, add reflections
- **Query plan data** - Get specific phases, tasks, or progress metrics

**Not for:** Creating new plans (use plan-generation-mentor agent for that)

## Quick Start

```python
from skills.learning_plan_manager.operations import load_plan, find_latest_plan

# 1. Find most recent plan
result = find_latest_plan("plans/")
print(f"Latest: {result.data['plan_name']}")

# 2. Load plan (summary format for efficiency)
plan = load_plan("plans/navigation-plan.md")
print(f"Progress: {plan.data['overall_progress']}%")
print(f"Next task: {plan.data['next_task']['description']}")

# 3. Get current status only (even more efficient)
status = load_plan("plans/navigation-plan.md", response_format="progress")
print(f"Current phase: {status.data['current_phase']['name']}")
```

For detailed documentation, see **reference.md**.
For usage examples, see **examples.md**.

## Operations

### load_plan(file_path, response_format="summary")
Load and parse a learning plan from markdown file.

**Returns:** Overview and next steps (summary), current status (progress), or full plan (detailed)

### find_latest_plan(plans_dir="plans/", response_format="summary")
Find most recently modified learning plan.

**Returns:** Plan name and metadata (summary) or full plan data (detailed/progress)

### list_plans(plans_dir="plans/", response_format="summary")
List all available learning plans.

**Returns:** Names and topics (summary) or full metadata (detailed)

See **reference.md** for complete parameter specifications and response formats.

## Token Efficiency

This skill provides excellent token savings for large learning plans:

| Operation | Format | Token Usage | Use When |
|-----------|--------|-------------|----------|
| load_plan | summary | 300-500 | Quick check, planning |
| load_plan | progress | 200-300 | Current status only |
| load_plan | detailed | 2000-5000 | Need all phases/tasks |
| find_latest_plan | summary | 300-500 | Find recent plan |
| list_plans | summary | 200-400 | Overview of all plans |

**Best Practice:** Start with summary or progress format to minimize token usage.

## Learning Plan Structure

Learning plans are structured markdown files:

```markdown
# Learning Plan: [Topic]

**Student:** [Name]
**Created:** [Date]
**Level:** [Beginner/Intermediate/Advanced]

## Phase 1: [Phase Name]

**Goal:** [Phase goal]

### Tasks

1. [x] Task 1 description
2. [ ] Task 2 description (current)
3. [ ] Task 3 description

### Journal

**2025-01-15:** Reflection on completed task

## Phase 2: [Phase Name]
...
```

## Example Workflow

```python
# 1. Find student's current plan
result = find_latest_plan("plans/")
plan_file = result.data['file_path']

# 2. Check progress (minimal tokens)
status = load_plan(plan_file, response_format="progress")
print(f"Current phase: {status.data['current_phase']['name']}")
print(f"Next task: {status.data['next_task']['description']}")

# 3. If needed, get full details for specific phase
if status.data['overall_progress'] < 50:
    # Still early, get full plan to understand scope
    full_plan = load_plan(plan_file, response_format="detailed")
    # Work with full phase/task data
```

## Error Handling

All operations return `OperationResult` with agent-friendly errors:

```python
result = load_plan("nonexistent-plan.md")

if not result.success:
    print(result.error)       # "Learning plan not found: nonexistent-plan.md"
    print(result.error_code)  # "PLAN_NOT_FOUND"

    # Actionable suggestions
    for suggestion in result.suggestions:
        print(f"  - {suggestion}")
    # - Check if the file path is correct
    # - Use find_latest_plan() to locate plans
    # - Use list_plans() to see available plans

    # Example fix
    print(result.example_fix)
    # load_plan('plans/navigation-plan.md')
```

## Integration

**With Learning Coordinator Agent:**
```python
# Load student's current plan
plan = load_plan("plans/current.md", response_format="progress")

# Coordinate next teaching steps based on progress
if plan.data['next_task']:
    task = plan.data['next_task']['description']
    # Guide student through this task
```

**With Learning Analytics:**
```python
# Load plan for analytics
plan = load_plan("plans/navigation-plan.md", response_format="detailed")

# Analyze with learning_analytics skill
from skills.learning_analytics import analyze_progress
analytics = analyze_progress(plan.data)

# Get velocity, struggle points, recommendations
print(f"Velocity: {analytics.data['velocity']}")
```

**With Session State:**
```python
# Track which plan student is working on
from skills.session_state import update_session
update_session(
    student_id="alice",
    current_plan=plan.data['plan_name'],
    current_phase=plan.data['current_phase']['number']
)
```

## Next Steps

- **Read reference.md** for complete API documentation
- **Read examples.md** for real-world usage patterns
- **Try with sample plans** in `plans/` directory
- **Combine with learning_analytics** for progress insights

---

*Last Updated: 2025-11-08*

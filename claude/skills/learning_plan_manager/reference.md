# Learning Plan Manager - API Reference

Complete documentation for all learning_plan_manager operations.

---

## Overview

Learning Plan Manager provides operations for managing structured markdown learning plans. It parses learning plan files, tracks progress, and provides student journey insights for teaching-first workflows.

---

## Operations

### load_plan

Load and parse a learning plan from a markdown file.

#### Signature

```python
def load_plan(
    file_path: str,
    response_format: str = "summary",
    **kwargs
) -> OperationResult
```

#### Parameters

**file_path** (str, required)
- Path to learning plan markdown file
- Can be relative or absolute path
- Must be a valid learning plan file

**response_format** (str, optional, default="summary")
- Controls the detail level of the response
- Options:
  - `"summary"` - Overview with next steps (300-500 tokens)
  - `"progress"` - Current status only (200-300 tokens)
  - `"detailed"` - Full plan with all phases/tasks (2000-5000 tokens)

#### Returns

**OperationResult** with the following data structure:

**Summary format:**
```python
{
    "success": True,
    "data": {
        "plan_name": "Autonomous Navigation Learning Journey",
        "topic": "autonomous navigation",
        "created": "2025-01-15T10:00:00",
        "total_phases": 6,
        "overall_progress": 33.3,
        "current_phase": {
            "name": "Research & Learning",
            "number": 2
        },
        "next_task": {
            "description": "Study ROS2 navigation stack documentation",
            "phase": "Research & Learning"
        },
        "efficiency_tip": "For current status only: load_plan(..., response_format='progress')"
    }
}
```

**Progress format (most token-efficient):**
```python
{
    "success": True,
    "data": {
        "current_phase": {
            "name": "Research & Learning",
            "number": 2,
            "progress": 50.0
        },
        "next_task": {
            "description": "Study ROS2 navigation stack documentation",
            "phase": "Research & Learning",
            "task_number": 3
        },
        "overall_progress": 33.3,
        "total_tasks": 30,
        "completed_tasks": 10,
        "efficiency_tip": "Use 'detailed' format only when you need all phases/tasks"
    }
}
```

**Detailed format:**
```python
{
    "success": True,
    "data": {
        "plan_name": "Autonomous Navigation Learning Journey",
        "topic": "autonomous navigation",
        "student": "Alice",
        "level": "beginner",
        "created": "2025-01-15T10:00:00",
        "total_phases": 6,
        "overall_progress": 33.3,
        "phases": [
            {
                "phase_number": 1,
                "name": "Setup & Prerequisites",
                "goal": "Set up development environment",
                "status": "completed",
                "progress": 100.0,
                "tasks": [
                    {
                        "task_number": 1,
                        "description": "Install ROS2",
                        "status": "completed",
                        "completed_date": "2025-01-16"
                    },
                    {
                        "task_number": 2,
                        "description": "Configure workspace",
                        "status": "completed",
                        "completed_date": "2025-01-17"
                    }
                ],
                "journal_entries": [
                    {
                        "date": "2025-01-17",
                        "content": "Successfully set up ROS2 workspace"
                    }
                ]
            },
            {
                "phase_number": 2,
                "name": "Research & Learning",
                "goal": "Understand navigation concepts",
                "status": "in_progress",
                "progress": 50.0,
                "tasks": [
                    {
                        "task_number": 1,
                        "description": "Read navigation overview",
                        "status": "completed",
                        "completed_date": "2025-01-18"
                    },
                    {
                        "task_number": 2,
                        "description": "Watch navigation tutorials",
                        "status": "completed",
                        "completed_date": "2025-01-19"
                    },
                    {
                        "task_number": 3,
                        "description": "Study ROS2 navigation stack",
                        "status": "pending",
                        "completed_date": null
                    }
                ],
                "journal_entries": []
            },
            // ... more phases
        ],
        "metadata": {
            "tags": ["ros2", "navigation", "robotics"],
            "difficulty": "intermediate",
            "estimated_hours": 120
        }
    }
}
```

#### Error Handling

**PLAN_NOT_FOUND:**
```python
{
    "success": False,
    "error": "Learning plan not found: plans/nonexistent.md",
    "error_code": "PLAN_NOT_FOUND",
    "suggestions": [
        "Check if the file path is correct",
        "Use find_latest_plan() to locate plans",
        "Use list_plans() to see available plans"
    ],
    "example_fix": "load_plan('plans/navigation-plan.md')"
}
```

**INVALID_PLAN_FORMAT:**
```python
{
    "success": False,
    "error": "Invalid learning plan format: missing required sections",
    "error_code": "INVALID_PLAN_FORMAT",
    "suggestions": [
        "Check that file has required markdown structure",
        "Ensure metadata section exists",
        "Verify phases and tasks are properly formatted"
    ],
    "example_fix": "Use plan-generation-mentor to create valid plan"
}
```

#### Token Efficiency

- **Progress format:** 200-300 tokens (most efficient for status check)
- **Summary format:** 300-500 tokens (good for overview)
- **Detailed format:** 2000-5000 tokens (only when needed)

**Savings:** Up to 95% when using progress instead of detailed

---

### find_latest_plan

Find the most recently modified learning plan in a directory.

#### Signature

```python
def find_latest_plan(
    plans_dir: str = "plans/",
    response_format: str = "summary",
    **kwargs
) -> OperationResult
```

#### Parameters

**plans_dir** (str, optional, default="plans/")
- Directory containing learning plans
- Searches for `*-plan.md` files
- Returns most recently modified

**response_format** (str, optional, default="summary")
- Same options as `load_plan`
- "summary" returns just metadata
- "progress" or "detailed" loads full plan

#### Returns

**OperationResult** with:

**Summary format:**
```python
{
    "success": True,
    "data": {
        "plan_name": "Autonomous Navigation Learning Journey",
        "file_path": "plans/navigation-plan.md",
        "topic": "autonomous navigation",
        "modified": "2025-01-20T14:30:00",
        "total_phases": 6,
        "efficiency_tip": "Found latest plan. Use load_plan() with 'progress' format for status."
    }
}
```

**Progress/Detailed format:**
- Automatically calls `load_plan()` with specified format
- Returns same structure as `load_plan`

#### Error Handling

**NO_PLANS_FOUND:**
```python
{
    "success": False,
    "error": "No learning plans found in: plans/",
    "error_code": "NO_PLANS_FOUND",
    "suggestions": [
        "Check if directory exists and contains *-plan.md files",
        "Use plan-generation-mentor to create a learning plan",
        "Verify you're in the correct directory"
    ],
    "example_fix": "Ensure plans directory has .md files"
}
```

---

### list_plans

List all available learning plans in a directory.

#### Signature

```python
def list_plans(
    plans_dir: str = "plans/",
    response_format: str = "summary",
    **kwargs
) -> OperationResult
```

#### Parameters

**plans_dir** (str, optional, default="plans/")
- Directory containing learning plans
- Searches for `*-plan.md` files

**response_format** (str, optional, default="summary")
- `"summary"` - Just names and topics
- `"detailed"` - Full metadata for each plan

#### Returns

**OperationResult** with:

**Summary format:**
```python
{
    "success": True,
    "data": {
        "total_plans": 3,
        "plans": [
            {
                "name": "Autonomous Navigation Learning Journey",
                "file_path": "plans/navigation-plan.md",
                "topic": "autonomous navigation"
            },
            {
                "name": "Python Testing Mastery",
                "file_path": "plans/testing-plan.md",
                "topic": "python testing"
            },
            {
                "name": "ROS2 Fundamentals",
                "file_path": "plans/ros2-plan.md",
                "topic": "ros2 basics"
            }
        ]
    }
}
```

**Detailed format:**
```python
{
    "success": True,
    "data": {
        "total_plans": 3,
        "plans": [
            {
                "name": "Autonomous Navigation Learning Journey",
                "file_path": "plans/navigation-plan.md",
                "topic": "autonomous navigation",
                "student": "Alice",
                "level": "beginner",
                "created": "2025-01-15T10:00:00",
                "total_phases": 6,
                "overall_progress": 33.3,
                "current_phase": "Research & Learning"
            },
            // ... more plans with full metadata
        ]
    }
}
```

---

## Learning Plan File Format

### Required Structure

```markdown
# Learning Plan: [Title]

**Student:** [Name]
**Created:** [YYYY-MM-DD]
**Level:** [Beginner/Intermediate/Advanced]
**Topic:** [Topic]

## Phase 1: [Phase Name]

**Goal:** [Phase goal description]

### Tasks

1. [x] Completed task description
2. [ ] Pending task description
3. [ ] Another pending task

### Journal

**YYYY-MM-DD:** Journal entry reflecting on progress
**YYYY-MM-DD:** Another journal entry

## Phase 2: [Phase Name]
...
```

### Task Status

- `[x]` - Completed task
- `[ ]` - Pending task
- First pending task is considered "current task"

### Phase Status

- **Completed:** All tasks marked `[x]`
- **In Progress:** Some tasks completed, some pending
- **Pending:** No tasks completed

---

## Common Workflows

### Workflow 1: Check Student Progress

```python
# Find their current plan
plan = find_latest_plan("plans/students/alice/")

# Get just current status (200 tokens)
status = load_plan(plan.data['file_path'], response_format="progress")

print(f"Alice is on phase {status.data['current_phase']['number']}")
print(f"Next task: {status.data['next_task']['description']}")
print(f"Overall progress: {status.data['overall_progress']}%")

# Decide next teaching action based on progress
```

### Workflow 2: Resume Learning Session

```python
# Find where student left off
plan = find_latest_plan()

# Get overview
overview = load_plan(plan.data['file_path'], response_format="summary")

# If early in plan, get full details to understand scope
if overview.data['overall_progress'] < 25:
    full_plan = load_plan(plan.data['file_path'], response_format="detailed")
    # Review all phases to provide context
else:
    # Just work on current task
    print(f"Continue with: {overview.data['next_task']['description']}")
```

### Workflow 3: List All Students' Plans

```python
# Get all plans
plans = list_plans("plans/", response_format="summary")

print(f"Managing {plans.data['total_plans']} learning plans:")
for plan in plans.data['plans']:
    print(f"  - {plan['topic']} ({plan['name']})")

# Load specific plan for detailed work
selected = load_plan(plans.data['plans'][0]['file_path'])
```

---

## Best Practices

### 1. Use Progress Format for Status Checks

```python
# ✅ Efficient: Just checking current status
status = load_plan("plan.md", response_format="progress")
# 200 tokens

# ❌ Wasteful: Loading entire plan just to check status
full = load_plan("plan.md", response_format="detailed")
# 5000 tokens - 96% waste!
```

### 2. Progressive Detail Loading

```python
# Start with summary
summary = load_plan("plan.md")

# Only get details if needed
if summary.data['overall_progress'] < 50:
    # Early stages - get full context
    detailed = load_plan("plan.md", response_format="detailed")
else:
    # Late stages - just work on current task
    # Use summary data
```

### 3. Find Before Load

```python
# ✅ Good: Find first, then load
latest = find_latest_plan()
plan = load_plan(latest.data['file_path'], response_format="progress")

# ❌ Bad: Guessing file path
plan = load_plan("plans/unknown-plan.md")  # Might not exist
```

---

## Integration Patterns

### With Learning Analytics

```python
from skills.learning_plan_manager import load_plan
from skills.learning_analytics import analyze_progress

# Load full plan for analytics
plan = load_plan("plan.md", response_format="detailed")

# Analyze progress patterns
analytics = analyze_progress(plan.data)

if analytics.data['velocity'] < 0.5:
    print("Student is struggling - adjust teaching approach")
```

### With Session State

```python
from skills.learning_plan_manager import find_latest_plan
from skills.session_state import update_session

# Find current plan
plan = find_latest_plan()
status = load_plan(plan.data['file_path'], response_format="progress")

# Update session state
update_session(
    student_id="alice",
    current_plan=status.data['plan_name'],
    current_phase=status.data['current_phase']['number'],
    next_task=status.data['next_task']['description']
)
```

### With Plan Generation

```python
from skills.learning_plan_manager import list_plans

# Check if student already has a plan
plans = list_plans("plans/alice/")

if plans.data['total_plans'] == 0:
    # Use plan-generation-mentor agent to create one
    pass
else:
    # Continue existing plan
    latest = find_latest_plan("plans/alice/")
```

---

## Performance Notes

### Execution Time

- **find_latest_plan:** < 0.1s (scans directory)
- **list_plans:** < 0.2s (scans directory + parses metadata)
- **load_plan:** 0.1-0.5s (depends on plan size)

### Token Usage Summary

| Operation | Summary | Progress | Detailed | Savings |
|-----------|---------|----------|----------|---------|
| load_plan | 300-500 | 200-300 | 2000-5000 | 90-95% |
| find_latest_plan | 200-300 | 200-300 | 2000-5000 | Same as load_plan |
| list_plans | 200-400 | N/A | 1000-3000 | 70-80% |

---

## Related Skills

- **learning_analytics** - Analyze progress velocity, detect struggles
- **session_state** - Track student sessions and context
- **plan_generation_mentor** (agent) - Create new learning plans
- **interactive_diagram** - Visualize learning journey

---

## Dependencies

### Required

- Python 3.8+
- Markdown parsing (built-in)

### Optional

- None

---

*Last Updated: 2025-11-08*

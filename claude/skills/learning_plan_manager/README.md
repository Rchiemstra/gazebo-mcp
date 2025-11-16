# Learning Plan Manager Skill

**Version**: 0.1.0
**Status**: ✅ Fully Implemented and Tested

## Overview

The `learning-plan-manager` skill provides structured operations on learning plan markdown files, eliminating the need for manual markdown parsing in agents.

## Features

- **Parse** learning plan markdown into structured Pydantic models
- **Query** plan status, progress, current phase, next tasks
- **Update** task status, checkpoints, journal entries
- **Export** to JSON, progress reports
- **Validate** plan structure and format

## Installation

The skill is already installed in the `skills/` directory. To use it:

```python
from skills.learning_plan_manager import LearningPlanManager

manager = LearningPlanManager()
```

## Quick Start

```python
from skills.learning_plan_manager import LearningPlanManager, TaskStatus

# Initialize
manager = LearningPlanManager()

# Load the most recent plan
plan = manager.find_latest_plan()

# Query current status
current_phase = plan.get_current_phase()
next_task = plan.get_next_task()
progress = plan.calculate_progress()

print(f"Phase: {current_phase.title}")
print(f"Next: {next_task.title}")
print(f"Progress: {progress['overall_percentage']:.1f}%")

# Update a task
plan = manager.update_task_status(
    plan,
    next_task.id,
    TaskStatus.COMPLETED,
    notes="Finished successfully"
)

# Save changes
manager.save_plan(plan)

# Generate progress report
report = manager.export_progress_report(plan)
print(report)
```

## Usage in Agents

Agents can invoke this skill via the Skill tool:

```markdown
Agent prompt: "What phase is the student in?"

Agent uses: Skill(learning-plan-manager)

Skill returns: {
  "current_phase": {
    "number": 1,
    "title": "Understanding & Research",
    "next_task": "Educational Theory Research"
  },
  "progress": 23.5
}

Agent teaches: "You're in Phase 1: Understanding & Research.
Your next task is Educational Theory Research. You're 23.5% through overall!"
```

## API Reference

### Manager Methods

**Query Operations:**
- `load_plan(file_path)` - Load and parse a learning plan
- `find_latest_plan()` - Get most recently updated plan
- `list_plans()` - List all available plans with metadata
- `get_phase_summary(plan, phase_id)` - Get detailed phase info
- `search_tasks(plan, query)` - Find tasks matching query

**Update Operations:**
- `update_task_status(plan, task_id, status, notes?)` - Update task
- `update_checkpoint_status(plan, checkpoint_id, status, notes?)` - Update checkpoint
- `add_journal_entry(plan, entry)` - Add journal entry
- `mark_phase_started(plan, phase_id)` - Mark phase as started
- `mark_phase_completed(plan, phase_id)` - Mark phase as completed
- `save_plan(plan)` - Save changes to markdown file

**Export Operations:**
- `export_json(plan)` - Export as JSON
- `export_progress_report(plan)` - Generate markdown progress report

### Plan Methods

The `LearningPlan` object has these helpful methods:

- `plan.get_current_phase()` - Get the currently active phase
- `plan.get_next_task(phase_id?)` - Get next task to work on
- `plan.calculate_progress()` - Calculate progress statistics

## Data Models

All data is validated using Pydantic models:

- `LearningPlan` - Complete plan with metadata, phases, journal
- `Phase` - Learning phase with tasks and checkpoints
- `Task` - Individual learning task
- `Checkpoint` - Understanding verification checkpoint
- `JournalEntry` - Learning journal entry
- `Prerequisite` - Prerequisite check item

**Enums:**
- `TaskStatus` - NOT_STARTED, IN_PROGRESS, COMPLETED, BLOCKED, SKIPPED
- `CheckpointStatus` - NOT_REACHED, IN_REVIEW, PASSED, NEEDS_WORK
- `ComplexityLevel` - BEGINNER, INTERMEDIATE, ADVANCED, EXPERT

## Testing

Run the test suite:

```bash
python examples/test_learning_plan_manager.py
```

All tests should pass ✅

## Integration Examples

### With /continue-plan command

```python
# learning-coordinator agent
def continue_learning():
    manager = LearningPlanManager()
    plan = manager.find_latest_plan()

    current = plan.get_current_phase()
    next_task = plan.get_next_task()
    progress = plan.calculate_progress()

    return {
        "welcome_back_message": f"You're in {current.title}",
        "next_task": next_task.title,
        "progress": progress['overall_percentage']
    }
```

### With plan-generation-mentor

```python
# Validate generated plans
def validate_plan(plan_path):
    manager = LearningPlanManager()
    try:
        plan = manager.load_plan(plan_path)
        print("✅ Plan is valid!")
        return True
    except ValidationError as e:
        print(f"❌ Plan has issues: {e}")
        return False
```

## Performance

- **Parsing**: <100ms for typical plans
- **Updates**: In-memory (fast)
- **Saving**: <50ms for typical plans
- **No caching**: Plans may be edited externally

## Limitations

- Currently only supports the learning plan markdown format used in this project
- No versioning/history tracking (Git handles that)
- Large plans (>1000 tasks) may be slower

## Future Enhancements

Potential improvements:
- Export to HTML/PDF (currently markdown and JSON only)
- Plan templates for common learning journeys
- Analytics dashboard generation
- Integration with learning-analytics skill (Phase 2)
- Batch operations on multiple plans

## Files

```
skills/learning_plan_manager/
├── __init__.py       # Package exports
├── models.py         # Pydantic data models
├── parser.py         # Markdown → structured data
├── writer.py         # Structured data → markdown
├── validator.py      # Plan structure validation
├── manager.py        # Main API
├── skill.md          # Skill definition for agents
└── README.md         # This file
```

## License

Part of the Claude Code Learning System.

## Support

For issues or questions:
1. Check the technical spec: `docs/PHASE1_SKILLS_TECHNICAL_SPEC.md`
2. Review test examples: `examples/test_learning_plan_manager.py`
3. See skill definition: `skills/learning_plan_manager/skill.md`

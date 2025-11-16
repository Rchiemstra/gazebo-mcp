# session-state Skill

**Persistent student state management for personalized, adaptive learning.**

The session-state skill manages cross-session student data including profiles, learning history, achievements, and teaching insights. It enables truly personalized learning by remembering what works for each student and maintaining continuity across sessions.

---

## Features

✅ **Student Profiles** - Store learning preferences and settings
✅ **Session Tracking** - Track sessions over time for continuity
✅ **Learning History** - All-time statistics and progress tracking
✅ **Achievement System** - 15+ achievements for motivation
✅ **Teaching Memory** - Remember what teaching strategies work
✅ **File-Based Persistence** - Simple JSON storage, no database needed

---

## Quick Start

```python
from skills.session_state import StateManager

# Initialize
manager = StateManager()

# Create student
state = manager.create_student(
    student_id="alex_2025",
    name="Alex",
    learning_style="visual",
    difficulty_preference="intermediate"
)

# Start session
session = manager.start_session("alex_2025", plan_id="nav_plan_1")

# End session
manager.end_session("alex_2025", "Great progress today!")

# Check achievements
new_achievements = manager.check_achievements("alex_2025")
for achievement in new_achievements:
    print(f"🎉 {achievement.title}")
```

---

## Installation

No installation needed - the skill uses only Python standard library and Pydantic (already required).

**Directory structure:**
```
skills/session_state/
├── __init__.py          - Package exports
├── models.py            - Data models (6 models)
├── state_manager.py     - Main StateManager class
├── achievements.py      - Achievement definitions & logic
├── skill.md             - Agent integration guide
└── README.md            - This file
```

**Storage:**
```
student_states/          - Created automatically
├── student_alex_2025.json
├── student_jordan_2025.json
└── ...
```

---

## Core Concepts

### 1. Student Profile

Stores preferences and settings:
- Learning style (visual, hands-on, reading, listening, mixed)
- Difficulty preference (beginner, intermediate, advanced, adaptive)
- Preferred pace (slow, moderate, fast)
- Display preferences (diagrams, celebrations)
- Preferred specialists

### 2. Sessions

Track individual learning sessions:
- Start/end time, duration
- Tasks completed
- Questions asked
- Specialists consulted
- Session notes

### 3. Learning History

All-time statistics:
- Plans completed (with details)
- Total tasks/checkpoints
- Average velocity
- Most struggled topics
- Favorite specialists

### 4. Achievements

15+ achievements across 5 categories:
- **Milestone** - Complete tasks, plans (5 achievements)
- **Streak** - Learn consecutive days (3 achievements)
- **Speed** - Fast completion (3 achievements)
- **Mastery** - Perfect performance (2 achievements)
- **Persistence** - Overcome struggles (2 achievements)

### 5. Teaching Memory

What works for this student:
- Effective strategies
- Ineffective strategies
- Learns best when...
- Struggles with...
- Specialist effectiveness ratings

---

## API Reference

### StateManager Class

Main class for managing student state.

```python
from skills.session_state import StateManager

manager = StateManager(storage_dir="student_states/")
```

#### Profile Management

**create_student(student_id, name=None, \*\*preferences) → StudentState**

Create new student profile.

```python
state = manager.create_student(
    "alex_2025",
    name="Alex",
    learning_style="visual",
    difficulty_preference="intermediate",
    show_diagrams=True
)
```

**get_student(student_id) → StudentState | None**

Load existing student.

```python
state = manager.get_student("alex_2025")
```

**update_profile(student_id, \*\*updates) → StudentState**

Update profile fields.

```python
state = manager.update_profile(
    "alex_2025",
    learning_style="hands_on",
    preferred_pace="fast"
)
```

#### Session Management

**start_session(student_id, plan_id=None) → Session**

Start new learning session.

```python
session = manager.start_session("alex_2025", plan_id="nav_1")
```

**end_session(student_id, session_notes="") → Session**

End current session.

```python
session = manager.end_session("alex_2025", "Great progress!")
```

**get_current_session(student_id) → Session | None**

Get active session.

```python
session = manager.get_current_session("alex_2025")
```

#### Learning History

**add_plan_to_history(student_id, plan_history)**

Add completed plan to history.

```python
from skills.session_state import PlanHistory

plan_hist = PlanHistory(
    plan_id="nav_1",
    plan_title="Navigation System",
    started_at="2025-10-01",
    completed_at="2025-10-15",
    total_tasks=20,
    completed_tasks=20,
    completion_percentage=100.0,
    average_velocity=2.5,
    total_time_weeks=2.0,
    checkpoints_passed=4,
    checkpoints_failed=0
)

manager.add_plan_to_history("alex_2025", plan_hist)
```

**get_learning_history(student_id) → LearningHistory**

Get complete history.

```python
history = manager.get_learning_history("alex_2025")
print(f"Completed: {history.completed_plans} plans")
print(f"Total tasks: {history.total_tasks_completed}")
```

**get_recent_activity(student_id, days=7) → dict**

Get recent activity summary.

```python
activity = manager.get_recent_activity("alex_2025", days=7)
print(f"Last session: {activity['last_session']}")
print(f"Sessions: {activity['sessions_this_period']}")
print(f"Tasks: {activity['tasks_completed_this_period']}")
```

#### Achievements

**check_achievements(student_id, analytics=None) → List[Achievement]**

Check for new achievements.

```python
new_achievements = manager.check_achievements("alex_2025")

for achievement in new_achievements:
    print(f"{achievement.icon} {achievement.title}")
    print(f"   {achievement.description}")
```

**get_achievements(student_id) → List[Achievement]**

Get all achievements.

```python
achievements = manager.get_achievements("alex_2025")
print(f"Total: {len(achievements)}")
```

#### Teaching Memory

**record_teaching_strategy(student_id, strategy, effective)**

Record strategy effectiveness.

```python
manager.record_teaching_strategy(
    "alex_2025",
    "visual diagrams with annotations",
    effective=True
)
```

**record_specialist_interaction(student_id, specialist, helpful)**

Record specialist effectiveness.

```python
manager.record_specialist_interaction(
    "alex_2025",
    "robotics-vision-navigator",
    helpful=True
)
```

**get_teaching_insights(student_id) → TeachingMemory**

Get teaching insights.

```python
insights = manager.get_teaching_insights("alex_2025")

print("Effective strategies:")
for strategy in insights.effective_strategies:
    print(f"  ✅ {strategy}")
```

#### Persistence

**save_state(student_state)**

Save state to file (auto-called by update methods).

**load_state(student_id) → StudentState | None**

Load state from file.

**list_students() → List[str]**

List all student IDs.

```python
students = manager.list_students()
print(f"Total students: {len(students)}")
```

---

## Data Models

### StudentProfile

```python
class StudentProfile(BaseModel):
    student_id: str
    name: Optional[str]

    # Preferences
    learning_style: LearningStyle
    difficulty_preference: DifficultyPreference
    preferred_pace: str
    preferred_specialists: List[str]

    # Settings
    show_diagrams: bool
    enable_celebrations: bool
```

### Session

```python
class Session(BaseModel):
    session_id: str
    student_id: str

    start_time: str
    end_time: Optional[str]
    duration_minutes: Optional[int]

    plan_id: Optional[str]
    tasks_completed: List[str]
    questions_asked: int
    session_notes: str
```

### LearningHistory

```python
class LearningHistory(BaseModel):
    student_id: str

    plans: List[PlanHistory]
    total_plans: int
    completed_plans: int

    total_tasks_completed: int
    total_checkpoints_passed: int
    average_velocity_all_time: float
    most_struggled_topics: List[str]
```

### Achievement

```python
class Achievement(BaseModel):
    achievement_id: str
    type: AchievementType
    title: str
    description: str

    earned_at: str
    criteria: str
    icon: str
    rarity: str
```

---

## Achievement Catalog

### Milestone Achievements

| Icon | Title | Criteria | Rarity |
|------|-------|----------|--------|
| 🎯 | First Task Complete | Complete 1 task | Common |
| ✅ | First Checkpoint Passed | Pass 1 checkpoint | Common |
| 🎓 | First Plan Complete | Complete 1 plan | Rare |
| 🌟 | Five Plans Complete | Complete 5 plans | Rare |
| 💎 | Ten Plans Complete | Complete 10 plans | Epic |

### Streak Achievements

| Icon | Title | Criteria | Rarity |
|------|-------|----------|--------|
| 🔥 | 3-Day Streak | Learn 3 consecutive days | Common |
| 🔥🔥 | 7-Day Streak | Learn 7 consecutive days | Rare |
| 🔥🔥🔥 | 30-Day Streak | Learn 30 consecutive days | Legendary |

### Speed Achievements

| Icon | Title | Criteria | Rarity |
|------|-------|----------|--------|
| ⚡ | Speed Learner | Complete 5 tasks in 1 day | Common |
| ⚡⚡ | Lightning Fast | Complete plan in 50% of time | Epic |
| ⚡⚡⚡ | Task Machine | Complete 10 tasks in 1 session | Rare |

### Mastery Achievements

| Icon | Title | Criteria | Rarity |
|------|-------|----------|--------|
| 💯 | Perfect Score | Pass all checkpoints (0 fails) | Epic |
| 🌟 | No Struggles | Complete plan with 0 struggles | Rare |

### Persistence Achievements

| Icon | Title | Criteria | Rarity |
|------|-------|----------|--------|
| 💪 | Comeback Kid | Complete task after 10+ days | Rare |
| 💪💪 | Never Give Up | Complete plan with 3+ struggles | Epic |

---

## Storage Format

### File Location

`student_states/student_{student_id}.json`

### Example File

```json
{
  "profile": {
    "student_id": "alex_2025",
    "name": "Alex",
    "learning_style": "visual",
    "difficulty_preference": "intermediate",
    "preferred_pace": "moderate",
    "show_diagrams": true,
    "enable_celebrations": true
  },
  "sessions": [
    {
      "session_id": "sess_0001",
      "student_id": "alex_2025",
      "start_time": "2025-10-19T10:00:00",
      "end_time": "2025-10-19T11:30:00",
      "duration_minutes": 90,
      "plan_id": "nav_plan_1",
      "tasks_completed": ["task-1-1", "task-1-2"],
      "questions_asked": 3
    }
  ],
  "history": {
    "student_id": "alex_2025",
    "plans": [
      {
        "plan_id": "nav_plan_1",
        "plan_title": "Navigation System",
        "started_at": "2025-10-01",
        "completed_at": "2025-10-15",
        "total_tasks": 20,
        "completed_tasks": 20,
        "completion_percentage": 100.0,
        "average_velocity": 2.5,
        "total_time_weeks": 2.0,
        "checkpoints_passed": 4,
        "checkpoints_failed": 0
      }
    ],
    "total_tasks_completed": 20,
    "total_checkpoints_passed": 4
  },
  "achievements": [
    {
      "achievement_id": "first_task",
      "type": "milestone",
      "title": "First Task Complete!",
      "description": "You completed your first task",
      "earned_at": "2025-10-01T14:30:00",
      "icon": "🎯",
      "rarity": "common"
    }
  ],
  "teaching_memory": {
    "student_id": "alex_2025",
    "effective_strategies": ["visual diagrams", "small tasks"],
    "learns_best_when": ["concepts shown visually"],
    "specialist_effectiveness": {
      "robotics-vision-navigator": 0.9
    }
  }
}
```

---

## Examples

### Example 1: Complete Session Workflow

```python
from skills.session_state import StateManager

manager = StateManager()

# Get or create student
state = manager.get_student("alex_2025")
if not state:
    state = manager.create_student(
        "alex_2025",
        name="Alex",
        learning_style="visual"
    )

# Start session
session = manager.start_session("alex_2025", plan_id="nav_1")

# During session
state = manager.get_student("alex_2025")
state.current_session.tasks_completed.append("task-1-1")
state.current_session.questions_asked += 1
manager.save_state(state)

# End session
session = manager.end_session("alex_2025", "Completed navigation basics")

# Check achievements
new_achievements = manager.check_achievements("alex_2025")
if new_achievements:
    print("\n🎉 Achievements Unlocked!")
    for achievement in new_achievements:
        print(f"{achievement.icon} {achievement.title}")
```

### Example 2: Get Student Overview

```python
def get_student_overview(student_id: str) -> str:
    manager = StateManager()
    state = manager.get_student(student_id)

    if not state:
        return "Student not found"

    # Get data
    history = state.history
    activity = manager.get_recent_activity(student_id, days=7)
    achievements = manager.get_achievements(student_id)

    # Format overview
    overview = f"## {state.profile.name}'s Profile\n\n"
    overview += f"**Learning Style:** {state.profile.learning_style}\n"
    overview += f"**Preferred Pace:** {state.profile.preferred_pace}\n\n"

    overview += f"**Recent Activity (7 days):**\n"
    overview += f"- Last session: {activity['last_session']}\n"
    overview += f"- Sessions: {activity['sessions_this_period']}\n"
    overview += f"- Tasks completed: {activity['tasks_completed_this_period']}\n\n"

    overview += f"**All-Time Stats:**\n"
    overview += f"- Plans completed: {history.completed_plans}\n"
    overview += f"- Total tasks: {history.total_tasks_completed}\n"
    overview += f"- Checkpoints passed: {history.total_checkpoints_passed}\n\n"

    overview += f"**Achievements ({len(achievements)}):**\n"
    for achievement in achievements[:5]:  # Show first 5
        overview += f"{achievement.icon} {achievement.title}\n"

    return overview
```

### Example 3: Personalize Based on History

```python
def should_use_visual_aids(student_id: str) -> bool:
    manager = StateManager()
    state = manager.get_student(student_id)

    if not state:
        return True  # Default to yes

    # Check preference
    if state.profile.learning_style == "visual":
        return True

    # Check teaching memory
    insights = manager.get_teaching_insights(student_id)
    if "visual diagrams" in insights.effective_strategies:
        return True

    if "visual" in insights.learns_best_when:
        return True

    return False
```

---

## Integration with Other Skills

### With learning-plan-manager

Track plan completion in history:

```python
from skills.learning_plan_manager import LearningPlanManager
from skills.session_state import StateManager, PlanHistory

plan_mgr = LearningPlanManager()
state_mgr = StateManager()

plan = plan_mgr.find_latest_plan()

# When plan completes
plan_hist = PlanHistory(
    plan_id=plan.metadata.plan_id,
    plan_title=plan.title,
    # ... fill in details ...
)

state_mgr.add_plan_to_history("alex_2025", plan_hist)
```

### With learning-analytics

Use analytics for achievement checking:

```python
from skills.learning_analytics import LearningAnalyzer
from skills.session_state import StateManager

analyzer = LearningAnalyzer()
state_mgr = StateManager()

analytics = analyzer.analyze_plan(plan)
new_achievements = state_mgr.check_achievements("alex_2025", analytics)
```

### With interactive-diagram

Visualize learning history:

```python
from skills.interactive_diagram import DiagramGenerator
from skills.session_state import StateManager

generator = DiagramGenerator()
state_mgr = StateManager()

history = state_mgr.get_learning_history("alex_2025")

# Could create timeline diagram of plans, achievement progress chart, etc.
```

---

## Best Practices

1. **Always check if student exists before creating**
   ```python
   state = manager.get_student(student_id)
   if not state:
       state = manager.create_student(student_id)
   ```

2. **End sessions cleanly**
   ```python
   # Always end session when done
   manager.end_session(student_id, "Session notes")
   ```

3. **Check achievements at natural milestones**
   ```python
   # After session
   manager.end_session(student_id)
   new_achievements = manager.check_achievements(student_id)
   ```

4. **Record specific teaching insights**
   ```python
   # Good - specific
   manager.record_teaching_strategy(
       student_id,
       "mermaid diagram showing ROS node connections",
       effective=True
   )

   # Bad - too vague
   manager.record_teaching_strategy(student_id, "diagram", effective=True)
   ```

5. **Use insights to personalize**
   ```python
   insights = manager.get_teaching_insights(student_id)
   # Adapt your teaching based on insights.effective_strategies
   ```

---

## Performance

- **File I/O**: ~10-50ms per save/load
- **Memory**: ~50-200KB per student
- **Scalability**: Handles 100-1000 students easily
- **Caching**: In-memory cache for active students

---

## Troubleshooting

**Q: Student already exists error**

A: Check if student exists first with `get_student()` before creating.

**Q: Session not ending**

A: Make sure to call `end_session()` before starting a new session.

**Q: Achievements not unlocking**

A: Call `check_achievements()` at session end or after adding plan to history.

**Q: File not found**

A: Student state is created on first `create_student()` call.

---

## See Also

- **skill.md** - Agent integration guide
- **PHASE4_SESSION_STATE_SPEC.md** - Technical specification
- **PHASE4_IMPLEMENTATION_PLAN.md** - Implementation details
- **examples/test_session_state.py** - Test suite

---

**Version:** 1.0
**Created:** 2025-10-19
**Part of:** Phase 4 Skills System

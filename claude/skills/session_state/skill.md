---
name: session-state
version: 1.0.0
description: Manages persistent student state across learning sessions, enabling personalized, adaptive teaching
category: learning-and-education
tools:
  - Read
  - Write
operations:
  create_student: "Create a new student profile with learning preferences"
  get_student: "Retrieve student state and profile"
  update_profile: "Update student learning preferences"
  start_session: "Start a new learning session"
  end_session: "End current session and check achievements"
  get_current_session: "Get active session information"
  add_plan_to_history: "Add completed plan to learning history"
  get_learning_history: "Get student's learning history and statistics"
  get_recent_activity: "Get recent activity within specified time period"
  check_achievements: "Check for newly earned achievements"
  get_achievements: "Get all student achievements"
  record_teaching_strategy: "Record effectiveness of teaching strategy"
  record_specialist_interaction: "Record specialist interaction feedback"
  get_teaching_insights: "Get personalized teaching insights"
dependencies: []
---

# session-state Skill - Agent Integration Guide

## Overview

The **session-state** skill manages persistent student state across learning sessions, enabling personalized, adaptive teaching that remembers student preferences, tracks learning history, awards achievements, and records what teaching strategies work best for each student.

**Key Capabilities:**
- Student profile management with learning preferences
- Session tracking for continuity across sessions
- Learning history with all-time statistics
- Achievement system with 15+ achievements
- Teaching memory for personalization
- File-based persistence (simple, portable)

---

## When to Use This Skill

### Use session-state when you need to:

1. **Welcome returning students** - Greet students personally and recall their progress
2. **Personalize teaching** - Adapt your approach based on what worked before
3. **Track achievements** - Celebrate milestones and motivate students
4. **Maintain continuity** - Remember context across sessions
5. **Learn about students** - Record what teaching strategies are effective

### Typical Use Cases:

- **learning-coordinator**: Session management, welcoming students, celebrating achievements
- **plan-generation-mentor**: Personalizing plans based on history and preferences
- **All teaching agents**: Recording effective/ineffective strategies

---

## How It Works

### State Management Flow

```
1. Student arrives → Load or create state
2. Start session → Track session context
3. During learning → Record observations
4. Complete tasks → Update history
5. End session → Check achievements, save state
6. Next session → Load state, maintain continuity
```

### Data Persistence

- **Storage**: JSON files (one per student)
- **Location**: `student_states/student_{student_id}.json`
- **Format**: Human-readable JSON
- **Auto-save**: After every state change

---

## API Reference

### Initialization

```python
from skills.session_state import StateManager

manager = StateManager()  # Uses default storage_dir
# or
manager = StateManager(storage_dir="custom_path/")
```

### Profile Management

**Create student:**
```python
state = manager.create_student(
    student_id="alex_2025",
    name="Alex",
    learning_style="visual",
    difficulty_preference="intermediate",
    preferred_pace="moderate",
    show_diagrams=True
)
```

**Get student:**
```python
state = manager.get_student("alex_2025")
if state:
    print(f"Welcome back, {state.profile.name}!")
```

**Update profile:**
```python
state = manager.update_profile(
    "alex_2025",
    learning_style="hands_on",
    preferred_pace="fast"
)
```

### Session Management

**Start session:**
```python
session = manager.start_session("alex_2025", plan_id="nav_plan_1")
```

**During session (update current session):**
```python
state = manager.get_student("alex_2025")
if state.current_session:
    state.current_session.tasks_completed.append("task-1-1")
    state.current_session.questions_asked += 1
    state.current_session.specialists_consulted.append("robotics-vision-navigator")
    manager.save_state(state)
```

**End session:**
```python
session = manager.end_session("alex_2025", session_notes="Great progress today!")
```

**Get current session:**
```python
session = manager.get_current_session("alex_2025")
```

### Learning History

**Add plan to history:**
```python
from skills.session_state import PlanHistory

plan_hist = PlanHistory(
    plan_id="nav_plan_1",
    plan_title="Navigation System",
    started_at="2025-10-01",
    completed_at="2025-10-15",
    total_tasks=20,
    completed_tasks=20,
    completion_percentage=100.0,
    average_velocity=2.5,
    total_time_weeks=2.0,
    checkpoints_passed=4,
    checkpoints_failed=0,
    struggled_with=["path planning"]
)

manager.add_plan_to_history("alex_2025", plan_hist)
```

**Get learning history:**
```python
history = manager.get_learning_history("alex_2025")
print(f"Completed plans: {history.completed_plans}")
print(f"Total tasks: {history.total_tasks_completed}")
print(f"Average velocity: {history.average_velocity_all_time}")
```

**Get recent activity:**
```python
activity = manager.get_recent_activity("alex_2025", days=7)
print(f"Last session: {activity['last_session']}")
print(f"Sessions this week: {activity['sessions_this_period']}")
print(f"Tasks completed: {activity['tasks_completed_this_period']}")
```

### Achievements

**Check for new achievements:**
```python
new_achievements = manager.check_achievements("alex_2025", analytics=None)

for achievement in new_achievements:
    print(f"🎉 Achievement Unlocked: {achievement.icon} {achievement.title}")
    print(f"   {achievement.description}")
```

**Get all achievements:**
```python
achievements = manager.get_achievements("alex_2025")
print(f"Total achievements: {len(achievements)}")
```

### Teaching Memory

**Record teaching strategy:**
```python
manager.record_teaching_strategy(
    "alex_2025",
    strategy="visual diagrams with step-by-step breakdown",
    effective=True
)
```

**Record specialist interaction:**
```python
manager.record_specialist_interaction(
    "alex_2025",
    specialist="robotics-vision-navigator",
    helpful=True
)
```

**Get teaching insights:**
```python
insights = manager.get_teaching_insights("alex_2025")

print("Effective strategies:")
for strategy in insights.effective_strategies:
    print(f"  ✅ {strategy}")

print("Learns best when:")
for condition in insights.learns_best_when:
    print(f"  💡 {condition}")

print("Favorite specialists:")
for specialist in insights.favorite_specialists:
    print(f"  ⭐ {specialist}")
```

---

## Usage Examples

### Example 1: Welcome Returning Student

```python
from skills.session_state import StateManager

def welcome_student(student_id: str):
    manager = StateManager()
    state = manager.get_student(student_id)

    if not state:
        # New student
        return "Welcome! Let's get started."

    # Returning student
    activity = manager.get_recent_activity(student_id, days=7)
    achievements = manager.get_achievements(student_id)

    message = f"Welcome back, {state.profile.name}! "

    if activity['last_session'] == "today":
        message += "Great to see you again today! "
    elif activity['last_session']:
        message += f"Last session was {activity['last_session']}. "

    if activity['sessions_this_period'] > 0:
        message += f"You've had {activity['sessions_this_period']} sessions "
        message += f"and completed {activity['tasks_completed_this_period']} tasks this week. "

    if achievements:
        recent_achievements = [a for a in achievements if a.earned_at]
        if recent_achievements:
            latest = max(recent_achievements, key=lambda a: a.earned_at)
            message += f"\n\nYour latest achievement: {latest.icon} {latest.title}"

    message += "\n\nReady to continue where we left off?"

    return message
```

### Example 2: Personalize Teaching

```python
def personalize_plan_generation(student_id: str, plan_content: str):
    manager = StateManager()
    state = manager.get_student(student_id)

    if not state:
        return plan_content  # Default plan for new students

    insights = manager.get_teaching_insights(student_id)

    # Adapt plan based on insights
    adaptations = []

    if "visual diagrams" in insights.effective_strategies:
        adaptations.append("- Including visual diagrams for each concept")

    if "small tasks" in insights.effective_strategies:
        adaptations.append("- Breaking down into smaller, incremental tasks")

    if insights.struggles_with:
        adaptations.append(
            f"- Extra practice on: {', '.join(insights.struggles_with[:3])}"
        )

    if state.profile.learning_style == "visual":
        adaptations.append("- Visual learning materials emphasized")

    if adaptations:
        personalization = "\n\n**Personalized for you:**\n"
        personalization += "\n".join(adaptations)
        plan_content += personalization

    return plan_content
```

### Example 3: Track Session and Check Achievements

```python
def complete_session_workflow(student_id: str, plan_id: str, tasks_completed: list):
    manager = StateManager()

    # Start session
    session = manager.start_session(student_id, plan_id=plan_id)

    # During session, update progress
    state = manager.get_student(student_id)
    if state.current_session:
        state.current_session.tasks_completed.extend(tasks_completed)
        state.current_session.questions_asked = 3
        manager.save_state(state)

    # End session
    session = manager.end_session(student_id, "Completed navigation tasks")

    # Check for achievements
    new_achievements = manager.check_achievements(student_id)

    # Celebrate!
    if new_achievements:
        celebration = "\n\n🎉 Achievement Unlocked!\n"
        for achievement in new_achievements:
            celebration += f"\n{achievement.icon} **{achievement.title}**\n"
            celebration += f"   {achievement.description}\n"
        return celebration

    return ""
```

### Example 4: Learning Coordinator Integration

```python
def handle_student_interaction(student_id: str, query: str):
    manager = StateManager()
    state = manager.get_student(student_id)

    # Create if new
    if not state:
        state = manager.create_student(student_id, name=extract_name(query))

    # Start session if not active
    if not state.current_session:
        manager.start_session(student_id)

    # Get teaching insights
    insights = manager.get_teaching_insights(student_id)

    # Use insights to adapt response
    response_style = "visual" if state.profile.learning_style == "visual" else "text"

    # ... generate response based on insights ...

    # Record effectiveness (would do this after student feedback)
    # manager.record_teaching_strategy(student_id, "used examples", effective=True)

    return response
```

---

## Integration with Other Skills

### With learning-plan-manager

```python
from skills.learning_plan_manager import LearningPlanManager
from skills.session_state import StateManager, PlanHistory

# When plan is completed
plan_manager = LearningPlanManager()
state_manager = StateManager()

plan = plan_manager.find_latest_plan()

# Create history entry
plan_hist = PlanHistory(
    plan_id=plan.metadata.plan_id,
    plan_title=plan.title,
    started_at=plan.metadata.created_at,
    completed_at="2025-10-19",
    total_tasks=len(plan.get_all_tasks()),
    completed_tasks=len([t for t in plan.get_all_tasks() if t.completed]),
    completion_percentage=100.0,
    average_velocity=2.5,
    total_time_weeks=2.0,
    checkpoints_passed=4,
    checkpoints_failed=0
)

state_manager.add_plan_to_history("alex_2025", plan_hist)
```

### With learning-analytics

```python
from skills.learning_analytics import LearningAnalyzer
from skills.session_state import StateManager

analyzer = LearningAnalyzer()
state_manager = StateManager()

# Analyze plan
analytics = analyzer.analyze_plan(plan)

# Check achievements (analytics provides context for some achievements)
new_achievements = state_manager.check_achievements("alex_2025", analytics)

# Record struggles
if analytics.struggle_areas:
    insights = state_manager.get_teaching_insights("alex_2025")
    # Update struggles based on analytics
```

---

## Best Practices

### 1. Always Load State First

```python
# ✅ Good
state = manager.get_student(student_id)
if state:
    # Use state
else:
    # Create new student

# ❌ Bad
state = manager.create_student(student_id)  # Fails if exists
```

### 2. Start/End Sessions Consistently

```python
# ✅ Good
session = manager.start_session(student_id)
# ... interaction ...
manager.end_session(student_id, "Session notes")

# ❌ Bad
# Forgetting to end session before starting new one
```

### 3. Check Achievements at Natural Points

```python
# ✅ Good - Check at session end
manager.end_session(student_id)
new_achievements = manager.check_achievements(student_id)

# ✅ Good - Check after major milestone
manager.add_plan_to_history(student_id, plan_hist)
new_achievements = manager.check_achievements(student_id)

# ❌ Bad - Checking too frequently
# Every single action
```

### 4. Record Teaching Memory Thoughtfully

```python
# ✅ Good - Specific, actionable insights
manager.record_teaching_strategy(
    student_id,
    "visual diagram showing ROS node connections",
    effective=True
)

# ❌ Bad - Too vague
manager.record_teaching_strategy(
    student_id,
    "explained things",
    effective=True
)
```

### 5. Use Teaching Insights to Personalize

```python
# ✅ Good
insights = manager.get_teaching_insights(student_id)
if "visual diagrams" in insights.effective_strategies:
    # Include diagrams in response
    pass

# ❌ Bad - Ignoring insights
# Just using default approach every time
```

---

## Achievement List

### Milestone (5)
- 🎯 **First Task Complete** - Complete 1 task
- ✅ **First Checkpoint Passed** - Pass 1 checkpoint
- 🎓 **First Plan Complete** - Complete 1 plan
- 🌟 **Five Plans Complete** - Complete 5 plans
- 💎 **Ten Plans Complete** - Complete 10 plans

### Streak (3)
- 🔥 **3-Day Streak** - Learn 3 consecutive days
- 🔥🔥 **7-Day Streak** - Learn 7 consecutive days
- 🔥🔥🔥 **30-Day Streak** - Learn 30 consecutive days

### Speed (3)
- ⚡ **Speed Learner** - Complete 5 tasks in 1 day
- ⚡⚡ **Lightning Fast** - Complete plan in 50% of time
- ⚡⚡⚡ **Task Machine** - Complete 10 tasks in 1 session

### Mastery (2)
- 💯 **Perfect Score** - Pass all checkpoints without fails
- 🌟 **No Struggles** - Complete plan with 0 struggles

### Persistence (2)
- 💪 **Comeback Kid** - Complete task after 10+ days struggle
- 💪💪 **Never Give Up** - Complete plan with 3+ severe struggles

---

## Output Format

The skill works programmatically (no text output). Agents should format results for users.

**Example formatted output:**

```markdown
## Your Learning Profile

**Name:** Alex
**Learning Style:** Visual
**Preferred Pace:** Moderate

**Recent Activity (Last 7 Days):**
- Sessions: 3
- Tasks completed: 7
- Time spent: 3 hours

**All-Time Stats:**
- Plans completed: 2
- Total tasks: 45
- Checkpoints passed: 8

**Achievements (5):**
🎯 First Task Complete
🎓 First Plan Complete
🔥 3-Day Streak
⚡ Speed Learner
💯 Perfect Score
```

---

## Error Handling

```python
try:
    state = manager.get_student(student_id)
    if not state:
        state = manager.create_student(student_id)
except ValueError as e:
    # Handle error (e.g., student already exists)
    print(f"Error: {e}")
```

---

*For detailed technical documentation, see README.md*

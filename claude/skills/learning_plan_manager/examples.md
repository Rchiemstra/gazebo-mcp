# Learning Plan Manager - Usage Examples

Real-world examples demonstrating how to use learning_plan_manager effectively in teaching workflows.

---

## Example 1: Quick Progress Check

**Scenario:** Check where a student is in their learning journey.

```python
from skills.learning_plan_manager.operations import find_latest_plan, load_plan

# Find student's current plan
latest = find_latest_plan("plans/alice/")

if latest.success:
    print(f"Found plan: {latest.data['plan_name']}")

    # Get current status (most token-efficient format)
    status = load_plan(
        latest.data['file_path'],
        response_format="progress"
    )

    print(f"\nCurrent Status:")
    print(f"  Phase: {status.data['current_phase']['name']}")
    print(f"  Progress: {status.data['overall_progress']}%")
    print(f"  Next task: {status.data['next_task']['description']}")

    # Determine next teaching action
    if status.data['overall_progress'] < 25:
        print("\n→ Action: Provide foundational context")
    elif status.data['overall_progress'] < 75:
        print("\n→ Action: Guide through current task")
    else:
        print("\n→ Action: Prepare final assessment")
```

**Output:**
```
Found plan: Autonomous Navigation Learning Journey

Current Status:
  Phase: Research & Learning
  Progress: 33.3%
  Next task: Study ROS2 navigation stack documentation

→ Action: Guide through current task
```

---

## Example 2: Resume Learning Session

**Scenario:** Start a learning session where the student left off.

```python
from skills.learning_plan_manager.operations import load_plan, find_latest_plan

# Find where student left off
plan_ref = find_latest_plan("plans/")

# Get overview first
overview = load_plan(plan_ref.data['file_path'], response_format="summary")

print("=" * 60)
print(f"Welcome back! Resuming: {overview.data['topic']}")
print("=" * 60)

print(f"\nOverall Progress: {overview.data['overall_progress']}%")
print(f"Current Phase: {overview.data['current_phase']['name']}")

# If early in journey, provide context
if overview.data['overall_progress'] < 25:
    print("\nYou're in the early stages. Let me provide some context...")

    # Get full plan for context
    full_plan = load_plan(
        plan_ref.data['file_path'],
        response_format="detailed"
    )

    print(f"\nYour learning journey has {len(full_plan.data['phases'])} phases:")
    for phase in full_plan.data['phases']:
        status_icon = "✓" if phase['status'] == 'completed' else "→" if phase['status'] == 'in_progress' else " "
        print(f"  [{status_icon}] Phase {phase['phase_number']}: {phase['name']}")

# Otherwise, jump right into current task
else:
    print(f"\nLet's continue with your next task:")
    print(f"  {overview.data['next_task']['description']}")
    print(f"\nReady to begin?")
```

**Output:**
```
============================================================
Welcome back! Resuming: autonomous navigation
============================================================

Overall Progress: 33.3%
Current Phase: Research & Learning

Let's continue with your next task:
  Study ROS2 navigation stack documentation

Ready to begin?
```

---

## Example 3: Managing Multiple Students

**Scenario:** Teaching coordinator checking multiple students' progress.

```python
from skills.learning_plan_manager.operations import list_plans, load_plan

# Get all plans
plans = list_plans("plans/", response_format="summary")

print(f"Managing {plans.data['total_plans']} students:")
print("=" * 60)

# Check each student's progress
students_progress = []

for plan_ref in plans.data['plans']:
    # Load progress for each
    status = load_plan(plan_ref['file_path'], response_format="progress")

    students_progress.append({
        'topic': plan_ref['topic'],
        'progress': status.data['overall_progress'],
        'current_phase': status.data['current_phase']['name'],
        'file': plan_ref['file_path']
    })

# Sort by progress (identify struggling students)
students_progress.sort(key=lambda x: x['progress'])

print("\nStudents needing attention (lowest progress first):")
for student in students_progress[:3]:
    print(f"\n  {student['topic']}")
    print(f"    Progress: {student['progress']}%")
    print(f"    Phase: {student['current_phase']}")

print("\n" + "=" * 60)
print("Focus on helping students with lowest progress first!")
```

**Output:**
```
Managing 5 students:
============================================================

Students needing attention (lowest progress first):

  database optimization
    Progress: 15.0%
    Phase: Setup & Prerequisites

  python testing
    Progress: 25.5%
    Phase: Unit Testing Basics

  autonomous navigation
    Progress: 33.3%
    Phase: Research & Learning

============================================================
Focus on helping students with lowest progress first!
```

---

## Example 4: Progressive Detail Loading

**Scenario:** Load plan details progressively based on need.

```python
from skills.learning_plan_manager.operations import load_plan

plan_file = "plans/navigation-plan.md"

# Step 1: Get high-level status (200 tokens)
print("Step 1: Checking status...")
status = load_plan(plan_file, response_format="progress")

print(f"Progress: {status.data['overall_progress']}%")
print(f"Completed: {status.data['completed_tasks']}/{status.data['total_tasks']} tasks")

# Step 2: Decide if more detail is needed
if status.data['overall_progress'] < 50:
    print("\nStep 2: Loading full plan for context (early stage)...")

    # Get full plan
    full_plan = load_plan(plan_file, response_format="detailed")

    # Show all phases
    print("\nLearning Journey Roadmap:")
    for phase in full_plan.data['phases']:
        print(f"  Phase {phase['phase_number']}: {phase['name']}")
        print(f"    Goal: {phase['goal']}")
        print(f"    Status: {phase['status']} ({phase['progress']}%)")

        # Show tasks for current phase
        if phase['status'] == 'in_progress':
            print(f"    Tasks:")
            for task in phase['tasks']:
                status_icon = "✓" if task['status'] == 'completed' else "→"
                print(f"      [{status_icon}] {task['description']}")

else:
    print("\nStep 2: Well along in journey, focusing on current task...")
    print(f"  {status.data['next_task']['description']}")

print(f"\nTotal tokens used: ~{200 if status.data['overall_progress'] >= 50 else 2500}")
```

**Output (Early Stage):**
```
Step 1: Checking status...
Progress: 25.0%
Completed: 5/20 tasks

Step 2: Loading full plan for context (early stage)...

Learning Journey Roadmap:
  Phase 1: Setup & Prerequisites
    Goal: Set up development environment
    Status: completed (100.0%)

  Phase 2: Research & Learning
    Goal: Understand navigation concepts
    Status: in_progress (50.0%)
    Tasks:
      [✓] Read navigation overview
      [✓] Watch navigation tutorials
      [→] Study ROS2 navigation stack

  Phase 3: Basic Implementation
    Goal: Implement simple navigation
    Status: pending (0.0%)

  ...

Total tokens used: ~2500
```

---

## Example 5: Integration with Learning Analytics

**Scenario:** Analyze student's learning velocity and adjust teaching.

```python
from skills.learning_plan_manager.operations import load_plan
from skills.learning_analytics import analyze_progress

# Load full plan for analytics
plan = load_plan("plans/navigation-plan.md", response_format="detailed")

if plan.success:
    # Analyze progress patterns
    analytics = analyze_progress(plan.data)

    print("Learning Analytics:")
    print("=" * 60)
    print(f"Velocity: {analytics.data['velocity']:.2f} tasks/day")
    print(f"Consistency: {analytics.data['consistency']:.1%}")

    # Check for struggles
    if analytics.data['struggling_areas']:
        print(f"\nStruggling with:")
        for area in analytics.data['struggling_areas']:
            print(f"  - {area['phase']}: {area['reason']}")

    # Get recommendations
    print(f"\nRecommendations:")
    for rec in analytics.data['recommendations']:
        print(f"  • {rec}")

    # Adjust teaching approach
    if analytics.data['velocity'] < 0.5:
        print("\n→ Action: Slow down, provide more support")
    elif analytics.data['velocity'] > 2.0:
        print("\n→ Action: Student is excelling, add challenges")
    else:
        print("\n→ Action: Current pace is good, maintain approach")
```

**Output:**
```
Learning Analytics:
============================================================
Velocity: 0.8 tasks/day
Consistency: 75.0%

Struggling with:
  - Research & Learning: Taking longer than expected

Recommendations:
  • Break down complex tasks into smaller steps
  • Provide more examples and guided practice
  • Schedule check-in to address confusion

→ Action: Current pace is good, maintain approach
```

---

## Example 6: Finding Specific Plan

**Scenario:** Find a specific plan by topic or student.

```python
from skills.learning_plan_manager.operations import list_plans, load_plan

# List all available plans
all_plans = list_plans("plans/")

print(f"Available learning plans ({all_plans.data['total_plans']}):")
print("=" * 60)

# Search for specific topic
search_topic = "navigation"

matching_plans = [
    p for p in all_plans.data['plans']
    if search_topic.lower() in p['topic'].lower()
]

if matching_plans:
    print(f"\nFound {len(matching_plans)} plan(s) matching '{search_topic}':")

    for plan_ref in matching_plans:
        # Get progress for each matching plan
        status = load_plan(plan_ref['file_path'], response_format="progress")

        print(f"\n  {plan_ref['name']}")
        print(f"    File: {plan_ref['file_path']}")
        print(f"    Progress: {status.data['overall_progress']}%")
        print(f"    Current: {status.data['current_phase']['name']}")
else:
    print(f"\nNo plans found matching '{search_topic}'")
```

**Output:**
```
Available learning plans (5):
============================================================

Found 2 plan(s) matching 'navigation':

  Autonomous Navigation Learning Journey
    File: plans/navigation-plan.md
    Progress: 33.3%
    Current: Research & Learning

  Advanced Navigation Techniques
    File: plans/advanced-navigation-plan.md
    Progress: 10.0%
    Current: Setup & Prerequisites
```

---

## Example 7: Token-Efficient Status Dashboard

**Scenario:** Create a dashboard showing all students without excessive tokens.

```python
from skills.learning_plan_manager.operations import list_plans, load_plan

# Get all plans (summary format - minimal tokens)
plans = list_plans("plans/", response_format="summary")

print("Student Learning Dashboard")
print("=" * 60)

# For each plan, get just progress status
for plan_ref in plans.data['plans']:
    # Use progress format for token efficiency
    status = load_plan(plan_ref['file_path'], response_format="progress")

    # Show one-line status
    progress_bar = "█" * int(status.data['overall_progress'] / 10)
    progress_bar += "░" * (10 - int(status.data['overall_progress'] / 10))

    print(f"{plan_ref['topic'][:30]:30} [{progress_bar}] {status.data['overall_progress']:5.1f}%")

print("=" * 60)
print(f"Total students: {plans.data['total_plans']}")
print(f"Tokens used: ~{200 + plans.data['total_plans'] * 250} (very efficient!)")
```

**Output:**
```
Student Learning Dashboard
============================================================
autonomous navigation          [███░░░░░░░]  33.3%
python testing                 [██░░░░░░░░]  25.5%
database optimization          [█░░░░░░░░░]  15.0%
ros2 fundamentals              [█████░░░░░]  50.0%
web development                [███████░░░]  75.0%
============================================================
Total students: 5
Tokens used: ~1450 (very efficient!)
```

---

## Example 8: Error Handling & Recovery

**Scenario:** Robust plan loading with fallbacks.

```python
from skills.learning_plan_manager.operations import (
    load_plan,
    find_latest_plan,
    list_plans
)

def load_student_plan(student_dir):
    """
    Robustly load student's learning plan with fallbacks.
    """
    # Try finding latest plan
    result = find_latest_plan(student_dir)

    if not result.success:
        print(f"Error: {result.error}")

        # Try listing plans as fallback
        plans = list_plans(student_dir)

        if plans.success and plans.data['total_plans'] > 0:
            print(f"Found {plans.data['total_plans']} plans, using first one")
            result = load_plan(plans.data['plans'][0]['file_path'])
        else:
            print("No plans found. Creating new plan needed.")
            print(f"Suggestions:")
            for suggestion in result.suggestions:
                print(f"  - {suggestion}")
            return None

    # Load the plan with error handling
    plan = load_plan(result.data['file_path'], response_format="progress")

    if not plan.success:
        print(f"Error loading plan: {plan.error}")
        print(f"Error code: {plan.error_code}")

        # Show fix suggestion
        if plan.example_fix:
            print(f"Try: {plan.example_fix}")
        return None

    return plan

# Use it
plan = load_student_plan("plans/alice/")

if plan:
    print(f"\n✓ Successfully loaded plan")
    print(f"  Progress: {plan.data['overall_progress']}%")
    print(f"  Next task: {plan.data['next_task']['description']}")
else:
    print("\n✗ Could not load plan - manual intervention needed")
```

---

## Example 9: Batch Processing

**Scenario:** Process all plans to generate summary report.

```python
from skills.learning_plan_manager.operations import list_plans, load_plan

# Get all plans
all_plans = list_plans("plans/")

print("Learning Progress Report")
print("=" * 60)

# Track statistics
total_progress = 0
phase_distribution = {}
struggling_students = []

for plan_ref in all_plans.data['plans']:
    # Get progress for each plan (token-efficient)
    status = load_plan(plan_ref['file_path'], response_format="progress")

    total_progress += status.data['overall_progress']

    # Track phase distribution
    phase = status.data['current_phase']['name']
    phase_distribution[phase] = phase_distribution.get(phase, 0) + 1

    # Identify struggling students
    if status.data['overall_progress'] < 30:
        struggling_students.append({
            'topic': plan_ref['topic'],
            'progress': status.data['overall_progress']
        })

# Generate report
print(f"\nTotal Students: {all_plans.data['total_plans']}")
print(f"Average Progress: {total_progress / all_plans.data['total_plans']:.1f}%")

print(f"\nPhase Distribution:")
for phase, count in sorted(phase_distribution.items(), key=lambda x: x[1], reverse=True):
    print(f"  {phase}: {count} students")

if struggling_students:
    print(f"\nStudents Needing Attention ({len(struggling_students)}):")
    for student in struggling_students:
        print(f"  - {student['topic']} ({student['progress']:.1f}%)")

print("\n" + "=" * 60)
```

**Output:**
```
Learning Progress Report
============================================================

Total Students: 5
Average Progress: 39.8%

Phase Distribution:
  Research & Learning: 2 students
  Setup & Prerequisites: 2 students
  Implementation: 1 students

Students Needing Attention (2):
  - database optimization (15.0%)
  - python testing (25.5%)

============================================================
```

---

## Common Patterns

### Pattern: Summary → Progress → Detailed

```python
# Always start with find or list (summary)
latest = find_latest_plan()

# Get current status (progress - most efficient)
status = load_plan(latest.data['file_path'], response_format="progress")

# Only get details when needed
if status.data['overall_progress'] < 25:
    # Early stage - need context
    full = load_plan(latest.data['file_path'], response_format="detailed")
```

### Pattern: Error-Resilient Loading

```python
result = load_plan("plan.md")

if not result.success:
    # Use suggestions to recover
    for suggestion in result.suggestions:
        print(f"  - {suggestion}")

    # Try alternative
    latest = find_latest_plan()
    if latest.success:
        result = load_plan(latest.data['file_path'])
```

### Pattern: Batch with Token Efficiency

```python
# Get overview first (minimal tokens)
plans = list_plans()

# Process each with progress format
for plan in plans.data['plans']:
    status = load_plan(plan['file_path'], response_format="progress")
    # Work with status (200-300 tokens per plan)

# Total: ~200 + (300 * N) tokens
# vs. 5000 * N for detailed format (95% savings!)
```

---

## Next Steps

- Review **reference.md** for complete API documentation
- Try these examples with sample plans in `plans/` directory
- Combine with **learning_analytics** for deeper insights
- Use with **session_state** for student tracking

---

*Last Updated: 2025-11-08*

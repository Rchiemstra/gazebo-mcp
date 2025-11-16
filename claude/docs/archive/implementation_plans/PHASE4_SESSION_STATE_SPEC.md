# Phase 4: session-state Skill - Technical Specification

**Purpose**: Manage cross-session student state including learning history, preferences, achievements, and personalized teaching memory to enable persistent, adaptive learning experiences.

**Created**: 2025-10-19
**Version**: 1.0
**Status**: Technical Specification

---

## Table of Contents

1. [Overview](#overview)
2. [Dependencies](#dependencies)
3. [Data Models](#data-models)
4. [Core Functionality](#core-functionality)
5. [Persistence Strategy](#persistence-strategy)
6. [API Design](#api-design)
7. [Implementation Approach](#implementation-approach)
8. [Testing Strategy](#testing-strategy)
9. [Integration with Agents](#integration-with-agents)
10. [Performance Considerations](#performance-considerations)

---

## Overview

### Purpose

The session-state skill provides persistent student state across learning sessions:
- Student profiles with learning preferences
- Learning history and achievements
- Session tracking and continuity
- Personalized teaching memory
- Progress over time

### Use Cases

1. **Learning Coordinator**: Greet returning students, recall previous sessions
2. **Plan Generation Mentor**: Personalize plans based on student history
3. **Analytics**: Long-term trends across multiple plans
4. **Achievements**: Track milestones and celebrate progress
5. **Preferences**: Remember student's preferred learning style

### Key Features

- **Student Profiles**: Name, learning style, preferences
- **Session Management**: Track sessions over time
- **Learning History**: All plans, tasks completed, time spent
- **Achievements**: Milestones unlocked, badges earned
- **Teaching Memory**: What worked, what didn't
- **Preferences**: Pace, difficulty, preferred specialists
- **Persistence**: JSON file-based storage (simple, portable)

---

## Dependencies

### Required Skills

**learning-plan-manager** (Phase 1) ✅
- Provides plan data to store in history

**learning-analytics** (Phase 2) ✅
- Provides analytics to track over time

**interactive-diagram** (Phase 3) ✅ (optional)
- Can visualize learning history

### Python Libraries

```python
# Standard library only
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from pathlib import Path
import json
from pydantic import BaseModel, Field
```

**No new dependencies!**

---

## Data Models

### 1. StudentProfile

Core student information.

```python
class LearningStyle(str, Enum):
    """Student's preferred learning style"""
    VISUAL = "visual"
    HANDS_ON = "hands_on"
    READING = "reading"
    LISTENING = "listening"
    MIXED = "mixed"


class DifficultyPreference(str, Enum):
    """Preferred difficulty level"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    ADAPTIVE = "adaptive"  # Adjust based on performance


class StudentProfile(BaseModel):
    """Student profile and preferences"""

    student_id: str = Field(description="Unique student identifier")
    name: Optional[str] = None
    email: Optional[str] = None

    # Preferences
    learning_style: LearningStyle = Field(default=LearningStyle.MIXED)
    difficulty_preference: DifficultyPreference = Field(
        default=DifficultyPreference.ADAPTIVE
    )
    preferred_pace: str = Field(
        default="moderate",
        description="slow, moderate, fast"
    )
    preferred_specialists: List[str] = Field(
        default_factory=list,
        description="Specialist agents student prefers"
    )

    # Settings
    show_diagrams: bool = Field(default=True)
    enable_celebrations: bool = Field(default=True)
    reminder_frequency: str = Field(default="weekly")

    # Metadata
    created_at: str = Field(
        default_factory=lambda: datetime.now().isoformat()
    )
    last_active: str = Field(
        default_factory=lambda: datetime.now().isoformat()
    )
```

### 2. Session

Individual learning session tracking.

```python
class Session(BaseModel):
    """Individual learning session"""

    session_id: str
    student_id: str

    start_time: str
    end_time: Optional[str] = None
    duration_minutes: Optional[int] = None

    # Session context
    plan_id: Optional[str] = None
    phase_number: Optional[int] = None
    tasks_completed: List[str] = Field(default_factory=list)

    # Interaction
    questions_asked: int = Field(default=0)
    specialists_consulted: List[str] = Field(default_factory=list)
    struggles_encountered: List[str] = Field(default_factory=list)

    # Notes
    session_notes: str = Field(default="")
    agent_observations: List[str] = Field(default_factory=list)
```

### 3. LearningHistory

Historical learning data.

```python
class PlanHistory(BaseModel):
    """History of a completed or in-progress plan"""

    plan_id: str
    plan_title: str
    started_at: str
    completed_at: Optional[str] = None

    total_tasks: int
    completed_tasks: int
    completion_percentage: float

    # Performance
    average_velocity: float  # tasks per week
    total_time_weeks: float
    checkpoints_passed: int
    checkpoints_failed: int

    # Struggles
    struggled_with: List[str] = Field(
        default_factory=list,
        description="Task titles student struggled with"
    )


class LearningHistory(BaseModel):
    """Complete learning history"""

    student_id: str

    # Plans
    plans: List[PlanHistory] = Field(default_factory=list)
    total_plans: int = Field(default=0)
    completed_plans: int = Field(default=0)

    # Overall stats
    total_tasks_completed: int = Field(default=0)
    total_checkpoints_passed: int = Field(default=0)
    total_learning_time_hours: float = Field(default=0.0)

    # Trends
    average_velocity_all_time: float = Field(default=0.0)
    most_struggled_topics: List[str] = Field(default_factory=list)
    favorite_specialists: List[str] = Field(default_factory=list)
```

### 4. Achievement

Gamification and motivation.

```python
class AchievementType(str, Enum):
    """Types of achievements"""
    MILESTONE = "milestone"
    STREAK = "streak"
    MASTERY = "mastery"
    SPEED = "speed"
    PERSISTENCE = "persistence"


class Achievement(BaseModel):
    """Achievement/badge earned"""

    achievement_id: str
    type: AchievementType
    title: str
    description: str

    earned_at: str
    criteria: str  # How it was earned

    # Visual
    icon: str = Field(default="🏆")
    rarity: str = Field(default="common")  # common, rare, epic, legendary
```

### 5. TeachingMemory

Agent memory of what works for this student.

```python
class TeachingMemory(BaseModel):
    """What agents learned about teaching this student"""

    student_id: str

    # What works
    effective_strategies: List[str] = Field(
        default_factory=list,
        description="Teaching strategies that worked"
    )

    # What doesn't work
    ineffective_strategies: List[str] = Field(
        default_factory=list,
        description="Strategies that didn't help"
    )

    # Patterns
    learns_best_when: List[str] = Field(
        default_factory=list,
        description="Conditions when student learns best"
    )

    struggles_with: List[str] = Field(
        default_factory=list,
        description="Types of concepts student struggles with"
    )

    # Specialist effectiveness
    specialist_effectiveness: Dict[str, float] = Field(
        default_factory=dict,
        description="How helpful each specialist was (0-1)"
    )

    # Notes
    agent_notes: List[str] = Field(
        default_factory=list,
        description="Agent observations about student"
    )
```

### 6. StudentState

Main state object combining all data.

```python
class StudentState(BaseModel):
    """Complete student state"""

    # Core
    profile: StudentProfile
    sessions: List[Session] = Field(default_factory=list)
    history: LearningHistory
    achievements: List[Achievement] = Field(default_factory=list)
    teaching_memory: TeachingMemory

    # Current session
    current_session: Optional[Session] = None

    # Metadata
    state_version: str = Field(default="1.0")
    last_updated: str = Field(
        default_factory=lambda: datetime.now().isoformat()
    )
```

---

## Core Functionality

### StateManager Class

Main class for managing student state.

```python
class StateManager:
    """Manages student state and persistence"""

    def __init__(self, storage_dir: str = "student_states/"):
        """Initialize state manager"""
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)

    # ===== Profile Management =====

    def create_student(
        self,
        student_id: str,
        name: Optional[str] = None,
        **preferences
    ) -> StudentState:
        """Create new student state"""

    def get_student(self, student_id: str) -> Optional[StudentState]:
        """Load student state"""

    def update_profile(
        self,
        student_id: str,
        **updates
    ) -> StudentState:
        """Update student profile"""

    # ===== Session Management =====

    def start_session(
        self,
        student_id: str,
        plan_id: Optional[str] = None
    ) -> Session:
        """Start new learning session"""

    def end_session(
        self,
        student_id: str,
        session_notes: str = ""
    ) -> Session:
        """End current session"""

    def get_current_session(
        self,
        student_id: str
    ) -> Optional[Session]:
        """Get current active session"""

    # ===== Learning History =====

    def add_plan_to_history(
        self,
        student_id: str,
        plan_history: PlanHistory
    ):
        """Add completed/in-progress plan to history"""

    def get_learning_history(
        self,
        student_id: str
    ) -> LearningHistory:
        """Get complete learning history"""

    def get_recent_activity(
        self,
        student_id: str,
        days: int = 7
    ) -> Dict[str, Any]:
        """Get recent activity summary"""

    # ===== Achievements =====

    def award_achievement(
        self,
        student_id: str,
        achievement: Achievement
    ):
        """Award achievement to student"""

    def check_achievements(
        self,
        student_id: str,
        analytics: Any
    ) -> List[Achievement]:
        """Check if student earned new achievements"""

    def get_achievements(
        self,
        student_id: str
    ) -> List[Achievement]:
        """Get all student achievements"""

    # ===== Teaching Memory =====

    def record_teaching_strategy(
        self,
        student_id: str,
        strategy: str,
        effective: bool
    ):
        """Record whether a teaching strategy worked"""

    def record_specialist_interaction(
        self,
        student_id: str,
        specialist: str,
        helpful: bool
    ):
        """Record specialist interaction effectiveness"""

    def get_teaching_insights(
        self,
        student_id: str
    ) -> TeachingMemory:
        """Get teaching insights for this student"""

    # ===== Persistence =====

    def save_state(self, student_state: StudentState):
        """Save student state to file"""

    def load_state(self, student_id: str) -> Optional[StudentState]:
        """Load student state from file"""

    def list_students(self) -> List[str]:
        """List all student IDs"""
```

---

## Persistence Strategy

### File-Based Storage

**Format**: JSON files (one per student)

**Directory Structure**:
```
student_states/
├── student_12345.json
├── student_67890.json
└── ...
```

**Advantages**:
- Simple, no database needed
- Human-readable
- Version control friendly
- Easy backup
- Portable

**File Format**:
```json
{
  "profile": {
    "student_id": "12345",
    "name": "Alex",
    "learning_style": "visual",
    ...
  },
  "sessions": [...],
  "history": {...},
  "achievements": [...],
  "teaching_memory": {...}
}
```

### Optimization

- **Lazy loading**: Load state only when needed
- **Incremental saves**: Save after changes
- **Compression**: Optional gzip for large histories
- **Caching**: In-memory cache of active students

---

## API Design

### Example Usage

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

# During session, update
session.tasks_completed.append("task-1-1")
session.questions_asked += 1

# End session
manager.end_session("alex_2025", "Great progress today!")

# Add to history
from skills.session_state import PlanHistory
history_entry = PlanHistory(
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
    checkpoints_failed=0
)
manager.add_plan_to_history("alex_2025", history_entry)

# Check achievements
from skills.learning_analytics import LearningAnalyzer
analyzer = LearningAnalyzer()
analytics = analyzer.analyze_plan(plan)
new_achievements = manager.check_achievements("alex_2025", analytics)

# Get teaching insights
insights = manager.get_teaching_insights("alex_2025")
print(f"Effective strategies: {insights.effective_strategies}")
```

---

## Implementation Approach

### Phase A: Core Models (30 min)

**Implement**:
- StudentProfile
- Session
- LearningHistory
- Achievement
- TeachingMemory
- StudentState

**File**: `skills/session_state/models.py`

### Phase B: State Manager (60 min)

**Implement**:
- StateManager class
- Profile management methods
- Session management methods
- History methods
- Persistence (save/load)

**File**: `skills/session_state/state_manager.py`

### Phase C: Achievement System (30 min)

**Implement**:
- Achievement definitions
- Achievement checking logic
- Badge awarding

**File**: `skills/session_state/achievements.py`

### Phase D: Documentation & Testing (40 min)

**Implement**:
- skill.md
- README.md
- Comprehensive tests
- Integration examples

---

## Testing Strategy

### Unit Tests

**File**: `examples/test_session_state.py`

**Tests** (8-10 tests):
1. Test create student
2. Test start/end session
3. Test learning history
4. Test achievements
5. Test teaching memory
6. Test persistence (save/load)
7. Test state updates
8. Test recent activity
9. Test teaching insights
10. Test list students

### Integration Tests

- Test with real learning plans
- Test cross-session continuity
- Test achievement unlocking with real analytics

---

## Integration with Agents

### learning-coordinator

**Welcome returning students:**

```markdown
Skill(session-state) with query:
"Get student alex_2025 and check recent activity"

Returns:
{
  "profile": {"name": "Alex", "learning_style": "visual"},
  "recent_activity": {
    "last_session": "2 days ago",
    "sessions_this_week": 3,
    "tasks_completed_this_week": 7
  },
  "achievements": ["First Plan Complete!", "7-Day Streak"]
}

Agent response:
"Welcome back, Alex! Great to see you again. I see you've been very active
this week with 3 sessions and 7 tasks completed. You're on a 7-day streak! 🔥

Ready to continue where we left off?"
```

---

### plan-generation-mentor

**Personalize plans:**

```markdown
Skill(session-state) with query:
"Get teaching insights for alex_2025"

Returns:
{
  "effective_strategies": ["visual diagrams", "small incremental tasks"],
  "struggles_with": ["complex algorithms", "abstract concepts"],
  "learns_best_when": ["concepts shown visually", "hands-on practice"]
}

Agent uses insights:
"Based on your learning history, I'll create this plan with:
- Visual diagrams for each concept (you learn best visually)
- Smaller, incremental tasks (this has worked well for you)
- Extra practice on algorithm sections (I know these can be tricky)"
```

---

## Performance Considerations

### File I/O

- Load state: ~10-50ms (depends on file size)
- Save state: ~10-50ms
- Acceptable for learning context (not real-time)

### Memory

- StudentState: ~50-200KB per student
- Can cache 100+ students in memory
- Lazy load when needed

### Scalability

- **< 100 students**: File-based perfect
- **100-1000 students**: Still fine, consider indexing
- **1000+ students**: Consider database migration

---

## Achievement Definitions

### Milestone Achievements

- **First Task Complete** - Complete your first task
- **First Checkpoint Passed** - Pass your first checkpoint
- **First Plan Complete** - Finish your first learning plan
- **10 Plans Complete** - Complete 10 learning plans

### Streak Achievements

- **3-Day Streak** - Learn 3 days in a row
- **7-Day Streak** - Learn 7 days in a row
- **30-Day Streak** - Learn 30 days in a row

### Speed Achievements

- **Speed Learner** - Complete 5 tasks in one day
- **Lightning Fast** - Complete a plan in half estimated time

### Mastery Achievements

- **Perfect Score** - Pass all checkpoints on first try
- **No Struggles** - Complete plan with no struggle areas

### Persistence Achievements

- **Comeback Kid** - Complete a task after struggling 10+ days
- **Never Give Up** - Complete a plan despite 3+ severe struggles

---

## Summary

The session-state skill provides:

✅ **Persistent student profiles** across sessions
✅ **Learning history** tracking over time
✅ **Session management** for continuity
✅ **Achievement system** for motivation
✅ **Teaching memory** for personalization
✅ **Simple file-based storage** (no database)

**Complexity**: Medium - state management with persistence

**Value**: High - enables personalized, adaptive teaching over time

---

*Technical Specification End*

"""
Data models for session-state skill.

Defines student state, learning history, achievements, and teaching memory.
"""

from datetime import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum


# ============================================================================
# Enums
# ============================================================================

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


class AchievementType(str, Enum):
    """Types of achievements"""
    MILESTONE = "milestone"
    STREAK = "streak"
    MASTERY = "mastery"
    SPEED = "speed"
    PERSISTENCE = "persistence"


# ============================================================================
# Student Profile
# ============================================================================

class StudentProfile(BaseModel):
    """Student profile and preferences"""

    student_id: str = Field(description="Unique student identifier")
    name: Optional[str] = None
    email: Optional[str] = None

    # Learning Preferences
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


# ============================================================================
# Session Tracking
# ============================================================================

class Session(BaseModel):
    """Individual learning session"""

    session_id: str
    student_id: str

    start_time: str
    end_time: Optional[str] = None
    duration_minutes: Optional[int] = None

    # Session Context
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


# ============================================================================
# Learning History
# ============================================================================

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

    # Overall Stats
    total_tasks_completed: int = Field(default=0)
    total_checkpoints_passed: int = Field(default=0)
    total_learning_time_hours: float = Field(default=0.0)

    # Trends
    average_velocity_all_time: float = Field(default=0.0)
    most_struggled_topics: List[str] = Field(default_factory=list)
    favorite_specialists: List[str] = Field(default_factory=list)


# ============================================================================
# Achievements
# ============================================================================

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


# ============================================================================
# Teaching Memory
# ============================================================================

class TeachingMemory(BaseModel):
    """What agents learned about teaching this student"""

    student_id: str

    # What Works
    effective_strategies: List[str] = Field(
        default_factory=list,
        description="Teaching strategies that worked"
    )

    # What Doesn't Work
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

    # Specialist Effectiveness
    specialist_effectiveness: Dict[str, float] = Field(
        default_factory=dict,
        description="How helpful each specialist was (0-1)"
    )

    # Notes
    agent_notes: List[str] = Field(
        default_factory=list,
        description="Agent observations about student"
    )


# ============================================================================
# Main State
# ============================================================================

class StudentState(BaseModel):
    """Complete student state"""

    # Core Components
    profile: StudentProfile
    sessions: List[Session] = Field(default_factory=list)
    history: LearningHistory
    achievements: List[Achievement] = Field(default_factory=list)
    teaching_memory: TeachingMemory

    # Current Session
    current_session: Optional[Session] = None

    # Metadata
    state_version: str = Field(default="1.0")
    last_updated: str = Field(
        default_factory=lambda: datetime.now().isoformat()
    )

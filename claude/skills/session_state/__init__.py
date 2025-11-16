"""
session-state skill - Persistent student state management.

Manages cross-session student state including learning history, preferences,
achievements, and personalized teaching memory.

Example:
    from skills.session_state import StateManager

    manager = StateManager()

    # Create student
    state = manager.create_student(
        "alex_2025",
        name="Alex",
        learning_style="visual"
    )

    # Start session
    session = manager.start_session("alex_2025", plan_id="nav_1")

    # End session
    manager.end_session("alex_2025", "Great progress!")

    # Check achievements
    new_achievements = manager.check_achievements("alex_2025")
"""

from .models import (
    # Enums
    LearningStyle,
    DifficultyPreference,
    AchievementType,

    # Models
    StudentProfile,
    Session,
    PlanHistory,
    LearningHistory,
    Achievement,
    TeachingMemory,
    StudentState,
)

from .state_manager import StateManager

from .achievements import (
    ACHIEVEMENTS,
    check_all_achievements,
    check_milestone_achievements,
    check_streak_achievements,
    check_speed_achievements,
    check_mastery_achievements,
    check_persistence_achievements,
)

__all__ = [
    # Enums
    "LearningStyle",
    "DifficultyPreference",
    "AchievementType",

    # Models
    "StudentProfile",
    "Session",
    "PlanHistory",
    "LearningHistory",
    "Achievement",
    "TeachingMemory",
    "StudentState",

    # State Manager
    "StateManager",

    # Achievements
    "ACHIEVEMENTS",
    "check_all_achievements",
    "check_milestone_achievements",
    "check_streak_achievements",
    "check_speed_achievements",
    "check_mastery_achievements",
    "check_persistence_achievements",
]

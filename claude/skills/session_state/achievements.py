"""
Achievement system for gamification and motivation.

Defines 15+ achievements and checking logic.
"""

from typing import List, Optional
from datetime import datetime, timedelta
from .models import Achievement, AchievementType, StudentState


# ============================================================================
# Achievement Definitions
# ============================================================================

ACHIEVEMENTS = [
    # Milestone Achievements (5)
    Achievement(
        achievement_id="first_task",
        type=AchievementType.MILESTONE,
        title="First Task Complete!",
        description="You completed your first learning task",
        earned_at="",  # Set when earned
        criteria="Complete 1 task",
        icon="🎯",
        rarity="common"
    ),
    Achievement(
        achievement_id="first_checkpoint",
        type=AchievementType.MILESTONE,
        title="First Checkpoint Passed!",
        description="You passed your first checkpoint",
        earned_at="",
        criteria="Pass 1 checkpoint",
        icon="✅",
        rarity="common"
    ),
    Achievement(
        achievement_id="first_plan",
        type=AchievementType.MILESTONE,
        title="First Plan Complete!",
        description="You finished your first learning plan",
        earned_at="",
        criteria="Complete 1 learning plan",
        icon="🎓",
        rarity="rare"
    ),
    Achievement(
        achievement_id="five_plans",
        type=AchievementType.MILESTONE,
        title="Five Plans Complete!",
        description="You completed 5 learning plans",
        earned_at="",
        criteria="Complete 5 learning plans",
        icon="🌟",
        rarity="rare"
    ),
    Achievement(
        achievement_id="ten_plans",
        type=AchievementType.MILESTONE,
        title="Ten Plans Complete!",
        description="You completed 10 learning plans",
        earned_at="",
        criteria="Complete 10 learning plans",
        icon="💎",
        rarity="epic"
    ),

    # Streak Achievements (3)
    Achievement(
        achievement_id="streak_3",
        type=AchievementType.STREAK,
        title="3-Day Streak",
        description="You learned 3 days in a row",
        earned_at="",
        criteria="Learn 3 consecutive days",
        icon="🔥",
        rarity="common"
    ),
    Achievement(
        achievement_id="streak_7",
        type=AchievementType.STREAK,
        title="7-Day Streak",
        description="You learned 7 days in a row",
        earned_at="",
        criteria="Learn 7 consecutive days",
        icon="🔥🔥",
        rarity="rare"
    ),
    Achievement(
        achievement_id="streak_30",
        type=AchievementType.STREAK,
        title="30-Day Streak",
        description="You learned 30 days in a row",
        earned_at="",
        criteria="Learn 30 consecutive days",
        icon="🔥🔥🔥",
        rarity="legendary"
    ),

    # Speed Achievements (3)
    Achievement(
        achievement_id="speed_learner",
        type=AchievementType.SPEED,
        title="Speed Learner",
        description="You completed 5 tasks in one day",
        earned_at="",
        criteria="Complete 5 tasks in 1 day",
        icon="⚡",
        rarity="common"
    ),
    Achievement(
        achievement_id="lightning_fast",
        type=AchievementType.SPEED,
        title="Lightning Fast",
        description="You completed a plan in half the estimated time",
        earned_at="",
        criteria="Complete plan in 50% of estimated time",
        icon="⚡⚡",
        rarity="epic"
    ),
    Achievement(
        achievement_id="task_machine",
        type=AchievementType.SPEED,
        title="Task Machine",
        description="You completed 10 tasks in one session",
        earned_at="",
        criteria="Complete 10 tasks in 1 session",
        icon="⚡⚡⚡",
        rarity="rare"
    ),

    # Mastery Achievements (2)
    Achievement(
        achievement_id="perfect_score",
        type=AchievementType.MASTERY,
        title="Perfect Score",
        description="You passed all checkpoints on the first try",
        earned_at="",
        criteria="Pass all checkpoints without fails",
        icon="💯",
        rarity="epic"
    ),
    Achievement(
        achievement_id="no_struggles",
        type=AchievementType.MASTERY,
        title="No Struggles",
        description="You completed a plan with no struggle areas",
        earned_at="",
        criteria="Complete plan with 0 struggles",
        icon="🌟",
        rarity="rare"
    ),

    # Persistence Achievements (2)
    Achievement(
        achievement_id="comeback_kid",
        type=AchievementType.PERSISTENCE,
        title="Comeback Kid",
        description="You completed a task after struggling for 10+ days",
        earned_at="",
        criteria="Complete task after 10+ days struggle",
        icon="💪",
        rarity="rare"
    ),
    Achievement(
        achievement_id="never_give_up",
        type=AchievementType.PERSISTENCE,
        title="Never Give Up",
        description="You completed a plan despite 3+ severe struggles",
        earned_at="",
        criteria="Complete plan with 3+ severe struggles",
        icon="💪💪",
        rarity="epic"
    ),
]


# ============================================================================
# Achievement Checking Functions
# ============================================================================

def check_milestone_achievements(
    state: StudentState,
    analytics: Optional[object] = None
) -> List[Achievement]:
    """
    Check for milestone achievements.

    Args:
        state: Student state
        analytics: Learning analytics (optional)

    Returns:
        List of newly earned achievements
    """
    earned = []
    already_earned = {a.achievement_id for a in state.achievements}

    # First task
    if "first_task" not in already_earned:
        if state.history.total_tasks_completed >= 1:
            achievement = _create_achievement("first_task")
            earned.append(achievement)

    # First checkpoint
    if "first_checkpoint" not in already_earned:
        if state.history.total_checkpoints_passed >= 1:
            achievement = _create_achievement("first_checkpoint")
            earned.append(achievement)

    # First plan
    if "first_plan" not in already_earned:
        if state.history.completed_plans >= 1:
            achievement = _create_achievement("first_plan")
            earned.append(achievement)

    # Five plans
    if "five_plans" not in already_earned:
        if state.history.completed_plans >= 5:
            achievement = _create_achievement("five_plans")
            earned.append(achievement)

    # Ten plans
    if "ten_plans" not in already_earned:
        if state.history.completed_plans >= 10:
            achievement = _create_achievement("ten_plans")
            earned.append(achievement)

    return earned


def check_streak_achievements(state: StudentState) -> List[Achievement]:
    """
    Check for streak achievements.

    Args:
        state: Student state

    Returns:
        List of newly earned achievements
    """
    earned = []
    already_earned = {a.achievement_id for a in state.achievements}

    # Calculate current streak
    streak_days = _calculate_streak(state.sessions)

    # 3-day streak
    if "streak_3" not in already_earned and streak_days >= 3:
        achievement = _create_achievement("streak_3")
        earned.append(achievement)

    # 7-day streak
    if "streak_7" not in already_earned and streak_days >= 7:
        achievement = _create_achievement("streak_7")
        earned.append(achievement)

    # 30-day streak
    if "streak_30" not in already_earned and streak_days >= 30:
        achievement = _create_achievement("streak_30")
        earned.append(achievement)

    return earned


def check_speed_achievements(
    state: StudentState,
    analytics: Optional[object] = None
) -> List[Achievement]:
    """
    Check for speed achievements.

    Args:
        state: Student state
        analytics: Learning analytics (optional)

    Returns:
        List of newly earned achievements
    """
    earned = []
    already_earned = {a.achievement_id for a in state.achievements}

    # Speed learner (5 tasks in one day)
    if "speed_learner" not in already_earned:
        max_tasks_per_day = _get_max_tasks_per_day(state.sessions)
        if max_tasks_per_day >= 5:
            achievement = _create_achievement("speed_learner")
            earned.append(achievement)

    # Task machine (10 tasks in one session)
    if "task_machine" not in already_earned:
        max_tasks_per_session = max(
            (len(s.tasks_completed) for s in state.sessions),
            default=0
        )
        if max_tasks_per_session >= 10:
            achievement = _create_achievement("task_machine")
            earned.append(achievement)

    # Lightning fast (plan in half estimated time)
    if "lightning_fast" not in already_earned and analytics:
        # Check if any plan was completed in < 50% of estimated time
        for plan_hist in state.history.plans:
            if plan_hist.completed_at:
                # Assume estimated time is in plan (would need to access plan data)
                # For now, use a heuristic: very high velocity
                if plan_hist.average_velocity >= 10.0:  # 10 tasks/week is very fast
                    achievement = _create_achievement("lightning_fast")
                    earned.append(achievement)
                    break

    return earned


def check_mastery_achievements(
    state: StudentState,
    analytics: Optional[object] = None
) -> List[Achievement]:
    """
    Check for mastery achievements.

    Args:
        state: Student state
        analytics: Learning analytics (optional)

    Returns:
        List of newly earned achievements
    """
    earned = []
    already_earned = {a.achievement_id for a in state.achievements}

    # Perfect score (all checkpoints passed, none failed)
    if "perfect_score" not in already_earned:
        for plan_hist in state.history.plans:
            if plan_hist.completed_at and plan_hist.checkpoints_failed == 0:
                if plan_hist.checkpoints_passed > 0:
                    achievement = _create_achievement("perfect_score")
                    earned.append(achievement)
                    break

    # No struggles
    if "no_struggles" not in already_earned:
        for plan_hist in state.history.plans:
            if plan_hist.completed_at and len(plan_hist.struggled_with) == 0:
                achievement = _create_achievement("no_struggles")
                earned.append(achievement)
                break

    return earned


def check_persistence_achievements(
    state: StudentState,
    analytics: Optional[object] = None
) -> List[Achievement]:
    """
    Check for persistence achievements.

    Args:
        state: Student state
        analytics: Learning analytics (optional)

    Returns:
        List of newly earned achievements
    """
    earned = []
    already_earned = {a.achievement_id for a in state.achievements}

    # Never give up (completed plan with 3+ severe struggles)
    if "never_give_up" not in already_earned:
        for plan_hist in state.history.plans:
            if plan_hist.completed_at and len(plan_hist.struggled_with) >= 3:
                achievement = _create_achievement("never_give_up")
                earned.append(achievement)
                break

    # Comeback kid would need task-level timing data
    # For now, skip (would need more detailed task history)

    return earned


def check_all_achievements(
    state: StudentState,
    analytics: Optional[object] = None
) -> List[Achievement]:
    """
    Check all achievement types.

    Args:
        state: Student state
        analytics: Learning analytics (optional)

    Returns:
        List of all newly earned achievements
    """
    earned = []

    earned.extend(check_milestone_achievements(state, analytics))
    earned.extend(check_streak_achievements(state))
    earned.extend(check_speed_achievements(state, analytics))
    earned.extend(check_mastery_achievements(state, analytics))
    earned.extend(check_persistence_achievements(state, analytics))

    return earned


# ============================================================================
# Helper Functions
# ============================================================================

def _create_achievement(achievement_id: str) -> Achievement:
    """
    Create achievement instance from definition.

    Args:
        achievement_id: Achievement ID

    Returns:
        Achievement with earned_at set to now
    """
    # Find definition
    definition = next(
        (a for a in ACHIEVEMENTS if a.achievement_id == achievement_id),
        None
    )

    if not definition:
        raise ValueError(f"Unknown achievement: {achievement_id}")

    # Create instance with current time
    return Achievement(
        achievement_id=definition.achievement_id,
        type=definition.type,
        title=definition.title,
        description=definition.description,
        earned_at=datetime.now().isoformat(),
        criteria=definition.criteria,
        icon=definition.icon,
        rarity=definition.rarity
    )


def _calculate_streak(sessions: List) -> int:
    """
    Calculate current learning streak in days.

    Args:
        sessions: List of sessions

    Returns:
        Number of consecutive days with sessions
    """
    if not sessions:
        return 0

    # Get unique session dates (YYYY-MM-DD)
    session_dates = set()
    for session in sessions:
        if session.start_time:
            date_str = session.start_time[:10]  # Get YYYY-MM-DD
            session_dates.add(date_str)

    if not session_dates:
        return 0

    # Sort dates
    sorted_dates = sorted(session_dates, reverse=True)

    # Count consecutive days from today
    today = datetime.now().date()
    streak = 0

    for i, date_str in enumerate(sorted_dates):
        session_date = datetime.fromisoformat(date_str).date()
        expected_date = today - timedelta(days=i)

        if session_date == expected_date:
            streak += 1
        else:
            break

    return streak


def _get_max_tasks_per_day(sessions: List) -> int:
    """
    Get maximum tasks completed in a single day.

    Args:
        sessions: List of sessions

    Returns:
        Max tasks in one day
    """
    # Group sessions by date
    tasks_by_date = {}

    for session in sessions:
        if session.start_time:
            date_str = session.start_time[:10]
            tasks_count = len(session.tasks_completed)

            if date_str in tasks_by_date:
                tasks_by_date[date_str] += tasks_count
            else:
                tasks_by_date[date_str] = tasks_count

    return max(tasks_by_date.values()) if tasks_by_date else 0

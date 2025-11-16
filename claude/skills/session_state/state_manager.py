"""
State manager for persistent student state.

Manages student profiles, sessions, history, achievements, and teaching memory.
"""

from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import json

from .models import (
    StudentProfile,
    Session,
    PlanHistory,
    LearningHistory,
    Achievement,
    TeachingMemory,
    StudentState,
    LearningStyle,
    DifficultyPreference,
)
from .achievements import check_all_achievements


# ============================================================================
# State Manager
# ============================================================================

class StateManager:
    """
    Manages student state and persistence.

    Provides methods for profile management, session tracking, learning history,
    achievements, teaching memory, and file-based persistence.
    """

    def __init__(self, storage_dir: str = "student_states/"):
        """
        Initialize state manager.

        Args:
            storage_dir: Directory for storing student state files
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True, parents=True)

        # In-memory cache for active students
        self._cache: Dict[str, StudentState] = {}

    # ========================================================================
    # Profile Management
    # ========================================================================

    def create_student(
        self,
        student_id: str,
        name: Optional[str] = None,
        **preferences
    ) -> StudentState:
        """
        Create new student state.

        Args:
            student_id: Unique student identifier
            name: Student name (optional)
            **preferences: Additional profile preferences

        Returns:
            New student state

        Example:
            state = manager.create_student(
                "alex_2025",
                name="Alex",
                learning_style="visual",
                difficulty_preference="intermediate"
            )
        """
        # Check if student already exists
        existing = self.get_student(student_id)
        if existing:
            raise ValueError(f"Student {student_id} already exists")

        # Create profile
        profile = StudentProfile(
            student_id=student_id,
            name=name,
            **preferences
        )

        # Create history
        history = LearningHistory(student_id=student_id)

        # Create teaching memory
        teaching_memory = TeachingMemory(student_id=student_id)

        # Create state
        state = StudentState(
            profile=profile,
            history=history,
            teaching_memory=teaching_memory
        )

        # Save
        self.save_state(state)

        return state

    def get_student(self, student_id: str) -> Optional[StudentState]:
        """
        Load student state.

        Args:
            student_id: Student identifier

        Returns:
            Student state or None if not found
        """
        # Check cache first
        if student_id in self._cache:
            return self._cache[student_id]

        # Load from file
        state = self.load_state(student_id)

        # Cache if found
        if state:
            self._cache[student_id] = state

        return state

    def update_profile(
        self,
        student_id: str,
        **updates
    ) -> StudentState:
        """
        Update student profile.

        Args:
            student_id: Student identifier
            **updates: Profile fields to update

        Returns:
            Updated student state

        Example:
            state = manager.update_profile(
                "alex_2025",
                learning_style="hands_on",
                preferred_pace="fast"
            )
        """
        state = self.get_student(student_id)
        if not state:
            raise ValueError(f"Student {student_id} not found")

        # Update profile fields
        for key, value in updates.items():
            if hasattr(state.profile, key):
                setattr(state.profile, key, value)

        # Update last active
        state.profile.last_active = datetime.now().isoformat()
        state.last_updated = datetime.now().isoformat()

        # Save
        self.save_state(state)

        return state

    # ========================================================================
    # Session Management
    # ========================================================================

    def start_session(
        self,
        student_id: str,
        plan_id: Optional[str] = None
    ) -> Session:
        """
        Start new learning session.

        Args:
            student_id: Student identifier
            plan_id: Current plan ID (optional)

        Returns:
            New session

        Example:
            session = manager.start_session("alex_2025", plan_id="nav_plan_1")
        """
        state = self.get_student(student_id)
        if not state:
            raise ValueError(f"Student {student_id} not found")

        # End current session if exists
        if state.current_session:
            self.end_session(student_id)
            state = self.get_student(student_id)  # Reload

        # Create new session
        session_id = f"sess_{len(state.sessions) + 1:04d}"
        session = Session(
            session_id=session_id,
            student_id=student_id,
            start_time=datetime.now().isoformat(),
            plan_id=plan_id
        )

        # Set as current
        state.current_session = session
        state.last_updated = datetime.now().isoformat()

        # Save
        self.save_state(state)

        return session

    def end_session(
        self,
        student_id: str,
        session_notes: str = ""
    ) -> Session:
        """
        End current session.

        Args:
            student_id: Student identifier
            session_notes: Notes about the session (optional)

        Returns:
            Completed session

        Example:
            session = manager.end_session("alex_2025", "Great progress today!")
        """
        state = self.get_student(student_id)
        if not state:
            raise ValueError(f"Student {student_id} not found")

        if not state.current_session:
            raise ValueError("No active session")

        # Complete session
        session = state.current_session
        session.end_time = datetime.now().isoformat()
        session.session_notes = session_notes

        # Calculate duration
        start = datetime.fromisoformat(session.start_time)
        end = datetime.fromisoformat(session.end_time)
        session.duration_minutes = int((end - start).total_seconds() / 60)

        # Add to sessions list
        state.sessions.append(session)

        # Clear current session
        state.current_session = None

        # Update profile
        state.profile.last_active = datetime.now().isoformat()
        state.last_updated = datetime.now().isoformat()

        # Save
        self.save_state(state)

        return session

    def get_current_session(
        self,
        student_id: str
    ) -> Optional[Session]:
        """
        Get current active session.

        Args:
            student_id: Student identifier

        Returns:
            Current session or None
        """
        state = self.get_student(student_id)
        if not state:
            return None

        return state.current_session

    # ========================================================================
    # Learning History
    # ========================================================================

    def add_plan_to_history(
        self,
        student_id: str,
        plan_history: PlanHistory
    ):
        """
        Add completed/in-progress plan to history.

        Args:
            student_id: Student identifier
            plan_history: Plan history entry

        Example:
            plan_hist = PlanHistory(
                plan_id="nav_1",
                plan_title="Navigation",
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
        """
        state = self.get_student(student_id)
        if not state:
            raise ValueError(f"Student {student_id} not found")

        # Check if plan already in history (update if so)
        existing_idx = None
        for i, p in enumerate(state.history.plans):
            if p.plan_id == plan_history.plan_id:
                existing_idx = i
                break

        if existing_idx is not None:
            state.history.plans[existing_idx] = plan_history
        else:
            state.history.plans.append(plan_history)

        # Update totals
        state.history.total_plans = len(state.history.plans)
        state.history.completed_plans = sum(
            1 for p in state.history.plans if p.completed_at
        )

        state.history.total_tasks_completed = sum(
            p.completed_tasks for p in state.history.plans
        )

        state.history.total_checkpoints_passed = sum(
            p.checkpoints_passed for p in state.history.plans
        )

        # Calculate average velocity
        completed_plans = [p for p in state.history.plans if p.completed_at]
        if completed_plans:
            velocities = [p.average_velocity for p in completed_plans]
            state.history.average_velocity_all_time = sum(velocities) / len(velocities)

        # Update struggled topics
        all_struggles = []
        for p in state.history.plans:
            all_struggles.extend(p.struggled_with)

        # Get top 5 most common struggles
        from collections import Counter
        struggle_counts = Counter(all_struggles)
        state.history.most_struggled_topics = [
            topic for topic, _ in struggle_counts.most_common(5)
        ]

        state.last_updated = datetime.now().isoformat()

        # Save
        self.save_state(state)

    def get_learning_history(
        self,
        student_id: str
    ) -> LearningHistory:
        """
        Get complete learning history.

        Args:
            student_id: Student identifier

        Returns:
            Learning history
        """
        state = self.get_student(student_id)
        if not state:
            raise ValueError(f"Student {student_id} not found")

        return state.history

    def get_recent_activity(
        self,
        student_id: str,
        days: int = 7
    ) -> Dict[str, Any]:
        """
        Get recent activity summary.

        Args:
            student_id: Student identifier
            days: Number of days to look back

        Returns:
            Activity summary dict

        Example:
            activity = manager.get_recent_activity("alex_2025", days=7)
            # Returns:
            # {
            #     "last_session": "2 days ago",
            #     "sessions_this_period": 3,
            #     "tasks_completed_this_period": 7,
            #     "time_spent_minutes": 180
            # }
        """
        state = self.get_student(student_id)
        if not state:
            raise ValueError(f"Student {student_id} not found")

        # Calculate cutoff date
        cutoff = datetime.now() - timedelta(days=days)

        # Filter recent sessions
        recent_sessions = [
            s for s in state.sessions
            if datetime.fromisoformat(s.start_time) >= cutoff
        ]

        # Calculate stats
        tasks_completed = sum(
            len(s.tasks_completed) for s in recent_sessions
        )

        time_spent = sum(
            s.duration_minutes or 0 for s in recent_sessions
        )

        # Last session
        last_session_time = None
        if state.sessions:
            last_session = max(
                state.sessions,
                key=lambda s: s.start_time
            )
            last_start = datetime.fromisoformat(last_session.start_time)
            days_ago = (datetime.now() - last_start).days
            if days_ago == 0:
                last_session_time = "today"
            elif days_ago == 1:
                last_session_time = "yesterday"
            else:
                last_session_time = f"{days_ago} days ago"

        return {
            "last_session": last_session_time,
            "sessions_this_period": len(recent_sessions),
            "tasks_completed_this_period": tasks_completed,
            "time_spent_minutes": time_spent,
        }

    # ========================================================================
    # Achievements
    # ========================================================================

    def award_achievement(
        self,
        student_id: str,
        achievement: Achievement
    ):
        """
        Award achievement to student.

        Args:
            student_id: Student identifier
            achievement: Achievement to award
        """
        state = self.get_student(student_id)
        if not state:
            raise ValueError(f"Student {student_id} not found")

        # Check if already earned
        if achievement.achievement_id in {a.achievement_id for a in state.achievements}:
            return

        # Add achievement
        state.achievements.append(achievement)
        state.last_updated = datetime.now().isoformat()

        # Save
        self.save_state(state)

    def check_achievements(
        self,
        student_id: str,
        analytics: Optional[Any] = None
    ) -> List[Achievement]:
        """
        Check if student earned new achievements.

        Args:
            student_id: Student identifier
            analytics: Learning analytics (optional)

        Returns:
            List of newly earned achievements

        Example:
            new_achievements = manager.check_achievements("alex_2025", analytics)
            for achievement in new_achievements:
                print(f"🎉 {achievement.title}: {achievement.description}")
        """
        state = self.get_student(student_id)
        if not state:
            raise ValueError(f"Student {student_id} not found")

        # Check all achievements
        new_achievements = check_all_achievements(state, analytics)

        # Award each new achievement
        for achievement in new_achievements:
            self.award_achievement(student_id, achievement)

        return new_achievements

    def get_achievements(
        self,
        student_id: str
    ) -> List[Achievement]:
        """
        Get all student achievements.

        Args:
            student_id: Student identifier

        Returns:
            List of achievements
        """
        state = self.get_student(student_id)
        if not state:
            raise ValueError(f"Student {student_id} not found")

        return state.achievements

    # ========================================================================
    # Teaching Memory
    # ========================================================================

    def record_teaching_strategy(
        self,
        student_id: str,
        strategy: str,
        effective: bool
    ):
        """
        Record whether a teaching strategy worked.

        Args:
            student_id: Student identifier
            strategy: Description of strategy used
            effective: Whether it was effective

        Example:
            manager.record_teaching_strategy(
                "alex_2025",
                "visual diagrams with step-by-step breakdown",
                effective=True
            )
        """
        state = self.get_student(student_id)
        if not state:
            raise ValueError(f"Student {student_id} not found")

        if effective:
            if strategy not in state.teaching_memory.effective_strategies:
                state.teaching_memory.effective_strategies.append(strategy)
        else:
            if strategy not in state.teaching_memory.ineffective_strategies:
                state.teaching_memory.ineffective_strategies.append(strategy)

        state.last_updated = datetime.now().isoformat()

        # Save
        self.save_state(state)

    def record_specialist_interaction(
        self,
        student_id: str,
        specialist: str,
        helpful: bool
    ):
        """
        Record specialist interaction effectiveness.

        Args:
            student_id: Student identifier
            specialist: Specialist agent name
            helpful: Whether the specialist was helpful

        Example:
            manager.record_specialist_interaction(
                "alex_2025",
                "robotics-vision-navigator",
                helpful=True
            )
        """
        state = self.get_student(student_id)
        if not state:
            raise ValueError(f"Student {student_id} not found")

        # Update specialist effectiveness (simple average)
        current = state.teaching_memory.specialist_effectiveness.get(specialist, 0.5)
        new_value = 1.0 if helpful else 0.0

        # Moving average (70% old, 30% new)
        updated = current * 0.7 + new_value * 0.3

        state.teaching_memory.specialist_effectiveness[specialist] = updated

        # Update favorite specialists
        sorted_specialists = sorted(
            state.teaching_memory.specialist_effectiveness.items(),
            key=lambda x: x[1],
            reverse=True
        )
        state.history.favorite_specialists = [
            name for name, score in sorted_specialists[:3]
        ]

        state.last_updated = datetime.now().isoformat()

        # Save
        self.save_state(state)

    def get_teaching_insights(
        self,
        student_id: str
    ) -> TeachingMemory:
        """
        Get teaching insights for this student.

        Args:
            student_id: Student identifier

        Returns:
            Teaching memory with insights

        Example:
            insights = manager.get_teaching_insights("alex_2025")
            print(f"Effective: {insights.effective_strategies}")
            print(f"Learns best: {insights.learns_best_when}")
        """
        state = self.get_student(student_id)
        if not state:
            raise ValueError(f"Student {student_id} not found")

        return state.teaching_memory

    # ========================================================================
    # Persistence
    # ========================================================================

    def save_state(self, student_state: StudentState):
        """
        Save student state to file.

        Args:
            student_state: Student state to save
        """
        file_path = self._get_file_path(student_state.profile.student_id)

        # Convert to dict
        state_dict = student_state.model_dump()

        # Write to file
        with open(file_path, 'w') as f:
            json.dump(state_dict, f, indent=2)

        # Update cache
        self._cache[student_state.profile.student_id] = student_state

    def load_state(self, student_id: str) -> Optional[StudentState]:
        """
        Load student state from file.

        Args:
            student_id: Student identifier

        Returns:
            Student state or None if not found
        """
        file_path = self._get_file_path(student_id)

        if not file_path.exists():
            return None

        # Read file
        with open(file_path, 'r') as f:
            state_dict = json.load(f)

        # Convert to model
        state = StudentState(**state_dict)

        return state

    def list_students(self) -> List[str]:
        """
        List all student IDs.

        Returns:
            List of student identifiers
        """
        student_files = self.storage_dir.glob("student_*.json")
        student_ids = []

        for file in student_files:
            # Extract student_id from filename
            # Format: student_{student_id}.json
            filename = file.stem  # Remove .json
            student_id = filename.replace("student_", "")
            student_ids.append(student_id)

        return sorted(student_ids)

    # ========================================================================
    # Helper Methods
    # ========================================================================

    def _get_file_path(self, student_id: str) -> Path:
        """
        Get file path for student state.

        Args:
            student_id: Student identifier

        Returns:
            Path to student state file
        """
        return self.storage_dir / f"student_{student_id}.json"

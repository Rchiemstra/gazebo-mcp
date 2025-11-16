"""
Test suite for session-state skill.

Tests student state management, sessions, history, achievements, and persistence.
"""

import sys
from pathlib import Path
import shutil

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from skills.session_state import (
    StateManager,
    LearningStyle,
    DifficultyPreference,
    PlanHistory,
)


def print_header(title):
    print("\n" + "="*60)
    print(f"{title}")
    print("="*60)


def setup_test_manager():
    """Setup manager with temp directory"""
    test_dir = "test_student_states/"
    # Clean up if exists
    if Path(test_dir).exists():
        shutil.rmtree(test_dir)

    manager = StateManager(storage_dir=test_dir)
    return manager, test_dir


def cleanup_test_manager(test_dir):
    """Clean up test directory"""
    if Path(test_dir).exists():
        shutil.rmtree(test_dir)


def test_create_student():
    """Test creating student profile"""
    print_header("Test 1: Create Student")

    manager, test_dir = setup_test_manager()

    try:
        # Create student
        state = manager.create_student(
            student_id="test_alex",
            name="Alex",
            learning_style="visual",
            difficulty_preference="intermediate"
        )

        print(f"✅ Created student: {state.profile.name}")
        print(f"   Student ID: {state.profile.student_id}")
        print(f"   Learning style: {state.profile.learning_style}")
        print(f"   Difficulty: {state.profile.difficulty_preference}")

        # Verify
        assert state.profile.student_id == "test_alex"
        assert state.profile.name == "Alex"
        assert state.profile.learning_style == LearningStyle.VISUAL
        assert state.profile.difficulty_preference == DifficultyPreference.INTERMEDIATE

        # Verify file created
        file_path = Path(test_dir) / "student_test_alex.json"
        assert file_path.exists()

        return True

    finally:
        cleanup_test_manager(test_dir)


def test_load_student():
    """Test loading student state"""
    print_header("Test 2: Load Student")

    manager, test_dir = setup_test_manager()

    try:
        # Create student
        manager.create_student(student_id="test_alex", name="Alex")

        # Load student
        state = manager.get_student("test_alex")

        print(f"✅ Loaded student: {state.profile.name}")

        assert state is not None
        assert state.profile.student_id == "test_alex"

        # Test non-existent student
        non_existent = manager.get_student("does_not_exist")
        assert non_existent is None

        return True

    finally:
        cleanup_test_manager(test_dir)


def test_update_profile():
    """Test updating student profile"""
    print_header("Test 3: Update Profile")

    manager, test_dir = setup_test_manager()

    try:
        # Create student
        manager.create_student(student_id="test_alex", name="Alex")

        # Update profile
        state = manager.update_profile(
            "test_alex",
            learning_style="hands_on",
            preferred_pace="fast"
        )

        print(f"✅ Updated profile")
        print(f"   Learning style: {state.profile.learning_style}")
        print(f"   Preferred pace: {state.profile.preferred_pace}")

        assert state.profile.learning_style == LearningStyle.HANDS_ON
        assert state.profile.preferred_pace == "fast"

        return True

    finally:
        cleanup_test_manager(test_dir)


def test_start_end_session():
    """Test session management"""
    print_header("Test 4: Session Management")

    manager, test_dir = setup_test_manager()

    try:
        # Create student
        manager.create_student(student_id="test_alex", name="Alex")

        # Start session
        session = manager.start_session("test_alex", plan_id="test_plan_1")

        print(f"✅ Started session: {session.session_id}")
        print(f"   Plan ID: {session.plan_id}")

        assert session.session_id == "sess_0001"
        assert session.plan_id == "test_plan_1"
        assert session.start_time is not None
        assert session.end_time is None

        # Get current session
        current = manager.get_current_session("test_alex")
        assert current is not None
        assert current.session_id == "sess_0001"

        # End session
        ended_session = manager.end_session("test_alex", "Test session complete")

        print(f"✅ Ended session")
        print(f"   Duration: {ended_session.duration_minutes} minutes")
        print(f"   Notes: {ended_session.session_notes}")

        assert ended_session.end_time is not None
        assert ended_session.duration_minutes is not None
        assert ended_session.session_notes == "Test session complete"

        # Verify current session is None
        current = manager.get_current_session("test_alex")
        assert current is None

        # Verify session in history
        state = manager.get_student("test_alex")
        assert len(state.sessions) == 1

        return True

    finally:
        cleanup_test_manager(test_dir)


def test_learning_history():
    """Test learning history management"""
    print_header("Test 5: Learning History")

    manager, test_dir = setup_test_manager()

    try:
        # Create student
        manager.create_student(student_id="test_alex", name="Alex")

        # Add plan to history
        plan_hist = PlanHistory(
            plan_id="test_plan_1",
            plan_title="Test Navigation",
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

        manager.add_plan_to_history("test_alex", plan_hist)

        print(f"✅ Added plan to history")

        # Get history
        history = manager.get_learning_history("test_alex")

        print(f"   Total plans: {history.total_plans}")
        print(f"   Completed plans: {history.completed_plans}")
        print(f"   Total tasks: {history.total_tasks_completed}")
        print(f"   Average velocity: {history.average_velocity_all_time}")

        assert history.total_plans == 1
        assert history.completed_plans == 1
        assert history.total_tasks_completed == 20
        assert history.total_checkpoints_passed == 4
        assert history.average_velocity_all_time == 2.5

        return True

    finally:
        cleanup_test_manager(test_dir)


def test_recent_activity():
    """Test recent activity tracking"""
    print_header("Test 6: Recent Activity")

    manager, test_dir = setup_test_manager()

    try:
        # Create student
        manager.create_student(student_id="test_alex", name="Alex")

        # Start and end a session
        manager.start_session("test_alex", plan_id="test_plan_1")

        # Update session with tasks
        state = manager.get_student("test_alex")
        state.current_session.tasks_completed = ["task-1", "task-2", "task-3"]
        manager.save_state(state)

        manager.end_session("test_alex", "Session complete")

        # Get recent activity
        activity = manager.get_recent_activity("test_alex", days=7)

        print(f"✅ Recent activity (7 days):")
        print(f"   Last session: {activity['last_session']}")
        print(f"   Sessions: {activity['sessions_this_period']}")
        print(f"   Tasks completed: {activity['tasks_completed_this_period']}")

        assert activity['sessions_this_period'] == 1
        assert activity['tasks_completed_this_period'] == 3
        assert activity['last_session'] == "today"

        return True

    finally:
        cleanup_test_manager(test_dir)


def test_achievements():
    """Test achievement system"""
    print_header("Test 7: Achievements")

    manager, test_dir = setup_test_manager()

    try:
        # Create student
        manager.create_student(student_id="test_alex", name="Alex")

        # Add plan to history (should trigger achievements)
        plan_hist = PlanHistory(
            plan_id="test_plan_1",
            plan_title="Test Plan",
            started_at="2025-10-01",
            completed_at="2025-10-15",
            total_tasks=20,
            completed_tasks=20,
            completion_percentage=100.0,
            average_velocity=2.5,
            total_time_weeks=2.0,
            checkpoints_passed=4,
            checkpoints_failed=0,
        )

        manager.add_plan_to_history("test_alex", plan_hist)

        # Check achievements
        new_achievements = manager.check_achievements("test_alex")

        print(f"✅ Achievements unlocked: {len(new_achievements)}")
        for achievement in new_achievements:
            print(f"   {achievement.icon} {achievement.title}")

        # Should have at least first_task, first_checkpoint, first_plan
        assert len(new_achievements) >= 3

        # Get all achievements
        all_achievements = manager.get_achievements("test_alex")
        assert len(all_achievements) >= 3

        # Check again (should return 0 new achievements)
        new_again = manager.check_achievements("test_alex")
        assert len(new_again) == 0

        return True

    finally:
        cleanup_test_manager(test_dir)


def test_teaching_memory():
    """Test teaching memory"""
    print_header("Test 8: Teaching Memory")

    manager, test_dir = setup_test_manager()

    try:
        # Create student
        manager.create_student(student_id="test_alex", name="Alex")

        # Record teaching strategies
        manager.record_teaching_strategy(
            "test_alex",
            "visual diagrams",
            effective=True
        )

        manager.record_teaching_strategy(
            "test_alex",
            "abstract explanations",
            effective=False
        )

        # Record specialist interactions
        manager.record_specialist_interaction(
            "test_alex",
            "robotics-vision-navigator",
            helpful=True
        )

        manager.record_specialist_interaction(
            "test_alex",
            "debugging-detective",
            helpful=True
        )

        # Get insights
        insights = manager.get_teaching_insights("test_alex")

        print(f"✅ Teaching insights recorded")
        print(f"   Effective strategies: {insights.effective_strategies}")
        print(f"   Ineffective strategies: {insights.ineffective_strategies}")
        print(f"   Specialist effectiveness: {insights.specialist_effectiveness}")

        assert "visual diagrams" in insights.effective_strategies
        assert "abstract explanations" in insights.ineffective_strategies
        assert "robotics-vision-navigator" in insights.specialist_effectiveness

        return True

    finally:
        cleanup_test_manager(test_dir)


def test_persistence():
    """Test file-based persistence"""
    print_header("Test 9: Persistence")

    manager, test_dir = setup_test_manager()

    try:
        # Create student
        manager.create_student(student_id="test_alex", name="Alex")

        # Modify state
        manager.start_session("test_alex")
        manager.end_session("test_alex")

        # Create new manager instance (fresh cache)
        manager2 = StateManager(storage_dir=test_dir)

        # Load student with new manager
        state = manager2.get_student("test_alex")

        print(f"✅ State persisted and loaded")
        print(f"   Student ID: {state.profile.student_id}")
        print(f"   Sessions: {len(state.sessions)}")

        assert state is not None
        assert state.profile.student_id == "test_alex"
        assert len(state.sessions) == 1

        return True

    finally:
        cleanup_test_manager(test_dir)


def test_list_students():
    """Test listing all students"""
    print_header("Test 10: List Students")

    manager, test_dir = setup_test_manager()

    try:
        # Create multiple students
        manager.create_student(student_id="alex", name="Alex")
        manager.create_student(student_id="jordan", name="Jordan")
        manager.create_student(student_id="sam", name="Sam")

        # List students
        students = manager.list_students()

        print(f"✅ Listed students: {len(students)}")
        for student_id in students:
            print(f"   - {student_id}")

        assert len(students) == 3
        assert "alex" in students
        assert "jordan" in students
        assert "sam" in students

        return True

    finally:
        cleanup_test_manager(test_dir)


def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("session-state Skill - Test Suite")
    print("="*60)

    tests = [
        ("Create Student", test_create_student),
        ("Load Student", test_load_student),
        ("Update Profile", test_update_profile),
        ("Session Management", test_start_end_session),
        ("Learning History", test_learning_history),
        ("Recent Activity", test_recent_activity),
        ("Achievements", test_achievements),
        ("Teaching Memory", test_teaching_memory),
        ("Persistence", test_persistence),
        ("List Students", test_list_students),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Print summary
    print_header("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)

    print(f"\nPassed: {passed}/{total}")

    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")

    if passed == total:
        print(f"\n✅ All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)

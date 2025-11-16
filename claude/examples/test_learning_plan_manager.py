"""
Test script for learning-plan-manager skill.

Demonstrates basic usage and validates against existing learning plans.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from skills.learning_plan_manager import (
    LearningPlanManager,
    TaskStatus,
    CheckpointStatus,
)


def test_load_and_query():
    """Test loading and querying a learning plan"""
    print("=" * 60)
    print("Test 1: Load and Query Learning Plan")
    print("=" * 60)

    manager = LearningPlanManager()

    # Find latest plan
    print("\n1. Finding latest plan...")
    plan = manager.find_latest_plan()

    if not plan:
        print("❌ No learning plans found in plans/ directory")
        return False

    print(f"✅ Loaded: {plan.metadata.title}")
    print(f"   Created: {plan.metadata.created.strftime('%Y-%m-%d')}")
    print(f"   Complexity: {plan.metadata.complexity_level.value}")

    # Get current phase
    print("\n2. Getting current phase...")
    current_phase = plan.get_current_phase()
    if current_phase:
        print(f"✅ Current Phase: Phase {current_phase.number} - {current_phase.title}")
        print(f"   Learning Goals: {len(current_phase.learning_goals)}")
        print(f"   Tasks: {len(current_phase.tasks)}")
    else:
        print("⚠️  No current phase found")

    # Get next task
    print("\n3. Getting next task...")
    next_task = plan.get_next_task()
    if next_task:
        print(f"✅ Next Task: {next_task.title}")
        print(f"   Status: {next_task.status.value}")
    else:
        print("⚠️  No next task found (all completed?)")

    # Calculate progress
    print("\n4. Calculating progress...")
    progress = plan.calculate_progress()
    print(f"✅ Overall Progress: {progress['overall_percentage']:.1f}%")
    print(f"   Phases: {progress['phases']['completed']}/{progress['phases']['total']}")
    print(f"   Tasks: {progress['tasks']['completed']}/{progress['tasks']['total']}")
    print(
        f"   Checkpoints: {progress['checkpoints']['passed']}/{progress['checkpoints']['total']}"
    )

    return True


def test_list_plans():
    """Test listing all plans"""
    print("\n" + "=" * 60)
    print("Test 2: List All Plans")
    print("=" * 60 + "\n")

    manager = LearningPlanManager()

    plans = manager.list_plans()

    if not plans:
        print("❌ No plans found")
        return False

    print(f"✅ Found {len(plans)} plan(s):\n")

    for i, plan_summary in enumerate(plans, 1):
        print(f"{i}. {plan_summary['title']}")
        print(f"   Progress: {plan_summary['progress']:.1f}%")
        print(f"   Current: {plan_summary['current_phase'] or 'Not started'}")
        print(f"   Updated: {plan_summary['updated'].strftime('%Y-%m-%d %H:%M')}")
        print()

    return True


def test_progress_report():
    """Test generating progress report"""
    print("=" * 60)
    print("Test 3: Generate Progress Report")
    print("=" * 60 + "\n")

    manager = LearningPlanManager()

    plan = manager.find_latest_plan()
    if not plan:
        print("❌ No plan found")
        return False

    report = manager.export_progress_report(plan)

    print("✅ Generated progress report:\n")
    print(report[:500] + "..." if len(report) > 500 else report)

    return True


def test_export_json():
    """Test JSON export"""
    print("\n" + "=" * 60)
    print("Test 4: Export to JSON")
    print("=" * 60 + "\n")

    manager = LearningPlanManager()

    plan = manager.find_latest_plan()
    if not plan:
        print("❌ No plan found")
        return False

    json_str = manager.export_json(plan)

    # Parse to verify it's valid JSON
    import json

    try:
        data = json.loads(json_str)
        print(f"✅ Exported to JSON ({len(json_str)} bytes)")
        print(f"   Contains {len(data['phases'])} phases")
        print(f"   Contains {sum(len(p['tasks']) for p in data['phases'])} tasks")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return False


def test_update_task(dry_run=True):
    """Test updating task status"""
    print("\n" + "=" * 60)
    print(f"Test 5: Update Task Status {'(DRY RUN)' if dry_run else ''}")
    print("=" * 60 + "\n")

    manager = LearningPlanManager()

    plan = manager.find_latest_plan()
    if not plan:
        print("❌ No plan found")
        return False

    # Find a task to update
    next_task = plan.get_next_task()
    if not next_task:
        print("⚠️  No task to update (all completed)")
        return True

    print(f"Current task: {next_task.title}")
    print(f"Current status: {next_task.status.value}")

    if not dry_run:
        # Actually update
        old_status = next_task.status
        plan = manager.update_task_status(
            plan,
            next_task.id,
            TaskStatus.IN_PROGRESS,
            notes="Updated by test script",
        )

        print(f"\n✅ Updated task status: {old_status.value} → in_progress")

        # Save
        saved_path = manager.save_plan(plan)
        print(f"✅ Saved to: {saved_path}")
    else:
        print(
            "\n⚠️  DRY RUN - no changes made (set dry_run=False to actually update)"
        )

    return True


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("Learning Plan Manager - Test Suite")
    print("=" * 60)

    tests = [
        test_load_and_query,
        test_list_plans,
        test_progress_report,
        test_export_json,
        lambda: test_update_task(dry_run=True),  # Dry run by default
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n❌ Test failed with exception: {e}")
            import traceback

            traceback.print_exc()
            results.append(False)

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"\nPassed: {passed}/{total}")

    if passed == total:
        print("✅ All tests passed!")
    else:
        print(f"❌ {total - passed} test(s) failed")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

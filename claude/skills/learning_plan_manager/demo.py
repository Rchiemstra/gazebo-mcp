#!/usr/bin/env python3
"""
Demo: Learning Plan Manager Skill

This demonstrates how agents would use the learning-plan-manager skill
to access and manipulate learning plans.

NOTE: This is a documentation-only skill. These operations are not yet
implemented. See skill.md for the full API documentation.
"""

from skills.learning_plan_manager.operations import (
    find_latest_plan,
    get_current_phase,
    get_next_task,
    calculate_progress,
    update_task_status,
    add_journal_entry,
    OperationResult
)


def demo_basic_workflow():
    """Demonstrate a typical teaching agent workflow."""
    print("=" * 70)
    print("Learning Plan Manager - Basic Workflow Demo")
    print("=" * 70)

    # 1. Find the latest learning plan
    print("\n1. Finding latest learning plan...")
    result = find_latest_plan()
    print(f"   Result: {result}")

    # 2. Get current phase
    print("\n2. Getting current phase...")
    result = get_current_phase(plan_file="learning-plan.json")
    print(f"   Result: {result}")

    # 3. Get next task for student
    print("\n3. Getting next task...")
    result = get_next_task(
        plan_file="learning-plan.json",
        phase_id="phase-001"
    )
    print(f"   Result: {result}")

    # 4. Update task status
    print("\n4. Marking task as completed...")
    result = update_task_status(
        plan_file="learning-plan.json",
        task_id="task-001",
        status="completed"
    )
    print(f"   Result: {result}")

    # 5. Add journal entry
    print("\n5. Adding journal entry...")
    result = add_journal_entry(
        plan_file="learning-plan.json",
        entry_type="progress",
        content="Student successfully completed first task!"
    )
    print(f"   Result: {result}")

    # 6. Calculate overall progress
    print("\n6. Calculating progress...")
    result = calculate_progress(plan_file="learning-plan.json")
    print(f"   Result: {result}")


def demo_teaching_scenario():
    """Demonstrate how a teaching agent would use this skill."""
    print("\n" + "=" * 70)
    print("Teaching Agent Scenario")
    print("=" * 70)

    print("\nA teaching agent helping a student:")
    print("  1. Checks the learning plan to see current progress")
    print("  2. Identifies the next task for the student")
    print("  3. Guides the student through the task")
    print("  4. Updates task status when complete")
    print("  5. Records observations in journal")
    print("  6. Checks if phase is complete to move forward")

    print("\nThis skill provides the data layer for adaptive teaching!")


if __name__ == "__main__":
    print("\n" + "!" * 70)
    print("NOTE: This is a documentation-only skill")
    print("All operations will return NOT_IMPLEMENTED errors")
    print("See skill.md for full API documentation")
    print("!" * 70)

    demo_basic_workflow()
    demo_teaching_scenario()

    print("\n" + "=" * 70)
    print("Demo complete! See skill.md for full capabilities.")
    print("=" * 70 + "\n")

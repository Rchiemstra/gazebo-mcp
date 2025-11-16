"""
Learning Plan Manager Operations

Agent-friendly interface with token efficiency and error handling.
"""

from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
import time

from .manager import LearningPlanManager
from .validator import ValidationError


@dataclass
class OperationResult:
    """Result from a skill operation."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    duration: float = 0.0
    metadata: Optional[Dict[str, Any]] = None


def load_plan(
    file_path: str,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Load and parse a learning plan from markdown file.

    Args:
        file_path: Path to learning plan markdown file
        response_format: "summary" (overview), "progress" (current status), or "detailed" (full plan)

    Returns:
        OperationResult with learning plan data

    Token Efficiency:
        - Use response_format="summary" for overview (< 500 tokens)
        - Use response_format="progress" for current status only
        - Use response_format="detailed" only when you need all phases/tasks
        - Large plans (6+ phases) can use 5000+ tokens in detailed mode
    """
    start_time = time.time()

    try:
        manager = LearningPlanManager()
        plan = manager.load_plan(file_path)

        duration = time.time() - start_time

        # Calculate progress
        progress = plan.calculate_progress()
        current_phase = plan.get_current_phase()
        next_task = plan.get_next_task()

        # Always include summary
        data = {
            "plan_name": plan.metadata.name,
            "topic": plan.metadata.topic,
            "created": plan.metadata.created.isoformat() if plan.metadata.created else None,
            "total_phases": len(plan.phases),
            "overall_progress": round(progress * 100, 1),
            "current_phase": {
                "name": current_phase.name,
                "number": current_phase.phase_number
            } if current_phase else None,
            "next_task": {
                "description": next_task.description,
                "phase": current_phase.name if current_phase else None
            } if next_task else None
        }

        if response_format == "detailed":
            # Full plan details
            data.update({
                "phases": [
                    {
                        "number": phase.phase_number,
                        "name": phase.name,
                        "description": phase.description,
                        "tasks": [
                            {
                                "description": task.description,
                                "status": task.status.value,
                                "priority": task.priority
                            }
                            for task in phase.tasks
                        ],
                        "checkpoints": [
                            {
                                "question": cp.question,
                                "status": cp.status.value if cp.status else "pending"
                            }
                            for cp in phase.checkpoints
                        ]
                    }
                    for phase in plan.phases
                ],
                "journal_entries": [
                    {
                        "date": entry.date.isoformat(),
                        "content": entry.content
                    }
                    for entry in plan.journal_entries
                ] if plan.journal_entries else []
            })
        elif response_format == "progress":
            # Just current status
            completed_tasks = sum(
                1 for phase in plan.phases
                for task in phase.tasks
                if task.status.value == "completed"
            )
            total_tasks = sum(len(phase.tasks) for phase in plan.phases)

            data.update({
                "tasks_completed": completed_tasks,
                "tasks_total": total_tasks,
                "tasks_remaining": total_tasks - completed_tasks,
                "current_phase_progress": round(current_phase.calculate_progress() * 100, 1) if current_phase else 0,
                "efficiency_tip": (
                    f"Progress loaded! {completed_tasks}/{total_tasks} tasks complete.\n"
                    f"Current: Phase {current_phase.phase_number} - {current_phase.name}\n"
                    f"For full plan details: load_plan('{file_path}', response_format='detailed')"
                )
            })
        else:  # summary
            phase_names = [p.name for p in plan.phases]
            estimated_detailed_tokens = len(plan.phases) * 500  # Rough estimate

            data.update({
                "phase_names": phase_names,
                "prerequisites": [str(p) for p in plan.metadata.prerequisites] if plan.metadata.prerequisites else [],
                "efficiency_tip": (
                    f"Plan loaded! {len(plan.phases)} phases, {progress*100:.0f}% complete.\n"
                    f"Using summary mode for efficiency (saves ~{estimated_detailed_tokens} tokens).\n"
                    f"For current progress: load_plan('{file_path}', response_format='progress')\n"
                    f"For full details: load_plan('{file_path}', response_format='detailed')"
                )
            })

        return OperationResult(
            success=True,
            data=data,
            duration=duration,
            metadata={
                "skill": "learning-plan-manager",
                "operation": "load_plan",
                "version": "0.1.0",
                "response_format": response_format
            }
        )

    except FileNotFoundError:
        return OperationResult(
            success=False,
            error=f"Cannot find learning plan: {file_path}",
            error_code="FILE_NOT_FOUND",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check if the file path is correct",
                    "Use Glob('plans/*-learning-plan.md') to find learning plans",
                    "Or use find_latest_plan() to get the most recent plan",
                    f"Verify the file exists with Bash('ls -la {Path(file_path).parent}')"
                ],
                "example_fix": "load_plan('plans/autonomous-navigation-learning-plan.md')"
            }
        )
    except ValidationError as e:
        return OperationResult(
            success=False,
            error=f"Learning plan format is invalid: {str(e)}",
            error_code="VALIDATION_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check the plan markdown format",
                    "Ensure all required sections are present (## Phase N, ### Tasks, etc.)",
                    "Use LearningPlanValidator to see specific issues",
                    "Compare with an example plan in plans/ directory"
                ]
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Failed to load learning plan: {str(e)}",
            error_code="LOAD_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure the file is a markdown file",
                    "Check if the file is readable",
                    "Try with a different plan file first"
                ]
            }
        )


def find_latest_plan(response_format: str = "summary", **kwargs) -> OperationResult:
    """
    Find and load the most recently updated learning plan.

    Args:
        response_format: "summary" (overview), "progress" (current status), or "detailed" (full plan)

    Returns:
        OperationResult with latest learning plan data

    Token Efficiency:
        - Same as load_plan - use response_format to control detail level
        - Returns None data if no plans found (not an error)
    """
    start_time = time.time()

    try:
        manager = LearningPlanManager()
        plan = manager.find_latest_plan()

        if plan is None:
            return OperationResult(
                success=True,
                data=None,
                duration=time.time() - start_time,
                metadata={
                    "skill": "learning-plan-manager",
                    "operation": "find_latest_plan",
                    "version": "0.1.0",
                    "message": "No learning plans found in plans/ directory"
                }
            )

        # Reuse load_plan logic
        return load_plan(plan.file_path, response_format=response_format)

    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Failed to find latest plan: {str(e)}",
            error_code="FIND_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check if plans/ directory exists",
                    "Ensure there are *-learning-plan.md files in plans/",
                    "Create a new plan with /start-learning <topic>"
                ]
            }
        )


def list_plans(response_format: str = "summary", **kwargs) -> OperationResult:
    """
    List all available learning plans with metadata.

    Args:
        response_format: "summary" (just names) or "detailed" (full metadata)

    Returns:
        OperationResult with list of plans

    Token Efficiency:
        - Use response_format="summary" for just plan names and topics
        - Use response_format="detailed" when you need dates and progress
    """
    start_time = time.time()

    try:
        manager = LearningPlanManager()
        plans = manager.list_plans()

        duration = time.time() - start_time

        if not plans:
            return OperationResult(
                success=True,
                data={
                    "plans": [],
                    "count": 0,
                    "message": "No learning plans found in plans/ directory"
                },
                duration=duration,
                metadata={
                    "skill": "learning-plan-manager",
                    "operation": "list_plans",
                    "version": "0.1.0"
                }
            )

        if response_format == "detailed":
            # Full metadata
            data = {
                "plans": plans,
                "count": len(plans)
            }
        else:  # summary
            # Just names and topics
            data = {
                "plans": [
                    {
                        "name": p["name"],
                        "topic": p["topic"],
                        "progress": p["progress"]
                    }
                    for p in plans
                ],
                "count": len(plans),
                "efficiency_tip": (
                    f"Found {len(plans)} learning plans.\n"
                    f"For full metadata: list_plans(response_format='detailed')"
                )
            }

        return OperationResult(
            success=True,
            data=data,
            duration=duration,
            metadata={
                "skill": "learning-plan-manager",
                "operation": "list_plans",
                "version": "0.1.0",
                "response_format": response_format
            }
        )

    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Failed to list plans: {str(e)}",
            error_code="LIST_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check if plans/ directory exists",
                    "Ensure you have read permissions",
                    f"Run: Bash('ls -la plans/') to see directory contents"
                ]
            }
        )


__all__ = [
    "load_plan",
    "find_latest_plan",
    "list_plans",
    "OperationResult"
]

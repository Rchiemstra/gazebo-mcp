"""
Learning Plan Manager

Main interface for learning plan operations.
"""

from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

from .models import (
    LearningPlan,
    TaskStatus,
    CheckpointStatus,
    JournalEntry,
    Task,
)
from .parser import LearningPlanParser
from .writer import LearningPlanWriter
from .validator import LearningPlanValidator, ValidationError


class LearningPlanManager:
    """
    Main interface for learning plan operations.

    Usage:
        manager = LearningPlanManager()
        plan = manager.load_plan("plans/my-learning-plan.md")
        progress = plan.calculate_progress()
        next_task = plan.get_next_task()
    """

    def __init__(self, plans_dir: Optional[Path] = None):
        """
        Initialize the manager.

        Args:
            plans_dir: Directory containing learning plans (default: ./plans)
        """
        self.plans_dir = plans_dir or Path("plans")
        self.parser = LearningPlanParser()
        self.writer = LearningPlanWriter()
        self.validator = LearningPlanValidator()

    # ===== READ OPERATIONS =====

    def load_plan(self, file_path: str | Path) -> LearningPlan:
        """
        Load and parse a learning plan from markdown.

        Args:
            file_path: Path to learning plan markdown file

        Returns:
            Parsed LearningPlan object

        Raises:
            FileNotFoundError: If plan file doesn't exist
            ValidationError: If plan format is invalid
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Learning plan not found: {path}")

        content = path.read_text()
        plan = self.parser.parse(content)
        plan.file_path = str(path)

        # Validate structure
        try:
            self.validator.validate(plan)
        except ValidationError as e:
            # Log warning but don't fail - plans may be in progress
            print(f"Warning: Plan validation issues: {e}")

        return plan

    def find_latest_plan(self) -> Optional[LearningPlan]:
        """
        Find the most recently updated learning plan.

        Returns:
            Latest LearningPlan or None if no plans exist
        """
        if not self.plans_dir.exists():
            return None

        plan_files = list(self.plans_dir.glob("*-learning-plan.md"))
        if not plan_files:
            return None

        # Sort by last modified time
        latest_file = max(plan_files, key=lambda p: p.stat().st_mtime)
        return self.load_plan(latest_file)

    def list_plans(self) -> List[Dict[str, Any]]:
        """
        List all available learning plans with metadata.

        Returns:
            List of plan summaries
        """
        if not self.plans_dir.exists():
            return []

        plans = []
        for plan_file in self.plans_dir.glob("*-learning-plan.md"):
            try:
                plan = self.load_plan(plan_file)
                progress = plan.calculate_progress()
                current_phase = plan.get_current_phase()

                plans.append(
                    {
                        "file": str(plan_file),
                        "title": plan.metadata.title,
                        "created": plan.metadata.created,
                        "updated": plan.metadata.last_updated,
                        "progress": progress["overall_percentage"],
                        "current_phase": current_phase.title
                        if current_phase
                        else None,
                        "estimated_time": plan.metadata.estimated_time,
                        "complexity": plan.metadata.complexity_level.value,
                    }
                )
            except Exception as e:
                # Log but don't fail on individual plan errors
                print(f"Warning: Could not load {plan_file}: {e}")

        return sorted(plans, key=lambda p: p["updated"], reverse=True)

    # ===== WRITE OPERATIONS =====

    def update_task_status(
        self,
        plan: LearningPlan,
        task_id: str,
        status: TaskStatus,
        notes: Optional[str] = None,
    ) -> LearningPlan:
        """
        Update a task's status.

        Args:
            plan: LearningPlan to update
            task_id: Task identifier
            status: New status
            notes: Optional notes about the update

        Returns:
            Updated LearningPlan
        """
        # Validate
        self.validator.validate_update(plan, {"task_id": task_id})

        # Find and update task
        for phase in plan.phases:
            for task in phase.tasks:
                if task.id == task_id:
                    task.status = status
                    if notes:
                        task.notes = notes
                    if status == TaskStatus.COMPLETED:
                        task.completed_at = datetime.now()
                    break

        plan.metadata.last_updated = datetime.now()

        # Update progress summary
        progress = plan.calculate_progress()
        current_phase = plan.get_current_phase()
        plan.metadata.progress_summary = (
            f"Progress: Phase {current_phase.number if current_phase else 'N/A'}, "
            f"{progress['overall_percentage']:.1f}% Complete"
        )

        return plan

    def update_checkpoint_status(
        self,
        plan: LearningPlan,
        checkpoint_id: str,
        status: CheckpointStatus,
        notes: Optional[str] = None,
    ) -> LearningPlan:
        """
        Update a checkpoint's status.

        Args:
            plan: LearningPlan to update
            checkpoint_id: Checkpoint identifier
            status: New status
            notes: Optional notes

        Returns:
            Updated LearningPlan
        """
        # Validate
        self.validator.validate_update(plan, {"checkpoint_id": checkpoint_id})

        # Find and update checkpoint
        for phase in plan.phases:
            for checkpoint in phase.checkpoints:
                if checkpoint.id == checkpoint_id:
                    checkpoint.status = status
                    if notes:
                        checkpoint.notes = notes
                    if status == CheckpointStatus.PASSED:
                        checkpoint.passed_at = datetime.now()
                    break

        plan.metadata.last_updated = datetime.now()
        return plan

    def add_journal_entry(
        self, plan: LearningPlan, entry: JournalEntry
    ) -> LearningPlan:
        """
        Add a new journal entry.

        Args:
            plan: LearningPlan to update
            entry: Journal entry to add

        Returns:
            Updated LearningPlan
        """
        plan.journal_entries.append(entry)
        plan.metadata.last_updated = datetime.now()
        return plan

    def mark_phase_started(self, plan: LearningPlan, phase_id: str) -> LearningPlan:
        """
        Mark a phase as started.

        Args:
            plan: LearningPlan to update
            phase_id: Phase identifier

        Returns:
            Updated LearningPlan
        """
        phase = plan._get_phase_by_id(phase_id)
        if phase and not phase.started_at:
            phase.started_at = datetime.now()
            plan.metadata.last_updated = datetime.now()
        return plan

    def mark_phase_completed(
        self, plan: LearningPlan, phase_id: str
    ) -> LearningPlan:
        """
        Mark a phase as completed.

        Args:
            plan: LearningPlan to update
            phase_id: Phase identifier

        Returns:
            Updated LearningPlan
        """
        phase = plan._get_phase_by_id(phase_id)
        if phase and not phase.completed_at:
            phase.completed_at = datetime.now()
            plan.metadata.last_updated = datetime.now()
        return plan

    def save_plan(self, plan: LearningPlan) -> Path:
        """
        Save plan back to markdown file.

        Args:
            plan: LearningPlan to save

        Returns:
            Path to saved file

        Raises:
            ValueError: If plan has no file_path set
        """
        if not plan.file_path:
            raise ValueError("Plan must have file_path set to save")

        markdown_content = self.writer.write(plan)
        path = Path(plan.file_path)

        # Ensure directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(markdown_content)
        return path

    # ===== QUERY OPERATIONS =====

    def get_phase_summary(self, plan: LearningPlan, phase_id: str) -> Dict[str, Any]:
        """
        Get detailed summary of a phase.

        Args:
            plan: LearningPlan
            phase_id: Phase identifier

        Returns:
            Dictionary with phase summary
        """
        phase = plan._get_phase_by_id(phase_id)
        if not phase:
            return {}

        return {
            "id": phase.id,
            "number": phase.number,
            "title": phase.title,
            "duration": phase.duration,
            "started": phase.started_at,
            "completed": phase.completed_at,
            "learning_goals": phase.learning_goals,
            "tasks": {
                "total": len(phase.tasks),
                "completed": sum(
                    1 for t in phase.tasks if t.status == TaskStatus.COMPLETED
                ),
                "in_progress": sum(
                    1 for t in phase.tasks if t.status == TaskStatus.IN_PROGRESS
                ),
                "not_started": sum(
                    1 for t in phase.tasks if t.status == TaskStatus.NOT_STARTED
                ),
            },
            "checkpoints": {
                "total": len(phase.checkpoints),
                "passed": sum(
                    1 for c in phase.checkpoints if c.status == CheckpointStatus.PASSED
                ),
            },
            "specialists": phase.specialist_support,
        }

    def search_tasks(self, plan: LearningPlan, query: str) -> List[Task]:
        """
        Search for tasks matching query.

        Args:
            plan: LearningPlan to search
            query: Search query string

        Returns:
            List of matching tasks
        """
        results = []
        query_lower = query.lower()

        for phase in plan.phases:
            for task in phase.tasks:
                if query_lower in task.title.lower() or query_lower in task.description.lower():
                    results.append(task)

        return results

    # ===== EXPORT OPERATIONS =====

    def export_json(self, plan: LearningPlan) -> str:
        """
        Export plan as JSON.

        Args:
            plan: LearningPlan to export

        Returns:
            JSON string
        """
        return plan.model_dump_json(indent=2)

    def export_progress_report(self, plan: LearningPlan) -> str:
        """
        Generate a human-readable progress report.

        Args:
            plan: LearningPlan to report on

        Returns:
            Markdown progress report
        """
        progress = plan.calculate_progress()
        current_phase = plan.get_current_phase()
        next_task = plan.get_next_task()

        report = f"""# Learning Progress Report

## {plan.metadata.title}

**Last Updated**: {plan.metadata.last_updated.strftime("%Y-%m-%d %H:%M")}
**Estimated Time**: {plan.metadata.estimated_time}
**Complexity**: {plan.metadata.complexity_level.value.title()}

## Overall Progress: {progress['overall_percentage']:.1f}%

### Phases: {progress['phases']['completed']}/{progress['phases']['total']} ({progress['phases']['percentage']:.1f}%)
### Tasks: {progress['tasks']['completed']}/{progress['tasks']['total']} ({progress['tasks']['percentage']:.1f}%)
### Checkpoints: {progress['checkpoints']['passed']}/{progress['checkpoints']['total']} ({progress['checkpoints']['percentage']:.1f}%)

## Current Status

"""
        if current_phase:
            report += f"**Current Phase**: Phase {current_phase.number} - {current_phase.title}\n\n"

        if next_task:
            report += f"**Next Task**: {next_task.title}\n\n"

        # Add phase breakdown
        report += "## Phase Breakdown\n\n"
        for phase in plan.phases:
            status_icon = (
                "✅" if phase.completed_at else "🔄" if phase.started_at else "⏳"
            )
            report += f"### {status_icon} Phase {phase.number}: {phase.title}\n\n"

            phase_summary = self.get_phase_summary(plan, phase.id)
            report += f"- Tasks: {phase_summary['tasks']['completed']}/{phase_summary['tasks']['total']}\n"
            report += f"- Checkpoints: {phase_summary['checkpoints']['passed']}/{phase_summary['checkpoints']['total']}\n"
            if phase.started_at:
                report += (
                    f"- Started: {phase.started_at.strftime('%Y-%m-%d')}\n"
                )
            if phase.completed_at:
                report += f"- Completed: {phase.completed_at.strftime('%Y-%m-%d')}\n"
            report += "\n"

        return report

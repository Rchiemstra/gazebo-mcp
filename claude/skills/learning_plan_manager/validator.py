"""
Learning Plan Validator

Validates learning plan structure and content.
"""

from typing import List
from .models import LearningPlan, Phase


class ValidationError(Exception):
    """Raised when learning plan validation fails"""

    pass


class LearningPlanValidator:
    """Validates learning plan structure"""

    def validate(self, plan: LearningPlan) -> None:
        """
        Validate plan structure.

        Args:
            plan: LearningPlan to validate

        Raises:
            ValidationError: If plan is invalid
        """
        errors = []

        # Validate metadata
        if not plan.metadata.title:
            errors.append("Plan must have a title")

        if not plan.metadata.estimated_time:
            errors.append("Plan must have estimated learning time")

        # Validate phases
        if not plan.phases:
            errors.append("Plan must have at least one phase")
        else:
            errors.extend(self._validate_phases(plan.phases))

        # Validate learning objectives
        if not plan.learning_objectives:
            errors.append("Plan must have learning objectives")

        # Raise if any errors
        if errors:
            error_msg = "Learning plan validation failed:\n" + "\n".join(
                f"  - {error}" for error in errors
            )
            raise ValidationError(error_msg)

    def _validate_phases(self, phases: List[Phase]) -> List[str]:
        """Validate phase structure"""
        errors = []

        # Check phase numbering
        expected_number = 1
        for phase in phases:
            if phase.number != expected_number:
                errors.append(
                    f"Phase numbering error: expected {expected_number}, got {phase.number}"
                )
            expected_number += 1

        # Check each phase has content
        for phase in phases:
            if not phase.title:
                errors.append(f"Phase {phase.number} must have a title")

            if not phase.learning_goals:
                errors.append(f"Phase {phase.number} should have learning goals")

            # Warn if no tasks (not an error, might be planning phase)
            if not phase.tasks:
                errors.append(
                    f"Warning: Phase {phase.number} has no tasks (this may be intentional)"
                )

        return errors

    def validate_update(self, plan: LearningPlan, changes: dict) -> None:
        """
        Validate that proposed changes are valid.

        Args:
            plan: Current plan
            changes: Proposed changes

        Raises:
            ValidationError: If changes are invalid
        """
        errors = []

        # Validate task ID exists if updating task
        if "task_id" in changes:
            task_id = changes["task_id"]
            found = False
            for phase in plan.phases:
                for task in phase.tasks:
                    if task.id == task_id:
                        found = True
                        break
                if found:
                    break

            if not found:
                errors.append(f"Task ID not found: {task_id}")

        # Validate checkpoint ID exists if updating checkpoint
        if "checkpoint_id" in changes:
            checkpoint_id = changes["checkpoint_id"]
            found = False
            for phase in plan.phases:
                for checkpoint in phase.checkpoints:
                    if checkpoint.id == checkpoint_id:
                        found = True
                        break
                if found:
                    break

            if not found:
                errors.append(f"Checkpoint ID not found: {checkpoint_id}")

        if errors:
            error_msg = "Update validation failed:\n" + "\n".join(
                f"  - {error}" for error in errors
            )
            raise ValidationError(error_msg)

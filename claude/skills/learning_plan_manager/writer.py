"""
Learning Plan Writer

Writes LearningPlan objects back to markdown format.
"""

from typing import List
from .models import (
    LearningPlan,
    Phase,
    Task,
    Checkpoint,
    TaskStatus,
    CheckpointStatus,
)


class LearningPlanWriter:
    """Writes LearningPlan objects back to markdown"""

    def write(self, plan: LearningPlan) -> str:
        """
        Convert LearningPlan to markdown.

        Args:
            plan: LearningPlan object to convert

        Returns:
            Markdown string
        """
        sections = []

        # Title and metadata
        sections.append(self._write_header(plan))

        # Learning objectives
        sections.append(self._write_learning_objectives(plan))

        # Prerequisites
        sections.append(self._write_prerequisites(plan))

        # Phases
        sections.append(self._write_phases(plan))

        # Learning team
        if plan.learning_team:
            sections.append(self._write_learning_team(plan))

        # Milestones
        if plan.milestones:
            sections.append(self._write_milestones(plan))

        # Journal entries
        if plan.journal_entries:
            sections.append(self._write_journal_entries(plan))

        # Resources
        if plan.resources:
            sections.append(self._write_resources(plan))

        # Common pitfalls
        if plan.common_pitfalls:
            sections.append(self._write_common_pitfalls(plan))

        return "\n\n".join(sections) + "\n"

    def _write_header(self, plan: LearningPlan) -> str:
        """Write title and metadata"""
        lines = [
            f"# {plan.metadata.title}",
            "",
            f"**Created**: {plan.metadata.created.strftime('%Y-%m-%d')}",
            f"**Estimated Learning Time**: {plan.metadata.estimated_time}",
            f"**Complexity Level**: {plan.metadata.complexity_level.value.title()}",
        ]

        # Add last updated with progress if available
        updated_line = f"**Last Updated**: {plan.metadata.last_updated.strftime('%Y-%m-%d')}"
        if plan.metadata.progress_summary:
            updated_line += f" ({plan.metadata.progress_summary})"
        lines.append(updated_line)

        lines.append("")
        lines.append("---")

        return "\n".join(lines)

    def _write_learning_objectives(self, plan: LearningPlan) -> str:
        """Write learning objectives section"""
        lines = [
            "## 🎯 Learning Objectives",
            "",
        ]

        # What You'll Learn
        if "what_you_will_learn" in plan.learning_objectives:
            lines.append("### What You'll Learn")
            lines.append("")
            for item in plan.learning_objectives["what_you_will_learn"]:
                lines.append(f"- {item}")
            lines.append("")

        # Skills You'll Develop
        if "skills_you_will_develop" in plan.learning_objectives:
            lines.append("### Skills You'll Develop")
            lines.append("")
            for item in plan.learning_objectives["skills_you_will_develop"]:
                lines.append(f"- {item}")
            lines.append("")

        # Outcomes
        if "outcomes" in plan.learning_objectives:
            lines.append("### Outcomes")
            lines.append("")
            for item in plan.learning_objectives["outcomes"]:
                lines.append(f"- {item}")
            lines.append("")

        lines.append("---")

        return "\n".join(lines)

    def _write_prerequisites(self, plan: LearningPlan) -> str:
        """Write prerequisites section"""
        if not plan.prerequisites:
            return ""

        lines = [
            "## 📋 Prerequisites Check",
            "",
            "Before starting, you should understand:",
        ]

        for prereq in plan.prerequisites:
            checkbox = "[x]" if prereq.completed else "[ ]"
            line = f"- {checkbox} {prereq.description}"
            lines.append(line)
            if prereq.context:
                lines.append(f"  - {prereq.context}")

        lines.append("")
        lines.append("---")

        return "\n".join(lines)

    def _write_phases(self, plan: LearningPlan) -> str:
        """Write all phases"""
        lines = [
            "## 📚 Learning Phases",
            "",
        ]

        for phase in plan.phases:
            lines.extend(self._write_phase(phase))
            lines.append("")
            lines.append("---")
            lines.append("")

        return "\n".join(lines)

    def _write_phase(self, phase: Phase) -> List[str]:
        """Write a single phase"""
        # Phase header
        lines = []

        # Add duration to title if present
        title = phase.title
        if phase.duration:
            title += f" ({phase.duration})"

        lines.append(f"## Phase {phase.number}: {title}")
        lines.append("")

        # Status indicators
        if phase.completed_at:
            lines.append(f"✅ **Status**: Completed on {phase.completed_at.strftime('%Y-%m-%d')}")
        elif phase.started_at:
            lines.append(f"🔄 **Status**: In Progress (started {phase.started_at.strftime('%Y-%m-%d')})")
        else:
            lines.append("⏳ **Status**: Not Started")

        lines.append("")

        # Learning goals
        if phase.learning_goals:
            lines.append("### Learning Goals")
            lines.append("")
            for goal in phase.learning_goals:
                lines.append(f"- {goal}")
            lines.append("")

        # Tasks
        if phase.tasks:
            lines.append("### Tasks")
            lines.append("")
            for task in phase.tasks:
                lines.extend(self._write_task(task))
                lines.append("")

        # Checkpoints
        if phase.checkpoints:
            for checkpoint in phase.checkpoints:
                lines.extend(self._write_checkpoint(checkpoint))
                lines.append("")

        # Specialist support
        if phase.specialist_support:
            lines.append("### Specialist Support")
            lines.append("")
            for agent, role in phase.specialist_support.items():
                lines.append(f"- **{agent}**: {role}")
            lines.append("")

        return lines

    def _write_task(self, task: Task) -> List[str]:
        """Write a single task"""
        lines = []

        # Task header with status emoji
        status_emoji = {
            TaskStatus.COMPLETED: "✅",
            TaskStatus.IN_PROGRESS: "🔄",
            TaskStatus.BLOCKED: "🚫",
            TaskStatus.SKIPPED: "⏭️",
            TaskStatus.NOT_STARTED: "⏳",
        }

        emoji = status_emoji.get(task.status, "⏳")
        lines.append(f"#### {emoji} {task.title}")
        lines.append("")

        # Description
        if task.description:
            lines.append(task.description)
            lines.append("")

        # Learning activity
        if task.learning_activity:
            lines.append(f"**Learning Activity**: {task.learning_activity}")
            lines.append("")

        # Research questions
        if task.research_questions:
            lines.append("**Research Questions**:")
            for question in task.research_questions:
                lines.append(f"- {question}")
            lines.append("")

        # Checkpoint questions
        if task.checkpoint_questions:
            lines.append("**Checkpoint Questions**:")
            for question in task.checkpoint_questions:
                lines.append(f"- {question}")
            lines.append("")

        # Specialist agents
        if task.specialist_agents:
            agents_str = ", ".join(task.specialist_agents)
            lines.append(f"**Consult**: {agents_str}")
            lines.append("")

        # Notes
        if task.notes:
            lines.append(f"**Notes**: {task.notes}")
            lines.append("")

        # Completion time
        if task.completed_at:
            lines.append(f"**Completed**: {task.completed_at.strftime('%Y-%m-%d %H:%M')}")
            lines.append("")

        return lines

    def _write_checkpoint(self, checkpoint: Checkpoint) -> List[str]:
        """Write an understanding checkpoint"""
        lines = []

        # Status icon
        status_icon = {
            CheckpointStatus.PASSED: "✅",
            CheckpointStatus.IN_REVIEW: "🔍",
            CheckpointStatus.NEEDS_WORK: "⚠️",
            CheckpointStatus.NOT_REACHED: "⏳",
        }

        icon = status_icon.get(checkpoint.status, "⏳")
        lines.append(f"### {icon} Understanding Checkpoint")
        lines.append("")

        lines.append("Before moving to the next phase, verify you can:")
        lines.append("")

        for i, question in enumerate(checkpoint.questions, 1):
            lines.append(f"{i}. {question}")

        lines.append("")

        if checkpoint.notes:
            lines.append(f"**Notes**: {checkpoint.notes}")
            lines.append("")

        if checkpoint.passed_at:
            lines.append(f"**Passed**: {checkpoint.passed_at.strftime('%Y-%m-%d')}")
            lines.append("")

        return lines

    def _write_learning_team(self, plan: LearningPlan) -> str:
        """Write learning team section"""
        lines = [
            "## 👥 Learning Team - Who Can Help",
            "",
        ]

        for agent, role in plan.learning_team.items():
            lines.append(f"### {agent}")
            lines.append(f"- {role}")
            lines.append("")

        lines.append("---")

        return "\n".join(lines)

    def _write_milestones(self, plan: LearningPlan) -> str:
        """Write milestones section"""
        lines = [
            "## 🎓 Learning Milestones",
            "",
        ]

        for milestone in plan.milestones:
            lines.append(f"- {milestone}")

        lines.append("")
        lines.append("---")

        return "\n".join(lines)

    def _write_journal_entries(self, plan: LearningPlan) -> str:
        """Write journal entries section"""
        lines = [
            "## 📝 Learning Journal",
            "",
        ]

        for entry in plan.journal_entries:
            lines.append(entry.raw_content)
            lines.append("")

        lines.append("---")

        return "\n".join(lines)

    def _write_resources(self, plan: LearningPlan) -> str:
        """Write resources section"""
        lines = [
            "## 🔗 Resources",
            "",
        ]

        for resource in plan.resources:
            lines.append(f"- {resource}")

        lines.append("")
        lines.append("---")

        return "\n".join(lines)

    def _write_common_pitfalls(self, plan: LearningPlan) -> str:
        """Write common pitfalls section"""
        lines = [
            "## ⚠️ Common Pitfalls to Avoid",
            "",
        ]

        for i, pitfall in enumerate(plan.common_pitfalls, 1):
            lines.append(f"### {i}. {pitfall}")
            lines.append("")

        lines.append("---")

        return "\n".join(lines)

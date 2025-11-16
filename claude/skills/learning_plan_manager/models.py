"""
Data models for learning plans.

Pydantic models representing the structure of learning plan markdown files.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Task completion status"""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"


class CheckpointStatus(str, Enum):
    """Understanding checkpoint status"""

    NOT_REACHED = "not_reached"
    IN_REVIEW = "in_review"
    PASSED = "passed"
    NEEDS_WORK = "needs_work"


class ComplexityLevel(str, Enum):
    """Learning complexity"""

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class Task(BaseModel):
    """Individual learning task"""

    id: str = Field(description="Unique task identifier")
    title: str = Field(description="Task title")
    description: str = Field(description="Task description/instructions")
    status: TaskStatus = TaskStatus.NOT_STARTED
    learning_activity: Optional[str] = None
    research_questions: List[str] = Field(default_factory=list)
    checkpoint_questions: List[str] = Field(default_factory=list)
    specialist_agents: List[str] = Field(default_factory=list)
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None


class Checkpoint(BaseModel):
    """Understanding checkpoint"""

    id: str = Field(description="Unique checkpoint identifier")
    title: str = Field(description="Checkpoint title")
    questions: List[str] = Field(description="Questions to verify understanding")
    status: CheckpointStatus = CheckpointStatus.NOT_REACHED
    passed_at: Optional[datetime] = None
    notes: Optional[str] = None


class Phase(BaseModel):
    """Learning phase"""

    id: str = Field(description="Unique phase identifier")
    number: int = Field(description="Phase number (1-based)")
    title: str = Field(description="Phase title")
    duration: Optional[str] = Field(description="e.g., 'Week 1-2'")
    learning_goals: List[str] = Field(default_factory=list)
    tasks: List[Task] = Field(default_factory=list)
    checkpoints: List[Checkpoint] = Field(default_factory=list)
    specialist_support: Dict[str, str] = Field(
        default_factory=dict,
        description="Map of specialist name to their role in this phase",
    )
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class JournalEntry(BaseModel):
    """Learning journal entry"""

    id: str = Field(description="Unique entry identifier")
    date: datetime = Field(default_factory=datetime.now)
    session_number: Optional[int] = None
    concepts_explored: Optional[str] = None
    key_insights: Optional[str] = None
    challenges: Optional[str] = None
    practice_done: Optional[str] = None
    questions_for_next_time: List[str] = Field(default_factory=list)
    raw_content: str = Field(description="Full markdown content")


class Prerequisite(BaseModel):
    """Prerequisite check item"""

    description: str
    completed: bool = False
    context: Optional[str] = None


class LearningPlanMetadata(BaseModel):
    """Plan header metadata"""

    title: str
    created: datetime
    last_updated: datetime
    estimated_time: str
    complexity_level: ComplexityLevel
    progress_summary: Optional[str] = None


class LearningPlan(BaseModel):
    """Complete learning plan structure"""

    metadata: LearningPlanMetadata
    learning_objectives: Dict[str, List[str]] = Field(
        description="Categories: 'what_you_will_learn', 'skills_you_will_develop', 'outcomes'"
    )
    prerequisites: List[Prerequisite] = Field(default_factory=list)
    phases: List[Phase] = Field(default_factory=list)
    learning_team: Dict[str, str] = Field(
        default_factory=dict, description="Map of agent name to their role"
    )
    milestones: List[str] = Field(default_factory=list)
    journal_entries: List[JournalEntry] = Field(default_factory=list)
    resources: List[str] = Field(default_factory=list)
    common_pitfalls: List[str] = Field(default_factory=list)
    file_path: Optional[str] = Field(default=None, description="Path to source markdown file")

    def get_current_phase(self) -> Optional[Phase]:
        """Get the currently active phase"""
        for phase in self.phases:
            if phase.started_at and not phase.completed_at:
                return phase
            # If no started phases, return first incomplete
            if not phase.started_at:
                return phase
        return None

    def get_next_task(self, phase_id: Optional[str] = None) -> Optional[Task]:
        """Get the next task to work on"""
        target_phase = (
            self.get_current_phase()
            if not phase_id
            else self._get_phase_by_id(phase_id)
        )
        if not target_phase:
            return None

        for task in target_phase.tasks:
            if task.status in [TaskStatus.NOT_STARTED, TaskStatus.IN_PROGRESS]:
                return task
        return None

    def calculate_progress(self) -> Dict[str, Any]:
        """Calculate progress statistics"""
        total_phases = len(self.phases)
        completed_phases = sum(1 for p in self.phases if p.completed_at)

        total_tasks = sum(len(p.tasks) for p in self.phases)
        completed_tasks = sum(
            sum(1 for t in p.tasks if t.status == TaskStatus.COMPLETED)
            for p in self.phases
        )

        total_checkpoints = sum(len(p.checkpoints) for p in self.phases)
        passed_checkpoints = sum(
            sum(1 for c in p.checkpoints if c.status == CheckpointStatus.PASSED)
            for p in self.phases
        )

        return {
            "phases": {
                "total": total_phases,
                "completed": completed_phases,
                "percentage": (completed_phases / total_phases * 100)
                if total_phases
                else 0,
            },
            "tasks": {
                "total": total_tasks,
                "completed": completed_tasks,
                "percentage": (completed_tasks / total_tasks * 100)
                if total_tasks
                else 0,
            },
            "checkpoints": {
                "total": total_checkpoints,
                "passed": passed_checkpoints,
                "percentage": (passed_checkpoints / total_checkpoints * 100)
                if total_checkpoints
                else 0,
            },
            "overall_percentage": (
                (
                    completed_tasks / total_tasks * 0.7
                    + passed_checkpoints / total_checkpoints * 0.3
                )
                * 100
                if total_tasks and total_checkpoints
                else 0
            ),
        }

    def _get_phase_by_id(self, phase_id: str) -> Optional[Phase]:
        """Helper to find phase by ID"""
        return next((p for p in self.phases if p.id == phase_id), None)

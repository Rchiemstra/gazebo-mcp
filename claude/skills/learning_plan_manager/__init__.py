"""
Learning Plan Manager Skill

Provides structured operations on learning plan markdown files.
Parse, query, update, and export learning plans without manual markdown manipulation.
"""

from .models import (
    TaskStatus,
    CheckpointStatus,
    ComplexityLevel,
    Task,
    Checkpoint,
    Phase,
    JournalEntry,
    Prerequisite,
    LearningPlanMetadata,
    LearningPlan,
)
from .manager import LearningPlanManager
from .parser import LearningPlanParser
from .writer import LearningPlanWriter
from .validator import LearningPlanValidator

# Import operations for agent invocation
from .operations import load_plan, find_latest_plan, list_plans, OperationResult

__all__ = [
    # Enums
    "TaskStatus",
    "CheckpointStatus",
    "ComplexityLevel",
    # Models
    "Task",
    "Checkpoint",
    "Phase",
    "JournalEntry",
    "Prerequisite",
    "LearningPlanMetadata",
    "LearningPlan",
    # Main classes
    "LearningPlanManager",
    "LearningPlanParser",
    "LearningPlanWriter",
    "LearningPlanValidator",
    # Operations (agent-friendly interface)
    "load_plan",
    "find_latest_plan",
    "list_plans",
    "OperationResult",
]

__version__ = "0.1.0"

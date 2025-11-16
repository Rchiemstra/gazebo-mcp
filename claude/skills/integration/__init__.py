"""
Skills Integration Layer

Provides standardized interface for agents to interact with skills.
"""

from .skill_registry import SkillRegistry, SkillMetadata
from .skill_loader import SkillLoader, SkillInstance
from .skill_invoker import SkillInvoker, SkillRequest, SkillResult, SkillError

__all__ = [
    "SkillRegistry",
    "SkillMetadata",
    "SkillLoader",
    "SkillInstance",
    "SkillInvoker",
    "SkillRequest",
    "SkillResult",
    "SkillError",
]

__version__ = "1.0.0"

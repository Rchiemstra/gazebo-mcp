"""Data models for Claude Learning System."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, List, Any
from enum import Enum


class AgentType(Enum):
    """Available teaching specialist agents."""

    LEARNING_COORDINATOR = "learning-coordinator"
    PLAN_GENERATION_MENTOR = "plan-generation-mentor"
    ROS2_LEARNING_MENTOR = "ros2-learning-mentor"
    CODE_ARCHITECTURE_MENTOR = "code-architecture-mentor"
    ROBOTICS_VISION_NAVIGATOR = "robotics-vision-navigator"
    JETANK_HARDWARE_SPECIALIST = "jetank-hardware-specialist"
    PYTHON_BEST_PRACTICES = "python-best-practices"
    CPP_BEST_PRACTICES = "cpp-best-practices"
    DEBUGGING_DETECTIVE = "debugging-detective"
    TESTING_SPECIALIST = "testing-specialist"
    GIT_WORKFLOW_EXPERT = "git-workflow-expert"
    DOCUMENTATION_GENERATOR = "documentation-generator"
    FILE_SEARCH_AGENT = "file-search-agent"
    PROJECT_PLAN_ORCHESTRATOR = "project-plan-orchestrator"


class LearningPhase(Enum):
    """Learning plan phases."""

    RESEARCH = "research"
    DESIGN = "design"
    IMPLEMENT = "implement"
    REFLECT = "reflect"


@dataclass
class AgentResponse:
    """Response from an agent interaction."""

    content: str
    agent_type: AgentType
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    tool_uses: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class LearningSession:
    """Represents a learning session."""

    topic: str
    session_id: str
    agent_type: AgentType
    started_at: datetime = field(default_factory=datetime.now)
    current_phase: Optional[LearningPhase] = None
    messages: List[AgentResponse] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    completed: bool = False
    git_branch: Optional[str] = None
    last_committed_phase: Optional[LearningPhase] = None
    phase_commits: List[Dict[str, Any]] = field(default_factory=list)

    def add_response(self, response: AgentResponse) -> None:
        """Add a response to the session."""
        self.messages.append(response)

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get formatted conversation history."""
        return [
            {"role": "assistant", "content": msg.content, "timestamp": msg.timestamp.isoformat()}
            for msg in self.messages
        ]

    def record_phase_commit(self, phase: LearningPhase, commit_hash: Optional[str] = None) -> None:
        """Record that a phase was committed."""
        self.last_committed_phase = phase
        self.phase_commits.append({
            "phase": phase.value,
            "timestamp": datetime.now().isoformat(),
            "commit_hash": commit_hash,
        })


@dataclass
class PlanMetadata:
    """Metadata for a learning plan."""

    topic: str
    created_at: datetime
    estimated_duration: str
    phases: List[LearningPhase]
    current_phase: Optional[LearningPhase] = None
    completion_percentage: int = 0

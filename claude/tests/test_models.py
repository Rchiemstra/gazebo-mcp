"""Tests for data models."""

import pytest
from datetime import datetime
from claude_learning.models import (
    AgentType,
    LearningPhase,
    AgentResponse,
    LearningSession,
    PlanMetadata,
)


def test_agent_type_enum():
    """Test AgentType enum values."""
    assert AgentType.LEARNING_COORDINATOR.value == "learning-coordinator"
    assert AgentType.ROS2_LEARNING_MENTOR.value == "ros2-learning-mentor"
    assert AgentType.CODE_ARCHITECTURE_MENTOR.value == "code-architecture-mentor"


def test_learning_phase_enum():
    """Test LearningPhase enum values."""
    assert LearningPhase.RESEARCH.value == "research"
    assert LearningPhase.DESIGN.value == "design"
    assert LearningPhase.IMPLEMENT.value == "implement"
    assert LearningPhase.REFLECT.value == "reflect"


def test_agent_response_creation():
    """Test creating an AgentResponse."""
    response = AgentResponse(
        content="This is a teaching response",
        agent_type=AgentType.PYTHON_BEST_PRACTICES,
        metadata={"topic": "async programming"},
    )

    assert response.content == "This is a teaching response"
    assert response.agent_type == AgentType.PYTHON_BEST_PRACTICES
    assert response.metadata["topic"] == "async programming"
    assert isinstance(response.timestamp, datetime)
    assert response.tool_uses == []


def test_learning_session_creation():
    """Test creating a LearningSession."""
    session = LearningSession(
        topic="ROS2 Navigation",
        session_id="test-123",
        agent_type=AgentType.ROBOTICS_VISION_NAVIGATOR,
        current_phase=LearningPhase.RESEARCH,
    )

    assert session.topic == "ROS2 Navigation"
    assert session.session_id == "test-123"
    assert session.agent_type == AgentType.ROBOTICS_VISION_NAVIGATOR
    assert session.current_phase == LearningPhase.RESEARCH
    assert session.completed is False
    assert len(session.messages) == 0


def test_learning_session_add_response():
    """Test adding responses to a session."""
    session = LearningSession(
        topic="Test Topic",
        session_id="test-456",
        agent_type=AgentType.LEARNING_COORDINATOR,
    )

    response1 = AgentResponse(
        content="First response",
        agent_type=AgentType.LEARNING_COORDINATOR,
    )
    response2 = AgentResponse(
        content="Second response",
        agent_type=AgentType.LEARNING_COORDINATOR,
    )

    session.add_response(response1)
    session.add_response(response2)

    assert len(session.messages) == 2
    assert session.messages[0].content == "First response"
    assert session.messages[1].content == "Second response"


def test_learning_session_conversation_history():
    """Test getting conversation history."""
    session = LearningSession(
        topic="Test Topic",
        session_id="test-789",
        agent_type=AgentType.LEARNING_COORDINATOR,
    )

    response = AgentResponse(
        content="Test message",
        agent_type=AgentType.LEARNING_COORDINATOR,
    )
    session.add_response(response)

    history = session.get_conversation_history()

    assert len(history) == 1
    assert history[0]["role"] == "assistant"
    assert history[0]["content"] == "Test message"
    assert "timestamp" in history[0]


def test_plan_metadata_creation():
    """Test creating PlanMetadata."""
    metadata = PlanMetadata(
        topic="Autonomous Navigation",
        created_at=datetime.now(),
        estimated_duration="6-8 weeks",
        phases=[LearningPhase.RESEARCH, LearningPhase.DESIGN],
        current_phase=LearningPhase.RESEARCH,
        completion_percentage=25,
    )

    assert metadata.topic == "Autonomous Navigation"
    assert metadata.estimated_duration == "6-8 weeks"
    assert len(metadata.phases) == 2
    assert metadata.current_phase == LearningPhase.RESEARCH
    assert metadata.completion_percentage == 25

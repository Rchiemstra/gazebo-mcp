"""Tests for AgentClient."""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from claude_learning import AgentClient, AgentConfig, AgentType, LearningPhase
from claude_learning.models import LearningSession


@pytest.fixture
def mock_config(tmp_path):
    """Create a mock configuration for testing."""
    # Create agent files
    agents_dir = tmp_path / "agents"
    agents_dir.mkdir()

    test_agent = agents_dir / "learning-coordinator.md"
    test_agent.write_text("# Learning Coordinator\n\nYou are a teaching mentor.")

    return AgentConfig(
        api_key="test-api-key",
        agents_dir=agents_dir,
        workspace_root=tmp_path,
    )


@pytest.fixture
def client(mock_config):
    """Create an AgentClient for testing."""
    return AgentClient(mock_config)


def test_client_initialization(client, mock_config):
    """Test client initialization."""
    assert client.config == mock_config
    assert len(client._active_sessions) == 0


def test_get_sdk_options(client):
    """Test SDK options creation."""
    options = client._get_sdk_options(
        system_prompt="Test prompt",
        custom_tools=["Read", "Write"],
    )

    assert options.model == "claude-sonnet-4-5-20250929"
    assert options.system_prompt == "Test prompt"
    assert options.allowed_tools == ["Read", "Write"]
    assert options.permission_mode == "ask"


@pytest.mark.asyncio
async def test_start_learning_session(client):
    """Test starting a new learning session."""
    session = await client.start_learning_session(
        topic="Test Topic",
        agent_type=AgentType.LEARNING_COORDINATOR,
        initial_phase=LearningPhase.RESEARCH,
    )

    assert isinstance(session, LearningSession)
    assert session.topic == "Test Topic"
    assert session.agent_type == AgentType.LEARNING_COORDINATOR
    assert session.current_phase == LearningPhase.RESEARCH
    assert session.session_id in client._active_sessions


def test_get_session(client):
    """Test retrieving a session by ID."""
    # Manually add a session
    session = LearningSession(
        topic="Test",
        session_id="test-123",
        agent_type=AgentType.LEARNING_COORDINATOR,
    )
    client._active_sessions["test-123"] = session

    retrieved = client.get_session("test-123")
    assert retrieved == session

    # Test non-existent session
    assert client.get_session("nonexistent") is None


def test_list_active_sessions(client):
    """Test listing active sessions."""
    # Add multiple sessions
    session1 = LearningSession(
        topic="Topic 1",
        session_id="id-1",
        agent_type=AgentType.LEARNING_COORDINATOR,
    )
    session2 = LearningSession(
        topic="Topic 2",
        session_id="id-2",
        agent_type=AgentType.ROS2_LEARNING_MENTOR,
    )

    client._active_sessions["id-1"] = session1
    client._active_sessions["id-2"] = session2

    sessions = client.list_active_sessions()
    assert len(sessions) == 2
    assert session1 in sessions
    assert session2 in sessions


def test_close_session(client):
    """Test closing a session."""
    session = LearningSession(
        topic="Test",
        session_id="close-test",
        agent_type=AgentType.LEARNING_COORDINATOR,
    )
    client._active_sessions["close-test"] = session

    client.close_session("close-test")

    assert "close-test" not in client._active_sessions
    assert session.completed is True

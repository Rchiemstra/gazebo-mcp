"""Tests for configuration management."""

import os
import pytest
from pathlib import Path
from claude_learning.config import AgentConfig


def test_config_from_env(monkeypatch):
    """Test configuration from environment variables."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-123")
    monkeypatch.setenv("CLAUDE_MODEL", "claude-sonnet-4-5-20250929")
    monkeypatch.setenv("MAX_TOKENS", "4096")

    config = AgentConfig.from_env()

    assert config.api_key == "test-key-123"
    assert config.model == "claude-sonnet-4-5-20250929"
    assert config.max_tokens == 4096


def test_config_explicit_api_key():
    """Test configuration with explicit API key."""
    config = AgentConfig(api_key="explicit-key-456")

    assert config.api_key == "explicit-key-456"
    assert config.model == "claude-sonnet-4-5-20250929"  # Default


def test_config_missing_api_key(monkeypatch):
    """Test that missing API key raises error."""
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    with pytest.raises(ValueError, match="ANTHROPIC_API_KEY not found"):
        AgentConfig()


def test_agent_path_resolution():
    """Test agent file path resolution."""
    config = AgentConfig(api_key="test-key")

    agent_path = config.get_agent_path("ros2-learning-mentor")
    assert agent_path == config.agents_dir / "ros2-learning-mentor.md"


def test_command_path_resolution():
    """Test command file path resolution."""
    config = AgentConfig(api_key="test-key")

    command_path = config.get_command_path("create-plan")
    assert command_path == config.commands_dir / "create-plan.md"


def test_load_agent_prompt(tmp_path):
    """Test loading agent prompt from file."""
    # Create a temporary agents directory
    agents_dir = tmp_path / "agents"
    agents_dir.mkdir()

    # Create a test agent file
    test_agent = agents_dir / "test-agent.md"
    test_content = "# Test Agent\n\nThis is a test agent prompt."
    test_agent.write_text(test_content)

    # Create config with custom agents directory
    config = AgentConfig(
        api_key="test-key",
        agents_dir=agents_dir
    )

    # Load the prompt
    loaded_content = config.load_agent_prompt("test-agent")
    assert loaded_content == test_content


def test_load_missing_agent_prompt():
    """Test that loading missing agent raises error."""
    config = AgentConfig(api_key="test-key")

    with pytest.raises(FileNotFoundError):
        config.load_agent_prompt("nonexistent-agent")

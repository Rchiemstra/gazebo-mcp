"""Configuration management for Claude Learning System."""

import os
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass, field
from dotenv import load_dotenv
from enum import Enum

# Load environment variables
load_dotenv()


class ClientMode(Enum):
    """Execution mode for Claude client."""
    API = "api"  # Use Claude API directly
    CLI = "cli"  # Use Claude Code CLI
    AUTO = "auto"  # Start with API, fallback to CLI on quota exhaustion


@dataclass
class AgentConfig:
    """Configuration for Claude Agent SDK."""

    api_key: Optional[str] = None
    model: str = "claude-sonnet-4-5-20250929"
    max_tokens: int = 8192
    temperature: float = 1.0
    allowed_tools: List[str] = field(
        default_factory=lambda: [
            "Read",
            "Write",
            "Edit",
            "Bash",
            "Glob",
            "Grep",
            "WebFetch",
            "WebSearch",
        ]
    )
    permission_mode: str = "ask"
    workspace_root: Path = field(default_factory=lambda: Path.cwd())
    agents_dir: Path = field(default_factory=lambda: Path.cwd() / "agents")
    commands_dir: Path = field(default_factory=lambda: Path.cwd() / "commands")
    plans_dir: Path = field(default_factory=lambda: Path.cwd() / "plans")
    client_mode: ClientMode = ClientMode.AUTO
    cli_executable: str = "claude"  # Claude Code CLI executable path

    # Git integration settings
    enable_git: bool = True  # Enable automatic Git integration
    auto_create_branch: bool = True  # Create branch for each learning session
    auto_commit: bool = True  # Auto-commit after phase completion
    auto_push: bool = True  # Auto-push commits to remote
    git_author_name: Optional[str] = None  # Override Git author name
    git_author_email: Optional[str] = None  # Override Git author email

    # Dynamic model selection settings
    enable_dynamic_model_selection: bool = True  # Enable complexity-based model selection
    cost_conscious_mode: bool = True  # Prefer cheaper models when possible
    prefer_quality_mode: bool = False  # Prefer higher-tier models for borderline cases

    def __post_init__(self) -> None:
        """Validate and initialize configuration."""
        if self.api_key is None:
            self.api_key = os.getenv("ANTHROPIC_API_KEY")
            if not self.api_key:
                raise ValueError(
                    "ANTHROPIC_API_KEY not found. Set it in .env or pass to AgentConfig"
                )

        # Set API key in environment for SDK to use
        os.environ["ANTHROPIC_API_KEY"] = self.api_key

        # Ensure directories exist
        self.agents_dir.mkdir(parents=True, exist_ok=True)
        self.commands_dir.mkdir(parents=True, exist_ok=True)
        self.plans_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def from_env(cls) -> "AgentConfig":
        """Create configuration from environment variables."""
        # Parse client mode from environment
        mode_str = os.getenv("CLAUDE_CLIENT_MODE", "auto").lower()
        try:
            client_mode = ClientMode(mode_str)
        except ValueError:
            client_mode = ClientMode.AUTO

        # Parse boolean Git settings
        enable_git = os.getenv("CLAUDE_ENABLE_GIT", "true").lower() == "true"
        auto_create_branch = os.getenv("CLAUDE_AUTO_CREATE_BRANCH", "true").lower() == "true"
        auto_commit = os.getenv("CLAUDE_AUTO_COMMIT", "true").lower() == "true"
        auto_push = os.getenv("CLAUDE_AUTO_PUSH", "true").lower() == "true"

        # Parse boolean dynamic model selection settings
        enable_dynamic_model = os.getenv("CLAUDE_DYNAMIC_MODEL_SELECTION", "true").lower() == "true"
        cost_conscious = os.getenv("CLAUDE_COST_CONSCIOUS", "true").lower() == "true"
        prefer_quality = os.getenv("CLAUDE_PREFER_QUALITY", "false").lower() == "true"

        return cls(
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            model=os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5-20250929"),
            max_tokens=int(os.getenv("MAX_TOKENS", "8192")),
            temperature=float(os.getenv("TEMPERATURE", "1.0")),
            permission_mode=os.getenv("PERMISSION_MODE", "ask"),
            client_mode=client_mode,
            cli_executable=os.getenv("CLAUDE_CLI_PATH", "claude"),
            enable_git=enable_git,
            auto_create_branch=auto_create_branch,
            auto_commit=auto_commit,
            auto_push=auto_push,
            git_author_name=os.getenv("GIT_AUTHOR_NAME"),
            git_author_email=os.getenv("GIT_AUTHOR_EMAIL"),
            enable_dynamic_model_selection=enable_dynamic_model,
            cost_conscious_mode=cost_conscious,
            prefer_quality_mode=prefer_quality,
        )

    def get_agent_path(self, agent_name: str) -> Path:
        """Get the file path for an agent definition."""
        return self.agents_dir / f"{agent_name}.md"

    def get_command_path(self, command_name: str) -> Path:
        """Get the file path for a command definition."""
        return self.commands_dir / f"{command_name}.md"

    def load_agent_prompt(self, agent_name: str) -> str:
        """Load an agent's system prompt from file."""
        agent_path = self.get_agent_path(agent_name)
        if not agent_path.exists():
            raise FileNotFoundError(f"Agent file not found: {agent_path}")
        return agent_path.read_text()

    def load_command_prompt(self, command_name: str) -> str:
        """Load a command's prompt from file."""
        command_path = self.get_command_path(command_name)
        if not command_path.exists():
            raise FileNotFoundError(f"Command file not found: {command_path}")
        return command_path.read_text()

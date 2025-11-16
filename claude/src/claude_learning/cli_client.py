"""CLI client wrapper for Claude Code CLI."""

import asyncio
import subprocess
import json
from typing import Optional, Dict, Any, AsyncIterator
from pathlib import Path
from datetime import datetime

from .config import AgentConfig
from .models import AgentResponse, AgentType


class ClaudeCLIClient:
    """Wrapper for Claude Code CLI interactions."""

    def __init__(self, config: AgentConfig):
        """
        Initialize CLI client.

        Args:
            config: Agent configuration with CLI settings
        """
        self.config = config
        self.cli_path = config.cli_executable

    async def execute_query(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        agent_type: Optional[AgentType] = None,
    ) -> AgentResponse:
        """
        Execute a query using Claude Code CLI.

        Args:
            prompt: The prompt to send to Claude
            system_prompt: Optional system prompt (agent instructions)
            agent_type: The agent type for context

        Returns:
            AgentResponse with the CLI response
        """
        # Prepare the CLI command
        cmd = [self.cli_path]

        # Add system prompt if provided (using agent file)
        if system_prompt and agent_type:
            # Save system prompt to temporary agent file
            temp_agent_file = self._create_temp_agent_file(agent_type.value, system_prompt)
            # Note: Claude CLI may need specific flags for custom agents
            # This is a simplified version - adjust based on actual CLI capabilities

        # Add the prompt
        cmd.extend(["query", prompt])

        try:
            # Execute the CLI command
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.config.workspace_root),
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown CLI error"
                raise RuntimeError(f"Claude CLI error: {error_msg}")

            # Parse the response
            response_text = stdout.decode().strip()

            return AgentResponse(
                content=response_text,
                agent_type=agent_type or AgentType.LEARNING_COORDINATOR,
                timestamp=datetime.now(),
                metadata={"execution_mode": "cli"},
                tool_uses=[],
            )

        except FileNotFoundError:
            raise RuntimeError(
                f"Claude CLI not found at '{self.cli_path}'. "
                "Make sure Claude Code is installed and accessible in PATH, "
                "or set CLAUDE_CLI_PATH environment variable."
            )
        except Exception as e:
            raise RuntimeError(f"Failed to execute Claude CLI: {str(e)}")

    def _create_temp_agent_file(self, agent_name: str, system_prompt: str) -> Path:
        """Create a temporary agent file for the CLI."""
        temp_file = self.config.workspace_root / ".temp" / f"{agent_name}_temp.md"
        temp_file.parent.mkdir(parents=True, exist_ok=True)
        temp_file.write_text(system_prompt)
        return temp_file

    async def check_availability(self) -> bool:
        """
        Check if Claude CLI is available and working.

        Returns:
            True if CLI is available, False otherwise
        """
        try:
            process = await asyncio.create_subprocess_exec(
                self.cli_path,
                "--version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await process.communicate()
            return process.returncode == 0
        except FileNotFoundError:
            return False
        except Exception:
            return False

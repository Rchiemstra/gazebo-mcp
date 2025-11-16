"""Main client for interacting with Claude Agent SDK."""

import asyncio
from typing import AsyncIterator, Optional, Dict, Any, List
from datetime import datetime
from pathlib import Path
import uuid
import logging

from claude_agent_sdk import query, ClaudeSDKClient, ClaudeAgentOptions

from .config import AgentConfig, ClientMode
from .models import AgentType, AgentResponse, LearningSession, LearningPhase
from .cli_client import ClaudeCLIClient
from .git_utils import GitManager

# Import model selector
try:
    from skills.common.model_selector import ModelSelector, ClaudeModel
    MODEL_SELECTOR_AVAILABLE = True
except ImportError:
    MODEL_SELECTOR_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("ModelSelector not available. Dynamic model selection disabled.")

# Configure logging
logger = logging.getLogger(__name__)


class AgentClient:
    """Client for interacting with Claude teaching agents using the Agent SDK."""

    def __init__(self, config: Optional[AgentConfig] = None):
        """
        Initialize the Agent Client.

        Args:
            config: Agent configuration. If None, loads from environment.
        """
        self.config = config or AgentConfig.from_env()
        self._active_sessions: Dict[str, LearningSession] = {}
        self._cli_client: Optional[ClaudeCLIClient] = None
        self._current_mode = self.config.client_mode
        self._api_exhausted = False

        # Initialize CLI client if needed
        if self._current_mode in [ClientMode.CLI, ClientMode.AUTO]:
            self._cli_client = ClaudeCLIClient(self.config)

        # Initialize Git manager if enabled
        self._git_manager: Optional[GitManager] = None
        if self.config.enable_git:
            self._git_manager = GitManager(self.config.workspace_root)
            if not self._git_manager.is_git_repo():
                logger.warning(
                    "Git integration enabled but workspace is not a Git repository. "
                    "Git features will be disabled."
                )
                self._git_manager = None

        # Initialize model selector if enabled
        self._model_selector: Optional[ModelSelector] = None
        if MODEL_SELECTOR_AVAILABLE and self.config.enable_dynamic_model_selection:
            # Convert model string to ClaudeModel enum
            try:
                default_model = ClaudeModel(self.config.model)
            except ValueError:
                logger.warning(f"Unknown model {self.config.model}, using SONNET as default")
                default_model = ClaudeModel.SONNET

            self._model_selector = ModelSelector(
                enabled=True,
                default_model=default_model,
                cost_conscious=self.config.cost_conscious_mode,
                prefer_quality=self.config.prefer_quality_mode
            )
            logger.info("Dynamic model selection enabled")
        else:
            logger.info("Dynamic model selection disabled")

    def _select_model(self, prompt: str, agent_type: AgentType) -> str:
        """
        Select appropriate model for the task based on complexity.

        Args:
            prompt: The task prompt
            agent_type: The agent type being invoked

        Returns:
            Model string to use
        """
        # If dynamic selection disabled or not available, use default
        if not self._model_selector:
            return self.config.model

        # Try to select model based on prompt complexity
        try:
            selected_model = self._model_selector.select_for_prompt(prompt)
            logger.info(f"Selected model {selected_model.value} for agent {agent_type.value}")
            return selected_model.value
        except Exception as e:
            logger.warning(f"Error in model selection: {e}. Using default model.")
            return self.config.model

    def _get_sdk_options(
        self,
        system_prompt: Optional[str] = None,
        custom_tools: Optional[List[str]] = None,
        prompt: Optional[str] = None,
        agent_type: Optional[AgentType] = None
    ) -> ClaudeAgentOptions:
        """Create SDK options from configuration."""
        # Select model dynamically if enabled
        model = self.config.model
        if prompt and agent_type and self._model_selector:
            model = self._select_model(prompt, agent_type)

        return ClaudeAgentOptions(
            model=model,
            system_prompt=system_prompt,
            allowed_tools=custom_tools or self.config.allowed_tools,
            permission_mode=self.config.permission_mode,
        )

    def _should_use_cli(self) -> bool:
        """Determine if CLI should be used based on current mode and state."""
        if self._current_mode == ClientMode.CLI:
            return True
        elif self._current_mode == ClientMode.API:
            return False
        elif self._current_mode == ClientMode.AUTO:
            return self._api_exhausted
        return False

    async def _execute_with_fallback(
        self,
        agent_type: AgentType,
        prompt: str,
        system_prompt: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> AgentResponse:
        """
        Execute query with automatic fallback from API to CLI.

        Args:
            agent_type: The type of agent to query
            prompt: The query prompt
            system_prompt: The agent's system prompt
            context: Additional context

        Returns:
            AgentResponse from either API or CLI
        """
        # Add context to prompt if provided
        full_prompt = prompt
        if context:
            context_str = "\n\n**Context:**\n" + "\n".join(
                f"- {k}: {v}" for k, v in context.items()
            )
            full_prompt = f"{prompt}{context_str}"

        # Try API first if not exhausted and not in CLI-only mode
        if not self._should_use_cli():
            try:
                logger.info(f"Executing query via API for agent: {agent_type.value}")
                return await self._query_via_api(agent_type, full_prompt, system_prompt, context)
            except Exception as e:
                error_str = str(e).lower()
                # Check for quota/rate limit errors
                if any(keyword in error_str for keyword in [
                    "rate limit", "quota", "429", "insufficient", "credits"
                ]):
                    logger.warning(f"API quota exhausted or rate limited: {e}")
                    if self._current_mode == ClientMode.AUTO:
                        logger.info("Switching to CLI mode due to API exhaustion")
                        self._api_exhausted = True
                    else:
                        # Re-raise if not in AUTO mode
                        raise
                else:
                    # Re-raise other errors
                    raise

        # Use CLI (either by choice or fallback)
        if self._cli_client:
            logger.info(f"Executing query via CLI for agent: {agent_type.value}")
            return await self._cli_client.execute_query(
                full_prompt,
                system_prompt=system_prompt,
                agent_type=agent_type,
            )
        else:
            raise RuntimeError(
                "CLI client not available. Set client_mode to 'cli' or 'auto' "
                "and ensure Claude Code CLI is installed."
            )

    async def _query_via_api(
        self,
        agent_type: AgentType,
        full_prompt: str,
        system_prompt: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> AgentResponse:
        """Execute query via Claude API."""
        options = self._get_sdk_options(
            system_prompt=system_prompt,
            prompt=full_prompt,
            agent_type=agent_type
        )

        # Collect response
        response_content = []
        tool_uses = []

        async for message in query(prompt=full_prompt, options=options):
            if isinstance(message, dict):
                if message.get("type") == "text":
                    response_content.append(message.get("content", ""))
                elif message.get("type") == "tool_use":
                    tool_uses.append(message)
            else:
                response_content.append(str(message))

        return AgentResponse(
            content="".join(response_content),
            agent_type=agent_type,
            timestamp=datetime.now(),
            metadata={**(context or {}), "execution_mode": "api"},
            tool_uses=tool_uses,
        )

    async def query_agent(
        self,
        agent_type: AgentType,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> AgentResponse:
        """
        Send a one-off query to a teaching agent.

        Args:
            agent_type: The type of agent to query
            prompt: The learning question or task
            context: Additional context for the query

        Returns:
            AgentResponse with the agent's teaching response
        """
        # Load agent's system prompt
        agent_prompt = self.config.load_agent_prompt(agent_type.value)

        # Execute with automatic fallback
        return await self._execute_with_fallback(
            agent_type=agent_type,
            prompt=prompt,
            system_prompt=agent_prompt,
            context=context,
        )

    async def start_learning_session(
        self,
        topic: str,
        agent_type: AgentType = AgentType.LEARNING_COORDINATOR,
        initial_phase: Optional[LearningPhase] = None,
    ) -> LearningSession:
        """
        Start a new learning session with conversation context.

        Args:
            topic: The learning topic
            agent_type: The agent to work with (default: learning coordinator)
            initial_phase: Starting phase for the learning journey

        Returns:
            LearningSession object for tracking progress
        """
        session_id = str(uuid.uuid4())
        session = LearningSession(
            topic=topic,
            session_id=session_id,
            agent_type=agent_type,
            current_phase=initial_phase,
        )

        # Create Git branch for this session if enabled
        if self._git_manager and self.config.auto_create_branch:
            branch_name = self._git_manager.generate_branch_name(topic, session_id)
            if self._git_manager.create_branch(branch_name, checkout=True):
                session.git_branch = branch_name
                logger.info(f"Created and checked out Git branch: {branch_name}")
            else:
                logger.warning(f"Failed to create Git branch for session: {session_id}")

        self._active_sessions[session_id] = session
        return session

    async def continue_session(
        self,
        session: LearningSession,
        prompt: str,
        update_phase: Optional[LearningPhase] = None,
    ) -> AgentResponse:
        """
        Continue an existing learning session.

        Args:
            session: The active learning session
            prompt: Next question or input
            update_phase: Update the current learning phase if provided

        Returns:
            AgentResponse from the agent
        """
        # Checkout the session's Git branch if it exists
        if self._git_manager and session.git_branch:
            current_branch = self._git_manager.get_current_branch()
            if current_branch != session.git_branch:
                if self._git_manager.checkout_branch(session.git_branch):
                    logger.info(f"Checked out session branch: {session.git_branch}")
                else:
                    logger.warning(f"Failed to checkout session branch: {session.git_branch}")

        if update_phase:
            session.current_phase = update_phase

        # Build context from session history
        context = {
            "topic": session.topic,
            "session_id": session.session_id,
            "phase": session.current_phase.value if session.current_phase else "initial",
            "previous_interactions": len(session.messages),
        }

        response = await self.query_agent(
            agent_type=session.agent_type,
            prompt=prompt,
            context=context,
        )

        session.add_response(response)
        return response

    async def ask_specialist(
        self,
        agent_type: AgentType,
        question: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> AgentResponse:
        """
        Ask a specific teaching specialist a question.

        Args:
            agent_type: The specialist to consult
            question: The question to ask
            context: Additional context

        Returns:
            AgentResponse with specialist's guidance
        """
        return await self.query_agent(
            agent_type=agent_type,
            prompt=question,
            context=context,
        )

    async def create_learning_plan(
        self,
        topic: str,
        student_context: Optional[Dict[str, Any]] = None,
    ) -> AgentResponse:
        """
        Create a comprehensive learning plan.

        Args:
            topic: What to learn
            student_context: Information about student background, goals, etc.

        Returns:
            AgentResponse containing the learning plan
        """
        prompt = f"Create a comprehensive learning plan for: {topic}"

        return await self.query_agent(
            agent_type=AgentType.PLAN_GENERATION_MENTOR,
            prompt=prompt,
            context=student_context,
        )

    async def check_understanding(
        self,
        topic: str,
        session: Optional[LearningSession] = None,
    ) -> AgentResponse:
        """
        Verify understanding of a topic through discussion.

        Args:
            topic: Topic to verify understanding of
            session: Optional active session for context

        Returns:
            AgentResponse with understanding check questions/discussion
        """
        context = {}
        if session:
            context = {
                "session_topic": session.topic,
                "current_phase": session.current_phase.value if session.current_phase else None,
                "learning_history": session.get_conversation_history()[-3:],  # Last 3 interactions
            }

        prompt = f"Check my understanding of: {topic}"

        return await self.query_agent(
            agent_type=AgentType.LEARNING_COORDINATOR,
            prompt=prompt,
            context=context,
        )

    def get_session(self, session_id: str) -> Optional[LearningSession]:
        """Retrieve an active session by ID."""
        return self._active_sessions.get(session_id)

    def list_active_sessions(self) -> List[LearningSession]:
        """List all active learning sessions."""
        return list(self._active_sessions.values())

    async def complete_phase(
        self,
        session: LearningSession,
        phase: LearningPhase,
        summary: Optional[str] = None,
    ) -> bool:
        """
        Mark a phase as complete and commit changes to Git.

        Args:
            session: The learning session
            phase: The phase that was completed
            summary: Optional summary of the phase work

        Returns:
            True if commit/push successful, False otherwise
        """
        if not self._git_manager or not self.config.auto_commit:
            logger.info("Git integration disabled, skipping phase commit")
            return True

        if not session.git_branch:
            logger.warning("No Git branch associated with session")
            return False

        # Ensure we're on the correct branch
        if self._git_manager.get_current_branch() != session.git_branch:
            if not self._git_manager.checkout_branch(session.git_branch):
                logger.error(f"Failed to checkout branch: {session.git_branch}")
                return False

        # Get phase number (based on enum order)
        phase_number = list(LearningPhase).index(phase) + 1

        # Create commit for this phase
        commit_success = self._git_manager.create_phase_commit(
            phase_name=phase.value,
            phase_number=phase_number,
            topic=session.topic,
            summary=summary,
        )

        if not commit_success:
            logger.error(f"Failed to commit phase {phase.value}")
            return False

        # Record the commit in the session
        session.record_phase_commit(phase)

        # Push to remote if configured
        if self.config.auto_push:
            if self._git_manager.has_remote():
                push_success = self._git_manager.push_branch(session.git_branch)
                if push_success:
                    logger.info(f"Pushed phase {phase.value} to remote")
                else:
                    logger.warning(f"Failed to push phase {phase.value} to remote")
                    return False
            else:
                logger.info("No remote configured, skipping push")

        logger.info(f"Successfully committed and pushed phase: {phase.value}")
        return True

    def close_session(self, session_id: str) -> None:
        """Mark a session as completed and archive it."""
        if session_id in self._active_sessions:
            session = self._active_sessions[session_id]
            session.completed = True
            # Could save to disk here
            del self._active_sessions[session_id]

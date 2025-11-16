"""Example: Demonstrating Git integration with learning sessions."""

import asyncio
import logging
from claude_learning import (
    AgentClient,
    AgentConfig,
    AgentType,
    LearningPhase,
)

# Configure logging to see Git operations
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def demo_full_git_workflow():
    """Demonstrate complete Git workflow for a learning session."""
    print("=== Git Integration Demo ===\n")

    # Create config with Git enabled (default)
    config = AgentConfig.from_env()
    client = AgentClient(config)

    print("Step 1: Starting a new learning session...")
    print("This will automatically create a new Git branch\n")

    # Start a learning session - automatically creates Git branch
    session = await client.start_learning_session(
        topic="Python Decorators",
        agent_type=AgentType.PYTHON_BEST_PRACTICES,
        initial_phase=LearningPhase.RESEARCH,
    )

    print(f"✓ Session created: {session.session_id}")
    print(f"✓ Git branch: {session.git_branch}")
    print(f"✓ Current phase: {session.current_phase.value if session.current_phase else 'N/A'}\n")

    # Continue the session - ask a question
    print("Step 2: Asking a question in the session...")
    response = await client.continue_session(
        session=session,
        prompt="Explain what Python decorators are and why they're useful",
    )
    print(f"✓ Response received ({len(response.content)} characters)\n")

    # Simulate completing research phase
    print("Step 3: Completing RESEARCH phase...")
    print("This will create a commit and push to remote\n")

    # Complete the research phase - automatically commits and pushes
    success = await client.complete_phase(
        session=session,
        phase=LearningPhase.RESEARCH,
        summary="Learned fundamentals of Python decorators and common use cases",
    )

    if success:
        print("✓ Phase committed and pushed successfully")
        print(f"✓ Commits so far: {len(session.phase_commits)}\n")
    else:
        print("✗ Phase commit failed\n")

    # Move to design phase
    print("Step 4: Moving to DESIGN phase...")
    response = await client.continue_session(
        session=session,
        prompt="How would I design a timing decorator to measure function execution?",
        update_phase=LearningPhase.DESIGN,
    )
    print(f"✓ Moved to DESIGN phase")
    print(f"✓ Response received\n")

    # Complete design phase
    print("Step 5: Completing DESIGN phase...")
    success = await client.complete_phase(
        session=session,
        phase=LearningPhase.DESIGN,
        summary="Designed a timing decorator with context manager support",
    )

    if success:
        print("✓ DESIGN phase committed and pushed")
        print(f"✓ Total commits: {len(session.phase_commits)}\n")

    # Show session summary
    print("=== Session Summary ===")
    print(f"Topic: {session.topic}")
    print(f"Session ID: {session.session_id}")
    print(f"Git Branch: {session.git_branch}")
    print(f"Current Phase: {session.current_phase.value if session.current_phase else 'N/A'}")
    print(f"Interactions: {len(session.messages)}")
    print(f"Phase Commits: {len(session.phase_commits)}")
    print("\nCommit History:")
    for commit in session.phase_commits:
        print(f"  - {commit['phase']}: {commit['timestamp']}")


async def demo_continue_existing_session():
    """Demonstrate continuing an existing session (checks out branch)."""
    print("\n\n=== Continuing Existing Session Demo ===\n")

    config = AgentConfig.from_env()
    client = AgentClient(config)

    # Start first session
    print("Creating session 1...")
    session1 = await client.start_learning_session(
        topic="Async Programming",
        agent_type=AgentType.PYTHON_BEST_PRACTICES,
    )
    print(f"✓ Session 1 branch: {session1.git_branch}\n")

    # Start second session (switches to new branch)
    print("Creating session 2 (switches branches)...")
    session2 = await client.start_learning_session(
        topic="Testing Strategies",
        agent_type=AgentType.TESTING_SPECIALIST,
    )
    print(f"✓ Session 2 branch: {session2.git_branch}\n")

    # Continue first session (automatically checks out session 1 branch)
    print("Continuing session 1 (automatically checks out its branch)...")
    await client.continue_session(
        session=session1,
        prompt="Explain async/await",
    )
    print(f"✓ Checked out: {session1.git_branch}")
    print("✓ Can now work on session 1\n")

    # Continue second session (switches back)
    print("Continuing session 2 (switches back)...")
    await client.continue_session(
        session=session2,
        prompt="What is TDD?",
    )
    print(f"✓ Checked out: {session2.git_branch}")
    print("✓ Can now work on session 2\n")


async def demo_git_disabled():
    """Demonstrate running without Git integration."""
    print("\n\n=== Git Disabled Demo ===\n")

    config = AgentConfig.from_env()
    config.enable_git = False  # Disable Git

    client = AgentClient(config)

    session = await client.start_learning_session(
        topic="Design Patterns",
        agent_type=AgentType.CODE_ARCHITECTURE_MENTOR,
    )

    print(f"Git Branch: {session.git_branch or 'None (Git disabled)'}")
    print("Session works normally without Git integration")


async def main():
    """Run all demos."""
    # Demo 1: Full Git workflow
    await demo_full_git_workflow()

    # Demo 2: Multiple sessions with branch switching
    await demo_continue_existing_session()

    # Demo 3: Git disabled
    await demo_git_disabled()

    print("\n\n=== Configuration ===")
    print("Control Git integration via environment variables:")
    print("  CLAUDE_ENABLE_GIT=true|false           - Enable/disable Git integration")
    print("  CLAUDE_AUTO_CREATE_BRANCH=true|false   - Auto-create branch per session")
    print("  CLAUDE_AUTO_COMMIT=true|false          - Auto-commit on phase completion")
    print("  CLAUDE_AUTO_PUSH=true|false            - Auto-push commits to remote")
    print("\nOr in code:")
    print("  config = AgentConfig.from_env()")
    print("  config.enable_git = False")
    print("  config.auto_commit = False")


if __name__ == "__main__":
    asyncio.run(main())

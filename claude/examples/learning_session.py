"""Example: Multi-turn learning session with conversation context."""

import asyncio
from claude_learning import AgentClient, AgentConfig, AgentType, LearningPhase


async def main():
    """Demonstrate a continuous learning session."""
    # Initialize client
    config = AgentConfig.from_env()
    client = AgentClient(config)

    print("=== Learning Session Example ===\n")

    # Start a new learning session
    print("Starting learning session on autonomous navigation...")
    session = await client.start_learning_session(
        topic="autonomous navigation for mobile robots",
        agent_type=AgentType.LEARNING_COORDINATOR,
        initial_phase=LearningPhase.RESEARCH,
    )

    print(f"Session ID: {session.session_id}")
    print(f"Current Phase: {session.current_phase.value}\n")

    # First interaction
    print("Student: What are the key components I need to understand?\n")
    response1 = await client.continue_session(
        session=session,
        prompt="What are the key components I need to understand for autonomous navigation?",
    )
    print(f"Mentor: {response1.content}\n")

    # Second interaction
    print("Student: Can you explain path planning algorithms?\n")
    response2 = await client.continue_session(
        session=session,
        prompt="Can you explain the main path planning algorithms?",
    )
    print(f"Mentor: {response2.content}\n")

    # Move to design phase
    print("Moving to DESIGN phase...\n")
    response3 = await client.continue_session(
        session=session,
        prompt="I understand the basics now. Help me design the system architecture.",
        update_phase=LearningPhase.DESIGN,
    )
    print(f"Mentor: {response3.content}\n")

    # Show session summary
    print(f"\n=== Session Summary ===")
    print(f"Topic: {session.topic}")
    print(f"Total interactions: {len(session.messages)}")
    print(f"Current phase: {session.current_phase.value}")

    # Close session
    client.close_session(session.session_id)
    print(f"Session closed: {session.session_id}")


if __name__ == "__main__":
    asyncio.run(main())

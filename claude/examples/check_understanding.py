"""Example: Checking understanding through discussion."""

import asyncio
from claude_learning import AgentClient, AgentConfig, AgentType, LearningPhase


async def main():
    """Demonstrate understanding verification."""
    # Initialize client
    config = AgentConfig.from_env()
    client = AgentClient(config)

    print("=== Understanding Check Example ===\n")

    # Create a session with learning history
    session = await client.start_learning_session(
        topic="ROS2 pub/sub patterns",
        agent_type=AgentType.LEARNING_COORDINATOR,
        initial_phase=LearningPhase.IMPLEMENT,
    )

    # Simulate some learning has happened
    await client.continue_session(
        session=session,
        prompt="I've been studying ROS2 publishers and subscribers. Can you check my understanding?",
    )

    print("Student: I think I understand ROS2 pub/sub. Ready for assessment.\n")

    # Check understanding
    response = await client.check_understanding(
        topic="ROS2 publishers and subscribers",
        session=session,
    )

    print(f"Mentor: {response.content}\n")

    # The mentor will ask questions to verify understanding
    # In a real scenario, you would continue the conversation
    print("\n[In a real scenario, continue the discussion-based assessment]")

    client.close_session(session.session_id)


if __name__ == "__main__":
    asyncio.run(main())

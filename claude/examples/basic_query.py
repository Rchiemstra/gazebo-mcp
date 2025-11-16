"""Example: Basic agent query using Claude Agent SDK."""

import asyncio
from claude_learning import AgentClient, AgentConfig, AgentType


async def main():
    """Demonstrate basic agent query."""
    # Initialize client with configuration
    config = AgentConfig.from_env()
    client = AgentClient(config)

    print("=== Basic Agent Query Example ===\n")

    # Ask the ROS2 learning mentor a question
    print("Asking ROS2 Learning Mentor about publishers and subscribers...")
    response = await client.query_agent(
        agent_type=AgentType.ROS2_LEARNING_MENTOR,
        prompt="Explain the difference between ROS2 publishers and subscribers",
        context={"experience_level": "beginner"},
    )

    print(f"\n{response.content}\n")
    print(f"Response received at: {response.timestamp}")
    print(f"Tools used: {len(response.tool_uses)}")


if __name__ == "__main__":
    asyncio.run(main())

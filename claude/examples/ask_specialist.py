"""Example: Consulting different teaching specialists."""

import asyncio
from claude_learning import AgentClient, AgentConfig, AgentType


async def main():
    """Demonstrate asking different specialists."""
    # Initialize client
    config = AgentConfig.from_env()
    client = AgentClient(config)

    print("=== Specialist Consultation Example ===\n")

    # 1. Ask Code Architecture Mentor about design patterns
    print("1. Consulting Code Architecture Mentor about design patterns...\n")
    response1 = await client.ask_specialist(
        agent_type=AgentType.CODE_ARCHITECTURE_MENTOR,
        question="When should I use the Strategy pattern vs the State pattern?",
        context={"project_type": "robotics control system"},
    )
    print(f"Architecture Mentor: {response1.content}\n")
    print("-" * 80 + "\n")

    # 2. Ask Python Best Practices about async programming
    print("2. Consulting Python Best Practices about async programming...\n")
    response2 = await client.ask_specialist(
        agent_type=AgentType.PYTHON_BEST_PRACTICES,
        question="How should I structure async functions for ROS2 integration?",
    )
    print(f"Python Expert: {response2.content}\n")
    print("-" * 80 + "\n")

    # 3. Ask Robotics Vision Navigator about SLAM
    print("3. Consulting Robotics Vision Navigator about SLAM...\n")
    response3 = await client.ask_specialist(
        agent_type=AgentType.ROBOTICS_VISION_NAVIGATOR,
        question="What are the trade-offs between visual SLAM and lidar SLAM?",
        context={"robot_type": "JETANK", "environment": "indoor"},
    )
    print(f"Vision Navigator: {response3.content}\n")


if __name__ == "__main__":
    asyncio.run(main())

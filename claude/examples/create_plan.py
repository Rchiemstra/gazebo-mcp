"""Example: Creating a comprehensive learning plan."""

import asyncio
from claude_learning import AgentClient, AgentConfig


async def main():
    """Demonstrate creating a learning plan."""
    # Initialize client
    config = AgentConfig.from_env()
    client = AgentClient(config)

    print("=== Learning Plan Creation Example ===\n")

    # Define student context
    student_context = {
        "experience_level": "intermediate",
        "background": "Python programming, basic robotics",
        "goals": "Build autonomous navigation system for JETANK robot",
        "time_available": "6-8 weeks, 10 hours per week",
        "preferred_learning_style": "hands-on with theory",
    }

    print("Creating learning plan for autonomous navigation...")
    print(f"Student context: {student_context}\n")

    # Create the plan
    response = await client.create_learning_plan(
        topic="autonomous navigation with obstacle avoidance",
        student_context=student_context,
    )

    print("=== Generated Learning Plan ===\n")
    print(response.content)

    # Save plan to file
    plan_file = config.plans_dir / "autonomous_navigation_plan.md"
    plan_file.write_text(response.content)
    print(f"\n✓ Plan saved to: {plan_file}")


if __name__ == "__main__":
    asyncio.run(main())

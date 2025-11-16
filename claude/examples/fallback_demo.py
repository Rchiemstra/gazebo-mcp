"""Example: Demonstrating automatic fallback from API to CLI."""

import asyncio
import logging
from claude_learning import AgentClient, AgentConfig, AgentType, ClientMode

# Configure logging to see the fallback in action
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def demo_auto_fallback():
    """Demonstrate automatic fallback from API to CLI."""
    print("=== AUTO Mode: API with CLI Fallback Demo ===\n")

    # Create config with AUTO mode (default)
    config = AgentConfig.from_env()
    # Ensure it's in AUTO mode
    config.client_mode = ClientMode.AUTO

    client = AgentClient(config)

    # First query - will try API
    print("Query 1: Using API (if available)...")
    response1 = await client.query_agent(
        agent_type=AgentType.PYTHON_BEST_PRACTICES,
        prompt="What are Python type hints and why should I use them?",
        context={"experience_level": "beginner"},
    )
    print(f"Response mode: {response1.metadata.get('execution_mode', 'unknown')}")
    print(f"Response: {response1.content[:200]}...\n")

    # If API quota runs out, subsequent queries will use CLI automatically
    print("Query 2: (Will use CLI if API exhausted)...")
    response2 = await client.query_agent(
        agent_type=AgentType.TESTING_SPECIALIST,
        prompt="Explain test-driven development in simple terms",
        context={"experience_level": "beginner"},
    )
    print(f"Response mode: {response2.metadata.get('execution_mode', 'unknown')}")
    print(f"Response: {response2.content[:200]}...\n")


async def demo_cli_only():
    """Demonstrate CLI-only mode."""
    print("\n=== CLI-Only Mode Demo ===\n")

    # Create config forcing CLI mode
    config = AgentConfig.from_env()
    config.client_mode = ClientMode.CLI

    client = AgentClient(config)

    print("Query: Using CLI directly...")
    response = await client.query_agent(
        agent_type=AgentType.DEBUGGING_DETECTIVE,
        prompt="How do I debug a Python program effectively?",
        context={"experience_level": "intermediate"},
    )
    print(f"Response mode: {response.metadata.get('execution_mode', 'unknown')}")
    print(f"Response: {response.content[:200]}...\n")


async def demo_api_only():
    """Demonstrate API-only mode."""
    print("\n=== API-Only Mode Demo ===\n")

    # Create config forcing API mode
    config = AgentConfig.from_env()
    config.client_mode = ClientMode.API

    client = AgentClient(config)

    try:
        print("Query: Using API only (no fallback)...")
        response = await client.query_agent(
            agent_type=AgentType.CODE_ARCHITECTURE_MENTOR,
            prompt="What is the MVC pattern?",
            context={"experience_level": "intermediate"},
        )
        print(f"Response mode: {response.metadata.get('execution_mode', 'unknown')}")
        print(f"Response: {response.content[:200]}...\n")
    except Exception as e:
        print(f"Error (expected if API quota exhausted): {e}")


async def main():
    """Run all demos."""
    # Demo 1: AUTO mode with fallback
    await demo_auto_fallback()

    # Demo 2: CLI-only mode
    await demo_cli_only()

    # Demo 3: API-only mode
    await demo_api_only()

    print("\n=== Configuration via Environment Variables ===")
    print("Set CLAUDE_CLIENT_MODE to:")
    print("  - 'api' for API-only (faster, uses quota)")
    print("  - 'cli' for CLI-only (uses Claude Code CLI)")
    print("  - 'auto' for automatic fallback (default)")
    print("\nExample:")
    print("  export CLAUDE_CLIENT_MODE=auto")
    print("  export CLAUDE_CLI_PATH=/path/to/claude  # if not in PATH")


if __name__ == "__main__":
    asyncio.run(main())

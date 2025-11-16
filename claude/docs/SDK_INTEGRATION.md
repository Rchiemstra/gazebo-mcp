# SDK Integration Guide

This guide explains how to use the Python SDK integration for the Claude Learning System.

## Overview

The Python SDK integration allows you to programmatically interact with the teaching agents using the **Claude Agent SDK**. This enables building custom applications, automation workflows, and integrations.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip or poetry for package management
- Anthropic API key

### Setup

1. **Clone the repository**:
   ```bash
   cd claude_code
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -e .
   ```

4. **Configure API key**:
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

## Quick Start

### Basic Query

```python
import asyncio
from claude_learning import AgentClient, AgentType

async def main():
    client = AgentClient.from_env()

    response = await client.query_agent(
        agent_type=AgentType.ROS2_LEARNING_MENTOR,
        prompt="Explain ROS2 topics",
    )

    print(response.content)

asyncio.run(main())
```

### Learning Session

```python
import asyncio
from claude_learning import AgentClient, AgentType, LearningPhase

async def main():
    client = AgentClient.from_env()

    # Start session
    session = await client.start_learning_session(
        topic="autonomous navigation",
        agent_type=AgentType.LEARNING_COORDINATOR,
        initial_phase=LearningPhase.RESEARCH,
    )

    # Continue conversation
    response = await client.continue_session(
        session=session,
        prompt="What should I learn first?",
    )

    print(response.content)

    # Close when done
    client.close_session(session.session_id)

asyncio.run(main())
```

## Core Components

### AgentClient

The main interface for interacting with teaching agents.

```python
from claude_learning import AgentClient, AgentConfig

# From environment
client = AgentClient.from_env()

# Custom configuration
config = AgentConfig(
    api_key="your-key",
    model="claude-sonnet-4-5-20250929",
    max_tokens=8192,
)
client = AgentClient(config)
```

### Agent Types

Available teaching specialists:

- `LEARNING_COORDINATOR` - Overall learning guidance
- `PLAN_GENERATION_MENTOR` - Creates learning plans
- `ROS2_LEARNING_MENTOR` - ROS2 concepts
- `CODE_ARCHITECTURE_MENTOR` - Design patterns
- `ROBOTICS_VISION_NAVIGATOR` - Computer vision, SLAM
- `JETANK_HARDWARE_SPECIALIST` - Hardware integration
- `PYTHON_BEST_PRACTICES` - Python expertise
- `CPP_BEST_PRACTICES` - C++ expertise
- `DEBUGGING_DETECTIVE` - Debugging help
- `TESTING_SPECIALIST` - Testing guidance
- `GIT_WORKFLOW_EXPERT` - Git workflows
- `DOCUMENTATION_GENERATOR` - Documentation

### Learning Phases

Track learning progression:

- `RESEARCH` - Understanding concepts
- `DESIGN` - Planning implementation
- `IMPLEMENT` - Building the solution
- `REFLECT` - Reviewing and learning

## Key Methods

### `query_agent()`

One-off query to a teaching agent:

```python
response = await client.query_agent(
    agent_type=AgentType.PYTHON_BEST_PRACTICES,
    prompt="How should I structure async code?",
    context={"experience": "intermediate"},
)
```

### `start_learning_session()`

Begin a stateful learning session:

```python
session = await client.start_learning_session(
    topic="ROS2 navigation",
    agent_type=AgentType.LEARNING_COORDINATOR,
    initial_phase=LearningPhase.RESEARCH,
)
```

### `continue_session()`

Continue an active session:

```python
response = await client.continue_session(
    session=session,
    prompt="Next question...",
    update_phase=LearningPhase.DESIGN,  # Optional
)
```

### `ask_specialist()`

Quick consultation with a specialist:

```python
response = await client.ask_specialist(
    agent_type=AgentType.CODE_ARCHITECTURE_MENTOR,
    question="When to use Strategy pattern?",
)
```

### `create_learning_plan()`

Generate a comprehensive learning plan:

```python
response = await client.create_learning_plan(
    topic="autonomous navigation",
    student_context={
        "experience_level": "intermediate",
        "background": "Python, basic robotics",
        "goals": "Build navigation system",
    },
)
```

### `check_understanding()`

Verify learning through discussion:

```python
response = await client.check_understanding(
    topic="ROS2 publishers",
    session=session,  # Optional context
)
```

## Examples

The `examples/` directory contains complete working examples:

- `basic_query.py` - Simple agent query
- `learning_session.py` - Multi-turn conversation
- `ask_specialist.py` - Consulting specialists
- `create_plan.py` - Generating learning plans
- `check_understanding.py` - Understanding verification

Run an example:

```bash
python examples/basic_query.py
```

## Testing

Run the test suite:

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=src/claude_learning
```

## Configuration

### Environment Variables

Create a `.env` file:

```bash
ANTHROPIC_API_KEY=your_api_key_here
CLAUDE_MODEL=claude-sonnet-4-5-20250929
MAX_TOKENS=8192
TEMPERATURE=1.0
PERMISSION_MODE=ask
```

### AgentConfig Options

```python
config = AgentConfig(
    api_key="...",              # Anthropic API key
    model="...",                # Claude model to use
    max_tokens=8192,            # Max response tokens
    temperature=1.0,            # Creativity (0-1)
    allowed_tools=[...],        # Tools agent can use
    permission_mode="ask",      # ask, acceptEdits, acceptAll
    workspace_root=Path("..."), # Project root
    agents_dir=Path("..."),     # Agent definitions
    commands_dir=Path("..."),   # Command definitions
    plans_dir=Path("..."),      # Generated plans
)
```

## Best Practices

1. **Use sessions for multi-turn conversations** - Maintains context
2. **Close sessions when done** - Frees resources
3. **Provide context** - Helps agents give better guidance
4. **Track learning phases** - Shows progression
5. **Save plans to disk** - Keep learning records
6. **Handle async properly** - Use `asyncio.run()` or event loops

## Migration from Claude Code SDK

This project uses the **Claude Agent SDK** (not the deprecated Claude Code SDK).

Key differences:
- Package: `claude-agent-sdk` (not `claude-code-sdk`)
- Import: `from claude_agent_sdk import ...`
- Options: `ClaudeAgentOptions` (not `ClaudeCodeOptions`)
- System prompts must be explicitly provided
- Settings sources must be manually specified

See [project-context/project-context.md](../project-context/project-context.md) for full migration guide.

## Troubleshooting

### API Key Issues

```python
# Explicitly set API key
config = AgentConfig(api_key="your-key-here")
client = AgentClient(config)
```

### Agent File Not Found

Ensure agent definitions exist in `agents/` directory:

```bash
ls agents/
# Should show: learning-coordinator.md, ros2-learning-mentor.md, etc.
```

### Async Errors

Always use `asyncio.run()` for top-level async code:

```python
import asyncio

async def main():
    # Your async code here
    pass

asyncio.run(main())
```

## Next Steps

- Explore the [examples/](../examples/) directory
- Review [agent definitions](../agents/) for teaching styles
- Check [migration guide](../project-context/project-context.md)
- Build custom integrations with the SDK

## Support

For issues or questions:
- Check existing agent definitions in `agents/`
- Review example code in `examples/`
- Consult API documentation: https://docs.claude.com/en/api/agent-sdk/python

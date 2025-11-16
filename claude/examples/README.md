# Python SDK Examples

This directory contains examples demonstrating how to use the Claude Learning System Python SDK.

## Prerequisites

Before running these examples, ensure you have:

1. Installed the package: `pip install -e .`
2. Configured your API key in `.env`
3. Activated your virtual environment

## Examples

### 1. Basic Query (`basic_query.py`)

Simple one-off query to a teaching agent.

```bash
python examples/basic_query.py
```

**What it demonstrates:**
- Initializing the AgentClient
- Querying a specific agent (ROS2 Learning Mentor)
- Handling agent responses
- Passing context to queries

### 2. Learning Session (`learning_session.py`)

Multi-turn conversation with conversation context.

```bash
python examples/learning_session.py
```

**What it demonstrates:**
- Starting a stateful learning session
- Continuing conversations with context
- Changing learning phases
- Session management and closure

### 3. Ask Specialist (`ask_specialist.py`)

Consulting different teaching specialists.

```bash
python examples/ask_specialist.py
```

**What it demonstrates:**
- Querying multiple different specialists
- Passing project-specific context
- Getting specialized guidance
- Comparing different expert perspectives

### 4. Create Plan (`create_plan.py`)

Generating comprehensive learning plans.

```bash
python examples/create_plan.py
```

**What it demonstrates:**
- Creating learning plans
- Providing student context
- Saving plans to disk
- Using the plan generation mentor

### 5. Check Understanding (`check_understanding.py`)

Verifying learning through discussion-based assessment.

```bash
python examples/check_understanding.py
```

**What it demonstrates:**
- Understanding verification
- Using session history for context
- Discussion-based assessment approach
- Interactive learning validation

## Running All Examples

To run all examples in sequence:

```bash
for example in examples/*.py; do
    echo "Running $example..."
    python "$example"
    echo "---"
done
```

## Customizing Examples

All examples can be customized by:

1. **Changing the agent type**:
   ```python
   from claude_learning import AgentType

   # Use a different specialist
   agent_type=AgentType.CODE_ARCHITECTURE_MENTOR
   ```

2. **Modifying prompts**:
   ```python
   prompt="Your custom question here"
   ```

3. **Adding context**:
   ```python
   context={
       "experience_level": "intermediate",
       "project_type": "robotics",
       "goals": "build autonomous system"
   }
   ```

4. **Adjusting configuration**:
   ```python
   from claude_learning import AgentConfig

   config = AgentConfig(
       api_key="your-key",
       model="claude-sonnet-4-5-20250929",
       max_tokens=4096,
       temperature=0.7,
   )
   ```

## Best Practices

1. **Always use async/await**: All SDK methods are asynchronous
2. **Close sessions**: Call `client.close_session()` when done
3. **Handle errors**: Wrap in try/except for production use
4. **Provide context**: More context = better guidance
5. **Save important responses**: Store plans and insights

## Environment Variables

Examples use these environment variables:

- `ANTHROPIC_API_KEY`: Your API key (required)
- `CLAUDE_MODEL`: Model to use (default: claude-sonnet-4-5-20250929)
- `MAX_TOKENS`: Max response tokens (default: 8192)
- `TEMPERATURE`: Response creativity (default: 1.0)
- `PERMISSION_MODE`: Tool permission mode (default: ask)

## Troubleshooting

### "API key not found"

Ensure `.env` exists with:
```
ANTHROPIC_API_KEY=your_key_here
```

### "Agent file not found"

Examples expect agent definitions in `agents/` directory. Ensure you're running from project root:

```bash
cd /path/to/claude_code
python examples/basic_query.py
```

### "Module not found"

Install the package in editable mode:

```bash
pip install -e .
```

### Rate Limiting

If you hit rate limits, add delays between requests:

```python
import asyncio
await asyncio.sleep(2)  # Wait 2 seconds between requests
```

## Next Steps

After running these examples:

1. Read [SDK_INTEGRATION.md](../docs/SDK_INTEGRATION.md) for full API reference
2. Explore [agent definitions](../agents/) to understand teaching styles
3. Build your own integration using these examples as templates
4. Check [tests/](../tests/) for more usage patterns

## Contributing

To add a new example:

1. Create `examples/your_example.py`
2. Follow the existing example structure
3. Add docstring explaining what it demonstrates
4. Update this README with a description
5. Test thoroughly before committing

Happy Learning! 🎓

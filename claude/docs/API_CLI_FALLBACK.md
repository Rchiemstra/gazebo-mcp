# API to CLI Automatic Fallback

This feature allows you to configure your Claude Learning System to automatically switch between using the Claude API directly and the Claude Code CLI, with automatic fallback when API quota is exhausted.

## Overview

The system supports three execution modes:

1. **API Mode** (`api`) - Uses Claude API directly (faster, consumes API quota)
2. **CLI Mode** (`cli`) - Uses Claude Code CLI (no API quota used)
3. **AUTO Mode** (`auto`) - Starts with API, automatically falls back to CLI when quota exhausted (default)

## Configuration

### Environment Variables

Set the client mode using environment variables:

```bash
# Choose execution mode (api, cli, or auto)
export CLAUDE_CLIENT_MODE=auto

# Optional: Set custom Claude CLI path (if not in PATH)
export CLAUDE_CLI_PATH=/path/to/claude
```

### In Code

```python
from claude_learning import AgentClient, AgentConfig, ClientMode

# Option 1: Use environment variables
config = AgentConfig.from_env()
client = AgentClient(config)

# Option 2: Set mode explicitly
config = AgentConfig.from_env()
config.client_mode = ClientMode.AUTO  # or ClientMode.API or ClientMode.CLI
client = AgentClient(config)

# Option 3: Full manual configuration
config = AgentConfig(
    client_mode=ClientMode.AUTO,
    cli_executable="claude",  # or full path
    # ... other config options
)
client = AgentClient(config)
```

## How It Works

### AUTO Mode (Recommended)

1. Client starts using Claude API for queries
2. If API quota exhausted or rate limited, system detects the error
3. All subsequent queries automatically use Claude Code CLI
4. No manual intervention required

The system detects these error conditions for fallback:
- Rate limit errors (HTTP 429)
- Quota exhausted errors
- Insufficient credits errors
- Any error message containing: "rate limit", "quota", "insufficient", "credits"

### API Mode

- Always uses Claude API
- Throws error if quota exhausted (no fallback)
- Faster response times when quota available

### CLI Mode

- Always uses Claude Code CLI
- No API quota consumed
- Requires Claude Code installed and accessible

## Example Usage

```python
import asyncio
from claude_learning import AgentClient, AgentConfig, ClientMode, AgentType

async def main():
    # AUTO mode with fallback
    config = AgentConfig.from_env()
    config.client_mode = ClientMode.AUTO

    client = AgentClient(config)

    # First query - uses API
    response1 = await client.query_agent(
        agent_type=AgentType.PYTHON_BEST_PRACTICES,
        prompt="Explain Python decorators",
    )

    print(f"Execution mode: {response1.metadata.get('execution_mode')}")
    # Output: "api" or "cli" depending on quota status

    # If API quota exhausted, this uses CLI automatically
    response2 = await client.query_agent(
        agent_type=AgentType.TESTING_SPECIALIST,
        prompt="Explain unit testing",
    )

    print(f"Execution mode: {response2.metadata.get('execution_mode')}")
    # Output: "cli" if API was exhausted

asyncio.run(main())
```

## Checking Execution Mode

Each `AgentResponse` includes metadata about which execution mode was used:

```python
response = await client.query_agent(...)

# Check which mode was used
mode = response.metadata.get('execution_mode')
if mode == 'api':
    print("Used API")
elif mode == 'cli':
    print("Used CLI")
```

## Logging

Enable logging to see fallback behavior:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

You'll see messages like:
```
INFO - claude_learning.agent_client - Executing query via API for agent: python-best-practices
WARNING - claude_learning.agent_client - API quota exhausted or rate limited: ...
INFO - claude_learning.agent_client - Switching to CLI mode due to API exhaustion
INFO - claude_learning.agent_client - Executing query via CLI for agent: testing-specialist
```

## Requirements

- **For API Mode**: Valid `ANTHROPIC_API_KEY` environment variable
- **For CLI Mode**: Claude Code CLI installed and accessible
  - Install: Follow instructions at https://docs.claude.com/claude-code
  - Verify: Run `claude --version` in terminal

## Examples

See `examples/fallback_demo.py` for comprehensive examples of all modes:

```bash
python examples/fallback_demo.py
```

## Troubleshooting

### "Claude CLI not found" Error

**Problem**: CLI client can't find the `claude` executable

**Solutions**:
1. Install Claude Code: https://docs.claude.com/claude-code
2. Add to PATH: `export PATH=$PATH:/path/to/claude`
3. Or set explicit path: `export CLAUDE_CLI_PATH=/full/path/to/claude`

### API Still Used After Quota Exhausted

**Problem**: System doesn't fallback even when quota exhausted

**Check**:
1. Mode is set to AUTO: `export CLAUDE_CLIENT_MODE=auto`
2. CLI is available: `claude --version`
3. Error is quota-related (check error message)

### CLI Mode Not Working

**Problem**: CLI mode fails to execute

**Check**:
1. Claude Code is installed and updated
2. CLI executable path is correct
3. Required permissions for execution

## Best Practices

1. **Development**: Use AUTO mode for seamless development
2. **Production**:
   - Use API mode if you have quota and want speed
   - Use CLI mode if you want to avoid API charges
3. **Testing**: Use CLI mode to avoid consuming API quota during tests
4. **Set appropriate logging** to monitor fallback behavior
5. **Monitor API usage** to avoid unexpected fallbacks

## Performance Considerations

- **API Mode**: Faster response times, uses quota
- **CLI Mode**: May be slightly slower, no quota usage
- **AUTO Mode**: Best of both - fast when quota available, seamless fallback

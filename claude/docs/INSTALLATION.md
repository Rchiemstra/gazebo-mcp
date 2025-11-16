# Installation Guide

Complete guide for setting up the Claude Learning System with Python SDK integration.

## Prerequisites

- **Python**: 3.8 or higher
- **pip**: Latest version
- **Git**: For cloning the repository
- **Anthropic API Key**: Get one from [console.anthropic.com](https://console.anthropic.com/)

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd claude_code
```

### 2. Create Virtual Environment

Using `venv`:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Using `conda`:

```bash
conda create -n claude-learning python=3.10
conda activate claude-learning
```

### 3. Install Dependencies

For basic usage:

```bash
pip install -e .
```

For development (includes testing tools):

```bash
pip install -e ".[dev]"
```

### 4. Configure Environment

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```bash
ANTHROPIC_API_KEY=your_api_key_here
CLAUDE_MODEL=claude-sonnet-4-5-20250929
MAX_TOKENS=8192
TEMPERATURE=1.0
PERMISSION_MODE=ask
```

### 5. Verify Installation

Run a test to verify everything works:

```bash
python -c "from claude_learning import AgentClient; print('✓ Installation successful')"
```

Run the test suite:

```bash
pytest
```

## Quick Verification

Try a simple example:

```python
# test_setup.py
import asyncio
from claude_learning import AgentClient, AgentType

async def test():
    try:
        client = AgentClient.from_env()
        print("✓ Client initialized successfully")
        print(f"✓ API key configured: {client.config.api_key[:10]}...")
        print(f"✓ Model: {client.config.model}")
        print("✓ Setup complete!")
    except Exception as e:
        print(f"✗ Error: {e}")

asyncio.run(test())
```

Run it:

```bash
python test_setup.py
```

## Directory Structure After Installation

```
claude_code/
├── venv/                    # Virtual environment
├── src/
│   └── claude_learning.egg-info/  # Package metadata
├── .env                     # Your configuration (not committed)
└── ...                      # Rest of the project
```

## Troubleshooting

### ImportError: No module named 'claude_agent_sdk'

The `claude-agent-sdk` should be installed automatically. If not:

```bash
pip install claude-agent-sdk
```

### API Key Not Found

Ensure `.env` file is in the project root:

```bash
ls -la .env
cat .env  # Verify ANTHROPIC_API_KEY is set
```

Or set it in your shell:

```bash
export ANTHROPIC_API_KEY=your_key_here
```

### Permission Denied Errors

On Linux/Mac, ensure proper permissions:

```bash
chmod 755 examples/*.py
```

### Python Version Issues

Check your Python version:

```bash
python --version  # Should be 3.8+
```

Use specific version if needed:

```bash
python3.10 -m venv venv
```

## Next Steps

1. **Run Examples**: `python examples/basic_query.py`
2. **Read Documentation**: See [SDK_INTEGRATION.md](./SDK_INTEGRATION.md)
3. **Explore Agents**: Browse `agents/` directory
4. **Create Your First Plan**: Try examples/create_plan.py

## Updating

To update the SDK:

```bash
pip install --upgrade claude-agent-sdk
```

To update the project:

```bash
git pull
pip install -e ".[dev]"
```

## Uninstalling

```bash
pip uninstall claude-learning-system claude-agent-sdk
deactivate  # Exit virtual environment
rm -rf venv  # Remove virtual environment
```

## Support

For issues:
- Check the [SDK_INTEGRATION.md](./SDK_INTEGRATION.md) guide
- Review example code in `examples/`
- Consult API docs: https://docs.claude.com/en/api/agent-sdk/python

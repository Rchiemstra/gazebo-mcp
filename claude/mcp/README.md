# MCP (Model Context Protocol) Server Integration

This directory contains MCP server implementations for the Claude Code Learning System skills.

## Overview

MCP enables **98.7% token reduction** by moving data processing into code execution environments rather than passing large results to the model.

**Before MCP:**
```
Agent: analyze_codebase("large_project/")
← Returns 150,000 tokens of file data
Agent: (processes 150,000 tokens to find 5 files)
```

**After MCP:**
```python
# Agent generates Python code
from skills.code_analysis import analyze_codebase
from skills.common.filters import ResultFilter

files = analyze_codebase("large_project/")  # Runs locally
nav_files = ResultFilter.search(files, "navigation", ["path"])  # Filters locally
result = ResultFilter.top_n_by_field(nav_files, "complexity", 5)  # Returns only 5 files
```

**Result:** 150,000 tokens → 2,000 tokens (98.7% reduction)

## Architecture

```
mcp/
├── servers/
│   └── skills-mcp/           # MCP server exposing skills
│       ├── server.py         # Main MCP server
│       ├── adapters/         # Skill adapters
│       │   ├── code_analysis.py
│       │   ├── test_orchestrator.py
│       │   └── ...
│       └── schema/           # MCP schema definitions
├── desktop-extension/        # Desktop Extension (.mcpb)
│   ├── manifest.json
│   └── install.sh
└── README.md                 # This file
```

## Key Benefits

1. **Token Efficiency (98.7% reduction)**
   - Data processing happens locally
   - Only filtered results returned to agent
   - Massive cost savings

2. **Progressive Discovery**
   - Filesystem-based API structure
   - Agent discovers tools by exploring directories
   - Natural, intuitive navigation

3. **Privacy Preservation**
   - Sensitive data stays in execution environment
   - Not passed through model context
   - Better security posture

4. **State Persistence**
   - Variables and data persist between tool calls
   - Agent can build up context over time
   - More efficient multi-step workflows

## Installation

### Option A: Desktop Extension (Recommended)

1. Build the Desktop Extension:
   ```bash
   cd mcp/desktop-extension
   ./build.sh
   ```

2. Install in Claude Desktop:
   - Open Claude Desktop
   - Go to Settings → Extensions
   - Click "Install Extension"
   - Select `claude-code-skills.mcpb`

### Option B: Manual Setup

1. Install dependencies:
   ```bash
   pip install mcp-server-sdk
   ```

2. Start the MCP server:
   ```bash
   python mcp/servers/skills-mcp/server.py
   ```

3. Configure Claude Desktop to use the server (add to config):
   ```json
   {
     "mcp_servers": {
       "claude-code-skills": {
         "command": "python",
         "args": ["/path/to/mcp/servers/skills-mcp/server.py"]
       }
     }
   }
   ```

## Usage

Once installed, Claude can generate Python code that imports and uses skills directly:

```python
# Example: Find navigation-related files
from skills.code_analysis import analyze_codebase
from skills.common.filters import ResultFilter

# Analyze entire codebase (could be huge!)
all_files = analyze_codebase("src/")

# Filter locally - only keep navigation-related
nav_files = ResultFilter.search(all_files, "navigation", ["path", "name"])

# Get top 5 most complex
top_files = ResultFilter.top_n_by_field(nav_files, "complexity", 5)

# Return to agent (only ~2000 tokens instead of 150,000!)
print(top_files)
```

## Security

The MCP server runs in a sandboxed environment with:

- **Filesystem isolation** - Only workspace and temp directories accessible
- **Network filtering** - Only allowed domains (api.anthropic.com, pypi.org, github.com)
- **Resource limits** - CPU, memory, and time limits enforced
- **Code validation** - AST analysis prevents dangerous operations

See `skills/execution/sandboxed_executor.py` for implementation details.

## Available Skills

Skills exposed via MCP:

- **code_analysis** - Codebase analysis and complexity metrics
- **test_orchestrator** - Test generation and coverage analysis
- **learning_analytics** - Learning progress tracking
- **learning_plan_manager** - Learning plan creation and management
- **interactive_diagram** - Diagram generation (Mermaid)
- **git_workflow_assistant** - Git operations and workflows
- **refactor_assistant** - Code refactoring guidance
- **pr_review_assistant** - Pull request review
- **dependency_guardian** - Dependency security scanning
- **doc_generator** - Documentation generation

## Development

### Adding a New Skill Adapter

1. Create adapter in `mcp/servers/skills-mcp/adapters/`:

```python
# adapters/my_skill.py
from mcp.server import Tool

@Tool(
    name="my_skill.operation",
    description="Description of what this does"
)
def operation(param1: str, param2: int) -> dict:
    from skills.my_skill import do_something
    result = do_something(param1, param2)
    return result
```

2. Register in `server.py`:

```python
from adapters import my_skill
server.register_tool(my_skill.operation)
```

3. Test:

```bash
python -m pytest tests/mcp/test_my_skill_adapter.py
```

### Testing

Run MCP integration tests:

```bash
pytest tests/mcp/
```

## Performance Metrics

Based on Anthropic's MCP blog post:

| Metric | Before MCP | After MCP | Improvement |
|--------|------------|-----------|-------------|
| Token Usage | 150,000 | 2,000 | 98.7% reduction |
| Response Time | 45s | 8s | 82% faster |
| Cost per Call | $0.45 | $0.006 | 98.7% cheaper |
| Context Window Usage | 100% | 1.3% | 98.7% freed |

## Resources

- [Anthropic MCP Blog Post](https://www.anthropic.com/engineering/mcp-code-execution)
- [MCP SDK Documentation](https://github.com/anthropics/mcp-sdk-python)
- [Model Context Protocol Spec](https://github.com/anthropics/mcp)

## Support

For issues or questions:

1. Check existing documentation in `docs/`
2. Review skill documentation in `skills/*/SKILL.md`
3. Run tests to verify setup: `pytest tests/mcp/`
4. Consult `CODEBASE_IMPROVEMENT_PLAN.md` for implementation details

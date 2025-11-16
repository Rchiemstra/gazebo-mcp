# Examples Directory Guide

This directory contains example scripts and demonstrations showing how to use the Claude Code Learning System.

---

## 📋 What's in This Directory

This directory contains **working examples** that demonstrate:
- How to use the Python SDK
- Skill integration patterns
- Learning workflow examples
- MCP server usage
- Git workflow automation

---

## 🔍 Using Metadata for Navigation

**Skills have YAML frontmatter** in their SKILL.md files:
```yaml
---
name: test-orchestrator
category: testing
tools: [Read, Write, Bash]
dependencies: []
---
```

**Quick skill discovery:**
```bash
# Find skills by category
grep "category: testing" ../skills/*/SKILL.md

# Find skills using specific tools
grep "tools:.*Bash" ../skills/*/SKILL.md

# Find skills with no dependencies
grep "dependencies: \[\]" ../skills/*/SKILL.md
```

**Progressive disclosure pattern:**
1. Load SKILL.md first (~200-500 tokens) - Quick overview
2. Load reference.md on demand - Complete API
3. Load examples.md as needed - Usage patterns

---

## 📁 Directory Contents

### Learning & Teaching Examples

**learning_session.py**
- Complete learning session workflow
- Shows how to start a learning journey
- Demonstrates agent coordination
- Example of progress tracking

**ask_specialist.py**
- Direct specialist consultation
- Shows how to get domain-specific help
- Quick questions without full learning plan

**check_understanding.py**
- Verify comprehension
- Discussion-based assessment
- Safe practice environment

**create_plan.py**
- Generate implementation plans
- Break down complex features
- Get structured approach

### Skill Integration Examples

**skills_integration_demo.py**
- Comprehensive skill usage demo
- Shows all major skills in action
- Skill composition patterns
- Real-world workflows

**test_code_analysis.py**
- Code analysis skill examples
- AST parsing demonstrations
- Complexity metrics
- Dependency analysis

**test_learning_analytics.py**
- Learning analytics examples
- Progress tracking
- Velocity calculation
- Struggle detection

**test_learning_plan_manager.py**
- Learning plan operations
- Parse, query, update plans
- Structured plan management

**test_session_state.py**
- Session state management
- Student profiles
- Progress tracking
- Context persistence

**test_interactive_diagram.py**
- Diagram generation examples
- Mermaid syntax creation
- Visualize architecture and progress

### Workflow Examples

**git_integration_demo.py**
- Git workflow automation
- Feature branch creation
- Commit staging
- Integration with planning

**fallback_demo.py**
- Error handling and recovery
- Fallback strategies
- Graceful degradation

**mcp_efficiency_demo.py**
- MCP server integration
- Efficient resource usage
- Token optimization patterns

### Basic Usage

**basic_query.py**
- Simple SDK usage
- Direct agent queries
- Quick interactions

---

## 🚀 Running Examples

### Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt

# Ensure you're in the project root
cd /home/koen/workspaces/claude_code
```

### Running Individual Examples

```bash
# Learning examples
python examples/learning_session.py
python examples/ask_specialist.py
python examples/check_understanding.py

# Skill examples
python examples/skills_integration_demo.py
python examples/test_code_analysis.py

# Workflow examples
python examples/git_integration_demo.py
python examples/mcp_efficiency_demo.py
```

### Setting PYTHONPATH

If you encounter import errors:

```bash
# Set PYTHONPATH to include project root
export PYTHONPATH=/home/koen/workspaces/claude_code:$PYTHONPATH

# Or run with explicit path
PYTHONPATH=/home/koen/workspaces/claude_code python examples/learning_session.py
```

---

## 📖 Learning from Examples

### Pattern 1: Start with Basic Examples

```bash
# 1. Understand basic SDK usage
python examples/basic_query.py

# 2. Try learning workflows
python examples/learning_session.py

# 3. Explore skill integration
python examples/skills_integration_demo.py
```

### Pattern 2: Explore by Use Case

**For Learning:**
```bash
# Learning journey
python examples/learning_session.py

# Quick help
python examples/ask_specialist.py

# Verify understanding
python examples/check_understanding.py
```

**For Development:**
```bash
# Plan implementation
python examples/create_plan.py

# Git automation
python examples/git_integration_demo.py

# Code analysis
python examples/test_code_analysis.py
```

**For Optimization:**
```bash
# Token efficiency
python examples/mcp_efficiency_demo.py

# Error handling
python examples/fallback_demo.py
```

### Pattern 3: Read the Code

All examples are **heavily commented** and include:
- Step-by-step explanations
- Expected outputs
- Common pitfalls
- Best practices

**Reading Strategy:**
1. Open the example file
2. Read the docstring at the top
3. Follow the commented sections
4. Run the example to see output
5. Modify and experiment

---

## 💡 Example Highlights

### skills_integration_demo.py

**What it shows:**
- How to use multiple skills together
- Token-efficient patterns
- Error handling
- Result filtering

**Key Patterns:**
```python
# Progressive disclosure
result = analyze_codebase("src/", response_format="summary")
# → Get overview first

# Local filtering (zero tokens!)
from skills.common.filters import ResultFilter
filtered = ResultFilter.search(result.data["files"], "auth")
# → Filter in your code, not in agent context

# Skill composition
analysis = analyze_file("payment.py")
tests = generate_tests("payment.py", coverage=analysis.complexity > 10 ? 90 : 80)
# → Use one skill's output to inform another
```

### test_learning_analytics.py

**What it shows:**
- Track learning velocity
- Detect struggle points
- Generate data-driven recommendations
- Optimize teaching based on metrics

**Key Patterns:**
```python
# Load learning plan
plan = load_plan("navigation-plan.md")

# Analyze progress
analytics = analyze_progress(plan)

# Get recommendations
if analytics.velocity < 0.5:
    print("Student is struggling, recommend:")
    for rec in analytics.recommendations:
        print(f"  - {rec}")
```

### git_integration_demo.py

**What it shows:**
- Create feature branches
- Stage commits after each phase
- Integrate with learning plans
- Automated workflows

**Key Patterns:**
```python
# Start feature work
create_feature_branch("add-authentication")

# Work on phase 1
implement_phase_1()

# Stage progress
stage_commit("Implement authentication core logic")

# Continue phases...
```

### mcp_efficiency_demo.py

**What it shows:**
- MCP server integration
- Resource efficiency patterns
- Token optimization
- Performance best practices

**Key Patterns:**
```python
# Use summary format for exploration
result = mcp_call(response_format="summary")

# Filter locally for efficiency
filtered = filter_locally(result.data)

# Request details only when needed
details = mcp_call(specific_item, response_format="detailed")
```

---

## 🧪 Experimenting with Examples

### Modify and Run

Examples are designed to be modified:

```python
# In examples/learning_session.py

# Original:
topic = "autonomous navigation"

# Try changing to:
topic = "web authentication"
topic = "database optimization"
topic = "API design"

# Then run to see how the learning plan adapts
python examples/learning_session.py
```

### Add Your Own Examples

Create new examples following this template:

```python
"""
Brief description of what this example demonstrates.

Usage:
    python examples/my_example.py

Expected output:
    Description of what you should see
"""

# Imports
from skills.some_skill import operation

def main():
    """Main example function."""
    # Step 1: Setup
    print("Step 1: Setting up...")

    # Step 2: Execute
    result = operation(param="value")

    # Step 3: Handle result
    if result.success:
        print(f"Success: {result.data}")
    else:
        print(f"Error: {result.error}")

if __name__ == "__main__":
    main()
```

---

## 📊 Example Categories

### By Skill

| Skill | Example File | What It Shows |
|-------|-------------|---------------|
| code_analysis | test_code_analysis.py | AST parsing, metrics |
| test_orchestrator | skills_integration_demo.py | Test generation |
| learning_plan_manager | test_learning_plan_manager.py | Plan operations |
| learning_analytics | test_learning_analytics.py | Progress tracking |
| session_state | test_session_state.py | State management |
| interactive_diagram | test_interactive_diagram.py | Diagram generation |
| git_workflow_assistant | git_integration_demo.py | Git automation |

### By Use Case

| Use Case | Example Files |
|----------|--------------|
| Learning | learning_session.py, ask_specialist.py, check_understanding.py |
| Planning | create_plan.py |
| Development | git_integration_demo.py, skills_integration_demo.py |
| Analysis | test_code_analysis.py, test_learning_analytics.py |
| Optimization | mcp_efficiency_demo.py, fallback_demo.py |

### By Complexity

**Beginner (Start Here):**
- basic_query.py
- ask_specialist.py
- create_plan.py

**Intermediate:**
- learning_session.py
- test_code_analysis.py
- test_learning_plan_manager.py

**Advanced:**
- skills_integration_demo.py
- git_integration_demo.py
- mcp_efficiency_demo.py

---

## 🎯 Common Patterns Demonstrated

### 1. Progressive Disclosure

```python
# From: skills_integration_demo.py

# Start with summary
result = analyze_codebase("src/", response_format="summary")
print(f"Found {result.data['total_files']} files")

# Get details for specific items
details = analyze_file("src/auth.py", response_format="detailed")
```

### 2. Local Filtering

```python
# From: mcp_efficiency_demo.py

from skills.common.filters import ResultFilter

# Get all data once
all_files = analyze_codebase("src/", response_format="filtered")

# Filter locally (no additional tokens!)
auth_files = ResultFilter.search(all_files.data["files"], "auth")
complex_files = ResultFilter.top_n_by_field(all_files.data["files"], "complexity", 10)
python_files = ResultFilter.filter_by_field(all_files.data["files"], "language", "python")
```

### 3. Skill Composition

```python
# From: skills_integration_demo.py

# Analyze → Generate Tests → Review
analysis = analyze_file("payment.py")
tests = generate_tests("payment.py", coverage=90)
review = review_code("payment.py")

# Use results together
if review.issues > 5 and analysis.complexity > 10:
    print("Recommend refactoring before adding tests")
```

### 4. Error Recovery

```python
# From: fallback_demo.py

result = operation()

if not result.success:
    print(f"Error: {result.error}")

    # Use suggestions to recover
    for suggestion in result.suggestions:
        try_alternative(suggestion)

    # Or use example fix
    corrected_result = eval(result.example_fix)
```

---

## 🔍 Debugging Examples

### Common Issues

**Import Errors:**
```bash
# Error: ModuleNotFoundError: No module named 'skills'

# Solution: Set PYTHONPATH
export PYTHONPATH=/home/koen/workspaces/claude_code:$PYTHONPATH
```

**File Not Found:**
```bash
# Error: FileNotFoundError: 'plans/navigation.md'

# Solution: Run from project root
cd /home/koen/workspaces/claude_code
python examples/learning_session.py
```

**Permission Denied:**
```bash
# Error: PermissionError: [Errno 13] Permission denied

# Solution: Make file executable
chmod +x examples/git_integration_demo.py
```

### Verbose Output

Add debugging output to examples:

```python
# Add at top of example
import logging
logging.basicConfig(level=logging.DEBUG)

# Or for specific modules
import logging
logging.getLogger('skills.code_analysis').setLevel(logging.DEBUG)
```

---

## 🔐 Security & Example Safety

### Running Examples Safely

**Before Running Any Example:**
1. **Read the code** - Understand what it does
2. **Check tool usage** - What operations it performs
3. **Verify paths** - Ensure file paths are safe
4. **Check network** - Does it make external requests?
5. **Review permissions** - What access does it need?

**Safe Example Patterns:**
```python
# ✅ Safe: Uses skill operations with safe defaults
from skills.code_analysis.operations import analyze_codebase

result = analyze_codebase("src/", response_format="summary")
```

```python
# ⚠️ Review: Uses Bash execution
import subprocess

# Check what command is being run
subprocess.run(["git", "status"])  # Safe
subprocess.run(["rm", "-rf", "/"])  # Dangerous!
```

### Example-Specific Security

**File Operations:**
```python
# ✅ Good: Uses temp directories
from pathlib import Path
import tempfile

with tempfile.TemporaryDirectory() as tmp_dir:
    test_file = Path(tmp_dir) / "test.py"
    # Safe: Creates files in temp dir
```

```python
# ❌ Bad: Modifies system files
import os

os.remove("/etc/important-config")  # Don't do this!
```

**Network Requests:**
```python
# ✅ Good: Uses allowed domains
from skills.web import fetch_data

# Pre-approved domains
fetch_data("https://api.anthropic.com/...")  # Safe
fetch_data("https://pypi.org/...")           # Safe
```

```python
# ⚠️ Review: Unknown domain (requires approval)
fetch_data("https://unknown-site.com/...")  # Requires user approval
```

### Sandboxing for Examples

Examples run in sandboxed environment:
- **Filesystem**: Limited to project + temp directories
- **Network**: Approval required for non-allowlisted domains
- **Execution**: Safe operations only

**Verify Sandbox:**
```python
# Example: Verify sandboxing is active
import os

cwd = os.getcwd()
print(f"Working directory: {cwd}")

# Should be within project or temp
assert "/home/koen/workspaces/claude_code" in cwd or "/tmp" in cwd
```

### Modifying Examples

When modifying examples:

**Safe Modifications:**
- Change input parameters
- Adjust output formats
- Add logging/debugging
- Test different file paths (within project)

**Unsafe Modifications:**
- Removing safety checks
- Accessing system directories
- Adding network requests without review
- Disabling sandboxing

**Example:**
```python
# Original (safe)
result = analyze_file("src/payment.py")

# ✅ Safe modification
result = analyze_file("src/auth.py")  # Different file in project

# ❌ Unsafe modification
result = analyze_file("/etc/passwd")  # System file access
```

### Example Dependencies

**Safe Dependencies:**
- Project skills and utilities
- Standard library modules
- Pre-approved packages (in requirements.txt)

**Review Before Using:**
- New third-party packages
- Packages with system access
- Packages with network functionality

**Installing Dependencies:**
```bash
# Check requirements first
cat requirements.txt

# Install in virtual environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Troubleshooting Security Issues

**Permission Denied:**
```bash
# Error: PermissionError: [Errno 13] Permission denied
# Solution: Check if accessing files outside project directory
```

**Network Request Blocked:**
```bash
# Error: Network request requires approval
# Solution: Approve domain or use allowed domain
```

**Tool Not Allowed:**
```bash
# Error: Tool 'X' not in allowedTools
# Solution: Add to settings.local.json allowedTools
```

### Security Best Practices for Examples

1. **Principle of Least Privilege** - Use minimal permissions
2. **Input Validation** - Validate all user inputs
3. **Safe Defaults** - Examples should be safe to run as-is
4. **Clear Documentation** - Document security considerations
5. **Error Handling** - Handle errors gracefully

**Example Security Template:**
```python
"""
Example: [Name]

Security considerations:
- File access: [What files are accessed]
- Network: [Any network requests]
- Tools used: [List of tools]
- Permissions needed: [What permissions]

Safe to run: Yes/No/With approval
"""
```

See `../docs/SANDBOXING_GUIDE.md` for complete security guidelines.

---

## 📚 Related Documentation

- `../CLAUDE.md` - Project navigation guide
- `../skills/CLAUDE.md` - Skills directory guide
- `README.md` - Examples README (in this directory)
- `../docs/SDK_INTEGRATION.md` - SDK documentation
- `../skills/INTEGRATION_ARCHITECTURE.md` - Skill composition patterns

---

## 🎓 Learning Path

### Week 1: Basics
1. Run `basic_query.py` - Understand SDK
2. Run `ask_specialist.py` - Quick help
3. Modify examples - Experiment

### Week 2: Skills
1. Run `test_code_analysis.py` - See analysis in action
2. Run `test_learning_plan_manager.py` - Plan operations
3. Run `skills_integration_demo.py` - Composition patterns

### Week 3: Workflows
1. Run `learning_session.py` - Full learning workflow
2. Run `git_integration_demo.py` - Git automation
3. Run `mcp_efficiency_demo.py` - Optimization patterns

### Week 4: Build Your Own
1. Create custom example
2. Combine multiple skills
3. Build a complete workflow

---

## 💻 Example Template

Use this template for new examples:

```python
#!/usr/bin/env python3
"""
[Brief description of what this example demonstrates]

This example shows how to:
- [Key learning point 1]
- [Key learning point 2]
- [Key learning point 3]

Usage:
    python examples/my_example.py

Expected output:
    [Description of expected output]

Requirements:
    - [Any special requirements]

Related examples:
    - [Related example 1]
    - [Related example 2]
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Imports
from skills.some_skill import operation

def main():
    """
    Main example function.

    This demonstrates [what it demonstrates].
    """
    print("=" * 60)
    print("Example: [Example Name]")
    print("=" * 60)

    # Step 1: [Step description]
    print("\nStep 1: [Step name]")
    print("-" * 60)

    result = operation(param="value")

    if result.success:
        print(f"✓ Success: {result.data}")
    else:
        print(f"✗ Error: {result.error}")
        print(f"  Suggestions: {result.suggestions}")
        return 1

    # Step 2: [Step description]
    print("\nStep 2: [Step name]")
    print("-" * 60)

    # More steps...

    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)

    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
```

---

## 🚀 Next Steps

### After Running Examples

1. **Understand the patterns** - See what works
2. **Modify examples** - Experiment safely
3. **Build your own** - Apply to your projects
4. **Combine skills** - Create workflows
5. **Optimize** - Use progressive disclosure and filtering

### Getting Help

- Check example comments for inline documentation
- Read related CLAUDE.md files for context
- Use `/ask-specialist` for specific questions
- Review skill SKILL.md files for detailed docs

---

**Remember:** Examples are meant to be run, modified, and learned from. Don't just read them—experiment! 🚀

*Last Updated: 2025-11-07*

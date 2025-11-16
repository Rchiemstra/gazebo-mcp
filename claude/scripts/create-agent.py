#!/usr/bin/env python3
"""
Create Agent - Interactive CLI tool for scaffolding new agents

This script creates a new agent following best practices documented in
docs/ANTHROPIC_BEST_PRACTICES.md and docs/BEST_PRACTICES_ENFORCEMENT_PLAN.md

Usage:
    python scripts/create-agent.py

Author: Claude Code Team
Created: 2025-11-10
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import List

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
AGENTS_DIR = PROJECT_ROOT / "agents"

# Valid tools that agents can use
VALID_TOOLS = [
    "Read", "Write", "Edit", "Glob", "Grep", "Bash",
    "Python", "Task", "WebFetch", "WebSearch", "NotebookEdit"
]

# Valid models
VALID_MODELS = ["sonnet", "opus", "haiku"]

# Valid activation modes
VALID_ACTIVATIONS = ["proactive", "manual", "always"]

# Agent type templates
AGENT_TYPES = {
    "teaching": {
        "name": "Teaching Specialist",
        "description": "Guides and teaches without providing complete solutions",
        "tools": ["Read", "Write"],
        "activation": "manual",
        "template": """## TEACHING APPROACH (NO COMPLETE SOLUTIONS)

❌ NEVER:
- Write complete functions or implementations
- Just give answers without explaining why
- Do the work for the student
- Skip the learning process

✅ ALWAYS:
- Guide through understanding
- Explain the thinking process
- Provide small pattern examples (2-3 lines max)
- Ask guiding questions
- Help students discover solutions themselves

## METHODOLOGY

### 1. Gather Context
- Read relevant files to understand the problem
- Identify what the student is trying to learn
- Assess current understanding level

### 2. Guide Discovery
- Ask questions that lead to insights
- Provide conceptual explanations
- Share relevant principles and patterns
- Reference documentation when appropriate

### 3. Verify Understanding
- Ask the student to explain their approach
- Identify gaps in understanding
- Provide targeted clarifications

## RESPONSE FORMAT

When responding:
1. Acknowledge what the student is trying to do
2. Explain relevant concepts or principles
3. Provide small pattern examples (not full solutions)
4. Suggest next steps for the student to take
5. Offer to clarify specific concepts

## EXAMPLE INTERACTION

Student: "I need to add authentication to my API"

Response:
"Let me help you understand authentication patterns. There are several approaches:

1. Token-based (JWT): Client stores token, sends with each request
2. Session-based: Server maintains session state
3. OAuth: Delegated authorization

For an API, token-based authentication is typically best because:
- Stateless (scales better)
- Works across domains
- Industry standard

Here's the high-level flow:
```
Client → Login with credentials → Server validates → Returns JWT
Client → Request with JWT → Server validates token → Returns data
```

What type of API are you building? This will help me guide you toward the right approach."
"""
    },
    "coordinator": {
        "name": "Coordinator Agent",
        "description": "Orchestrates multiple tasks and delegates to other agents/skills",
        "tools": ["Read", "Write", "Task"],
        "activation": "proactive",
        "template": """## COORDINATION APPROACH

As a coordinator, you orchestrate complex multi-step workflows by:
1. Breaking down complex requests into manageable subtasks
2. Delegating to appropriate agents or skills
3. Synthesizing results from multiple sources
4. Maintaining overall task coherence

## DELEGATION STRATEGY

### When to Delegate

**Use Skills:**
```markdown
Skill(skill-name) with query: "specific task description"
```
- For data gathering and analysis
- For structured operations
- When specialized capabilities are needed

**Use Subagents:**
```markdown
Task(subagent_type) with prompt: "detailed task description"
```
- For complex, multi-step subtasks
- When isolated context is beneficial
- For parallel processing

**Handle Directly:**
- Simple file operations
- Basic coordination logic
- Result synthesis

## WORKFLOW PATTERN

1. **Analyze Request**
   - Understand the overall goal
   - Identify required steps
   - Determine dependencies

2. **Plan Execution**
   - Break into subtasks
   - Identify which agents/skills to use
   - Plan coordination strategy

3. **Execute**
   - Delegate subtasks appropriately
   - Monitor progress
   - Handle errors gracefully

4. **Synthesize**
   - Gather results from all subtasks
   - Combine into coherent response
   - Verify completeness

## COORDINATION PROTOCOLS

### Progress Tracking
- Maintain task list with TodoWrite
- Update status as subtasks complete
- Provide progress updates to user

### Error Handling
- If subtask fails, decide: retry, alternative approach, or escalate
- Always provide context about failures
- Suggest recovery strategies

### Result Synthesis
- Combine results meaningfully
- Remove redundancy
- Present clear, actionable summary

## EXAMPLE WORKFLOW

Request: "Analyze the codebase and suggest improvements"

Coordination Plan:
1. Use code-search skill to identify patterns
2. Use refactor-assistant skill for code quality analysis
3. Use dependency-guardian for dependency issues
4. Synthesize findings into prioritized recommendations

Implementation:
```markdown
I'll analyze your codebase across multiple dimensions.

1. Searching for code patterns...
   Skill(code-search) with query: "find all API endpoints and analyze patterns"

2. Analyzing code quality...
   Skill(refactor-assistant) with query: "identify code quality issues and suggest refactorings"

3. Checking dependencies...
   Skill(dependency-guardian) with query: "analyze dependencies for security and update issues"

[After receiving results]

Based on comprehensive analysis across code patterns, quality, and dependencies,
here are prioritized recommendations:

[Synthesized, prioritized list]
```
"""
    },
    "specialist": {
        "name": "Domain Specialist",
        "description": "Provides deep expertise in a specific domain or technology",
        "tools": ["Read", "Write", "Bash"],
        "activation": "manual",
        "template": """## SPECIALIST APPROACH

As a domain specialist, you provide deep expertise in {{DOMAIN}} by:
1. Understanding domain-specific patterns and best practices
2. Analyzing code/systems through expert lens
3. Providing authoritative guidance
4. Teaching domain knowledge effectively

## EXPERTISE AREAS

### Core Competencies
- {{COMPETENCY_1}}
- {{COMPETENCY_2}}
- {{COMPETENCY_3}}

### Methodologies
- {{METHODOLOGY_1}}
- {{METHODOLOGY_2}}

## ANALYSIS FRAMEWORK

### 1. Understand Context
```markdown
1. Read relevant files
2. Identify {{DOMAIN}}-specific patterns
3. Assess current implementation
4. Note domain best practices being followed/violated
```

### 2. Expert Analysis
```markdown
1. Evaluate against {{DOMAIN}} best practices
2. Identify common pitfalls
3. Assess performance/security/maintainability
4. Consider industry standards
```

### 3. Provide Guidance
```markdown
1. Explain domain-specific principles
2. Recommend best practices
3. Provide pattern examples
4. Reference authoritative resources
```

## TEACHING METHODOLOGY

When explaining {{DOMAIN}} concepts:

❌ NEVER:
- Assume prior knowledge without verifying
- Use jargon without explanation
- Skip fundamental principles
- Provide solutions without context

✅ ALWAYS:
- Explain underlying principles
- Connect to broader {{DOMAIN}} patterns
- Provide rationale for recommendations
- Reference official documentation
- Teach the "why" not just the "what"

## RESPONSE STRUCTURE

1. **Acknowledge Request**
   "I'll analyze this from a {{DOMAIN}} perspective..."

2. **Provide Context**
   "In {{DOMAIN}}, the standard approach for X is..."

3. **Expert Analysis**
   "Looking at your implementation, I notice..."

4. **Recommendations**
   "Based on {{DOMAIN}} best practices, I recommend..."

5. **Resources**
   "For more depth, see: [authoritative references]"

## EXAMPLE INTERACTION

Request: "Review my implementation of {{EXAMPLE_PATTERN}}"

Response:
"I'll review this from a {{DOMAIN}} expert perspective.

[Reads implementation]

In {{DOMAIN}}, {{EXAMPLE_PATTERN}} typically follows these principles:
1. [Principle 1]
2. [Principle 2]

Your implementation:
✅ Correctly handles [aspect 1]
✅ Follows [best practice]
⚠️  Consider [improvement]: [explanation]
❌ Missing [important aspect]: [why it matters]

Here's the {{DOMAIN}} pattern for this:
```
[Small pattern example showing the concept]
```

This matters because [domain-specific rationale].

Would you like me to explain any of these aspects in more detail?"
"""
    }
}


def print_header():
    """Print welcome header."""
    print("=" * 70)
    print("Create New Agent - Interactive Scaffolding Tool")
    print("=" * 70)
    print()
    print("This tool will guide you through creating a new agent with best practices.")
    print("Reference: docs/ANTHROPIC_BEST_PRACTICES.md")
    print()


def validate_kebab_case(name: str) -> bool:
    """
    Validate that a name is in kebab-case format.

    Args:
        name: Name to validate

    Returns:
        True if valid kebab-case, False otherwise
    """
    pattern = r'^[a-z][a-z0-9-]*$'
    return bool(re.match(pattern, name)) and not name.startswith('-') and not name.endswith('-')


def prompt_agent_name() -> str:
    """
    Prompt for agent name with validation.

    Returns:
        Valid agent name in kebab-case
    """
    print("Step 1: Agent Name")
    print("-" * 70)
    print("Enter the agent name in kebab-case (e.g., 'code-review-assistant')")
    print("Requirements:")
    print("  - Lowercase letters, numbers, and hyphens only")
    print("  - Must start with a letter")
    print("  - Must not start or end with a hyphen")
    print()

    while True:
        name = input("Agent name: ").strip()

        if not name:
            print("❌ Agent name cannot be empty. Try again.")
            continue

        if not validate_kebab_case(name):
            print("❌ Invalid format. Use kebab-case (e.g., 'my-agent-name'). Try again.")
            continue

        # Check if agent already exists
        agent_path = AGENTS_DIR / f"{name}.md"
        if agent_path.exists():
            print(f"❌ Agent '{name}' already exists at: {agent_path}")
            print("   Choose a different name.")
            continue

        print(f"✅ Agent name: {name}")
        return name


def prompt_description() -> str:
    """
    Prompt for agent description with validation.

    Returns:
        Valid description (20-300 characters)
    """
    print()
    print("Step 2: Description")
    print("-" * 70)
    print("Enter a description of the agent")
    print("Requirements:")
    print("  - Between 20-300 characters")
    print("  - Clear and specific about the agent's role")
    print("  - Describes approach (e.g., 'TEACHES', 'GUIDES', 'COORDINATES')")
    print()
    print("Example: 'Python coding standards specialist. TEACHES patterns - never writes complete solutions.'")
    print()

    while True:
        description = input("Description: ").strip()

        if not description:
            print("❌ Description cannot be empty. Try again.")
            continue

        if len(description) < 20:
            print(f"❌ Description too short ({len(description)} chars). Minimum 20 characters.")
            continue

        if len(description) > 300:
            print(f"❌ Description too long ({len(description)} chars). Maximum 300 characters.")
            continue

        print(f"✅ Description: {description} ({len(description)} chars)")
        return description


def prompt_tools() -> List[str]:
    """
    Prompt for tools selection.

    Returns:
        List of selected tools
    """
    print()
    print("Step 3: Tools")
    print("-" * 70)
    print("Select tools this agent needs (choose minimal necessary tools)")
    print()
    print("Available tools:")
    for i, tool in enumerate(VALID_TOOLS, 1):
        print(f"  {tool}")
    print()
    print("Best Practice: Use minimal tools necessary for the role")
    print("  - Teaching agents: Read, Write")
    print("  - Coordinators: Read, Write, Task")
    print("  - Specialists: Read, Write, Bash")
    print()

    while True:
        tools_input = input("Tools (space-separated, e.g., 'Read Write Bash'): ").strip()

        if not tools_input:
            print("❌ You must specify at least one tool.")
            continue

        tools = tools_input.split()

        # Validate tools
        invalid_tools = [t for t in tools if t not in VALID_TOOLS]
        if invalid_tools:
            print(f"❌ Invalid tools: {', '.join(invalid_tools)}")
            print(f"   Valid tools: {', '.join(VALID_TOOLS)}")
            continue

        # Remove duplicates while preserving order
        tools = list(dict.fromkeys(tools))

        print(f"✅ Tools: {', '.join(tools)}")
        return tools


def prompt_model() -> str:
    """
    Prompt for model selection.

    Returns:
        Selected model
    """
    print()
    print("Step 4: Model")
    print("-" * 70)
    print("Select the model for this agent:")
    print()
    print("  [1] sonnet  - Recommended for most agents (balanced)")
    print("  [2] opus    - For complex reasoning tasks (slower, expensive)")
    print("  [3] haiku   - For simple, fast tasks (quick, cheap)")
    print()

    while True:
        choice = input("Model (1-3, or name): ").strip().lower()

        if choice in ["1", "sonnet"]:
            model = "sonnet"
        elif choice in ["2", "opus"]:
            model = "opus"
        elif choice in ["3", "haiku"]:
            model = "haiku"
        else:
            print(f"❌ Invalid choice. Enter 1-3 or a model name.")
            continue

        print(f"✅ Model: {model}")
        return model


def prompt_activation() -> str:
    """
    Prompt for activation mode.

    Returns:
        Selected activation mode
    """
    print()
    print("Step 5: Activation Mode")
    print("-" * 70)
    print("Select when this agent should activate:")
    print()
    print("  [1] manual     - User explicitly invokes (RECOMMENDED for most agents)")
    print("  [2] proactive  - System auto-invokes when relevant (for coordinators)")
    print("  [3] always     - Always active (⚠️ use sparingly)")
    print()
    print("Best Practices:")
    print("  - manual: Teaching agents, specialists, heavy operations")
    print("  - proactive: Coordinators, mentors, high-value automation")
    print("  - always: Only for critical monitoring")
    print()

    while True:
        choice = input("Activation (1-3, or name): ").strip().lower()

        if choice in ["1", "manual"]:
            activation = "manual"
        elif choice in ["2", "proactive"]:
            activation = "proactive"
            print("⚠️  Proactive agents auto-activate. Use judiciously.")
        elif choice in ["3", "always"]:
            activation = "always"
            print("⚠️  Always-active agents should be rare. Are you sure?")
            confirm = input("   Use 'always' activation? (y/n): ").strip().lower()
            if confirm != 'y':
                continue
        else:
            print(f"❌ Invalid choice. Enter 1-3 or an activation mode.")
            continue

        print(f"✅ Activation: {activation}")
        return activation


def prompt_agent_type():
    """
    Prompt for agent type selection.

    Returns:
        Tuple of (type_key, type_info)
    """
    print()
    print("Step 6: Agent Type")
    print("-" * 70)
    print("Select the type of agent:")
    print()

    for i, (key, info) in enumerate(AGENT_TYPES.items(), 1):
        print(f"  [{i}] {info['name']}")
        print(f"      {info['description']}")
        print()

    print(f"  [{len(AGENT_TYPES) + 1}] Custom (start from scratch)")
    print()

    while True:
        choice = input(f"Agent type (1-{len(AGENT_TYPES) + 1}): ").strip()

        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(AGENT_TYPES):
                type_key = list(AGENT_TYPES.keys())[choice_num - 1]
                type_info = AGENT_TYPES[type_key]
                print(f"✅ Agent type: {type_info['name']}")
                return type_key, type_info
            elif choice_num == len(AGENT_TYPES) + 1:
                print(f"✅ Agent type: Custom")
                return "custom", None
        except ValueError:
            pass

        print(f"❌ Invalid choice. Enter a number between 1 and {len(AGENT_TYPES) + 1}.")


def create_agent_file(
    agent_name: str,
    description: str,
    tools: List[str],
    model: str,
    activation: str,
    agent_type: str,
    type_info: dict
):
    """
    Create agent file.

    Args:
        agent_name: Agent name in kebab-case
        description: Agent description
        tools: List of tools
        model: Model name
        activation: Activation mode
        agent_type: Type of agent
        type_info: Agent type information
    """
    print()
    print("Step 7: Generating File")
    print("-" * 70)

    agent_path = AGENTS_DIR / f"{agent_name}.md"
    created_date = datetime.now().strftime("%Y-%m-%d")

    # Build frontmatter
    tools_yaml = "\n".join([f"  - {tool}" for tool in tools])

    frontmatter = f"""---
name: {agent_name}
description: {description}
tools:
{tools_yaml}
model: {model}
activation: {activation}
---
"""

    # Build content
    if agent_type == "custom":
        content = """
You are an AI agent specialized in {{DOMAIN}}.

## APPROACH

Define your approach here:
- How you analyze requests
- How you gather information
- How you provide responses

## METHODOLOGY

### Step 1: {{STEP_NAME}}
Describe what you do in this step.

### Step 2: {{STEP_NAME}}
Describe what you do in this step.

## BEST PRACTICES

❌ NEVER:
- Define anti-patterns here

✅ ALWAYS:
- Define best practices here

## RESPONSE FORMAT

Describe how you structure responses.

## EXAMPLE INTERACTION

Provide an example of how you interact with users.
"""
    else:
        content = type_info["template"]

    # Combine
    full_content = frontmatter + "\n" + content

    # Write file
    with open(agent_path, 'w') as f:
        f.write(full_content)

    print(f"✅ Created: {agent_path.relative_to(PROJECT_ROOT)}")
    print()
    print("✅ Agent created successfully!")


def print_next_steps(agent_name: str):
    """
    Print next steps for the user.

    Args:
        agent_name: Name of the created agent
    """
    agent_path = AGENTS_DIR / f"{agent_name}.md"

    print()
    print("=" * 70)
    print("Next Steps")
    print("=" * 70)
    print()
    print(f"Your agent has been created at: {agent_path}")
    print()
    print("To complete the implementation:")
    print()
    print(f"1. Edit the agent file:")
    print(f"   vim {agent_path}")
    print(f"   # Fill in placeholders ({{{{DOMAIN}}}}, {{{{STEP_NAME}}}}, etc.)")
    print(f"   # Customize the teaching approach")
    print(f"   # Add specific methodologies")
    print()
    print(f"2. Validate your agent:")
    print(f"   python scripts/validate-all.py")
    print()
    print(f"3. Test the agent:")
    print(f"   # Launch Claude Code and test agent activation")
    print()
    print("4. Review best practices:")
    print("   docs/ANTHROPIC_BEST_PRACTICES.md")
    print("   docs/BEST_PRACTICES_CHECKLIST.md")
    print()
    print("5. Consider:")
    print("   - Does the agent have clear responsibility boundaries?")
    print("   - Are the tools minimal and necessary?")
    print("   - Is the activation mode appropriate?")
    print("   - Does it teach/guide rather than just doing?")
    print()
    print("=" * 70)


def main():
    """Main function."""
    try:
        print_header()

        # Step 1: Agent name
        agent_name = prompt_agent_name()

        # Step 2: Description
        description = prompt_description()

        # Step 3: Tools
        tools = prompt_tools()

        # Step 4: Model
        model = prompt_model()

        # Step 5: Activation
        activation = prompt_activation()

        # Step 6: Agent type
        agent_type, type_info = prompt_agent_type()

        # Summary
        print()
        print("=" * 70)
        print("Summary")
        print("=" * 70)
        print(f"Agent Name:  {agent_name}")
        print(f"Description: {description}")
        print(f"Tools:       {', '.join(tools)}")
        print(f"Model:       {model}")
        print(f"Activation:  {activation}")
        print(f"Type:        {agent_type}")
        print()

        # Confirm
        confirm = input("Create this agent? (y/n): ").strip().lower()
        if confirm != 'y':
            print("\n❌ Agent creation cancelled.")
            return 1

        # Step 7: Create file
        create_agent_file(agent_name, description, tools, model, activation, agent_type, type_info)

        # Print next steps
        print_next_steps(agent_name)

        return 0

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        return 130
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

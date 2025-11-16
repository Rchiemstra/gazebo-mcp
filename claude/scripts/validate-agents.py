#!/usr/bin/env python3
"""
Agent Validation Script

Validates all agent files against the agent schema and checks for common issues.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple

# YAML frontmatter extraction pattern
FRONTMATTER_PATTERN = r'^---\n(.*?)\n---'

# Valid tool names
VALID_TOOLS = [
    "Read", "Write", "Edit", "Glob", "Grep", "Bash", "Python",
    "Task", "WebFetch", "WebSearch", "NotebookEdit"
]

# Valid models
VALID_MODELS = ["sonnet", "opus", "haiku"]

# Valid activation modes
VALID_ACTIVATIONS = ["proactive", "manual", "always"]


def extract_frontmatter(content: str) -> Dict[str, Any]:
    """Extract YAML frontmatter from markdown file."""
    match = re.search(FRONTMATTER_PATTERN, content, re.DOTALL)
    if not match:
        return {}

    frontmatter_text = match.group(1)
    frontmatter = {}

    # Simple YAML parsing (handles our specific format)
    current_key = None
    current_list = []

    for line in frontmatter_text.split('\n'):
        line = line.strip()
        if not line:
            continue

        # Check for key-value pair
        if ':' in line and not line.startswith('-'):
            if current_key and current_list:
                frontmatter[current_key] = current_list
                current_list = []

            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            if value:  # Inline value
                frontmatter[key] = value
                current_key = None
            else:  # Start of list
                current_key = key
        elif line.startswith('-') and current_key:
            # List item
            item = line[1:].strip()
            current_list.append(item)

    # Add last list if exists
    if current_key and current_list:
        frontmatter[current_key] = current_list

    return frontmatter


def validate_agent(file_path: Path) -> Tuple[bool, List[str]]:
    """
    Validate a single agent file.

    Returns:
        (is_valid, list_of_errors)
    """
    errors = []

    try:
        content = file_path.read_text()
    except Exception as e:
        return False, [f"Failed to read file: {e}"]

    # Extract frontmatter
    frontmatter = extract_frontmatter(content)

    if not frontmatter:
        return False, ["No YAML frontmatter found"]

    # Check required fields
    required_fields = ["name", "description", "tools", "model"]
    for field in required_fields:
        if field not in frontmatter:
            errors.append(f"Missing required field: {field}")

    # Validate name format (kebab-case)
    if "name" in frontmatter:
        name = frontmatter["name"]
        if not re.match(r'^[a-z][a-z0-9-]*$', name):
            errors.append(f"Invalid name format: '{name}' (must be lowercase kebab-case)")

    # Validate description length
    if "description" in frontmatter:
        desc = frontmatter["description"]
        if len(desc) < 20:
            errors.append(f"Description too short: {len(desc)} chars (min 20)")
        if len(desc) > 300:
            errors.append(f"Description too long: {len(desc)} chars (max 300)")

    # Validate tools
    if "tools" in frontmatter:
        tools = frontmatter["tools"]
        if isinstance(tools, str):
            errors.append(f"Tools must be a list, not a string: '{tools}'")
        elif isinstance(tools, list):
            for tool in tools:
                if tool not in VALID_TOOLS:
                    errors.append(f"Invalid tool: '{tool}' (must be one of {VALID_TOOLS})")
        else:
            errors.append(f"Tools must be a list")

    # Validate model
    if "model" in frontmatter:
        model = frontmatter["model"]
        if model not in VALID_MODELS:
            errors.append(f"Invalid model: '{model}' (must be one of {VALID_MODELS})")

    # Validate activation (optional but recommended)
    if "activation" in frontmatter:
        activation = frontmatter["activation"]
        if activation not in VALID_ACTIVATIONS:
            errors.append(f"Invalid activation: '{activation}' (must be one of {VALID_ACTIVATIONS})")
    else:
        errors.append("Missing recommended field: activation (should be 'proactive' or 'manual')")

    is_valid = len(errors) == 0
    return is_valid, errors


def main():
    """Main validation routine."""
    # Find agents directory
    repo_root = Path(__file__).parent.parent
    agents_dir = repo_root / "agents"

    if not agents_dir.exists():
        print(f"❌ Agents directory not found: {agents_dir}")
        sys.exit(1)

    # Get all agent files
    agent_files = list(agents_dir.glob("*.md"))

    if not agent_files:
        print(f"❌ No agent files found in {agents_dir}")
        sys.exit(1)

    print(f"🔍 Validating {len(agent_files)} agent files...\n")

    # Validate each agent
    all_valid = True
    results = []

    for agent_file in sorted(agent_files):
        is_valid, errors = validate_agent(agent_file)
        results.append((agent_file.name, is_valid, errors))

        if not is_valid:
            all_valid = False

    # Print results
    valid_count = sum(1 for _, is_valid, _ in results if is_valid)

    print(f"📊 Validation Results: {valid_count}/{len(agent_files)} agents valid\n")

    for filename, is_valid, errors in results:
        if is_valid:
            print(f"✅ {filename}")
        else:
            print(f"❌ {filename}")
            for error in errors:
                print(f"   - {error}")

    print()

    if all_valid:
        print("🎉 All agents validated successfully!")
        sys.exit(0)
    else:
        print(f"⚠️  {len(agent_files) - valid_count} agents have validation errors")
        sys.exit(1)


if __name__ == "__main__":
    main()

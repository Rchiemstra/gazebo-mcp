#!/usr/bin/env python3
"""
Command Validation Script

Validates all command files are properly configured and in the correct location.
"""

import sys
from pathlib import Path
from typing import List, Tuple

def check_command_file(file_path: Path) -> Tuple[bool, List[str]]:
    """
    Validate a single command file.

    Returns:
        (is_valid, list_of_issues)
    """
    issues = []

    try:
        content = file_path.read_text()
    except Exception as e:
        return False, [f"Failed to read file: {e}"]

    # Check 1: File is not empty
    if not content.strip():
        issues.append("File is empty")

    # Check 2: Contains $ARGUMENTS variable (expected in most commands)
    if "$ARGUMENTS" not in content:
        issues.append("Warning: No $ARGUMENTS variable found (may not be needed for all commands)")

    # Check 3: Has reasonable length (at least 100 chars)
    if len(content) < 100:
        issues.append(f"File seems too short: {len(content)} chars (expected at least 100)")

    # Check 4: Contains instructions (basic check)
    if not any(keyword in content.lower() for keyword in ["you are", "your mission", "process", "step"]):
        issues.append("File may not contain proper command instructions")

    is_valid = len(issues) == 0
    return is_valid, issues


def main():
    """Main validation routine."""
    repo_root = Path(__file__).parent.parent

    # Check both locations
    claude_commands_dir = repo_root / ".claude" / "commands"
    original_commands_dir = repo_root / "commands"

    print("🔍 Validating Command Configuration...\n")

    # Check .claude/commands/ directory exists
    if not claude_commands_dir.exists():
        print(f"❌ CRITICAL: .claude/commands/ directory not found!")
        print(f"   Expected: {claude_commands_dir}")
        print(f"   Commands will not be discovered by Claude Code!")
        sys.exit(1)

    print(f"✅ .claude/commands/ directory exists: {claude_commands_dir}")

    # Get command files from .claude/commands/
    command_files = list(claude_commands_dir.glob("*.md"))

    if not command_files:
        print(f"❌ CRITICAL: No command files found in .claude/commands/")
        sys.exit(1)

    print(f"✅ Found {len(command_files)} command files\n")

    # List expected commands
    expected_commands = [
        "ask-specialist.md",
        "check-understanding.md",
        "continue-plan.md",
        "create-plan.md",
        "create-project-plan.md",
        "reflection.md",
        "start-learning.md",
        "update-plan.md"
    ]

    # Check for missing commands
    found_commands = [f.name for f in command_files]
    missing = set(expected_commands) - set(found_commands)
    extra = set(found_commands) - set(expected_commands)

    if missing:
        print(f"⚠️  Missing commands: {', '.join(missing)}\n")

    if extra:
        print(f"ℹ️  Additional commands: {', '.join(extra)}\n")

    # Validate each command file
    print("📋 Validating Command Files:\n")

    all_valid = True
    results = []

    for cmd_file in sorted(command_files):
        is_valid, issues = check_command_file(cmd_file)
        results.append((cmd_file.name, is_valid, issues))

        if not is_valid:
            all_valid = False

    # Print results
    valid_count = sum(1 for _, is_valid, _ in results if is_valid)

    for filename, is_valid, issues in results:
        command_name = filename.replace('.md', '')
        if is_valid:
            print(f"✅ /{command_name}")
        else:
            print(f"⚠️  /{command_name}")
            for issue in issues:
                print(f"   - {issue}")

    print(f"\n📊 Validation Results: {valid_count}/{len(command_files)} commands valid\n")

    # Check original commands/ directory
    if original_commands_dir.exists():
        original_files = list(original_commands_dir.glob("*.md"))
        print(f"ℹ️  Original commands/ directory also exists with {len(original_files)} files")
        print(f"   (kept for backward compatibility)\n")

    # Summary
    print("=" * 60)
    if all_valid:
        print("🎉 All commands are properly configured!")
        print("\nCommands are located in:")
        print(f"  - {claude_commands_dir} (Claude Code discovery)")
        print(f"  - {original_commands_dir} (backup/compatibility)")
        print("\nAll commands should be available via slash commands (/command-name)")
        sys.exit(0)
    else:
        print("⚠️  Some commands have validation warnings")
        print("   Review issues above and fix if needed")
        sys.exit(1)


if __name__ == "__main__":
    main()

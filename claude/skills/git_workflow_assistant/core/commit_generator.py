"""
Commit Message Generator

Generates conventional commit messages from repository changes.
"""

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any

from .change_analyzer import ChangeAnalyzer, ChangeType


@dataclass
class CommitMessage:
    """A generated commit message."""
    message: str
    type: str
    scope: Optional[str]
    description: str
    body: str
    footer: str
    is_breaking: bool


class CommitMessageGenerator:
    """Generates semantic commit messages."""

    def __init__(self, repo_path: str):
        """
        Initialize generator.

        Args:
            repo_path: Path to git repository
        """
        self.repo_path = Path(repo_path)
        self.analyzer = ChangeAnalyzer(str(repo_path))

    def generate(
        self,
        commit_type: Optional[str] = None,
        scope: Optional[str] = None,
        breaking: bool = False
    ) -> CommitMessage:
        """
        Generate commit message from changes.

        Args:
            commit_type: Optional commit type override
            scope: Optional commit scope
            breaking: Mark as breaking change

        Returns:
            Generated commit message
        """
        # Analyze changes
        analysis = self.analyzer.analyze()

        # Determine type
        if commit_type:
            msg_type = commit_type
        else:
            msg_type = analysis.change_type.value

        # Determine scope
        if not scope and analysis.affected_modules:
            scope = analysis.affected_modules[0]

        # Check for breaking changes
        is_breaking = breaking or len(analysis.breaking_changes) > 0

        # Generate description
        description = self._generate_description(analysis, msg_type)

        # Generate body
        body = self._generate_body(analysis)

        # Generate footer
        footer = self._generate_footer(analysis, is_breaking)

        # Assemble message
        message = self._assemble_message(
            msg_type, scope, description, body, footer, is_breaking
        )

        return CommitMessage(
            message=message,
            type=msg_type,
            scope=scope,
            description=description,
            body=body,
            footer=footer,
            is_breaking=is_breaking
        )

    def _generate_description(self, analysis, msg_type: str) -> str:
        """Generate short description."""
        stats = analysis.statistics
        files = analysis.staged_files

        # Try to extract description from file names
        if len(files) == 1:
            file_path = Path(files[0].path)
            file_name = file_path.stem

            # Remove underscores and convert to words
            words = file_name.replace('_', ' ').replace('-', ' ')

            if files[0].is_new:
                return f"add {words} module"
            elif files[0].is_deleted:
                return f"remove {words} module"
            else:
                return f"update {words}"

        # Multiple files - generate generic description
        if msg_type == 'feat':
            return f"add new functionality"
        elif msg_type == 'fix':
            return f"fix issues in {len(files)} files"
        elif msg_type == 'docs':
            return f"update documentation"
        elif msg_type == 'test':
            return f"add tests"
        elif msg_type == 'refactor':
            return f"refactor code structure"
        elif msg_type == 'style':
            return f"format code"
        elif msg_type == 'chore':
            return f"update dependencies"
        else:
            return f"update {len(files)} files"

    def _generate_body(self, analysis) -> str:
        """Generate detailed body."""
        lines = []

        # Add statistics
        stats = analysis.statistics
        if stats['files_changed'] > 0:
            lines.append(f"Changed {stats['files_changed']} file(s):")

            # List files
            for file in analysis.staged_files[:5]:  # Max 5 files
                status_symbol = {
                    'A': '+',
                    'M': '~',
                    'D': '-'
                }.get(file.status, '?')

                lines.append(f"  {status_symbol} {file.path}")

            if len(analysis.staged_files) > 5:
                remaining = len(analysis.staged_files) - 5
                lines.append(f"  ... and {remaining} more files")

        # Add change summary
        if stats['total_additions'] > 0 or stats['total_deletions'] > 0:
            lines.append("")
            lines.append(
                f"+{stats['total_additions']} -{stats['total_deletions']} lines"
            )

        return '\n'.join(lines)

    def _generate_footer(self, analysis, is_breaking: bool) -> str:
        """Generate footer with metadata."""
        lines = []

        # Add breaking change notice
        if is_breaking:
            lines.append("BREAKING CHANGE: API changes detected")

            if analysis.breaking_changes:
                for change in analysis.breaking_changes:
                    lines.append(f"  - {change}")

        # Add affected modules
        if analysis.affected_modules:
            modules_str = ', '.join(analysis.affected_modules[:3])
            lines.append(f"Affects: {modules_str}")

        return '\n'.join(lines)

    def _assemble_message(
        self,
        msg_type: str,
        scope: Optional[str],
        description: str,
        body: str,
        footer: str,
        is_breaking: bool
    ) -> str:
        """Assemble complete commit message."""
        # Build header
        if scope:
            header = f"{msg_type}({scope}): {description}"
        else:
            header = f"{msg_type}: {description}"

        # Add breaking change indicator
        if is_breaking:
            header = f"{msg_type}({scope})!: {description}" if scope else f"{msg_type}!: {description}"

        # Assemble parts
        parts = [header]

        if body:
            parts.append("")
            parts.append(body)

        if footer:
            parts.append("")
            parts.append(footer)

        return '\n'.join(parts)

    def validate_message(self, message: str) -> bool:
        """
        Validate commit message format.

        Args:
            message: Commit message to validate

        Returns:
            True if valid
        """
        lines = message.splitlines()
        if not lines:
            return False

        # Check header format
        header = lines[0]

        # Must have type
        if ':' not in header:
            return False

        type_part = header.split(':')[0]

        # Valid types
        valid_types = [
            'feat', 'fix', 'docs', 'style', 'refactor',
            'test', 'chore', 'perf', 'ci', 'build'
        ]

        # Extract type (handle scope and breaking change indicator)
        commit_type = type_part.split('(')[0].rstrip('!')

        if commit_type not in valid_types:
            return False

        return True


def generate_commit_message(
    repo_path: str = '.',
    commit_type: Optional[str] = None,
    scope: Optional[str] = None,
    breaking: bool = False
) -> Dict[str, Any]:
    """
    Generate conventional commit message from changes.

    Args:
        repo_path: Path to git repository
        commit_type: Optional type override ('feat', 'fix', etc.)
        scope: Optional commit scope
        breaking: Mark as breaking change

    Returns:
        Dictionary with commit message components

    Example:
        >>> commit = generate_commit_message(repo_path='.')
        >>> print(commit['message'])
        feat(auth): add user authentication

        Changed 3 file(s):
          + auth/login.py
          + auth/register.py
          ~ auth/__init__.py

        +150 -20 lines
    """
    generator = CommitMessageGenerator(repo_path)
    result = generator.generate(commit_type, scope, breaking)

    return {
        'message': result.message,
        'type': result.type,
        'scope': result.scope,
        'description': result.description,
        'body': result.body,
        'footer': result.footer,
        'is_breaking': result.is_breaking
    }

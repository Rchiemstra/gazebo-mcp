"""
Pull Request Generator

Generates pull request titles, descriptions, and metadata.
"""

import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict, Any

from .change_analyzer import ChangeAnalyzer


@dataclass
class PullRequest:
    """A generated pull request."""
    title: str
    description: str
    labels: List[str] = field(default_factory=list)
    reviewers: List[str] = field(default_factory=list)
    checklist: List[str] = field(default_factory=list)


class PRGenerator:
    """Generates pull request content."""

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
        source_branch: str,
        target_branch: str,
        template: Optional[str] = None
    ) -> PullRequest:
        """
        Generate pull request content.

        Args:
            source_branch: Source branch name
            target_branch: Target branch name
            template: Optional PR template path

        Returns:
            Generated pull request
        """
        # Get commits between branches
        commits = self._get_commits_between(source_branch, target_branch)

        # Analyze changes
        analysis = self.analyzer.analyze()

        # Generate title
        title = self._generate_title(source_branch, commits, analysis)

        # Generate description
        description = self._generate_description(commits, analysis, template)

        # Generate labels
        labels = self._generate_labels(analysis)

        # Generate checklist
        checklist = self._generate_checklist(analysis)

        return PullRequest(
            title=title,
            description=description,
            labels=labels,
            reviewers=[],
            checklist=checklist
        )

    def _get_commits_between(self, source: str, target: str) -> List[str]:
        """Get commits between two branches."""
        try:
            result = subprocess.run(
                ['git', 'log', f'{target}..{source}', '--oneline'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )

            commits = result.stdout.strip().splitlines()
            return commits

        except subprocess.CalledProcessError:
            return []

    def _generate_title(self, branch_name: str, commits: List[str], analysis) -> str:
        """Generate PR title."""
        # Try to extract from branch name
        parts = branch_name.split('/')

        if len(parts) >= 2:
            # Remove prefix (feature/, bugfix/, etc.)
            title_parts = parts[1:]

            # Convert to readable title
            title = ' '.join(title_parts).replace('-', ' ').replace('_', ' ')
            return title.capitalize()

        # Fallback to commit message
        if commits:
            # Use first commit message
            first_commit = commits[0]
            # Remove hash
            message = ' '.join(first_commit.split()[1:])
            return message.capitalize()

        # Fallback to generic title
        return f"Update from {branch_name}"

    def _generate_description(
        self,
        commits: List[str],
        analysis,
        template: Optional[str]
    ) -> str:
        """Generate PR description."""
        lines = []

        # Add template if provided
        if template:
            lines.append(template)
            lines.append("")

        # Add summary
        lines.append("## Summary")
        lines.append("")

        if analysis.change_type:
            lines.append(f"Type: `{analysis.change_type.value}`")

        stats = analysis.statistics
        lines.append(f"- {stats['files_changed']} files changed")
        lines.append(f"- +{stats['total_additions']} -{stats['total_deletions']} lines")

        if analysis.affected_modules:
            modules = ', '.join(analysis.affected_modules)
            lines.append(f"- Affected modules: {modules}")

        lines.append("")

        # Add commits
        if commits:
            lines.append("## Commits")
            lines.append("")
            for commit in commits[:10]:  # Max 10 commits
                lines.append(f"- {commit}")

            if len(commits) > 10:
                lines.append(f"- ... and {len(commits) - 10} more commits")

            lines.append("")

        # Add breaking changes warning
        if analysis.breaking_changes:
            lines.append("## ⚠️ Breaking Changes")
            lines.append("")
            for change in analysis.breaking_changes:
                lines.append(f"- {change}")
            lines.append("")

        # Add changed files
        if analysis.staged_files:
            lines.append("## Changed Files")
            lines.append("")
            for file in analysis.staged_files[:15]:  # Max 15 files
                status = {
                    'A': '✨ Added',
                    'M': '📝 Modified',
                    'D': '🗑️ Deleted'
                }.get(file.status, '❓ Changed')

                lines.append(f"- {status}: `{file.path}`")

            if len(analysis.staged_files) > 15:
                remaining = len(analysis.staged_files) - 15
                lines.append(f"- ... and {remaining} more files")

            lines.append("")

        return '\n'.join(lines)

    def _generate_labels(self, analysis) -> List[str]:
        """Generate suggested labels."""
        labels = []

        # Add type label
        labels.append(analysis.change_type.value)

        # Add impact label
        impact = analysis.impact_level.value
        if impact in ['high', 'critical']:
            labels.append(impact)

        # Add breaking change label
        if analysis.breaking_changes:
            labels.append('breaking-change')

        # Add module labels
        for module in analysis.affected_modules[:3]:  # Max 3 modules
            labels.append(f"module:{module}")

        return labels

    def _generate_checklist(self, analysis) -> List[str]:
        """Generate PR checklist."""
        checklist = [
            "[ ] Code follows project style guidelines",
            "[ ] Self-review completed",
            "[ ] Comments added for complex code",
            "[ ] Documentation updated",
            "[ ] No new warnings generated",
        ]

        # Add breaking change item if needed
        if analysis.breaking_changes:
            checklist.insert(0, "[ ] Breaking changes documented")

        # Add test item if source files changed
        has_source_changes = any(
            f.path.endswith(('.py', '.js', '.ts'))
            for f in analysis.staged_files
        )

        if has_source_changes:
            checklist.insert(0, "[ ] Tests added/updated")

        return checklist


def create_pull_request(
    repo_path: str = '.',
    source_branch: str = 'HEAD',
    target_branch: str = 'main',
    template: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate pull request content.

    Args:
        repo_path: Path to git repository
        source_branch: Source branch name
        target_branch: Target branch name
        template: Optional PR template text

    Returns:
        Dictionary with PR content

    Example:
        >>> pr = create_pull_request(
        ...     repo_path='.',
        ...     source_branch='feature/user-auth',
        ...     target_branch='main'
        ... )
        >>> print(pr['title'])
        User auth
        >>> print(pr['description'])
        ## Summary
        ...
    """
    generator = PRGenerator(repo_path)
    result = generator.generate(source_branch, target_branch, template)

    return {
        'title': result.title,
        'description': result.description,
        'labels': result.labels,
        'reviewers': result.reviewers,
        'checklist': result.checklist
    }

"""
Change Analyzer

Analyzes git repository changes and determines their type and impact.
"""

import subprocess
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Dict, Optional, Any


class ChangeType(Enum):
    """Type of code change."""
    FEATURE = "feat"
    FIX = "fix"
    DOCS = "docs"
    STYLE = "style"
    REFACTOR = "refactor"
    TEST = "test"
    CHORE = "chore"
    PERF = "perf"
    CI = "ci"
    BUILD = "build"


class ImpactLevel(Enum):
    """Impact level of changes."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class FileChange:
    """Information about a changed file."""
    path: str
    status: str  # 'A'dded, 'M'odified, 'D'eleted, 'R'enamed
    additions: int = 0
    deletions: int = 0
    is_new: bool = False
    is_deleted: bool = False


@dataclass
class ChangeAnalysis:
    """Analysis of repository changes."""
    staged_files: List[FileChange] = field(default_factory=list)
    unstaged_files: List[FileChange] = field(default_factory=list)
    change_type: ChangeType = ChangeType.CHORE
    breaking_changes: List[str] = field(default_factory=list)
    impact_level: ImpactLevel = ImpactLevel.LOW
    statistics: Dict[str, Any] = field(default_factory=dict)
    affected_modules: List[str] = field(default_factory=list)


class ChangeAnalyzer:
    """Analyzes git repository changes."""

    def __init__(self, repo_path: str):
        """
        Initialize analyzer.

        Args:
            repo_path: Path to git repository
        """
        self.repo_path = Path(repo_path)

    def analyze(self, include_unstaged: bool = False) -> ChangeAnalysis:
        """
        Analyze repository changes.

        Args:
            include_unstaged: Include unstaged changes

        Returns:
            Change analysis
        """
        analysis = ChangeAnalysis()

        # Get staged changes
        analysis.staged_files = self._get_staged_files()

        # Get unstaged changes if requested
        if include_unstaged:
            analysis.unstaged_files = self._get_unstaged_files()

        # Determine change type
        analysis.change_type = self._determine_change_type(
            analysis.staged_files + analysis.unstaged_files
        )

        # Calculate statistics
        analysis.statistics = self._calculate_statistics(
            analysis.staged_files + analysis.unstaged_files
        )

        # Determine impact level
        analysis.impact_level = self._determine_impact_level(
            analysis.staged_files + analysis.unstaged_files,
            analysis.statistics
        )

        # Identify breaking changes
        analysis.breaking_changes = self._identify_breaking_changes(
            analysis.staged_files + analysis.unstaged_files
        )

        # Identify affected modules
        analysis.affected_modules = self._identify_affected_modules(
            analysis.staged_files + analysis.unstaged_files
        )

        return analysis

    def _get_staged_files(self) -> List[FileChange]:
        """Get list of staged files."""
        try:
            # Get staged files
            result = subprocess.run(
                ['git', 'diff', '--cached', '--name-status'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )

            files = []
            for line in result.stdout.strip().splitlines():
                if not line:
                    continue

                parts = line.split('\t', 1)
                if len(parts) != 2:
                    continue

                status, path = parts

                file_change = FileChange(
                    path=path,
                    status=status,
                    is_new=status == 'A',
                    is_deleted=status == 'D'
                )

                # Get additions/deletions
                stats = self._get_file_stats(path, cached=True)
                file_change.additions = stats['additions']
                file_change.deletions = stats['deletions']

                files.append(file_change)

            return files

        except subprocess.CalledProcessError:
            return []

    def _get_unstaged_files(self) -> List[FileChange]:
        """Get list of unstaged files."""
        try:
            # Get unstaged files
            result = subprocess.run(
                ['git', 'diff', '--name-status'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )

            files = []
            for line in result.stdout.strip().splitlines():
                if not line:
                    continue

                parts = line.split('\t', 1)
                if len(parts) != 2:
                    continue

                status, path = parts

                file_change = FileChange(
                    path=path,
                    status=status,
                    is_new=False,
                    is_deleted=status == 'D'
                )

                # Get additions/deletions
                stats = self._get_file_stats(path, cached=False)
                file_change.additions = stats['additions']
                file_change.deletions = stats['deletions']

                files.append(file_change)

            return files

        except subprocess.CalledProcessError:
            return []

    def _get_file_stats(self, file_path: str, cached: bool = False) -> Dict[str, int]:
        """Get addition/deletion stats for a file."""
        try:
            cmd = ['git', 'diff', '--numstat']
            if cached:
                cmd.append('--cached')
            cmd.append(file_path)

            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )

            if not result.stdout.strip():
                return {'additions': 0, 'deletions': 0}

            parts = result.stdout.strip().split('\t')
            if len(parts) >= 2:
                additions = int(parts[0]) if parts[0].isdigit() else 0
                deletions = int(parts[1]) if parts[1].isdigit() else 0
                return {'additions': additions, 'deletions': deletions}

        except (subprocess.CalledProcessError, ValueError):
            pass

        return {'additions': 0, 'deletions': 0}

    def _determine_change_type(self, files: List[FileChange]) -> ChangeType:
        """Determine the type of change based on files."""
        if not files:
            return ChangeType.CHORE

        # Count files by type
        source_files = 0
        test_files = 0
        doc_files = 0
        config_files = 0
        new_files = 0

        for file in files:
            path_lower = file.path.lower()

            if file.is_new:
                new_files += 1

            if path_lower.endswith(('.py', '.js', '.ts', '.java', '.go', '.rs')):
                if 'test' in path_lower or path_lower.startswith('test_'):
                    test_files += 1
                else:
                    source_files += 1

            elif path_lower.endswith(('.md', '.rst', '.txt', '.doc')):
                doc_files += 1

            elif path_lower.endswith(('.json', '.yml', '.yaml', '.toml', '.ini', '.cfg')):
                config_files += 1

        # Determine type
        if test_files > source_files:
            return ChangeType.TEST

        if doc_files > 0 and source_files == 0:
            return ChangeType.DOCS

        if config_files > 0 and source_files == 0:
            if any('ci' in f.path.lower() or 'github' in f.path.lower() for f in files):
                return ChangeType.CI
            return ChangeType.BUILD

        if new_files > len(files) / 2:
            return ChangeType.FEATURE

        # Check file content for patterns
        if self._contains_bug_fix_patterns(files):
            return ChangeType.FIX

        if self._contains_refactor_patterns(files):
            return ChangeType.REFACTOR

        # Default to feature for source changes
        if source_files > 0:
            return ChangeType.FEATURE

        return ChangeType.CHORE

    def _contains_bug_fix_patterns(self, files: List[FileChange]) -> bool:
        """Check if changes contain bug fix patterns."""
        # Look for bug fix keywords in diffs
        try:
            result = subprocess.run(
                ['git', 'diff', '--cached'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )

            diff_content = result.stdout.lower()

            # Bug fix indicators
            bug_keywords = [
                'fix', 'bug', 'issue', 'error', 'problem',
                'correct', 'resolve', 'patch'
            ]

            return any(keyword in diff_content for keyword in bug_keywords)

        except subprocess.CalledProcessError:
            return False

    def _contains_refactor_patterns(self, files: List[FileChange]) -> bool:
        """Check if changes contain refactoring patterns."""
        # Large deletions with similar additions often indicate refactoring
        for file in files:
            if file.deletions > 10 and file.additions > 10:
                ratio = min(file.additions, file.deletions) / max(file.additions, file.deletions)
                if ratio > 0.7:  # Similar number of additions and deletions
                    return True

        return False

    def _calculate_statistics(self, files: List[FileChange]) -> Dict[str, Any]:
        """Calculate change statistics."""
        total_additions = sum(f.additions for f in files)
        total_deletions = sum(f.deletions for f in files)
        files_changed = len(files)
        new_files = sum(1 for f in files if f.is_new)
        deleted_files = sum(1 for f in files if f.is_deleted)
        modified_files = files_changed - new_files - deleted_files

        return {
            'total_additions': total_additions,
            'total_deletions': total_deletions,
            'files_changed': files_changed,
            'new_files': new_files,
            'modified_files': modified_files,
            'deleted_files': deleted_files,
            'net_change': total_additions - total_deletions
        }

    def _determine_impact_level(
        self,
        files: List[FileChange],
        stats: Dict[str, Any]
    ) -> ImpactLevel:
        """Determine the impact level of changes."""
        files_changed = stats['files_changed']
        total_changes = stats['total_additions'] + stats['total_deletions']

        # Critical: many files or very large changes
        if files_changed > 20 or total_changes > 1000:
            return ImpactLevel.CRITICAL

        # High: significant number of files or large changes
        if files_changed > 10 or total_changes > 500:
            return ImpactLevel.HIGH

        # Medium: moderate changes
        if files_changed > 3 or total_changes > 100:
            return ImpactLevel.MEDIUM

        # Low: small changes
        return ImpactLevel.LOW

    def _identify_breaking_changes(self, files: List[FileChange]) -> List[str]:
        """Identify potential breaking changes."""
        breaking = []

        # Check for deleted files
        for file in files:
            if file.is_deleted and file.path.endswith(('.py', '.js', '.ts')):
                breaking.append(f"Deleted file: {file.path}")

        # Check for API changes (simplified)
        try:
            result = subprocess.run(
                ['git', 'diff', '--cached'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )

            diff_content = result.stdout

            # Look for removed public functions/classes
            removed_lines = [
                line for line in diff_content.splitlines()
                if line.startswith('-') and not line.startswith('---')
            ]

            for line in removed_lines:
                # Public function/class removed
                if 'def ' in line and not line.strip().startswith('-    def _'):
                    breaking.append("Removed public function")
                elif 'class ' in line and not line.strip().startswith('-class _'):
                    breaking.append("Removed public class")

        except subprocess.CalledProcessError:
            pass

        return breaking

    def _identify_affected_modules(self, files: List[FileChange]) -> List[str]:
        """Identify affected modules/components."""
        modules = set()

        for file in files:
            path = Path(file.path)

            # Extract module name from path
            if len(path.parts) > 1:
                # Use first directory as module name
                module = path.parts[0]
                modules.add(module)

        return sorted(list(modules))


def analyze_changes(
    repo_path: str = '.',
    include_unstaged: bool = False
) -> Dict[str, Any]:
    """
    Analyze git repository changes.

    Args:
        repo_path: Path to git repository
        include_unstaged: Include unstaged changes in analysis

    Returns:
        Dictionary with change analysis

    Example:
        >>> analysis = analyze_changes(repo_path='.')
        >>> print(f"Change type: {analysis['change_type']}")
        >>> print(f"Impact: {analysis['impact_level']}")
        >>> print(f"Files changed: {analysis['statistics']['files_changed']}")
    """
    analyzer = ChangeAnalyzer(repo_path)
    result = analyzer.analyze(include_unstaged)

    return {
        'staged_files': [
            {
                'path': f.path,
                'status': f.status,
                'additions': f.additions,
                'deletions': f.deletions,
                'is_new': f.is_new,
                'is_deleted': f.is_deleted
            }
            for f in result.staged_files
        ],
        'unstaged_files': [
            {
                'path': f.path,
                'status': f.status,
                'additions': f.additions,
                'deletions': f.deletions
            }
            for f in result.unstaged_files
        ],
        'change_type': result.change_type.value,
        'breaking_changes': result.breaking_changes,
        'impact_level': result.impact_level.value,
        'statistics': result.statistics,
        'affected_modules': result.affected_modules
    }

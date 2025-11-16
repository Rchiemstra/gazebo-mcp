"""
Update Checker

Checks for available updates to dependencies.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

from .dependency_analyzer import DependencyAnalysis, Dependency, Ecosystem


class UpdateType(Enum):
    """Type of version update."""
    MAJOR = "major"  # 1.x.x -> 2.x.x
    MINOR = "minor"  # 1.1.x -> 1.2.x
    PATCH = "patch"  # 1.1.1 -> 1.1.2


@dataclass
class PackageUpdate:
    """Represents an available package update."""
    package_name: str
    current_version: str
    latest_version: str
    update_type: UpdateType
    ecosystem: Ecosystem
    breaking_changes: bool
    release_notes_url: Optional[str] = None
    published_date: Optional[str] = None


@dataclass
class UpdateCheckResult:
    """Results of update checking."""
    project_path: str
    outdated_count: int
    major_updates: int
    minor_updates: int
    patch_updates: int
    updates_available: List[PackageUpdate] = field(default_factory=list)
    up_to_date_count: int = 0
    errors: List[str] = field(default_factory=list)


class UpdateChecker:
    """Checks for available updates to dependencies."""

    def __init__(self):
        # Mock registry of latest versions
        # In production, this would query package registries:
        # - PyPI API for Python
        # - npm registry API for Node.js
        self.latest_versions = self._load_mock_latest_versions()

    def check_updates(
        self,
        analysis: DependencyAnalysis,
        include_major: bool = False,
        dev_dependencies: bool = True
    ) -> UpdateCheckResult:
        """
        Check for available updates.

        Args:
            analysis: DependencyAnalysis from analyzer
            include_major: Include major version updates
            dev_dependencies: Check dev dependencies

        Returns:
            UpdateCheckResult with available updates
        """
        updates = []
        errors = []
        up_to_date = 0

        for dep in analysis.dependencies:
            # Skip dev dependencies if requested
            if not dev_dependencies and dep.dependency_type.value == 'dev':
                continue

            try:
                update = self._check_package_update(dep)

                if update:
                    # Filter major updates if not included
                    if not include_major and update.update_type == UpdateType.MAJOR:
                        continue

                    updates.append(update)
                else:
                    up_to_date += 1

            except Exception as e:
                errors.append(f"Error checking {dep.name}: {e}")

        # Count by update type
        major_count = sum(1 for u in updates if u.update_type == UpdateType.MAJOR)
        minor_count = sum(1 for u in updates if u.update_type == UpdateType.MINOR)
        patch_count = sum(1 for u in updates if u.update_type == UpdateType.PATCH)

        return UpdateCheckResult(
            project_path=analysis.project_path,
            outdated_count=len(updates),
            major_updates=major_count,
            minor_updates=minor_count,
            patch_updates=patch_count,
            updates_available=updates,
            up_to_date_count=up_to_date,
            errors=errors
        )

    def _check_package_update(self, dep: Dependency) -> Optional[PackageUpdate]:
        """Check if a package has an available update."""
        ecosystem_key = dep.ecosystem.value

        if ecosystem_key not in self.latest_versions:
            return None

        if dep.name not in self.latest_versions[ecosystem_key]:
            return None

        latest_info = self.latest_versions[ecosystem_key][dep.name]
        latest_version = latest_info['version']
        current_version = self._normalize_version(dep.version)

        # Skip if version is "any" or cannot be parsed
        if current_version == 'any' or current_version == 'unknown':
            return None

        # Compare versions
        comparison = self._compare_versions(current_version, latest_version)

        if comparison < 0:  # Current < Latest
            update_type = self._determine_update_type(current_version, latest_version)
            breaking = update_type == UpdateType.MAJOR

            return PackageUpdate(
                package_name=dep.name,
                current_version=current_version,
                latest_version=latest_version,
                update_type=update_type,
                ecosystem=dep.ecosystem,
                breaking_changes=breaking,
                release_notes_url=latest_info.get('release_notes'),
                published_date=latest_info.get('published_date')
            )

        return None  # Already up to date

    def _normalize_version(self, version: str) -> str:
        """Normalize version string."""
        # Remove semver prefixes
        version = version.lstrip('^~>=<!')
        # Remove 'v' prefix
        version = version.lstrip('v')
        # Take first part if multiple constraints
        version = version.split(',')[0].split(';')[0].strip()
        return version

    def _compare_versions(self, v1: str, v2: str) -> int:
        """
        Compare two versions.
        Returns: -1 if v1 < v2, 0 if equal, 1 if v1 > v2
        """
        try:
            parts1 = [int(p) for p in v1.split('.') if p.isdigit()]
            parts2 = [int(p) for p in v2.split('.') if p.isdigit()]

            # Pad shorter version with zeros
            max_len = max(len(parts1), len(parts2))
            parts1 += [0] * (max_len - len(parts1))
            parts2 += [0] * (max_len - len(parts2))

            for p1, p2 in zip(parts1, parts2):
                if p1 < p2:
                    return -1
                elif p1 > p2:
                    return 1

            return 0
        except:
            return 0  # Can't compare

    def _determine_update_type(self, current: str, latest: str) -> UpdateType:
        """Determine if update is major, minor, or patch."""
        try:
            current_parts = [int(p) for p in current.split('.') if p.isdigit()]
            latest_parts = [int(p) for p in latest.split('.') if p.isdigit()]

            # Ensure at least 3 parts (major.minor.patch)
            while len(current_parts) < 3:
                current_parts.append(0)
            while len(latest_parts) < 3:
                latest_parts.append(0)

            # Major version change
            if latest_parts[0] > current_parts[0]:
                return UpdateType.MAJOR

            # Minor version change
            if latest_parts[1] > current_parts[1]:
                return UpdateType.MINOR

            # Patch version change
            return UpdateType.PATCH

        except:
            return UpdateType.MINOR  # Default to minor

    def _load_mock_latest_versions(self) -> Dict:
        """
        Load mock registry of latest versions.

        In production, this would query:
        - PyPI API: https://pypi.org/pypi/{package}/json
        - npm registry: https://registry.npmjs.org/{package}
        """
        return {
            'python': {
                'django': {
                    'version': '4.2.7',
                    'published_date': '2023-11-01',
                    'release_notes': 'https://docs.djangoproject.com/en/4.2/releases/4.2.7/'
                },
                'flask': {
                    'version': '3.0.0',
                    'published_date': '2023-09-30',
                    'release_notes': 'https://flask.palletsprojects.com/en/3.0.x/changes/'
                },
                'requests': {
                    'version': '2.31.0',
                    'published_date': '2023-05-22',
                    'release_notes': 'https://github.com/psf/requests/releases/tag/v2.31.0'
                },
                'pytest': {
                    'version': '7.4.3',
                    'published_date': '2023-10-25',
                    'release_notes': 'https://docs.pytest.org/en/stable/changelog.html'
                },
                'numpy': {
                    'version': '1.26.2',
                    'published_date': '2023-11-12',
                    'release_notes': 'https://github.com/numpy/numpy/releases/tag/v1.26.2'
                },
                'pandas': {
                    'version': '2.1.3',
                    'published_date': '2023-11-10',
                    'release_notes': 'https://pandas.pydata.org/docs/whatsnew/v2.1.3.html'
                },
                'pillow': {
                    'version': '10.1.0',
                    'published_date': '2023-10-15',
                    'release_notes': 'https://pillow.readthedocs.io/en/stable/releasenotes/10.1.0.html'
                },
                'sqlalchemy': {
                    'version': '2.0.23',
                    'published_date': '2023-11-10',
                    'release_notes': 'https://docs.sqlalchemy.org/en/20/changelog/changelog_20.html'
                }
            },
            'npm': {
                'express': {
                    'version': '4.18.2',
                    'published_date': '2022-10-29',
                    'release_notes': 'https://github.com/expressjs/express/releases/tag/4.18.2'
                },
                'react': {
                    'version': '18.2.0',
                    'published_date': '2022-06-14',
                    'release_notes': 'https://github.com/facebook/react/releases/tag/v18.2.0'
                },
                'lodash': {
                    'version': '4.17.21',
                    'published_date': '2021-02-20',
                    'release_notes': 'https://github.com/lodash/lodash/releases/tag/4.17.21'
                },
                'axios': {
                    'version': '1.6.2',
                    'published_date': '2023-11-14',
                    'release_notes': 'https://github.com/axios/axios/releases/tag/v1.6.2'
                },
                'webpack': {
                    'version': '5.89.0',
                    'published_date': '2023-10-31',
                    'release_notes': 'https://github.com/webpack/webpack/releases/tag/v5.89.0'
                },
                'typescript': {
                    'version': '5.3.2',
                    'published_date': '2023-11-15',
                    'release_notes': 'https://devblogs.microsoft.com/typescript/announcing-typescript-5-3/'
                },
                'eslint': {
                    'version': '8.54.0',
                    'published_date': '2023-11-03',
                    'release_notes': 'https://github.com/eslint/eslint/releases/tag/v8.54.0'
                },
                'jest': {
                    'version': '29.7.0',
                    'published_date': '2023-09-15',
                    'release_notes': 'https://github.com/jestjs/jest/releases/tag/v29.7.0'
                }
            }
        }


def check_updates(
    project_path: str,
    ecosystem: Optional[str] = None,
    include_major: bool = False
) -> Dict:
    """
    Convenience function to check for updates.

    Args:
        project_path: Path to project directory
        ecosystem: Specific ecosystem to check
        include_major: Include major version updates

    Returns:
        Dictionary with update check results
    """
    from .dependency_analyzer import DependencyAnalyzer

    # First analyze dependencies
    analyzer = DependencyAnalyzer()
    analysis = analyzer.analyze_project(project_path, ecosystem)

    # Then check for updates
    checker = UpdateChecker()
    result = checker.check_updates(analysis, include_major)

    return {
        'project_path': result.project_path,
        'outdated_count': result.outdated_count,
        'major_updates': result.major_updates,
        'minor_updates': result.minor_updates,
        'patch_updates': result.patch_updates,
        'up_to_date_count': result.up_to_date_count,
        'updates_available': [
            {
                'package_name': upd.package_name,
                'current_version': upd.current_version,
                'latest_version': upd.latest_version,
                'update_type': upd.update_type.value,
                'breaking_changes': upd.breaking_changes,
                'release_notes_url': upd.release_notes_url,
                'published_date': upd.published_date
            }
            for upd in result.updates_available
        ],
        'errors': result.errors
    }

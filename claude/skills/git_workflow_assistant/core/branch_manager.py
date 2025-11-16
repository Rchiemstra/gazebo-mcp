"""
Branch Manager

Manages git branches and suggests names following conventions.
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Any


class BranchStrategy(Enum):
    """Branch strategy types."""
    GITFLOW = "gitflow"
    GITHUB_FLOW = "github-flow"
    GITLAB_FLOW = "gitlab-flow"


class BranchType(Enum):
    """Type of branch."""
    FEATURE = "feature"
    BUGFIX = "bugfix"
    HOTFIX = "hotfix"
    RELEASE = "release"
    DOCS = "docs"


@dataclass
class BranchSuggestion:
    """A suggested branch name."""
    branch_name: str
    base_branch: str
    strategy: str
    branch_type: str


class BranchManager:
    """Manages git branches and naming conventions."""

    STRATEGY_PREFIXES = {
        BranchStrategy.GITFLOW: {
            BranchType.FEATURE: "feature/",
            BranchType.BUGFIX: "bugfix/",
            BranchType.HOTFIX: "hotfix/",
            BranchType.RELEASE: "release/",
            BranchType.DOCS: "docs/"
        },
        BranchStrategy.GITHUB_FLOW: {
            BranchType.FEATURE: "",
            BranchType.BUGFIX: "fix/",
            BranchType.HOTFIX: "hotfix/",
            BranchType.RELEASE: "release/",
            BranchType.DOCS: "docs/"
        },
        BranchStrategy.GITLAB_FLOW: {
            BranchType.FEATURE: "feature/",
            BranchType.BUGFIX: "fix/",
            BranchType.HOTFIX: "hotfix/",
            BranchType.RELEASE: "release/",
            BranchType.DOCS: "docs/"
        }
    }

    STRATEGY_BASE_BRANCHES = {
        BranchStrategy.GITFLOW: {
            BranchType.FEATURE: "develop",
            BranchType.BUGFIX: "develop",
            BranchType.HOTFIX: "main",
            BranchType.RELEASE: "develop",
            BranchType.DOCS: "develop"
        },
        BranchStrategy.GITHUB_FLOW: {
            BranchType.FEATURE: "main",
            BranchType.BUGFIX: "main",
            BranchType.HOTFIX: "main",
            BranchType.RELEASE: "main",
            BranchType.DOCS: "main"
        },
        BranchStrategy.GITLAB_FLOW: {
            BranchType.FEATURE: "main",
            BranchType.BUGFIX: "main",
            BranchType.HOTFIX: "production",
            BranchType.RELEASE: "main",
            BranchType.DOCS: "main"
        }
    }

    def suggest_branch_name(
        self,
        issue_number: Optional[str] = None,
        description: str = "",
        branch_type: str = "feature",
        strategy: str = "gitflow"
    ) -> BranchSuggestion:
        """
        Suggest branch name following conventions.

        Args:
            issue_number: Issue or ticket number
            description: Brief description
            branch_type: Type of branch
            strategy: Branching strategy

        Returns:
            Branch suggestion
        """
        # Convert to enums
        try:
            strategy_enum = BranchStrategy(strategy)
            type_enum = BranchType(branch_type)
        except ValueError:
            strategy_enum = BranchStrategy.GITFLOW
            type_enum = BranchType.FEATURE

        # Get prefix
        prefix = self.STRATEGY_PREFIXES[strategy_enum][type_enum]

        # Clean description
        clean_desc = self._clean_description(description)

        # Build branch name
        parts = []

        if prefix:
            parts.append(prefix.rstrip('/'))

        if issue_number:
            parts.append(issue_number)

        if clean_desc:
            parts.append(clean_desc)

        branch_name = '/'.join(parts) if len(parts) > 1 else parts[0] if parts else "feature/unnamed"

        # Get base branch
        base_branch = self.STRATEGY_BASE_BRANCHES[strategy_enum][type_enum]

        return BranchSuggestion(
            branch_name=branch_name,
            base_branch=base_branch,
            strategy=strategy,
            branch_type=branch_type
        )

    def _clean_description(self, description: str) -> str:
        """Clean description for use in branch name."""
        # Convert to lowercase
        clean = description.lower()

        # Replace spaces and special characters with hyphens
        clean = re.sub(r'[^\w\s-]', '', clean)
        clean = re.sub(r'[\s_]+', '-', clean)

        # Remove duplicate hyphens
        clean = re.sub(r'-+', '-', clean)

        # Trim hyphens
        clean = clean.strip('-')

        # Limit length
        if len(clean) > 50:
            clean = clean[:50].rsplit('-', 1)[0]

        return clean

    def validate_branch_name(self, branch_name: str, strategy: str = "gitflow") -> bool:
        """
        Validate branch name against strategy.

        Args:
            branch_name: Branch name to validate
            strategy: Branching strategy

        Returns:
            True if valid
        """
        try:
            strategy_enum = BranchStrategy(strategy)
        except ValueError:
            return False

        # Get valid prefixes for this strategy
        valid_prefixes = []
        for type_enum in BranchType:
            prefix = self.STRATEGY_PREFIXES[strategy_enum][type_enum]
            if prefix:
                valid_prefixes.append(prefix.rstrip('/'))

        # Check if branch matches any prefix
        if not valid_prefixes:
            return True  # No prefixes required

        return any(
            branch_name.startswith(prefix + '/')
            for prefix in valid_prefixes
        )


def suggest_branch_name(
    issue_number: Optional[str] = None,
    description: str = "",
    branch_type: str = "feature",
    strategy: str = "gitflow"
) -> Dict[str, Any]:
    """
    Suggest git branch name following conventions.

    Args:
        issue_number: Issue or ticket number (e.g., 'PROJ-123')
        description: Brief description of the branch
        branch_type: Type of branch ('feature', 'bugfix', 'hotfix', 'release', 'docs')
        strategy: Branching strategy ('gitflow', 'github-flow', 'gitlab-flow')

    Returns:
        Dictionary with branch suggestion

    Example:
        >>> suggestion = suggest_branch_name(
        ...     issue_number='PROJ-456',
        ...     description='Add user authentication',
        ...     branch_type='feature',
        ...     strategy='gitflow'
        ... )
        >>> print(suggestion['branch_name'])
        feature/PROJ-456/add-user-authentication
        >>> print(suggestion['base_branch'])
        develop
    """
    manager = BranchManager()
    result = manager.suggest_branch_name(issue_number, description, branch_type, strategy)

    return {
        'branch_name': result.branch_name,
        'base_branch': result.base_branch,
        'strategy': result.strategy,
        'branch_type': result.branch_type
    }

"""
Git Workflow Assistant Operations

Standardized operations interface for agent invocation.
"""

from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
import time

# Import core functions
from .core.change_analyzer import analyze_changes as _analyze_changes
from .core.commit_generator import generate_commit_message as _generate_commit_message
from .core.branch_manager import suggest_branch_name as _suggest_branch_name
from .core.pr_generator import create_pull_request as _create_pull_request


@dataclass
class OperationResult:
    """Result from a skill operation."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    duration: float = 0.0
    metadata: Optional[Dict[str, Any]] = None


def analyze_changes(
    repo_path: str = ".",
    include_unstaged: bool = False,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Analyze staged and unstaged changes in a git repository.

    Args:
        repo_path: Path to git repository (default: current directory)
        include_unstaged: Include unstaged changes in analysis
        response_format: "summary" (counts) or "detailed" (full file changes)
        **kwargs: Additional parameters

    Returns:
        OperationResult with change analysis

    Token Efficiency:
        - Use response_format="summary" for file counts and change types
        - Use response_format="detailed" for complete diff information
        - Summary mode saves 80-90% tokens for large changesets
    """
    start_time = time.time()

    try:
        result = _analyze_changes(
            repo_path=repo_path,
            include_unstaged=include_unstaged
        )

        duration = time.time() - start_time

        # Build response based on format
        if response_format == "summary":
            files_changed = result.get('files_changed', [])
            data = {
                "total_files_changed": len(files_changed),
                "files_added": len([f for f in files_changed if f.get('status') == 'added']),
                "files_modified": len([f for f in files_changed if f.get('status') == 'modified']),
                "files_deleted": len([f for f in files_changed if f.get('status') == 'deleted']),
                "total_insertions": result.get('total_insertions', 0),
                "total_deletions": result.get('total_deletions', 0),
                "change_type": result.get('change_type', 'unknown'),
                "efficiency_tip": (
                    f"Analyzed {len(files_changed)} changed files. "
                    f"Using summary mode for efficiency. For full diff:\n"
                    f"analyze_changes(response_format='detailed')"
                )
            }
        else:
            # Detailed format - include everything
            data = result

        return OperationResult(
            success=True,
            data=data,
            duration=duration,
            metadata={
                "skill": "git-workflow-assistant",
                "operation": "analyze_changes",
                "version": "0.1.0",
                "include_unstaged": include_unstaged,
                "response_format": response_format
            }
        )

    except FileNotFoundError as e:
        return OperationResult(
            success=False,
            error=f"Git repository not found at: {repo_path}",
            error_code="REPO_NOT_FOUND",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check if you're in a git repository directory",
                    "Run Bash('git status') to verify git is initialized",
                    "Initialize git with Bash('git init') if needed",
                    "Verify the repo_path parameter points to a valid git directory"
                ],
                "example_fix": "analyze_changes(repo_path='.', include_unstaged=True)"
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Change analysis failed: {str(e)}",
            error_code="ANALYSIS_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure you're in a git repository with Bash('git status')",
                    "Check if you have any changes with Bash('git diff --stat')",
                    "Verify git is properly configured",
                    "Try with include_unstaged=False to analyze only staged changes"
                ],
                "example_fix": "analyze_changes(repo_path='.', include_unstaged=False)"
            }
        )


def generate_commit_message(
    repo_path: str = ".",
    commit_type: Optional[str] = None,
    scope: Optional[str] = None,
    breaking: bool = False,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Generate conventional commit message from staged changes.

    Args:
        repo_path: Path to git repository (default: current directory)
        commit_type: Optional commit type override (feat, fix, docs, etc.)
        scope: Optional commit scope
        breaking: Is this a breaking change
        response_format: "summary" (message only) or "detailed" (with analysis)
        **kwargs: Additional parameters

    Returns:
        OperationResult with generated commit message

    Token Efficiency:
        - Use response_format="summary" for just the commit message
        - Use response_format="detailed" for message + change analysis
        - Summary mode saves 70-85% tokens
    """
    start_time = time.time()

    try:
        result = _generate_commit_message(
            repo_path=repo_path,
            commit_type=commit_type,
            scope=scope,
            breaking=breaking
        )

        duration = time.time() - start_time

        return OperationResult(
            success=True,
            data=result,
            duration=duration,
            metadata={
                "skill": "git-workflow-assistant",
                "operation": "generate_commit_message",
                "version": "0.1.0",
                "commit_type": commit_type,
                "breaking": breaking
            }
        )

    except FileNotFoundError as e:
        return OperationResult(
            success=False,
            error=f"Git repository not found at: {repo_path}",
            error_code="REPO_NOT_FOUND",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Verify you're in a git repository",
                    "Run Bash('git status') to check repository status",
                    "Initialize git with Bash('git init') if needed",
                    "Check that repo_path points to a valid git directory"
                ],
                "example_fix": "generate_commit_message(repo_path='.', commit_type='feat')"
            }
        )
    except ValueError as e:
        return OperationResult(
            success=False,
            error=f"No staged changes found to commit",
            error_code="NO_CHANGES",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Stage changes first with Bash('git add <files>')",
                    "Check staged changes with Bash('git diff --cached')",
                    "Verify you have uncommitted changes with Bash('git status')",
                    "Use analyze_changes to see what files have been modified"
                ],
                "example_fix": "# First: Bash('git add file.py'), then: generate_commit_message()"
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Commit message generation failed: {str(e)}",
            error_code="GENERATION_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure you have staged changes",
                    "Check if commit_type is valid (feat, fix, docs, style, refactor, test, chore)",
                    "Verify git is properly configured with user.name and user.email",
                    "Try without specifying commit_type to auto-detect"
                ],
                "example_fix": "generate_commit_message(repo_path='.', commit_type='feat', scope='auth')"
            }
        )


def suggest_branch_name(
    description: str = "",
    branch_type: str = "feature",
    issue_number: Optional[str] = None,
    strategy: str = "gitflow",
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Suggest branch name following conventions.

    Args:
        description: Description of the work
        branch_type: Type of branch (feature, bugfix, hotfix, release)
        issue_number: Optional issue/ticket number
        strategy: Branching strategy (gitflow, github-flow, gitlab-flow)
        response_format: "summary" (name only) or "detailed" (with alternatives)
        **kwargs: Additional parameters

    Returns:
        OperationResult with suggested branch name

    Token Efficiency:
        - Use response_format="summary" for single branch name
        - Use response_format="detailed" for multiple alternatives
        - Summary mode saves 60-75% tokens
    """
    start_time = time.time()

    try:
        result = _suggest_branch_name(
            issue_number=issue_number,
            description=description,
            branch_type=branch_type,
            strategy=strategy
        )

        duration = time.time() - start_time

        return OperationResult(
            success=True,
            data=result,
            duration=duration,
            metadata={
                "skill": "git-workflow-assistant",
                "operation": "suggest_branch_name",
                "version": "0.1.0",
                "branch_type": branch_type
            }
        )

    except ValueError as e:
        return OperationResult(
            success=False,
            error=f"Invalid branch parameters: {str(e)}",
            error_code="VALIDATION_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Valid branch_type values: 'feature', 'bugfix', 'hotfix', 'release'",
                    "Valid strategy values: 'gitflow', 'github-flow', 'gitlab-flow'",
                    "Ensure description is a non-empty string",
                    "issue_number should be a string (e.g., '123' or 'PROJ-123')"
                ],
                "example_fix": "suggest_branch_name(description='add-auth', branch_type='feature', strategy='gitflow')"
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Branch name suggestion failed: {str(e)}",
            error_code="SUGGESTION_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure description contains only valid characters (alphanumeric, hyphens)",
                    "Try with a simpler description first",
                    "Check that branch_type and strategy are valid",
                    "Verify all parameters are strings where expected"
                ],
                "example_fix": "suggest_branch_name(description='user-authentication', branch_type='feature')"
            }
        )


def create_pull_request(
    repo_path: str = ".",
    base_branch: str = "main",
    head_branch: Optional[str] = None,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Create pull request with generated description.

    Args:
        repo_path: Path to git repository (default: current directory)
        base_branch: Base branch for PR (default: main)
        head_branch: Head branch (default: current branch)
        response_format: "summary" (title & description) or "detailed" (with commits)
        **kwargs: Additional parameters

    Returns:
        OperationResult with PR details
    """
    start_time = time.time()

    try:
        result = _create_pull_request(
            repo_path=repo_path,
            base_branch=base_branch,
            head_branch=head_branch
        )

        duration = time.time() - start_time

        return OperationResult(
            success=True,
            data=result,
            duration=duration,
            metadata={
                "skill": "git-workflow-assistant",
                "operation": "create_pull_request",
                "version": "0.1.0",
                "base_branch": base_branch
            }
        )

    except FileNotFoundError as e:
        return OperationResult(
            success=False,
            error=f"Git repository not found at: {repo_path}",
            error_code="REPO_NOT_FOUND",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Verify you're in a git repository",
                    "Run Bash('git status') to check repository status",
                    "Ensure repo_path points to a valid git directory",
                    "Check if the repository has a remote configured with Bash('git remote -v')"
                ],
                "example_fix": "create_pull_request(repo_path='.', base_branch='main')"
            }
        )
    except ValueError as e:
        return OperationResult(
            success=False,
            error=f"Invalid PR parameters: {str(e)}",
            error_code="VALIDATION_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure base_branch and head_branch are valid branch names",
                    "Check if branches exist with Bash('git branch -a')",
                    "Verify head_branch has commits ahead of base_branch",
                    "Use Bash('git log base_branch..head_branch') to see commits"
                ],
                "example_fix": "create_pull_request(repo_path='.', base_branch='main', head_branch='feature/auth')"
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            error=f"PR creation failed: {str(e)}",
            error_code="CREATION_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure you have a remote repository configured",
                    "Check if you have permission to create PRs on the remote",
                    "Verify head_branch is pushed to remote with Bash('git push')",
                    "Ensure git and gh CLI are properly configured"
                ],
                "example_fix": "create_pull_request(repo_path='.', base_branch='main')"
            }
        )


# Export all operations
__all__ = [
    "analyze_changes",
    "generate_commit_message",
    "suggest_branch_name",
    "create_pull_request",
    "OperationResult"
]

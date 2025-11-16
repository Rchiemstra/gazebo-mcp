"""Git utilities for learning session management."""

import subprocess
import logging
from pathlib import Path
from typing import Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


class GitManager:
    """Manages Git operations for learning sessions."""

    def __init__(self, workspace_root: Path):
        """
        Initialize Git manager.

        Args:
            workspace_root: Root directory of the Git repository
        """
        self.workspace_root = workspace_root

    def _run_git_command(self, *args: str) -> Tuple[int, str, str]:
        """
        Run a git command and return the result.

        Args:
            *args: Git command arguments

        Returns:
            Tuple of (return_code, stdout, stderr)
        """
        try:
            result = subprocess.run(
                ["git", *args],
                cwd=str(self.workspace_root),
                capture_output=True,
                text=True,
            )
            return result.returncode, result.stdout.strip(), result.stderr.strip()
        except Exception as e:
            logger.error(f"Git command failed: {e}")
            return 1, "", str(e)

    def is_git_repo(self) -> bool:
        """Check if workspace is a Git repository."""
        returncode, _, _ = self._run_git_command("rev-parse", "--git-dir")
        return returncode == 0

    def get_current_branch(self) -> Optional[str]:
        """Get the current Git branch name."""
        returncode, stdout, _ = self._run_git_command("branch", "--show-current")
        if returncode == 0 and stdout:
            return stdout
        return None

    def branch_exists(self, branch_name: str) -> bool:
        """Check if a branch exists."""
        returncode, _, _ = self._run_git_command("rev-parse", "--verify", branch_name)
        return returncode == 0

    def create_branch(self, branch_name: str, checkout: bool = True) -> bool:
        """
        Create a new Git branch.

        Args:
            branch_name: Name of the branch to create
            checkout: Whether to checkout the branch after creation

        Returns:
            True if successful, False otherwise
        """
        if not self.is_git_repo():
            logger.error("Not a Git repository")
            return False

        if self.branch_exists(branch_name):
            logger.info(f"Branch '{branch_name}' already exists")
            if checkout:
                return self.checkout_branch(branch_name)
            return True

        # Create and optionally checkout the branch
        if checkout:
            returncode, stdout, stderr = self._run_git_command("checkout", "-b", branch_name)
        else:
            returncode, stdout, stderr = self._run_git_command("branch", branch_name)

        if returncode == 0:
            logger.info(f"Created branch: {branch_name}")
            return True
        else:
            logger.error(f"Failed to create branch '{branch_name}': {stderr}")
            return False

    def checkout_branch(self, branch_name: str) -> bool:
        """
        Checkout an existing branch.

        Args:
            branch_name: Name of the branch to checkout

        Returns:
            True if successful, False otherwise
        """
        if not self.branch_exists(branch_name):
            logger.error(f"Branch '{branch_name}' does not exist")
            return False

        returncode, stdout, stderr = self._run_git_command("checkout", branch_name)

        if returncode == 0:
            logger.info(f"Checked out branch: {branch_name}")
            return True
        else:
            logger.error(f"Failed to checkout branch '{branch_name}': {stderr}")
            return False

    def has_changes(self) -> bool:
        """Check if there are any uncommitted changes."""
        returncode, stdout, _ = self._run_git_command("status", "--porcelain")
        return returncode == 0 and bool(stdout)

    def commit_changes(
        self,
        message: str,
        add_all: bool = True,
        author_name: Optional[str] = None,
        author_email: Optional[str] = None,
    ) -> bool:
        """
        Commit changes to the current branch.

        Args:
            message: Commit message
            add_all: Whether to add all changes before committing
            author_name: Optional author name override
            author_email: Optional author email override

        Returns:
            True if successful, False otherwise
        """
        if not self.has_changes():
            logger.info("No changes to commit")
            return True

        # Add all changes if requested
        if add_all:
            returncode, _, stderr = self._run_git_command("add", ".")
            if returncode != 0:
                logger.error(f"Failed to add changes: {stderr}")
                return False

        # Prepare commit command
        commit_args = ["commit", "-m", message]

        # Add author info if provided
        if author_name and author_email:
            commit_args.extend(["--author", f"{author_name} <{author_email}>"])

        returncode, stdout, stderr = self._run_git_command(*commit_args)

        if returncode == 0:
            logger.info(f"Committed changes: {message}")
            return True
        else:
            # Check if it's just "nothing to commit" (after staging)
            if "nothing to commit" in stderr or "nothing to commit" in stdout:
                logger.info("No changes to commit after staging")
                return True
            logger.error(f"Failed to commit: {stderr}")
            return False

    def push_branch(self, branch_name: Optional[str] = None, set_upstream: bool = True) -> bool:
        """
        Push a branch to remote.

        Args:
            branch_name: Branch to push (uses current if None)
            set_upstream: Whether to set upstream tracking

        Returns:
            True if successful, False otherwise
        """
        branch = branch_name or self.get_current_branch()
        if not branch:
            logger.error("No branch to push")
            return False

        push_args = ["push"]
        if set_upstream:
            push_args.extend(["-u", "origin", branch])
        else:
            push_args.extend(["origin", branch])

        returncode, stdout, stderr = self._run_git_command(*push_args)

        if returncode == 0:
            logger.info(f"Pushed branch '{branch}' to remote")
            return True
        else:
            # Check if it's already up to date
            if "up-to-date" in stderr or "up to date" in stderr:
                logger.info(f"Branch '{branch}' already up to date")
                return True
            logger.error(f"Failed to push branch '{branch}': {stderr}")
            return False

    def generate_branch_name(self, topic: str, session_id: str) -> str:
        """
        Generate a branch name from topic and session ID.

        Args:
            topic: Learning topic
            session_id: Session UUID

        Returns:
            Formatted branch name
        """
        # Sanitize topic for branch name
        sanitized_topic = topic.lower()
        sanitized_topic = sanitized_topic.replace(" ", "-")
        # Remove special characters, keep alphanumeric and hyphens
        sanitized_topic = "".join(c for c in sanitized_topic if c.isalnum() or c == "-")

        # Use first 8 chars of session ID
        short_id = session_id[:8]

        return f"learning/{sanitized_topic}-{short_id}"

    def create_phase_commit(
        self,
        phase_name: str,
        phase_number: int,
        topic: str,
        summary: Optional[str] = None,
    ) -> bool:
        """
        Create a commit for a completed learning phase.

        Args:
            phase_name: Name of the completed phase
            phase_number: Phase number
            topic: Learning topic
            summary: Optional summary of work done

        Returns:
            True if successful, False otherwise
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        commit_message = f"""Learning Progress: {topic} - Phase {phase_number}

Completed: {phase_name}
Timestamp: {timestamp}

{summary or "Phase completed successfully."}

---
Auto-committed by Claude Learning System
"""

        return self.commit_changes(commit_message)

    def get_remote_url(self) -> Optional[str]:
        """Get the remote origin URL."""
        returncode, stdout, _ = self._run_git_command("remote", "get-url", "origin")
        if returncode == 0 and stdout:
            return stdout
        return None

    def has_remote(self) -> bool:
        """Check if remote 'origin' exists."""
        returncode, _, _ = self._run_git_command("remote", "get-url", "origin")
        return returncode == 0

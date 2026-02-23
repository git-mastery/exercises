import re
from typing import Optional

from exercise_utils import git, github_cli


class RoleMarker:
    """Wrapper for git and GitHub operations with automatic role marker formatting.

    Usage:
        bob = RoleMarker("teammate-bob")
        bob.commit("Add feature", verbose=True)
        # Creates: "[ROLE:teammate-bob] Add feature"
    """

    PATTERN = re.compile(r"^\[ROLE:([a-zA-Z0-9_-]+)\]\s*", re.IGNORECASE)

    def __init__(self, role: str) -> None:
        """Initialize RoleMarker with a specific role."""
        self.role = role


    @staticmethod
    def format(role: str, text: str) -> str:
        """Format text with a role marker.
        Example:
            format('teammate-alice', 'Add feature') -> '[ROLE:teammate-alice] Add feature'
        """
        return f"[ROLE:{role}] {text}"


    @staticmethod
    def extract_role(text: str) -> Optional[str]:
        """Extract role name from text with role marker if present."""
        match = RoleMarker.PATTERN.match(text)
        return match.group(1).lower() if match else None


    @staticmethod
    def has_role_marker(text: str) -> bool:
        """Check if text contains a role marker."""
        return RoleMarker.PATTERN.match(text) is not None


    @staticmethod
    def strip_role_marker(text: str) -> str:
        """Remove role marker from text if present."""
        return RoleMarker.PATTERN.sub("", text)


    def _format_text(self, text: str) -> str:
        """Format text with this instance's role marker if not already present."""
        if not self.has_role_marker(text):
            return self.format(self.role, text)
        return text


    # Git operations with automatic role markers

    def commit(self, message: str, verbose: bool) -> None:
        """Create a commit with automatic role marker."""
        git.commit(self._format_text(message), verbose)


    def merge_with_message(
        self, target_branch: str, ff: bool, message: str, verbose: bool
    ) -> None:
        """Merge branches with custom message and automatic role marker."""
        git.merge_with_message(target_branch, ff, self._format_text(message), verbose)


    # GitHub PR operations with automatic role markers

    def create_pr(
        self, title: str, body: str, base: str, head: str, verbose: bool
    ) -> bool:
        """Create a pull request with automatic role markers. """
        return github_cli.create_pr(self._format_text(title), self._format_text(body), base, head, verbose)


    def comment_on_pr(self, pr_number: int, comment: str, verbose: bool) -> bool:
        """Add a comment to a pull request with automatic role marker."""
        return github_cli.comment_on_pr(pr_number, self._format_text(comment), verbose)


    def review_pr(
        self, pr_number: int, comment: str, action: str, verbose: bool
    ) -> bool:
        """Submit a review on a pull request with automatic role marker.     True if review was submitted successfully, False otherwise
        """
        return github_cli.review_pr(pr_number, self._format_text(comment), action, verbose)


    def close_pr(
        self, pr_number: int, verbose: bool, comment: Optional[str] = None
    ) -> bool:
        """Close a pull request without merging."""
        formatted_comment = self._format_text(comment) if comment else None
        return github_cli.close_pr(pr_number, verbose, formatted_comment)

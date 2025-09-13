"""Wrapper for Git CLI commands."""

from typing import List

from exercise_utils.cli import run_command


def tag(tag_name: str, verbose: bool) -> None:
    """Tags the latest commit with the given tag_name."""
    run_command(["git", "tag", tag_name], verbose)


def add(files: List[str], verbose: bool) -> None:
    """Adds a given list of file paths."""
    run_command(["git", "add", *files], verbose)


def commit(message: str, verbose: bool) -> None:
    """Creates a commit with the given message."""
    run_command(["git", "commit", "-m", message], verbose)


def empty_commit(message: str, verbose: bool) -> None:
    """Creates an empty commit with the given message."""
    run_command(["git", "commit", "-m", message, "--allow-empty"], verbose)


def checkout(branch: str, create_branch: bool, verbose: bool) -> None:
    """Checkout to the given branch, creating it if requested."""
    if create_branch:
        run_command(["git", "checkout", "-b", branch], verbose)
    else:
        run_command(["git", "checkout", branch], verbose)


def merge(target_branch: str, verbose: bool) -> None:
    """Merges the current branch with the target one.

    Forcefully sets --no-edit to avoid requiring the student to enter the commit
    message.
    """
    run_command(["git", "merge", target_branch, "--no-edit"], verbose)

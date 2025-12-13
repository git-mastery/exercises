"""Wrapper for Git CLI commands."""

from typing import List, Optional

from exercise_utils.cli import run, run_command


def tag(tag_name: str, verbose: bool) -> None:
    """Tags the latest commit with the given tag_name."""
    run_command(["git", "tag", tag_name], verbose)


def tag_with_options(tag_name: str, options: List[str], verbose: bool) -> None:
    """Tags with the given tag_name with specified options."""
    run_command(["git", "tag", tag_name, *options], verbose)


def add(files: List[str], verbose: bool) -> None:
    """Adds a given list of file paths."""
    run_command(["git", "add", *files], verbose)


# TODO(woojiahao): Maybe these should be built from a class like builder for each
# option
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


def merge(target_branch: str, ff: bool, verbose: bool) -> None:
    """Merges the current branch with the target one.

    Forcefully sets --no-edit to avoid requiring the student to enter the commit
    message.
    """
    if ff:
        run_command(["git", "merge", target_branch, "--no-edit"], verbose)
    else:
        run_command(["git", "merge", target_branch, "--no-edit", "--no-ff"], verbose)


def merge_with_message(
    target_branch: str, ff: bool, message: str, verbose: bool
) -> None:
    """Merges the current branch with the target one."""
    if ff:
        run_command(["git", "merge", target_branch, "-m", message], verbose)
    else:
        run_command(["git", "merge", target_branch, "-m", message, "--no-ff"], verbose)


def init(verbose: bool) -> None:
    """Initializes the current folder as a Git repository.

    Forces the name of the initial branch to be main.
    """
    run_command(["git", "init", "--initial-branch=main"], verbose)


def push(remote: str, branch: str, verbose: bool) -> None:
    """Push the given branch on the remote."""
    run_command(["git", "push", remote, branch], verbose)


def track_remote_branch(remote: str, branch: str, verbose: bool) -> None:
    """Tracks a remote branch locally using the same name."""
    run_command(["git", "branch", branch, f"{remote}/{branch}"], verbose)


def remove_remote(remote: str, verbose: bool) -> None:
    """Removes a given remote."""
    run_command(["git", "remote", "rm", remote], verbose)


def add_remote(remote: str, remote_url: str, verbose: bool) -> None:
    """Adds a remote with the given name and URL."""
    run_command(["git", "remote", "add", remote, remote_url], verbose)


def clone_repo_with_git(
    repository_url: str, verbose: bool, name: Optional[str] = None
) -> None:
    """Clones a Git repository. Does not require Github CLI."""
    if name is not None:
        run(["git", "clone", repository_url, name], verbose)
    else:
        run(["git", "clone", repository_url], verbose)

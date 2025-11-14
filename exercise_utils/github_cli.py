"""Wrapper for Github CLI commands."""
# TODO: The following should be built using the builder pattern

from typing import Optional

from exercise_utils.cli import run


def fork_repo(repository_name: str, fork_name: str, verbose: bool) -> None:
    """Creates a fork of a repository."""
    run(
        [
            "gh",
            "repo",
            "fork",
            repository_name,
            "--default-branch-only",
            "--fork-name",
            fork_name,
        ],
        verbose,
    )


def clone_repo(repository_name: str, verbose: bool, name: Optional[str] = None) -> None:
    """Creates a clone of a repository."""
    if name is not None:
        run(["gh", "repo", "clone", repository_name, name], verbose)
    else:
        run(["gh", "repo", "clone", repository_name], verbose)


def delete_repo(repository_name: str, verbose: bool) -> None:
    """Deletes a repository."""
    run(["gh", "repo", "delete", repository_name, "--yes"], verbose)


def create_repo(repository_name: str, verbose: bool) -> None:
    """Creates a Github repository on the current user's account."""
    run(["gh", "repo", "create", repository_name, "--public"], verbose)


def get_github_username(verbose: bool) -> str:
    """Returns the currently authenticated Github user's username."""
    result = run(["gh", "api", "user", "-q", ".login"], verbose)

    if result.is_success():
        username = result.stdout.splitlines()[0]
        return username
    return ""


def has_repo(repo_name: str, is_fork: bool, verbose: bool) -> bool:
    """Returns if the given repository exists under the current user's repositories."""
    command = ["gh", "repo", "view", repo_name]
    if is_fork:
        command.extend(["--json", "isFork", "--jq", ".isFork"])
    result = run(
        command,
        verbose,
        env={"GH_PAGER": "cat"},
    )
    return result.is_success() and result.stdout == "true"

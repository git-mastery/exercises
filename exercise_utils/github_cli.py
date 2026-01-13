"""Wrapper for Github CLI commands."""
# TODO: The following should be built using the builder pattern

from typing import Optional

from exercise_utils.cli import run


def fork_repo(
    repository_name: str,
    fork_name: str,
    verbose: bool,
    default_branch_only: bool = True,
) -> None:
    """
    Creates a fork of a repository.
    Forks only the default branch, unless specified otherwise.
    """
    command = ["gh", "repo", "fork", repository_name]
    if default_branch_only:
        command.append("--default-branch-only")
    command.extend(["--fork-name", fork_name])

    run(command, verbose)


def clone_repo_with_gh(
    repository_name: str, verbose: bool, name: Optional[str] = None
) -> None:
    """Creates a clone of a repository using Github CLI."""
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

    return result.is_success() and (not is_fork or result.stdout == "true")


def has_fork(
    repository_name: str, owner_name: str, username: str, verbose: bool
) -> bool:
    """Returns if the current user has a fork of the given repository by owner"""
    result = run(
        [
            "gh",
            "api",
            "--paginate",
            f"repos/{owner_name}/{repository_name}/forks",
            "-q",
            f'''.[] | .owner.login | select(. =="{username}")''',
        ],
        verbose,
    )

    return result.is_success() and result.stdout.strip() == username


def get_fork_name(
    repository_name: str, owner_name: str, username: str, verbose: bool
) -> str:
    """Returns the name of the current user's fork repo"""
    result = run(
        [
            "gh",
            "api",
            "--paginate",
            f"repos/{owner_name}/{repository_name}/forks",
            "-q",
            f'''.[] | select(.owner.login =="{username}") | .name''',
        ],
        verbose,
    )

    if result.is_success():
        forkname = result.stdout.splitlines()[0]
        return forkname
    return ""

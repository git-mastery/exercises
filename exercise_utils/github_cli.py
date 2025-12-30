"""Wrapper for Github CLI commands."""
# TODO: The following should be built using the builder pattern

from typing import Optional

from exercise_utils.cli import run
from repo_smith.repo_smith import RepoSmith




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


def get_github_username(rs: RepoSmith) -> str:
    """Returns the currently authenticated Github user's username."""
    result = rs.gh.api("user", jq=".login")

    if result.is_success():
        username = result.stdout.splitlines()[0]
        return username
    return ""


def get_github_git_protocol(verbose: bool) -> str:
    """returns GitHub CLI's preferred Git transport protocol"""
    result = run(["gh", "config", "get", "git_protocol"], verbose)
    if result.is_success():
        protocol = result.stdout.splitlines()[0].strip()
        return protocol
    return ""


def has_repo(rs: RepoSmith, owner_name: str, repo_name: str, is_fork: bool) -> bool:
    """Returns if the given repository exists under the current user's repositories."""
    result = (
        rs.gh.repo_view(owner_name, repo_name)
        if not is_fork
        else rs.gh.repo_view(owner_name, repo_name, jq=".isFork")
    )

    return result.is_success() and (not is_fork or result.stdout == "true")


def has_fork(
    rs: RepoSmith, owner_name: str, repository_name: str, username: str
) -> bool:
    """Returns if the current user has a fork of the given repository by owner"""
    result = rs.gh.api(
        f"repos/{owner_name}/{repository_name}/forks",
        paginate=True,
        jq=f'''.[] | .owner.login | select(. =="{username}")''',
    )

    return result.is_success() and result.stdout.strip() == username


def get_fork_name(
    rs: RepoSmith, owner_name: str, repository_name: str, username: str
) -> str:
    """Returns the name of the current user's fork repo"""
    result = rs.gh.api(
        f"repos/{owner_name}/{repository_name}/forks",
        paginate=True,
        jq=f'''.[] | select(.owner.login =="{username}") | .name''',
    )

    if result.is_success():
        forkname = result.stdout.splitlines()[0]
        return forkname
    return ""


def get_remote_url(repository_name: str, verbose: bool) -> str:
    """Returns a remote repo url based on the configured git protocol"""
    remote_url = f"https://github.com/{repository_name}.git"
    preferred_protocol = get_github_git_protocol(verbose)

    if preferred_protocol == "ssh":
        remote_url = f"git@github.com:{repository_name}.git"

    return remote_url

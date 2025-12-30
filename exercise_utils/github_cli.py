"""Wrapper for Github CLI commands."""

from repo_smith.repo_smith import RepoSmith


def get_github_username(rs: RepoSmith) -> str:
    """Returns the currently authenticated Github user's username."""
    result = rs.gh.api("user", jq=".login")

    if result.is_success():
        username = result.stdout.splitlines()[0]
        return username
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

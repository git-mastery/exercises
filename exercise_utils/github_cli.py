"""Wrapper for Github CLI commands."""
# TODO: The following should be built using the builder pattern

import re
from typing import Any, Optional

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


def get_github_git_protocol(verbose: bool) -> str:
    """returns GitHub CLI's preferred Git transport protocol"""
    result = run(["gh", "config", "get", "git_protocol"], verbose)
    if result.is_success():
        protocol = result.stdout.splitlines()[0].strip()
        return protocol
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


def get_remote_url(repository_name: str, verbose: bool) -> str:
    """Returns a remote repo url based on the configured git protocol"""
    remote_url = f"https://github.com/{repository_name}.git"
    preferred_protocol = get_github_git_protocol(verbose)

    if preferred_protocol == "ssh":
        remote_url = f"git@github.com:{repository_name}.git"

    return remote_url


def create_pr(
    title: str,
    body: str,
    base: str,
    head: str,
    repo_full_name: str,
    verbose: bool,
) -> Optional[int]:
    """Create a pull request."""
    command = [
        "gh",
        "pr",
        "create",
        "--title",
        title,
        "--body",
        body,
        "--base",
        base,
        "--head",
        head,
    ]

    command = _append_repo_flag(command, repo_full_name)

    result = run(command, verbose)
    if not result.is_success():
        return None

    match = re.search(r"/pull/(\d+)", result.stdout)
    if match is None:
        return None

    return int(match.group(1))


def _append_repo_flag(command: list[str], repo_full_name: str) -> list[str]:
    """Append --repo flag. PR commands require explicit repository context."""
    if repo_full_name.strip() == "":
        raise ValueError(
            "repo_full_name must be provided for deterministic PR commands"
        )

    command.extend(["--repo", repo_full_name])
    return command


def view_pr(pr_number: int, repo_full_name: str, verbose: bool) -> dict[str, Any]:
    """View pull request details."""
    fields = "title,body,state,author,headRefName,baseRefName,comments,reviews"

    command = ["gh", "pr", "view", str(pr_number), "--json", fields]
    command = _append_repo_flag(command, repo_full_name)

    result = run(
        command,
        verbose,
    )

    if result.is_success():
        import json

        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {}
    return {}


def comment_on_pr(
    pr_number: int,
    comment: str,
    repo_full_name: str,
    verbose: bool,
) -> bool:
    """Add a comment to a pull request."""
    command = ["gh", "pr", "comment", str(pr_number), "--body", comment]
    command = _append_repo_flag(command, repo_full_name)

    result = run(
        command,
        verbose,
    )
    return result.is_success()


def list_prs(state: str, repo_full_name: str, verbose: bool) -> list[dict[str, Any]]:
    """
    List pull requests.
    PR state filter ('open', 'closed', 'merged', 'all')
    """
    command = [
        "gh",
        "pr",
        "list",
        "--state",
        state,
        "--json",
        "number,title,state,author,headRefName,baseRefName",
    ]
    command = _append_repo_flag(command, repo_full_name)

    result = run(command, verbose)

    if result.is_success():
        import json

        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return []
    return []


def merge_pr(
    pr_number: int,
    merge_method: str,
    repo_full_name: str,
    delete_branch: bool = True,
    verbose: bool = False,
) -> bool:
    """
    Merge a pull request.
    Merge method ('merge', 'squash', 'rebase')
    """
    command = ["gh", "pr", "merge", str(pr_number), f"--{merge_method}"]

    if delete_branch:
        command.append("--delete-branch")

    command = _append_repo_flag(command, repo_full_name)

    result = run(command, verbose)
    return result.is_success()


def close_pr(
    pr_number: int,
    repo_full_name: str,
    comment: Optional[str] = None,
    verbose: bool = False,
) -> bool:
    """Close a pull request without merging."""
    command = ["gh", "pr", "close", str(pr_number)]

    if comment:
        command.extend(["--comment", comment])

    command = _append_repo_flag(command, repo_full_name)

    result = run(command, verbose)
    return result.is_success()


def review_pr(
    pr_number: int,
    comment: str,
    action: str,
    repo_full_name: str,
    verbose: bool,
) -> bool:
    """
    Submit a review on a pull request.
    Review action ('approve', 'request-changes', 'comment')
    """
    command = [
        "gh",
        "pr",
        "review",
        str(pr_number),
        "--body",
        comment,
        f"--{action}",
    ]

    command = _append_repo_flag(command, repo_full_name)

    result = run(command, verbose)
    return result.is_success()


def get_latest_pr_number_by_author(
    username: str, repo_full_name: str, verbose: bool
) -> Optional[int]:
    """Return the latest pull request number created by username in the repo."""
    command = [
        "gh",
        "pr",
        "list",
        "--author",
        username,
        "--state",
        "all",
        "--limit",
        "1",
        "--json",
        "number",
    ]
    command = _append_repo_flag(command, repo_full_name)

    result = run(command, verbose)
    if not result.is_success():
        return None

    import json

    try:
        prs = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None

    if not prs:
        return None

    pr_number = prs[0].get("number")
    return pr_number if isinstance(pr_number, int) else None

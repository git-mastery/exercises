"""Wrapper for Github CLI commands."""
# TODO: The following should be built using the builder pattern

import json
import re
from typing import Any, Optional

from exercise_utils.cli import run


_PR_STATES = {"open", "closed", "merged", "all"}
_PR_MERGE_METHODS = {"merge", "squash", "rebase"}
_PR_REVIEW_ACTIONS = {"request-changes", "comment"}


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
    repo_name: str,
    verbose: bool,
    draft: bool = False,
) -> Optional[int]:
    """Create a pull request."""
    command = _build_pr_command("create", repo_name=repo_name)
    command = _append_value_flag(command, "--title", title)
    command = _append_value_flag(command, "--body", body)
    command = _append_value_flag(command, "--base", base)
    command = _append_value_flag(command, "--head", head)
    command = _append_bool_flag(command, draft, "--draft")

    result = run(command, verbose)
    if not result.is_success():
        return None

    match = re.search(r"/pull/(\d+)", result.stdout)
    if match is None:
        return None

    return int(match.group(1))


def _append_repo_flag(command: list[str], repo_name: str) -> list[str]:
    """Append --repo flag. PR commands require explicit repository context."""
    if repo_name.strip() == "":
        raise ValueError("repo_name must be provided for deterministic PR commands")

    return [*command, "--repo", repo_name]


def _validate_choice(value: str, allowed: set[str], field_name: str) -> str:
    """Validate a string argument against a known set of values."""
    if value not in allowed:
        allowed_values = ", ".join(sorted(allowed))
        raise ValueError(
            f"Invalid {field_name}: {value}. Allowed values: {allowed_values}"
        )
    return value


def _build_pr_command(subcommand: str, *args: str, repo_name: str) -> list[str]:
    """Build a gh pr command and append deterministic repository context."""
    return _append_repo_flag(["gh", "pr", subcommand, *args], repo_name)


def _append_bool_flag(command: list[str], enabled: bool, flag: str) -> list[str]:
    """Append a CLI flag when the related boolean option is enabled."""
    return [*command, flag] if enabled else command


def _append_value_flag(command: list[str], flag: str, value: str) -> list[str]:
    """Append a value-taking CLI option in --flag=value form."""
    return [*command, f"{flag}={value}"]


def _parse_json_or_default(raw_output: str, default: Any) -> Any:
    """Parse JSON output and return a default value on decode failure."""
    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        return default


def view_pr(pr_number: int, repo_name: str, verbose: bool) -> dict[str, Any]:
    """View pull request details."""
    fields = "title,body,state,author,headRefName,baseRefName,comments,reviews"

    command = _build_pr_command(
        "view",
        str(pr_number),
        repo_name=repo_name,
    )
    command = _append_value_flag(command, "--json", fields)

    result = run(
        command,
        verbose,
    )

    if result.is_success():
        parsed = _parse_json_or_default(result.stdout, {})
        return parsed if isinstance(parsed, dict) else {}
    return {}


def comment_on_pr(
    pr_number: int,
    comment: str,
    repo_name: str,
    verbose: bool,
) -> bool:
    """Add a comment to a pull request."""
    command = _build_pr_command("comment", str(pr_number), repo_name=repo_name)
    command = _append_value_flag(command, "--body", comment)

    result = run(
        command,
        verbose,
    )
    return result.is_success()


def list_prs(
    state: str,
    repo_name: str,
    verbose: bool,
    limit: int = 30,
    search: Optional[str] = None,
) -> list[dict[str, Any]]:
    """
    List pull requests.
    PR state filter ('open', 'closed', 'merged', 'all')
    Optional search query using GitHub search syntax.
    """
    validated_state = _validate_choice(state, _PR_STATES, "state")
    fields = "number,title,state,author,headRefName,baseRefName"
    command = _build_pr_command("list", repo_name=repo_name)
    command = _append_value_flag(command, "--state", validated_state)
    command = _append_value_flag(command, "--json", fields)
    command = _append_value_flag(command, "--limit", str(limit))

    if search is not None and search.strip() != "":
        command = _append_value_flag(command, "--search", search)

    result = run(command, verbose)

    if result.is_success():
        parsed = _parse_json_or_default(result.stdout, [])
        return parsed if isinstance(parsed, list) else []
    return []


def merge_pr(
    pr_number: int,
    merge_method: str,
    repo_name: str,
    delete_branch: bool = True,
    verbose: bool = False,
) -> bool:
    """
    Merge a pull request.
    Merge method ('merge', 'squash', 'rebase')
    """
    validated_merge_method = _validate_choice(
        merge_method,
        _PR_MERGE_METHODS,
        "merge_method",
    )
    command = _build_pr_command(
        "merge",
        str(pr_number),
        f"--{validated_merge_method}",
        repo_name=repo_name,
    )

    command = _append_bool_flag(command, delete_branch, "--delete-branch")

    result = run(command, verbose)
    return result.is_success()


def close_pr(
    pr_number: int,
    repo_name: str,
    comment: Optional[str] = None,
    delete_branch: bool = False,
    verbose: bool = False,
) -> bool:
    """Close a pull request without merging."""
    command = _build_pr_command(
        "close",
        str(pr_number),
        repo_name=repo_name,
    )
    command = _append_bool_flag(command, delete_branch, "--delete-branch")

    if comment:
        command = _append_value_flag(command, "--comment", comment)

    result = run(command, verbose)
    return result.is_success()


def review_pr(
    pr_number: int,
    comment: str,
    action: str,
    repo_name: str,
    verbose: bool,
) -> bool:
    """
    Submit a review on a pull request.
    Review action ('request-changes', 'comment')
    """
    validated_action = _validate_choice(action, _PR_REVIEW_ACTIONS, "action")
    command = _build_pr_command("review", str(pr_number), repo_name=repo_name)
    command = _append_value_flag(command, "--body", comment)
    command.append(f"--{validated_action}")

    result = run(command, verbose)
    return result.is_success()


def get_pr_numbers_by_author(username: str, repo_name: str, verbose: bool) -> list[int]:
    """Return the latest opened pull request numbers created by username in the repo."""
    command = _build_pr_command("list", repo_name=repo_name)
    command = _append_value_flag(command, "--author", username)
    command = _append_value_flag(command, "--state", "open")
    command = _append_value_flag(command, "--json", "number")

    result = run(command, verbose)
    if not result.is_success():
        return []

    import json

    try:
        prs = json.loads(result.stdout)
    except json.JSONDecodeError:
        return []

    pr_numbers = [pr.get("number") for pr in prs if isinstance(pr.get("number"), int)]
    pr_numbers.sort()
    return pr_numbers


def get_latest_pr_number_by_author(
    username: str, repo_full_name: str, verbose: bool
) -> Optional[int]:
    """Return the latest open pull request number created by username in the repo."""
    if pr_numbers := get_pr_numbers_by_author(username, repo_full_name, verbose):
        return pr_numbers[-1]
    raise ValueError(f"No open PRs found for user {username} in repo {repo_full_name}.")

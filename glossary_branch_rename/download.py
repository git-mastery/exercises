import os
from pathlib import Path

from exercise_utils.cli import run_command
from exercise_utils.github_cli import delete_repo, fork_repo, get_github_username, has_repo
from exercise_utils.gitmastery import create_start_tag
from exercise_utils.git import clone_repo_with_git


def setup(verbose: bool = False):
    UPSTREAM_REPO = "git-mastery/samplerepo-funny-glossary"

    username = get_github_username(verbose)
    assert username is not None
    fork_name = f"{username}-gitmastery-samplerepo-funny-glossary"

    if has_repo(fork_name, True, verbose):
        delete_repo(fork_name, verbose)

    fork_repo(UPSTREAM_REPO, fork_name, verbose, default_branch_only=False)

    clone_repo_with_git(
        f"https://github.com/{username}/{fork_name}.git",
        verbose,
        ".",
    )

    run_command(["git", "fetch", "--all", "--prune"], verbose)

    branches = ["ABC", "DEF", "STU", "VWX"]
    for branch in branches:
        run_command(["git", "branch", "--track", branch, f"origin/{branch}"], verbose)

    run_command(["git", "checkout", "main"], verbose)
    create_start_tag(verbose)

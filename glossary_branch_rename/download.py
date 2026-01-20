import os
from pathlib import Path

from exercise_utils.cli import run_command
from exercise_utils.github_cli import delete_repo, fork_repo, get_github_username, has_repo
from exercise_utils.gitmastery import create_start_tag
from exercise_utils.git import clone_repo_with_git

__resources__ = {}


def setup(verbose: bool = False):
    upstream_repo = "git-mastery/samplerepo-funny-glossary"
    local_repo_name = "funny-glossary"

    username = get_github_username(verbose)
    assert username is not None
    fork_name = "gitmastery-samplerepo-funny-glossary"
    full_repo_name = f"{username}-{fork_name}"

    if has_repo(full_repo_name, True, verbose):
        delete_repo(full_repo_name, verbose)

    fork_repo(upstream_repo, fork_name, verbose, default_branch_only=False)

    clone_repo_with_git(
        f"https://github.com/{username}/{full_repo_name}.git",
        verbose,
        local_repo_name,
    )

    os.chdir(local_repo_name)
    run_command(["git", "fetch", "--all", "--prune"], verbose)

    run_command(
        ["git","branch", "--track", "ABC", "origin/ABC"],
        verbose,
    )
    run_command(
        ["git", "branch", "--track", "DEF", "origin/DEF"],
        verbose,
    )
    run_command(
        ["git","branch", "--track", "STU", "origin/STU"],
        verbose,
    )
    run_command(
        ["git","branch", "--track", "VWX", "origin/VWX"],
        verbose,
    )

    run_command(["git", "checkout", "main"], verbose)
    create_start_tag(verbose)

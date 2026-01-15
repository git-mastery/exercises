import os

from exercise_utils.cli import run_command
from exercise_utils.file import create_or_update_file
from exercise_utils.git import add, checkout, clone_repo_with_git, commit
from exercise_utils.github_cli import (
    delete_repo,
    get_github_username,
    has_repo,
)

__requires_git__ = True
__requires_github__ = True

REPO_OWNER = "git-mastery"
REPO_NAME = "samplerepo-funny-glossary"


def setup(verbose: bool = False):
    username = get_github_username(verbose)
    FORK_NAME = f"{username}-gitmastery-samplerepo-funny-glossary"

    if has_repo(FORK_NAME, True, verbose):
        delete_repo(FORK_NAME, verbose)

    run_command(
        ["gh", "repo", "fork", f"{REPO_OWNER}/{REPO_NAME}", "--fork-name", FORK_NAME],
        verbose,
    )

    clone_repo_with_git(
        f"https://github.com/{username}/{FORK_NAME}", verbose, "."
    )

    checkout("PQR", True, verbose)

    create_or_update_file(
        "r.txt",
        "refactoring: Improving the code without changing what it does... in theory.\n",
    )

    add(["r.txt"], verbose)
    commit("Add 'refactoring'", verbose)

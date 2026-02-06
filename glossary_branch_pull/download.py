from exercise_utils.cli import run_command
from exercise_utils.file import create_or_update_file
from exercise_utils.git import add, checkout, commit, remove_remote
from exercise_utils.github_cli import (
    clone_repo_with_gh,
    get_github_username,
    fork_repo,
    has_repo,
    delete_repo,
)

TARGET_REPO = "git-mastery/samplerepo-funny-glossary"
FORK_NAME = "gitmastery-samplerepo-funny-glossary"


def setup(verbose: bool = False):
    username = get_github_username(verbose)
    full_repo_name = f"{username}/{FORK_NAME}"

    if has_repo(full_repo_name, True, verbose):
        delete_repo(full_repo_name, verbose)

    fork_repo(TARGET_REPO, FORK_NAME, verbose, False)
    clone_repo_with_gh(f"{username}/{FORK_NAME}", verbose, ".")
    remove_remote("upstream", verbose)

    run_command(["git", "branch", "-dr", "origin/VWX"], verbose)

    checkout("ABC", False, verbose)
    run_command(["git", "reset", "--hard", "HEAD~1"], verbose)

    checkout("DEF", False, verbose)
    run_command(["git", "reset", "--hard", "HEAD~1"], verbose)
    create_or_update_file(
        "d.txt",
        """
        documentation: Evidence that someone once cared.
        """,
    )
    add(["d.txt"], verbose)
    commit("Add 'documentation'", verbose)

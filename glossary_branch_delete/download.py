from exercise_utils.cli import run_command
from exercise_utils.git import clone_repo_with_git
from exercise_utils.github_cli import (
    delete_repo,
    get_github_username,
    has_repo,
)
from exercise_utils.gitmastery import create_start_tag

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
        f"https://github.com/{username}/{FORK_NAME}", verbose, "funny-glossary"
    )

    create_start_tag(verbose)

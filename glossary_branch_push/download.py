from exercise_utils.file import create_or_update_file
from exercise_utils.git import add, checkout, commit
from exercise_utils.github_cli import (
    clone_repo_with_gh,
    delete_repo,
    fork_repo,
    get_github_username,
    has_repo,
)

REPO_OWNER = "git-mastery"
REPO_NAME = "samplerepo-funny-glossary"


def setup(verbose: bool = False):
    username = get_github_username(verbose)
    FORK_NAME = f"{username}-gitmastery-samplerepo-funny-glossary"

    if has_repo(FORK_NAME, True, verbose):
        delete_repo(FORK_NAME, verbose)

    fork_repo(f"{REPO_OWNER}/{REPO_NAME}", FORK_NAME, verbose, False)

    clone_repo_with_gh(f"https://github.com/{username}/{FORK_NAME}", verbose, ".")

    checkout("PQR", True, verbose)

    create_or_update_file(
        "r.txt",
        "refactoring: Improving the code without changing what it does... in theory.\n",
    )

    add(["r.txt"], verbose)
    commit("Add 'refactoring'", verbose)

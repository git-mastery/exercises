from exercise_utils.git import checkout
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

    # creates VWX branch locally, tracking remote branch
    checkout("VWX", False, verbose)
    checkout("main", False, verbose)

from exercise_utils.github_cli import (
    clone_repo_with_gh,
    delete_repo,
    fork_repo,
    get_github_username,
    has_repo,
)
from exercise_utils.git import remove_remote, track_remote_branch

UPSTREAM_REPO = "git-mastery/samplerepo-funny-glossary"
BRANCHES = ["ABC", "DEF", "STU", "VWX"]


def setup(verbose: bool = False):
    username = get_github_username(verbose)
    FORK_NAME = f"{username}-gitmastery-samplerepo-funny-glossary"

    if has_repo(FORK_NAME, True, verbose):
        delete_repo(FORK_NAME, verbose)

    fork_repo(UPSTREAM_REPO, FORK_NAME, verbose, default_branch_only=False)

    clone_repo_with_gh(
        f"{username}/{FORK_NAME}",
        verbose,
        ".",
    )
    remove_remote("upstream", verbose)

    for branch in BRANCHES:
        track_remote_branch("origin", branch, verbose)

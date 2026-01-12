from exercise_utils.git import clone_repo_with_git
from exercise_utils.github_cli import (
    fork_repo,
    get_fork_name,
    get_github_username,
    has_fork,
)

__requires_git__ = True
__requires_github__ = True

REPO_NAME = "samplerepo-company"
REPO_OWNER = "git-mastery"
FORK_NAME = "gitmastery-samplerepo-company"


def download(verbose: bool):
    username = get_github_username(verbose)

    if not has_fork(REPO_NAME, REPO_OWNER, username, verbose):
        fork_repo(f"{REPO_OWNER}/{REPO_NAME}", FORK_NAME, verbose, False)

    existing_name = get_fork_name(REPO_NAME, REPO_OWNER, username, verbose)
    clone_repo_with_git(
        f"https://github.com/{username}/{existing_name}", verbose, FORK_NAME
    )

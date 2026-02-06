import os
from exercise_utils.git import remove_remote
from exercise_utils.github_cli import (
    clone_repo_with_gh,
    delete_repo,
    fork_repo,
    get_fork_name,
    get_github_username,
    has_repo,
)

__requires_git__ = True
__requires_github__ = True

REPO_NAME = "samplerepo-company"
REPO_OWNER = "git-mastery"
FORK_NAME = "gitmastery-samplerepo-company"


def download(verbose: bool):
    username = get_github_username(verbose)
    full_repo_name = f"{username}/{FORK_NAME}"

    if has_repo(full_repo_name, True, verbose):
        delete_repo(full_repo_name, verbose)

    fork_repo(f"{REPO_OWNER}/{REPO_NAME}", FORK_NAME, verbose, False)

    existing_name = get_fork_name(REPO_NAME, REPO_OWNER, username, verbose)
    clone_repo_with_gh(f"{username}/{existing_name}", verbose, REPO_NAME)
    os.chdir(REPO_NAME)
    remove_remote("upstream", verbose)

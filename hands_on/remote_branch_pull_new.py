import os

from exercise_utils.file import append_to_file
from exercise_utils.git import delete_remote_tracking_branch_locally, remove_remote,  add, checkout, commit, push
from exercise_utils.github_cli import (
    get_github_username, fork_repo,
    has_repo,
    delete_repo,
    clone_repo_with_gh,
)

__requires_git__ = True
__requires_github__ = True

TARGET_REPO = "git-mastery/samplerepo-company"
FORK_NAME = "gitmastery-samplerepo-company"
LOCAL_DIR = "samplerepo-company"

def download(verbose: bool):
    username = get_github_username(verbose)
    full_repo_name = f"{username}/{FORK_NAME}"

    if has_repo(full_repo_name, True, verbose):
        delete_repo(full_repo_name, verbose)

    fork_repo(TARGET_REPO, FORK_NAME, verbose, False)
    clone_repo_with_gh(full_repo_name, verbose, LOCAL_DIR)

    os.chdir(LOCAL_DIR)

    remove_remote("upstream", verbose)
    delete_remote_tracking_branch_locally("origin", "track-sales", verbose)

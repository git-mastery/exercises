import os

from exercise_utils.git import remove_remote, run_command, track_remote_branch
from exercise_utils.github_cli import (
    clone_repo_with_gh,
    delete_repo,
    fork_repo,
    get_github_username,
    has_repo,
)

__requires_git__ = True
__requires_github__ = True

TARGET_REPO = "git-mastery/samplerepo-company-2"
FORK_NAME = "gitmastery-samplerepo-company-2"
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
    track_remote_branch("origin", "track-sales", verbose)
    run_command(["git", "branch", "-dr", "origin/track-sales"], verbose)

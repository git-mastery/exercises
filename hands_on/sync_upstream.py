import os

from exercise_utils.cli import run_command
from exercise_utils.git import add_remote
from exercise_utils.github_cli import (
    get_github_username,
    fork_repo,
    clone_repo_with_gh,
    has_repo,
    delete_repo,
)

__requires_git__ = True
__requires_github__ = True


TARGET_REPO = "git-mastery/samplerepo-finances-2"
FORK_NAME = "gm-samplerepo-finances-2"
LOCAL_DIR = "samplerepo-finances"


def download(verbose: bool):
    username = get_github_username(verbose)
    full_repo_name = f"{username}/{FORK_NAME}"

    if has_repo(full_repo_name, True, verbose):
        delete_repo(full_repo_name, verbose)

    fork_repo(TARGET_REPO, FORK_NAME, verbose)

    clone_repo_with_gh(full_repo_name, verbose, LOCAL_DIR)

    os.chdir(LOCAL_DIR)
    add_remote("upstream", f"https://github.com/{TARGET_REPO}", verbose)

    # Delete last two commits to simulate upstream having more commits than local
    run_command(["git", "reset", "--hard", "HEAD~2"], verbose)

    # Force-push to fork
    run_command(["git", "push", "-f", "origin", "master"], verbose)
    
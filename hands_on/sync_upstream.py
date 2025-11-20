import os

from exercise_utils.git import add_remote
from exercise_utils.github_cli import (
    get_github_username,
    fork_repo,
    clone_repo,
    has_repo,
    delete_repo
)

__requires_git__ = True
__requires_github__ = True


TARGET_REPO = "git-mastery/samplerepo-finances"
LOCAL_DIR = "gitmastery-samplerepo-finances"

def download(verbose: bool):
    username = get_github_username(verbose)
    full_repo_name = f"{username}/{LOCAL_DIR}"

    if has_repo(full_repo_name, True, verbose):
        delete_repo(full_repo_name, verbose)

    fork_repo(TARGET_REPO, LOCAL_DIR, verbose)

    clone_repo(full_repo_name, verbose)

    os.chdir(LOCAL_DIR)
    add_remote("origin", f"https://github.com/{full_repo_name}", verbose)

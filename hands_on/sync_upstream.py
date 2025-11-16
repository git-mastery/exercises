import os
import sys
import shutil

from exercise_utils.github_cli import (
    get_github_username,
    fork_repo,
    clone_repo,
    has_repo,
)

__requires_git__ = True
__requires_github__ = True


TARGET_REPO = "git-mastery/samplerepo-finances"
LOCAL_DIR = "samplerepo-finances"


def _get_full_repo_name(verbose: bool) -> str:
    username = get_github_username(verbose)
    return f"{username}/{LOCAL_DIR}"


def download(verbose: bool):
    full_repo_name = _get_full_repo_name(verbose)

    if has_repo(full_repo_name, is_fork=True, verbose=verbose):
        print(
            f"\nRepository 'https://github.com/{full_repo_name}' already exists on GitHub.\n"
            "Please delete the existing fork before proceeding."
        )
        sys.exit(1)

    if os.path.exists(LOCAL_DIR):
        shutil.rmtree(LOCAL_DIR)

    fork_repo(TARGET_REPO, fork_name="samplerepo-finances", verbose=verbose)

    clone_repo(full_repo_name, verbose=verbose)

    os.chdir(LOCAL_DIR)
    os.system(f"git remote add upstream https://github.com/{TARGET_REPO}")


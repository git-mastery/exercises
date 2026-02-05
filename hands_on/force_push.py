import os
from exercise_utils.cli import run_command
from exercise_utils.git import add_remote, remove_remote
from exercise_utils.github_cli import (
    clone_repo_with_gh,
    create_repo,
    get_remote_url,
    get_github_username,
)

__requires_git__ = True
__requires_github__ = True

REPO_NAME = "gitmastery-samplerepo-things"
UPSTREAM_REPO = "git-mastery/samplerepo-things"
WORK_DIR = "things"


def download(verbose: bool):
    username = get_github_username(verbose)
    remote_repo = f"{username}/{REPO_NAME}"
    remote_url = get_remote_url(remote_repo, verbose)

    create_repo(REPO_NAME, verbose)
    clone_repo_with_gh(UPSTREAM_REPO, verbose, WORK_DIR)
    os.chdir(WORK_DIR)
    remove_remote("origin", verbose)

    add_remote(
        "origin",
        remote_url,
        verbose,
    )
    run_command(["git", "push", "-u", "origin", "main"], verbose)

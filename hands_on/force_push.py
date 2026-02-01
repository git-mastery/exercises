import os
from exercise_utils.cli import run_command
from exercise_utils.git import add_remote, remove_remote
from exercise_utils.github_cli import (
    clone_repo_with_gh,
    create_repo,
    get_github_git_protocol,
    get_github_username,
)

__requires_git__ = True
__requires_github__ = True

REPO_NAME = "gitmastery-samplerepo-things"
UPSTREAM_REPO = "git-mastery/samplerepo-things"
WORK_DIR = "things"


def download(verbose: bool):
    username = get_github_username(verbose)
    remote_url = f"https://github.com/{username}/{REPO_NAME}"

    create_repo(REPO_NAME, verbose)
    clone_repo_with_gh(UPSTREAM_REPO, verbose, WORK_DIR)
    os.chdir(WORK_DIR)
    remove_remote("origin", verbose)

    github_protocol = get_github_git_protocol(verbose)
    if github_protocol == "ssh":
        remote_url = f"gihub@github.com:{username}/{REPO_NAME}.git"

    add_remote(
        "origin",
        remote_url,
        verbose,
    )
    run_command(["git", "push", "-u", "origin", "main"], verbose)

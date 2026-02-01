from logging import info
from exercise_utils.cli import run_command
import os

from exercise_utils.git import clone_repo_with_git
from exercise_utils.github_cli import get_github_git_protocol

__requires_git__ = True
__requires_github__ = True


def download(verbose: bool):
    ahead_repo = "https://github.com/git-mastery/samplerepo-finances-2.git"
    git_protocol = get_github_git_protocol(verbose)
    if git_protocol == "ssh":
        ahead_repo = "git@github.com:git-mastery/samplerepo-finances-2.git"
    clone_repo_with_git(
        "https://github.com/git-mastery/samplerepo-finances.git", verbose
    )
    os.chdir("samplerepo-finances")
    run_command(
        [
            "git",
            "remote",
            "set-url",
            "origin",
            ahead_repo,
        ],
        verbose,
    )

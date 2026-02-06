from exercise_utils.cli import run_command
import os

from exercise_utils.git import clone_repo_with_git
from exercise_utils.github_cli import get_remote_url

__requires_git__ = True
__requires_github__ = True


def download(verbose: bool):
    ahead_repo = "git-mastery/samplerepo-finances-2"
    ahead_repo_url = get_remote_url(ahead_repo, verbose)

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
            ahead_repo_url,
        ],
        verbose,
    )

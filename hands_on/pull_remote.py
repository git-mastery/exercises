import os

from exercise_utils.git import clone_repo_with_git
from exercise_utils.cli import run_command

__requires_git__ = True
__requires_github__ = False


def download(verbose: bool):
    os.makedirs("samplerepo-finances")
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
            "https://github.com/git-mastery/samplerepo-finances-2.git",
        ],
        verbose,
    )

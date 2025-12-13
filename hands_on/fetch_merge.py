import os

from exercise_utils.git import add_remote, clone_repo_with_git, remove_remote

__requires_git__ = True
__requires_github__ = False


def download(verbose: bool):
    clone_repo_with_git(
        "https://github.com/git-mastery/samplerepo-finances.git", verbose
    )
    os.chdir("samplerepo-finances")
    remove_remote("origin", verbose)
    add_remote(
        "origin", "https://github.com/git-mastery/samplerepo-finances-2", verbose
    )

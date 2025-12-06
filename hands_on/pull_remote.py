import os

from exercise_utils.git import add_remote, clone_repo_with_git

__requires_git__ = True
__requires_github__ = False


def download(verbose: bool):
    os.makedirs("samplerepo-finances")
    clone_repo_with_git(
        "https://github.com/git-mastery/samplerepo-finances.git", verbose
    )
    os.chdir("samplerepo-finances")
    add_remote(
        "origin", "https://github.com/git-mastery/samplerepo-finances-2.git", verbose
    )

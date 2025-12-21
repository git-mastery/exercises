import os

from exercise_utils.git import init


__requires_git__ = True
__requires_github__ = False


def download(verbose: bool):
    os.makedirs("things")
    os.chdir("things")
    init(verbose)

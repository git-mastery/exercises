import os

__requires_git__ = True
__requires_github__ = False


def download(verbose: bool):
    os.makedirs("things")

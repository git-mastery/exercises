import os

from utils.cmd import run_command

__requires_git__ = True
__requires_github__ = False


def download(verbose: bool):
    os.makedirs("things")
    os.chdir("things")
    run_command(["git", "init", "--initial-branch=main"], verbose)

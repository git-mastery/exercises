import os
from exercise_utils import cli

__requires_git__ = True
__requires_github__ = False


def download(verbose: bool):
    os.makedirs("things")
    os.chdir("things")
    cli.run_command(["git", "init", "--initial-branch=main"], verbose)

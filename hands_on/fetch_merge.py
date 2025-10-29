import os

from exercise_utils.cli import run_command
from exercise_utils.gitmastery import create_start_tag

__requires_git__ = True
__requires_github__ = True


def download(verbose: bool):
    os.makedirs("samplerepo-finances")
    # Clone the samplerepo-finances repo
    run_command(["git", "clone", "https://github.com/git-mastery/samplerepo-finances.git"], verbose) 
    os.chdir("samplerepo-finances")
    # Change the remote origin to point to samplerepo-finances-2
    run_command(["git", "remote", "set-url", "origin", "https://github.com/git-mastery/samplerepo-finances-2.git"], verbose) 

    pass

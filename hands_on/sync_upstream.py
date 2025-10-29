import os
import shutil
from exercise_utils.cli import run_command
from exercise_utils.gitmastery import create_start_tag

__requires_git__ = True
__requires_github__ = True

def download(verbose: bool):
    # Clean up if there exist the same name folder
    if os.path.exists("samplerepo-finances"):
        shutil.rmtree("samplerepo-finances")

    # Fork the samplerepo-finances repository and clone it locally
    run_command([
        "gh", "repo", "fork",
        "https://github.com/git-mastery/samplerepo-finances",
        "--clone",
        "--remote"
    ], verbose)

    # Navigate into samplerepo-finances directory
    os.chdir("samplerepo-finances")

    # Add the upstream remote pointing to the samplerepo-finances repository
    run_command([
        "git", "remote", "add", "upstream",
        "https://github.com/git-mastery/samplerepo-finances"
    ], verbose)

    # Mark this as the starting state
    create_start_tag("hp-sync-upstream", verbose)

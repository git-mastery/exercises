import os
import sys
import shutil
from exercise_utils.cli import run_command, run_command_no_exit

__requires_git__ = True
__requires_github__ = True


def _get_full_repo_name(verbose: bool) -> str:
    """Get the full GitHub repository name for the authenticated user."""
    output = run_command(["gh", "api", "user", "-q", ".login"], verbose)
    username = output.strip() if output else ""
    return f"{username}/{"samplerepo-finances"}"

def download(verbose: bool):
    full_repo_name = _get_full_repo_name(verbose)
    output = run_command_no_exit(["gh", "repo", "view", full_repo_name], verbose)

    if output is not None:
        print(
            f"\nRepository 'https://github.com/{full_repo_name}' already exists on GitHub.\n"
            "Please delete the existing fork before proceeding."
        )
        sys.exit(1)
    
    if os.path.exists("samplerepo-finances"):
        shutil.rmtree("samplerepo-finances")

    run_command([
        "gh", "repo", "fork",
        "https://github.com/git-mastery/samplerepo-finances",
        "--clone",
        "--remote"
    ], verbose)

    os.chdir("samplerepo-finances")

    run_command([
        "git", "remote", "add", "upstream",
        "https://github.com/git-mastery/samplerepo-finances"
    ], verbose)

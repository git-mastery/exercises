from exercise_utils.cli import run_command
from exercise_utils.gitmastery import create_start_tag

import os
from pathlib import Path

__requires_git__ = True
__requires_github__ = True


def download(verbose: bool):
    """
    hp-move-tags (T4L2)
    - Fork https://github.com/git-mastery/samplerepo-preferences to user account
    - Clone the fork locally as 'samplerepo-preferences'
    - Create:
        * lightweight tag `v1.0` on HEAD
        * annotated tag  `v0.9` on HEAD~2 with message "First beta release"
    """

    # Ensure GitHub CLI is authenticated
    gh_user = run_command(["gh", "api", "user", "--jq", ".login"], verbose).strip()
    if not gh_user:
        raise RuntimeError("GitHub CLI not authenticated. Run `gh auth login` and retry.")

    upstream = "git-mastery/samplerepo-preferences"
    target_dir = Path("samplerepo-preferences")

    # Fresh sandbox, if re-downloading
    if target_dir.exists():
        import shutil
        shutil.rmtree(target_dir)

    # Fork to user's account and clone here; origin -> user's fork, upstream -> original
    run_command(["gh", "repo", "fork", upstream, "--clone=true", "--remote=true"], verbose)

    if not target_dir.exists():
        raise RuntimeError("Expected 'samplerepo-preferences' not found after fork/clone.")

    os.chdir(target_dir)

    # Prepare the tags
    run_command(["git", "tag", "v1.0"], verbose)  # lightweight on HEAD
    run_command(["git", "tag", "-a", "v0.9", "HEAD~2", "-m", "First beta release"], verbose)

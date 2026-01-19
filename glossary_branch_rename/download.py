import os
from pathlib import Path

from exercise_utils.cli import run_command, run_command_no_exit
from exercise_utils.github_cli import get_github_username
from exercise_utils.gitmastery import create_start_tag

__resources__ = {}


def setup(verbose: bool = False):
    upstream_repo = "git-mastery/samplerepo-funny-glossary"
    local_repo_name = "funny-glossary"

    username = get_github_username(verbose)
    assert username is not None
    fork_name = f"{username}-gitmastery-samplerepo-funny-glossary"

    local_repo_path = Path(local_repo_name)
    if local_repo_path.exists():
        # If the repo already exists, refresh refs instead of recloning.
        run_command(["git", "-C", local_repo_name, "fetch", "--all", "--prune"], verbose)
    else:
        run_command(
            [
                "gh",
                "repo",
                "fork",
                upstream_repo,
                "--clone",
                "--fork-name",
                fork_name,
                "--",
                local_repo_name,
            ],
            verbose,
        )

    run_command(
        ["git", "-C", local_repo_name, "remote", "remove", "upstream"], verbose
    )

    create_start_tag(verbose)

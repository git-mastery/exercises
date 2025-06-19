import os
import subprocess
from sys import exit
from typing import List, Optional


def run_command(command: List[str], verbose: bool) -> Optional[str]:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )
        if verbose:
            print(result.stdout)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        if verbose:
            print(e.stderr)
        exit(1)


def setup(verbose: bool = False):
    username = run_command(["gh", "api", "user", "-q", ".login"], verbose=verbose)
    fork_name = f"{username}-gitmastery-push-over"

    has_fork = run_command(
        [
            "gh",
            "repo",
            "view",
            fork_name,
            "--json",
            "isFork",
            "--jq",
            ".isFork",
        ],
        verbose,
    )

    if not has_fork:
        run_command(
            [
                "gh",
                "repo",
                "fork",
                "git-mastery/push-over",
                "--default-branch-only",
                "--fork-name",
                fork_name,
            ],
            verbose=verbose,
        )

    has_clone = os.path.isdir(fork_name)

    if not has_clone:
        run_command(["gh", "repo", "clone", f"{username}/{fork_name}"], verbose=verbose)

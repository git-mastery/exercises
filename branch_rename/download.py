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
        return result.stdout
    except subprocess.CalledProcessError as e:
        if verbose:
            print(e.stderr)
        exit(1)


def setup(verbose: bool = False):
    run_command(["git", "checkout", "-b", "login"], verbose)
    run_command(
        ["git", "commit", "--allow-empty", "-m", "Implement login feature"], verbose
    )

    run_command(["git", "checkout", "main"], verbose)

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
    run_command(["git", "commit", "--allow-empty", "-m", "Implement loading"], verbose)
    run_command(["git", "commit", "--allow-empty", "-m", "Fix loading bug"], verbose)

    run_command(["git", "checkout", "-b", "optimization-approach-1"], verbose)
    run_command(["git", "commit", "--allow-empty", "-m", "Apply bubble sort"], verbose)
    run_command(["git", "commit", "--allow-empty", "-m", "Fix sorting bug"], verbose)

    run_command(["git", "checkout", "main"], verbose)
    run_command(["git", "checkout", "-b", "optimization-approach-2"], verbose)
    run_command(
        [
            "git",
            "commit",
            "--allow-empty",
            "-m",
            "Apply merge sort",
        ],
        verbose,
    )

    run_command(["git", "checkout", "main"], verbose)
    run_command(
        ["git", "merge", "optimization-approach-1", "--no-ff", "--no-edit"], verbose
    )

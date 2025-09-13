"""General utility functions for running CLI commands."""

import subprocess
from sys import exit
from typing import List, Optional


def run_command(command: List[str], verbose: bool) -> Optional[str]:
    """Runs the given command, logging the output if verbose is turned on.

    Exits if the command fails.
    """
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


def run_command_no_exit(command: List[str], verbose: bool) -> Optional[str]:
    """Runs the given command, logging the output if verbose is turned on.

    Does not exit if the command fails.
    """
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
        return None

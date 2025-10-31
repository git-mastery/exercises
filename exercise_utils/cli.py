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


def run_command_with_code(command: List[str], verbose: bool) -> tuple[Optional[str], int]:
    """Runs the given command and returns (output, return code)."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )
        if verbose:
            print(result.stdout)
        return result.stdout, result.returncode
    except subprocess.CalledProcessError as e:
        if verbose:
            print(e.stderr)
        return e.stderr, e.returncode

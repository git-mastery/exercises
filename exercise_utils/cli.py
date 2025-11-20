"""General utility functions for running CLI commands."""

import os
import subprocess
from dataclasses import dataclass
from subprocess import CompletedProcess
from sys import exit
from typing import Dict, List, Optional


@dataclass
class CommandResult:
    result: CompletedProcess[str]

    def is_success(self) -> bool:
        return self.result.returncode == 0

    @property
    def stdout(self) -> str:
        return self.result.stdout.strip()

    @property
    def returncode(self) -> int:
        return self.result.returncode


def run(
    command: List[str],
    verbose: bool,
    env: Dict[str, str] = {},
    exit_on_error: bool = False,
) -> CommandResult:
    """Runs the given command, logging the output if verbose is True."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            env=dict(os.environ, **env),
            encoding="utf-8",
        )
    except FileNotFoundError:
        if exit_on_error:
            exit(1)
        error_msg = f"Command not found: {command[0]}"
        result = CompletedProcess(command, returncode=127, stdout="", stderr=error_msg)
    except PermissionError:
        if exit_on_error:
            exit(1)
        error_msg = f"Permission denied: {command[0]}"
        result = CompletedProcess(command, returncode=126, stdout="", stderr=error_msg)
    except OSError as e:
        if exit_on_error:
            exit(1)
        error_msg = f"OS error when running command {command}: {e}"
        result = CompletedProcess(command, returncode=1, stdout="", stderr=error_msg)

    if verbose:
        if result.returncode == 0:
            print("\t" + result.stdout)
        else:
            print("\t" + result.stderr)

    return CommandResult(result=result)


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

import os
import pathlib
import subprocess
import textwrap
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


def create_or_update_file(
    filepath: str | pathlib.Path, contents: Optional[str] = None
) -> None:
    if os.path.dirname(filepath) != "":
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if contents is None:
        open(filepath, "a").close()
    else:
        with open(filepath, "w") as file:
            file.write(textwrap.dedent(contents).lstrip())


def setup(verbose: bool = False):
    crew = [
        "josh.txt",
        "adam.txt",
        "mary.txt",
        "jane.txt",
        "charlie.txt",
        "kristen.txt",
        "alice.txt",
        "john.txt",
    ]
    for member in crew:
        create_or_update_file(member)

    run_command(["git", "add", "."], verbose)

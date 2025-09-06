import os
import subprocess
from sys import exit
from typing import List, Optional

__requires_git__ = True
__requires_github__ = False


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


def download(verbose: bool):
    os.makedirs("things")
    os.chdir("things")
    run_command(["git", "init", "--initial-branch=main"], verbose)
    with open("fruits.txt", "w") as f:
        f.write("apples\nbananas\ncherries\n")
    run_command(["git", "add", "fruits.txt"], verbose)
    with open("fruits.txt", "a") as f:
        f.write("dragon fruits\n")

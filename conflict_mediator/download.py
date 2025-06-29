import os
import pathlib
import subprocess
import textwrap
from sys import exit
from typing import List, Optional

__resources__ = {"script.py": "script.py"}


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
    commits_str = run_command(
        ["git", "log", "--reverse", "--pretty=format:%h"], verbose
    )
    assert commits_str is not None
    first_commit = commits_str.split("\n")[-1]
    tag_name = f"git-mastery-start-{first_commit}"
    run_command(["git", "tag", tag_name], verbose)

    run_command(["git", "checkout", "-b", "A"], verbose)
    create_or_update_file("script.py", "print('Hello World!')")
    run_command(["git", "add", "script.py"], verbose)
    run_command(["git", "commit", "-m", "Hello world"], verbose)

    run_command(["git", "checkout", "main"], verbose)
    run_command(["git", "checkout", "-b", "B"], verbose)
    create_or_update_file("script.py", "print('Hello Everyone!')")
    run_command(["git", "add", "script.py"], verbose)
    run_command(["git", "commit", "-m", "Hello everyone"], verbose)

    run_command(["git", "checkout", "main"], verbose)
    run_command(["git", "merge", "A", "--no-edit"], verbose)
    run_command(["git", "merge", "B", "--no-edit"], verbose)

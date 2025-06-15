import os
import subprocess
from pathlib import Path
from sys import exit
from typing import List, Optional

__resources__ = {".gitignore": ".gitignore"}


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


def create_file(filename: str, contents: Optional[str] = None) -> None:
    os.makedirs(Path(filename).parent, exist_ok=True)
    if contents is None:
        open(filename, "a").close()
    else:
        with open(filename, "a") as file:
            file.write(contents)


def setup(verbose: bool = False):
    # Running these before since we want to generate the new files after to avoid
    # committing them
    commits_str = run_command(
        ["git", "log", "--reverse", "--pretty=format:%h"], verbose
    )
    assert commits_str is not None
    first_commit = commits_str.split("\n")[0]
    tag_name = f"git-mastery-start-{first_commit}"
    run_command(["git", "tag", tag_name], verbose)

    os.makedirs("many", exist_ok=True)
    for i in range(1, 101):
        create_file(f"many/file{i}.txt", str(i))

    create_file("ignore_me.txt", "You should not even see me!")
    create_file("why_am_i_hidden.txt", "Why am I getting hidden??")
    create_file(
        "this/is/very/nested/find_me.txt", "You should have been able to find me"
    )
    create_file("this/is/very/nested/runaway.txt", "Oh no")

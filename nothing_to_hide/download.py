import os
from pathlib import Path
import subprocess
import textwrap
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


def create_file(file_name: str, contents: str) -> None:
    os.makedirs(Path(file_name).parent, exist_ok=True)
    with open(file_name, "w") as file:
        file.write(textwrap.dedent(contents).strip())


def setup(verbose: bool = False):
    create_file("src/script.py", 'print("hello world!")')
    create_file(
        "src/.env",
        """
        KEY=secretshhh
        KEY=secretshhh
        """,
    )
    create_file(
        "sensitive/names.txt",
        """
        John
        Alice
        Bob
        Michael
        """,
    )
    for i in range(1, 6):
        create_file(f"sensitive/sensitive_{i}.txt", "")

    create_file(
        ".gitignore",
        """
        sensitive/*
        res/hidden.png
        src/.env
        !sensitive/names.txt
        """,
    )
    run_command(["git", "add", ".gitignore"], verbose)
    run_command(["git", "commit", "-m", "Add files"], verbose)

    commits_str = run_command(
        ["git", "log", "--reverse", "--pretty=format:%h"], verbose
    )
    assert commits_str is not None
    first_commit = commits_str.split("\n")[0]
    tag_name = f"git-mastery-start-{first_commit}"
    run_command(["git", "tag", tag_name], verbose)

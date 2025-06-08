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
    for i in range(1, 101):
        if i == 77:
            continue
        open(f"file{i}.txt", "a").close()

    run_command(["git", "add", "file*.txt"], verbose)
    run_command(["git", "commit", "-m", "Change 1"], verbose)

    with open("file14.txt", "a") as file:
        file.write("This is a change")

    open("file77.txt", "a").close()
    run_command(["chmod", "-w", "file{1..100}.txt"], verbose)

    commits_str = run_command(
        ["git", "log", "--reverse", "--pretty=format:%h"], verbose
    )
    assert commits_str is not None
    first_commit = commits_str.split("\n")[0]
    tag_name = f"git-mastery-start-{first_commit}"
    run_command(["git", "tag", tag_name], verbose)

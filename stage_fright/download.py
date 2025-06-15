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
    names = ["alice", "bob", "joe", "jim", "carrey"]
    for name in names:
        open(f"{name}.txt", "a").close()
    run_command(["git", "add", "jim.txt"], verbose)
    run_command(["git", "add", "carrey.txt"], verbose)
    commits_str = run_command(
        ["git", "log", "--reverse", "--pretty=format:%h"], verbose
    )
    assert commits_str is not None
    first_commit = commits_str.split(" ")[0]
    tag_name = f"git-mastery-start-{first_commit}"
    run_command(["git", "tag", tag_name], verbose)

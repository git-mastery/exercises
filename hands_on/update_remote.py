import os
import subprocess

from exercise_utils.cli import run_command
from exercise_utils.file import create_or_update_file, append_to_file
from exercise_utils.git import add, init, commit

__requires_git__ = True
__requires_github__ = True

REPO_NAME = "gitmastery-update-remote-things"

def download(verbose: bool):
    username = run_command(["gh", "api", "user", "-q", ".login"], verbose).strip()
    os.makedirs("things")
    os.chdir("things")
    init(verbose)
    create_or_update_file("fruits.txt", """
        apples
        bananas
        cherries
        dragon fruits
        """,
    )
    add(["fruits.txt"], verbose)
    append_to_file("fruits.txt", """
        figs
        """,
    )
    add(["fruits.txt"], verbose)
    commit("Insert figs into fruits.txt", verbose)
    create_or_update_file("colours.txt", """
        a file for colours 
        """,
    )
    create_or_update_file("shapes.txt", """
        a file for shapes 
        """,
    )
    add(["colours.txt", "shapes.txt"], verbose)
    commit("Add colours.txt, shapes.txt", verbose)
    repo_check = subprocess.run(
        ["gh", "repo", "view", f"{username}/{REPO_NAME}"],
        capture_output=True,
        text=True
    )

    if repo_check.returncode == 0:
        run_command(["gh", "repo", "delete", REPO_NAME, "--yes"], verbose)

    run_command(["gh", "repo", "create", REPO_NAME, "--public"], verbose)
    run_command(["git", "remote", "add", "origin", f"https://github.com/{username}/{REPO_NAME}"], verbose)

    default_branch = run_command(["git", "branch", "--list", "main", "master"], verbose).strip()
    if "main" in default_branch:
        default_branch = "main"
    else:
        default_branch = "master"

    run_command(["git", "push", "-u", "origin", default_branch], verbose)
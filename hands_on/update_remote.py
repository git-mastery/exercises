import os

from exercise_utils.cli import run_command
from exercise_utils.file import create_or_update_file, append_to_file
from exercise_utils.git import add, init, commit, add_remote
from exercise_utils.github_cli import (
    delete_repo,
    get_remote_url,
    has_repo,
    get_github_username,
    create_repo,
)

__requires_git__ = True
__requires_github__ = True

REPO_NAME = "gitmastery-things"


def download(verbose: bool):
    username = get_github_username(verbose)
    remote_repo = f"{username}/{REPO_NAME}"
    remote_url = get_remote_url(remote_repo, verbose)

    os.makedirs("things")
    os.chdir("things")
    init(verbose)

    create_or_update_file(
        "fruits.txt",
        """
        apples
        bananas
        cherries
        dragon fruits
        """,
    )
    add(["fruits.txt"], verbose)
    commit("Add fruits.txt", verbose)

    append_to_file("fruits.txt", "figs")
    add(["fruits.txt"], verbose)
    commit("Insert figs into fruits.txt", verbose)

    create_or_update_file(
        "colours.txt",
        """
        a file for colours 
        """,
    )
    create_or_update_file(
        "shapes.txt",
        """
        a file for shapes 
        """,
    )

    add(["colours.txt", "shapes.txt"], verbose)
    commit("Add colours.txt, shapes.txt", verbose)

    repo_check = has_repo(REPO_NAME, False, verbose)

    if repo_check:
        delete_repo(REPO_NAME, verbose)

    create_repo(REPO_NAME, verbose)
    add_remote("origin", remote_url, verbose)

    run_command(["git", "push", "-u", "origin", "main"], verbose)

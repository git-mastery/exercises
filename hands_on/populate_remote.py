import os
import subprocess

from exercise_utils.cli import run_command
from exercise_utils.file import create_or_update_file, append_to_file
from exercise_utils.git import add, init, commit, add_remote

__requires_git__ = True
__requires_github__ = True

REPO_NAME = "gitmastery-things"


def download(verbose: bool):
    _setup_local_repository(verbose)
    _ensure_clean_repository(verbose)
    _link_repositories(verbose)


def _setup_local_repository(verbose: bool):
    _initialize_workspace()
    init(verbose)
    _create_and_commit_fruits_file(verbose)
    _update_fruits_file(verbose)
    _add_additional_files(verbose)


def _ensure_clean_repository(verbose: bool):
    repo_check = subprocess.run(
        ["gh", "repo", "view", _get_full_repo_name(verbose)],
        capture_output=True,
        text=True
    )

    if repo_check.returncode == 0:
        run_command(["gh", "repo", "delete", REPO_NAME, "--yes"], verbose)

    run_command(["gh", "repo", "create", REPO_NAME, "--public"], verbose)


def _link_repositories(verbose: bool):
    full_repo_name = _get_full_repo_name(verbose)
    add_remote("origin", f"https://github.com/{full_repo_name}", verbose)


def _initialize_workspace():
    os.makedirs("things")
    os.chdir("things")


def _create_and_commit_fruits_file(verbose: bool):
    create_or_update_file("fruits.txt", """
        apples
        bananas
        cherries
        dragon fruits
        """,
    )
    add(["fruits.txt"], verbose)


def _update_fruits_file(verbose: bool):
    append_to_file("fruits.txt", """
        figs
        """,
    )
    add(["fruits.txt"], verbose)
    commit("Insert figs into fruits.txt", verbose)


def _add_additional_files(verbose: bool):
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


def _get_full_repo_name(verbose: bool) -> str:
    username = run_command(["gh", "api", "user", "-q", ".login"], verbose).strip()
    return f"{username}/{REPO_NAME}"

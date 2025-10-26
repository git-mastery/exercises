import os
import subprocess

from exercise_utils.cli import run_command
from exercise_utils.file import create_or_update_file, append_to_file
from exercise_utils.git import add, init, commit, add_origin

__requires_git__ = True
__requires_github__ = True

REPO_NAME = "gitmastery-things"


def download(verbose: bool):
    _setup_local_repository(verbose)
    _setup_remote_repository(verbose)
    _link_repositories(verbose)


def _setup_local_repository(verbose: bool):
    _initialize_workspace()
    init(verbose)
    _create_and_commit_fruits_file(verbose)
    _update_fruits_file(verbose)
    _add_additional_files(verbose)


def _setup_remote_repository(verbose: bool):
    username = _get_github_username(verbose)
    _ensure_clean_repository(verbose)


def _link_repositories(verbose: bool):
    remote_url = _build_remote_url(verbose)
    add_origin(remote_url, verbose)


def _initialize_workspace():
    os.makedirs("things")
    os.chdir("things")


def _create_and_commit_fruits_file(verbose: bool):
    content = """
        apples
        bananas
        cherries
        dragon fruits
        """
    create_or_update_file("fruits.txt", content)
    add(["fruits.txt"], verbose)


def _update_fruits_file(verbose: bool):
    append_to_file("fruits.txt", "figs")
    add(["fruits.txt"], verbose)
    commit("Insert figs into fruits.txt", verbose)


def _add_additional_files(verbose: bool):
    create_or_update_file("colours.txt", """
        a file for colours 
        """)
    create_or_update_file("shapes.txt", """
        a file for shapes 
        """)
    add(["colours.txt", "shapes.txt"], verbose)
    commit("Add colours.txt, shapes.txt", verbose)


def _get_github_username(verbose: bool) -> str:
    return run_command(["gh", "api", "user", "-q", ".login"], verbose).strip()


def _ensure_clean_repository(verbose: bool):
    result = subprocess.run(["gh", "api", "user", "-q", ".login"], capture_output=True, text=True)

    if result.returncode == 0:
        run_command(["gh", "repo", "delete", REPO_NAME, "--yes"], verbose)

    run_command(["gh", "repo", "create", REPO_NAME, "--public"], verbose)


def _build_remote_url(verbose: bool) -> str:
    username = _get_github_username(verbose)
    return f"https://github.com/{username}/{REPO_NAME}.git"

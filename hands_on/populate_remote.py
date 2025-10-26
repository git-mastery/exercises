import os

from exercise_utils.cli import run_command, run_command_with_code
from exercise_utils.file import create_or_update_file, append_to_file
from exercise_utils.git import add, init, commit, add_remote

__requires_git__ = True
__requires_github__ = True

REPO_NAME = "gitmastery-things"


def download(verbose: bool):
    _setup_local_repository(verbose)
    _create_things_repository(verbose)
    _link_repositories(verbose)


def _setup_local_repository(verbose: bool):
    _initialize_workspace(verbose)
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


def _create_things_repository(verbose: bool):
    """Create the gitmastery-things repository, deleting any existing ones."""
    _, return_code = run_command_with_code(["gh", "repo", "view", _get_full_repo_name(verbose)], verbose)
    if return_code == 0:
        run_command(["gh", "repo", "delete", REPO_NAME, "--yes"], verbose)

    run_command(["gh", "repo", "create", REPO_NAME, "--public"], verbose)


def _link_repositories(verbose: bool):
    full_repo_name = _get_full_repo_name(verbose)
    add_remote("origin", f"https://github.com/{full_repo_name}", verbose)


def _initialize_workspace(verbose: bool):
    os.makedirs("things")
    os.chdir("things")
    init(verbose)


def _get_full_repo_name(verbose: bool) -> str:
    username = run_command(["gh", "api", "user", "-q", ".login"], verbose).strip()
    return f"{username}/{REPO_NAME}"

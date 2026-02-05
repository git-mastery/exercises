import os

from exercise_utils.file import append_to_file, create_or_update_file
from exercise_utils.git import add, add_remote, commit, init
from exercise_utils.github_cli import (
    create_repo,
    delete_repo,
    get_remote_url,
    get_github_username,
    has_repo,
)

__requires_git__ = True
__requires_github__ = True

REPO_NAME = "gitmastery-things"


def download(verbose: bool):
    _setup_local_repository(verbose)
    _create_things_repository(verbose)
    _link_repositories(verbose)


def _setup_local_repository(verbose: bool):
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

    create_or_update_file("colours.txt", "a file for colours")
    create_or_update_file("shapes.txt", "a file for shapes")
    add(["colours.txt", "shapes.txt"], verbose)
    commit("Add colours.txt, shapes.txt", verbose)


def _create_things_repository(verbose: bool):
    """Create the gitmastery-things repository, deleting any existing ones."""
    full_repo_name = _get_full_repo_name(verbose)

    if has_repo(full_repo_name, False, verbose):
        delete_repo(full_repo_name, verbose)

    create_repo(REPO_NAME, verbose)


def _link_repositories(verbose: bool):
    full_repo_name = _get_full_repo_name(verbose)
    remote_url = get_remote_url(full_repo_name, verbose)

    add_remote("origin", remote_url, verbose)


def _get_full_repo_name(verbose: bool) -> str:
    username = get_github_username(verbose)
    return f"{username}/{REPO_NAME}"

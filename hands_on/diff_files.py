import os

from exercise_utils.file import create_or_update_file, append_to_file
from exercise_utils.git import add, init, commit

__requires_git__ = True
__requires_github__ = False


def download(verbose: bool):
    os.makedirs("employees")
    os.chdir("employees")
    init(verbose)

    create_or_update_file(
        "list.txt",
        """
        Andy Bernard
        """,
    )
    os.makedirs("andy")
    create_or_update_file(
        "andy/history.txt",
        """
        Previously in Stamford branch
        """,
    )
    add(["."], verbose)
    commit("Add Andy", verbose)

    append_to_file(
        "list.txt",
        """
        Pam Beesly
        """,
    )
    add(["."], verbose)
    commit("Add Pam", verbose)

    append_to_file(
        "list.txt",
        """
        Kelly Kapoor
        """,
    )
    add(["."], verbose)
    commit("Add Kelly", verbose)

    append_to_file(
        "list.txt",
        """
        Kevin Malone
        """,
    )
    add(["."], verbose)

    append_to_file(
        "list.txt",
        """
        Jim Halpert
        """,
    )
    append_to_file(
        "andy/history.txt",
        """
        Education: Cornell
        """,
    )

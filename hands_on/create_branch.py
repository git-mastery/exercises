import os

from exercise_utils.file import create_or_update_file
from exercise_utils.git import add, commit, init

__requires_git__ = True
__requires_github__ = False


def download(verbose: bool):
    os.makedirs("sports")
    os.chdir("sports")

    init(verbose)

    create_or_update_file(
        "golf.txt",
        """
        Arnold Palmer
        Tiger Woods
        """,
    )
    add(["golf.txt"], verbose)
    commit("Add golf.txt", verbose)

    create_or_update_file(
        "tennis.txt",
        """
        Pete Sampras
        Roger Federer
        Serena Williams
        """,
    )
    add(["tennis.txt"], verbose)
    commit("Add tennis.txt", verbose)

    create_or_update_file(
        "football.txt",
        """
        Pele
        Maradona
        """,
    )
    add(["football.txt"], verbose)
    commit("Add football.txt", verbose)

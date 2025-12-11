import os

from exercise_utils.file import create_or_update_file, append_to_file
from exercise_utils.git import add, commit, init, checkout

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

    checkout("feature1", True, verbose)

    create_or_update_file(
        "boxing.txt",
        """
        Muhammad Ali
        """,
    )
    add(["boxing.txt"], verbose)
    commit("Add boxing.txt", verbose)

    append_to_file("boxing.txt", "Mike Tyson")
    add(["boxing.txt"], verbose)
    commit("Add Tyson to boxing.txt", verbose)

    checkout("main", False, verbose)
    append_to_file("tennis.txt", "Martina Navratilova")
    add(["tennis.txt"], verbose)
    commit("Add Martina to tennis.txt", verbose)

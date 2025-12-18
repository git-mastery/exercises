from exercise_utils.file import create_or_update_file
from exercise_utils.git import add, commit, checkout


def setup(verbose: bool = False):
    create_or_update_file(
        "joey.txt",
        """
        Matt LeBlanc
        """,
    )
    add(["."], verbose)
    commit("Add Joey", verbose)

    create_or_update_file(
        "phoebe.txt",
        """
        Lisa Kudrow
        """,
    )
    add(["."], verbose)
    commit("Add Phoebe", verbose)

    checkout("supporting", True, verbose)
    create_or_update_file(
        "mike.txt",
        """
        Paul Rudd
        """,
    )
    add(["."], verbose)
    commit("Add Mike", verbose)

    create_or_update_file(
        "janice.txt",
        """
        Maggie Wheeler
        """,
    )
    add(["."], verbose)
    commit("Add Janice", verbose)

    checkout("main", False, verbose)
    create_or_update_file(
        "ross.txt",
        """
        David Schwimmer
        """,
    )
    add(["."], verbose)
    commit("Add Ross", verbose)

from exercise_utils.git import (
    add,
    commit,
    checkout,
    merge,
)
from exercise_utils.file import (
    create_or_update_file,
    append_to_file,
)


def setup(verbose: bool = False):
    create_or_update_file(
        "rick.txt",
        """
        Hero
        """,
    )
    add(["."], verbose)
    commit("Add Rick", verbose)

    create_or_update_file(
        "morty.txt",
        """
        Boy
        """,
    )
    add(["."], verbose)
    commit("Add Morty", verbose)

    checkout("others", True, verbose)

    create_or_update_file(
        "birdperson.txt",
        """
        No job
        """,
    )
    add(["."], verbose)
    commit("Add Birdperson", verbose)

    append_to_file(
        "birdperson.txt",
        """
        Cyborg
        """,
    )
    add(["."], verbose)
    commit("Add Cyborg to birdperson.txt", verbose)

    create_or_update_file(
        "tammy.txt",
        """
        Spy
        """,
    )
    add(["."], verbose)
    commit("Add Tammy", verbose)

    checkout("main", False, verbose)
    merge("others", True, verbose)

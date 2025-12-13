from exercise_utils.file import append_to_file, create_or_update_file
from exercise_utils.git import add, checkout, commit, merge_with_message


def setup(verbose: bool = False):
    create_or_update_file(
        "rick.txt",
        """
        Scientist
        """,
    )
    add(["rick.txt"], verbose)
    commit("Add Rick", verbose)

    create_or_update_file(
        "morty.txt",
        """
        Boy
        """,
    )
    add(["morty.txt"], verbose)
    commit("Add morty", verbose)

    checkout("daughter", True, verbose)
    create_or_update_file(
        "beth.txt",
        """
        Vet
        """,
    )
    add(["beth.txt"], verbose)
    commit("Add Beth", verbose)

    checkout("main", False, verbose)

    checkout("son-in-law", True, verbose)
    create_or_update_file(
        "jerry.txt",
        """
        Salesman
        """,
    )
    add(["jerry.txt"], verbose)
    commit("Add Jerry", verbose)

    checkout("main", False, verbose)
    append_to_file(
        "morty.txt",
        """
        Grandson
        """,
    )
    add(["morty.txt"], verbose)
    commit("Mention Morty is grandson", verbose)

    merge_with_message("daughter", True, "Introduce Beth", verbose)
    merge_with_message("son-in-law", True, "Introduce Jerry", verbose)

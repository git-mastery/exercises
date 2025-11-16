__resources__ = {"README.md": "README.md"}

from exercise_utils.cli import run_command
from exercise_utils.file import create_or_update_file
from exercise_utils.git import add, checkout, commit, merge_with_message
from exercise_utils.gitmastery import create_start_tag


def setup(verbose: bool = False):
    create_start_tag(verbose)

    # main branch
    checkout("main", False, verbose)
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

    # daughter branch
    checkout("daughter", True, verbose)
    create_or_update_file(
        "beth.txt",
        """
        Vet
        """,
    )
    add(["beth.txt"], verbose)
    commit("Add Beth", verbose)

    # son-in-law branch
    checkout("main", False, verbose)        # switch to main first

    checkout("son-in-law", True, verbose)
    create_or_update_file(
        "jerry.txt",
        """
        Salesman
        """,
    )
    add(["jerry.txt"], verbose)
    commit("Add Herry", verbose)

    # Append morty as a grandson
    checkout("main", False, verbose)
    create_or_update_file(
        "morty.txt",
        """
        Boy
        Grandson
        """,
    )
    add(["morty.txt"], verbose)
    commit("Mention Morty is grandson", verbose)

    # Merge daughter and son-in-law to main story
    merge_with_message("daughter", False, "Introduce Beth", verbose)
    merge_with_message("son-in-law", False, "Introduce Jerry", verbose)

import os
from typing import Any

from exercise_utils.file import create_or_update_file, append_to_file
from exercise_utils.git import add, init, commit

__requires_git__ = True
__requires_github__ = False


def download(verbose: bool = False) -> None:
    """Create a sandbox repository for the hp-view-graph hands-on.

    The sandbox layout matches the instructions provided in the exercise.
    """
    os.makedirs("things", exist_ok=True)
    os.chdir("things")

    # Initialize repository
    init(verbose)

    # Initial fruits file and commit
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

    # Append figs, stage and commit
    append_to_file("fruits.txt", "figs\n")
    add(["fruits.txt"], verbose)
    commit("Insert figs into fruits.txt", verbose)

    # Add colours and shapes together and commit
    create_or_update_file("colours.txt", "a file for colours\n")
    create_or_update_file("shapes.txt", "a file for shapes\n")
    add(["colours.txt", "shapes.txt"], verbose)
    commit("Add colours.txt, shapes.txt", verbose)

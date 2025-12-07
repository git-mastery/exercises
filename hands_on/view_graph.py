import os

from exercise_utils.file import create_or_update_file, append_to_file
from exercise_utils.git import add, init, commit

__requires_git__ = True
__requires_github__ = False


def download(verbose: bool = False) -> None:
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

    append_to_file("fruits.txt", "figs\n")
    add(["fruits.txt"], verbose)
    commit("Insert figs into fruits.txt", verbose)

    create_or_update_file("colours.txt", "a file for colours\n")
    create_or_update_file("shapes.txt", "a file for shapes\n")
    add(["colours.txt", "shapes.txt"], verbose)
    commit("Add colours.txt, shapes.txt", verbose)

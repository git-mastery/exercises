import os

from exercise_utils.file import append_to_file
from exercise_utils.git import add, commit, init

__requires_git__ = True
__requires_github__ = False


def download(verbose: bool):
    os.makedirs("things")
    os.chdir("things")

    init(verbose)

    append_to_file(
        "fruits.txt",
        "apples\nbananas\ncherries\ndragon fruits\n"
    )

    add(["fruits.txt"], verbose)
    commit("Add fruits.txt", verbose)

    append_to_file(
        "fruits.txt",
        "figs\n"
    )

    add(["fruits.txt"], verbose)
    commit("Insert figs into fruits.txt", verbose)

    append_to_file(
        "colours.txt",
        "a file for colours\n"
    )

    append_to_file(
        "shapes.txt",
        "a file for shapes\n"
    )

    add(["colours.txt", "shapes.txt"], verbose)
    commit("Add colours.txt and shapes.txt", verbose)
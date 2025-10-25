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
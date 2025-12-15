import os

from exercise_utils.file import create_or_update_file, append_to_file
from exercise_utils.git import add, commit, init, checkout

__requires_git__ = True
__requires_github__ = False


def download(verbose: bool):
    os.makedirs("nouns")
    os.chdir("nouns")

    init(verbose)

    create_or_update_file(
        "colours.txt",
        """
        blue
        """,
    )
    add(["colours.txt"], verbose)
    commit("Add colours.txt", verbose)

    checkout("fix1", True, verbose)
    append_to_file(
        "colours.txt",
        """
      green
      red
      white
      """,
    )
    add(["colours.txt"], verbose)
    commit("Add green, red, white", verbose)

    checkout("main", False, verbose)
    append_to_file(
        "colours.txt",
        """
      black
      red
      white
      """,
    )
    add(["colours.txt"], verbose)
    commit("Add black, red, white", verbose)

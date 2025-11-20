import os

from exercise_utils.file import create_or_update_file, append_to_file
from exercise_utils.git import add, init, commit, tag

__requires_git__ = True
__requires_github__ = False


def download(verbose: bool):
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
    append_to_file(
        "fruits.txt",
        """
                   elderberries
                   figs
                   """,
    )
    add(["fruits.txt"], verbose)
    commit("Add elderberries and figs to fruits.txt", verbose)

    create_or_update_file(
        "colours.txt",
        "a file for colours\n",
    )
    create_or_update_file(
        "shapes.txt",
        "a file for shapes\n",
    )
    add(["colours.txt", "shapes.txt"], verbose)
    commit("Add colours.txt, shapes.txt", verbose)

    tag("v0.9", verbose)

    # Replace the whole contents of fruits.txt
    create_or_update_file(
        "fruits.txt",
        """
                   apples, apricots
                   bananas
                   blueberries
                   cherries
                   dragon fruits
                   figs
                   """,
    )
    add(["fruits.txt"], verbose)
    commit("Update fruits list", verbose)

    append_to_file(
        "colours.txt",
        """
                    blue
                    red
                    white
                    """,
    )
    add(["colours.txt"], verbose)
    commit("colours.txt: Add some colours", verbose)

    append_to_file(
        "shapes.txt",
        """
                   circle
                   oval
                   rectangle
                   square
                   """,
    )
    add(["shapes.txt"], verbose)
    commit("shapes.txt: Add some shapes", verbose)

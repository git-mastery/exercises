import os

from exercise_utils.file import append_to_file, create_or_update_file
from exercise_utils.git import add, commit, init, tag

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
    commit("Add elderberries and figs into fruits.txt", verbose)

    create_or_update_file("colours.txt", "a file for colours\n")
    create_or_update_file("shapes.txt", "a file for shapes\n")
    add(["colours.txt", "shapes.txt"], verbose)
    commit("Add colours.txt, shapes.txt", verbose)
    tag("0.9", verbose)

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

    append_to_file("colours.txt", "bad colour\n")
    add(["colours.txt"], verbose)
    commit("Incorrectly update colours.txt", verbose)

    append_to_file("shapes.txt", "bad shape\n")
    add(["shapes.txt"], verbose)
    commit("Incorrectly update shapes.txt", verbose)

    append_to_file("fruits.txt", "bad fruit\n")
    add(["fruits.txt"], verbose)
    commit("Incorrectly update fruits.txt", verbose)

    create_or_update_file("incorrect.txt", "bad line\n")
    add(["incorrect.txt"], verbose)
    commit("Add incorrect.txt", verbose)

    append_to_file("colours.txt", "another bad colour\n")
    add(["colours.txt"], verbose)

    append_to_file("shapes.txt", "another bad shape\n")

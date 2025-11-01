import os

from exercise_utils.file import append_to_file, create_or_update_file
from exercise_utils.git import add, commit, init

__requires_git__ = True
__requires_github__ = False


def download(verbose: bool):
    os.makedirs("things")
    os.chdir("things")

    init(verbose)

    create_or_update_file(
        "fruits.txt",
        "apples\nbananas\ncherries\ndragon fruits\n",
    )

    add(["fruits.txt"], verbose)
    commit("Add fruits.txt", verbose)

    append_to_file("fruits.txt", "elderberries\nfigs\n")
    add(["fruits.txt"], verbose)
    commit("Add elderberries and figs into fruits.txt", verbose)

    create_or_update_file("colours.txt", "a file for colours\n")
    create_or_update_file("shapes.txt", "a file for shapes\n")
    add(["colours.txt", "shapes.txt"], verbose)
    commit("Add colours.txt, shapes.txt", verbose)

    create_or_update_file(
        "fruits.txt",
        "apples, apricots\nbananas\nblueberries\ncherries\ndragon fruits\nfigs\n",
    )
    add(["fruits.txt"], verbose)
    commit("Update fruits list", verbose)
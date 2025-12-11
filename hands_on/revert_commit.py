import os

from exercise_utils.file import create_or_update_file
from exercise_utils.git import add, commit, init

__requires_git__ = True
__requires_github__ = False


def download(verbose: bool):
    os.makedirs("pioneers")
    os.chdir("pioneers")
    init(verbose)

    create_or_update_file("neo.txt", "hacked the matrix\n")
    add(["neo.txt"], verbose)
    commit("Add Neo", verbose)

    create_or_update_file("alan-turing.txt", "father of theoretical computing\n")
    add(["alan-turing.txt"], verbose)
    commit("Add Turing", verbose)

    create_or_update_file("grace-hopper.txt", "created COBOL, compiler pioneer\n")
    add(["grace-hopper.txt"], verbose)
    commit("Add Hopper", verbose)

import time
import os

from exercise_utils.file import create_or_update_file
from exercise_utils.git import add, commit, checkout, init, merge_with_message

__requires_git__ = True
__requires_github__ = False


def download(verbose: bool):
    os.makedirs("samplerepo-books-2")
    os.chdir("samplerepo-books-2")

    init(verbose)

    create_or_update_file("horror.txt", "Horror Stories")
    add(["."], verbose)
    commit("Add horror.txt", verbose)

    checkout("textbooks", True, verbose)
    create_or_update_file("textbooks.txt", "Textbooks")
    add(["."], verbose)
    commit("Add textbooks.txt", verbose)

    checkout("main", False, verbose)

    checkout("fantasy", True, verbose)
    create_or_update_file("fantasy.txt", "Fantasy Books")
    add(["."], verbose)
    commit("Add fantasy.txt", verbose)

    checkout("main", False, verbose)

    # Sleep to ensure that the commit timestamps are different to ensure correct git revision graph in git log
    time.sleep(1)

    merge_with_message("textbooks", False, "Merge branch textbooks", verbose)

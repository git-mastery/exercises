import os

from exercise_utils.cli import run_command
from exercise_utils.gitmastery import create_start_tag
from exercise_utils.git import add, init, commit
from exercise_utils.file import create_or_update_file, append_to_file

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
    append_to_file("fruits.txt",
                   """
                   elderberries
                   figs
                   """
    )
    add(["fruits.txt"], verbose)
    commit("Add elderberries and figs to fruits.txt", verbose)

    

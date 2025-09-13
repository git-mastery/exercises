import os

from exercise_utils.cli import run_command
from exercise_utils.file import append_to_file, create_or_update_file
from exercise_utils.git import add, init

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
        """,
    )
    add(["fruits.txt"], verbose)
    run_command(["git", "add", "fruits.txt"], verbose)
    append_to_file("fruits.txt", "dragon fruits")

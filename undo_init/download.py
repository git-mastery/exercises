import os
from exercise_utils.file import create_or_update_file
from exercise_utils.git import init


def setup(verbose: bool = False):
    create_or_update_file(
        "todo.txt",
        """
        My tasks
        """,
    )

    os.makedirs("private")
    os.chdir("private")
    create_or_update_file(
        "contacts.txt",
        """
        My contacts
        """,
    )

    os.chdir("..")
    init(verbose)

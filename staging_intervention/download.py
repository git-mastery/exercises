from exercise_utils.file import create_or_update_file
from exercise_utils.git import add


def setup(verbose: bool = False):
    crew = [
        "josh.txt",
        "adam.txt",
        "mary.txt",
        "jane.txt",
        "charlie.txt",
        "kristen.txt",
        "alice.txt",
        "john.txt",
    ]
    for member in crew:
        create_or_update_file(member)

    add(["."], verbose)

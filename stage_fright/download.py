from exercise_utils.file import create_or_update_file
from exercise_utils.git import add
from exercise_utils.gitmastery import create_start_tag


def setup(verbose: bool = False):
    names = ["alice", "bob", "joe", "jim", "carrey"]
    for name in names:
        create_or_update_file(f"{name}.txt", "a")
    add(["jim.txt", "carrey.txt"], verbose)
    create_start_tag(verbose)

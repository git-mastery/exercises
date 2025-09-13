import os
import stat

from exercise_utils.file import append_to_file, create_or_update_file
from exercise_utils.git import add, commit
from exercise_utils.gitmastery import create_start_tag


def setup(verbose: bool = False):
    for i in range(1, 101):
        if i == 77:
            continue
        create_or_update_file(f"file{i}.txt")

    add([f"file{i}.txt" for i in range(1, 101) if i != 77], verbose)
    commit("Change 1", verbose)

    append_to_file("file14.txt", "This is a change")

    create_or_update_file("file77.txt")
    for i in range(1, 101):
        os.chmod(f"file{i}.txt", stat.S_IREAD)

    create_start_tag(verbose)

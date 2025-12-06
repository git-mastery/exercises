import os
from exercise_utils.file import create_or_update_file
from exercise_utils.git import init

__requires_git__ = True
__requires_github__ = False


def download(verbose: bool):
    os.makedirs("stuff", exist_ok=True)
    os.chdir("stuff")
    init(verbose)

    create_or_update_file("keep.txt", "good stuff")
    create_or_update_file("temp.txt", "temp stuff")
    create_or_update_file("file1.tmp", "more temp stuff")
    create_or_update_file("file2.tmp", "even more temp stuff")

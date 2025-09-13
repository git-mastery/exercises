from exercise_utils.file import create_or_update_file
from exercise_utils.git import add, checkout, commit, merge
from exercise_utils.gitmastery import create_start_tag

__resources__ = {"script.py": "script.py"}


def setup(verbose: bool = False):
    create_start_tag(verbose)

    checkout("john", True, verbose)
    create_or_update_file("script.py", "print('Hello World!')")
    add(["script.py"], verbose)
    commit("Hello world", verbose)

    checkout("main", False, verbose)
    checkout("josh", True, verbose)
    create_or_update_file("script.py", "print('Hello Everyone!')")
    add(["script.py"], verbose)
    commit("Hello everyone", verbose)

    checkout("main", False, verbose)
    merge("john", True, verbose)

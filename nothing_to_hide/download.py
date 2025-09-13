from exercise_utils.file import create_or_update_file
from exercise_utils.git import add, commit
from exercise_utils.gitmastery import create_start_tag

__resources__ = {"hidden.png": "res/hidden.png"}


def setup(verbose: bool = False):
    create_or_update_file("src/script.py", 'print("hello world!")')
    create_or_update_file(
        "src/.env",
        """
        KEY=secretshhh
        KEY=secretshhh
        """,
    )
    create_or_update_file(
        "sensitive/names.txt",
        """
        John
        Alice
        Bob
        Michael
        """,
    )
    for i in range(1, 6):
        create_or_update_file(f"sensitive/sensitive_{i}.txt")

    create_or_update_file(
        ".gitignore",
        """
        sensitive/*
        res/hidden.png
        src/.env
        !sensitive/names.txt
        """,
    )
    add([".gitignore"], verbose)
    commit("Add files", verbose)

    create_start_tag(verbose)

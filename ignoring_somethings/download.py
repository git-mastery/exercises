import os

from exercise_utils.file import create_or_update_file
from exercise_utils.gitmastery import create_start_tag

__resources__ = {".gitignore": ".gitignore"}


def setup(verbose: bool = False):
    # Running these before since we want to generate the new files after to avoid
    # committing them
    create_start_tag(verbose)

    os.makedirs("many", exist_ok=True)
    for i in range(1, 101):
        create_or_update_file(f"many/file{i}.txt", str(i))

    create_or_update_file("ignore_me.txt", "You should not even see me!")
    create_or_update_file("why_am_i_hidden.txt", "Why am I getting hidden??")
    create_or_update_file(
        "this/is/very/nested/find_me.txt", "You should have been able to find me"
    )
    create_or_update_file("this/is/very/nested/runaway.txt", "Oh no")

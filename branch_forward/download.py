from exercise_utils.file import append_to_file, create_or_update_file
from exercise_utils.git import add, checkout, commit


def setup(verbose: bool = False):
    create_or_update_file(
        "story.txt",
        """
        Harry was single.
        """,
    )
    add(["story.txt"], verbose)
    commit("Introduce Harry", verbose)

    append_to_file(
        "story.txt",
        """
        Harry did not have a family.
        """,
    )
    add(["story.txt"], verbose)
    commit("Add about family", verbose)

    checkout("with-ginny", True, verbose)
    append_to_file(
        "story.txt",
        """
        Then he met Ginny.
        """,
    )
    add(["story.txt"], verbose)
    commit("Add about Ginny", verbose)

    checkout("main", False, verbose)
    create_or_update_file(
        "cast.txt",
        """
        Harry
        """,
    )
    add(["cast.txt"], verbose)
    commit("Add cast.txt", verbose)

    checkout("with-sally", True, verbose)
    append_to_file(
        "story.txt",
        """
        Then he met Sally
        """,
    )
    add(["story.txt"], verbose)
    commit("Mention Sally", verbose)

    checkout("with-ginny", False, verbose)
    append_to_file(
        "story.txt",
        """
        Ginny was single too
        """,
    )
    add(["story.txt"], verbose)
    commit("Mention Ginny is single", verbose)

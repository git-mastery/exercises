from exercise_utils.file import create_or_update_file, append_to_file
from exercise_utils.git import add, commit


def setup(verbose: bool = False):
    create_or_update_file(
        "story.txt",
        """
        It was a dark and stormy night.
        """,
    )
    add(["story.txt"], verbose)
    commit("Describe night", verbose)

    append_to_file(
        "story.txt",
        """
        I was alone in my room.
        """,
    )
    add(["story.txt"], verbose)
    commit("Describe location", verbose)

    append_to_file(
        "story.txt",
        """
        I heard a strange noise.
        """,
    )
    add(["story.txt"], verbose)
    commit("Mention noise", verbose)

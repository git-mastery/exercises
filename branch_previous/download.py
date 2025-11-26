from exercise_utils.file import create_or_update_file, append_to_file
from exercise_utils.git import add, commit
from exercise_utils.gitmastery import create_start_tag

__resources__ = {"README.md": "README.md"}


def setup(verbose: bool = False):
    # First commit: Describe night
    create_or_update_file(
        "story.txt", 
        "It was a dark and stormy night.\n"
    )
    add(["story.txt"], verbose)
    commit("Describe night", verbose)

    # Second commit: Describe location
    append_to_file(
        "story.txt", 
        "It was a dark and stormy night.\nI was alone in my room.\n"
    )
    add(["story.txt"], verbose)
    commit("Describe location", verbose)

    # Third commit: Mention noise
    create_or_update_file(
        "story.txt",
        "It was a dark and stormy night.\nI was alone in my room.\nI heard a strange noise.\n",
    )
    add(["story.txt"], verbose)
    commit("Mention noise", verbose)


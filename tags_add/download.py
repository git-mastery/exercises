from exercise_utils.file import create_or_update_file
from exercise_utils.git import add, commit
from exercise_utils.gitmastery import create_start_tag

__resources__ = []

def setup(verbose: bool = False):
    create_or_update_file("README.md", "# T4L2: Add a tag\n")
    add(["README.md"], verbose)
    commit("chore: init README", verbose)

    create_or_update_file("main.txt", "v1 content\n")
    add(["main.txt"], verbose)
    commit("feat: initial content", verbose)

    create_start_tag(verbose)

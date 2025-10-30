import os
from exercise_utils.file import create_or_update_file, append_to_file
from exercise_utils.git import init, add, commit

__requires_git__ = True
__requires_github__ = False

def download(verbose: bool):
    os.makedirs("sandbox", exist_ok=True)
    os.chdir("sandbox")
    init(verbose)

    create_or_update_file("README.md", "# Ignore File Hands-on\n")
    add(["README.md"], verbose)
    commit("chore: init README", verbose)

    create_or_update_file(".gitignore", "logs/\n*.tmp\n")
    add([".gitignore"], verbose)
    commit("chore: add .gitignore for logs/ and *.tmp", verbose)

    create_or_update_file("notes.txt", "keep me tracked\n")
    add(["notes.txt"], verbose)
    commit("feat: add tracked notes.txt", verbose)

    os.makedirs("logs", exist_ok=True)
    create_or_update_file("logs/run.log", "this should be ignored\n")
    create_or_update_file("temp.tmp", "also ignored by pattern\n")

    append_to_file("notes.txt", "new line not committed yet\n")

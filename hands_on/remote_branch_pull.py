import os

from exercise_utils.file import append_to_file
from exercise_utils.git import add, checkout, clone_repo_with_git, commit, push
from exercise_utils.github_cli import (
    get_github_username,
    fork_repo,
    has_repo,
    delete_repo,
)

__requires_git__ = True
__requires_github__ = True


TARGET_REPO = "git-mastery/samplerepo-company"
FORK_NAME = "gitmastery-samplerepo-company"
LOCAL_DIR = "samplerepo-company"


def download(verbose: bool):
    username = get_github_username(verbose)
    full_repo_name = f"{username}/{FORK_NAME}"

    if has_repo(full_repo_name, True, verbose):
        delete_repo(full_repo_name, verbose)

    fork_repo(TARGET_REPO, FORK_NAME, verbose, False)
    clone_repo_with_git(f"https://github.com/{full_repo_name}", verbose, LOCAL_DIR)

    os.chdir(LOCAL_DIR)

    checkout("hiring", True, verbose)
    append_to_file("employees.txt", "Receptionist: Pam\n")
    add(["employees.txt"], verbose)
    commit("Add Pam to employees.txt", verbose)

    push("origin", "hiring", verbose)

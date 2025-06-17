import os
from typing import List

from git_autograder import GitAutograderOutput, GitAutograderRepo, GitAutograderStatus

MISSING_COMMITS = "You have not made any commits yet!"
STILL_IGNORING_FILE_22 = "You are still ignoring many/file22.txt."
STILL_HIDING = (
    "You are still ignoring why_am_i_hidden.txt. Find where the file is and fix that."
)
NOT_IGNORING_IGNORE_ME = "You are not ignoring ignore_me.txt"
NOT_IGNORING_RUNAWAY = (
    "You are not ignoring runaway.txt. Find where the file is and fix that."
)
NOT_PATTERN_MATCHING_RUNAWAY = (
    "You should be using ** to match all subfolders to ignore runaway.txt."
)


def verify(repo: GitAutograderRepo) -> GitAutograderOutput:
    main_branch = repo.branches.branch("main")

    if len(main_branch.user_commits) == 0:
        raise repo.wrong_answer([MISSING_COMMITS])

    main_branch.latest_commit.checkout()

    # Read the file and parse it
    with open(os.path.join(repo.repo_path, ".gitignore"), "r") as gitignore_file:
        lines = [
            line.strip() for line in gitignore_file.readlines() if line.strip() != ""
        ]

    comments: List[str] = []
    if "!many/file22.txt" not in lines:
        comments.append(STILL_IGNORING_FILE_22)

    if "why_am_i_hidden.txt" in lines:
        comments.append(STILL_HIDING)

    if "ignore_me.txt" not in lines:
        comments.append(NOT_IGNORING_IGNORE_ME)

    if "this/is/very/nested/runaway.txt" in lines:
        comments.append(NOT_PATTERN_MATCHING_RUNAWAY)
    elif "this/**/runaway.txt" not in lines:
        comments.append(NOT_IGNORING_RUNAWAY)

    main_branch.checkout()

    if comments:
        raise repo.wrong_answer(comments)

    return repo.to_output(
        ["Great work using .gitignore!"], status=GitAutograderStatus.SUCCESSFUL
    )

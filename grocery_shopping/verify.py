from typing import List

from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)
from git_autograder.diff import GitAutograderDiffHelper

EMPTY_COMMITS = "All commits are empty."
NO_DIFF = "There are no changes made to shopping-list.txt."
NO_ADD = "There are no new grocery list items added to the shopping list."
NO_REMOVE = "There are no grocery list items removed from the shopping list."
WRONG_FILE = "You haven't edited shopping-list.txt."


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    comments: List[str] = []

    main_branch = exercise.repo.branches.branch("main")

    # Verify that not all commits are empty
    if not main_branch.has_non_empty_commits():
        raise exercise.wrong_answer([EMPTY_COMMITS])

    # Check if they edited the shopping-list.md at least once
    if not main_branch.has_edited_file("shopping-list.txt"):
        raise exercise.wrong_answer([WRONG_FILE])

    # Verify if the final state of the file has additions and removals
    file_diff = GitAutograderDiffHelper.get_file_diff(
        main_branch.start_commit, main_branch.latest_commit, "shopping-list.txt"
    )
    if file_diff is None:
        raise exercise.wrong_answer([NO_DIFF])

    if not file_diff[0].has_added_line():
        comments.append(NO_ADD)

    if not file_diff[0].has_deleted_line():
        comments.append(NO_REMOVE)

    if comments:
        raise exercise.wrong_answer(comments)

    return exercise.to_output(
        [
            "Great work! You have successfully used `git add` and `git commit` to modify the shopping list! Keep it up!"
        ],
        GitAutograderStatus.SUCCESSFUL,
    )

from typing import List

from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)

EMPTY_COMMITS = "All commits are empty."
NO_DIFF = "There are no changes made to shopping-list.txt."
NO_ADD = "There are no new grocery list items added to the shopping list."
NO_REMOVE = "There are no grocery list items removed from the shopping list."
WRONG_FILE = "You haven't edited shopping-list.txt."

ORIGINAL_SHOPPING_LIST = {"Milk", "Eggs", "Bread", "Apples", "Ham"}


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    comments: List[str] = []

    main_branch = exercise.repo.branches.branch("main")

    # Verify that not all commits are empty
    if not main_branch.has_non_empty_commits():
        raise exercise.wrong_answer([EMPTY_COMMITS])

    # Check if they edited the shopping-list.md at least once
    if not main_branch.has_edited_file("shopping-list.txt"):
        raise exercise.wrong_answer([WRONG_FILE])

    shopping_list_blob = (
        main_branch.latest_user_commit.commit.tree / "shopping-list.txt"
    )
    current_shopping_list = {
        line[2:]
        for line in shopping_list_blob.data_stream.read().decode().split("\n")
        if line.startswith("- ")
    }

    added_items = current_shopping_list.difference(ORIGINAL_SHOPPING_LIST)
    deleted_items = ORIGINAL_SHOPPING_LIST.difference(current_shopping_list)

    if not added_items:
        comments.append(NO_ADD)

    if not deleted_items:
        comments.append(NO_REMOVE)

    if comments:
        raise exercise.wrong_answer(comments)

    return exercise.to_output(
        [
            "Great work! You have successfully used `git add` and `git commit` to modify the shopping list! Keep it up!"
        ],
        GitAutograderStatus.SUCCESSFUL,
    )

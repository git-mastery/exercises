import os
from typing import List

from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)

NO_ADD = "There are no new grocery list items added to the shopping list."
NO_REMOVE = "There are no grocery list items removed from the shopping list."
SHOPPING_LIST_FILE_MISSING = "The shopping-list.txt file should not be deleted."
ADD_NOT_COMMITTED = (
    "New grocery list items added to shopping-list.txt are not committed."
)
REMOVE_NOT_COMMITTED = (
    "Grocery list items removed from shopping-list.txt are not committed."
)

ORIGINAL_SHOPPING_LIST = {"Milk", "Eggs", "Bread", "Apples", "Ham"}


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    comments: List[str] = []
    repo_root = exercise.exercise_path
    repo_folder = exercise.config.exercise_repo.repo_name
    work_dir = os.path.join(repo_root, repo_folder)

    shopping_list_file_path = os.path.join(work_dir, "shopping-list.txt")
    if not os.path.exists(shopping_list_file_path):
        raise exercise.wrong_answer([SHOPPING_LIST_FILE_MISSING])

    with open(shopping_list_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    current_shopping_list = {
        line[2:].strip() for line in content.splitlines() if line.startswith("- ")
    }

    added_items = current_shopping_list.difference(ORIGINAL_SHOPPING_LIST)
    deleted_items = ORIGINAL_SHOPPING_LIST.difference(current_shopping_list)

    if not added_items:
        comments.append(NO_ADD)

    if not deleted_items:
        comments.append(NO_REMOVE)

    if comments:
        raise exercise.wrong_answer(comments)

    main_branch = exercise.repo.branches.branch("main")

    if not main_branch.user_commits:
        raise exercise.wrong_answer([ADD_NOT_COMMITTED, REMOVE_NOT_COMMITTED])

    shopping_list_blob = (
        main_branch.latest_user_commit.commit.tree / "shopping-list.txt"
    )
    current_shopping_list = {
        line[2:].strip()
        for line in shopping_list_blob.data_stream.read().decode().split("\n")
        if line.startswith("- ")
    }

    added_items = current_shopping_list.difference(ORIGINAL_SHOPPING_LIST)
    deleted_items = ORIGINAL_SHOPPING_LIST.difference(current_shopping_list)

    if not added_items:
        comments.append(ADD_NOT_COMMITTED)

    if not deleted_items:
        comments.append(REMOVE_NOT_COMMITTED)

    if comments:
        raise exercise.wrong_answer(comments)

    return exercise.to_output(
        [
            "Great work! You have successfully used `git add` and `git commit` to modify the shopping list! Keep it up!"
        ],
        GitAutograderStatus.SUCCESSFUL,
    )

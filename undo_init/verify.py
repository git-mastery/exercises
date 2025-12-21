import os
from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

INIT_NOT_UNDONE = "The init operation is not undone."
TODO_FILE_MISSING = "The todo.txt should not be deleted."
CONTACTS_FILE_MISSING = "The contacts.txt should not be deleted."
PRIVATE_FOLDER_MISSING = "The private folder should not be deleted."
SUCCESS_MESSAGE = "You have successfully undone the init operation!"


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    repo_root = exercise.exercise_path
    repo_folder = exercise.config.exercise_repo.repo_name
    work_dir = os.path.join(repo_root, repo_folder)
    comments = []

    dot_git_dir_path = os.path.join(work_dir, ".git")
    if os.path.exists(dot_git_dir_path):
        comments.append(INIT_NOT_UNDONE)

    todo_file_path = os.path.join(work_dir, "todo.txt")
    if not os.path.exists(todo_file_path):
        comments.append(TODO_FILE_MISSING)

    private_dir_path = os.path.join(work_dir, "private")
    if not os.path.exists(private_dir_path):
        comments.append(PRIVATE_FOLDER_MISSING)

    contacts_file_path = os.path.join(private_dir_path, "contacts.txt")
    if not os.path.exists(contacts_file_path):
        comments.append(CONTACTS_FILE_MISSING)

    if comments:
        raise exercise.wrong_answer(comments)

    return exercise.to_output([SUCCESS_MESSAGE], GitAutograderStatus.SUCCESSFUL)

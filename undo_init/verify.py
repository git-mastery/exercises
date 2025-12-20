import os
from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

INIT_NOT_UNDONE = "The init operation is not undone."
TODO_FILE_MISSING = "The todo.txt has been deleted."
CONTACTS_FILE_MISSING = "The contacts.txt has been deleted."
PRIVATE_FOLDER_MISSING = "The private folder has been deleted."
SUCCESS_MESSAGE = "You have successfully undone the init operation!"

def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    repo_root = exercise.exercise_path
    repo_folder = exercise.config.exercise_repo.repo_name
    work_dir = os.path.join(repo_root, repo_folder)

    dot_git_dir_path = os.path.join(work_dir, ".git")
    if os.path.exists(dot_git_dir_path):
        raise exercise.wrong_answer([INIT_NOT_UNDONE])
    
    todo_file_path = os.path.join(work_dir, "todo.txt")
    if not os.path.exists(todo_file_path):
        raise exercise.wrong_answer([TODO_FILE_MISSING])
    
    private_dir_path = os.path.join(work_dir, "private")
    if not os.path.exists(private_dir_path):
        raise exercise.wrong_answer([PRIVATE_FOLDER_MISSING])

    contacts_file_path = os.path.join(private_dir_path, "contacts.txt")
    if not os.path.exists(contacts_file_path):
        raise exercise.wrong_answer([CONTACTS_FILE_MISSING])

    return exercise.to_output([SUCCESS_MESSAGE], GitAutograderStatus.SUCCESSFUL)

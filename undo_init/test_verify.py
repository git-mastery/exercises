from unittest import mock

from exercise_utils.test import GitAutograderTestLoader, assert_output
from git_autograder import GitAutograderStatus

from .verify import (
    CONTACTS_FILE_MISSING,
    INIT_NOT_UNDONE,
    PRIVATE_FOLDER_MISSING,
    TODO_FILE_MISSING,
    verify,
)

REPOSITORY_NAME = "undo-init"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


def test_base():
    # We patch the ExerciseRepoConfig to return "ignore" instead of "local"
    with (
        mock.patch(
            "git_autograder.exercise_config.ExerciseConfig.ExerciseRepoConfig"
        ) as mock_config,
        loader.start() as (test, rs),
    ):
        # Configure the mock to return "ignore" when the loader accesses it
        instance = mock_config.return_value
        instance.repo_type = "ignore"
        instance.repo_name = "repo"  # Match the loader's hardcoded name
        instance.init = False

        rs.git.commit(message="Set initial state", allow_empty=True)
        rs.files.create_or_update("todo.txt", "My tasks")
        rs.files.create_or_update("private/contacts.txt", "My contacts")
        rs.files.delete(".git/")

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_init_not_undone():
    with loader.start() as (test, rs):
        rs.git.commit(message="Set initial state", allow_empty=True)
        rs.files.create_or_update("todo.txt", "My tasks")
        rs.files.create_or_update("private/contacts.txt", "My contacts")

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [INIT_NOT_UNDONE])


def test_todo_file_missing():
    with (
        mock.patch(
            "git_autograder.exercise_config.ExerciseConfig.ExerciseRepoConfig"
        ) as mock_config,
        loader.start() as (test, rs),
    ):
        instance = mock_config.return_value
        instance.repo_type = "ignore"
        instance.repo_name = "repo"
        instance.init = False

        rs.git.commit(message="Set initial state", allow_empty=True)
        rs.files.create_or_update("private/contacts.txt", "My contacts")
        rs.files.delete(".git/")

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [TODO_FILE_MISSING])


def test_private_dir_missing():
    with (
        mock.patch(
            "git_autograder.exercise_config.ExerciseConfig.ExerciseRepoConfig"
        ) as mock_config,
        loader.start() as (test, rs),
    ):
        instance = mock_config.return_value
        instance.repo_type = "ignore"
        instance.repo_name = "repo"
        instance.init = False

        rs.git.commit(message="Set initial state", allow_empty=True)
        rs.files.create_or_update("todo.txt", "My tasks")
        rs.files.delete(".git/")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [PRIVATE_FOLDER_MISSING, CONTACTS_FILE_MISSING],
        )


def test_contacts_file_missing():
    with (
        mock.patch(
            "git_autograder.exercise_config.ExerciseConfig.ExerciseRepoConfig"
        ) as mock_config,
        loader.start() as (test, rs),
    ):
        instance = mock_config.return_value
        instance.repo_type = "ignore"
        instance.repo_name = "repo"
        instance.init = False

        rs.git.commit(message="Set initial state", allow_empty=True)
        rs.files.create_or_update("todo.txt", "My tasks")
        rs.files.create_or_update("private/contacts.txt", "My contacts")
        rs.files.delete("private/contacts.txt")
        rs.files.delete(".git/")

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [CONTACTS_FILE_MISSING])

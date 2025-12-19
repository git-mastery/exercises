from unittest import mock
from git_autograder import GitAutograderStatus, GitAutograderTestLoader, assert_output

from ..verify import (
    INIT_NOT_UNDONE, 
    TODO_FILE_MISSING,
    CONTACTS_FILE_MISSING,
    PRIVATE_FOLDER_MISSING, 
    verify
)

REPOSITORY_NAME = "undo-init"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_base():

    # We patch the ExerciseRepoConfig to return "ignore" instead of "local"
    with mock.patch("git_autograder.exercise_config.ExerciseConfig.ExerciseRepoConfig") as mock_config:
        # Configure the mock to return "ignore" when the loader accesses it
        instance = mock_config.return_value
        instance.repo_type = "ignore"
        instance.repo_name = "repo" # Match the loader's hardcoded name
        instance.init = False

        with loader.load("specs/base.yml") as output:
            assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_init_not_undone():

    with loader.load("specs/init_not_undone.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [INIT_NOT_UNDONE])


def test_todo_file_missing():

    with mock.patch("git_autograder.exercise_config.ExerciseConfig.ExerciseRepoConfig") as mock_config:
        instance = mock_config.return_value
        instance.repo_type = "ignore"
        instance.repo_name = "repo"
        instance.init = False

        with loader.load("specs/todo_file_missing.yml") as output:
            assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [TODO_FILE_MISSING])


def test_private_dir_missing():

    with mock.patch("git_autograder.exercise_config.ExerciseConfig.ExerciseRepoConfig") as mock_config:
        instance = mock_config.return_value
        instance.repo_type = "ignore"
        instance.repo_name = "repo"
        instance.init = False

        with loader.load("specs/private_dir_missing.yml") as output:
            assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [PRIVATE_FOLDER_MISSING])


def test_contacts_file_missing():

    with mock.patch("git_autograder.exercise_config.ExerciseConfig.ExerciseRepoConfig") as mock_config:
        instance = mock_config.return_value
        instance.repo_type = "ignore"
        instance.repo_name = "repo"
        instance.init = False

        with loader.load("specs/contacts_file_missing.yml") as output:
            assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [CONTACTS_FILE_MISSING])

from sensors_reset.verify import (
    CONTAINS_TASK_ONE_COMMITS,
    CONTAINS_TASK_TWO_COMMIT,
    CONTAINS_TASK_THREE_COMMIT,
    WRONG_FILES_IN_STAGING_AREA,
    WRONG_FILES_IN_WORKING_DIRECTORY,
    WRONG_HEAD_COMMIT,
)
from git_autograder.status import GitAutograderStatus
from git_autograder.test_utils import assert_output
from git_autograder import GitAutograderTestLoader

from ..verify import verify

REPOSITORY_NAME = "sensors-reset"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_base():
    with loader.load("specs/base.yml", "start") as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_no_changes():
    with loader.load("specs/no_changes.yml", "start") as output:
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [CONTAINS_TASK_ONE_COMMITS]
        )


def test_incomplete_task_two_reset():
    with loader.load("specs/incomplete_task_two_reset.yml", "start") as output:
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [CONTAINS_TASK_TWO_COMMIT]
        )


def test_incomplete_task_three_reset():
    with loader.load("specs/incomplete_task_three_reset.yml", "start") as output:
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [CONTAINS_TASK_THREE_COMMIT]
        )


def test_wrong_task_two_reset():
    with loader.load("specs/wrong_task_two_reset.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [WRONG_FILES_IN_WORKING_DIRECTORY],
        )


def test_wrong_task_three_reset():
    with loader.load("specs/wrong_task_three_reset.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [WRONG_FILES_IN_WORKING_DIRECTORY, WRONG_FILES_IN_STAGING_AREA],
        )


def test_incorrect_head_commit():
    with loader.load("specs/incorrect_head_commit.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [WRONG_HEAD_COMMIT],
        )

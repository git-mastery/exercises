from exercise_utils.test import GitAutograderTestLoader, assert_output
from git_autograder.status import GitAutograderStatus

from .verify import (
    CONTAINS_TASK_ONE_COMMITS,
    CONTAINS_TASK_THREE_COMMIT,
    CONTAINS_TASK_TWO_COMMIT,
    WRONG_FILES_IN_STAGING_AREA,
    WRONG_FILES_IN_WORKING_DIRECTORY,
    WRONG_HEAD_COMMIT,
    verify,
)

REPOSITORY_NAME = "sensors-reset"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)

CLONE_URL = "https://github.com/git-mastery/gm-sensors"


def test_base():
    with loader.start(clone_from=CLONE_URL) as (test, rs):
        rs.git.reset("5950516", hard=True)
        rs.git.reset("f900a07", mixed=True)
        rs.git.reset("c47b187", soft=True)

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_no_changes():
    with loader.start(clone_from=CLONE_URL) as (test, _):
        output = test.run()
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [CONTAINS_TASK_ONE_COMMITS]
        )


def test_incomplete_task_two_reset():
    with loader.start(clone_from=CLONE_URL) as (test, rs):
        rs.git.reset("5950516", hard=True)

        output = test.run()
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [CONTAINS_TASK_TWO_COMMIT]
        )


def test_incomplete_task_three_reset():
    with loader.start(clone_from=CLONE_URL) as (test, rs):
        rs.git.reset("5950516", hard=True)
        rs.git.reset("f900a07", mixed=True)

        output = test.run()
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [CONTAINS_TASK_THREE_COMMIT]
        )


def test_wrong_task_two_reset():
    with loader.start(clone_from=CLONE_URL) as (test, rs):
        rs.git.reset("5950516", hard=True)
        rs.git.reset("f900a07", hard=True)
        rs.git.reset("c47b187", soft=True)

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [WRONG_FILES_IN_WORKING_DIRECTORY],
        )


def test_wrong_task_three_reset():
    with loader.start(clone_from=CLONE_URL) as (test, rs):
        rs.git.reset("5950516", hard=True)
        rs.git.reset("f900a07", mixed=True)
        rs.git.reset("c47b187", hard=True)

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [WRONG_FILES_IN_WORKING_DIRECTORY, WRONG_FILES_IN_STAGING_AREA],
        )


def test_incorrect_head_commit():
    with loader.start(clone_from=CLONE_URL) as (test, rs):
        rs.git.reset("5950516", hard=True)
        rs.git.reset("f900a07", mixed=True)
        rs.git.reset("c47b187", soft=True)
        rs.git.reset("e45a4fc", soft=True)

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [WRONG_HEAD_COMMIT],
        )

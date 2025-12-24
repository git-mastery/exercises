from git_autograder import GitAutograderStatus, GitAutograderTestLoader, assert_output

from ..verify import (
    MISSING_FILE,
    COMMITS_UNREVERTED,
    COMMITS_REVERTED_WRONG_ORDER,
    INCORRECT_READINGS,
    verify,
)

REPOSITORY_NAME = "sensors-revert"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_base():
    with loader.load("specs/base.yml", "start") as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_no_revert():
    with loader.load("specs/no_revert.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [COMMITS_UNREVERTED],
        )


def test_wrong_order_revert():
    with loader.load("specs/wrong_order_revert.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [COMMITS_REVERTED_WRONG_ORDER],
        )


def test_missing_files():
    with loader.load("specs/missing_files.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [MISSING_FILE.format(filename="east.csv"),
             MISSING_FILE.format(filename="north.csv"),
             MISSING_FILE.format(filename="south.csv"),
             MISSING_FILE.format(filename="west.csv"),],
        )


def test_incorrect_readings():
    with loader.load("specs/incorrect_readings.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [INCORRECT_READINGS],
        )


def test_no_revert_commit():
    with loader.load("specs/no_revert_commit.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [COMMITS_UNREVERTED],
        )


def test_only_jan_14_reverted():
    with loader.load("specs/only_jan_14_reverted.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [COMMITS_UNREVERTED],
        )


def test_only_jan_13_reverted():
    with loader.load("specs/only_jan_13_reverted.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [COMMITS_REVERTED_WRONG_ORDER],
        )

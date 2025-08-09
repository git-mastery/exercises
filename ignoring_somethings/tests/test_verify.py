from git_autograder import GitAutograderStatus, GitAutograderTestLoader, assert_output

from ..verify import (
    NOT_IGNORING_IGNORE_ME,
    NOT_IGNORING_REST_OF_MANY,
    NOT_IGNORING_RUNAWAY,
    NOT_PATTERN_MATCHING_RUNAWAY,
    STILL_HIDING,
    STILL_IGNORING_FILE_22,
    verify,
)

REPOSITORY_NAME = "ignoring-somethings"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_valid():
    with loader.load("specs/valid.yml") as output:
        assert_output(
            output,
            GitAutograderStatus.SUCCESSFUL,
            ["Great work using .gitignore!"],
        )


def test_no_change():
    with loader.load("specs/no_change.yml") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                STILL_IGNORING_FILE_22,
                STILL_HIDING,
                NOT_IGNORING_IGNORE_ME,
                NOT_IGNORING_RUNAWAY,
            ],
        )


def test_overriding():
    with loader.load("specs/overriding.yml") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                STILL_HIDING,
            ],
        )


def test_overriding_many():
    with loader.load("specs/overriding_many.yml") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [NOT_IGNORING_REST_OF_MANY],
        )


def test_not_pattern_matching():
    with loader.load("specs/not_pattern_matching.yml") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [NOT_PATTERN_MATCHING_RUNAWAY],
        )

from git_autograder import GitAutograderStatus, GitAutograderTestLoader, assert_output

from ..verify import (
    MERGE_NOT_RESOLVED,
    NOT_ON_MAIN,
    RESET_MESSAGE,
    UNCOMMITTED_CHANGES,
    verify,
)

REPOSITORY_NAME = "conflict-mediator"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_base():
    with loader.load("specs/base.yml", "start") as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_base_single_quotes():
    with loader.load("specs/base_single_quotes.yml", "start") as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_no_fix():
    with loader.load("specs/no_fix.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [MERGE_NOT_RESOLVED, RESET_MESSAGE],
        )


def test_uncommitted():
    with loader.load("specs/uncommitted.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [UNCOMMITTED_CHANGES])


def test_not_main():
    with loader.load("specs/not_main.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [NOT_ON_MAIN])

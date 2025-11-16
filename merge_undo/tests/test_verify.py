from git_autograder import GitAutograderStatus, GitAutograderTestLoader, assert_output

from ..verify import (
    NOT_ON_MAIN,
    RESET_MESSAGE,
    UNCOMMITTED_CHANGES,
    DETACHED_HEAD,
    MERGES_NOT_UNDONE,
    MAIN_WRONG_COMMIT,
    verify,
)

REPOSITORY_NAME = "merge-undo"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_base():
    with loader.load("specs/base.yml", "start") as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_merges_not_undone():
    with loader.load("specs/merges_not_undone.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [MERGES_NOT_UNDONE, RESET_MESSAGE],
        )


def test_detached_head():
    with loader.load("specs/detached_head.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [DETACHED_HEAD, RESET_MESSAGE],
        )


def test_main_wrong_commit():
    with loader.load("specs/main_wrong_commit.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [MAIN_WRONG_COMMIT, RESET_MESSAGE],
        )


def test_uncommitted():
    with loader.load("specs/uncommitted.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [UNCOMMITTED_CHANGES])


def test_not_main():
    with loader.load("specs/not_main.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [NOT_ON_MAIN])

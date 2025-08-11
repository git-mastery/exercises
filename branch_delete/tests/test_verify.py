from git_autograder import GitAutograderTestLoader, assert_output
from git_autograder.status import GitAutograderStatus

from ..verify import (
    FIX_SCROLLING_BUG_EXISTS,
    IMPROVE_LOADING_EXISTS,
    IMPROVE_LOADING_MERGED,
    verify,
)

REPOSITORY_NAME = "branch-delete"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_base():
    with loader.load("specs/base.yml") as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_fix_scrolling_bug_not_deleted():
    with loader.load("specs/fix_scrolling_bug_not_deleted.yml") as output:
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [FIX_SCROLLING_BUG_EXISTS]
        )


def test_improve_loading_not_deleted():
    with loader.load("specs/improve_loading_not_deleted.yml") as output:
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [IMPROVE_LOADING_EXISTS]
        )


def test_improve_loading_merged():
    with loader.load("specs/improve_loading_merged.yml") as output:
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [IMPROVE_LOADING_MERGED]
        )

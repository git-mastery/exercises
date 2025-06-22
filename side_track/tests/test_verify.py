from git_autograder import GitAutograderStatus, GitAutograderTestLoader
from git_autograder.test_utils import assert_output

from ..verify import (
    CALCULATOR_NOT_FIXED,
    GREET_NOT_FIXED,
    MISSING_BUG_FIX_BRANCH,
    MISSING_COMMITS,
    NOT_ON_MAIN,
    UNCOMMITTED_CHANGES,
    verify,
)

REPOSITORY_NAME = "side-track"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_uncommitted():
    with loader.load("specs/uncommitted.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [UNCOMMITTED_CHANGES])


def test_not_main():
    with loader.load("specs/not_main.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [NOT_ON_MAIN])


def test_no_bug_fix():
    with loader.load("specs/no_bug_fix.yml") as output:
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [MISSING_BUG_FIX_BRANCH]
        )


def test_missing_commits():
    with loader.load("specs/missing_commits.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [MISSING_COMMITS])


def test_greet_not_fixed():
    with loader.load("specs/greet_not_fixed.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [GREET_NOT_FIXED])


def test_add_not_fixed():
    with loader.load("specs/add_not_fixed.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [CALCULATOR_NOT_FIXED])

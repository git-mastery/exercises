from git_autograder import GitAutograderTestLoader, assert_output
from git_autograder.status import GitAutograderStatus

from ..verify import (
    FEATURE_LOGIN_MISSING,
    LOGIN_STILL_EXISTS,
    NO_RENAME_EVIDENCE_FEATURE_LOGIN,
    verify,
)

REPOSITORY_NAME = "branch-rename"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_base():
    with loader.load("specs/base.yml") as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_new_feature_login_branch():
    with loader.load("specs/new_feature_login_branch.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [LOGIN_STILL_EXISTS])


def test_rename_login_wrong():
    with loader.load("specs/rename_login_wrong.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [FEATURE_LOGIN_MISSING])


def test_not_rename():
    with loader.load("specs/not_rename.yml") as output:
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [NO_RENAME_EVIDENCE_FEATURE_LOGIN]
        )

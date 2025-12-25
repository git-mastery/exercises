from exercise_utils.test import GitAutograderTestLoader, assert_output
from git_autograder.status import GitAutograderStatus

from .verify import (
    FEATURE_LOGIN_MISSING,
    LOGIN_STILL_EXISTS,
    NO_RENAME_EVIDENCE_FEATURE_LOGIN,
    verify,
)

REPOSITORY_NAME = "branch-rename"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


def test_base():
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.git.branch("login")
        rs.git.branch("feature/login", old_branch="login", move=True)

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_new_feature_login_branch():
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.git.branch("login")
        rs.git.branch("feature/login")

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [LOGIN_STILL_EXISTS])


def test_rename_login_wrong():
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.git.branch("login")
        rs.git.branch("feature/logi", old_branch="login", move=True)

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [FEATURE_LOGIN_MISSING])


def test_not_rename():
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.git.branch("login")
        rs.git.branch("not-this", old_branch="login", move=True)
        rs.git.branch("feature/login")

        output = test.run()
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [NO_RENAME_EVIDENCE_FEATURE_LOGIN]
        )


def test_indirect_rename():
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.git.branch("login")
        rs.git.branch("feature/logi", old_branch="login", move=True)
        rs.git.branch("feature/login", old_branch="feature/logi", move=True)

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_rename_after():
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.git.branch("login")
        rs.git.branch("feature/login", old_branch="login", move=True)
        rs.git.branch("test", old_branch="feature/login", move=True)

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [FEATURE_LOGIN_MISSING])

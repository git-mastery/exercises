from contextlib import contextmanager
from typing import Iterator, Tuple

from exercise_utils.test import (
    GitAutograderTest,
    GitAutograderTestLoader,
    GitMasteryHelper,
    assert_output,
)
from git_autograder import GitAutograderStatus
from repo_smith.repo_smith import RepoSmith

from .verify import (
    FEATURE_DASHBOARD_MERGE_MISSING,
    FEATURE_LOGIN_MERGE_MISSING,
    FEATURE_PAYMENTS_MERGE_MISSING,
    MISSING_MERGES,
    NO_FAST_FORWARDING,
    NO_MERGES,
    NOT_ON_MAIN,
    RESET_MESSAGE,
    UNCOMMITTED_CHANGES,
    verify,
)

REPOSITORY_NAME = "branch-bender"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


@contextmanager
def base_setup() -> Iterator[Tuple[GitAutograderTest, RepoSmith]]:
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()

        rs.git.checkout("feature/login", branch=True)
        rs.git.commit(message="Empty commit on feature/login", allow_empty=True)
        rs.git.checkout("main")

        rs.git.checkout("feature/dashboard", branch=True)
        rs.git.commit(message="Empty commit on feature/dashboard", allow_empty=True)
        rs.git.checkout("main")

        rs.git.checkout("feature/payments", branch=True)
        rs.git.commit(message="Empty commit on feature/payments", allow_empty=True)
        rs.git.checkout("main")

        yield test, rs


def test_base():
    with base_setup() as (test, rs):
        rs.git.merge("feature/login", no_ff=True)
        rs.git.merge("feature/dashboard", no_ff=True)
        rs.git.merge("feature/payments", no_ff=True)

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_merge_undo_succeeds():
    with base_setup() as (test, rs):
        rs.git.merge("feature/login", no_ff=False)
        rs.git.reset("HEAD~1", hard=True)
        rs.git.merge("feature/login", no_ff=True)
        rs.git.merge("feature/dashboard", no_ff=True)
        rs.git.merge("feature/payments", no_ff=True)

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_ff_fails():
    with base_setup() as (test, rs):
        rs.git.merge("feature/login")
        rs.git.merge("feature/dashboard")
        rs.git.merge("feature/payments")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [NO_FAST_FORWARDING.format(branch_name="feature/login"), RESET_MESSAGE],
        )


def test_no_merges():
    with base_setup() as (test, _):
        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [NO_MERGES])


def test_missing_merges():
    with base_setup() as (test, rs):
        rs.git.merge("feature/login", no_ff=True)
        rs.git.merge("feature/dashboard", no_ff=True)

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [MISSING_MERGES])


def test_uncommitted():
    with loader.start() as (test, rs):
        rs.files.create_or_update("test.txt", "hi")
        rs.git.add(all=True)
        rs.git.commit(message="Start")
        rs.helper(GitMasteryHelper).create_start_tag()
        rs.files.create_or_update("test.txt", "changed")

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [UNCOMMITTED_CHANGES])


def test_not_main():
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.git.checkout("bug-fix", branch=True)

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [NOT_ON_MAIN])


def test_not_login_first():
    with base_setup() as (test, rs):
        rs.git.merge("feature/dashboard", no_ff=True)
        rs.git.merge("feature/login", no_ff=True)
        rs.git.merge("feature/payments", no_ff=True)

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [FEATURE_LOGIN_MERGE_MISSING, RESET_MESSAGE],
        )


def test_not_dashboard_second():
    with base_setup() as (test, rs):
        rs.git.merge("feature/login", no_ff=True)
        rs.git.merge("feature/payments", no_ff=True)
        rs.git.merge("feature/dashboard", no_ff=True)

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [FEATURE_DASHBOARD_MERGE_MISSING, RESET_MESSAGE],
        )


def test_not_payments_last():
    with base_setup() as (test, rs):
        rs.git.checkout("other", branch=True)
        rs.git.commit(message="Empty commit on other", allow_empty=True)
        rs.git.checkout("main")

        rs.git.merge("feature/login", no_ff=True)
        rs.git.merge("feature/dashboard", no_ff=True)
        rs.git.merge("other", no_ff=True)

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [FEATURE_PAYMENTS_MERGE_MISSING, RESET_MESSAGE],
        )

from git_autograder import GitAutograderStatus, GitAutograderTestLoader, assert_output

from ..verify import (
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

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_base():
    with loader.load("specs/base.yml", "start") as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_ff_fails():
    with loader.load("specs/ff_fails.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [NO_FAST_FORWARDING.format(branch_name="feature/login"), RESET_MESSAGE],
        )


def test_no_merges():
    with loader.load("specs/no_merges.yml", "start") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [NO_MERGES])


def test_missing_merges():
    with loader.load("specs/missing_merges.yml", "start") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [MISSING_MERGES])


def test_uncommitted():
    with loader.load("specs/uncommitted.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [UNCOMMITTED_CHANGES])


def test_not_main():
    with loader.load("specs/not_main.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [NOT_ON_MAIN])


def test_not_login_first():
    with loader.load("specs/not_login_first.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [FEATURE_LOGIN_MERGE_MISSING, RESET_MESSAGE],
        )


def test_not_dashboard_second():
    with loader.load("specs/not_dashboard_second.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [FEATURE_DASHBOARD_MERGE_MISSING, RESET_MESSAGE],
        )


def test_not_payments_last():
    with loader.load("specs/not_payments_last.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [FEATURE_PAYMENTS_MERGE_MISSING, RESET_MESSAGE],
        )

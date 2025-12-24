from git_autograder import GitAutograderTestLoader, assert_output
from git_autograder.status import GitAutograderStatus

from ..verify import (
    MISSING_BRANCH,
    WRONG_CONTENT,
    WRONG_START,
    MISSING_COMMIT,
    verify,
)

REPOSITORY_NAME = "branch-previous"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_base():
    with loader.load("specs/base.yml") as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_visitor_missing_branch():
    with loader.load("specs/visitor_missing_branch.yml") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [MISSING_BRANCH.format(branch_name="visitor-line")],
        )


def test_sleep_missing_branch():
    with loader.load("specs/sleep_missing_branch.yml") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [MISSING_BRANCH.format(branch_name="sleep-line")],
        )


def test_visitor_wrong_start_first_commit():
    with loader.load("specs/visitor_wrong_start_first_commit.yml") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [WRONG_START.format(branch_name="visitor-line")],
        )


def test_visitor_wrong_start_third_commit():
    with loader.load("specs/visitor_wrong_start_third_commit.yml") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [WRONG_START.format(branch_name="visitor-line")],
        )


def test_visitor_wrong_content():
    with loader.load("specs/visitor_wrong_content.yml") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                WRONG_CONTENT.format(
                    branch_name="visitor-line",
                    expected_content="I heard someone knocking at the door.",
                )
            ],
        )


def test_sleep_wrong_content():
    with loader.load("specs/sleep_wrong_content.yml") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                WRONG_CONTENT.format(
                    branch_name="sleep-line",
                    expected_content="I fell asleep on the couch.",
                )
            ],
        )


def test_visitor_missing_commit():
    with loader.load("specs/visitor_missing_commit.yml") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [MISSING_COMMIT.format(branch_name="visitor-line")],
        )

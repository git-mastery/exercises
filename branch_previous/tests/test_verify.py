from git_autograder import GitAutograderTestLoader, assert_output
from git_autograder.status import GitAutograderStatus

from ..verify import (
    BRANCH_MISSING,
    WRONG_CONTENT,
    WRONG_START,
    verify,
)

REPOSITORY_NAME = "branch-previous"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_base():
    with loader.load("specs/base.yml") as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_visitor_branch_missing():
    with loader.load("specs/visitor_branch_missing.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [BRANCH_MISSING.format(branch_name="visitor-line")])


def test_sleep_branch_missing():
    with loader.load("specs/sleep_branch_missing.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [BRANCH_MISSING.format(branch_name="sleep-line")])


def test_visitor_wrong_start():
    with loader.load("specs/visitor_wrong_start.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [WRONG_START.format(branch_name="visitor-line")])


def test_visitor_wrong_content():
    with loader.load("specs/visitor_wrong_content.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [WRONG_CONTENT.format(branch_name="visitor-line", expected_content="I heard someone knocking at the door.")])


def test_visitor_no_commit():
    with loader.load("specs/visitor_no_commit.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [WRONG_CONTENT.format(branch_name="visitor-line", expected_content="I heard someone knocking at the door.")])

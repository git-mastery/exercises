from git_autograder import GitAutograderStatus, GitAutograderTestLoader
from git_autograder.test_utils import assert_output

from ..verify import WRONG_BRANCH_POINT, verify

REPOSITORY_NAME = "mix-messy-docs"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_base():
    with loader.load("specs/base.yml", "start"):
        pass


def test_wrong_branch_point():
    with loader.load("specs/wrong_branch_point.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [WRONG_BRANCH_POINT])


def test_right_order():
    with loader.load("specs/right_order.yml") as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL)

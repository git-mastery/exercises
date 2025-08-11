from git_autograder import GitAutograderTestLoader, assert_output
from git_autograder.status import GitAutograderStatus

from ..verify import (
    OPTIMIZATION_APPROACH_1_EXISTS,
    OPTIMIZATION_APPROACH_2_EXISTS,
    OPTIMIZATION_APPROACH_2_MERGED,
    verify,
)

REPOSITORY_NAME = "branch-delete"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_base():
    with loader.load("specs/base.yml") as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_optimization_approach_1_not_deleted():
    with loader.load("specs/optimization_approach_1_not_deleted.yml") as output:
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [OPTIMIZATION_APPROACH_1_EXISTS]
        )


def test_optimization_approach_2_not_deleted():
    with loader.load("specs/optimization_approach_2_not_deleted.yml") as output:
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [OPTIMIZATION_APPROACH_2_EXISTS]
        )


def test_optimization_approach_2_merged():
    with loader.load("specs/optimization_approach_2_merged.yml") as output:
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [OPTIMIZATION_APPROACH_2_MERGED]
        )

from contextlib import contextmanager
from typing import Iterator, Tuple

from exercise_utils.test import (
    GitAutograderTest,
    GitAutograderTestLoader,
    assert_output,
)
from git_autograder.status import GitAutograderStatus
from repo_smith.repo_smith import RepoSmith

from .verify import (
    OPTIMIZATION_APPROACH_1_EXISTS,
    OPTIMIZATION_APPROACH_2_EXISTS,
    OPTIMIZATION_APPROACH_2_MERGED,
    verify,
)

REPOSITORY_NAME = "branch-delete"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


@contextmanager
def base_setup() -> Iterator[Tuple[GitAutograderTest, RepoSmith]]:
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.git.branch("optimization-approach-1")
        rs.git.branch("optimization-approach-2")

        yield test, rs


def test_base():
    with base_setup() as (test, rs):
        rs.git.branch("optimization-approach-1", delete=True)
        rs.git.branch("optimization-approach-2", delete=True)

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_optimization_approach_1_not_deleted():
    with base_setup() as (test, rs):
        rs.git.branch("optimization-approach-2", delete=True)

        output = test.run()
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [OPTIMIZATION_APPROACH_1_EXISTS]
        )


def test_optimization_approach_2_not_deleted():
    with base_setup() as (test, rs):
        rs.git.branch("optimization-approach-1", delete=True)

        output = test.run()
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [OPTIMIZATION_APPROACH_2_EXISTS]
        )


def test_optimization_approach_2_merged():
    with base_setup() as (test, rs):
        rs.git.checkout("optimization-approach-2")
        rs.git.commit(message="Empty", allow_empty=True)
        rs.git.checkout("main")
        rs.git.branch("optimization-approach-1", delete=True)
        rs.git.merge("optimization-approach-2")
        rs.git.branch("optimization-approach-2", delete=True)

        output = test.run()
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [OPTIMIZATION_APPROACH_2_MERGED]
        )

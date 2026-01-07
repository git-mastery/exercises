from contextlib import contextmanager
from typing import Iterator, Tuple

from repo_smith.repo_smith import RepoSmith
from exercise_utils.test import (
    GitAutograderTest,
    GitAutograderTestLoader,
    assert_output,
)
from git_autograder import GitAutograderStatus

from .verify import (
    FAST_FORWARD_REQUIRED,
    ONLY_WITH_SALLY_MERGED,
    verify,
)

REPOSITORY_NAME = "branch-forward"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


@contextmanager
def base_setup() -> Iterator[Tuple[GitAutograderTest, RepoSmith]]:
    with loader.start() as (test, rs):
        rs.git.commit(message="Set initial state", allow_empty=True)
        rs.git.commit(message="Introduce Harry", allow_empty=True)
        rs.git.commit(message="Add about family", allow_empty=True)

        rs.git.checkout("with-ginny", branch=True)
        rs.git.commit(message="Add about Ginny", allow_empty=True)

        rs.git.checkout("main")
        rs.git.commit(message="Add cast.txt", allow_empty=True)

        rs.git.checkout("with-sally", branch=True)
        rs.git.commit(message="Mention Sally", allow_empty=True)

        rs.git.checkout("with-ginny")
        rs.git.commit(message="Mention Ginny is single", allow_empty=True)

        rs.git.checkout("main")

        yield test, rs


def test_success():
    with base_setup() as (test, rs):
        rs.git.merge("with-sally")

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_no_merges():
    with base_setup() as (test, _):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [ONLY_WITH_SALLY_MERGED],
        )


def test_other_branch_non_ff():
    with base_setup() as (test, rs):
        rs.git.merge("with-ginny")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [ONLY_WITH_SALLY_MERGED],
        )


def test_other_branch_ff():
    with base_setup() as (test, rs):
        rs.git.checkout("with-ron", branch=True)
        rs.git.commit(message="Mention Ron", allow_empty=True)

        rs.git.checkout("main")
        rs.git.merge("with-ron")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [ONLY_WITH_SALLY_MERGED],
        )


def test_merge_with_sally_no_ff():
    with base_setup() as (test, rs):
        rs.git.merge("with-sally", no_ff=True)

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [FAST_FORWARD_REQUIRED],
        )

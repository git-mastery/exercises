from contextlib import contextmanager
from typing import Iterator, Tuple

from exercise_utils.test import (
    GitAutograderTest,
    GitAutograderTestLoader,
    assert_output,
)
from git_autograder import GitAutograderStatus
from repo_smith.repo_smith import RepoSmith

from .verify import PQR_BRANCH_NOT_PUSHED, verify

REPOSITORY_NAME = "glossary-branch-push"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


@contextmanager
def base_setup() -> Iterator[Tuple[GitAutograderTest, RepoSmith]]:
    with loader.start(include_remote_repo=True) as (test, rs, rs_remote):
        remote_path = str(rs_remote.repo.git_dir)
        rs.git.remote_add("origin", remote_path)

        rs.git.checkout("PQR", branch=True)
        rs.files.create_or_update(
            "r.txt",
            "refactoring: Improving the code without changing what it does... in theory.\n",
        )
        rs.git.add(all=True)
        rs.git.commit(message="Add 'refactoring'")
        rs.git.checkout("main")

        yield test, rs


def test_base():
    with base_setup() as (test, rs):
        rs.git.push("origin", "PQR")

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_pqr_not_pushed():
    with base_setup() as (test, rs):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [PQR_BRANCH_NOT_PUSHED],
        )

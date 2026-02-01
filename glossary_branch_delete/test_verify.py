from contextlib import contextmanager
from typing import Iterator, Tuple

from exercise_utils.test import (
    GitAutograderTest,
    GitAutograderTestLoader,
    assert_output,
)
from git_autograder import GitAutograderStatus
from repo_smith.repo_smith import RepoSmith

from .verify import (
    VWX_BRANCH_EXISTS_LOCALLY,
    VWX_BRANCH_EXISTS_REMOTELY,
    verify,
)

REPOSITORY_NAME = "glossary-branch-delete"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


@contextmanager
def base_setup() -> Iterator[Tuple[GitAutograderTest, RepoSmith]]:
    with loader.start(include_remote_repo=True) as (test, rs, rs_remote):
        remote_path = str(rs_remote.repo.git_dir)
        rs.git.remote_add("origin", remote_path)

        # doesnt create a branch on remote
        rs_remote.git.commit(allow_empty=True, message="Initial commit")
        rs_remote.git.checkout("TEST", branch=True)

        # works
        rs.git.checkout("VWX", branch=True)
        rs.git.commit(allow_empty=True, message="Empty commit")
        rs.git.push("origin", "VWX")

        rs.git.checkout("main")

        yield test, rs


def test_base():
    with base_setup() as (test, rs):
        rs.git.push("origin", ":VWX")
        rs.repo.delete_head("VWX", force=True)

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_vwx_exists_remotely():
    with base_setup() as (test, rs):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [VWX_BRANCH_EXISTS_REMOTELY],
        )


def test_vwx_exists_locally():
    with base_setup() as (test, rs):
        rs.git.checkout("VWX")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [VWX_BRANCH_EXISTS_LOCALLY],
        )


def test_vwx_exists_both():
    with base_setup() as (test, rs):
        rs.git.checkout("VWX")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [VWX_BRANCH_EXISTS_LOCALLY, VWX_BRANCH_EXISTS_REMOTELY],
        )

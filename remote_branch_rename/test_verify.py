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
    IMPROVE_LOADING_LOCAL_MISSING,
    IMPROVE_LOADING_LOCAL_STILL_EXISTS,
    IMPROVE_LOADING_REMOTE_MISSING,
    IMPROVE_LOADING_REMOTE_OLD_PRESENT,
    NO_RENAME_EVIDENCE_IMPROVE_LOADING,
    verify,
)

REPOSITORY_NAME = "remote-branch-rename"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


@contextmanager
def base_setup() -> Iterator[Tuple[GitAutograderTest, RepoSmith]]:
    with loader.start(include_remote_repo=True) as (test, rs, rs_remote):
        remote_path = str(rs_remote.repo.git_dir)

        rs.git.commit(message="Improved loading of page", allow_empty=True)
        rs.git.remote_add("origin", remote_path)
        rs.git.branch("improve-loadding")
        rs.git.push("origin", "improve-loadding")

        yield test, rs


def test_base():
    with base_setup() as (test, rs):
        rs.git.branch("improve-loading", old_branch="improve-loadding", move=True)
        rs.git.push("origin", "improve-loading")
        rs.git.push("origin", ":improve-loadding")

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_new_improve_loading_branch():
    with base_setup() as (test, rs):
        rs.git.branch("improve-loading")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [IMPROVE_LOADING_LOCAL_STILL_EXISTS],
        )


def test_rename_improve_loading_wrong():
    with base_setup() as (test, rs):
        rs.git.branch("improve-loaing", old_branch="improve-loadding", move=True)

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [IMPROVE_LOADING_LOCAL_MISSING],
        )


def test_improve_loading_no_rename_evidence():
    with base_setup() as (test, rs):
        rs.git.branch("improve-loading")
        rs.git.branch("improve-loadding", delete=True)

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [NO_RENAME_EVIDENCE_IMPROVE_LOADING],
        )


def test_improve_loadding_remote_exists():
    with base_setup() as (test, rs):
        rs.git.branch("improve-loading", old_branch="improve-loadding", move=True)
        rs.git.push("origin", "improve-loading")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [IMPROVE_LOADING_REMOTE_OLD_PRESENT],
        )


def test_improve_loading_remote_missing():
    with base_setup() as (test, rs):
        rs.git.branch("improve-loading", old_branch="improve-loadding", move=True)
        rs.git.push("origin", ":improve-loadding")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [IMPROVE_LOADING_REMOTE_MISSING],
        )

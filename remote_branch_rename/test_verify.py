from contextlib import contextmanager
from typing import Iterator, Tuple
from unittest.mock import patch

from repo_smith.repo_smith import RepoSmith

from exercise_utils.test import (
    GitAutograderTest,
    GitAutograderTestLoader,
    GitMasteryHelper,
    assert_output,
)
from git_autograder import GitAutograderStatus

from .verify import (
    FIX_SCROLLING_BUG_MISSING,
    IMPROVE_LOADING_LOCAL_MISSING,
    IMPROVE_LOADING_LOCAL_STILL_EXISTS,
    IMPROVE_LOADING_REMOTE_MISSING,
    IMPROVE_LOADING_REMOTE_OLD_PRESENT,
    NO_RENAME_EVIDENCE_TRY_QUICK_FIX,
    TRY_QUICK_FIX_STILL_EXISTS,
    verify,
)

REPOSITORY_NAME = "remote-branch-rename"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


@contextmanager
def base_setup() -> Iterator[Tuple[GitAutograderTest, RepoSmith]]:
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        rs.git.branch("try-quick-fix")
        rs.git.branch("improve-loadding")

        yield test, rs


def test_base():
    with (
        patch("remote_branch_rename.verify.fetch_remotes", side_effect=None),
        patch(
            "remote_branch_rename.verify.get_remotes", return_value=["improve-loading"]
        ),
        base_setup() as (test, rs),
    ):
        rs.git.branch("fix-scrolling-bug", old_branch="try-quick-fix", move=True)
        rs.git.branch("improve-loading", old_branch="improve-loadding", move=True)

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_new_fix_scrolling_bug_branch():
    with base_setup() as (test, rs):
        rs.git.branch("fix-scrolling-bug")
        rs.git.branch("improve-loading", old_branch="improve-loadding", move=True)

        output = test.run()
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [TRY_QUICK_FIX_STILL_EXISTS]
        )


def test_rename_quick_fix_wrong():
    with base_setup() as (test, rs):
        rs.git.branch("fix-scroling-bug", old_branch="try-quick-fix", move=True)
        rs.git.branch("improve-loading", old_branch="improve-loadding", move=True)

        output = test.run()
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [FIX_SCROLLING_BUG_MISSING]
        )


def test_not_quick_fix_rename():
    with base_setup() as (test, rs):
        rs.git.branch("not-this", old_branch="try-quick-fix", move=True)
        rs.git.branch("improve-loading", old_branch="improve-loadding", move=True)
        rs.git.branch("fix-scrolling-bug")

        output = test.run()
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [NO_RENAME_EVIDENCE_TRY_QUICK_FIX]
        )


def test_new_improve_loading_branch():
    with base_setup() as (test, rs):
        rs.git.branch("fix-scrolling-bug", old_branch="try-quick-fix", move=True)
        rs.git.branch("improve-loading")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [IMPROVE_LOADING_LOCAL_STILL_EXISTS],
        )


def test_rename_improve_loading_wrong():
    with base_setup() as (test, rs):
        rs.git.branch("fix-scrolling-bug", old_branch="try-quick-fix", move=True)
        rs.git.branch("improve-loaing", old_branch="improve-loadding", move=True)

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [IMPROVE_LOADING_LOCAL_MISSING],
        )


def test_improve_loadding_remote_exists():
    with (
        patch("remote_branch_rename.verify.fetch_remotes", side_effect=None),
        patch(
            "remote_branch_rename.verify.get_remotes", return_value=["improve-loadding"]
        ),
        base_setup() as (test, rs),
    ):
        rs.git.branch("fix-scrolling-bug", old_branch="try-quick-fix", move=True)
        rs.git.branch("improve-loading", old_branch="improve-loadding", move=True)

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [IMPROVE_LOADING_REMOTE_OLD_PRESENT],
        )


def test_improve_loading_remote_missing():
    with (
        patch("remote_branch_rename.verify.fetch_remotes", side_effect=None),
        patch(
            "remote_branch_rename.verify.get_remotes", return_value=["improve-loaing"]
        ),
        base_setup() as (test, rs),
    ):
        rs.git.branch("fix-scrolling-bug", old_branch="try-quick-fix", move=True)
        rs.git.branch("improve-loading", old_branch="improve-loadding", move=True)

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [IMPROVE_LOADING_REMOTE_MISSING],
        )

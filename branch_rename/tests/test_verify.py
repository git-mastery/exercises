from unittest.mock import patch

from git_autograder import GitAutograderStatus, GitAutograderTestLoader, assert_output

from ..verify import (
    FIX_SCROLLING_BUG_MISSING,
    IMPROVE_LOADING_LOCAL_MISSING,
    IMPROVE_LOADING_LOCAL_STILL_EXISTS,
    IMPROVE_LOADING_REMOTE_MISSING,
    IMPROVE_LOADING_REMOTE_OLD_PRESENT,
    NO_RENAME_EVIDENCE_TRY_QUICK_FIX,
    TRY_QUICK_FIX_STILL_EXISTS,
    verify,
)

REPOSITORY_NAME = "branch-rename"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_base():
    with (
        patch("branch_rename.verify.fetch_remotes", side_effect=None),
        patch("branch_rename.verify.get_remotes", return_value=["improve-loading"]),
        loader.load("specs/base.yml") as output,
    ):
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_new_fix_scrolling_bug_branch():
    with (
        loader.load("specs/new_fix_scrolling_bug_branch.yml") as output,
    ):
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [TRY_QUICK_FIX_STILL_EXISTS]
        )


def test_rename_quick_fix_wrong():
    with (
        loader.load("specs/rename_quick_fix_wrong.yml") as output,
    ):
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [FIX_SCROLLING_BUG_MISSING]
        )


def test_not_quick_fix_rename():
    with (
        loader.load("specs/not_quick_fix_rename.yml") as output,
    ):
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [NO_RENAME_EVIDENCE_TRY_QUICK_FIX]
        )


def test_new_improve_loading_branch():
    with (
        loader.load("specs/new_improve_loading_branch.yml") as output,
    ):
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [IMPROVE_LOADING_LOCAL_STILL_EXISTS],
        )


def test_rename_improve_loading_wrong():
    with (
        loader.load("specs/rename_improve_loading_wrong.yml") as output,
    ):
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [IMPROVE_LOADING_LOCAL_MISSING],
        )


def test_improve_loadding_remote_exists():
    with (
        patch("branch_rename.verify.fetch_remotes", side_effect=None),
        patch("branch_rename.verify.get_remotes", return_value=["improve-loadding"]),
        loader.load("specs/base.yml") as output,
    ):
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [IMPROVE_LOADING_REMOTE_OLD_PRESENT],
        )


def test_improve_loading_remote_missing():
    with (
        patch("branch_rename.verify.fetch_remotes", side_effect=None),
        patch("branch_rename.verify.get_remotes", return_value=["improve-loaing"]),
        loader.load("specs/base.yml") as output,
    ):
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [IMPROVE_LOADING_REMOTE_MISSING],
        )

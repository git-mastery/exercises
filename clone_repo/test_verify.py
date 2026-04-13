from unittest.mock import patch

import pytest
from exercise_utils.test import GitAutograderTestLoader, assert_output
from git_autograder import GitAutograderWrongAnswerException
from git_autograder.status import GitAutograderStatus

from .verify import (
    CLONE_MISSING,
    IMPROPER_GH_CLI_SETUP,
    NO_FORK_FOUND,
    NOT_GIT_MASTERY_FORK,
    ORIGIN_MISSING,
    ORIGIN_WRONG,
    UPSTREAM_MISSING,
    UPSTREAM_WRONG,
    verify,
)

REPOSITORY_NAME = "clone-repo"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)

# NOTE: This exercise is a special case where we do not require repo-smith. Instead,
# we directly mock function calls to verify that all branches are covered for us.


def test_pass():
    fake_origin = type(
        "FakeRemote", (), {"url": "https://github.com/dummy/gm-shapes.git"}
    )()
    fake_upstream = type(
        "FakeRemote", (), {"url": "https://github.com/git-mastery/gm-shapes.git"}
    )()
    with (
        loader.start_mock_exercise() as exercise,
        patch("clone_repo.verify.get_username", return_value="dummy"),
        patch("clone_repo.verify.has_fork", return_value=True),
        patch("clone_repo.verify.is_parent_git_mastery", return_value=True),
        patch("clone_repo.verify.has_shapes_folder", return_value=True),
        patch(
            "clone_repo.verify.remote",
            side_effect=lambda name: (
                fake_origin
                if name == "origin"
                else fake_upstream
                if name == "upstream"
                else None
            ),
        ),
    ):
        output = verify(exercise)
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_improper_gh_setup():
    with (
        loader.start_mock_exercise() as exercise,
        patch("clone_repo.verify.get_username", return_value=None),
        patch("clone_repo.verify.has_fork", return_value=True),
        patch("clone_repo.verify.is_parent_git_mastery", return_value=True),
        pytest.raises(GitAutograderWrongAnswerException) as exception,
    ):
        verify(exercise)

        assert exception.value.message == [IMPROPER_GH_CLI_SETUP]


def test_no_fork():
    with (
        loader.start_mock_exercise() as exercise,
        patch("clone_repo.verify.get_username", return_value="dummy"),
        patch("clone_repo.verify.has_fork", return_value=False),
        patch("clone_repo.verify.is_parent_git_mastery", return_value=True),
        pytest.raises(GitAutograderWrongAnswerException) as exception,
    ):
        verify(exercise)

        assert exception.value.message == [NO_FORK_FOUND]


def test_not_right_parent():
    with (
        loader.start_mock_exercise() as exercise,
        patch("clone_repo.verify.get_username", return_value="dummy"),
        patch("clone_repo.verify.has_fork", return_value=True),
        patch("clone_repo.verify.is_parent_git_mastery", return_value=False),
        pytest.raises(GitAutograderWrongAnswerException) as exception,
    ):
        verify(exercise)

        assert exception.value.message == [NOT_GIT_MASTERY_FORK]


def test_missing_shapes_folder():
    with (
        loader.start_mock_exercise() as exercise,
        patch("clone_repo.verify.get_username", return_value="dummy"),
        patch("clone_repo.verify.has_fork", return_value=True),
        patch("clone_repo.verify.is_parent_git_mastery", return_value=True),
        patch("clone_repo.verify.has_shapes_folder", return_value=False),
        pytest.raises(GitAutograderWrongAnswerException) as exception,
    ):
        verify(exercise)

        assert exception.value.message == [CLONE_MISSING]


def test_missing_origin_remote():
    with (
        loader.start_mock_exercise() as exercise,
        patch("clone_repo.verify.get_username", return_value="dummy"),
        patch("clone_repo.verify.has_fork", return_value=True),
        patch("clone_repo.verify.is_parent_git_mastery", return_value=True),
        patch("clone_repo.verify.has_shapes_folder", return_value=True),
        patch(
            "clone_repo.verify.remote",
            side_effect=lambda name: None if name == "origin" else object(),
        ),
        pytest.raises(GitAutograderWrongAnswerException) as exception,
    ):
        verify(exercise)

        assert exception.value.message == [ORIGIN_MISSING]


def test_wrong_origin_remote_url():
    fake_origin = type("FakeRemote", (), {"url": "https://github.com/wrong/repo.git"})()
    with (
        loader.start_mock_exercise() as exercise,
        patch("clone_repo.verify.get_username", return_value="dummy"),
        patch("clone_repo.verify.has_fork", return_value=True),
        patch("clone_repo.verify.is_parent_git_mastery", return_value=True),
        patch("clone_repo.verify.has_shapes_folder", return_value=True),
        patch(
            "clone_repo.verify.remote",
            side_effect=lambda name: fake_origin if name == "origin" else object(),
        ),
        pytest.raises(GitAutograderWrongAnswerException) as exception,
    ):
        verify(exercise)

        assert exception.value.message == [ORIGIN_WRONG]


def test_missing_upstream_remote():
    fake_origin = type(
        "FakeRemote", (), {"url": "https://github.com/dummy/gm-shapes.git"}
    )()
    with (
        loader.start_mock_exercise() as exercise,
        patch("clone_repo.verify.get_username", return_value="dummy"),
        patch("clone_repo.verify.has_fork", return_value=True),
        patch("clone_repo.verify.is_parent_git_mastery", return_value=True),
        patch("clone_repo.verify.has_shapes_folder", return_value=True),
        patch(
            "clone_repo.verify.remote",
            side_effect=lambda name: fake_origin if name == "origin" else None,
        ),
        pytest.raises(GitAutograderWrongAnswerException) as exception,
    ):
        verify(exercise)

        assert exception.value.message == [UPSTREAM_MISSING]


def test_wrong_upstream_remote_url():
    fake_origin = type(
        "FakeRemote", (), {"url": "https://github.com/dummy/gm-shapes.git"}
    )()
    fake_upstream = type(
        "FakeRemote", (), {"url": "https://github.com/wrong/repo.git"}
    )()
    with (
        loader.start_mock_exercise() as exercise,
        patch("clone_repo.verify.get_username", return_value="dummy"),
        patch("clone_repo.verify.has_fork", return_value=True),
        patch("clone_repo.verify.is_parent_git_mastery", return_value=True),
        patch("clone_repo.verify.has_shapes_folder", return_value=True),
        patch(
            "clone_repo.verify.remote",
            side_effect=lambda name: fake_origin if name == "origin" else fake_upstream,
        ),
        pytest.raises(GitAutograderWrongAnswerException) as exception,
    ):
        verify(exercise)

        assert exception.value.message == [UPSTREAM_WRONG]

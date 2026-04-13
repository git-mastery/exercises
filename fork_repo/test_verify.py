from unittest.mock import patch

import pytest
from exercise_utils.test import GitAutograderTestLoader, assert_output
from git_autograder import GitAutograderWrongAnswerException
from git_autograder.status import GitAutograderStatus

from .verify import IMPROPER_GH_CLI_SETUP, NO_FORK_FOUND, NOT_GIT_MASTERY_FORK, verify

REPOSITORY_NAME = "fork-repo"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)

# NOTE: This exercise is a special case where we do not require repo-smith. Instead,
# we directly mock function calls to verify that all branches are covered for us.


def test_pass():
    with (
        loader.start_mock_exercise() as exercise,
        patch("fork_repo.verify.get_username", return_value="dummy"),
        patch("fork_repo.verify.has_fork", return_value=True),
        patch("fork_repo.verify.is_parent_git_mastery", return_value=True),
    ):
        output = verify(exercise)
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_improper_gh_setup():
    with (
        loader.start_mock_exercise() as exercise,
        patch("fork_repo.verify.get_username", return_value=None),
        patch("fork_repo.verify.has_fork", return_value=True),
        patch("fork_repo.verify.is_parent_git_mastery", return_value=True),
        pytest.raises(GitAutograderWrongAnswerException) as exception,
    ):
        verify(exercise)

    assert exception.value.message == [IMPROPER_GH_CLI_SETUP]


def test_no_fork():
    with (
        loader.start_mock_exercise() as exercise,
        patch("fork_repo.verify.get_username", return_value="dummy"),
        patch("fork_repo.verify.has_fork", return_value=False),
        patch("fork_repo.verify.is_parent_git_mastery", return_value=True),
        pytest.raises(GitAutograderWrongAnswerException) as exception,
    ):
        verify(exercise)

    assert exception.value.message == [NO_FORK_FOUND]


def test_not_right_parent():
    with (
        loader.start_mock_exercise() as exercise,
        patch("fork_repo.verify.get_username", return_value="dummy"),
        patch("fork_repo.verify.has_fork", return_value=True),
        patch("fork_repo.verify.is_parent_git_mastery", return_value=False),
        pytest.raises(GitAutograderWrongAnswerException) as exception,
    ):
        verify(exercise)

    assert exception.value.message == [NOT_GIT_MASTERY_FORK]

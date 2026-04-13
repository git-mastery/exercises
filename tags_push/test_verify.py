from unittest.mock import patch

import pytest
from exercise_utils.test import GitAutograderTestLoader, assert_output
from git_autograder import GitAutograderStatus, GitAutograderWrongAnswerException

from .verify import (
    IMPROPER_GH_CLI_SETUP,
    TAG_1_MISSING,
    TAG_1_NAME,
    TAG_2_MISSING,
    TAG_2_NAME,
    TAG_DELETE_NAME,
    TAG_DELETE_NOT_REMOVED,
    verify,
)

REPOSITORY_NAME = "tags-push"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


# NOTE: This exercise is a special case where we do not require repo-smith. Instead,
# we directly mock function calls to verify that all branches are covered for us.


def test_pass():
    with (
        loader.start_mock_exercise() as exercise,
        patch("tags_push.verify.get_username", return_value="dummy"),
        patch(
            "tags_push.verify.get_remote_tags",
            return_value=[TAG_1_NAME, TAG_2_NAME],
        ),
    ):
        output = verify(exercise)
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_improper_gh_setup():
    with (
        loader.start_mock_exercise() as exercise,
        patch("tags_push.verify.get_username", return_value=None),
        patch(
            "tags_push.verify.get_remote_tags",
            return_value=[TAG_1_NAME, TAG_2_NAME],
        ),
        pytest.raises(GitAutograderWrongAnswerException) as exception,
    ):
        verify(exercise)

        assert exception.value.message == [IMPROPER_GH_CLI_SETUP]


def test_beta_present():
    with (
        loader.start_mock_exercise() as exercise,
        patch("tags_push.verify.get_username", return_value="dummy"),
        patch(
            "tags_push.verify.get_remote_tags",
            return_value=[TAG_1_NAME, TAG_2_NAME, TAG_DELETE_NAME],
        ),
        pytest.raises(GitAutograderWrongAnswerException) as exception,
    ):
        verify(exercise)

        assert exception.value.message == [TAG_DELETE_NOT_REMOVED]


def test_tag_1_absent():
    with (
        loader.start_mock_exercise() as exercise,
        patch("tags_push.verify.get_username", return_value="dummy"),
        patch("tags_push.verify.get_remote_tags", return_value=[TAG_2_NAME]),
        pytest.raises(GitAutograderWrongAnswerException) as exception,
    ):
        verify(exercise)

        assert exception.value.message == [TAG_1_MISSING]


def test_tag_2_absent():
    with (
        loader.start_mock_exercise() as exercise,
        patch("tags_push.verify.get_username", return_value="dummy"),
        patch("tags_push.verify.get_remote_tags", return_value=[TAG_1_NAME]),
        pytest.raises(GitAutograderWrongAnswerException) as exception,
    ):
        verify(exercise)

        assert exception.value.message == [TAG_2_MISSING]


def test_all_wrong():
    with (
        loader.start_mock_exercise() as exercise,
        patch("tags_push.verify.get_username", return_value="dummy"),
        patch("tags_push.verify.get_remote_tags", return_value=[TAG_DELETE_NAME]),
        pytest.raises(GitAutograderWrongAnswerException) as exception,
    ):
        verify(exercise)

    assert exception.value.message == [
        TAG_1_MISSING,
        TAG_2_MISSING,
        TAG_DELETE_NOT_REMOVED,
    ]

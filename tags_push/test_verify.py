import json
from pathlib import Path
from unittest.mock import patch

import pytest
from exercise_utils.test import GitAutograderTestLoader, assert_output
from git.repo import Repo
from git_autograder import (
    GitAutograderExercise,
    GitAutograderStatus,
    GitAutograderWrongAnswerException,
)

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


# TODO: The current tooling isn't mature enough to handle mock GitAutograderExercise in
# cases like these. We would ideally need some abstraction rather than creating our own.


@pytest.fixture
def exercise(tmp_path: Path) -> GitAutograderExercise:
    repo_dir = tmp_path / "ignore-me"
    repo_dir.mkdir()

    Repo.init(repo_dir)
    with open(tmp_path / ".gitmastery-exercise.json", "a") as config_file:
        config_file.write(
            json.dumps(
                {
                    "exercise_name": "tags-push",
                    "tags": [],
                    "requires_git": True,
                    "requires_github": True,
                    "base_files": {},
                    "exercise_repo": {
                        "repo_type": "local",
                        "repo_name": "ignore-me",
                        "init": True,
                        "create_fork": None,
                        "repo_title": None,
                    },
                    "downloaded_at": None,
                }
            )
        )

    exercise = GitAutograderExercise(exercise_path=tmp_path)
    return exercise


def test_pass(exercise: GitAutograderExercise):
    with (
        patch("tags_push.verify.get_username", return_value="dummy"),
        patch(
            "tags_push.verify.get_remote_tags", return_value=[TAG_1_NAME, TAG_2_NAME]
        ),
    ):
        output = verify(exercise)
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_improper_gh_setup(exercise: GitAutograderExercise):
    with (
        patch("tags_push.verify.get_username", return_value=None),
        patch(
            "tags_push.verify.get_remote_tags", return_value=[TAG_1_NAME, TAG_2_NAME]
        ),
        pytest.raises(GitAutograderWrongAnswerException, match=IMPROPER_GH_CLI_SETUP),
    ):
        verify(exercise)


def test_beta_present(exercise: GitAutograderExercise):
    with (
        patch("tags_push.verify.get_username", return_value="dummy"),
        patch(
            "tags_push.verify.get_remote_tags",
            return_value=[TAG_1_NAME, TAG_2_NAME, TAG_DELETE_NAME],
        ),
        pytest.raises(GitAutograderWrongAnswerException, match=TAG_DELETE_NOT_REMOVED),
    ):
        verify(exercise)


def test_tag_1_absent(exercise: GitAutograderExercise):
    with (
        patch("tags_push.verify.get_username", return_value="dummy"),
        patch("tags_push.verify.get_remote_tags", return_value=[TAG_2_NAME]),
        pytest.raises(GitAutograderWrongAnswerException, match=TAG_1_MISSING),
    ):
        verify(exercise)


def test_tag_2_absent(exercise: GitAutograderExercise):
    with (
        patch("tags_push.verify.get_username", return_value="dummy"),
        patch("tags_push.verify.get_remote_tags", return_value=[TAG_1_NAME]),
        pytest.raises(GitAutograderWrongAnswerException, match=TAG_2_MISSING),
    ):
        verify(exercise)


def test_all_wrong(exercise: GitAutograderExercise):
    with (
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

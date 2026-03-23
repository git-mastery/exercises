import json
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import PropertyMock, patch

import pytest
from exercise_utils.test import assert_output
from git.repo import Repo
from git_autograder import (
    GitAutograderExercise,
    GitAutograderStatus,
    GitAutograderWrongAnswerException,
)
from git_autograder.pr import GitAutograderPr

from .verify import (
    EXPECTED_CONTENT_STEP_3,
    JAVA_FILE_MISSING,
    JAVA_INVALID_CONTENT,
    PR_MISSING,
    WRONG_HEAD_BRANCH,
    verify,
)


@pytest.fixture
def exercise(tmp_path: Path) -> GitAutograderExercise:
    repo_dir = tmp_path / "ignore-me"
    repo_dir.mkdir()
    Repo.init(repo_dir)

    with open(tmp_path / ".gitmastery-exercise.json", "a") as config_file:
        config_file.write(
            json.dumps(
                {
                    "exercise_name": "create_pr_from_main",
                    "tags": [],
                    "requires_git": True,
                    "requires_github": True,
                    "base_files": {},
                    "exercise_repo": {
                        "repo_type": "local",
                        "repo_name": "ignore-me",
                        "init": True,
                        "create_fork": None,
                        "repo_title": "gm-shapes",
                        "pr_number": 1,
                        "pr_repo_full_name": "dummy/repo",
                    },
                    "downloaded_at": None,
                }
            )
        )

    with patch(
        "git_autograder.pr.fetch_pull_request_data",
        return_value={
            "title": "",
            "body": "",
            "state": "OPEN",
            "author": {"login": "dummy"},
            "baseRefName": "main",
            "headRefName": "main",
            "isDraft": False,
            "mergedAt": None,
            "mergedBy": None,
            "createdAt": None,
            "latestReviews": {"nodes": []},
            "comments": {"nodes": []},
            "commits": {"nodes": []},
        },
    ):
        return GitAutograderExercise(exercise_path=tmp_path)


class FakeCommit:
    def __init__(self, java_content: str | None) -> None:
        self._java_content = java_content

    @contextmanager
    def file(self, file_path: str):
        yield self._java_content


def _run_verify(
    exercise: GitAutograderExercise,
    pr_numbers: list[int] = [],
    head_branch: str = "",
    java_content: str | None = None,
):
    fake_commit = FakeCommit(java_content)
    with (
        patch("create_pr_from_main.verify.get_github_username", return_value="dummy"),
        patch(
            "create_pr_from_main.verify.get_pr_numbers_by_author",
            return_value=pr_numbers,
        ),
        patch("create_pr_from_main.verify.add_pr_config"),
        patch.object(exercise, "fetch_pr", return_value=None),
        patch.object(
            GitAutograderPr,
            "head_branch",
            new_callable=PropertyMock,
            return_value=head_branch,
        ),
        patch.object(
            GitAutograderPr,
            "last_user_commit",
            new_callable=PropertyMock,
            return_value=fake_commit,
        ),
    ):
        return verify(exercise)


def test_success(exercise: GitAutograderExercise):
    output = _run_verify(
        exercise,
        pr_numbers=[123],
        head_branch="main",
        java_content="\n".join(EXPECTED_CONTENT_STEP_3),
    )

    assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_pr_missing(exercise: GitAutograderExercise):
    with pytest.raises(GitAutograderWrongAnswerException) as exception:
        _run_verify(exercise)

    assert exception.value.message == [PR_MISSING]


def test_wrong_head_branch(exercise: GitAutograderExercise):
    with pytest.raises(GitAutograderWrongAnswerException) as exception:
        _run_verify(
            exercise,
            pr_numbers=[1],
            head_branch="feature/pr-branch"
        )

    assert exception.value.message == [WRONG_HEAD_BRANCH]


def test_java_file_missing(exercise: GitAutograderExercise):
    with pytest.raises(GitAutograderWrongAnswerException) as exception:
        _run_verify(
            exercise,
            pr_numbers=[1],
            head_branch="main",
            java_content=None,
        )

    assert exception.value.message == [JAVA_FILE_MISSING]


def test_java_content_invalid(exercise: GitAutograderExercise):
    with pytest.raises(GitAutograderWrongAnswerException) as exception:
        _run_verify(
            exercise,
            pr_numbers=[1],
            head_branch="main",
            java_content="wrong content\n",
        )

    assert exception.value.message == [JAVA_INVALID_CONTENT]

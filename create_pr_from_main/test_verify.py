from contextlib import contextmanager
from unittest.mock import PropertyMock, patch

import pytest
from exercise_utils.test import GitAutograderTestLoader, assert_output
from git_autograder import (
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

REPOSITORY_NAME = "create-pr-from-main"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)

# NOTE: This exercise is a special case where we do not require repo-smith. Instead,
# we directly mock function calls to verify that all branches are covered for us.


class FakeCommit:
    def __init__(self, java_content: str | None) -> None:
        self._java_content = java_content

    @contextmanager
    def file(self, file_path: str):
        yield self._java_content


def _run_verify(
    pr_numbers: list[int] = [],
    head_branch: str = "",
    java_content: str | None = None,
):
    fake_commit = FakeCommit(java_content)
    with loader.start_mock_exercise(
        has_pr_context=True, 
        pr_number=1, 
        pr_repo_full_name="dummy/repo"
    ) as exercise:
        with (
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


def test_success():
    output = _run_verify(
        pr_numbers=[123],
        head_branch="main",
        java_content="\n".join(EXPECTED_CONTENT_STEP_3),
    )

    assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_pr_missing():
    with pytest.raises(GitAutograderWrongAnswerException) as exception:
        _run_verify()

    assert exception.value.message == [PR_MISSING]


def test_wrong_head_branch():
    with pytest.raises(GitAutograderWrongAnswerException) as exception:
        _run_verify(
            pr_numbers=[1],
            head_branch="feature/pr-branch"
        )

    assert exception.value.message == [WRONG_HEAD_BRANCH]


def test_java_file_missing():
    with pytest.raises(GitAutograderWrongAnswerException) as exception:
        _run_verify(
            pr_numbers=[1],
            head_branch="main",
            java_content=None,
        )

    assert exception.value.message == [JAVA_FILE_MISSING]


def test_java_content_invalid():
    with pytest.raises(GitAutograderWrongAnswerException) as exception:
        _run_verify(
            pr_numbers=[1],
            head_branch="main",
            java_content="wrong content\n",
        )

    assert exception.value.message == [JAVA_INVALID_CONTENT]

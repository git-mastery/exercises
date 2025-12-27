from contextlib import contextmanager
from typing import Dict, Iterator, Optional, Tuple

from exercise_utils.test import (
    GitAutograderTest,
    GitAutograderTestLoader,
    GitMasteryHelper,
    assert_output,
)
from git_autograder import GitAutograderStatus
from git_autograder.answers.rules.has_exact_value_rule import HasExactValueRule
from repo_smith.repo_smith import RepoSmith

from .verify import NO_CHANGES_ERROR, QUESTION_ONE, QUESTION_TWO, verify

REPOSITORY_NAME = "branch-compare"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


@contextmanager
def base_setup(
    mock_answers: Optional[Dict[str, str]] = None,
) -> Iterator[Tuple[GitAutograderTest, RepoSmith]]:
    with loader.start(mock_answers=mock_answers) as (test, rs):
        rs.git.commit(message="Set initial state", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        rs.git.commit(message="Add empty data.txt", allow_empty=True)

        rs.git.checkout("stream-1", branch=True)
        rs.files.create_or_update("data.txt", "11111\n22222\n12345")
        rs.git.add(all=True)
        rs.git.commit(message="Add data to data.txt")

        rs.git.checkout("main")

        rs.git.checkout("stream-2", branch=True)
        rs.files.create_or_update("data.txt", "11111\n22222\n98765")
        rs.git.add(all=True)
        rs.git.commit(message="Add data to data.txt")

        rs.git.checkout("main")

        yield test, rs


def test_base():
    with base_setup(
        mock_answers={
            QUESTION_ONE: "12345",
            QUESTION_TWO: "98765",
        },
    ) as (test, _):
        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_wrong_stream1_diff():
    with base_setup(
        mock_answers={
            QUESTION_ONE: "99999",
            QUESTION_TWO: "98765",
        },
    ) as (test, _):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [HasExactValueRule.NOT_EXACT.format(question=QUESTION_ONE)],
        )


def test_wrong_stream2_diff():
    with base_setup(
        mock_answers={
            QUESTION_ONE: "12345",
            QUESTION_TWO: "99999",
        },
    ) as (test, _):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [HasExactValueRule.NOT_EXACT.format(question=QUESTION_TWO)],
        )


def test_changes_made_extra_commit():
    with base_setup() as (test, rs):
        rs.git.checkout("stream-1")
        rs.files.create_or_update("extra.txt", "extra content")
        rs.git.add(all=True)
        rs.git.commit(message="Extra change on stream-1")

        rs.git.checkout("main")

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [NO_CHANGES_ERROR])

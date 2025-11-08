from git_autograder import GitAutograderStatus, GitAutograderTestLoader, assert_output
from unittest.mock import patch
from git_autograder.answers.rules.has_exact_value_rule import HasExactValueRule

from ..verify import verify, QUESTION_ONE, QUESTION_TWO

REPOSITORY_NAME = "branch-compare"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_base():
    with (
        patch("branch_compare.verify.has_made_changes", return_value=False),
        patch("branch_compare.verify.get_stream1_diff", return_value="12345"),
        patch("branch_compare.verify.get_stream2_diff", return_value="98765"),
        loader.load(
            "specs/base.yml",
            "start",
            mock_answers={
                QUESTION_ONE: "12345",
                QUESTION_TWO: "98765",
            }
        ) as output,
    ):
        assert_output(output, GitAutograderStatus.SUCCESSFUL)

def test_wrong_stream1_diff():
    with (
        patch("branch_compare.verify.has_made_changes", return_value=False),
        patch("branch_compare.verify.get_stream1_diff", return_value="99999"),
        patch("branch_compare.verify.get_stream2_diff", return_value="98765"),
        loader.load(
            "specs/base.yml",
            "start",
            mock_answers={
                QUESTION_ONE: "12345",
                QUESTION_TWO: "98765",
            }
        ) as output,
    ):
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [HasExactValueRule.NOT_EXACT.format(question=QUESTION_ONE)],
        )

def test_wrong_stream2_diff():
    with (
        patch("branch_compare.verify.has_made_changes", return_value=False),
        patch("branch_compare.verify.get_stream1_diff", return_value="12345"),
        patch("branch_compare.verify.get_stream2_diff", return_value="99999"),
        loader.load(
            "specs/base.yml",
            "start",
            mock_answers={
                QUESTION_ONE: "12345",
                QUESTION_TWO: "98765",
            }
        ) as output,
    ):
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [HasExactValueRule.NOT_EXACT.format(question=QUESTION_TWO)],
        )

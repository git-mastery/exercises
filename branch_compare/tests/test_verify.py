from git_autograder import GitAutograderStatus, GitAutograderTestLoader, assert_output
from unittest.mock import patch

from ..verify import verify, QUESTION_ONE, QUESTION_TWO

REPOSITORY_NAME = "branch-compare"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_base():
    with (
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

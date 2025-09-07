from unittest.mock import patch
from git_autograder import GitAutograderStatus, GitAutograderTestLoader, assert_output
from git_autograder.answers.rules.has_exact_value_rule import HasExactValueRule

from ..verify import QUESTION_ONE, QUESTION_THREE, QUESTION_TWO, OneOfValueRule, verify

REPOSITORY_NAME = "log-and-order"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_base():
    with (
        patch("log_and_order.verify.get_head_sha", return_value="a" * 15),
        patch("log_and_order.verify.get_head_message", return_value="Hello world"),
        patch("log_and_order.verify.get_target_commit_sha", return_value="b" * 15),
        loader.load(
            "specs/base.yml",
            "start",
            mock_answers={
                QUESTION_ONE: "a" * 7,
                QUESTION_TWO: "Hello world",
                QUESTION_THREE: "b" * 7,
            },
        ) as output,
    ):
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_wrong_head_sha():
    with (
        patch("log_and_order.verify.get_head_sha", return_value="a" * 15),
        patch("log_and_order.verify.get_head_message", return_value="Hello world"),
        patch("log_and_order.verify.get_target_commit_sha", return_value="b" * 15),
        loader.load(
            "specs/base.yml",
            "start",
            mock_answers={
                QUESTION_ONE: "b" * 7,
                QUESTION_TWO: "Hello world",
                QUESTION_THREE: "b" * 7,
            },
        ) as output,
    ):
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [OneOfValueRule.MISMATCH_VALUE.format(question=QUESTION_ONE)],
        )


def test_wrong_head_message():
    with (
        patch("log_and_order.verify.get_head_sha", return_value="a" * 15),
        patch("log_and_order.verify.get_head_message", return_value="Hello world"),
        patch("log_and_order.verify.get_target_commit_sha", return_value="b" * 15),
        loader.load(
            "specs/base.yml",
            "start",
            mock_answers={
                QUESTION_ONE: "a" * 7,
                QUESTION_TWO: "Bye world",
                QUESTION_THREE: "b" * 7,
            },
        ) as output,
    ):
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [HasExactValueRule.NOT_EXACT.format(question=QUESTION_TWO)],
        )


def test_wrong_target_sha():
    with (
        patch("log_and_order.verify.get_head_sha", return_value="a" * 15),
        patch("log_and_order.verify.get_head_message", return_value="Hello world"),
        patch("log_and_order.verify.get_target_commit_sha", return_value="b" * 15),
        loader.load(
            "specs/base.yml",
            "start",
            mock_answers={
                QUESTION_ONE: "a" * 7,
                QUESTION_TWO: "Hello world",
                QUESTION_THREE: "a" * 7,
            },
        ) as output,
    ):
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [OneOfValueRule.MISMATCH_VALUE.format(question=QUESTION_THREE)],
        )

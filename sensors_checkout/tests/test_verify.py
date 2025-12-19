from git_autograder.answers.rules.not_empty_rule import NotEmptyRule
from git_autograder.answers.rules.has_exact_value_rule import HasExactValueRule
from git_autograder.status import GitAutograderStatus
from git_autograder.test_utils import assert_output
from git_autograder import GitAutograderTestLoader

from ..verify import (
    QUESTION_ONE,
    QUESTION_TWO,
    QUESTION_THREE,
    CORRECT_ANSWER_Q1,
    CORRECT_ANSWER_Q2,
    CORRECT_ANSWER_Q3,
    SUCCESS_MESSAGE,
    verify,
)

REPOSITORY_NAME = "sensors-checkout"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)

INCORRECT_ANSWER = "incorrect answer"


def test_correct_answers():
    with loader.load(
        "specs/base.yml",
        mock_answers={
            QUESTION_ONE: CORRECT_ANSWER_Q1,
            QUESTION_TWO: CORRECT_ANSWER_Q2,
            QUESTION_THREE: CORRECT_ANSWER_Q3,
        },
    ) as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL, [SUCCESS_MESSAGE])


def test_incomplete_answers():
    with loader.load(
        "specs/base.yml",
        mock_answers={
            QUESTION_ONE: CORRECT_ANSWER_Q1,
            QUESTION_TWO: CORRECT_ANSWER_Q2,
            QUESTION_THREE: "",
        },
    ) as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                NotEmptyRule.EMPTY.format(question=QUESTION_THREE),
            ],
        )


def test_no_answers():
    with loader.load(
        "specs/base.yml",
        mock_answers={
            QUESTION_ONE: "",
            QUESTION_TWO: "",
            QUESTION_THREE: "",
        },
    ) as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                NotEmptyRule.EMPTY.format(question=QUESTION_ONE),
                NotEmptyRule.EMPTY.format(question=QUESTION_TWO),
                NotEmptyRule.EMPTY.format(question=QUESTION_THREE),
            ],
        )


def test_incorrect_q1():
    with loader.load(
        "specs/base.yml",
        mock_answers={
            QUESTION_ONE: INCORRECT_ANSWER,
            QUESTION_TWO: CORRECT_ANSWER_Q2,
            QUESTION_THREE: CORRECT_ANSWER_Q3,
        },
    ) as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [HasExactValueRule.NOT_EXACT.format(question=QUESTION_ONE)],
        )


def test_incorrect_q2():
    with loader.load(
        "specs/base.yml",
        mock_answers={
            QUESTION_ONE: CORRECT_ANSWER_Q1,
            QUESTION_TWO: INCORRECT_ANSWER,
            QUESTION_THREE: CORRECT_ANSWER_Q3,
        },
    ) as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [HasExactValueRule.NOT_EXACT.format(question=QUESTION_TWO)],
        )


def test_incorrect_q3():
    with loader.load(
        "specs/base.yml",
        mock_answers={
            QUESTION_ONE: CORRECT_ANSWER_Q1,
            QUESTION_TWO: CORRECT_ANSWER_Q2,
            QUESTION_THREE: INCORRECT_ANSWER,
        },
    ) as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [HasExactValueRule.NOT_EXACT.format(question=QUESTION_THREE)],
        )

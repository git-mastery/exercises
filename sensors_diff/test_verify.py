from exercise_utils.test import GitAutograderTestLoader, assert_output
from git_autograder.answers.rules import (
    HasExactListRule,
    HasExactValueRule,
    NotEmptyRule,
)
from git_autograder.status import GitAutograderStatus

from .verify import (
    QUESTION_FOUR,
    QUESTION_ONE,
    QUESTION_THREE,
    QUESTION_TWO,
    SUCCESS_MESSAGE,
    verify,
)

REPOSITORY_NAME = "sensors-diff"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)

CORRECT_QUESTION_ONE_ANSWER = "7590"
CORRECT_QUESTION_TWO_ANSWER = """
- 3642
- 4531
"""
CORRECT_QUESTION_TWO_ANSWER_DIFFERENT_ORDER = """
- 4531
- 3642
"""
INCORRECT_QUESTION_TWO_MISSING_VALUE = """
- 4531
"""
CORRECT_QUESTION_THREE_ANSWER = """
- south.csv
- north.csv
- west.csv
"""
CORRECT_QUESTION_FOUR_ANSWER = "3471"
INCORRECT_ANSWER = "incorrect answer"


def test_valid_answers():
    with loader.start(
        mock_answers={
            QUESTION_ONE: CORRECT_QUESTION_ONE_ANSWER,
            QUESTION_TWO: CORRECT_QUESTION_TWO_ANSWER,
            QUESTION_THREE: CORRECT_QUESTION_THREE_ANSWER,
            QUESTION_FOUR: CORRECT_QUESTION_FOUR_ANSWER,
        },
    ) as (test, _):
        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL, [SUCCESS_MESSAGE])


def test_valid_answers_different_order():
    with loader.start(
        mock_answers={
            QUESTION_ONE: CORRECT_QUESTION_ONE_ANSWER,
            QUESTION_TWO: CORRECT_QUESTION_TWO_ANSWER_DIFFERENT_ORDER,
            QUESTION_THREE: CORRECT_QUESTION_THREE_ANSWER,
            QUESTION_FOUR: CORRECT_QUESTION_FOUR_ANSWER,
        },
    ) as (test, _):
        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL, [SUCCESS_MESSAGE])


def test_no_answers():
    with loader.start(
        mock_answers={
            QUESTION_ONE: "",
            QUESTION_TWO: "",
            QUESTION_THREE: "",
            QUESTION_FOUR: "",
        },
    ) as (test, _):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                NotEmptyRule.EMPTY.format(question=QUESTION_ONE),
                NotEmptyRule.EMPTY.format(question=QUESTION_TWO),
                NotEmptyRule.EMPTY.format(question=QUESTION_THREE),
                NotEmptyRule.EMPTY.format(question=QUESTION_FOUR),
            ],
        )


def test_incomplete_answers():
    with loader.start(
        mock_answers={
            QUESTION_ONE: CORRECT_QUESTION_ONE_ANSWER,
            QUESTION_TWO: "",
            QUESTION_THREE: "",
            QUESTION_FOUR: "",
        },
    ) as (test, _):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                NotEmptyRule.EMPTY.format(question=QUESTION_TWO),
                NotEmptyRule.EMPTY.format(question=QUESTION_THREE),
                NotEmptyRule.EMPTY.format(question=QUESTION_FOUR),
            ],
        )


def test_incorrect_question_one_answer():
    with loader.start(
        mock_answers={
            QUESTION_ONE: INCORRECT_ANSWER,
            QUESTION_TWO: CORRECT_QUESTION_TWO_ANSWER,
            QUESTION_THREE: CORRECT_QUESTION_THREE_ANSWER,
            QUESTION_FOUR: CORRECT_QUESTION_FOUR_ANSWER,
        },
    ) as (test, _):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                HasExactValueRule.NOT_EXACT.format(question=QUESTION_ONE),
            ],
        )


def test_incorrect_question_two_answer():
    with loader.start(
        mock_answers={
            QUESTION_ONE: CORRECT_QUESTION_ONE_ANSWER,
            QUESTION_TWO: INCORRECT_ANSWER,
            QUESTION_THREE: CORRECT_QUESTION_THREE_ANSWER,
            QUESTION_FOUR: CORRECT_QUESTION_FOUR_ANSWER,
        },
    ) as (test, _):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                HasExactListRule.INCORRECT_UNORDERED.format(question=QUESTION_TWO),
            ],
        )


def test_incorrect_question_two_answer_missing_value():
    with loader.start(
        mock_answers={
            QUESTION_ONE: CORRECT_QUESTION_ONE_ANSWER,
            QUESTION_TWO: INCORRECT_QUESTION_TWO_MISSING_VALUE,
            QUESTION_THREE: CORRECT_QUESTION_THREE_ANSWER,
            QUESTION_FOUR: CORRECT_QUESTION_FOUR_ANSWER,
        },
    ) as (test, _):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                HasExactListRule.INCORRECT_UNORDERED.format(question=QUESTION_TWO),
            ],
        )


def test_incorrect_question_three_answer():
    with loader.start(
        mock_answers={
            QUESTION_ONE: CORRECT_QUESTION_ONE_ANSWER,
            QUESTION_TWO: CORRECT_QUESTION_TWO_ANSWER,
            QUESTION_THREE: INCORRECT_ANSWER,
            QUESTION_FOUR: CORRECT_QUESTION_FOUR_ANSWER,
        },
    ) as (test, _):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                HasExactListRule.INCORRECT_UNORDERED.format(question=QUESTION_THREE),
            ],
        )


def test_incorrect_question_four_answer():
    with loader.start(
        mock_answers={
            QUESTION_ONE: CORRECT_QUESTION_ONE_ANSWER,
            QUESTION_TWO: CORRECT_QUESTION_TWO_ANSWER,
            QUESTION_THREE: CORRECT_QUESTION_THREE_ANSWER,
            QUESTION_FOUR: INCORRECT_ANSWER,
        },
    ) as (test, _):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                HasExactValueRule.NOT_EXACT.format(question=QUESTION_FOUR),
            ],
        )

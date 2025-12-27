from exercise_utils.test import GitAutograderTestLoader, assert_output
from git_autograder import GitAutograderStatus
from git_autograder.answers.rules import (
    ContainsListRule,
    HasExactListRule,
    HasExactValueRule,
    NotEmptyRule,
)

from .verify import QUESTION_FOUR, QUESTION_ONE, QUESTION_THREE, QUESTION_TWO, verify

REPOSITORY_NAME = "view-commits"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)

CORRECT_QUESTION_ONE = "Eric"
CORRECT_QUESTION_TWO = "Bruce"
CORRECT_QUESTION_THREE = """
- Beth
- Betsy
- Daisy
"""
CORRECT_QUESTION_FOUR = "- Charlie"

WRONG_QUESTION_ONE = "Ergodic"
WRONG_QUESTION_TWO = "Bru"
INCOMPLETE_QUESTION_THREE = """
- Betsy
- Daisy
"""
WRONG_QUESTION_THREE = """
- Betsy
- Bruce
- Daisy
"""
EXTRA_QUESTION_THREE = """
- Betsy
- Beth
- Eric
- Daisy
"""
WRONG_QUESTION_FOUR = "- Dave"


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


def test_incomplete_answer():
    with loader.start(
        mock_answers={
            QUESTION_ONE: CORRECT_QUESTION_ONE,
            QUESTION_TWO: CORRECT_QUESTION_TWO,
            QUESTION_THREE: "",
            QUESTION_FOUR: "",
        },
    ) as (test, _):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                NotEmptyRule.EMPTY.format(question=QUESTION_THREE),
                NotEmptyRule.EMPTY.format(question=QUESTION_FOUR),
            ],
        )


def test_wrong_question_one():
    with loader.start(
        mock_answers={
            QUESTION_ONE: WRONG_QUESTION_ONE,
            QUESTION_TWO: CORRECT_QUESTION_TWO,
            QUESTION_THREE: CORRECT_QUESTION_THREE,
            QUESTION_FOUR: CORRECT_QUESTION_FOUR,
        },
    ) as (test, _):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [HasExactValueRule.NOT_EXACT.format(question=QUESTION_ONE)],
        )


def test_wrong_question_two():
    with loader.start(
        mock_answers={
            QUESTION_ONE: CORRECT_QUESTION_ONE,
            QUESTION_TWO: WRONG_QUESTION_TWO,
            QUESTION_THREE: CORRECT_QUESTION_THREE,
            QUESTION_FOUR: CORRECT_QUESTION_FOUR,
        },
    ) as (test, _):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [HasExactValueRule.NOT_EXACT.format(question=QUESTION_TWO)],
        )


def test_incomplete_question_three():
    with loader.start(
        mock_answers={
            QUESTION_ONE: CORRECT_QUESTION_ONE,
            QUESTION_TWO: CORRECT_QUESTION_TWO,
            QUESTION_THREE: INCOMPLETE_QUESTION_THREE,
            QUESTION_FOUR: CORRECT_QUESTION_FOUR,
        },
    ) as (test, _):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [HasExactListRule.INCORRECT_UNORDERED.format(question=QUESTION_THREE)],
        )


def test_wrong_question_three():
    with loader.start(
        mock_answers={
            QUESTION_ONE: CORRECT_QUESTION_ONE,
            QUESTION_TWO: CORRECT_QUESTION_TWO,
            QUESTION_THREE: WRONG_QUESTION_THREE,
            QUESTION_FOUR: CORRECT_QUESTION_FOUR,
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


def test_wrong_question_three_extra_answer():
    with loader.start(
        mock_answers={
            QUESTION_ONE: CORRECT_QUESTION_ONE,
            QUESTION_TWO: CORRECT_QUESTION_TWO,
            QUESTION_THREE: EXTRA_QUESTION_THREE,
            QUESTION_FOUR: CORRECT_QUESTION_FOUR,
        },
    ) as (test, _):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [ContainsListRule.INVALID_ITEM.format(question=QUESTION_THREE)],
        )


def test_valid_answers():
    with loader.start(
        mock_answers={
            QUESTION_ONE: CORRECT_QUESTION_ONE,
            QUESTION_TWO: CORRECT_QUESTION_TWO,
            QUESTION_THREE: CORRECT_QUESTION_THREE,
            QUESTION_FOUR: CORRECT_QUESTION_FOUR,
        },
    ) as (test, _):
        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)

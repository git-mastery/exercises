from exercise_utils.test import GitAutograderTestLoader, assert_output
from git_autograder import GitAutograderStatus
from git_autograder.answers.rules import HasExactValueRule, NotEmptyRule

from .verify import QUESTION_ONE, QUESTION_TWO, verify

REPOSITORY_NAME = "amateur-detective"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


def test_no_answers():
    with loader.start(mock_answers={QUESTION_ONE: "", QUESTION_TWO: ""}) as (test, _):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                NotEmptyRule.EMPTY.format(question=QUESTION_ONE),
                NotEmptyRule.EMPTY.format(question=QUESTION_TWO),
            ],
        )


def test_one_answer():
    with loader.start(
        mock_answers={QUESTION_ONE: "file77.txt", QUESTION_TWO: ""},
    ) as (test, _):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                NotEmptyRule.EMPTY.format(question=QUESTION_TWO),
            ],
        )


def test_mixed_answers():
    with loader.start(
        mock_answers={QUESTION_ONE: "file75.txt", QUESTION_TWO: ""},
    ) as (test, _):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                NotEmptyRule.EMPTY.format(question=QUESTION_TWO),
                HasExactValueRule.NOT_EXACT.format(question=QUESTION_ONE),
            ],
        )


def test_valid_answers():
    with loader.start(
        mock_answers={QUESTION_ONE: "file77.txt", QUESTION_TWO: "file14.txt"},
    ) as (test, _):
        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)

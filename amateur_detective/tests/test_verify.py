from git_autograder import GitAutograderStatus, GitAutograderTestLoader, assert_output
from git_autograder.answers.rules import HasExactValueRule, NotEmptyRule

from ..verify import QUESTION_ONE, QUESTION_TWO, verify

REPOSITORY_NAME = "amateur-detective"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_no_answers():
    with loader.load(
        "specs/no_answers.yml", mock_answers={QUESTION_ONE: "", QUESTION_TWO: ""}
    ) as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                NotEmptyRule.EMPTY.format(question=QUESTION_ONE),
                NotEmptyRule.EMPTY.format(question=QUESTION_TWO),
            ],
        )


def test_one_answer():
    with loader.load(
        "specs/partial_answer.yml",
        mock_answers={QUESTION_ONE: "file77.txt", QUESTION_TWO: ""},
    ) as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                NotEmptyRule.EMPTY.format(question=QUESTION_TWO),
            ],
        )


def test_mixed_answers():
    with loader.load(
        "specs/mixed_answer.yml",
        mock_answers={QUESTION_ONE: "file75.txt", QUESTION_TWO: ""},
    ) as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                NotEmptyRule.EMPTY.format(question=QUESTION_TWO),
                HasExactValueRule.NOT_EXACT.format(question=QUESTION_ONE),
            ],
        )


def test_valid_answers():
    with loader.load(
        "specs/valid_answers.yml",
        mock_answers={QUESTION_ONE: "file77.txt", QUESTION_TWO: "file14.txt"},
    ) as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL)

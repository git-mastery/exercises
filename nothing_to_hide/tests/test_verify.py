from git_autograder import (
    GitAutograderStatus,
    GitAutograderTestLoader,
    assert_output,
)
from git_autograder.answers.rules import HasExactListRule, HasExactValueRule

from ..verify import (
    QUESTION_FOUR,
    QUESTION_ONE,
    QUESTION_THREE,
    QUESTION_TWO,
    verify,
)

REPOSITORY_NAME = "nothing-to-hide"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_correct():
    with loader.load("specs/valid_answers.yml", "start") as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_incomplete_hidden_files():
    with loader.load("specs/incomplete_hidden_files.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [HasExactListRule.INCORRECT_UNORDERED.format(question=QUESTION_ONE)],
        )


def test_wrong_question_two():
    with loader.load("specs/wrong_question_two.yml", "start") as output:
        print(output.comments)
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [HasExactValueRule.NOT_EXACT.format(question=QUESTION_TWO)],
        )


def test_wrong_question_three():
    with loader.load("specs/wrong_question_three.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [HasExactValueRule.NOT_EXACT.format(question=QUESTION_THREE)],
        )


def test_wrong_question_four():
    with loader.load("specs/wrong_question_four.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [HasExactValueRule.NOT_EXACT.format(question=QUESTION_FOUR)],
        )

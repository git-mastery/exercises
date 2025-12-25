from exercise_utils.test import (
    GitAutograderTestLoader,
    assert_output,
)
from git_autograder import GitAutograderStatus
from git_autograder.answers.rules import HasExactListRule, HasExactValueRule

from .verify import (
    QUESTION_FOUR,
    QUESTION_ONE,
    QUESTION_THREE,
    QUESTION_TWO,
    verify,
)

REPOSITORY_NAME = "nothing-to-hide"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)

QUESTION_ONE_ANSWER = """
- res/hidden.png
- sensitive/sensitive_1.txt
- sensitive/sensitive_2.txt
- sensitive/sensitive_3.txt
- sensitive/sensitive_4.txt
- sensitive/sensitive_5.txt
- src/.env
"""

INCOMPLETE_QUESTION_ONE_ANSWER = """
- res/hidden.png
- sensitive/sensitive_1.txt
- sensitive/sensitive_2.txt
- sensitive/sensitive_5.txt
- src/.env
"""


def test_correct():
    with loader.start(
        mock_answers={
            QUESTION_ONE: QUESTION_ONE_ANSWER,
            QUESTION_TWO: ".gitignore",
            QUESTION_THREE: "sensitive/*",
            QUESTION_FOUR: "!sensitive/names.txt",
        },
    ) as (test, _):
        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_incomplete_hidden_files():
    with loader.start(
        mock_answers={
            QUESTION_ONE: INCOMPLETE_QUESTION_ONE_ANSWER,
            QUESTION_TWO: ".gitignore",
            QUESTION_THREE: "sensitive/*",
            QUESTION_FOUR: "!sensitive/names.txt",
        },
    ) as (test, _):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [HasExactListRule.INCORRECT_UNORDERED.format(question=QUESTION_ONE)],
        )


def test_wrong_question_two():
    with loader.start(
        mock_answers={
            QUESTION_ONE: QUESTION_ONE_ANSWER,
            QUESTION_TWO: "src/script.py",
            QUESTION_THREE: "sensitive/*",
            QUESTION_FOUR: "!sensitive/names.txt",
        },
    ) as (test, _):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [HasExactValueRule.NOT_EXACT.format(question=QUESTION_TWO)],
        )


def test_wrong_question_three():
    with loader.start(
        mock_answers={
            QUESTION_ONE: QUESTION_ONE_ANSWER,
            QUESTION_TWO: ".gitignore",
            QUESTION_THREE: "src/",
            QUESTION_FOUR: "!sensitive/names.txt",
        },
    ) as (test, _):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [HasExactValueRule.NOT_EXACT.format(question=QUESTION_THREE)],
        )


def test_wrong_question_four():
    with loader.start(
        mock_answers={
            QUESTION_ONE: QUESTION_ONE_ANSWER,
            QUESTION_TWO: ".gitignore",
            QUESTION_THREE: "sensitive/*",
            QUESTION_FOUR: "src",
        },
    ) as (test, _):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [HasExactValueRule.NOT_EXACT.format(question=QUESTION_FOUR)],
        )

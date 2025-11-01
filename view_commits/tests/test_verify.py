from git_autograder import GitAutograderStatus, GitAutograderTestLoader, assert_output
from git_autograder.answers.rules import HasExactValueRule, HasExactListRule, NotEmptyRule, ContainsListRule
from ..verify import QUESTION_ONE, QUESTION_TWO, QUESTION_THREE, QUESTION_FOUR, verify

REPOSITORY_NAME = "view-commits"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)

CORRECT_QUESTION_THREE = """
- Betsy
- Beth
- Daisy
"""

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

def test_no_answers():
    with loader.load(
        "specs/no_answers.yml",
        mock_answers={
            QUESTION_ONE: "",
            QUESTION_TWO: "",
            QUESTION_THREE: "",
            QUESTION_FOUR: ""
        },
    ) as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                NotEmptyRule.EMPTY.format(question=QUESTION_ONE),
                NotEmptyRule.EMPTY.format(question=QUESTION_TWO),
                NotEmptyRule.EMPTY.format(question=QUESTION_THREE),
                NotEmptyRule.EMPTY.format(question=QUESTION_FOUR)
            ],
        )

def test_incomplete_answer():
    with loader.load(
        "specs/incomplete_answers.yml",
        mock_answers={
            QUESTION_ONE: "Eric",
            QUESTION_TWO: "Bruce",
            QUESTION_THREE: "",
            QUESTION_FOUR: ""
        },
    ) as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                NotEmptyRule.EMPTY.format(question=QUESTION_THREE),
                NotEmptyRule.EMPTY.format(question=QUESTION_FOUR)
            ],
        )

def test_wrong_question_one():
    with loader.load(
        "specs/wrong_question_one.yml",
        mock_answers={
            QUESTION_ONE: "Ergodic",
            QUESTION_TWO: "Bruce",
            QUESTION_THREE: CORRECT_QUESTION_THREE,
            QUESTION_FOUR: "- Charlie"
        },
    ) as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                HasExactValueRule.NOT_EXACT.format(question=QUESTION_ONE)
            ],
        )

def test_wrong_question_two():
    with loader.load(
        "specs/wrong_question_two.yml",
        mock_answers={
            QUESTION_ONE: "Eric",
            QUESTION_TWO: "Bru",
            QUESTION_THREE: CORRECT_QUESTION_THREE,
            QUESTION_FOUR: "- Charlie"
        },
    ) as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                HasExactValueRule.NOT_EXACT.format(question=QUESTION_TWO)
            ],
        )

def test_incomplete_question_three():
    with loader.load(
        "specs/incomplete_question_three.yml",
        mock_answers={
            QUESTION_ONE: "Eric",
            QUESTION_TWO: "Bruce",
            QUESTION_THREE: INCOMPLETE_QUESTION_THREE,
            QUESTION_FOUR: "- Charlie"
        },
    ) as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                HasExactListRule.INCORRECT_UNORDERED.format(question=QUESTION_THREE)
            ],
        )

def test_wrong_question_three():
    with loader.load(
        "specs/wrong_question_three.yml",
        mock_answers={
            QUESTION_ONE: "Eric",
            QUESTION_TWO: "Bruce",
            QUESTION_THREE: WRONG_QUESTION_THREE,
            QUESTION_FOUR: "- Charlie"
        },
    ) as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                HasExactListRule.INCORRECT_UNORDERED.format(question=QUESTION_THREE),
            ],
        )

def test_wrong_question_three_extra_answer():
    with loader.load(
        "specs/extra_question_three.yml",
        mock_answers={
            QUESTION_ONE: "Eric",
            QUESTION_TWO: "Bruce",
            QUESTION_THREE: EXTRA_QUESTION_THREE,
            QUESTION_FOUR: "- Charlie"
        },
    ) as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                ContainsListRule.INVALID_ITEM.format(question=QUESTION_THREE)
            ],
        )

def test_valid_answers():
    with loader.load(
        "specs/valid_answers.yml",
        mock_answers={
            QUESTION_ONE: "Eric",
            QUESTION_TWO: "Bruce",
            QUESTION_THREE: CORRECT_QUESTION_THREE,
            QUESTION_FOUR:"- Charlie"
        },
    ) as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL)
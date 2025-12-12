from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)
from git_autograder.answers.rules import (
    HasExactValueRule,
    NotEmptyRule,
)

QUESTION_ONE = "What's sum of values in south.csv on Jan 11th?"
QUESTION_TWO = "What's sum of values in west.csv on Jan 09th?"
QUESTION_THREE = "What's sum of values in north.csv on Jan 05th?"
SUCCESS_MESSAGE = "Great work traversing the revision history!"

CORRECT_ANSWER_Q1 = "110295"
CORRECT_ANSWER_Q2 = "111175"
CORRECT_ANSWER_Q3 = "113705"


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    # TODO: use reflog to verify that the student traversed the revision history
    (
        exercise.answers.add_validation(
            QUESTION_ONE,
            NotEmptyRule(),
            HasExactValueRule(CORRECT_ANSWER_Q1, is_case_sensitive=True),
        )
        .add_validation(
            QUESTION_TWO,
            NotEmptyRule(),
            HasExactValueRule(CORRECT_ANSWER_Q2, is_case_sensitive=True),
        )
        .add_validation(
            QUESTION_THREE,
            NotEmptyRule(),
            HasExactValueRule(CORRECT_ANSWER_Q3, is_case_sensitive=True),
        )
        .validate()
    )

    return exercise.to_output([SUCCESS_MESSAGE], GitAutograderStatus.SUCCESSFUL)

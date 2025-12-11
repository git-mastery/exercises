from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)
from git_autograder.answers.rules import (
    HasExactValueRule,
    NotEmptyRule,
    HasExactListRule,
)

QUESTION_ONE = "Which are the new values in staged files?"
QUESTION_TWO = "Which are the new values in modified but unstaged files?"
QUESTION_THREE = "Which files have changed from Jan 09th to Jan 15th?"
QUESTION_FOUR = (
    "Which new values are new in north.csv on Jan 10th, compared to Jan 01st?"
)
SUCCESS_MESSAGE = "Great work comparing commits in git history!"


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    (
        exercise.answers.add_validation(QUESTION_ONE, NotEmptyRule())
        .add_validation(QUESTION_ONE, HasExactValueRule("7590", is_case_sensitive=True))
        .add_validation(
            QUESTION_TWO,
            NotEmptyRule(),
            HasExactListRule(["4531", "3642"], is_case_sensitive=True),
        )
        .add_validation(
            QUESTION_THREE,
            NotEmptyRule(),
            HasExactListRule(
                ["north.csv", "south.csv", "west.csv"], is_case_sensitive=True
            ),
        )
        .add_validation(
            QUESTION_FOUR,
            NotEmptyRule(),
            HasExactValueRule("3471", is_case_sensitive=True),
        )
        .validate()
    )

    return exercise.to_output(
        [SUCCESS_MESSAGE],
        GitAutograderStatus.SUCCESSFUL,
    )

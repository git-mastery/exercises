from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)
from git_autograder.answers.rules import (
    HasExactValueRule,
    NotEmptyRule,
    HasExactListRule,
    ContainsListRule,
)

QUESTION_ONE = "In February, who was replaced in the Wednesday duty roster?"
QUESTION_TWO = "In February, who joined the Tuesday duty roster?"
QUESTION_THREE = "In April, what were the new names added to the duty rosters? Remove/add extra rows where appropriate."
QUESTION_FOUR = "In January, who were in the Tuesday duty roster? Remove/add extra rows where appropriate."


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    (
        exercise.answers.add_validation(QUESTION_ONE, NotEmptyRule())
        .add_validation(QUESTION_ONE, HasExactValueRule("Eric", is_case_sensitive=True))
        .add_validation(
            QUESTION_TWO,
            NotEmptyRule(),
            HasExactValueRule("Bruce", is_case_sensitive=True),
        )
        .add_validation(
            QUESTION_THREE,
            NotEmptyRule(),
            HasExactListRule(["Betsy", "Beth", "Daisy"], is_case_sensitive=True),
            ContainsListRule(
                ["Betsy", "Beth", "Daisy"], subset=True, is_case_sensitive=True
            ),
        )
        .add_validation(
            QUESTION_FOUR,
            NotEmptyRule(),
            HasExactListRule(["Charlie"], is_case_sensitive=True),
            ContainsListRule(["Charlie"], subset=True, is_case_sensitive=True),
        )
        .validate()
    )

    return exercise.to_output(
        ["Great work in viewing and understanding the diff of a specific commit!"],
        GitAutograderStatus.SUCCESSFUL,
    )

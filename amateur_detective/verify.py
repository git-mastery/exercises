from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)
from git_autograder.answers.rules import HasExactValueRule, NotEmptyRule

QUESTION_ONE = "Which file was added?"
QUESTION_TWO = "Which file was edited?"


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    (
        exercise.answers.add_validation(QUESTION_ONE, NotEmptyRule())
        .add_validation(QUESTION_ONE, HasExactValueRule("file77.txt"))
        .add_validation(QUESTION_TWO, NotEmptyRule())
        .add_validation(QUESTION_TWO, HasExactValueRule("file14.txt"))
        .validate()
    )

    return exercise.to_output(
        ["Congratulations on cracking the case! You found the hacker!"],
        GitAutograderStatus.SUCCESSFUL,
    )

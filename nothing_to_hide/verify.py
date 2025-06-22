from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)
from git_autograder.answers.rules import (
    HasExactListRule,
    HasExactValueRule,
    NotEmptyRule,
)

QUESTION_ONE = "What files are missing from Git, but found on your local repository?"
QUESTION_TWO = "What is responsible for the hidden files?"
QUESTION_THREE = "What is the general pattern used to hide the sensitive/ folder?"
QUESTION_FOUR = "What is the pattern used to only show sensitive/names.txt?"


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    (
        exercise.answers.add_validation(
            QUESTION_ONE,
            NotEmptyRule(),
            HasExactListRule(
                [
                    "res/hidden.png",
                    "sensitive/sensitive_1.txt",
                    "sensitive/sensitive_2.txt",
                    "sensitive/sensitive_3.txt",
                    "sensitive/sensitive_4.txt",
                    "sensitive/sensitive_5.txt",
                    "src/.env",
                ],
                is_case_sensitive=True,
            ),
        )
        .add_validation(
            QUESTION_TWO,
            NotEmptyRule(),
            HasExactValueRule(".gitignore", is_case_sensitive=True),
        )
        .add_validation(
            QUESTION_THREE,
            NotEmptyRule(),
            HasExactValueRule("sensitive/*", is_case_sensitive=True),
        )
        .add_validation(
            QUESTION_FOUR,
            NotEmptyRule(),
            HasExactValueRule("!sensitive/names.txt", is_case_sensitive=True),
        )
        .validate()
    )

    return exercise.to_output(
        ["Great work in identifying how .gitignore works!"],
        GitAutograderStatus.SUCCESSFUL,
    )

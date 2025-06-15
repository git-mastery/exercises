from git_autograder import GitAutograderOutput, GitAutograderRepo, GitAutograderStatus
from git_autograder.answers.rules import HasExactValueRule, NotEmptyRule

QUESTION_ONE = "Which file was added?"
QUESTION_TWO = "Which file was edited?"


def verify(repo: GitAutograderRepo) -> GitAutograderOutput:
    (
        repo.answers.add_validation(QUESTION_ONE, NotEmptyRule())
        .add_validation(QUESTION_ONE, HasExactValueRule("file77.txt"))
        .add_validation(QUESTION_TWO, NotEmptyRule())
        .add_validation(QUESTION_TWO, HasExactValueRule("file14.txt"))
        .validate()
    )

    return repo.to_output(
        ["Congratulations on cracking the case! You found the hacker!"],
        status=GitAutograderStatus.SUCCESSFUL,
    )

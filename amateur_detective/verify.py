from git_autograder import GitAutograderOutput, GitAutograderRepo
from git_autograder.answers.rules import HasExactValueRule, NotEmptyRule

QUESTION_ONE = "Which file was added?"
QUESTION_TWO = "Which file was edited?"


def verify(repo: GitAutograderRepo) -> GitAutograderOutput:
    repo.answers.validate_question(
        QUESTION_ONE,
        [
            NotEmptyRule(),
            HasExactValueRule("file77.txt"),
        ],
    ).validate_question(QUESTION_TWO, [NotEmptyRule(), HasExactValueRule("file14.txt")])

    return repo.to_output([])

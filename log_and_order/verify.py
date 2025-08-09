from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)
from git_autograder.answers.rules import NotEmptyRule, HasExactValueRule
from git_autograder.answers.rules.answer_rule import AnswerRule
from git_autograder.answers import GitAutograderAnswersRecord

QUESTION_ONE = "Where is the criminal currently hiding at? (What is the location in commit where HEAD is pointing to?)"
QUESTION_TWO = "When did the criminal rob Alice Bakersfield? (Find the date of the commit whose description details the robbery)"
QUESTION_THREE = 'What is the criminal\'s real name? (Find the one commit where the author is not "Anonymous")'
QUESTION_FOUR = "What did the criminal do on 13 September 2024? (What is the description of the commit on 13 September 2024?)"
QUESTION_FIVE = "What was the very first crime the criminal committed? (What is the message of the very first commit?)"


class ContainsValueRule(AnswerRule):
    MISSING_VALUE = "Answer for {question} missing the right values"

    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def apply(self, answer: GitAutograderAnswersRecord) -> None:
        if self.value not in answer.answer.strip().lower():
            raise Exception(self.MISSING_VALUE.format(question=answer.question))


class ContainsOneOfValueRule(AnswerRule):
    MISMATCH_VALUE = "Answer for {question} did not contain the right value"

    def __init__(self, *values: str) -> None:
        super().__init__()
        self.values = values

    def apply(self, answer: GitAutograderAnswersRecord) -> None:
        for value in self.values:
            if value in answer.answer.strip().lower():
                break
        else:
            raise Exception(self.MISMATCH_VALUE.format(question=answer.question))


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    exercise.answers.add_validation(
        QUESTION_ONE,
        NotEmptyRule(),
        ContainsOneOfValueRule(
            "abandoned warehouse at docks",
            "abandoned warehouse",
            "warehouse",
            "warehouse at docks",
        ),
    ).add_validation(
        QUESTION_TWO,
        NotEmptyRule(),
        ContainsOneOfValueRule(
            "2024-06-21",
            "2024-06-21 22:30",
            "21 June 2024",
            "21 Jun 2024",
            "21/06/2024",
        ),
    ).add_validation(
        QUESTION_THREE, NotEmptyRule(), HasExactValueRule("Josh Badur")
    ).add_validation(
        QUESTION_FOUR,
        HasExactValueRule(
            "Spray painted a giant smiley face over the precinct's main entrance."
        ),
    ).add_validation(
        QUESTION_FIVE, HasExactValueRule("Stole bicycle from Main Street")
    ).validate()

    return exercise.to_output([], GitAutograderStatus.SUCCESSFUL)

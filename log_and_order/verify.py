from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)
from git_autograder.answers import GitAutograderAnswersRecord
from git_autograder.answers.rules import HasExactValueRule, NotEmptyRule
from git_autograder.answers.rules.answer_rule import AnswerRule

QUESTION_ONE = "What is the SHA of the commit HEAD points to?"
QUESTION_TWO = "What is the commit message of the commit {SHA}?"
QUESTION_THREE = (
    'What is the SHA of the commit with the commit message "Rewrite the comments"?'
)


class OneOfValueRule(AnswerRule):
    MISMATCH_VALUE = "Answer for {question} did not match any of the accepted answers."

    def __init__(self, *values: str) -> None:
        super().__init__()
        self.values = values

    def apply(self, answer: GitAutograderAnswersRecord) -> None:
        for value in self.values:
            if value == answer.answer.strip().lower():
                break
        else:
            raise Exception(self.MISMATCH_VALUE.format(question=answer.question))


def ensure_str(val) -> str:
    if isinstance(val, bytes):
        return val.decode("utf-8", errors="replace").strip()
    return str(val).strip()


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    repo = exercise.repo.repo

    head_commit = repo.head.commit
    head_sha = head_commit.hexsha
    head_sha_short = head_sha[:7]

    head_message = ensure_str(head_commit.message).strip()

    target_msg = "Rewrite the comments"
    target_commit = next(
        (c for c in repo.iter_commits(all=True) if c.message.strip() == target_msg),
        None,
    )
    if target_commit is None:
        raise Exception("Could not find commit with message 'Rewrite the comments'")
    target_sha = target_commit.hexsha
    target_sha_short = target_sha[:7]

    exercise.answers.add_validation(
        QUESTION_ONE,
        NotEmptyRule(),
        OneOfValueRule(head_sha, head_sha_short),
    ).add_validation(
        QUESTION_TWO,
        NotEmptyRule(),
        HasExactValueRule(head_message),
    ).add_validation(
        QUESTION_THREE, NotEmptyRule(), OneOfValueRule(target_sha, target_sha_short)
    ).validate()

    return exercise.to_output([], GitAutograderStatus.SUCCESSFUL)

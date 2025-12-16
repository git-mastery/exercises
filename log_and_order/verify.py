import re

from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)
from git_autograder.answers import GitAutograderAnswersRecord
from git_autograder.answers.rules import HasExactValueRule, NotEmptyRule
from git_autograder.answers.rules.answer_rule import AnswerRule

QUESTION_ONE = "What is the SHA of the commit HEAD points to? You can use the full length SHA or the short SHA (i.e. first 7 characters of the SHA)"
QUESTION_TWO = "What is the commit message of the commit {SHA}?"
QUESTION_TWO_REGEX = re.compile(
    "^What is the commit message of the commit ([\\d\\w]+)\\?$"
)
QUESTION_THREE = 'What is the SHA of the commit with the commit message "Rewrite the comments"? You can use the full length SHA or the short SHA (i.e. first 7 characters of the SHA)'


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


def get_head_sha(exercise: GitAutograderExercise) -> str:
    head_commit = exercise.repo.repo.head.commit
    return head_commit.hexsha


def get_head_message(exercise: GitAutograderExercise) -> str:
    return ensure_str(exercise.repo.repo.head.commit.message).strip()


def get_target_commit_message(exercise: GitAutograderExercise, sha: str) -> str:
    target_commit = next(
        (
            c
            for c in exercise.repo.repo.iter_commits(all=True)
            if c.hexsha.strip() == sha
        ),
        None,
    )
    if target_commit is None:
        raise Exception(f"Could not find commit with SHA '{sha}'")
    return ensure_str(target_commit.message).strip()


def get_target_commit_sha(exercise: GitAutograderExercise) -> str:
    target_msg = "Rewrite the comments"
    target_commit = next(
        (
            c
            for c in exercise.repo.repo.iter_commits(all=True)
            if c.message.strip() == target_msg
        ),
        None,
    )
    if target_commit is None:
        raise Exception("Could not find commit with message 'Rewrite the comments'")
    return target_commit.hexsha


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    head_sha = get_head_sha(exercise)
    head_sha_short = head_sha[:7]

    # Get second question and find the SHA hash to pick
    second_question = exercise.answers.questions[1]
    sha_match = QUESTION_TWO_REGEX.match(second_question)
    assert sha_match is not None
    sha = sha_match.group(1)

    target_message = get_target_commit_message(exercise, sha)

    target_sha = get_target_commit_sha(exercise)
    target_sha_short = target_sha[:7]

    exercise.answers.add_validation(
        QUESTION_ONE,
        NotEmptyRule(),
        OneOfValueRule(head_sha, head_sha_short),
    ).add_validation(
        QUESTION_TWO.format(SHA=sha),
        NotEmptyRule(),
        HasExactValueRule(target_message),
    ).add_validation(
        QUESTION_THREE, NotEmptyRule(), OneOfValueRule(target_sha, target_sha_short)
    ).validate()

    return exercise.to_output([], GitAutograderStatus.SUCCESSFUL)

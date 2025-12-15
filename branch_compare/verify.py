from git_autograder import (
    GitAutograderBranch,
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

from git_autograder.answers.rules import HasExactValueRule, NotEmptyRule


QUESTION_ONE = "Which numbers are present in stream-1 but not in stream-2?"
QUESTION_TWO = "Which numbers are present in stream-2 but not in stream-1?"
NO_CHANGES_ERROR = (
    "No changes are supposed to be made to the two branches in this exercise"
)

FILE_PATH = "data.txt"
BRANCH_1 = "stream-1"
BRANCH_2 = "stream-2"


def has_made_changes(branch: GitAutograderBranch, expected_commits: int) -> bool:
    """Check branch has same number of commits as expected."""

    commits = branch.commits
    return len(commits) != expected_commits


def get_branch_diff(exercise: GitAutograderExercise, branch1: str, branch2: str) -> str:
    """Get a value present in branch1 but not in branch2."""
    exercise.repo.branches.branch(branch1).checkout()
    with exercise.repo.files.file(FILE_PATH) as f1:
        contents1 = f1.read()

    exercise.repo.branches.branch(branch2).checkout()
    with exercise.repo.files.file(FILE_PATH) as f2:
        contents2 = f2.read()

    exercise.repo.branches.branch("main").checkout()

    set1 = {line.strip() for line in contents1.splitlines() if line.strip()}
    set2 = {line.strip() for line in contents2.splitlines() if line.strip()}
    diff = set1 - set2
    return str(diff.pop())


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    branch_1 = exercise.repo.branches.branch(BRANCH_1)
    branch_2 = exercise.repo.branches.branch(BRANCH_2)
    if (
        not branch_1
        or not branch_2
        or has_made_changes(branch_1, 3)
        or has_made_changes(branch_2, 3)
    ):
        raise exercise.wrong_answer([NO_CHANGES_ERROR])

    ans_1 = get_branch_diff(exercise, BRANCH_1, BRANCH_2)
    ans_2 = get_branch_diff(exercise, BRANCH_2, BRANCH_1)

    exercise.answers.add_validation(
        QUESTION_ONE,
        NotEmptyRule(),
        HasExactValueRule(ans_1, is_case_sensitive=False),
    ).add_validation(
        QUESTION_TWO,
        NotEmptyRule(),
        HasExactValueRule(ans_2, is_case_sensitive=False),
    ).validate()

    return exercise.to_output(
        ["Great work comparing the branches successfully!"],
        GitAutograderStatus.SUCCESSFUL,
    )

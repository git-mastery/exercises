from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

from git_autograder.answers.rules import HasExactValueRule, NotEmptyRule


QUESTION_ONE = "Which numbers are present in stream-1 but not in stream-2?"
QUESTION_TWO = "Which numbers are present in stream-2 but not in stream-1?"

FILE_PATH = "data.txt"
BRANCH_1 = "stream-1"
BRANCH_2 = "stream-2"

def get_branch_diff(exercise: GitAutograderExercise, branch1: str, branch2: str) -> str:
    exercise.repo.branches.branch(branch1).checkout()
    with exercise.repo.files.file(FILE_PATH) as f1:
        contents1 = f1.read()

    exercise.repo.branches.branch(branch2).checkout()
    with exercise.repo.files.file(FILE_PATH) as f2:
        contents2 = f2.read()

    exercise.repo.branches.branch("main").checkout()

    set1 = set(contents1.splitlines())
    set2 = set(contents2.splitlines())
    diff = set1 - set2
    return str(diff.pop())

def get_stream1_diff(exercise: GitAutograderExercise) -> str:
    return get_branch_diff(exercise, BRANCH_1, BRANCH_2)

def get_stream2_diff(exercise: GitAutograderExercise) -> str:
    return get_branch_diff(exercise, BRANCH_2, BRANCH_1)

def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:

    ans_1 = get_stream1_diff(exercise)
    ans_2 = get_stream2_diff(exercise)

    exercise.answers.add_validation(
        QUESTION_ONE,
        NotEmptyRule(),
        HasExactValueRule(ans_1),
    ).add_validation(
        QUESTION_TWO, 
        NotEmptyRule(),
        HasExactValueRule(ans_2),
    ).validate()

    return exercise.to_output(["Great work comparing the branches successfully!"], GitAutograderStatus.SUCCESSFUL)

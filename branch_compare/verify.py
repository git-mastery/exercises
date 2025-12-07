from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

from git_autograder.answers.rules import HasExactValueRule, NotEmptyRule


QUESTION_ONE = "Which number (write only one number) is present in branch stream-1 but not in branch stream-2?"
QUESTION_TWO = "Which number (write only one number) is present in branch stream-2 but not in branch stream-1?"
NO_CHANGES_ERROR = "No changes are supposed to be made to the two branches in this exercise"

FILE_PATH = "data.txt"
BRANCH_1 = "stream-1"
BRANCH_2 = "stream-2"

def has_made_changes(exercise: GitAutograderExercise) -> bool:
    repo = exercise.repo.repo

    for bname in (BRANCH_1, BRANCH_2):
        if not exercise.repo.branches.has_branch(bname):
            return True

        head = repo.commit(bname)

        if len(head.parents) != 1:
            return True

        # Count commits unique to branch relative to main
        merge_bases = repo.merge_base(bname, "main")
        if not merge_bases:
            return True
        base = merge_bases[0]
        unique_commits = list(repo.iter_commits(f"{base.hexsha}..{bname}"))
        if len(unique_commits) != 1:
            return True

    return False

def get_branch_diff(exercise: GitAutograderExercise, branch1: str, branch2: str) -> str:
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

def get_stream1_diff(exercise: GitAutograderExercise) -> str:
    return get_branch_diff(exercise, BRANCH_1, BRANCH_2)

def get_stream2_diff(exercise: GitAutograderExercise) -> str:
    return get_branch_diff(exercise, BRANCH_2, BRANCH_1)

def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:

    if has_made_changes(exercise):
        return exercise.to_output([NO_CHANGES_ERROR], GitAutograderStatus.UNSUCCESSFUL)
    
    exercise.repo.branches.branch("main").checkout()

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

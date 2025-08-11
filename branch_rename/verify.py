from git import Repo
from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)

LOGIN_STILL_EXISTS = (
    "Branch 'login' still exists! Remember to rename it to 'feature/login'"
)
FEATURE_LOGIN_MISSING = "Branch 'feature/login' is missing, did you correctly rename the branch 'login' to 'feature/login'?"
NO_RENAME_EVIDENCE_FEATURE_LOGIN = "Branch 'login' was not renamed to 'feature/login'!"


def branch_has_rename_evidence(
    exercise: GitAutograderExercise, new_branch: str, old_branch: str
) -> bool:
    branch = exercise.repo.branches.branch_or_none(new_branch)
    if branch is None:
        return False

    expected = f"renamed refs/heads/{old_branch} to refs/heads/{new_branch}"
    for entry in branch.reflog:
        if entry.message == expected:
            return True
    return False


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    repo: Repo = exercise.repo.repo

    local_branches = [h.name for h in repo.heads]
    if "login" in local_branches:
        raise exercise.wrong_answer([LOGIN_STILL_EXISTS])

    if "feature/login" not in local_branches:
        raise exercise.wrong_answer([FEATURE_LOGIN_MISSING])

    if not branch_has_rename_evidence(exercise, "feature/login", "login"):
        raise exercise.wrong_answer([NO_RENAME_EVIDENCE_FEATURE_LOGIN])

    return exercise.to_output(
        ["Great work with renaming the branches on your local repository!"],
        GitAutograderStatus.SUCCESSFUL,
    )

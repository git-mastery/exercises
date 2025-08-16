import re

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
    """Performs a DFS on the branch renames starting with login till feature/login.

    This is necessary since the renames could be performed in parts:

    login -> feat/login -> feature/login
    """
    branch = exercise.repo.branches.branch_or_none(new_branch)
    if branch is None:
        # If new_branch not present at all
        return False

    rename_regex = re.compile("^renamed refs/heads/(.+) to refs/heads/(.+)$")
    for entry in branch.reflog[::-1]:
        match_group = rename_regex.match(entry.message)
        if match_group is None:
            continue
        original = match_group.group(1)
        new = match_group.group(2)
        if original == old_branch:
            old_branch = new

    return old_branch == new_branch


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

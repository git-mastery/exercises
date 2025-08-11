from git import Repo
from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)

TRY_QUICK_FIX_STILL_EXISTS = (
    "Branch 'try-quick-fix' still exists! Remember to rename it to 'fix-scrolling-bug'"
)
FIX_SCROLLING_BUG_MISSING = "Branch 'fix-scrolling-bug' is missing, did you correctly rename the branch 'try-quick-fix' to 'fix-scrolling-bug'?"
NO_RENAME_EVIDENCE_TRY_QUICK_FIX = (
    "Branch 'try-quick-fix' was not renamed to 'fix-scrolling-bug'!"
)

IMPROVE_LOADING_LOCAL_MISSING = "Local branch 'improve-loading' is missing, did you correctly rename the branch 'improve-loadding' to 'improve-loading'?"
NO_RENAME_EVIDENCE_IMPROVE_LOADING = (
    "Local branch 'improve-loadding' was not renamed to 'improve-loading'!"
)
IMPROVE_LOADING_REMOTE_MISSING = "Remote branch 'improve-loading' is missing, did you correctly push the renamed branch to the remote?"
IMPROVE_LOADING_REMOTE_OLD_PRESENT = "Remote branch 'improve-loadding' still exists! Remember to rename it to 'improve-loadding'"


def branch_has_rename_evidence(
    exercise: GitAutograderExercise, new_branch: str, old_branch: str
) -> bool:
    branch = exercise.repo.branches.branch_or_none(new_branch)
    if branch is None:
        return False

    expected = f"Branch: renamed refs/heads/{old_branch} to refs/heads/{new_branch}"
    for entry in branch.reflog:
        if entry.message == expected:
            return True
    return False


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    repo: Repo = exercise.repo.repo

    # try-quick-fix -> fix-scrolling-bug
    local_branches = [h.name for h in repo.heads]
    if "try-quick-fix" in local_branches:
        raise exercise.wrong_answer([TRY_QUICK_FIX_STILL_EXISTS])

    if "fix-scrolling-bug" not in local_branches:
        raise exercise.wrong_answer([FIX_SCROLLING_BUG_MISSING])

    if not branch_has_rename_evidence(exercise, "fix-scrolling-bug", "try-quick-fix"):
        raise exercise.wrong_answer([NO_RENAME_EVIDENCE_TRY_QUICK_FIX])

    # improve-loadding -> improve-loading
    if "improve-loading" not in local_branches:
        raise exercise.wrong_answer([IMPROVE_LOADING_LOCAL_MISSING])

    if not branch_has_rename_evidence(exercise, "improve-loading", "improve-loadding"):
        raise exercise.wrong_answer([NO_RENAME_EVIDENCE_IMPROVE_LOADING])

    # Fetch latest remote state
    for remote in repo.remotes:
        remote.fetch(prune=True)

    # Remote branch checks
    remote_branches = []
    for remote in repo.remotes:
        remote_branches.extend([ref.name for ref in remote.refs])

    if not any(ref.endswith("improve-loading") for ref in remote_branches):
        raise exercise.wrong_answer([IMPROVE_LOADING_REMOTE_MISSING])

    if any(ref.endswith("improve-loadding") for ref in remote_branches):
        raise exercise.wrong_answer([IMPROVE_LOADING_REMOTE_OLD_PRESENT])

    return exercise.to_output(
        [
            "Great work with renaming the branches on both your local and remote repositories!"
        ],
        GitAutograderStatus.SUCCESSFUL,
    )

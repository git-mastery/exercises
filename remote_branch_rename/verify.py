import re
from typing import List

from git import Repo
from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)

IMPROVE_LOADING_LOCAL_STILL_EXISTS = "Local branch 'improve-loadding' still exists! Remember to rename it to 'improve-loading'"
IMPROVE_LOADING_LOCAL_MISSING = "Local branch 'improve-loading' is missing, did you correctly rename the branch 'improve-loadding' to 'improve-loading'?"
NO_RENAME_EVIDENCE_IMPROVE_LOADING = (
    "Local branch 'improve-loadding' was not renamed to 'improve-loading'!"
)
IMPROVE_LOADING_REMOTE_MISSING = "Remote branch 'improve-loading' is missing, did you correctly push the renamed branch to the remote?"
IMPROVE_LOADING_REMOTE_OLD_PRESENT = "Remote branch 'improve-loadding' still exists! Remember to rename it to 'improve-loading'"


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


def fetch_remotes(repo: Repo) -> None:
    # Fetch latest remote state
    for remote in repo.remotes:
        remote.fetch(prune=True)


def get_remotes(repo: Repo) -> List[str]:
    remote_branches = []
    for remote in repo.remotes:
        remote_branches.extend([ref.name for ref in remote.refs])
    return remote_branches


def has_remote(remotes: List[str], target: str) -> bool:
    return any(ref.endswith(target) for ref in remotes)


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    repo: Repo = exercise.repo.repo

    # improve-loadding -> improve-loading
    local_branches = [h.name for h in repo.heads]
    if "improve-loadding" in local_branches:
        raise exercise.wrong_answer([IMPROVE_LOADING_LOCAL_STILL_EXISTS])

    if "improve-loading" not in local_branches:
        raise exercise.wrong_answer([IMPROVE_LOADING_LOCAL_MISSING])

    if not branch_has_rename_evidence(exercise, "improve-loading", "improve-loadding"):
        raise exercise.wrong_answer([NO_RENAME_EVIDENCE_IMPROVE_LOADING])

    fetch_remotes(repo)

    # Remote branch checks
    remote_branches = get_remotes(repo)

    if has_remote(remote_branches, "improve-loadding"):
        raise exercise.wrong_answer([IMPROVE_LOADING_REMOTE_OLD_PRESENT])

    if not has_remote(remote_branches, "improve-loading"):
        raise exercise.wrong_answer([IMPROVE_LOADING_REMOTE_MISSING])

    return exercise.to_output(
        [
            "Great work with renaming the branches on both your local and remote repositories!"
        ],
        GitAutograderStatus.SUCCESSFUL,
    )

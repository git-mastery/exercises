import re
from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

STU_BRANCH = "STU"
RENAMED_BRANCH = "S-to-Z"

STU_LOCAL_PRESENT = f"Local branch {STU_BRANCH} still exists."
RENAMED_LOCAL_MISSING = f"Local branch {RENAMED_BRANCH} is missing."
STU_REMOTE_PRESENT = f"Remote branch {STU_BRANCH} still exists."
RENAMED_REMOTE_MISSING = f"Remote branch {RENAMED_BRANCH} is missing."
NO_RENAME_EVIDENCE = (
    f"Local branch '{STU_BRANCH}' was not renamed to '{RENAMED_BRANCH}'!"
)
RESET_MESSAGE = (
    'If needed, reset the repository using "gitmastery progress reset" and start again.'
)


def branch_has_rename_evidence(
    exercise: GitAutograderExercise, new_branch: str, old_branch: str
) -> bool:
    """Performs a DFS on the branch renames starting with STU till S-to-Z.

    This is necessary since the renames could be performed in parts:

    STU -> S-to-U -> S-to-Z
    """
    branch = exercise.repo.branches.branch(new_branch)

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
    local_raw = exercise.repo.repo.git.branch("--list")
    local_branches = [
        line.strip().lstrip("* ").strip() for line in local_raw.splitlines()
    ]

    remote_raw = exercise.repo.repo.git.ls_remote("--heads", "origin")
    remote_branches = []
    for line in remote_raw.splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[1].startswith("refs/heads/"):
            remote_branches.append(parts[1].split("/")[-1])

    comments = []

    if STU_BRANCH in local_branches:
        comments.append(STU_LOCAL_PRESENT)

    if RENAMED_BRANCH not in local_branches:
        comments.append(RENAMED_LOCAL_MISSING)

    if STU_BRANCH in remote_branches:
        comments.append(STU_REMOTE_PRESENT)

    if RENAMED_BRANCH not in remote_branches:
        comments.append(RENAMED_REMOTE_MISSING)

    if comments:
        raise exercise.wrong_answer(comments)

    if not branch_has_rename_evidence(exercise, RENAMED_BRANCH, STU_BRANCH):
        raise exercise.wrong_answer([NO_RENAME_EVIDENCE, RESET_MESSAGE])

    return exercise.to_output(
        ["Nice work renaming the branch locally and on the remote!"],
        GitAutograderStatus.SUCCESSFUL,
    )

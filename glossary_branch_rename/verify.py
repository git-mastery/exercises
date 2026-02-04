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

    return exercise.to_output(
        ["Nice work renaming the branch locally and on the remote!"],
        GitAutograderStatus.SUCCESSFUL,
    )

from typing import List
from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

VWX_BRANCH_EXISTS_REMOTELY = (
    "Branch 'VWX' still exists on the remote! Remember to delete it from the remote."
)

VWX_BRANCH_EXISTS_LOCALLY = "Branch 'VWX' still exists locally! Remember to delete it from your local repository."


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    comments: List[str] = []

    local_branches = [h.name for h in exercise.repo.repo.heads]
    if "VWX" in local_branches:
        comments.append(VWX_BRANCH_EXISTS_LOCALLY)

    try:
        exercise.repo.repo.refs["origin/VWX"]
        comments.append(VWX_BRANCH_EXISTS_REMOTELY)
    except (IndexError, KeyError):
        pass  # Branch doesn't exist on remote, which is what we want

    if comments:
        raise exercise.wrong_answer(comments)

    return exercise.to_output(
        ["Great job deleting the VWX branch!"],
        GitAutograderStatus.SUCCESSFUL,
    )

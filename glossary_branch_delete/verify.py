from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

VWX_BRANCH_EXISTS_LOCALLY = "Branch 'VWX' still exists locally! Remember to delete it."
VWX_BRANCH_EXISTS_REMOTELY = (
    "Branch 'VWX' still exists on the remote! Remember to delete it from the remote."
)


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    if exercise.repo.branches.has_branch("VWX"):
        raise exercise.wrong_answer([VWX_BRANCH_EXISTS_LOCALLY])

    origin_remote = exercise.repo.remotes.remote("origin")
    origin_remote.remote.fetch()

    try:
        exercise.repo.repo.refs["origin/VWX"]
        raise exercise.wrong_answer([VWX_BRANCH_EXISTS_REMOTELY])
    except (IndexError, KeyError):
        pass

    return exercise.to_output(
        ["Great job deleting the VWX branch locally and remotely!"],
        GitAutograderStatus.SUCCESSFUL,
    )

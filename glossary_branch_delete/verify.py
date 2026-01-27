from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

VWX_BRANCH_EXISTS_REMOTELY = (
    "Branch 'VWX' still exists on the remote! Remember to delete it from the remote."
)


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    try:
        exercise.repo.repo.refs["origin/VWX"]
        raise exercise.wrong_answer([VWX_BRANCH_EXISTS_REMOTELY])
    except (IndexError, KeyError):
        pass  # Branch doesn't exist on remote, which is what we want

    return exercise.to_output(
        ["Great job deleting the VWX branch!"],
        GitAutograderStatus.SUCCESSFUL,
    )

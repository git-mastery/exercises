from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)

PQR_BRANCH_NOT_PUSHED = "Branch 'PQR' has not been pushed to the remote."


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    try:
        exercise.repo.repo.refs["origin/PQR"]
    except (IndexError, KeyError):
        raise exercise.wrong_answer([PQR_BRANCH_NOT_PUSHED])

    return exercise.to_output(
        ["Great work pushing the PQR branch to your fork!"],
        GitAutograderStatus.SUCCESSFUL,
    )

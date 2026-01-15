from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)

PQR_BRANCH_MISSING = "Branch 'PQR' is missing locally! Did you delete it?"
PQR_BRANCH_NOT_PUSHED = "Branch 'PQR' has not been pushed to the remote! Remember to push it to origin."


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    has_local_pqr_branch = exercise.repo.branches.has_branch("PQR")
    if not has_local_pqr_branch:
        raise exercise.wrong_answer([PQR_BRANCH_MISSING])

    origin_remote = exercise.repo.remotes.remote("origin")
    origin_remote.remote.fetch()

    try:
        remote_pqr = exercise.repo.repo.refs["origin/PQR"]
    except (IndexError, KeyError):
        raise exercise.wrong_answer([PQR_BRANCH_NOT_PUSHED])

    return exercise.to_output(
        ["Great work pushing the PQR branch to your fork!"],
        GitAutograderStatus.SUCCESSFUL,
    )

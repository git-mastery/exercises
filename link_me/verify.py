from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)

MISSING_UPSTREAM_REMOTE = "Missing remote called 'upstream'."
WRONG_UPSTREAM_URL = "Wrong 'upstream' remote URL"


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    if not exercise.repo.remotes.has_remote("upstream"):
        raise exercise.wrong_answer([MISSING_UPSTREAM_REMOTE])

    upstream = exercise.repo.remotes.remote("upstream")
    if not upstream.is_for_repo("git-mastery", "link-me"):
        raise exercise.wrong_answer([WRONG_UPSTREAM_URL])

    return exercise.to_output(
        ["Great work with using git remote to add an upstream remote!"],
        GitAutograderStatus.SUCCESSFUL,
    )

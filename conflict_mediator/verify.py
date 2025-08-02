from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)

UNCOMMITTED_CHANGES = "You still have uncommitted changes. Commit them first on the appropriate branch first!"
NOT_ON_MAIN = (
    "You aren't currently on the main branch. Checkout to that branch and try again!"
)
DETACHED_HEAD = "You should not be in a detached HEAD state! Run git checkout main to get back to main"
MERGE_NOT_RESOLVED = "You should resolve the merge by setting the print to be 'Hello Everyone and World!'"
RESET_MESSAGE = 'Reset the repository using "gitmastery progress reset" and start again'


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    if exercise.repo.repo.is_dirty():
        raise exercise.wrong_answer([UNCOMMITTED_CHANGES])

    try:
        if exercise.repo.repo.active_branch.name != "main":
            raise exercise.wrong_answer([NOT_ON_MAIN])
    except TypeError:
        raise exercise.wrong_answer([DETACHED_HEAD])

    with exercise.repo.files.file("script.py") as script_file:
        contents = script_file.read().strip()
        if (
            contents != 'print("Hello Everyone and World!")'
            and contents != "print('Hello Everyone and World!')"
        ):
            raise exercise.wrong_answer([MERGE_NOT_RESOLVED, RESET_MESSAGE])

    return exercise.to_output(
        ["Great work resolving the merge conflict!"], GitAutograderStatus.SUCCESSFUL
    )

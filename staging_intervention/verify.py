from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

EXPECTED_UNTRACKED = {
    "josh.txt",
    "adam.txt",
    "mary.txt",
}
EXTRA_FILES_UNSTAGED = (
    "You should only be unstaging the attendance files for Josh, Adam, and Mary."
)
MISSING_FILES_UNSTAGED = (
    "You need to unstage all three attendance files for Josh, Adam, and Mary."
)


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    untracked_files = set(exercise.repo.repo.untracked_files)
    comments = []

    extra_files_unstaged = untracked_files.difference(EXPECTED_UNTRACKED)
    missing_files_unstaged = EXPECTED_UNTRACKED.difference(untracked_files)

    if extra_files_unstaged:
        comments.append(EXTRA_FILES_UNSTAGED)

    if missing_files_unstaged:
        comments.append(MISSING_FILES_UNSTAGED)

    if comments:
        raise exercise.wrong_answer(comments)

    return exercise.to_output(
        ["Great work! You have successfully fixed the attendance system!"],
        GitAutograderStatus.SUCCESSFUL,
    )

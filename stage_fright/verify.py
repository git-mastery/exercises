from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)

EXPECTED_FILES = {"alice.txt", "bob.txt", "jim.txt", "joe.txt", "carrey.txt"}

NOT_ADDED = "Did not add {file}"


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    staged_diff = exercise.repo.repo.index.diff("HEAD")

    added_files = set()
    for diff_item in staged_diff:
        added_files.add(diff_item.a_path)

    if len(added_files & EXPECTED_FILES) != len(EXPECTED_FILES):
        missing_files = EXPECTED_FILES.difference(added_files)
        raise exercise.wrong_answer(
            [NOT_ADDED.format(file=file) for file in missing_files]
        )

    return exercise.to_output(
        ["Great work! You have successfully checked in all the actors!"],
        GitAutograderStatus.SUCCESSFUL,
    )

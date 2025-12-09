from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)

FAST_FORWARD_REQUIRED = (
    "You must use a fast-forward merge to bring a branch into 'main'."
)

ONLY_WITH_SALLY_MERGED = (
    "Only one of the two starting branches can be fast-forward merged into 'main'. Do not create new branches."
)

EXPECTED_MAIN_COMMIT_MESSAGES = {
    "Introduce Harry",
    "Add about family",
    "Add cast.txt",
    "Mention Sally",
}

def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    repo = exercise.repo.repo
    head_commit = repo.head.commit
    main_commits = list(repo.iter_commits("main"))

    sally_commit = next(
        (commit for commit in main_commits if commit.message.strip() == "Mention Sally"),
        None,
    )
    if sally_commit is None:
        raise exercise.wrong_answer([ONLY_WITH_SALLY_MERGED])

    # Confirm that the fast-forward landed exactly on the expected commit and did not
    # introduce a merge commit.
    if len(head_commit.parents) != 1:
        raise exercise.wrong_answer([FAST_FORWARD_REQUIRED])

    if head_commit.message.strip() != "Mention Sally":
        raise exercise.wrong_answer([ONLY_WITH_SALLY_MERGED])

    if any(len(commit.parents) > 1 for commit in main_commits):
        raise exercise.wrong_answer([FAST_FORWARD_REQUIRED])

    if len(main_commits) != len(EXPECTED_MAIN_COMMIT_MESSAGES):
        raise exercise.wrong_answer([ONLY_WITH_SALLY_MERGED])

    commit_messages = {commit.message.strip() for commit in main_commits}
    if not commit_messages.issubset(EXPECTED_MAIN_COMMIT_MESSAGES):
        raise exercise.wrong_answer([ONLY_WITH_SALLY_MERGED])

    if "Mention Ginny is single" in commit_messages:
        raise exercise.wrong_answer([ONLY_WITH_SALLY_MERGED])

    return exercise.to_output(
        ["Great job fast-forward merging only 'with-sally'!"],
        GitAutograderStatus.SUCCESSFUL,
    )


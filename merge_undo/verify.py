from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

MAIN_BRANCH_MISSING = (
    "Main branch is missing, you can reset the exercises if needed and try again."
)
MERGES_NOT_UNDONE = "It appears the merge commits are still in the history of the 'main' branch. This shouldn't be the case"
MAIN_WRONG_COMMIT = "The 'main' branch is not pointing to the correct commit. It should be pointing to the commit made just before the merges."
RESET_MESSAGE = 'Reset the repository using "gitmastery progress reset" and start again'
SUCCESS_MESSAGE = "Great work with undoing the merges! Try listing the directory to see what has changed."


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    main_branch = exercise.repo.branches.branch_or_none("main")

    if not main_branch:
        raise exercise.wrong_answer([MAIN_BRANCH_MISSING, RESET_MESSAGE])

    main_history = main_branch.commits

    if any(len(c.commit.parents) > 1 for c in main_history):
        raise exercise.wrong_answer([MERGES_NOT_UNDONE, RESET_MESSAGE])

    main_head_commit = main_branch.latest_commit
    expected_commit_message = "Mention Morty is grandson"
    if main_head_commit.commit.message.strip() != expected_commit_message:
        raise exercise.wrong_answer([MAIN_WRONG_COMMIT, RESET_MESSAGE])

    return exercise.to_output(
        [SUCCESS_MESSAGE],
        GitAutograderStatus.SUCCESSFUL,
    )

from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

NOT_ON_MAIN = (
    "You aren't currently on the main branch. Checkout to that branch and try again!"
)
DETACHED_HEAD = "You should not be in a detached HEAD state! Use git checkout main to get back to main"
MERGES_NOT_UNDONE = "It appears the merge commits are still in the history of the 'main' branch. This shouldn't be the case"
MAIN_WRONG_COMMIT = "The 'main' branch is not pointing to the correct commit. It should be pointing to the commit made just before the merges."
RESET_MESSAGE = 'Reset the repository using "gitmastery progress reset" and start again'
SUCCESS_MESSAGE = "Great work with undoing the merges! Try listing the directory to see what has changed."


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    repo = exercise.repo.repo

    try:
        if repo.active_branch.name != "main":
            raise exercise.wrong_answer([NOT_ON_MAIN])
    except TypeError:
        raise exercise.wrong_answer([DETACHED_HEAD, RESET_MESSAGE])

    main_branch = exercise.repo.branches.branch("main")
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

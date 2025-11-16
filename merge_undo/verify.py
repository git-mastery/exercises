from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

UNCOMMITTED_CHANGES = "You still have uncommitted changes. Commit them first on the appropriate branch first!"
NOT_ON_MAIN = (
    "You aren't currently on the main branch. Checkout to that branch and try again!"
)
DETACHED_HEAD = "You should not be in a detached HEAD state! Use git checkout main to get back to main"
MERGES_NOT_UNDONE = (
    "It appears the merge commits are still in the history of the 'main' branch. This shouldn't be the case"
)
MAIN_WRONG_COMMIT = "The 'main' branch is not pointing to the correct commit. It should be pointing to the commit made just before the merges."
DAUGHTER_BRANCH_MISSING = "The 'daughter' branch seems to have been deleted. It should still exist."
SON_IN_LAW_BRANCH_MISSING = "The 'son-in-law' branch seems to have been deleted. It should still exist."
RESET_MESSAGE = 'Reset the repository using "gitmastery progress reset" and start again'
SUCCESS_MESSAGE = "Great work with undoing the merges! Try listing the directory to see what has changed."


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    """
    Verifies that the user has successfully undone the last two merges on the main branch.
    """
    repo = exercise.repo.repo

    if repo.is_dirty():
        raise exercise.wrong_answer([UNCOMMITTED_CHANGES])

    try:
        if repo.active_branch.name != "main":
            raise exercise.wrong_answer([NOT_ON_MAIN])
    except TypeError:
        raise exercise.wrong_answer([DETACHED_HEAD])

    if not exercise.repo.branches.has_branch("daughter"):
        raise exercise.wrong_answer([DAUGHTER_BRANCH_MISSING, RESET_MESSAGE])

    if not exercise.repo.branches.has_branch("son-in-law"):
        raise exercise.wrong_answer([SON_IN_LAW_BRANCH_MISSING, RESET_MESSAGE])

    main_branch = exercise.repo.branches.branch("main")

    main_head_commit = main_branch.latest_commit
    expected_commit_message = "Mention Morty is grandson"

    if main_head_commit.commit.message.strip() != expected_commit_message:
        raise exercise.wrong_answer([MAIN_WRONG_COMMIT, RESET_MESSAGE])

    # After reset, merge messages shouldn't be in history
    main_history = main_branch.commits
    main_history_messages = [c.commit.message.strip() for c in main_history]

    merge_messages = ["Introduce Beth", "introduce Jerry"]
    if any(msg in main_history_messages for msg in merge_messages):
        raise exercise.wrong_answer([MERGES_NOT_UNDONE, RESET_MESSAGE])

    return exercise.to_output(
        [SUCCESS_MESSAGE],
        GitAutograderStatus.SUCCESSFUL,
    )

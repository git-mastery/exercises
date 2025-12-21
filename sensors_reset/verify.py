from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

CONTAINS_TASK_ONE_COMMITS = "It seems like the last two commits for Jan 14 and Jan 15 are still present in the commit history."
CONTAINS_TASK_TWO_COMMIT = (
    "It seems like the commit from Jan 13 is still present in the commit history."
)
CONTAINS_TASK_THREE_COMMIT = (
    "It seems like the commit from Jan 12 is still present in the commit history."
)
TASK_ONE_WRONG_RESET = "Changes from Jan 14 and Jan 15 should not be present in the working directory or staging area."
TASK_TWO_WRONG_RESET = "Changes from Jan 13 should be present in the working directory but not in the staging area."
TASK_THREE_WRONG_RESET = "Changes from Jan 12 should be present in both the working directory and staging area."


def get_staged_files(exercise: GitAutograderExercise) -> set:
    """Get files that are staged."""
    staged_diff = exercise.repo.repo.index.diff("HEAD")
    return {diff_item.a_path for diff_item in staged_diff}


def get_unstaged_files(exercise: GitAutograderExercise) -> set:
    """Get files that have unstaged changes."""
    unstaged_diff = exercise.repo.repo.index.diff(None)
    return {diff_item.a_path for diff_item in unstaged_diff}


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    master_branch = exercise.repo.branches.branch_or_none(
        "master"
    ) or exercise.repo.branches.branch_or_none("main")
    commit_messages = [str(c.commit.message) for c in master_branch.commits]

    staged_files = get_staged_files(exercise)
    unstaged_files = get_unstaged_files(exercise)

    # Task 1: Commits should be removed, changes should not be in staging or working directory
    if any(
        msg in commit_messages
        for msg in [
            "Record data for Jan 14",
            "Record data for Jan 15",
        ]
    ):
        raise exercise.wrong_answer([CONTAINS_TASK_ONE_COMMITS])

    # Task 2: Commit should be removed, changes should be in working directory but NOT staged
    if "Record data for Jan 13" in commit_messages:
        raise exercise.wrong_answer([CONTAINS_TASK_TWO_COMMIT])

    if not unstaged_files:
        raise exercise.wrong_answer([TASK_TWO_WRONG_RESET])

    # Task 3: Commit should be removed, changes should be in staging area
    if "Record data for Jan 12" in commit_messages:
        raise exercise.wrong_answer([CONTAINS_TASK_THREE_COMMIT])

    if not staged_files:
        raise exercise.wrong_answer([TASK_THREE_WRONG_RESET])

    return exercise.to_output(
        ["You have reset the repository to the correct state!"],
        GitAutograderStatus.SUCCESSFUL,
    )

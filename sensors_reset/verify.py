from typing import List

from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)

CONTAINS_TASK_ONE_COMMITS = "It seems like the last two commits for Jan 14 and Jan 15 are still present in the commit history."
CONTAINS_TASK_TWO_COMMIT = (
    "It seems like the commit from Jan 13 is still present in the commit history."
)
CONTAINS_TASK_THREE_COMMIT = (
    "It seems like the commit from Jan 12 is still present in the commit history."
)
WRONG_FILES_IN_STAGING_AREA = (
    "Unexpected files in staging area. Looks like you used the wrong reset mode."
)
WRONG_FILES_IN_WORKING_DIRECTORY = (
    "Unexpected files in working directory. Looks like you used the wrong reset mode."
)
WRONG_HEAD_COMMIT = "The head commit should be the commit from Jan 11."


def get_staged_files(exercise: GitAutograderExercise) -> List[str | None]:
    """Get files that are staged (differ between index and HEAD)."""
    repo = exercise.repo.repo
    return [diff_item.a_path for diff_item in repo.head.commit.diff()]


def get_unstaged_files(exercise: GitAutograderExercise) -> List[str | None]:
    """Get files that have unstaged changes (differ between working tree and index)."""
    repo = exercise.repo.repo
    return [d.a_path for d in repo.index.diff(None)]


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    branch = exercise.repo.branches.branch("main")
    commit_messages = [str(c.commit.message.strip()) for c in branch.commits]

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

    # Task 3: Commit should be removed, changes should be in staging area
    if "Record data for Jan 12" in commit_messages:
        raise exercise.wrong_answer([CONTAINS_TASK_THREE_COMMIT])

    if branch.latest_commit.commit.message.strip() != "Record data for Jan 11":
        raise exercise.wrong_answer([WRONG_HEAD_COMMIT])

    # TODO: need a way to verify task by task
    # currently we verify staging area and working directory of all tasks at once, since we cannot get state of each task
    comments: List[str] = []
    if len(unstaged_files) != 4 or not all(
        file in unstaged_files
        for file in ["east.csv", "north.csv", "south.csv", "west.csv"]
    ):
        comments.append(WRONG_FILES_IN_WORKING_DIRECTORY)

    if len(staged_files) != 3 or not all(
        file in staged_files for file in ["east.csv", "north.csv", "south.csv"]
    ):
        comments.append(WRONG_FILES_IN_STAGING_AREA)

    if comments:
        raise exercise.wrong_answer(comments)

    return exercise.to_output(
        ["You have reset the repository to the correct state!"],
        GitAutograderStatus.SUCCESSFUL,
    )

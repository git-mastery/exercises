from typing import List, Optional
from git_autograder import (
    GitAutograderCommit,
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)

FAST_FORWARD_REQUIRED = (
    "You must use a fast-forward merge to bring a branch into 'main'."
)

ONLY_WITH_SALLY_MERGED = "Only one of the two starting branches can be fast-forward merged into 'main'. Do not create new branches."

EXPECTED_MAIN_COMMIT_MESSAGES = {
    "Set initial state",
    "Introduce Harry",
    "Add about family",
    "Add cast.txt",
    "Mention Sally",
}


def get_commit_from_message(
    commits: List[GitAutograderCommit], message: str
) -> Optional[GitAutograderCommit]:
    """Find a commit with the given message from a list of commits."""
    for commit in commits:
        if message.strip() == commit.commit.message.strip():
            return commit
    return None


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    main_commits = exercise.repo.branches.branch("main").commits
    head_commit = exercise.repo.branches.branch("main").latest_commit

    sally_commit = get_commit_from_message(main_commits, "Mention Sally")
    if sally_commit is None:
        raise exercise.wrong_answer([ONLY_WITH_SALLY_MERGED])

    # Confirm that the fast-forward landed exactly on the expected commit and did not
    # introduce a merge commit.
    if len(head_commit.parents) != 1:
        raise exercise.wrong_answer([FAST_FORWARD_REQUIRED])

    if head_commit.commit.message.strip() != "Mention Sally":
        raise exercise.wrong_answer([ONLY_WITH_SALLY_MERGED])

    if any(len(commit.parents) > 1 for commit in main_commits):
        raise exercise.wrong_answer([FAST_FORWARD_REQUIRED])

    if len(main_commits) != len(EXPECTED_MAIN_COMMIT_MESSAGES):
        raise exercise.wrong_answer([ONLY_WITH_SALLY_MERGED])

    commit_messages = {commit.commit.message.strip() for commit in main_commits}
    if not commit_messages.issubset(EXPECTED_MAIN_COMMIT_MESSAGES):
        raise exercise.wrong_answer([ONLY_WITH_SALLY_MERGED])

    if "Mention Ginny is single" in commit_messages:
        raise exercise.wrong_answer([ONLY_WITH_SALLY_MERGED])

    return exercise.to_output(
        ["Great job fast-forward merging only 'with-sally'!"],
        GitAutograderStatus.SUCCESSFUL,
    )

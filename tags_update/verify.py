from typing import List, Optional

from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
    GitAutograderCommit,
)

MISSING_JANUARY_TAG = "You are missing the 'january-update' tag."
WRONG_JANUARY_TAG_COMMIT = "The 'january-update' tag is pointing to the wrong commit. It should point to the January commit."
MISSING_APRIL_TAG = "You are missing the 'april-update' tag."
WRONG_APRIL_TAG_COMMIT = "The 'april-update' tag is pointing to the wrong commit. It should point to the April commit."
OLD_FIRST_UPDATE_TAG = "The 'first-update' tag still exists."
SUCCESS_MESSAGE = "Great work! You have successfully updated the tags to point to the correct commits."
MISSING_COMMIT_MESSAGE = "Could not find a commit with '{message}' in the message."


def get_commit_from_message(
    commits: List[GitAutograderCommit], message: str
) -> Optional[GitAutograderCommit]:
    """Find a commit with the given message from a list of commits."""
    for commit in commits:
        if message.strip() == commit.commit.message.strip():
            return commit
    return None


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    comments: List[str] = []
    tags = exercise.repo.repo.tags
    main_branch_commits = exercise.repo.branches.branch("main").commits

    # Verify first-update is renamed to january-update
    if "first-update" in tags:
        comments.append(OLD_FIRST_UPDATE_TAG)

    if "january-update" not in tags:
        comments.append(MISSING_JANUARY_TAG)

    if comments:
        raise exercise.wrong_answer(comments)

    january_commit = get_commit_from_message(
        main_branch_commits, "Add January duty roster"
    )
    if january_commit is None:
        raise exercise.wrong_answer([MISSING_COMMIT_MESSAGE.format(message="January")])

    january_tag_commit = tags["january-update"].commit
    if january_tag_commit.hexsha != january_commit.hexsha:
        raise exercise.wrong_answer([WRONG_JANUARY_TAG_COMMIT])

    # Verify april-update is moved to correct commit
    if "april-update" not in tags:
        raise exercise.wrong_answer([MISSING_APRIL_TAG])

    april_commit = get_commit_from_message(
        main_branch_commits, "Update duty roster for April"
    )
    if april_commit is None:
        raise exercise.wrong_answer([MISSING_COMMIT_MESSAGE.format(message="April")])

    april_tag_commit = tags["april-update"].commit
    if april_tag_commit.hexsha != april_commit.hexsha:
        raise exercise.wrong_answer([WRONG_APRIL_TAG_COMMIT])

    return exercise.to_output(
        [SUCCESS_MESSAGE],
        GitAutograderStatus.SUCCESSFUL,
    )

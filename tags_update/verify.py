from typing import Optional
from git.objects.commit import Commit

from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)

MISSING_JANUARY_TAG = "The 'january-update' tag is missing! You need to rename 'first-update' to 'january-update'."
WRONG_JANUARY_TAG_COMMIT = "The 'january-update' tag is pointing to the wrong commit! It should point to the January commit."
MISSING_APRIL_TAG = "The 'april-update' tag is missing!"
WRONG_APRIL_TAG_COMMIT = "The 'april-update' tag is pointing to the wrong commit! It should point to the April commit, not the May commit."
OLD_FIRST_UPDATE_TAG = "The old 'first-update' tag still exists! You need to delete it after renaming to 'january-update'."
SUCCESS_MESSAGE = "Great work! You have successfully updated the tags to point to the correct commits."
MISSING_COMMIT_MESSAGE = "Could not find a commit with '{message}' in the message"


def find_commit_by_message(exercise: GitAutograderExercise, message: str) -> Optional[Commit]:
    """Find a commit with the given message."""
    commits = list(exercise.repo.repo.iter_commits(all=True))
    for commit in commits:
        if message.strip() == commit.message.strip():
            return commit
    return None


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    tags = exercise.repo.repo.tags

    # Verify that the tags exist and that the old first-update tag is deleted
    if "first-update" in tags:
        raise exercise.wrong_answer([OLD_FIRST_UPDATE_TAG])    
    if "january-update" not in tags:
        raise exercise.wrong_answer([MISSING_JANUARY_TAG])
    if "april-update" not in tags:
        raise exercise.wrong_answer([MISSING_APRIL_TAG])
    
    # Get correct commits that the tags should point to
    january_commit = find_commit_by_message(exercise, "Add January duty roster")
    if january_commit is None:
        raise exercise.wrong_answer([MISSING_COMMIT_MESSAGE.format(message="January")])
    
    april_commit = find_commit_by_message(exercise, "Update duty roster for April")
    if april_commit is None:
        raise exercise.wrong_answer([MISSING_COMMIT_MESSAGE.format(message="April")])

    # Verify that the tags point to the correct commits
    january_tag_commit = tags["january-update"].commit
    if january_tag_commit.hexsha != january_commit.hexsha:
        raise exercise.wrong_answer([WRONG_JANUARY_TAG_COMMIT])

    april_tag_commit = tags["april-update"].commit
    if april_tag_commit.hexsha != april_commit.hexsha:
        raise exercise.wrong_answer([WRONG_APRIL_TAG_COMMIT])
    
    return exercise.to_output(
        [SUCCESS_MESSAGE],
        GitAutograderStatus.SUCCESSFUL,
    )

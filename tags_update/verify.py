from typing import List, Optional

from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
    GitAutograderCommit,
)

MISSING_JANUARY_TAG = "The 'january-update' tag is missing! You need to rename 'first-update' to 'january-update'."
WRONG_JANUARY_TAG_COMMIT = "The 'january-update' tag is pointing to the wrong commit! It should point to the January commit."
MISSING_APRIL_TAG = "The 'april-update' tag is missing!"
WRONG_APRIL_TAG_COMMIT = "The 'april-update' tag is pointing to the wrong commit! It should point to the April commit, not the May commit."
OLD_FIRST_UPDATE_TAG = "The old 'first-update' tag still exists! You need to delete it after renaming to 'january-update'."
SUCCESS_MESSAGE = "Great work! You have successfully updated the tags to point to the correct commits."
MISSING_COMMIT_MESSAGE = "Could not find a commit with '{message}' in the message"


def get_commit_from_message(commits: List[GitAutograderCommit], message: str) -> Optional[GitAutograderCommit]:
    """Find a commit with the given message from a list of commits."""
    for commit in commits:
        if message.strip() == commit.commit.message.strip():
            return commit
    return None


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    tags = exercise.repo.repo.tags

    # Ensure first-update tag does not exist
    if "first-update" in tags:
        raise exercise.wrong_answer([OLD_FIRST_UPDATE_TAG])
    
    # Ensure january-update tag exists
    if "january-update" not in tags:
        raise exercise.wrong_answer([MISSING_JANUARY_TAG])
    
    # Ensure january-update tag points to the correct commit
    main_branch_commits = exercise.repo.branches.branch("main").commits
    january_commit = get_commit_from_message(main_branch_commits, "Add January duty roster")
    if january_commit is None:
        raise exercise.wrong_answer([MISSING_COMMIT_MESSAGE.format(message="January")])
    
    january_tag_commit = tags["january-update"].commit
    if january_tag_commit.hexsha != january_commit.hexsha:
        raise exercise.wrong_answer([WRONG_JANUARY_TAG_COMMIT])

    # Ensure april-update tag exists
    if "april-update" not in tags:
        raise exercise.wrong_answer([MISSING_APRIL_TAG])
    
    # Ensure april-update tag points to the correct commit
    april_commit = get_commit_from_message(main_branch_commits, "Update duty roster for April")
    if april_commit is None:
        raise exercise.wrong_answer([MISSING_COMMIT_MESSAGE.format(message="April")])
    
    april_tag_commit = tags["april-update"].commit
    if april_tag_commit.hexsha != april_commit.hexsha:
        raise exercise.wrong_answer([WRONG_APRIL_TAG_COMMIT])
    
    return exercise.to_output(
        [SUCCESS_MESSAGE],
        GitAutograderStatus.SUCCESSFUL,
    )

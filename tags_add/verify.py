from typing import List, Optional
from git_autograder import (
    GitAutograderCommit,
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)

FIRST_TAG_NOT_LIGHTWEIGHT = (
    '"first-pilot" should be a lightweight tag, not an annotated tag.'
)
SECOND_TAG_NOT_ANNOTATED = '"v1.0" should be an annotated tag, not a lightweight tag.'
MISSING_FIRST_TAG = 'Missing lightweight tag "first-pilot".'
MISSING_SECOND_TAG = 'Missing annotated tag "v1.0".'
WRONG_SECOND_TAG_MESSAGE = '"v1.0" message must be exactly "first full duty roster".'
FIRST_TAG_WRONG_COMMIT = '"first-pilot" should point to the first commit.'
SECOND_TAG_WRONG_COMMIT = (
    '"v1.0" should point to the commit that updates March duty roster.'
)
MISSING_FIRST_COMMIT = "Missing commit that adds January duty roster."
MISSING_MARCH_COMMIT = "Missing commit that updates March duty roster."


def get_commit_from_message(
    commits: List[GitAutograderCommit], message: str
) -> Optional[GitAutograderCommit]:
    """Find a commit with the given message from a list of commits."""
    for commit in commits:
        if message.strip() == commit.commit.message.strip():
            return commit
    return None


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    # Task 1: Verify lightweight tag "first-pilot" on the first commit
    tags = exercise.repo.repo.tags
    if "first-pilot" not in tags:
        raise exercise.wrong_answer([MISSING_FIRST_TAG])

    # Verify that "first-pilot" is a lightweight tag
    first_pilot_tag = tags["first-pilot"]
    if first_pilot_tag.tag is not None:
        raise exercise.wrong_answer([FIRST_TAG_NOT_LIGHTWEIGHT])

    main_branch = exercise.repo.branches.branch("main")
    main_branch_commits = main_branch.commits
    if len(main_branch_commits) == 0:
        raise exercise.wrong_answer([MISSING_FIRST_COMMIT])

    first_commit = main_branch_commits[-1]
    first_pilot_tag_commit = first_pilot_tag.commit
    if first_pilot_tag_commit.hexsha != first_commit.hexsha:
        raise exercise.wrong_answer([FIRST_TAG_WRONG_COMMIT])

    # Task 2: Verify annotated tag "v1.0" on March commit with correct message
    if "v1.0" not in tags:
        raise exercise.wrong_answer([MISSING_SECOND_TAG])

    # Verify that "v1.0" is an annotated tag
    v1_tag = tags["v1.0"]
    if v1_tag.tag is None:
        raise exercise.wrong_answer([SECOND_TAG_NOT_ANNOTATED])

    march_commit = get_commit_from_message(
        main_branch_commits, "Update roster for March"
    )
    if march_commit is None:
        raise exercise.wrong_answer([MISSING_MARCH_COMMIT])

    v1_tag_commit = v1_tag.commit
    if v1_tag_commit.hexsha != march_commit.hexsha:
        raise exercise.wrong_answer([SECOND_TAG_WRONG_COMMIT])

    # Use strip() and lower() for less strict comparison of tag message
    if v1_tag.tag.message.strip().lower() != "first full duty roster":
        raise exercise.wrong_answer([WRONG_SECOND_TAG_MESSAGE])

    return exercise.to_output(
        ["Great work using git tag to annotate various commits in the repository!"],
        GitAutograderStatus.SUCCESSFUL,
    )

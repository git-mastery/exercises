from typing import List, Optional
from git_autograder import GitAutograderCommit, GitAutograderExercise, GitAutograderOutput, GitAutograderStatus

FIRST_TAG = "first-pilot"
SECOND_TAG = "v1.0"
SECOND_TAG_MSG = "first full duty roster"
MARCH_MSG_FRAGMENT = "Update roster for March"

MISSING_FIRST_TAG = f'Missing lightweight tag "{FIRST_TAG}".'
MISSING_SECOND_TAG = f'Missing annotated tag "{SECOND_TAG}".'
WRONG_SECOND_TAG_MESSAGE = f'"{SECOND_TAG}" message must be exactly "{SECOND_TAG_MSG}".'
FIRST_TAG_WRONG_COMMIT = f'"{FIRST_TAG}" should point to the first commit.'
SECOND_TAG_WRONG_COMMIT = f'"{SECOND_TAG}" should point to the commit that updates March duty roster.'
MISSING_FIRST_COMMIT = "Missing commit that adds January duty roster."
MISSING_MARCH_COMMIT = "Missing commit that updates March duty roster."
SUCCESS_MESSAGE = "Great work using git tag to annotate various commits in the repository!"


def get_commit_from_message(commits: List[GitAutograderCommit], message: str) -> Optional[GitAutograderCommit]:
    """Find a commit with the given message from a list of commits."""
    for commit in commits:
        if message.strip() == commit.commit.message.strip():
            return commit
    return None


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:    
    # Verify lightweight tag "first-pilot" on the first commit
    tags = exercise.repo.repo.tags
    if FIRST_TAG not in tags:
        raise exercise.wrong_answer([MISSING_FIRST_TAG])

    main_branch = exercise.repo.branches.branch("main")
    main_branch_commits = main_branch.commits
    if len(main_branch_commits) == 0:
        raise exercise.wrong_answer([MISSING_FIRST_COMMIT])

    first_commit = main_branch_commits[-1]
    first_pilot_tag_commit = tags[FIRST_TAG].commit
    if first_pilot_tag_commit.hexsha != first_commit.hexsha:
        raise exercise.wrong_answer([FIRST_TAG_WRONG_COMMIT])

    # Verify annotated tag "v1.0" on March commit with correct message
    if SECOND_TAG not in tags:
        raise exercise.wrong_answer([MISSING_SECOND_TAG])

    v1_tag = tags[SECOND_TAG]
    if v1_tag is None:
        raise exercise.wrong_answer([MISSING_SECOND_TAG])

    march_commit = get_commit_from_message(main_branch_commits, MARCH_MSG_FRAGMENT)
    if march_commit is None:
        raise exercise.wrong_answer([MISSING_MARCH_COMMIT])

    v1_tag_commit = v1_tag.commit
    if v1_tag_commit.hexsha != march_commit.hexsha:
        raise exercise.wrong_answer([SECOND_TAG_WRONG_COMMIT])

    if v1_tag.tag.message.strip() != SECOND_TAG_MSG:
        raise exercise.wrong_answer([WRONG_SECOND_TAG_MESSAGE])

    return exercise.to_output(
        [SUCCESS_MESSAGE],
        GitAutograderStatus.SUCCESSFUL,
    )

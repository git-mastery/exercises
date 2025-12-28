from typing import List, Optional

from git_autograder import (
    GitAutograderCommit,
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)

MISSING_LOCATION_COMMIT = "The commit with message 'Describe location' is not found."
MISSING_STORY_FILE = "The file 'story.txt' is not found."
MISSING_BRANCH = "The '{branch_name}' branch is missing."
MISSING_COMMIT = "No commits were made in the '{branch_name}' branch."
WRONG_START = (
    "The '{branch_name}' branch should start from the second commit "
    "(with message 'Describe location')."
)
WRONG_CONTENT = (
    "The '{branch_name}' branch should have the line '{expected_content}' "
    "added to story.txt."
)
SUCCESS_MESSAGE = (
    "Excellent work! You've successfully created branches from a "
    "previous commit and explored alternative storylines!"
)


def get_commit_from_message(
    commits: List[GitAutograderCommit], message: str
) -> Optional[GitAutograderCommit]:
    """Find a commit with the given message from a list of commits."""
    for commit in commits:
        if message.strip() == commit.commit.message.strip():
            return commit
    return None


def verify_branch(
    branch_name: str,
    expected_start_commit: GitAutograderCommit,
    expected_content: str,
    exercise: GitAutograderExercise,
) -> None:
    """
    Check that the given branch exists, starts from the expected commit,
    and contains the expected content in story.txt.
    """
    branch_helper = exercise.repo.branches
    if not branch_helper.has_branch(branch_name):
        raise exercise.wrong_answer([MISSING_BRANCH.format(branch_name=branch_name)])

    branch = branch_helper.branch(branch_name)
    latest_commit = branch.latest_commit

    if latest_commit.hexsha == expected_start_commit.hexsha:
        raise exercise.wrong_answer([MISSING_COMMIT.format(branch_name=branch_name)])

    if expected_start_commit.hexsha not in [
        parent.hexsha for parent in latest_commit.commit.parents
    ]:
        raise exercise.wrong_answer([WRONG_START.format(branch_name=branch_name)])

    with latest_commit.file("story.txt") as content:
        if content is None:
            raise exercise.wrong_answer([MISSING_STORY_FILE])

        if expected_content not in content:
            raise exercise.wrong_answer(
                [
                    WRONG_CONTENT.format(
                        branch_name=branch_name, expected_content=expected_content
                    )
                ]
            )


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    commits = exercise.repo.branches.branch("main").commits
    describe_location_commit = get_commit_from_message(commits, "Describe location")

    if describe_location_commit is None:
        raise exercise.wrong_answer([MISSING_LOCATION_COMMIT])

    verify_branch(
        branch_name="visitor-line",
        expected_start_commit=describe_location_commit,
        expected_content="I heard someone knocking at the door.",
        exercise=exercise,
    )

    verify_branch(
        branch_name="sleep-line",
        expected_start_commit=describe_location_commit,
        expected_content="I fell asleep on the couch.",
        exercise=exercise,
    )

    return exercise.to_output(
        [SUCCESS_MESSAGE],
        GitAutograderStatus.SUCCESSFUL,
    )

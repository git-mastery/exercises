from typing import Optional

from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
    GitAutograderCommit,
)

from git.objects.commit import Commit

BRANCH_MISSING = "The '{branch_name}' branch is missing."
COMMIT_MISSING = "No commits were made in the '{branch_name}' branch."
WRONG_START = "The '{branch_name}' branch should start from the second commit (with message 'Describe location')."
WRONG_CONTENT = "The '{branch_name}' branch should have the line '{expected_content}' added to story.txt."

def get_commit_from_message(exercise: GitAutograderExercise, message: str) -> Optional[Commit]:
    """Find a commit with the given message."""
    commits = list(exercise.repo.repo.iter_commits(all=True))
    for commit in commits:
        if message.strip() == commit.message.strip():
            return commit
    return None
    
def check_file_changes(
        branch_name: str,
        expected_content: str,
        exercise: GitAutograderExercise
    ) -> None:
    
    latest_commit = exercise.repo.branches.branch(branch_name).latest_commit
    with latest_commit.file("story.txt") as content:
        if expected_content not in content:
            raise exercise.wrong_answer([WRONG_CONTENT.format(
                branch_name=branch_name,
                expected_content=expected_content
            )])
    
    return

def check_branch_structure(
        branch_name: str, 
        expected_start_commit: Commit,
        exercise: GitAutograderExercise
    ) -> None:

    # Check if branch exists
    branch_helper = exercise.repo.branches
    if not branch_helper.has_branch(branch_name):
        raise exercise.wrong_answer([BRANCH_MISSING.format(branch_name=branch_name)])
    
    branch = branch_helper.branch(branch_name)
    latest_commit = branch.latest_commit.commit

    # Check that user made commits in the branch
    if latest_commit == expected_start_commit:
        raise exercise.wrong_answer([COMMIT_MISSING.format(branch_name=branch_name)])

    # Check that branch starts from correct commit
    if not expected_start_commit in latest_commit.parents:
        raise exercise.wrong_answer([WRONG_START.format(branch_name=branch_name)])

    return


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    
    describe_location_commit = get_commit_from_message(exercise, "Describe location")

    check_branch_structure(
        branch_name="visitor-line",
        expected_start_commit=describe_location_commit,
        exercise=exercise
    )

    check_branch_structure(
        branch_name="sleep-line",
        expected_start_commit=describe_location_commit,
        exercise=exercise
    )

    check_file_changes(
        branch_name="visitor-line",
        expected_content="I heard someone knocking at the door.",
        exercise=exercise
    )

    check_file_changes(
        branch_name="sleep-line",
        expected_content="I fell asleep on the couch.",
        exercise=exercise
    )

    return exercise.to_output(
        [
            "Excellent work! You've successfully created branches from a previous commit and explored alternative storylines!"
        ],
        GitAutograderStatus.SUCCESSFUL,
    )


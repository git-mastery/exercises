from typing import Optional

from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
    GitAutograderBranch,
    GitAutograderCommit,
)

MAIN_BRANCH_CHANGED = "The 'main' branch has been changed. Please ensure it remains unchanged for this exercise."
BRANCH_MISSING = "The '{branch_name}' branch is missing."
WRONG_START = "The '{branch_name}' branch should start from the second commit (with message 'Describe location')."
WRONG_CONTENT = "The '{branch_name}' branch should have the line '{expected_content}' added to story.txt."
NO_COMMIT = "You need to commit the changes in the '{branch_name}' branch."

def get_commit_from_message(exercise: GitAutograderExercise, message: str) -> Optional[GitAutograderCommit]:
    """Find a commit with the given message."""
    commits = list(exercise.repo.repo.iter_commits(all=True))
    for commit in commits:
        if message.strip() == commit.message.strip():
            return commit
    return None

def check_main_branch_unchanged(exercise: GitAutograderExercise) -> None:
    """Check that the main branch has not been changed."""
    branch_helper = exercise.repo.branches
    commits = branch_helper.branch("main").commits
    
    if len(commits) != 3:
        raise exercise.wrong_answer([MAIN_BRANCH_CHANGED])
    
def check_branch_changes(
        branch_name: str,
        prev_commit: GitAutograderCommit,
        expected_content: str,
        expected_filename: str,
        exercise: GitAutograderExercise
    ) -> None:
    """Check that the latest commit in the branch has the expected changes in the expected file."""
    print(f"Checking changes in branch {branch_name}...")
    latest_commit = exercise.repo.branches.branch(branch_name).latest_commit
    with latest_commit.file("story.txt") as content:
        print(content)
        if not content:
            raise exercise.wrong_answer([WRONG_CONTENT.format(
                branch_name=branch_name,
                expected_content=expected_content
            )])
        if expected_content not in content:
            raise exercise.wrong_answer([WRONG_CONTENT.format(
                branch_name=branch_name,
                expected_content=expected_content
            )])
    
    return

def check_branch_structure(
        branch_name: str, 
        expected_branch_length: int,
        expected_start_commit: GitAutograderCommit,
        exercise: GitAutograderExercise
    ) -> None:

    # Check if branch exists
    branch_helper = exercise.repo.branches
    if not branch_helper.has_branch(branch_name):
        raise exercise.wrong_answer([BRANCH_MISSING.format(branch_name=branch_name)])
    
    # Check that user made commits in the branch
    branch = branch_helper.branch(branch_name)
    latest_commit = branch.latest_commit
    print("branch", branch_name, len(list(branch.commits)))
    # if latest_commit == expected_start_commit:
    #     raise exercise.wrong_answer([WRONG_START.format(branch_name=branch_name)])

    # Check that branch starts from correct commit
    if not latest_commit.is_child(expected_start_commit):
        raise exercise.wrong_answer([WRONG_START.format(branch_name=branch_name)])

    return


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    # Find the "Describe location" commit
    describe_location_commit = get_commit_from_message(exercise, "Describe location")

    check_branch_structure(
        branch_name="visitor-line",
        expected_branch_length=3,
        expected_start_commit=describe_location_commit,
        exercise=exercise
    )

    check_branch_structure(
        branch_name="sleep-line",
        expected_branch_length=3,
        expected_start_commit=describe_location_commit,
        exercise=exercise
    )

    check_branch_changes(
        branch_name="visitor-line",
        prev_commit=describe_location_commit,
        expected_content="I heard someone knocking at the door.",
        expected_filename="story.txt",
        exercise=exercise
    )

    check_branch_changes(
        branch_name="sleep-line",
        prev_commit=describe_location_commit,
        expected_content="I fell asleep on the couch.",
        expected_filename="story.txt",
        exercise=exercise
    )

    return exercise.to_output(
        [
            "Excellent work! You've successfully created branches from a previous commit and explored alternative storylines!"
        ],
        GitAutograderStatus.SUCCESSFUL,
    )


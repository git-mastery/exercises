from typing import List
from git_autograder import (
    GitAutograderCommit,
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

BRANCH_MISSING = "The local {branch} branch is not created."
BRANCH_NOT_TRACKING = "The local {branch} branch does not track origin/{branch}."
REMOTE_COMMIT_MISSING = "New commit in the remote {branch} branch is not pulled to the local {branch} branch."
LOCAL_COMMIT_MISSING = "The original local commit on DEF is missing. " \
"You may have lost your work instead of merging."


def get_commit_from_message(commits: List[GitAutograderCommit], message: str) \
    -> GitAutograderCommit | None:
    """Find a commit with the given message from a list of commits."""
    for commit in commits:
        if message.strip() == commit.commit.message.strip():
            return commit
    return None

def get_commit_from_hexsha(commits: List[GitAutograderCommit], hexsha: str) \
    -> GitAutograderCommit | None:
    """Find a commit with the given hexsha from a list of commits."""
    for commit in commits:
        if hexsha.strip() == commit.commit.hexsha.strip():
            return commit
    return None

def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    repo = exercise.repo 
    comments = []

    if not repo.branches.has_branch("STU"):
        comments.append(BRANCH_MISSING.format(branch="STU"))
    else:
        try:
            exercise.repo.repo.refs["origin/STU"]
        except (IndexError, KeyError):
            comments.append(BRANCH_NOT_TRACKING.format(branch="STU"))
            pass 

    if not repo.branches.has_branch("VWX"):
        comments.append(BRANCH_MISSING.format(branch="VWX"))
    else:
        try:
            exercise.repo.repo.refs["origin/VWX"]
        except (IndexError, KeyError):
            comments.append(BRANCH_NOT_TRACKING.format(branch="VWX"))
            pass 

    if not repo.branches.has_branch("ABC"):
        comments.append(BRANCH_MISSING.format(branch="ABC"))
    else:
        try:
            remote_abc = exercise.repo.repo.refs["origin/ABC"]
            abc_commits = repo.branches.branch("ABC").commits
            if not get_commit_from_hexsha(abc_commits, remote_abc.commit.hexsha):
                comments.append(REMOTE_COMMIT_MISSING.format(branch="ABC"))
        except (IndexError, KeyError):
            comments.append(BRANCH_NOT_TRACKING.format(branch="ABC"))
            pass 
            
    if not repo.branches.has_branch("DEF"):
        comments.append(BRANCH_MISSING.format(branch="DEF"))
    else:
        def_commits = repo.branches.branch("DEF").commits
        if not get_commit_from_message(def_commits, "Add 'documentation'"):
            comments.append(LOCAL_COMMIT_MISSING)
        try:
            remote_def = exercise.repo.repo.refs["origin/DEF"]
            if not get_commit_from_hexsha(def_commits, remote_def.commit.hexsha):
                comments.append(REMOTE_COMMIT_MISSING.format(branch="DEF"))
        except (IndexError, KeyError):
            comments.append(BRANCH_NOT_TRACKING.format(branch="DEF"))
            pass 

    if comments:
        raise exercise.wrong_answer(comments)
    return exercise.to_output([
        "Great work! All required branches are present and correctly set up."
    ], GitAutograderStatus.SUCCESSFUL)

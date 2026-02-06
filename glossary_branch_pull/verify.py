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
LOCAL_COMMIT_MISSING = (
    "The original local commit on DEF is missing. "
    "You may have lost your work instead of merging."
)


def get_commit_from_message(
    commits: List[GitAutograderCommit], message: str
) -> GitAutograderCommit | None:
    """Find a commit with the given message from a list of commits."""
    for commit in commits:
        if message.strip() == commit.commit.message.strip():
            return commit
    return None


def get_commit_from_hexsha(
    commits: List[GitAutograderCommit], hexsha: str
) -> GitAutograderCommit | None:
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
        stu_branch = repo.branches.branch("STU").branch
        remote_stu = stu_branch.tracking_branch()
        if not remote_stu or remote_stu.name != "origin/STU":
            comments.append(BRANCH_NOT_TRACKING.format(branch="STU"))

    if not repo.branches.has_branch("VWX"):
        comments.append(BRANCH_MISSING.format(branch="VWX"))
    else:
        vwx_branch = repo.branches.branch("VWX").branch
        remote_vwx = vwx_branch.tracking_branch()
        if not remote_vwx or remote_vwx.name != "origin/VWX":
            comments.append(BRANCH_NOT_TRACKING.format(branch="VWX"))

    if not repo.branches.has_branch("ABC"):
        comments.append(BRANCH_MISSING.format(branch="ABC"))
    else:
        abc_commits = repo.branches.branch("ABC").commits
        abc_branch = repo.branches.branch("ABC").branch
        remote_abc = abc_branch.tracking_branch()
        if not remote_abc or remote_abc.name != "origin/ABC":
            comments.append(BRANCH_NOT_TRACKING.format(branch="ABC"))
        elif not get_commit_from_hexsha(abc_commits, remote_abc.commit.hexsha):
            comments.append(REMOTE_COMMIT_MISSING.format(branch="ABC"))

    if not repo.branches.has_branch("DEF"):
        comments.append(BRANCH_MISSING.format(branch="DEF"))
    else:
        def_commits = repo.branches.branch("DEF").commits
        if not get_commit_from_message(def_commits, "Add 'documentation'"):
            comments.append(LOCAL_COMMIT_MISSING)
        def_branch = repo.branches.branch("DEF").branch
        remote_def = def_branch.tracking_branch()
        if not remote_def or remote_def.name != "origin/DEF":
            comments.append(BRANCH_NOT_TRACKING.format(branch="DEF"))
        elif not get_commit_from_hexsha(def_commits, remote_def.commit.hexsha):
            comments.append(REMOTE_COMMIT_MISSING.format(branch="DEF"))

    if comments:
        raise exercise.wrong_answer(comments)
    return exercise.to_output(
        ["Great work! All required branches are present and correctly set up."],
        GitAutograderStatus.SUCCESSFUL,
    )

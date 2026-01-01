import os
import subprocess
from typing import List, Optional

from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

IMPROPER_GH_CLI_SETUP = "Your Github CLI is not setup correctly"

TAG_1_NAME = "v1.0"
TAG_2_NAME = "v2.0"
TAG_DELETE_NAME = "beta"

TAG_1_MISSING = f"Tag {TAG_1_NAME} is missing, did you push it to the remote?"
TAG_2_MISSING = f"Tag {TAG_2_NAME} is missing, did you push it to the remote?"
TAG_DELETE_NOT_REMOVED = f"Tag {TAG_DELETE_NAME} is still on the remote!"


def run_command(command: List[str]) -> Optional[str]:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            env=dict(os.environ, **{"GH_PAGER": "cat"}),
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def get_username() -> Optional[str]:
    return run_command(["gh", "api", "user", "-q", ".login"])


def get_remote_tags(username: str, exercise: GitAutograderExercise) -> List[str]:
    raw_tags = exercise.repo.repo.git.ls_remote("--tags")
    if raw_tags is None:
        return []
    return [line.split("/")[2] for line in raw_tags.strip().splitlines()]


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    username = get_username()
    if username is None:
        raise exercise.wrong_answer([IMPROPER_GH_CLI_SETUP])

    tag_names = get_remote_tags(username, exercise)

    comments = []

    if TAG_1_NAME not in tag_names:
        comments.append(TAG_1_MISSING)

    if TAG_2_NAME not in tag_names:
        comments.append(TAG_2_MISSING)

    if TAG_DELETE_NAME in tag_names:
        comments.append(TAG_DELETE_NOT_REMOVED)

    if comments:
        raise exercise.wrong_answer(comments)

    return exercise.to_output(
        [
            "Wonderful! You have successfully synced the local tags with the remote tags!"
        ],
        GitAutograderStatus.SUCCESSFUL,
    )

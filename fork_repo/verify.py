import os
import subprocess
from typing import List, Optional

from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)

# NOTE: that we create functions for each command to allow unit testing to mock the
# return values directly.

ORIGINAL_FORK_NAME = "gm-shapes"
IMPROPER_GH_CLI_SETUP = "Your Github CLI is not setup correctly"
NO_FORK_FOUND = f"No fork of git-mastery/{ORIGINAL_FORK_NAME} found. Remember to fork it from https://github.com/git-mastery/gm-shapes and keep the name as gm-shapes"
NOT_GIT_MASTERY_FORK = f"Your fork was not from git-mastery/{ORIGINAL_FORK_NAME}. Remember to fork it from https://github.com/git-mastery/gm-shapes and keep the name as gm-shapes"


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


def has_fork(username: str) -> bool:
    result = run_command(
        [
            "gh",
            "repo",
            "view",
            f"{username}/{ORIGINAL_FORK_NAME}",
            "--json",
            "isFork",
            "--jq",
            ".isFork",
        ]
    )
    return result is not None and result == "true"


def is_parent_git_mastery(username: str) -> bool:
    result = run_command(
        [
            "gh",
            "repo",
            "view",
            f"{username}/{ORIGINAL_FORK_NAME}",
            "--json",
            "parent",
            "--jq",
            ".parent.owner.login",
        ]
    )
    return result is not None and result == "git-mastery"


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    username = get_username()
    if username is None:
        raise exercise.wrong_answer([IMPROPER_GH_CLI_SETUP])

    if not has_fork(username):
        raise exercise.wrong_answer([NO_FORK_FOUND])

    if not is_parent_git_mastery(username):
        raise exercise.wrong_answer([NOT_GIT_MASTERY_FORK])

    return exercise.to_output(
        ["Great work creating a fork with Github!"], GitAutograderStatus.SUCCESSFUL
    )

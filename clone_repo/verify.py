import os
import subprocess
from typing import List, Optional
from urllib.parse import urlparse

from git import Remote
from git.repo import Repo
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
ORIGIN_MISSING = "The remote 'origin' is missing!"
UPSTREAM_MISSING = "The remote 'upstream' is missing!"
ORIGIN_WRONG = "The origin remote does not point to your fork!"
UPSTREAM_WRONG = "The upstream remote does not point to the original repository!"
CLONE_MISSING = "Clone named shapes is missing! Remember to clone your fork using the name 'shapes', not 'gm-shapes'!"


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


def has_shapes_folder() -> bool:
    return os.path.isdir("shapes")


def is_remote(remote_url: str, owner: str, repo_name: str) -> bool:
    # TODO: copied from git-autograder, might need to make this a proper function to
    # use next time
    if remote_url.startswith("https://github.com"):
        # https://github.com/<owner>/<repo>.git
        parsed = urlparse(remote_url)
        path_parts = parsed.path.strip("/").split("/")
    elif remote_url.startswith("git@github.com"):
        # git@github.com:<owner>/<repo>.git
        components = remote_url.split(":")
        if len(components) != 2:
            return False
        path_parts = components[1].split("/")
    else:
        return False

    owner_part, repo_part = path_parts
    if repo_part.endswith(".git"):
        repo_part = repo_part[:-4]

    return owner_part == owner and repo_part == repo_name


def remote(remote_name: str) -> Optional[Remote]:
    repo = Repo("shapes")
    try:
        remote = repo.remote(remote_name)
        return remote
    except Exception:
        return None


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    username = get_username()
    if username is None:
        raise exercise.wrong_answer([IMPROPER_GH_CLI_SETUP])

    if not has_fork(username):
        raise exercise.wrong_answer([NO_FORK_FOUND])

    if not is_parent_git_mastery(username):
        raise exercise.wrong_answer([NOT_GIT_MASTERY_FORK])

    if not has_shapes_folder():
        raise exercise.wrong_answer([CLONE_MISSING])

    origin_remote = remote("origin")
    if not origin_remote:
        raise exercise.wrong_answer([ORIGIN_MISSING])
    if not is_remote(origin_remote.url, username, "gm-shapes"):
        raise exercise.wrong_answer([ORIGIN_WRONG])

    upstream_remote = remote("upstream")
    if not upstream_remote:
        raise exercise.wrong_answer([UPSTREAM_MISSING])
    if not is_remote(upstream_remote.url, "git-mastery", "gm-shapes"):
        raise exercise.wrong_answer([UPSTREAM_WRONG])

    return exercise.to_output(
        ["Great work creating a clone of a fork from Github!"],
        GitAutograderStatus.SUCCESSFUL,
    )

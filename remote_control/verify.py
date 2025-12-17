import os
import subprocess
from typing import Optional

from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)


# TODO: We should unify how we call gh from within Python
def get_github_username() -> Optional[str]:
    try:
        result = subprocess.run(
            ["gh", "api", "user", "-q", ".login"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def has_public_repo(username: str) -> bool:
    try:
        result = subprocess.run(
            [
                "gh",
                "repo",
                "view",
                f"{username}/gitmastery-{username}-remote-control",
                "--json",
                "visibility",
                "--jq",
                ".visibility",
            ],
            capture_output=True,
            text=True,
            check=True,
            env=dict(os.environ, **{"GH_PAGER": "cat"}),
        )
        return result.stdout.strip() == "PUBLIC"
    except subprocess.CalledProcessError:
        return False


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    username = get_github_username()
    if username is None:
        raise exercise.wrong_answer(["Your Github CLI is not setup correctly"])

    print(f"Create a repo called gitmastery-{username}-remote-control")
    url = input("Enter the url of your remote repository: ")
    if (
        not url.strip()
        == f"https://github.com/{username}/gitmastery-{username}-remote-control"
    ):
        raise exercise.wrong_answer(["That is not the right Github url!"])

    if has_public_repo(username):
        return exercise.to_output(
            [
                "Great work setting up a public remote repository!",
            ],
            GitAutograderStatus.SUCCESSFUL,
        )
    else:
        raise exercise.wrong_answer(
            [
                "The remote repository url you provided either does not exist or is private. Try again!"
            ]
        )

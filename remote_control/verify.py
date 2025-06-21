import subprocess
from typing import List, Optional

from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)


def run_command(command: List[str]) -> Optional[str]:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    username = run_command(["gh", "api", "user", "-q", ".login"])
    if username is None:
        raise exercise.wrong_answer(["Your Github CLI is not setup correctly"])

    username = username.strip()

    print(f"Create a repo called gitmastery-{username}-remote-control")
    url = input("Enter the url of your remote repository: ")
    if not url.startswith(
        f"https://github.com/{username}/gitmastery-{username}-remote-control"
    ):
        raise exercise.wrong_answer(["That is not the right Github url!"])

    code = subprocess.call(["git", "ls-remote", url, "--quiet"])
    if code == 0:
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

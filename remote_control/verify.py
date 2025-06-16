import subprocess
from datetime import datetime
from typing import List, Optional

import pytz
from git_autograder import GitAutograderOutput, GitAutograderStatus


def run_command(command: List[str]) -> Optional[str]:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return None


def verify() -> GitAutograderOutput:
    started_at = datetime.now(tz=pytz.UTC)

    username = run_command(["gh", "api", "user", "-q", ".login"])
    if username is None:
        return GitAutograderOutput(
            status=GitAutograderStatus.UNSUCCESSFUL,
            started_at=started_at,
            completed_at=datetime.now(tz=pytz.UTC),
            comments=["Your Github CLI is not setup correctly"],
            exercise_name="remote-control",
        )

    print(f"Create a repo called gitmastery-{username}-remote-control")
    url = input("Enter the url of your remote repository: ")
    if not url.startswith(f"https://github.com/gitmastery-{username}-remote-control"):
        return GitAutograderOutput(
            status=GitAutograderStatus.UNSUCCESSFUL,
            started_at=started_at,
            completed_at=datetime.now(tz=pytz.UTC),
            comments=["That is not the right Github URL!"],
            exercise_name="remote-control",
        )

    code = subprocess.call(["git", "ls-remote", url, "--quiet"])
    if code == 0:
        return GitAutograderOutput(
            status=GitAutograderStatus.SUCCESSFUL,
            started_at=started_at,
            completed_at=datetime.now(tz=pytz.UTC),
            comments=["Great work setting up a public remote repository!"],
            exercise_name="remote-control",
        )
    else:
        return GitAutograderOutput(
            status=GitAutograderStatus.UNSUCCESSFUL,
            started_at=started_at,
            completed_at=datetime.now(tz=pytz.UTC),
            comments=[
                "The remote repository url you provided either does not exist or is private. Try again!"
            ],
            exercise_name="remote-control",
        )

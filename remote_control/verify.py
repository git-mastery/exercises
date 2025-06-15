import subprocess
from datetime import datetime

import pytz
from git_autograder import GitAutograderOutput, GitAutograderStatus


def verify() -> GitAutograderOutput:
    started_at = datetime.now(tz=pytz.UTC)
    url = input("Enter the url of your remote repository: ")
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
                "The remote repository url you provided either does not exist, or is private. Try again!"
            ],
            exercise_name="remote-control",
        )

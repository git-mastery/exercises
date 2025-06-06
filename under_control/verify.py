from datetime import datetime
from pathlib import Path

import pytz
from git_autograder import GitAutograderOutput
from git_autograder.status import GitAutograderStatus


def verify() -> GitAutograderOutput:
    started_at = datetime.now(tz=pytz.UTC)

    current = Path.cwd()
    for parent in [current] + list(current.parents):
        if (parent / ".gitmastery-exercise.json").is_file():
            if (parent / ".git").is_dir():
                return GitAutograderOutput(
                    status=GitAutograderStatus.SUCCESSFUL,
                    started_at=started_at,
                    completed_at=datetime.now(tz=pytz.UTC),
                    comments=[
                        "You successfully used git init to initialize this folder as a Git repository!"
                    ],
                    exercise_name="under-control",
                )
    return GitAutograderOutput(
        status=GitAutograderStatus.UNSUCCESSFUL,
        started_at=started_at,
        completed_at=datetime.now(tz=pytz.UTC),
        comments=["This folder isn't a Git repository yet!"],
        exercise_name="under-control",
    )

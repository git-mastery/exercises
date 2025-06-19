import os
import subprocess
from typing import List, Optional
from datetime import datetime
import pytz

from git_autograder import GitAutograderOutput, GitAutograderRepo, GitAutograderStatus

MISSING_REPO = "You should have {repo} in your exercise folder. You might want to re-download the exercise."


def run_command(command: List[str], verbose: bool) -> Optional[str]:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )
        if verbose:
            print(result.stdout)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        if verbose:
            print(e.stderr)
        return None


def verify() -> GitAutograderOutput:
    comments: List[str] = []
    started_at = datetime.now(tz=pytz.UTC)

    username = run_command(["gh", "api", "user", "-q", ".login"], verbose=False)
    repo_name = f"{username}-gitmastery-push-over"

    if not os.path.isdir(repo_name):
        return GitAutograderOutput(
            status=GitAutograderStatus.UNSUCCESSFUL,
            started_at=started_at,
            completed_at=datetime.now(tz=pytz.UTC),
            comments=[MISSING_REPO.format(repo=repo_name)],
        )

    repo = GitAutograderRepo("push-over", repo_name)

    return repo.to_output(comments)

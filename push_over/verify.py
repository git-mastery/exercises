import os
import subprocess
from datetime import datetime
from typing import List, Optional

import pytz
from git_autograder import GitAutograderOutput, GitAutograderRepo, GitAutograderStatus

MISSING_REPO = "You should have {repo} in your exercise folder. You might want to re-download the exercise."
MISSING_COMMIT = "You should have made a separate commit!"
MISSING_COMMIT_REMOTE = (
    "You might have forgotten to push your commit to the remote repository."
)


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

    main_branch = repo.branches.branch("main")
    if len(main_branch.commits) == 1:
        raise repo.wrong_answer([MISSING_COMMIT])

    origin_remote = repo.remotes.remote("origin")
    origin_remote.remote.fetch()
    remote_branch = repo.repo.refs["origin/main"]
    remote_commits = list(repo.repo.iter_commits(remote_branch))

    if len(remote_commits) == 1:
        raise repo.wrong_answer([MISSING_COMMIT_REMOTE])

    return repo.to_output(
        ["Great work pushing changes to the remote!"],
        status=GitAutograderStatus.SUCCESSFUL,
    )

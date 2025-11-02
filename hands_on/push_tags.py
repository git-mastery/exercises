import os
import subprocess
from exercise_utils.cli import run_command
from exercise_utils.git import tag_with_options, annotated_tag_with_options

__requires_git__ = True
__requires_github__ = True

REPO_NAME = "samplerepo-preferences"


def download(verbose: bool):

    # Cannot use run_command function because returned object should not be None.
    username = subprocess.run(
        ["gh", "api", "user", "-q", ".login"],
        capture_output=True,
        text=True,
    ).stdout.strip()

    # Cannot use run_command function because return code is needed.
    check_repo = subprocess.run(
        ["gh", "repo", "view", f"{username}/{REPO_NAME}"],
        capture_output=True,
        text=True,
    )

    if check_repo.returncode == 0:
        print(f"{username}/{REPO_NAME} already exists, the fork repo will be named as {username}/{REPO_NAME}-1")

    run_command(["gh", "repo", "fork", f"git-mastery/{REPO_NAME}", REPO_NAME, "--clone"], verbose)

    os.chdir(REPO_NAME)

    tag_with_options("v1.0", ["HEAD~1"], verbose)
    annotated_tag_with_options("v0.9", ["HEAD~2", "-m", "First beta release"], verbose)

    pass

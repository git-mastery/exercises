import os
import subprocess
from exercise_utils.cli import run_command
from exercise_utils.git import tag_with_options, annotated_tag_with_options

__requires_git__ = True
__requires_github__ = True

REPO_NAME = "samplerepo-preferences"

def get_username() -> str:
    # Cannot use run_command function because returned object should not be None.
    return subprocess.run(
        ["gh", "api", "user", "-q", ".login"],
        capture_output=True,
        text=True,
    ).stdout.strip()


def check_same_repo_name(username: str, repo_name: str) -> None:
    # Cannot use run_command function because return code is needed.
    check_repo = subprocess.run(
        ["gh", "repo", "view", f"{username}/{repo_name}"],
        capture_output=True,
        text=True,
    )
    if check_repo.returncode == 0:
        print(f"Warning: {username}/{REPO_NAME} already exists, the fork repo will be "
              f"named as {username}/{REPO_NAME}-1")

def check_existing_fork(username: str, fork_owner_name: str, repo_name: str) -> None:
    try:
        result = subprocess.run(
            ["gh",
            "api",
            f"repos/{fork_owner_name}/{repo_name}/forks",
            "-q",
            f'''.[] | .owner.login | select(. =="{username}")''',
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        if result.stdout == username:
            print(f"ERROR: A fork of {fork_owner_name}/{repo_name} already exists! "
                "Please delete the fork and run this download operation again.\n"
                "!Aborting...")
            exit(1)
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        exit(1)




def download(verbose: bool):
    username = get_username()
    check_existing_fork(username, "git-mastery", REPO_NAME)
    check_same_repo_name(username, REPO_NAME)

    run_command(["gh", "repo", "fork", f"git-mastery/{REPO_NAME}", REPO_NAME, "--clone"], verbose)

    os.chdir(REPO_NAME)

    tag_with_options("v1.0", ["HEAD~1"], verbose)
    annotated_tag_with_options("v0.9", ["HEAD~2", "-m", "First beta release"], verbose)

    pass

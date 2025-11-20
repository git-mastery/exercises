import os
from exercise_utils.cli import run
from exercise_utils.git import tag_with_options, annotated_tag_with_options
from exercise_utils.github_cli import clone_repo_with_gh, fork_repo, get_github_username, has_repo

__requires_git__ = True
__requires_github__ = True

def check_existing_fork(username: str, fork_owner_name: str, repo_name: str, verbose: bool) -> None:
    result = run(
        ["gh",
        "api",
        f"repos/{fork_owner_name}/{repo_name}/forks",
        "-q",
        f'''.[] | .owner.login | select(. =="{username}")''',
        ],
        verbose
    )
    if result.is_success():
        if result.stdout == username:
            print(f"ERROR: A fork of {fork_owner_name}/{repo_name} already exists! "
                "Please delete the fork and run this download operation again.\n"
                "!Aborting...")
            exit(1)

def check_same_repo_name(username: str, repo_name: str, verbose: bool) -> str:
    if has_repo(repo_name, False, verbose):
        print(f"Warning: {username}/{repo_name} already exists, the fork repo will be "
              f"named as {username}/{repo_name}-1")
        return repo_name + "-1"
    return repo_name

def download(verbose: bool):
    REPO_NAME = "samplerepo-preferences"
    FORK_NAME = "gitmastery-samplerepo-preferences"
    username = get_github_username(verbose)

    check_existing_fork(username, "git-mastery", REPO_NAME, verbose)
    NEW_FORK_NAME = check_same_repo_name(username, FORK_NAME, verbose)

    fork_repo(f"git-mastery/{REPO_NAME}", NEW_FORK_NAME, verbose)
    clone_repo_with_gh(NEW_FORK_NAME, verbose, FORK_NAME)


    os.chdir(FORK_NAME)

    tag_with_options("v1.0", ["HEAD~1"], verbose)
    annotated_tag_with_options("v0.9", ["HEAD~2", "-m", "First beta release"], verbose)


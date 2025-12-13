import os
from exercise_utils.git import tag_with_options
from exercise_utils.github_cli import (
    clone_repo_with_gh,
    fork_repo,
    get_fork_name,
    get_github_username,
    has_fork,
    has_repo,
)

__requires_git__ = True
__requires_github__ = True


def check_same_repo_name(username: str, repo_name: str, verbose: bool) -> str:
    if has_repo(repo_name, False, verbose):
        print(
            f"Warning: {username}/{repo_name} already exists, the fork repo will be "
            f"named as {username}/{repo_name}-1"
        )
        return repo_name + "-1"
    return repo_name


def download(verbose: bool):
    REPO_NAME = "samplerepo-preferences"
    FORK_NAME = "gitmastery-samplerepo-preferences"
    username = get_github_username(verbose)

    if has_fork(REPO_NAME, "git-mastery", username, verbose):
        existing_name = get_fork_name(REPO_NAME, "git-mastery", username, verbose)
        clone_repo_with_gh(existing_name, verbose, FORK_NAME)
    else:
        NEW_FORK_NAME = check_same_repo_name(username, FORK_NAME, verbose)
        fork_repo(f"git-mastery/{REPO_NAME}", NEW_FORK_NAME, verbose)
        clone_repo_with_gh(NEW_FORK_NAME, verbose, FORK_NAME)

    os.chdir(FORK_NAME)

    tag_with_options("v1.0", ["HEAD~1"], verbose)
    tag_with_options("v0.9", ["HEAD~2", "-a", "-m", "First beta release"], verbose)

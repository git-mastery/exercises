import os
from exercise_utils.git import (
    tag,
    tag_with_options,
)
from exercise_utils.github_cli import (
    get_github_username,
    has_repo,
    fork_repo,
    delete_repo,
    clone_repo_with_gh,
)

__requires_git__ = True
__requires_github__ = True


TARGET_REPO = "git-mastery/samplerepo-preferences"
LOCAL_DIR = "gitmastery-samplerepo-preferences"


def download(verbose: bool):
    username = get_github_username(verbose)
    full_repo_name = f"{username}/{LOCAL_DIR}"

    if has_repo(full_repo_name, True, verbose):
        delete_repo(full_repo_name, verbose)

    fork_repo(TARGET_REPO, LOCAL_DIR, verbose)
    clone_repo_with_gh(full_repo_name, verbose)

    os.chdir(LOCAL_DIR)
    tag("v1.0", verbose)
    tag_with_options("v0.9", ["HEAD~2", "-a", "-m", "First beta release"], verbose)

from exercise_utils.git import clone_repo_with_git
from exercise_utils.github_cli import (
    get_github_username,
    has_repo,
    fork_repo_all_branches,
    delete_repo,
)

__requires_git__ = True
__requires_github__ = True

TARGET_REPO = "git-mastery/samplerepo-company"
LOCAL_DIR = "gitmastery-samplerepo-company"


def download(verbose: bool):
    username = get_github_username(verbose)
    full_repo_name = f"{username}/{LOCAL_DIR}"
    repo_url = f"https://github.com/{full_repo_name}"

    if has_repo(full_repo_name, True, verbose):
        delete_repo(full_repo_name, verbose)

    fork_repo_all_branches(TARGET_REPO, LOCAL_DIR, verbose)
    clone_repo_with_git(repo_url, verbose, "samplerepo-company")
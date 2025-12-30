from repo_smith.repo_smith import RepoSmith

from exercise_utils.github_cli import (
    get_fork_name,
    get_github_username,
    has_fork,
    has_repo,
)

__requires_git__ = True
__requires_github__ = True


def check_same_repo_name(rs: RepoSmith, username: str, repo_name: str) -> str:
    if has_repo(rs, username, repo_name, is_fork=False):
        print(
            f"Warning: {username}/{repo_name} already exists, the fork repo will be "
            f"named as {username}/{repo_name}-1"
        )
        return repo_name + "-1"
    return repo_name


def download(rs: RepoSmith):
    REPO_NAME = "samplerepo-preferences"
    FORK_NAME = "gitmastery-samplerepo-preferences"
    username = get_github_username(rs)

    if has_fork(rs, "git-mastery", REPO_NAME, username):
        existing_name = get_fork_name(rs, "git-mastery", REPO_NAME, username)
        rs.gh.repo_clone(username, existing_name, FORK_NAME)
    else:
        NEW_FORK_NAME = check_same_repo_name(rs, username, FORK_NAME)
        rs.gh.repo_fork("git-mastery", REPO_NAME, fork_name=NEW_FORK_NAME)
        rs.gh.repo_clone(username, NEW_FORK_NAME, FORK_NAME)

    rs.files.cd(FORK_NAME)

    rs.git.tag("v1.0", "HEAD~1")
    rs.git.tag("v0.9", "HEAD~2", message="First beta release", annotate=True)

from repo_smith.repo_smith import RepoSmith
from exercise_utils.github_cli import (
    get_github_username,
    has_repo,
)

__requires_git__ = True
__requires_github__ = True


TARGET_REPO = "git-mastery/samplerepo-preferences"
LOCAL_DIR = "gitmastery-samplerepo-preferences"


def download(rs: RepoSmith):
    username = get_github_username(rs)

    if has_repo(rs, username, LOCAL_DIR, is_fork=True):
        rs.gh.repo_delete(username, LOCAL_DIR)

    rs.gh.repo_fork("git-mastery", "samplerepo-preferences", fork_name=LOCAL_DIR, clone=True)

    rs.files.cd(LOCAL_DIR)
    rs.git.tag("v1.0", "HEAD~1")
    rs.git.tag("v0.9", "HEAD~1", message="First beta release", annotate=True)

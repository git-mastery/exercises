from repo_smith.repo_smith import RepoSmith

from exercise_utils.github_cli import get_github_username, has_repo

__requires_git__ = True
__requires_github__ = True


TARGET_REPO = "git-mastery/samplerepo-finances-2"
FORK_NAME = "gm-samplerepo-finances-2"
LOCAL_DIR = "samplerepo-finances"


def download(rs: RepoSmith):
    username = get_github_username(rs)

    if has_repo(rs, username, FORK_NAME, is_fork=True):
        rs.gh.repo_delete(username, FORK_NAME)

    rs.gh.repo_fork("git-mastery", "samplerepo-finances-2", fork_name=FORK_NAME)
    rs.gh.repo_clone(username, FORK_NAME, LOCAL_DIR)

    rs.files.cd(LOCAL_DIR)

    rs.git.reset("HEAD~2", hard=True)
    rs.git.run(["git", "push", "-f", "origin", "main"])

from repo_smith.repo_smith import RepoSmith

from exercise_utils.github_cli import get_github_username

__requires_git__ = True
__requires_github__ = True

REPO_NAME = "gitmastery-samplerepo-things"
UPSTREAM_REPO = "git-mastery/samplerepo-things"
WORK_DIR = "things"


def download(rs: RepoSmith):
    username = get_github_username(rs)

    rs.gh.repo_create(username, REPO_NAME, public=True)
    rs.gh.repo_clone(username, REPO_NAME, WORK_DIR)
    rs.files.cd(WORK_DIR)
    rs.git.remote_remove("origin")

    rs.git.remote_add(
        "origin",
        f"https://github.com/{username}/{REPO_NAME}",
    )
    rs.git.run(["git", "push", "-u", "origin", "main"])

from repo_smith.repo_smith import RepoSmith
from exercise_utils.github_cli import get_github_username, has_repo

__requires_git__ = True
__requires_github__ = True

REPO_NAME = "gitmastery-things"


def download(rs: RepoSmith):
    rs.files.mkdir("things")
    rs.files.cd("things")
    rs.git.init()

    rs.files.create_or_update(
        "fruits.txt",
        """
        apples
        bananas
        cherries
        dragon fruits
        """,
    )
    rs.git.add(["fruits.txt"])
    rs.git.commit(message="Add fruits.txt")

    rs.files.append("fruits.txt", "figs")
    rs.git.add(["fruits.txt"])
    rs.git.commit(message="Insert figs into fruits.txt")

    rs.files.create_or_update("colours.txt", "a file for colours")
    rs.files.create_or_update("shapes.txt", "a file for shapes")
    rs.git.add(["colours.txt", "shapes.txt"])
    rs.git.commit(message="Add colours.txt, shapes.txt")

    username = get_github_username(rs)
    if has_repo(rs, username, REPO_NAME, is_fork=False):
        rs.gh.repo_delete(username, REPO_NAME)

    rs.gh.repo_create(username, REPO_NAME, public=True)
    rs.git.remote_add("origin", f"https://github.com/{username}/{REPO_NAME}")

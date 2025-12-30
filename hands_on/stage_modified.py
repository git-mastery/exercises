from repo_smith.repo_smith import RepoSmith

__requires_git__ = True
__requires_github__ = False


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
        """,
    )
    rs.git.add(["fruits.txt"])
    rs.files.append("fruits.txt", "dragon fruits")

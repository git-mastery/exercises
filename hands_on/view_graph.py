from repo_smith.repo_smith import RepoSmith

__requires_git__ = True
__requires_github__ = False


def download(rs: RepoSmith) -> None:
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

    rs.files.append("fruits.txt", "figs\n")
    rs.git.add(["fruits.txt"])
    rs.git.commit(message="Insert figs into fruits.txt")

    rs.files.create_or_update("colours.txt", "a file for colours\n")
    rs.files.create_or_update("shapes.txt", "a file for shapes\n")
    rs.git.add(["colours.txt", "shapes.txt"])
    rs.git.commit(message="Add colours.txt, shapes.txt")

from repo_smith.repo_smith import RepoSmith

__requires_git__ = True
__requires_github__ = False


def download(rs: RepoSmith):
    rs.files.mkdir("sports")
    rs.files.cd("sports")

    rs.git.init()

    rs.files.create_or_update(
        "golf.txt",
        """
        Arnold Palmer
        Tiger Woods
        """,
    )
    rs.git.add(["golf.txt"])
    rs.git.commit(message="Add golf.txt")

    rs.files.create_or_update(
        "tennis.txt",
        """
        Pete Sampras
        Roger Federer
        Serena Williams
        """,
    )
    rs.git.add(["tennis.txt"])
    rs.git.commit(message="Add tennis.txt")

    rs.files.create_or_update(
        "football.txt",
        """
        Pele
        Maradona
        """,
    )
    rs.git.add(["football.txt"])
    rs.git.commit(message="Add football.txt")

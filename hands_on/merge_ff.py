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

    rs.git.checkout("add-swimming", branch=True)

    rs.files.create_or_update(
        "swimming.txt",
        """
        Michael Phelps
        """,
    )
    rs.git.add(["swimming.txt"])
    rs.git.commit(message="Add swimming.txt")

    rs.files.append("swimming.txt", "Ian Thorpe")
    rs.git.add(["swimming.txt"])
    rs.git.commit(message="Add Thorpe to swimming.txt")

    rs.git.checkout("main")

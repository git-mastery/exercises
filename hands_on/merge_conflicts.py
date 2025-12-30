from repo_smith.repo_smith import RepoSmith


__requires_git__ = True
__requires_github__ = False


def download(rs: RepoSmith):
    rs.files.mkdir("nouns")
    rs.files.cd("nouns")

    rs.git.init()

    rs.files.create_or_update(
        "colours.txt",
        """
        blue
        """,
    )
    rs.git.add(["colours.txt"])
    rs.git.commit(message="Add colours.txt")

    rs.git.checkout("fix1", branch=True)
    rs.files.append(
        "colours.txt",
        """
        green
        red
        white
        """,
    )
    rs.git.add(["colours.txt"])
    rs.git.commit(message="Add green, red, white")

    rs.git.checkout("main")
    rs.files.append(
        "colours.txt",
        """
        black
        red
        white
        """,
    )
    rs.git.add(["colours.txt"])
    rs.git.commit(message="Add black, red, white")

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
        dragon fruits
        """,
    )
    rs.git.add(["fruits.txt"])
    rs.git.commit(message="Add fruits.txt")

    rs.files.append(
        "fruits.txt",
        """
        elderberries
        figs
        """,
    )
    rs.git.add(["fruits.txt"])
    rs.git.commit(message="Add elderberries and figs into fruits.txt")

    rs.files.create_or_update("colours.txt", "a file for colours\n")
    rs.files.create_or_update("shapes.txt", "a file for shapes\n")
    rs.git.add(["colours.txt", "shapes.txt"])
    rs.git.commit(message="Add colours.txt, shapes.txt")
    rs.git.tag("0.9")

    rs.files.create_or_update(
        "fruits.txt",
        """
        apples, apricots
        bananas
        blueberries
        cherries
        dragon fruits
        figs
        """,
    )
    rs.git.add(["fruits.txt"])
    rs.git.commit(message="Update fruits list")

    rs.files.append("colours.txt", "bad colour\n")
    rs.git.add(["colours.txt"])
    rs.git.commit(message="Incorrectly update colours.txt")

    rs.files.append("shapes.txt", "bad shape\n")
    rs.git.add(["shapes.txt"])
    rs.git.commit(message="Incorrectly update shapes.txt")

    rs.files.append("fruits.txt", "bad fruit\n")
    rs.git.add(["fruits.txt"])
    rs.git.commit(message="Incorrectly update fruits.txt")

    rs.files.create_or_update("incorrect.txt", "bad line\n")
    rs.git.add(["incorrect.txt"])
    rs.git.commit(message="Add incorrect.txt")

    rs.files.append("colours.txt", "another bad colour\n")
    rs.git.add(["colours.txt"])

    rs.files.append("shapes.txt", "another bad shape\n")

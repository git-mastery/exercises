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
    rs.git.commit(message="Add elderberries and figs to fruits.txt")

    rs.files.create_or_update(
        "colours.txt",
        "a file for colours\n",
    )
    rs.files.create_or_update(
        "shapes.txt",
        "a file for shapes\n",
    )
    rs.git.add(["colours.txt", "shapes.txt"])
    rs.git.commit(message="Add colours.txt, shapes.txt")

    rs.git.tag("v0.9")

    # Replace the whole contents of fruits.txt
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

    rs.files.append(
        "colours.txt",
        """
        blue
        red
        white
        """,
    )
    rs.git.add(["colours.txt"])
    rs.git.commit(message="colours.txt: Add some colours")

    rs.files.append(
        "shapes.txt",
        """
        circle
        oval
        rectangle
        square
        """,
    )
    rs.git.add(["shapes.txt"])
    rs.git.commit(message="shapes.txt: Add some shapes")

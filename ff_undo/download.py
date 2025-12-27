from repo_smith.repo_smith import RepoSmith


def setup(rs: RepoSmith):
    rs.files.create_or_update(
        "rick.txt",
        """
        Hero
        """,
    )
    rs.git.add(all=True)
    rs.git.commit(message="Add Rick")

    rs.files.create_or_update(
        "morty.txt",
        """
        Boy
        """,
    )
    rs.git.add(all=True)
    rs.git.commit(message="Add Morty")

    rs.git.checkout("others", branch=True)

    rs.files.create_or_update(
        "birdperson.txt",
        """
        No job
        """,
    )
    rs.git.add(all=True)
    rs.git.commit(message="Add Birdperson")

    rs.files.append(
        "birdperson.txt",
        """
        Cyborg
        """,
    )
    rs.git.add(all=True)
    rs.git.commit(message="Add Cybord to birdperson.txt")

    rs.files.create_or_update(
        "tammy.txt",
        """
        Spy
        """,
    )
    rs.git.add(all=True)
    rs.git.commit(message="Add Tammy")

    rs.git.checkout("main")
    rs.git.merge("others", ff=True)

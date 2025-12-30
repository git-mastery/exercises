from repo_smith.repo_smith import RepoSmith

__requires_git__ = True
__requires_github__ = False


def download(rs: RepoSmith):
    rs.files.mkdir("pioneers")
    rs.files.cd("pioneers")
    rs.git.init()

    rs.files.create_or_update("neo.txt", "hacked the matrix\n")
    rs.git.add(["neo.txt"])
    rs.git.commit(message="Add Neo")

    rs.files.create_or_update("alan-turing.txt", "father of theoretical computing\n")
    rs.git.add(["alan-turing.txt"])
    rs.git.commit(message="Add Turing")

    rs.files.create_or_update("grace-hopper.txt", "created COBOL, compiler pioneer\n")
    rs.git.add(["grace-hopper.txt"])
    rs.git.commit(message="Add Hopper")

from repo_smith.repo_smith import RepoSmith

__requires_git__ = True
__requires_github__ = False


def download(rs: RepoSmith):
    rs.files.mkdir("stuff")
    rs.files.cd("stuff")
    rs.git.init()

    rs.files.create_or_update("keep.txt", "good stuff")
    rs.files.create_or_update("temp.txt", "temp stuff")
    rs.files.create_or_update("file1.tmp", "more temp stuff")
    rs.files.create_or_update("file2.tmp", "even more temp stuff")

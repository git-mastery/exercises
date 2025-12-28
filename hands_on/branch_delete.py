import os

from repo_smith.repo_smith import RepoSmith

__requires_git__ = True
__requires_github__ = False


def download(rs: RepoSmith):
    os.makedirs("samplerepo-books-2")
    os.chdir("samplerepo-books-2")

    rs.git.init()

    rs.files.create_or_update("horror.txt", "Horror Stories")
    rs.git.add(all=True)
    rs.git.commit(message="Add horror.txt")

    rs.git.checkout("textbooks", branch=True)
    rs.files.create_or_update("textbooks.txt", "Textbooks")
    rs.git.add(all=True)
    rs.git.commit(message="Add textbooks.txt")

    rs.git.checkout("main")

    rs.git.checkout("fantasy", branch=True)
    rs.files.create_or_update("fantasy.txt", "Fantasy Books")
    rs.git.add(all=True)
    rs.git.commit(message="Add fantasy.txt")

    rs.git.checkout("main")
    rs.git.merge("textbooks", no_ff=True, message="Merge branch textbooks")

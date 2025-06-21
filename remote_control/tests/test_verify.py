from git_autograder import GitAutograderTestLoader

from ..verify import verify

REPOSITORY_NAME = "remote-control"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test():
    pass

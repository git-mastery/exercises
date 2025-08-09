from git_autograder import GitAutograderTestLoader

from ..verify import verify

REPOSITORY_NAME = "log-and-order"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test():
    with loader.load("specs/base.yml", "start"):
        pass

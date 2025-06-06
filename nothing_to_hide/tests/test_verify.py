from git_autograder import GitAutograderTestLoader

from ..verify import verify

REPOSITORY_NAME = "nothing-to-hide"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test():
    with loader.load("specs/base.yml", "start"):
        pass

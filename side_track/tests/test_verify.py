from git_autograder import GitAutograderTestLoader

from ..verify import verify

REPOSITORY_NAME = "side-track"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test():
    with loader.load("specs/base.yml", "start"):
        pass

from git_autograder import GitAutograderTestLoader

from ..verify import verify

REPOSITORY_NAME = "push-over"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test():
    with loader.load("specs/base.yml", "start"):
        pass

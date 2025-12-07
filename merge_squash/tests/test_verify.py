from git_autograder import GitAutograderTestLoader

from ..verify import verify

REPOSITORY_NAME = "merge-squash"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_base():
    with loader.load("specs/base.yml", "start"):
        pass

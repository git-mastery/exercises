from exercise_utils.test import GitAutograderTestLoader

from .verify import verify

REPOSITORY_NAME = "remote-control"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


def test():
    pass

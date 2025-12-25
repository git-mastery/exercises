from exercise_utils.test import GitAutograderTestLoader

from .verify import verify

REPOSITORY_NAME = "push-over"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


def test():
    with loader.start():
        pass

from exercise_utils.test import GitAutograderTestLoader

from .verify import verify

REPOSITORY_NAME = "glossary-branch-pull"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


def test_base():
    with loader.start() as (test, rs):
        pass

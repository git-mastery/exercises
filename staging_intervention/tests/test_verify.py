from git_autograder import GitAutograderTestLoader, assert_output
from git_autograder.status import GitAutograderStatus

from ..verify import EXTRA_FILES_UNSTAGED, MISSING_FILES_UNSTAGED, verify

REPOSITORY_NAME = "staging-intervention"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_base():
    with loader.load("specs/base.yml", "start") as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_extra_unstaged():
    with loader.load("specs/extra_unstaged.yml", "start") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [EXTRA_FILES_UNSTAGED])


def test_missing_unstaged():
    with loader.load("specs/missing_unstaged.yml", "start") as output:
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [MISSING_FILES_UNSTAGED]
        )


def test_mixed_unstaged():
    with loader.load("specs/mixed_unstaged.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [EXTRA_FILES_UNSTAGED, MISSING_FILES_UNSTAGED],
        )

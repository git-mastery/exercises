from git_autograder import GitAutograderTestLoader, assert_output
from git_autograder.status import GitAutograderStatus

from ..verify import (
    verify,
    MISSING_JANUARY_TAG,
    WRONG_APRIL_TAG_COMMIT,
    OLD_FIRST_UPDATE_TAG,
    SUCCESS_MESSAGE,
    MISSING_COMMIT_MESSAGE,
)

REPOSITORY_NAME = "tags-update"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_base():
    with loader.load("specs/base.yml", "start") as output:
        print(output)
        assert_output(output, GitAutograderStatus.SUCCESSFUL, [SUCCESS_MESSAGE])


def test_missing_tags():
    with loader.load("specs/missing_tags.yml", "start") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [MISSING_JANUARY_TAG])


def test_wrong_april_tag():
    with loader.load("specs/wrong_april_tag.yml", "start") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [WRONG_APRIL_TAG_COMMIT])


def test_old_tag_still_exists():
    with loader.load("specs/old_tag_still_exists.yml", "start") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [OLD_FIRST_UPDATE_TAG])


def test_missing_january_commit():
    with loader.load("specs/missing_january_commit.yml", "start") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [MISSING_COMMIT_MESSAGE.format(message="January")])

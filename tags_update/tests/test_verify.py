from git_autograder import GitAutograderStatus, GitAutograderTestLoader, assert_output

from ..verify import (
    verify,
    MISSING_JANUARY_TAG,
    MISSING_APRIL_TAG,
    WRONG_JANUARY_TAG_COMMIT,
    WRONG_APRIL_TAG_COMMIT,
    OLD_FIRST_UPDATE_TAG,
    SUCCESS_MESSAGE,
    MISSING_COMMIT_MESSAGE,
)

REPOSITORY_NAME = "tags-update"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_base():
    with loader.load("specs/base.yml", "start") as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL, [SUCCESS_MESSAGE])


def test_missing_january_tag():
    with loader.load("specs/missing_january_tag.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [MISSING_JANUARY_TAG],
        )


def test_missing_april_tag():
    with loader.load("specs/missing_april_tag.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [MISSING_APRIL_TAG],
        )


def test_old_tag_still_exists():
    with loader.load("specs/old_tag_still_exists.yml", "start") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [OLD_FIRST_UPDATE_TAG])


def test_wrong_january_tag():
    with loader.load("specs/wrong_january_tag.yml", "start") as output:
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [WRONG_JANUARY_TAG_COMMIT]
        )


def test_missing_january_commit():
    with loader.load("specs/missing_january_commit.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [MISSING_COMMIT_MESSAGE.format(message="January")],
        )


def test_wrong_april_tag():
    with loader.load("specs/wrong_april_tag.yml", "start") as output:
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [WRONG_APRIL_TAG_COMMIT]
        )


def test_first_update_tag_not_renamed():
    with loader.load("specs/first_update_tag_not_renamed.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [OLD_FIRST_UPDATE_TAG, MISSING_JANUARY_TAG],
        )

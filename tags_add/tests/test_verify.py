from git_autograder import GitAutograderStatus, GitAutograderTestLoader, assert_output

from ..verify import (
    FIRST_TAG_NOT_LIGHTWEIGHT,
    SECOND_TAG_NOT_ANNOTATED,
    verify,
    FIRST_TAG_WRONG_COMMIT,
    MISSING_FIRST_TAG,
    MISSING_SECOND_TAG,
    SECOND_TAG_WRONG_COMMIT,
    WRONG_SECOND_TAG_MESSAGE,
)

REPOSITORY_NAME = "tags-add"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_base():
    with loader.load("specs/base.yml", "start") as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_missing_first_pilot_tag():
    with loader.load("specs/missing_first_pilot_tag.yml", "start") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [MISSING_FIRST_TAG])


def test_missing_v1_tag():
    with loader.load("specs/missing_v1_tag.yml", "start") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [MISSING_SECOND_TAG])


def test_wrong_message_v1_tag():
    with loader.load("specs/wrong_message_v1_tag.yml", "start") as output:
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [WRONG_SECOND_TAG_MESSAGE]
        )


def test_wrong_commit_first_pilot_tag():
    with loader.load("specs/wrong_commit_first_pilot_tag.yml", "start") as output:
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [FIRST_TAG_WRONG_COMMIT]
        )


def test_wrong_commit_v1_tag():
    with loader.load("specs/wrong_commit_v1_tag.yml", "start") as output:
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [SECOND_TAG_WRONG_COMMIT]
        )


def test_wrong_tag_type_first_pilot():
    with loader.load("specs/wrong_tag_type_first_pilot.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [FIRST_TAG_NOT_LIGHTWEIGHT],
        )


def test_wrong_tag_type_v1_tag():
    with loader.load("specs/wrong_tag_type_v1_tag.yml", "start") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [SECOND_TAG_NOT_ANNOTATED],
        )

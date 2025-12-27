from exercise_utils.test import GitAutograderTestLoader, assert_output
from git_autograder import GitAutograderStatus

from .verify import (
    FIRST_TAG_NOT_LIGHTWEIGHT,
    FIRST_TAG_WRONG_COMMIT,
    MISSING_FIRST_TAG,
    MISSING_SECOND_TAG,
    SECOND_TAG_NOT_ANNOTATED,
    SECOND_TAG_WRONG_COMMIT,
    WRONG_SECOND_TAG_MESSAGE,
    verify,
)

REPOSITORY_NAME = "tags-add"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


def test_base():
    with loader.start() as (test, rs):
        rs.git.commit(message="Add January duty roster", allow_empty=True)
        rs.git.tag("first-pilot")
        rs.git.commit(message="Update duty roster for February", allow_empty=True)
        rs.git.commit(message="Update roster for March", allow_empty=True)
        rs.git.tag("v1.0", message="first full duty roster")
        rs.git.commit(message="Update duty roster for April", allow_empty=True)
        rs.git.commit(message="Update roster for May", allow_empty=True)

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_missing_first_pilot_tag():
    with loader.start() as (test, rs):
        rs.git.commit(message="Add January duty roster", allow_empty=True)
        rs.git.commit(message="Update duty roster for February", allow_empty=True)
        rs.git.commit(message="Update roster for March", allow_empty=True)
        rs.git.tag("v1.0", message="first full duty roster")
        rs.git.commit(message="Update duty roster for April", allow_empty=True)
        rs.git.commit(message="Update roster for May", allow_empty=True)

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [MISSING_FIRST_TAG])


def test_missing_v1_tag():
    with loader.start() as (test, rs):
        rs.git.commit(message="Add January duty roster", allow_empty=True)
        rs.git.tag("first-pilot")
        rs.git.commit(message="Update duty roster for February", allow_empty=True)
        rs.git.commit(message="Update roster for March", allow_empty=True)
        rs.git.commit(message="Update duty roster for April", allow_empty=True)
        rs.git.commit(message="Update roster for May", allow_empty=True)

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [MISSING_SECOND_TAG])


def test_wrong_message_v1_tag():
    with loader.start() as (test, rs):
        rs.git.commit(message="Add January duty roster", allow_empty=True)
        rs.git.tag("first-pilot")
        rs.git.commit(message="Update duty roster for February", allow_empty=True)
        rs.git.commit(message="Update roster for March", allow_empty=True)
        rs.git.tag("v1.0", message="wrong message")
        rs.git.commit(message="Update duty roster for April", allow_empty=True)
        rs.git.commit(message="Update roster for May", allow_empty=True)

        output = test.run()
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [WRONG_SECOND_TAG_MESSAGE]
        )


def test_wrong_commit_first_pilot_tag():
    with loader.start() as (test, rs):
        rs.git.commit(message="Add January duty roster", allow_empty=True)
        rs.git.commit(message="Update duty roster for February", allow_empty=True)
        rs.git.tag("first-pilot")
        rs.git.commit(message="Update roster for March", allow_empty=True)
        rs.git.tag("v1.0", message="first full duty roster")
        rs.git.commit(message="Update duty roster for April", allow_empty=True)
        rs.git.commit(message="Update roster for May", allow_empty=True)

        output = test.run()
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [FIRST_TAG_WRONG_COMMIT]
        )


def test_wrong_commit_v1_tag():
    with loader.start() as (test, rs):
        rs.git.commit(message="Add January duty roster", allow_empty=True)
        rs.git.tag("first-pilot")
        rs.git.commit(message="Update duty roster for February", allow_empty=True)
        rs.git.commit(message="Update roster for March", allow_empty=True)
        rs.git.commit(message="Update duty roster for April", allow_empty=True)
        rs.git.commit(message="Update roster for May", allow_empty=True)
        rs.git.tag("v1.0", message="first full duty roster")

        output = test.run()
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [SECOND_TAG_WRONG_COMMIT]
        )


def test_wrong_tag_type_first_pilot():
    with loader.start() as (test, rs):
        rs.git.commit(message="Add January duty roster", allow_empty=True)
        rs.git.tag("first-pilot", message="test message", annotate=True)
        rs.git.commit(message="Update duty roster for February", allow_empty=True)
        rs.git.commit(message="Update roster for March", allow_empty=True)
        rs.git.commit(message="Update duty roster for April", allow_empty=True)
        rs.git.commit(message="Update roster for May", allow_empty=True)
        rs.git.tag("v1.0", message="first full duty roster")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [FIRST_TAG_NOT_LIGHTWEIGHT],
        )


def test_wrong_tag_type_v1_tag():
    with loader.start() as (test, rs):
        rs.git.commit(message="Add January duty roster", allow_empty=True)
        rs.git.tag("first-pilot")
        rs.git.commit(message="Update duty roster for February", allow_empty=True)
        rs.git.commit(message="Update roster for March", allow_empty=True)
        rs.git.commit(message="Update duty roster for April", allow_empty=True)
        rs.git.commit(message="Update roster for May", allow_empty=True)
        rs.git.tag("v1.0", annotate=False)

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [SECOND_TAG_NOT_ANNOTATED],
        )

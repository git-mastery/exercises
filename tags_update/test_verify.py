from exercise_utils.test import GitAutograderTestLoader, assert_output
from git_autograder import GitAutograderStatus

from .verify import (
    MISSING_APRIL_TAG,
    MISSING_COMMIT_MESSAGE,
    MISSING_JANUARY_TAG,
    OLD_FIRST_UPDATE_TAG,
    SUCCESS_MESSAGE,
    WRONG_APRIL_TAG_COMMIT,
    WRONG_JANUARY_TAG_COMMIT,
    verify,
)

REPOSITORY_NAME = "tags-update"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


def test_base():
    with loader.start() as (test, rs):
        rs.git.commit(message="Add January duty roster", allow_empty=True)
        rs.git.tag("january-update")
        rs.git.commit(message="Update duty roster for February", allow_empty=True)
        rs.git.commit(message="Update roster for March", allow_empty=True)
        rs.git.commit(message="Update duty roster for April", allow_empty=True)
        rs.git.tag("april-update")
        rs.git.commit(message="Update roster for May", allow_empty=True)
        rs.git.tag("may-update")

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL, [SUCCESS_MESSAGE])


def test_missing_january_tag():
    with loader.start() as (test, rs):
        rs.git.commit(message="Add January duty roster", allow_empty=True)
        rs.git.commit(message="Update duty roster for February", allow_empty=True)
        rs.git.commit(message="Update roster for March", allow_empty=True)
        rs.git.commit(message="Update duty roster for April", allow_empty=True)
        rs.git.tag("april-update")
        rs.git.commit(message="Update roster for May", allow_empty=True)
        rs.git.tag("may-update")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [MISSING_JANUARY_TAG],
        )


def test_missing_april_tag():
    with loader.start() as (test, rs):
        rs.git.commit(message="Add January duty roster", allow_empty=True)
        rs.git.tag("january-update")
        rs.git.commit(message="Update duty roster for February", allow_empty=True)
        rs.git.commit(message="Update roster for March", allow_empty=True)
        rs.git.commit(message="Update duty roster for April", allow_empty=True)
        rs.git.commit(message="Update roster for May", allow_empty=True)
        rs.git.tag("may-update")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [MISSING_APRIL_TAG],
        )


def test_old_tag_still_exists():
    with loader.start() as (test, rs):
        rs.git.commit(message="Add January duty roster", allow_empty=True)
        rs.git.tag("first-update")
        rs.git.commit(message="Update duty roster for February", allow_empty=True)
        rs.git.commit(message="Update roster for March", allow_empty=True)
        rs.git.commit(message="Update duty roster for April", allow_empty=True)
        rs.git.commit(message="Update roster for May", allow_empty=True)
        rs.git.tag("april-update")
        rs.git.tag("may-update")

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [OLD_FIRST_UPDATE_TAG])


def test_wrong_january_tag():
    with loader.start() as (test, rs):
        rs.git.commit(message="Add January duty roster", allow_empty=True)
        rs.git.commit(message="Update duty roster for February", allow_empty=True)
        rs.git.tag("january-update")
        rs.git.commit(message="Update roster for March", allow_empty=True)
        rs.git.commit(message="Update duty roster for April", allow_empty=True)
        rs.git.tag("april-update")
        rs.git.commit(message="Update roster for May", allow_empty=True)
        rs.git.tag("may-update")

        output = test.run()
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [WRONG_JANUARY_TAG_COMMIT]
        )


def test_missing_january_commit():
    with loader.start() as (test, rs):
        rs.git.commit(message="Update duty roster for February", allow_empty=True)
        rs.git.tag("january-update")
        rs.git.commit(message="Update roster for March", allow_empty=True)
        rs.git.commit(message="Update duty roster for April", allow_empty=True)
        rs.git.tag("april-update")
        rs.git.commit(message="Update roster for May", allow_empty=True)
        rs.git.tag("may-update")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [MISSING_COMMIT_MESSAGE.format(message="January")],
        )


def test_wrong_april_tag():
    with loader.start() as (test, rs):
        rs.git.commit(message="Add January duty roster", allow_empty=True)
        rs.git.tag("january-update")
        rs.git.commit(message="Update duty roster for February", allow_empty=True)
        rs.git.commit(message="Update roster for March", allow_empty=True)
        rs.git.commit(message="Update duty roster for April", allow_empty=True)
        rs.git.commit(message="Update roster for May", allow_empty=True)
        rs.git.tag("april-update")
        rs.git.tag("may-update")

        output = test.run()
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [WRONG_APRIL_TAG_COMMIT]
        )


def test_first_update_tag_not_renamed():
    with loader.start() as (test, rs):
        rs.git.commit(message="Add January duty roster", allow_empty=True)
        rs.git.tag("first-update")
        rs.git.commit(message="Update duty roster for February", allow_empty=True)
        rs.git.commit(message="Update roster for March", allow_empty=True)
        rs.git.commit(message="Update duty roster for April", allow_empty=True)
        rs.git.tag("april-update")
        rs.git.commit(message="Update roster for May", allow_empty=True)
        rs.git.tag("may-update")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [OLD_FIRST_UPDATE_TAG, MISSING_JANUARY_TAG],
        )

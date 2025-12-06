from git_autograder import GitAutograderStatus, GitAutograderTestLoader, assert_output

from ..verify import MISSING_FIRST_TAG, MISSING_SECOND_TAG, SUCCESS_MESSAGE, WRONG_SECOND_TAG_MESSAGE, verify

REPOSITORY_NAME = "tags-add"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_base():
    with loader.load("specs/base.yml", "start") as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL, [SUCCESS_MESSAGE])


def test_missing_first_pilot_tag():
    with loader.load("specs/missing_first_pilot_tag.yml", "start") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [MISSING_FIRST_TAG])


def test_missing_v1_tag():
    with loader.load("specs/missing_v1_tag.yml", "start") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [MISSING_SECOND_TAG])


def test_wrong_message_v1_tag():
    with loader.load("specs/wrong_message_v1_tag.yml", "start") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [WRONG_SECOND_TAG_MESSAGE])

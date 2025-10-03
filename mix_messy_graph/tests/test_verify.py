from git_autograder import GitAutograderStatus, GitAutograderTestLoader, assert_output

from ..verify import (
    FEATURE_SEARCH_BRANCH_STILL_EXISTS,
    FEATURE_DELETE_BRANCH_STILL_EXISTS,
    FEATURES_FILE_CONTENT_INVALID,
    LIST_BRANCH_STILL_EXISTS,
    MISMATCH_COMMIT_MESSAGE,
    SQUASH_NOT_USED,
    verify,
)

REPOSITORY_NAME = "mix-messy-graph"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_base():
    with loader.load("specs/base.yml") as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_non_squash_merge_used():
    with loader.load("specs/non_squash_merge_used.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [SQUASH_NOT_USED])


def test_wrong_commit_message():
    with loader.load("specs/wrong_commit_message.yml") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                MISMATCH_COMMIT_MESSAGE.format(
                    expected="Add the search feature", given="Add the search feature!"
                )
            ],
        )


def test_missing_commit():
    with loader.load("specs/missing_commit.yml") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                MISMATCH_COMMIT_MESSAGE.format(
                    expected="Add the delete feature", given="<Missing commit>"
                )
            ],
        )


def test_branches_not_deleted():
    with loader.load("specs/branches_not_deleted.yml") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                FEATURE_SEARCH_BRANCH_STILL_EXISTS,
                FEATURE_DELETE_BRANCH_STILL_EXISTS,
                LIST_BRANCH_STILL_EXISTS,
            ],
        )


def test_features_content_invalid():
    with loader.load("specs/features_content_invalid.yml") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [FEATURES_FILE_CONTENT_INVALID],
        )

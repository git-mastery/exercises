from git_autograder import GitAutograderStatus, GitAutograderTestLoader
from git_autograder.test_utils import assert_output

from ..verify import (
    FEATURE_LIST_BRANCH_MISSING,
    FEATURES_FILE_CONTENT_INVALID,
    LIST_BRANCH_STILL_EXISTS,
    MERGE_FEATURE_DELETE_SECOND,
    MERGE_FEATURE_SEARCH_FIRST,
    MISSING_DEVELOPMENT_BRANCH,
    MISSING_FEATURES_FILE,
    RESET_MESSAGE,
    WRONG_BRANCH_POINT,
    verify,
)

REPOSITORY_NAME = "mix-messy-docs"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_missing_development():
    with loader.load("specs/missing_development.yml") as output:
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [MISSING_DEVELOPMENT_BRANCH]
        )


def test_wrong_branch_point():
    with loader.load("specs/wrong_branch_point.yml") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [WRONG_BRANCH_POINT])


def test_right_order():
    with loader.load("specs/right_order.yml") as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_no_merge_feature_search():
    with loader.load("specs/no_merge_feature_search.yml") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [MERGE_FEATURE_SEARCH_FIRST, RESET_MESSAGE],
        )


def test_no_merge_feature_delete():
    with loader.load("specs/no_merge_feature_delete.yml") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [MERGE_FEATURE_DELETE_SECOND, RESET_MESSAGE],
        )


def test_list_branch_exists():
    with loader.load("specs/list_branch_exists.yml") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [LIST_BRANCH_STILL_EXISTS],
        )


def test_feature_list_branch_missing():
    with loader.load("specs/feature_list_branch_missing.yml") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [FEATURE_LIST_BRANCH_MISSING],
        )


def test_contents_wrong():
    with loader.load("specs/contents_wrong.yml") as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [FEATURES_FILE_CONTENT_INVALID],
        )

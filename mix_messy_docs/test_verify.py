from exercise_utils.test import GitAutograderTestLoader, GitMasteryHelper, assert_output
from git_autograder import GitAutograderStatus

from .verify import (
    FEATURE_LIST_BRANCH_MISSING,
    FEATURES_FILE_CONTENT_INVALID,
    LIST_BRANCH_STILL_EXISTS,
    MERGE_FEATURE_DELETE_SECOND,
    MERGE_FEATURE_SEARCH_FIRST,
    MERGE_WRONG_ORDER,
    MISSING_DEVELOPMENT_BRANCH,
    RESET_MESSAGE,
    WRONG_BRANCH_POINT,
    verify,
)

REPOSITORY_NAME = "mix-messy-docs"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)

FEATURES = """
# Features

## Create Book

Allows creating one book at a time.

## Searching for Books

Allows searching for books by keywords.
Works only for book titles.

## Deleting Books

Allows deleting books.
"""


def test_right_order():
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()

        rs.files.create_or_update("conflict.txt", "Hello world")
        rs.git.add(all=True)
        rs.git.commit(message="Expected branch point")
        rs.git.tag("v1.0")

        rs.git.checkout("feature-search", branch=True)
        rs.files.create_or_update("conflict.txt", "Hello world!")
        rs.git.add(all=True)
        rs.git.commit(message="Feature search changes")

        rs.git.checkout("main")
        rs.git.checkout("feature-delete", branch=True)
        rs.files.create_or_update("conflict.txt", "Hello world?")
        rs.git.add(all=True)
        rs.git.commit(message="Feature delete changes")

        rs.git.checkout("main")
        rs.git.checkout("feature-list", branch=True)
        rs.git.commit(message="Feature list changes", allow_empty=True)

        rs.git.checkout("main")
        rs.git.checkout("development", branch=True)
        rs.git.commit(message="Commit on development", allow_empty=True)
        rs.git.merge("feature-search", no_ff=True)
        rs.git.merge("feature-delete")
        rs.files.create_or_update("conflict.txt", "New contents")
        rs.git.add(all=True)
        rs.git.commit(no_edit=True)

        rs.git.branch("feature-search", delete=True)
        rs.git.branch("feature-delete", delete=True)

        rs.files.create_or_update("features.md", FEATURES)

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_missing_development():
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()

        output = test.run()
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [MISSING_DEVELOPMENT_BRANCH]
        )


def test_wrong_branch_point():
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)

        rs.git.checkout("development", branch=True)
        rs.git.commit(message="Commit on development", allow_empty=True)

        rs.git.checkout("main")
        rs.git.commit(message="Expected branch point", allow_empty=True)
        rs.git.tag("v1.0")

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [WRONG_BRANCH_POINT])


def test_no_merge_feature_search():
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()

        rs.files.create_or_update("conflict.txt", "Hello world")
        rs.git.add(all=True)
        rs.git.commit(message="Expected branch point")
        rs.git.tag("v1.0")

        rs.git.checkout("feature-search", branch=True)
        rs.files.create_or_update("conflict.txt", "Hello world!")
        rs.git.add(all=True)
        rs.git.commit(message="Feature search changes")

        rs.git.checkout("main")
        rs.git.checkout("feature-delete", branch=True)
        rs.files.create_or_update("conflict.txt", "Hello world?")
        rs.git.add(all=True)
        rs.git.commit(message="Feature delete changes")

        rs.git.checkout("main")
        rs.git.checkout("feature-list", branch=True)
        rs.git.commit(message="Feature list changes", allow_empty=True)

        rs.git.checkout("main")
        rs.git.checkout("development", branch=True)
        rs.git.commit(message="Commit on development", allow_empty=True)
        rs.git.merge("feature-delete")
        rs.files.create_or_update("conflict.txt", "New contents")
        rs.git.add(all=True)
        rs.git.commit(no_edit=True)

        rs.git.branch("feature-search", delete=True, force=True)
        rs.git.branch("feature-delete", delete=True)

        rs.files.create_or_update("features.md", FEATURES)

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [MERGE_FEATURE_SEARCH_FIRST, RESET_MESSAGE],
        )


def test_no_merge_feature_delete():
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()

        rs.files.create_or_update("conflict.txt", "Hello world")
        rs.git.add(all=True)
        rs.git.commit(message="Expected branch point")
        rs.git.tag("v1.0")

        rs.git.checkout("feature-search", branch=True)
        rs.files.create_or_update("conflict.txt", "Hello world!")
        rs.git.add(all=True)
        rs.git.commit(message="Feature search changes")

        rs.git.checkout("main")
        rs.git.checkout("feature-delete", branch=True)
        rs.files.create_or_update("conflict.txt", "Hello world?")
        rs.git.add(all=True)
        rs.git.commit(message="Feature delete changes")

        rs.git.checkout("main")
        rs.git.checkout("feature-list", branch=True)
        rs.git.commit(message="Feature list changes", allow_empty=True)

        rs.git.checkout("main")
        rs.git.checkout("development", branch=True)
        rs.git.commit(message="Commit on development", allow_empty=True)
        rs.git.merge("feature-search", no_ff=True)

        rs.git.branch("feature-search", delete=True)
        rs.git.branch("feature-delete", delete=True, force=True)

        rs.files.create_or_update("features.md", FEATURES)

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [MERGE_FEATURE_DELETE_SECOND, RESET_MESSAGE],
        )


def test_list_branch_exists():
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()

        rs.files.create_or_update("conflict.txt", "Hello world")
        rs.git.add(all=True)
        rs.git.commit(message="Expected branch point")
        rs.git.tag("v1.0")

        rs.git.checkout("feature-search", branch=True)
        rs.files.create_or_update("conflict.txt", "Hello world!")
        rs.git.add(all=True)
        rs.git.commit(message="Feature search changes")

        rs.git.checkout("main")
        rs.git.checkout("feature-delete", branch=True)
        rs.files.create_or_update("conflict.txt", "Hello world?")
        rs.git.add(all=True)
        rs.git.commit(message="Feature delete changes")

        rs.git.checkout("main")
        rs.git.checkout("list", branch=True)
        rs.git.commit(message="Feature list changes", allow_empty=True)

        rs.git.checkout("main")
        rs.git.checkout("feature-list", branch=True)
        rs.git.commit(message="Feature list changes", allow_empty=True)

        rs.git.checkout("main")
        rs.git.checkout("development", branch=True)
        rs.git.commit(message="Commit on development", allow_empty=True)
        rs.git.merge("feature-search", no_ff=True)
        rs.git.merge("feature-delete")
        rs.files.create_or_update("conflict.txt", "New contents")
        rs.git.add(all=True)
        rs.git.commit(no_edit=True)

        rs.git.branch("feature-search", delete=True)
        rs.git.branch("feature-delete", delete=True)

        rs.files.create_or_update("features.md", FEATURES)

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [LIST_BRANCH_STILL_EXISTS],
        )


def test_feature_list_branch_missing():
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()

        rs.files.create_or_update("conflict.txt", "Hello world")
        rs.git.add(all=True)
        rs.git.commit(message="Expected branch point")
        rs.git.tag("v1.0")

        rs.git.checkout("feature-search", branch=True)
        rs.files.create_or_update("conflict.txt", "Hello world!")
        rs.git.add(all=True)
        rs.git.commit(message="Feature search changes")

        rs.git.checkout("main")
        rs.git.checkout("feature-delete", branch=True)
        rs.files.create_or_update("conflict.txt", "Hello world?")
        rs.git.add(all=True)
        rs.git.commit(message="Feature delete changes")

        rs.git.checkout("main")
        rs.git.checkout("other-list", branch=True)
        rs.git.commit(message="Feature list changes", allow_empty=True)

        rs.git.checkout("main")
        rs.git.checkout("development", branch=True)
        rs.git.commit(message="Commit on development", allow_empty=True)
        rs.git.merge("feature-search", no_ff=True)
        rs.git.merge("feature-delete")
        rs.files.create_or_update("conflict.txt", "New contents")
        rs.git.add(all=True)
        rs.git.commit(no_edit=True)

        rs.git.branch("feature-search", delete=True)
        rs.git.branch("feature-delete", delete=True)

        rs.files.create_or_update("features.md", FEATURES)

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [FEATURE_LIST_BRANCH_MISSING],
        )


def test_contents_wrong():
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()

        rs.files.create_or_update("conflict.txt", "Hello world")
        rs.git.add(all=True)
        rs.git.commit(message="Expected branch point")
        rs.git.tag("v1.0")

        rs.git.checkout("feature-search", branch=True)
        rs.files.create_or_update("conflict.txt", "Hello world!")
        rs.git.add(all=True)
        rs.git.commit(message="Feature search changes")

        rs.git.checkout("main")
        rs.git.checkout("feature-delete", branch=True)
        rs.files.create_or_update("conflict.txt", "Hello world?")
        rs.git.add(all=True)
        rs.git.commit(message="Feature delete changes")

        rs.git.checkout("main")
        rs.git.checkout("feature-list", branch=True)
        rs.git.commit(message="Feature list changes", allow_empty=True)

        rs.git.checkout("main")
        rs.git.checkout("development", branch=True)
        rs.git.commit(message="Commit on development", allow_empty=True)
        rs.git.merge("feature-search", no_ff=True)
        rs.git.merge("feature-delete")
        rs.files.create_or_update("conflict.txt", "New contents")
        rs.git.add(all=True)
        rs.git.commit(no_edit=True)

        rs.git.branch("feature-search", delete=True)
        rs.git.branch("feature-delete", delete=True)

        rs.files.create_or_update("features.md", FEATURES[0])

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [FEATURES_FILE_CONTENT_INVALID],
        )


def test_wrong_merge_order():
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()

        rs.files.create_or_update("conflict.txt", "Hello world")
        rs.git.add(all=True)
        rs.git.commit(message="Expected branch point")
        rs.git.tag("v1.0")

        rs.git.checkout("feature-search", branch=True)
        rs.files.create_or_update("conflict.txt", "Hello world!")
        rs.git.add(all=True)
        rs.git.commit(message="Feature search changes")

        rs.git.checkout("main")
        rs.git.checkout("feature-delete", branch=True)
        rs.files.create_or_update("conflict.txt", "Hello world?")
        rs.git.add(all=True)
        rs.git.commit(message="Feature delete changes")

        rs.git.checkout("main")
        rs.git.checkout("feature-list", branch=True)
        rs.git.commit(message="Feature list changes", allow_empty=True)

        rs.git.checkout("main")
        rs.git.checkout("development", branch=True)
        rs.git.commit(message="Commit on development", allow_empty=True)
        rs.git.merge("feature-delete", no_ff=True)
        rs.git.merge("feature-search", no_ff=True)
        rs.files.create_or_update("conflict.txt", "New contents")
        rs.git.add(all=True)
        rs.git.commit(no_edit=True)

        rs.git.branch("feature-search", delete=True)
        rs.git.branch("feature-delete", delete=True)

        rs.files.create_or_update("features.md", FEATURES)

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [MERGE_WRONG_ORDER, RESET_MESSAGE],
        )

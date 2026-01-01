from exercise_utils.test import GitAutograderTestLoader, GitMasteryHelper, assert_output
from git_autograder import GitAutograderStatus

from .verify import (
    FEATURE_DELETE_BRANCH_STILL_EXISTS,
    FEATURE_SEARCH_BRANCH_STILL_EXISTS,
    FEATURES_FILE_CONTENT_INVALID,
    LIST_BRANCH_STILL_EXISTS,
    MISMATCH_COMMIT_MESSAGE,
    SQUASH_NOT_USED,
    verify,
)

REPOSITORY_NAME = "mix-messy-graph"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)

FEATURES_FILE_CONTENT_DELETE_COMMIT = """
# Features

## Creating Books

Allows creating one book at a time.

## Searching for Books

Allows searching for books by keywords.
Works only for book titles.

## Deleting Books

Allows deleting books.
"""

FEATURES_FILE_CONTENT_SEARCH_COMMIT = """
# Features

## Creating Books

Allows creating one book at a time.

## Searching for Books

Allows searching for books by keywords.
Works only for book titles.
"""

FEATURES_FILE_CONTENT_FIX_HEADINGS_COMMIT = """
# Features

## Creating Books

Allows creating one book at a time.
"""


FEATURES_FILE_CONTENT_CREATE_COMMIT = """
# Features

## Create Book

Allows creating one book at a time.
"""

FEATURES_FILE_CONTENT_FEATURES_COMMIT = """
# Features
"""


def test_base():
    with loader.start() as (test, rs):
        rs.files.create_or_update("features.md", FEATURES_FILE_CONTENT_FEATURES_COMMIT)
        rs.git.add("features.md")
        rs.git.commit(message="Add features.md")
        rs.helper(GitMasteryHelper).create_start_tag()

        rs.files.create_or_update("features.md", FEATURES_FILE_CONTENT_CREATE_COMMIT)
        rs.git.add("features.md")
        rs.git.commit(message="Mention feature for creating books")
        rs.git.tag("v1.0")

        rs.files.create_or_update(
            "features.md", FEATURES_FILE_CONTENT_FIX_HEADINGS_COMMIT
        )
        rs.git.add("features.md")
        rs.git.commit(message="Fix phrasing of heading")

        rs.files.create_or_update("features.md", FEATURES_FILE_CONTENT_SEARCH_COMMIT)
        rs.git.add("features.md")
        rs.git.commit(message="Add the search feature")

        rs.files.create_or_update("features.md", FEATURES_FILE_CONTENT_DELETE_COMMIT)
        rs.git.add("features.md")
        rs.git.commit(message="Add the delete feature")

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_invalid_features_content():
    with loader.start() as (test, rs):
        rs.files.create_or_update("features.md", FEATURES_FILE_CONTENT_FEATURES_COMMIT)
        rs.git.add("features.md")
        rs.git.commit(message="Add features.md")
        rs.helper(GitMasteryHelper).create_start_tag()

        rs.files.create_or_update("features.md", FEATURES_FILE_CONTENT_CREATE_COMMIT)
        rs.git.add("features.md")
        rs.git.commit(message="Mention feature for creating books")
        rs.git.tag("v1.0")

        rs.git.commit(message="Fix phrasing of heading", allow_empty=True)

        rs.files.create_or_update("features.md", FEATURES_FILE_CONTENT_SEARCH_COMMIT)
        rs.git.add("features.md")
        rs.git.commit(message="Add the search feature")

        rs.files.create_or_update("features.md", FEATURES_FILE_CONTENT_DELETE_COMMIT)
        rs.git.add("features.md")
        rs.git.commit(message="Add the delete feature")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [FEATURES_FILE_CONTENT_INVALID.format(commit="Fix phrasing of heading")],
        )


def test_non_squash_merge_used():
    with loader.start() as (test, rs):
        rs.git.commit(message="Add features.md", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        rs.git.commit(message="Mention feature for creating books", allow_empty=True)
        rs.git.tag("v1.0")
        rs.git.commit(message="Fix phrasing of heading", allow_empty=True)

        rs.git.checkout("feature-search", branch=True)
        rs.git.commit(message="Feature search", allow_empty=True)
        rs.git.checkout("main")
        rs.git.merge("feature-search")

        rs.git.commit(message="Add the delete feature", allow_empty=True)
        rs.files.create_or_update("features.md", FEATURES_FILE_CONTENT_DELETE_COMMIT)

        output = test.run()
        # This would fail because the squash merge changes the commit messages and the contents
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                MISMATCH_COMMIT_MESSAGE.format(
                    expected="Add the search feature", given="Feature search"
                )
            ],
        )


def test_non_squash_merge_used_2():
    with loader.start() as (test, rs):
        rs.git.commit(message="Add features.md", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        rs.git.commit(message="Mention feature for creating books", allow_empty=True)
        rs.git.tag("v1.0")
        rs.git.commit(message="Fix phrasing of heading", allow_empty=True)

        rs.git.checkout("feature-search", branch=True)
        rs.git.commit(message="Feature search", allow_empty=True)
        rs.git.checkout("main")
        rs.git.merge("feature-search", no_ff=True)

        rs.git.commit(message="Add the delete feature", allow_empty=True)
        rs.files.create_or_update("features.md", FEATURES_FILE_CONTENT_DELETE_COMMIT)

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [SQUASH_NOT_USED],
        )


def test_wrong_commit_message():
    with loader.start() as (test, rs):
        rs.git.commit(message="Add features.md", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        rs.git.commit(message="Mention feature for creating books", allow_empty=True)
        rs.git.tag("v1.0")
        rs.git.commit(message="Fix phrasing of heading", allow_empty=True)
        rs.git.commit(message="Add the search feature!", allow_empty=True)
        rs.git.commit(message="Add the delete feature", allow_empty=True)
        rs.files.create_or_update("features.md", FEATURES_FILE_CONTENT_DELETE_COMMIT)

        output = test.run()
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
    with loader.start() as (test, rs):
        rs.git.commit(message="Add features.md", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        rs.git.commit(message="Mention feature for creating books", allow_empty=True)
        rs.git.tag("v1.0")
        rs.git.commit(message="Fix phrasing of heading", allow_empty=True)
        rs.git.commit(message="Add the search feature", allow_empty=True)
        rs.files.create_or_update("features.md", FEATURES_FILE_CONTENT_DELETE_COMMIT)

        output = test.run()
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
    with loader.start() as (test, rs):
        rs.git.commit(message="Add features.md", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        rs.git.commit(message="Mention feature for creating books", allow_empty=True)
        rs.git.tag("v1.0")
        rs.git.commit(message="Fix phrasing of heading", allow_empty=True)
        rs.git.commit(message="Add the search feature", allow_empty=True)
        rs.git.commit(message="Add the delete feature", allow_empty=True)

        rs.git.branch("feature-search")
        rs.git.branch("feature-delete")
        rs.git.branch("list")

        rs.files.create_or_update("features.md", FEATURES_FILE_CONTENT_DELETE_COMMIT)

        output = test.run()
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
    with loader.start() as (test, rs):
        rs.git.commit(message="Add features.md", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        rs.git.commit(message="Mention feature for creating books", allow_empty=True)
        rs.git.tag("v1.0")
        rs.git.commit(message="Fix phrasing of heading", allow_empty=True)
        rs.git.commit(message="Add the search feature", allow_empty=True)
        rs.git.commit(message="Add the delete feature", allow_empty=True)
        rs.files.create_or_update("features.md", FEATURES_FILE_CONTENT_DELETE_COMMIT[0])

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [FEATURES_FILE_CONTENT_INVALID.format(commit="Add features.md")],
        )

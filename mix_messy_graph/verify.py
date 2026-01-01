from typing import Optional, List
from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
    GitAutograderCommit,
)
from itertools import zip_longest

SQUASH_NOT_USED = (
    "You should be using squash merges for both 'feature-search' and 'feature-delete'"
)
WRONG_ORDER_OF_MERGING = "You need to merge 'feature-search' before 'feature-delete'"
FEATURE_SEARCH_MERGE_MESSAGE = (
    "The message for merging 'feature-search' should be 'Add the search feature'"
)
FEATURE_DELETE_MERGE_MESSAGE = (
    "The message for merging 'feature-delete' should be 'Add the delete feature'"
)
MISMATCH_COMMIT_MESSAGE = (
    "Expected commit message of '{expected}', got '{given}' instead."
)

FEATURE_SEARCH_BRANCH_STILL_EXISTS = "Branch 'feature-search' still exists."
FEATURE_DELETE_BRANCH_STILL_EXISTS = "Branch 'feature-delete' still exists."
LIST_BRANCH_STILL_EXISTS = "Branch 'list' still exists."

MISSING_FEATURES_FILE = "You are missing 'features.md'!"
FEATURES_FILE_CONTENT_INVALID = "Contents of 'features.md' is not valid at commit with message '{commit}'! Try again!"

EXPECTED_COMMIT_MESSAGES = [
    "Add features.md",
    "Mention feature for creating books",
    "Fix phrasing of heading",
    "Add the search feature",
    "Add the delete feature",
]

EXPECTED_LINES_DELETE_COMMIT = [
    "# Features",
    "## Creating Books",
    "Allows creating one book at a time.",
    "## Searching for Books",
    "Allows searching for books by keywords.",
    "Works only for book titles.",
    "## Deleting Books",
    "Allows deleting books.",
]

EXPECTED_LINES_SEARCH_COMMIT = [
    "# Features",
    "## Creating Books",
    "Allows creating one book at a time.",
    "## Searching for Books",
    "Allows searching for books by keywords.",
    "Works only for book titles.",
]

EXPECTED_LINES_FIX_HEADING_COMMIT = [
    "# Features",
    "## Creating Books",
    "Allows creating one book at a time.",
]

EXPECTED_LINES_CREATE_BOOK_COMMIT = [
    "# Features",
    "## Create Book",
    "Allows creating one book at a time.",
]

EXPECTED_LINES_FEATURES_COMMIT = [
    "# Features",
]


def ensure_str(val) -> str:
    if isinstance(val, bytes):
        return val.decode("utf-8", errors="replace").strip()
    return str(val).strip()


def get_commit_from_message(
    commits: List[GitAutograderCommit], message: str
) -> Optional[GitAutograderCommit]:
    """Find a commit with the given message from a list of commits."""
    for commit in commits:
        if message.strip() == commit.commit.message.strip():
            return commit
    return None


def verify_commit_file_content(
    exercise: GitAutograderExercise,
    commit: GitAutograderCommit | None,
    file_name: str,
    expected_content: List[str],
):
    """Checkout to specific commit and verify that the file content of the given commit matches the expected content."""
    if not commit:
        return
    commit.checkout()
    with exercise.repo.files.file_or_none(file_name) as file:
        if file is None:
            raise exercise.wrong_answer([MISSING_FEATURES_FILE])

        contents = [line.strip() for line in file.readlines() if line.strip() != ""]
        if contents != expected_content:
            raise exercise.wrong_answer(
                [
                    FEATURES_FILE_CONTENT_INVALID.format(
                        commit=commit.commit.message.strip()
                    )
                ]
            )
    exercise.repo.branches.branch("main").checkout()


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    main_branch = exercise.repo.branches.branch("main")

    # Verify that there are no merge commits
    merge_commits = [c for c in main_branch.commits if len(c.parents) > 1]
    if merge_commits:
        raise exercise.wrong_answer([SQUASH_NOT_USED])

    # Verify that the commit messages are correct
    commits = main_branch.commits
    commit_messages = [ensure_str(c.commit.message) for c in commits][::-1]
    for expected, given in zip_longest(EXPECTED_COMMIT_MESSAGES, commit_messages):
        if expected != given:
            raise exercise.wrong_answer(
                [
                    MISMATCH_COMMIT_MESSAGE.format(
                        expected=expected, given=(given or "<Missing commit>")
                    )
                ]
            )

    # Verify that the branches are deleted
    feature_search_branch = exercise.repo.branches.branch_or_none("feature-search")
    feature_delete_branch = exercise.repo.branches.branch_or_none("feature-delete")
    list_branch = exercise.repo.branches.branch_or_none("list")
    branch_exists_messages = []
    if feature_search_branch is not None:
        branch_exists_messages.append(FEATURE_SEARCH_BRANCH_STILL_EXISTS)
    if feature_delete_branch is not None:
        branch_exists_messages.append(FEATURE_DELETE_BRANCH_STILL_EXISTS)
    if list_branch is not None:
        branch_exists_messages.append(LIST_BRANCH_STILL_EXISTS)

    if branch_exists_messages:
        raise exercise.wrong_answer(branch_exists_messages)

    # Verify that the features.md file is correct
    # Checkout to specific commit to verify the contents of features.md
    features_commit = get_commit_from_message(commits, "Add features.md")
    verify_commit_file_content(
        exercise, features_commit, "features.md", EXPECTED_LINES_FEATURES_COMMIT
    )

    create_books_commit = get_commit_from_message(
        commits, "Mention feature for creating books"
    )
    verify_commit_file_content(
        exercise, create_books_commit, "features.md", EXPECTED_LINES_CREATE_BOOK_COMMIT
    )

    fix_heading_commit = get_commit_from_message(commits, "Fix phrasing of heading")
    verify_commit_file_content(
        exercise, fix_heading_commit, "features.md", EXPECTED_LINES_FIX_HEADING_COMMIT
    )

    add_search_commit = get_commit_from_message(commits, "Add the search feature")
    verify_commit_file_content(
        exercise, add_search_commit, "features.md", EXPECTED_LINES_SEARCH_COMMIT
    )

    delete_feature_commit = get_commit_from_message(commits, "Add the delete feature")
    verify_commit_file_content(
        exercise, delete_feature_commit, "features.md", EXPECTED_LINES_DELETE_COMMIT
    )

    return exercise.to_output(
        ["You have successfully completed the exercise!"],
        GitAutograderStatus.SUCCESSFUL,
    )

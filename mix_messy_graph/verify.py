from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
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
FEATURES_FILE_CONTENT_INVALID = "Contents of 'features.md' is not valid! Try again!"

EXPECTED_COMMIT_MESSAGES = [
    "Add features.md",
    "Mention feature for creating books",
    "Fix phrasing of heading",
    "Add the search feature",
    "Add the delete feature",
]

EXPECTED_LINES = [
    "# Features",
    "## Create Book",
    "Allows creating one book at a time.",
    "## Searching for Books",
    "Allows searching for books by keywords.",
    "Works only for book titles.",
    "## Deleting Books",
    "Allows deleting books.",
]


def ensure_str(val) -> str:
    if isinstance(val, bytes):
        return val.decode("utf-8", errors="replace").strip()
    return str(val).strip()


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    main_branch = exercise.repo.branches.branch("main")
    merge_commits = [c for c in main_branch.commits if len(c.parents) > 1]
    merge_reflogs = [e for e in main_branch.reflog if "merge" in e.action]
    # We expect 1 merge reflog entry because of the setup step which merges the branch,
    # but no other merges should be present
    if merge_commits or len(merge_reflogs) > 1:
        raise exercise.wrong_answer([SQUASH_NOT_USED])

    commit_messages = [ensure_str(c.commit.message) for c in main_branch.commits][::-1]
    for expected, given in zip_longest(EXPECTED_COMMIT_MESSAGES, commit_messages):
        if expected != given:
            raise exercise.wrong_answer(
                [
                    MISMATCH_COMMIT_MESSAGE.format(
                        expected=expected, given=(given or "<Missing commit>")
                    )
                ]
            )

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

    with exercise.repo.files.file_or_none("features.md") as features_file:
        if features_file is None:
            raise exercise.wrong_answer([MISSING_FEATURES_FILE])

        contents = [
            line.strip() for line in features_file.readlines() if line.strip() != ""
        ]
        if contents != EXPECTED_LINES:
            raise exercise.wrong_answer([FEATURES_FILE_CONTENT_INVALID])

    return exercise.to_output([], GitAutograderStatus.SUCCESSFUL)

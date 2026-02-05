from git import Commit
from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

MISSING_DEVELOPMENT_BRANCH = "You are missing the 'development' branch!"
WRONG_BRANCH_POINT = "You did not branch from the commit with tag v1.0!"
FEATURE_SEARCH_BRANCH_STILL_EXISTS = (
    "Branch 'feature-search' still exists! Remember to delete it after merging!"
)
FEATURE_DELETE_BRANCH_STILL_EXISTS = (
    "Branch 'feature-delete' still exists! Remember to delete it after merging!"
)
LIST_BRANCH_STILL_EXISTS = (
    "Branch 'list' still exists! Remember to rename it to 'feature-list'!"
)
FEATURE_LIST_BRANCH_MISSING = "Branch 'feature-list' is missing. Did you misspell it?"
MERGE_FEATURE_SEARCH_FIRST = "You need to merge 'feature-search' first!"
MERGE_FEATURE_DELETE_SECOND = "You need to merge 'feature-delete' second!"
MISSING_FEATURES_FILE = "You are missing 'features.md'!"
FEATURES_FILE_CONTENT_INVALID = "Contents of 'features.md' is not valid! Try again!"
MERGE_WRONG_ORDER = (
    "Merges are in wrong order! feature-search should be merged before feature-delete."
)

RESET_MESSAGE = 'Reset the repository using "gitmastery progress reset" and start again'


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


def _get_commit_message(commit: Commit) -> str:
    """Normalize commit message to string."""
    if commit.message is None:
        return ""
    if isinstance(commit.message, (bytes, bytearray, memoryview)):
        return bytes(commit.message).decode("utf-8", errors="ignore")
    return commit.message


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    # Step 1: create development branch from tag v1.0
    development_branch = exercise.repo.branches.branch_or_none("development")
    if development_branch is None:
        raise exercise.wrong_answer([MISSING_DEVELOPMENT_BRANCH])

    tag_commit = exercise.repo.repo.tags["v1.0"].commit
    development_commit = development_branch.latest_commit

    # Check if development branch was created from v1.0
    main_branch = exercise.repo.branches.branch("main")  # main branch must exist
    merge_base = exercise.repo.repo.git.merge_base(
        main_branch.latest_commit.hexsha, development_commit.hexsha
    )
    commits_between = list(
        exercise.repo.repo.iter_commits(f"{tag_commit.hexsha}..{merge_base}")
    )
    if commits_between:
        # There are commits on main after v1.0 that are ancestors of development
        # This means development wasn't created from v1.0
        raise exercise.wrong_answer([WRONG_BRANCH_POINT])

    commits_since_tag = list(
        exercise.repo.repo.iter_commits(
            f"{tag_commit.hexsha}..{development_commit.hexsha}"
        )
    )
    merge_commits = [commit for commit in commits_since_tag if len(commit.parents) > 1]

    # Step 2: merge feature-search to development branch, delete feature-search branch
    feature_search_merges = [
        commit
        for commit in merge_commits
        if all(
            keyword in _get_commit_message(commit).lower()
            for keyword in ["feature-search", "merge", "development"]
        )
    ]

    has_feature_search_merge = len(feature_search_merges) > 0
    if not has_feature_search_merge:
        raise exercise.wrong_answer([MERGE_FEATURE_SEARCH_FIRST])

    feature_search_branch = exercise.repo.branches.branch_or_none("feature-search")
    if feature_search_branch is not None:
        raise exercise.wrong_answer([FEATURE_SEARCH_BRANCH_STILL_EXISTS])

    # Step 3: merge feature-delete to development branch, delete feature-delete branch
    feature_delete_merges = [
        commit
        for commit in merge_commits
        if all(
            keyword in _get_commit_message(commit).lower()
            for keyword in ["feature-delete", "merge", "development"]
        )
    ]

    has_feature_delete_merge = len(feature_delete_merges) > 0
    if not has_feature_delete_merge:
        raise exercise.wrong_answer([MERGE_FEATURE_DELETE_SECOND])

    feature_delete_branch = exercise.repo.branches.branch_or_none("feature-delete")
    if feature_delete_branch is not None:
        raise exercise.wrong_answer([FEATURE_DELETE_BRANCH_STILL_EXISTS])

    # Verify order of merges
    search_merge = feature_search_merges[-1]
    delete_merge = feature_delete_merges[-1]

    if not exercise.repo.repo.is_ancestor(search_merge, delete_merge):
        raise exercise.wrong_answer([MERGE_WRONG_ORDER, RESET_MESSAGE])

    with exercise.repo.files.file_or_none("features.md") as features_file:
        if features_file is None:
            raise exercise.wrong_answer([MISSING_FEATURES_FILE])

        contents = [
            line.strip() for line in features_file.readlines() if line.strip() != ""
        ]
        if contents != EXPECTED_LINES:
            raise exercise.wrong_answer([FEATURES_FILE_CONTENT_INVALID])

    # Step 4: rename list branch to feature-list
    feature_list_branch = exercise.repo.branches.branch_or_none("feature-list")
    list_branch = exercise.repo.branches.branch_or_none("list")
    if feature_list_branch is None:
        if list_branch is not None:
            raise exercise.wrong_answer([LIST_BRANCH_STILL_EXISTS])
        else:
            raise exercise.wrong_answer([FEATURE_LIST_BRANCH_MISSING])
    elif list_branch is not None:
        raise exercise.wrong_answer([LIST_BRANCH_STILL_EXISTS])

    return exercise.to_output(
        [
            "Great work using all of the concepts you've learnt about branching to mix the messy documentation!"
        ],
        GitAutograderStatus.SUCCESSFUL,
    )

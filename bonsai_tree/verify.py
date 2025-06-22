import os
from typing import List

from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)

MAIN_MISSING_DANGERS = "The main branch is missing the dangers-to-bonsais.txt file"
MAIN_WRONG_TEXT = "The dangers-to-bonsais.txt file on the main branch does not have the right contents"
MAIN_DANGERS_NOT_PARENT = (
    "The commit that added dangers-to-bonsais.txt was not branched from"
)

HISTORY_MISSING_HISTORY = (
    "The history branch is missing the history-of-bonsais.txt file"
)
HISTORY_WRONG_TEXT = "The history-of-bonsais.txt file on the history branch does not have the right contents"
HISTORY_DANGERS_NOT_PARENT = (
    "The commit that added history-of-bonsais.txt was not branched from"
)

CARE_MISSING_CARE = "The care branch is missing the edit to bonsai-care.txt file"
CARE_WRONG_TEXT = (
    "The bonsai-cre.txt file on the care branch does not have the right contents"
)

"""
1. Add dangers-to-bonsais.txt on main
2. Branch to history
3. Add history-of-bonsais.txt on history
4. Branch to care
5. Edit bonsais-care.txt
"""

DANGER_FILENAME = "dangers-to-bonsais.txt"
HISTORY_FILENAME = "history-of-bonsais.txt"
CARE_FILENAME = "bonsai-care.txt"
EXPECTED_BRANCHES = {"history", "care", "main"}

DANGER_FILE = """
Bonsai trees are delicate and vulnerable to threats like overwatering, pests, fungal infections, and extreme temperatures. Poor pruning or wiring can cause lasting damage, while dehydration and root rot are common killers. Without careful maintenance, these miniature trees can quickly decline.
"""

HISTORY_FILE = """
Bonsai originated in China over a thousand years ago as "penjing," the art of miniature landscape cultivation. The practice later spread to Japan, where it evolved into the refined bonsai we know today, emphasizing simplicity, balance, and harmony with nature. Traditionally associated with Zen Buddhism, bonsai became a symbol of patience and artistic expression. Over time, it gained global popularity, with enthusiasts worldwide cultivating these miniature trees as a blend of horticulture and art.
"""

CARE_FILE = """
Proper bonsai care involves balancing water, light, and nutrients to maintain a healthy tree. Bonsais require well-draining soil and regular watering, but overwatering can lead to root rot. They need adequate sunlight, with indoor varieties thriving near bright windows and outdoor species requiring seasonal adjustments. Pruning and wiring help shape the tree, while repotting every few years ensures root health. Protecting bonsais from pests, extreme temperatures, and diseases is essential for their longevity, making their care both an art and a discipline.
"""


def parse_branch_contains(text: str) -> List[str]:
    return [line[2:] for line in text.split("\n")]


def are_files_equal(given: str, expected: str) -> bool:
    with (
        open(given, "r") as given_file,
        open(expected, "r") as expected_file,
    ):
        contents = given_file.read().replace("\n", "")
        expected_contents = expected_file.read().replace("\n", "")
        return contents == expected_contents


def is_file_content_equal(given: str, expected: str) -> bool:
    with (
        open(given, "r") as given_file,
    ):
        contents = given_file.read().replace("\n", "")
        return contents == expected.strip().replace("\n", "")


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    origin_remote = exercise.repo.remotes.remote_or_none("origin")
    if origin_remote is not None:
        origin_remote.track_branches(["history", "care"])

    main_branch = exercise.repo.branches.branch("main")
    main_branch.checkout()
    # Verify step 1
    added_danger_commits = []
    for commit in main_branch.user_commits:
        if commit.file_change_type(DANGER_FILENAME) == "A" and len(commit.parents) == 1:
            added_danger_commits.append(commit)

    if not added_danger_commits:
        raise exercise.wrong_answer([MAIN_MISSING_DANGERS])

    if not is_file_content_equal(
        os.path.join(exercise.repo.repo.working_dir, DANGER_FILENAME), DANGER_FILE
    ):
        raise exercise.wrong_answer([MAIN_WRONG_TEXT])

    history_branch = exercise.repo.branches.branch("history")

    history_branch.checkout()
    # Verify step 2
    added_history_commits = []
    for commit in history_branch.user_commits:
        if (
            commit.file_change_type(HISTORY_FILENAME) == "A"
            and len(commit.parents) == 1
            and "main" not in commit.branches
        ):
            added_history_commits.append(commit)

    if not added_history_commits:
        raise exercise.wrong_answer([HISTORY_MISSING_HISTORY])

    if not is_file_content_equal(
        os.path.join(exercise.repo.repo.working_dir, HISTORY_FILENAME),
        HISTORY_FILE,
    ):
        raise exercise.wrong_answer([HISTORY_WRONG_TEXT])

    care_branch = exercise.repo.branches.branch("care")

    care_branch.checkout()
    # Verify step 3
    edited_care_commits = []
    for commit in care_branch.user_commits:
        if (
            commit.file_change_type(CARE_FILENAME) == "M"
            and len(commit.parents) == 1
            and (len({"main", "history"} & set(commit.branches)) == 0)
        ):
            edited_care_commits.append(commit)

    if not edited_care_commits:
        raise exercise.wrong_answer([CARE_MISSING_CARE])

    if not is_file_content_equal(
        os.path.join(exercise.repo.repo.working_dir, CARE_FILENAME),
        CARE_FILE,
    ):
        raise exercise.wrong_answer([CARE_WRONG_TEXT])

    return exercise.to_output(
        [
            "Great work on using branches to maintain the care notes for your bonsai trees!"
        ],
        GitAutograderStatus.SUCCESSFUL,
    )

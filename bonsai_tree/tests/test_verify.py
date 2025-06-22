from git_autograder import GitAutograderStatus, GitAutograderTestLoader
from git_autograder.helpers.branch_helper import BranchHelper
from git_autograder.test_utils import assert_output

from ..verify import (
    CARE_MISSING_CARE,
    CARE_WRONG_TEXT,
    HISTORY_MISSING_HISTORY,
    HISTORY_WRONG_TEXT,
    MAIN_MISSING_DANGERS,
    MAIN_WRONG_TEXT,
    verify,
)

"""
1. Add dangers-to-bonsais.txt on main
2. Branch to history
3. Add history-of-bonsais.txt on history
4. Branch to care
5. Edit bonsais-care.txt

a) Missing history branch
b) Missing care branch
c) Missing added file dangers-to-bonsais on main (A)
d) Missing added file history-of-bonsais on history (B)
e) Missing edit on bonsai-care on care (C)

f) (A) is not first
g) (B) is not second
h) (C) is not last
"""

REPOSITORY_NAME = "bonsai-tree"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_bonsai_tree():
    with loader.load("specs/bonsai-tree.yml", "start") as r:
        assert_output(r, GitAutograderStatus.SUCCESSFUL)


def test_missing_history_branch():
    with loader.load("specs/missing_history_branch.yml", "start") as r:
        assert_output(
            r,
            GitAutograderStatus.ERROR,
            [BranchHelper.MISSING_BRANCH.format(branch="history")],
        )


def test_missing_care_branch():
    with loader.load("specs/missing_care_branch.yml", "start") as r:
        assert_output(
            r,
            GitAutograderStatus.ERROR,
            [BranchHelper.MISSING_BRANCH.format(branch="care")],
        )


def test_invalid_dangers():
    with loader.load("specs/invalid_dangers.yml", "start") as r:
        assert_output(r, GitAutograderStatus.UNSUCCESSFUL, [MAIN_WRONG_TEXT])


def test_missing_dangers():
    with loader.load("specs/missing_dangers.yml", "start") as r:
        assert_output(r, GitAutograderStatus.UNSUCCESSFUL, [MAIN_MISSING_DANGERS])


def test_missing_history():
    with loader.load("specs/missing_history.yml", "start") as r:
        assert_output(r, GitAutograderStatus.UNSUCCESSFUL, [HISTORY_MISSING_HISTORY])


def test_invalid_history():
    with loader.load("specs/invalid-history.yml", "start") as r:
        assert_output(r, GitAutograderStatus.UNSUCCESSFUL, [HISTORY_WRONG_TEXT])


def test_missing_care():
    with loader.load("specs/missing-care.yml", "start") as r:
        assert_output(r, GitAutograderStatus.UNSUCCESSFUL, [CARE_MISSING_CARE])


def test_invalid_care():
    with loader.load("specs/invalid-care.yml", "start") as r:
        assert_output(r, GitAutograderStatus.UNSUCCESSFUL, [CARE_WRONG_TEXT])

from exercise_utils.test import GitAutograderTestLoader, GitMasteryHelper, assert_output
from git_autograder import GitAutograderStatus
from git_autograder.helpers.branch_helper import BranchHelper

from .verify import (
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

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)

DANGERS = "Bonsai trees are delicate and vulnerable to threats like overwatering, pests, fungal infections, and extreme temperatures. Poor pruning or wiring can cause lasting damage, while dehydration and root rot are common killers. Without careful maintenance, these miniature trees can quickly decline."
HISTORY = 'Bonsai originated in China over a thousand years ago as "penjing," the art of miniature landscape cultivation. The practice later spread to Japan, where it evolved into the refined bonsai we know today, emphasizing simplicity, balance, and harmony with nature. Traditionally associated with Zen Buddhism, bonsai became a symbol of patience and artistic expression. Over time, it gained global popularity, with enthusiasts worldwide cultivating these miniature trees as a blend of horticulture and art.'
CARE = "Proper bonsai care involves balancing water, light, and nutrients to maintain a healthy tree. Bonsais require well-draining soil and regular watering, but overwatering can lead to root rot. They need adequate sunlight, with indoor varieties thriving near bright windows and outdoor species requiring seasonal adjustments. Pruning and wiring help shape the tree, while repotting every few years ensures root health. Protecting bonsais from pests, extreme temperatures, and diseases is essential for their longevity, making their care both an art and a discipline."


def test_bonsai_tree():
    with loader.start() as (test, rs):
        rs.files.create_or_update("bonsai-care.txt")
        rs.git.add(all=True)
        rs.git.commit(message="Start")
        rs.helper(GitMasteryHelper).create_start_tag()

        rs.files.create_or_update("dangers-to-bonsais.txt", DANGERS)
        rs.git.add(all=True)
        rs.git.commit(message="Add dangers")

        rs.git.checkout("history", branch=True)
        rs.files.create_or_update("history-of-bonsais.txt", HISTORY)
        rs.git.add(all=True)
        rs.git.commit(message="Add history")

        rs.git.checkout("care", branch=True)
        rs.files.create_or_update("bonsai-care.txt", CARE)
        rs.git.add(all=True)
        rs.git.commit(message="Add bonsai care")

        rs.git.checkout("main")

        r = test.run()
        assert_output(r, GitAutograderStatus.SUCCESSFUL)


def test_missing_history_branch():
    with loader.start() as (test, rs):
        rs.files.create_or_update("bonsai-care.txt")
        rs.git.add(all=True)
        rs.git.commit(message="Start")
        rs.helper(GitMasteryHelper).create_start_tag()

        rs.files.create_or_update("dangers-to-bonsais.txt", DANGERS)
        rs.git.add(all=True)
        rs.git.commit(message="Add dangers")

        r = test.run()
        assert_output(
            r,
            GitAutograderStatus.ERROR,
            [BranchHelper.MISSING_BRANCH.format(branch="history")],
        )


def test_missing_care_branch():
    with loader.start() as (test, rs):
        rs.files.create_or_update("bonsai-care.txt")
        rs.git.add(all=True)
        rs.git.commit(message="Start")
        rs.helper(GitMasteryHelper).create_start_tag()

        rs.files.create_or_update("dangers-to-bonsais.txt", DANGERS)
        rs.git.add(all=True)
        rs.git.commit(message="Add dangers")

        rs.git.checkout("history", branch=True)
        rs.files.create_or_update("history-of-bonsais.txt", HISTORY)
        rs.git.add(all=True)
        rs.git.commit(message="Add history")

        rs.git.checkout("main")

        r = test.run()
        assert_output(
            r,
            GitAutograderStatus.ERROR,
            [BranchHelper.MISSING_BRANCH.format(branch="care")],
        )


def test_invalid_dangers():
    with loader.start() as (test, rs):
        rs.files.create_or_update("bonsai-care.txt")
        rs.git.add(all=True)
        rs.git.commit(message="Start")
        rs.helper(GitMasteryHelper).create_start_tag()

        rs.files.create_or_update("dangers-to-bonsais.txt", DANGERS[0])
        rs.git.add(all=True)
        rs.git.commit(message="Add dangers")

        rs.git.checkout("history", branch=True)
        rs.files.create_or_update("history-of-bonsais.txt", HISTORY)
        rs.git.add(all=True)
        rs.git.commit(message="Add history")

        rs.git.checkout("care", branch=True)
        rs.files.create_or_update("bonsai-care.txt", CARE)
        rs.git.add(all=True)
        rs.git.commit(message="Add bonsai care")

        rs.git.checkout("main")

        r = test.run()
        assert_output(r, GitAutograderStatus.UNSUCCESSFUL, [MAIN_WRONG_TEXT])


def test_missing_dangers():
    with loader.start() as (test, rs):
        rs.files.create_or_update("bonsai-care.txt")
        rs.git.add(all=True)
        rs.git.commit(message="Start")
        rs.helper(GitMasteryHelper).create_start_tag()

        rs.files.create_or_update("not-dangers-to-bonsais.txt", DANGERS)
        rs.git.add(all=True)
        rs.git.commit(message="Add not dangers")

        rs.git.checkout("history", branch=True)
        rs.files.create_or_update("history-of-bonsais.txt", HISTORY)
        rs.git.add(all=True)
        rs.git.commit(message="Add history")

        rs.git.checkout("care", branch=True)
        rs.files.create_or_update("bonsai-care.txt", CARE)
        rs.git.add(all=True)
        rs.git.commit(message="Add bonsai care")

        rs.git.checkout("main")

        r = test.run()
        assert_output(r, GitAutograderStatus.UNSUCCESSFUL, [MAIN_MISSING_DANGERS])


def test_missing_history():
    with loader.start() as (test, rs):
        rs.files.create_or_update("bonsai-care.txt")
        rs.git.add(all=True)
        rs.git.commit(message="Start")
        rs.helper(GitMasteryHelper).create_start_tag()

        rs.files.create_or_update("dangers-to-bonsais.txt", DANGERS)
        rs.git.add(all=True)
        rs.git.commit(message="Add dangers")

        rs.git.checkout("history", branch=True)
        rs.files.create_or_update("not-history-of-bonsais.txt", HISTORY)
        rs.git.add(all=True)
        rs.git.commit(message="Add not history")

        rs.git.checkout("care", branch=True)
        rs.files.create_or_update("bonsai-care.txt", CARE)
        rs.git.add(all=True)
        rs.git.commit(message="Add bonsai care")

        rs.git.checkout("main")

        r = test.run()
        assert_output(r, GitAutograderStatus.UNSUCCESSFUL, [HISTORY_MISSING_HISTORY])


def test_invalid_history():
    with loader.start() as (test, rs):
        rs.files.create_or_update("bonsai-care.txt")
        rs.git.add(all=True)
        rs.git.commit(message="Start")
        rs.helper(GitMasteryHelper).create_start_tag()

        rs.files.create_or_update("dangers-to-bonsais.txt", DANGERS)
        rs.git.add(all=True)
        rs.git.commit(message="Add dangers")

        rs.git.checkout("history", branch=True)
        rs.files.create_or_update("history-of-bonsais.txt", HISTORY[0])
        rs.git.add(all=True)
        rs.git.commit(message="Add history")

        rs.git.checkout("care", branch=True)
        rs.files.create_or_update("bonsai-care.txt", CARE)
        rs.git.add(all=True)
        rs.git.commit(message="Add bonsai care")

        rs.git.checkout("main")

        r = test.run()
        assert_output(r, GitAutograderStatus.UNSUCCESSFUL, [HISTORY_WRONG_TEXT])


def test_missing_care():
    with loader.start() as (test, rs):
        rs.files.create_or_update("bonsai-care.txt")
        rs.git.add(all=True)
        rs.git.commit(message="Start")
        rs.helper(GitMasteryHelper).create_start_tag()

        rs.files.create_or_update("dangers-to-bonsais.txt", DANGERS)
        rs.git.add(all=True)
        rs.git.commit(message="Add dangers")

        rs.git.checkout("history", branch=True)
        rs.files.create_or_update("history-of-bonsais.txt", HISTORY)
        rs.git.add(all=True)
        rs.git.commit(message="Add history")

        rs.git.checkout("care", branch=True)
        rs.files.create_or_update("not-bonsai-care.txt", CARE)
        rs.git.add(all=True)
        rs.git.commit(message="Add not bonsai care")

        rs.git.checkout("main")

        r = test.run()
        assert_output(r, GitAutograderStatus.UNSUCCESSFUL, [CARE_MISSING_CARE])


def test_invalid_care():
    with loader.start() as (test, rs):
        rs.files.create_or_update("bonsai-care.txt")
        rs.git.add(all=True)
        rs.git.commit(message="Start")
        rs.helper(GitMasteryHelper).create_start_tag()

        rs.files.create_or_update("dangers-to-bonsais.txt", DANGERS)
        rs.git.add(all=True)
        rs.git.commit(message="Add dangers")

        rs.git.checkout("history", branch=True)
        rs.files.create_or_update("history-of-bonsais.txt", HISTORY)
        rs.git.add(all=True)
        rs.git.commit(message="Add history")

        rs.git.checkout("care", branch=True)
        rs.files.create_or_update("bonsai-care.txt", CARE[0])
        rs.git.add(all=True)
        rs.git.commit(message="Add bonsai care")

        rs.git.checkout("main")

        r = test.run()
        assert_output(r, GitAutograderStatus.UNSUCCESSFUL, [CARE_WRONG_TEXT])

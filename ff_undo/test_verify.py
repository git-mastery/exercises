from exercise_utils.test import GitAutograderTestLoader, GitMasteryHelper, assert_output
from git_autograder.status import GitAutograderStatus

from .verify import (
    MAIN_COMMITS_INCORRECT,
    MERGE_NOT_UNDONE,
    OTHERS_BRANCH_MISSING,
    OTHERS_COMMITS_INCORRECT,
    verify,
)

REPOSITORY_NAME = "ff-undo"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


def test_correct_solution():
    with loader.start() as (test, rs):
        rs.git.commit(message="Set initial state", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        rs.git.commit(message="Add Rick", allow_empty=True)
        rs.git.commit(message="Add Morty", allow_empty=True)

        rs.git.checkout("others", branch=True)

        rs.git.commit(message="Add Birdperson", allow_empty=True)
        rs.git.commit(message="Add Cyborg to birdperson.txt", allow_empty=True)
        rs.git.commit(message="Add Tammy", allow_empty=True)

        rs.git.checkout("main")

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_merge_not_undone():
    with loader.start() as (test, rs):
        rs.git.commit(message="Set initial state", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        rs.git.commit(message="Add Rick", allow_empty=True)
        rs.git.commit(message="Add Morty", allow_empty=True)

        rs.git.checkout("others", branch=True)

        rs.git.commit(message="Add Birdperson", allow_empty=True)
        rs.git.commit(message="Add Cyborg to birdperson.txt", allow_empty=True)
        rs.git.commit(message="Add Tammy", allow_empty=True)

        rs.git.checkout("main")
        rs.git.merge("others", message="Introduce others")

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [MERGE_NOT_UNDONE])


def test_branch_missing():
    with loader.start() as (test, rs):
        rs.git.commit(message="Set initial state", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        rs.git.commit(message="Add Rick", allow_empty=True)
        rs.git.commit(message="Add Morty", allow_empty=True)

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [OTHERS_BRANCH_MISSING])


def test_main_commits_incorrect():
    with loader.start() as (test, rs):
        rs.git.commit(message="Set initial state", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        rs.git.commit(message="Add Morty", allow_empty=True)

        rs.git.checkout("others", branch=True)

        rs.git.commit(message="Add Birdperson", allow_empty=True)
        rs.git.commit(message="Add Cyborg to birdperson.txt", allow_empty=True)
        rs.git.commit(message="Add Tammy", allow_empty=True)

        rs.git.checkout("main")

        output = test.run()
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [MAIN_COMMITS_INCORRECT]
        )


def test_others_commits_incorrect():
    with loader.start() as (test, rs):
        rs.git.commit(message="Set initial state", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        rs.git.commit(message="Add Rick", allow_empty=True)
        rs.git.commit(message="Add Morty", allow_empty=True)

        rs.git.checkout("others", branch=True)

        rs.git.commit(message="Add Birdperson", allow_empty=True)
        rs.git.commit(message="Add Tammy", allow_empty=True)

        rs.git.checkout("main")

        output = test.run()
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [OTHERS_COMMITS_INCORRECT]
        )

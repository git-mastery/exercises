from exercise_utils.test import GitAutograderTestLoader, assert_output
from git_autograder import GitAutograderStatus
from repo_smith.repo_smith import RepoSmith

from .verify import (
    CHANGES_FROM_SUPPORTING_NOT_PRESENT,
    MAIN_COMMITS_INCORRECT,
    SQUASH_NOT_USED,
    SQUASH_ON_SUPPORTING,
    verify,
)

REPOSITORY_NAME = "merge-squash"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


def _create_and_commit_file(
    rs: RepoSmith, filename: str, contents: str, commit_message: str
) -> None:
    rs.files.create_or_update(filename, contents)
    rs.git.add(filename)
    rs.git.commit(message=commit_message)


def test_base():
    with loader.start() as (test, rs):
        _create_and_commit_file(rs, "joey.txt", "Matt LeBlanc", "Add Joey")
        _create_and_commit_file(rs, "phoebe.txt", "Lisa Kudrow", "Add Phoebe")

        rs.git.checkout("supporting", branch=True)

        _create_and_commit_file(rs, "mike.txt", "Paul Rudd", "Add Mike")
        _create_and_commit_file(rs, "janice.txt", "Maggie Wheeler", "Add Janice")

        rs.git.checkout("main")

        _create_and_commit_file(rs, "ross.txt", "David Schwimmer", "Add Ross")

        rs.git.merge("supporting", squash=True)
        rs.git.commit(message="Squash commit")

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_non_squash_merge_used():
    with loader.start() as (test, rs):
        _create_and_commit_file(rs, "joey.txt", "Matt LeBlanc", "Add Joey")
        _create_and_commit_file(rs, "phoebe.txt", "Lisa Kudrow", "Add Phoebe")

        rs.git.checkout("supporting", branch=True)

        _create_and_commit_file(rs, "mike.txt", "Paul Rudd", "Add Mike")
        _create_and_commit_file(rs, "janice.txt", "Maggie Wheeler", "Add Janice")

        rs.git.checkout("main")

        _create_and_commit_file(rs, "ross.txt", "David Schwimmer", "Add Ross")

        rs.git.merge("supporting")

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [SQUASH_NOT_USED])


def test_not_merged():
    with loader.start() as (test, rs):
        _create_and_commit_file(rs, "joey.txt", "Matt LeBlanc", "Add Joey")
        _create_and_commit_file(rs, "phoebe.txt", "Lisa Kudrow", "Add Phoebe")

        rs.git.checkout("supporting", branch=True)

        _create_and_commit_file(rs, "mike.txt", "Paul Rudd", "Add Mike")
        _create_and_commit_file(rs, "janice.txt", "Maggie Wheeler", "Add Janice")

        rs.git.checkout("main")

        _create_and_commit_file(rs, "ross.txt", "David Schwimmer", "Add Ross")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [CHANGES_FROM_SUPPORTING_NOT_PRESENT],
        )


def test_missing_main_commits():
    with loader.start() as (test, rs):
        _create_and_commit_file(rs, "joey.txt", "Matt LeBlanc", "Add Joey")

        rs.git.checkout("supporting", branch=True)

        _create_and_commit_file(rs, "mike.txt", "Paul Rudd", "Add Mike")
        _create_and_commit_file(rs, "janice.txt", "Maggie Wheeler", "Add Janice")

        rs.git.checkout("main")

        _create_and_commit_file(rs, "ross.txt", "David Schwimmer", "Add Ross")

        rs.git.merge("supporting", squash=True)
        rs.git.commit(message="Squash commit")

        output = test.run()
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [MAIN_COMMITS_INCORRECT]
        )


def test_wrong_branch_squashed():
    with loader.start() as (test, rs):
        _create_and_commit_file(rs, "joey.txt", "Matt LeBlanc", "Add Joey")
        _create_and_commit_file(rs, "phoebe.txt", "Lisa Kudrow", "Add Phoebe")

        rs.git.checkout("supporting", branch=True)

        _create_and_commit_file(rs, "mike.txt", "Paul Rudd", "Add Mike")
        _create_and_commit_file(rs, "janice.txt", "Maggie Wheeler", "Add Janice")

        rs.git.checkout("main")

        _create_and_commit_file(rs, "ross.txt", "David Schwimmer", "Add Ross")

        rs.git.checkout("supporting")
        rs.git.merge("main", squash=True)
        rs.git.commit(message="Squash commit")

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [SQUASH_ON_SUPPORTING])

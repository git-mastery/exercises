from exercise_utils.test import GitAutograderTestLoader, assert_output
from git_autograder import GitAutograderStatus
from repo_smith.repo_smith import RepoSmith

from .verify import (
    MAIN_WRONG_COMMIT,
    MERGES_NOT_UNDONE,
    NOT_ON_MAIN,
    RESET_MESSAGE,
    verify,
)

REPOSITORY_NAME = "merge-undo"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


def _create_and_commit_file(
    rs: RepoSmith, filename: str, contents: str, commit_message: str
) -> None:
    rs.files.create_or_update(filename, contents)
    rs.git.add(filename)
    rs.git.commit(message=commit_message)


def test_base():
    with loader.start() as (test, rs):
        _create_and_commit_file(rs, "rick.txt", "Scientist", "Add Rick")
        _create_and_commit_file(rs, "morty.txt", "Boy", "Add Morty")

        rs.git.checkout("daughter", branch=True)
        _create_and_commit_file(rs, "beth.txt", "Vet", "Add Beth")

        rs.git.checkout("main")
        rs.git.checkout("son-in-law", branch=True)
        _create_and_commit_file(rs, "jerry.txt", "Salesman", "Add Jerry")

        rs.git.checkout("main")
        _create_and_commit_file(
            rs,
            "morty.txt",
            """
            Boy
            Grandson
            """,
            "Mention Morty is grandson",
        )

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_merges_not_undone():
    with loader.start() as (test, rs):
        _create_and_commit_file(rs, "rick.txt", "Scientist", "Add Rick")
        _create_and_commit_file(rs, "morty.txt", "Boy", "Add Morty")

        rs.git.checkout("daughter", branch=True)
        _create_and_commit_file(rs, "beth.txt", "Vet", "Add Beth")

        rs.git.checkout("main")
        rs.git.checkout("son-in-law", branch=True)
        _create_and_commit_file(rs, "jerry.txt", "Salesman", "Add Jerry")

        rs.git.checkout("main")
        _create_and_commit_file(
            rs,
            "morty.txt",
            """
            Boy
            Grandson
            """,
            "Mention Morty is grandson",
        )
        rs.git.merge("daughter", message="Int", no_ff=True)
        rs.git.merge("son-in-law", message="introduce Jerry", no_ff=True)

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [MERGES_NOT_UNDONE, RESET_MESSAGE],
        )


def test_main_wrong_commit():
    with loader.start() as (test, rs):
        _create_and_commit_file(rs, "rick.txt", "Scientist", "Add Rick")
        _create_and_commit_file(rs, "morty.txt", "Boy", "Add Morty")

        rs.git.checkout("daughter", branch=True)
        _create_and_commit_file(rs, "beth.txt", "Vet", "Add Beth")

        rs.git.checkout("main")
        rs.git.checkout("son-in-law", branch=True)
        _create_and_commit_file(rs, "jerry.txt", "Salesman", "Add Jerry")

        rs.git.checkout("main")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [MAIN_WRONG_COMMIT, RESET_MESSAGE],
        )


def test_not_main():
    with loader.start() as (test, rs):
        _create_and_commit_file(rs, "rick.txt", "Scientist", "Add Rick")
        _create_and_commit_file(rs, "morty.txt", "Boy", "Add Morty")

        rs.git.checkout("daughter", branch=True)
        _create_and_commit_file(rs, "beth.txt", "Vet", "Add Beth")

        rs.git.checkout("main")
        rs.git.checkout("son-in-law", branch=True)
        _create_and_commit_file(rs, "jerry.txt", "Salesman", "Add Jerry")

        rs.git.checkout("main")
        _create_and_commit_file(
            rs,
            "morty.txt",
            """
            Boy
            Grandson
            """,
            "Mention Morty is grandson",
        )
        rs.git.checkout("daughter")

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [NOT_ON_MAIN])

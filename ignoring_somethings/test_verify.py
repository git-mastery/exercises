from exercise_utils.test import GitAutograderTestLoader, GitMasteryHelper, assert_output
from git_autograder import GitAutograderStatus
from repo_smith.repo_smith import RepoSmith

from .verify import (
    NOT_IGNORING_IGNORE_ME,
    NOT_IGNORING_REST_OF_MANY,
    NOT_IGNORING_RUNAWAY,
    NOT_PATTERN_MATCHING_RUNAWAY,
    STILL_HIDING,
    STILL_IGNORING_FILE_22,
    verify,
)

REPOSITORY_NAME = "ignoring-somethings"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


def _create_and_commit_file(
    rs: RepoSmith, filename: str, contents: str, commit_message: str
) -> None:
    rs.files.create_or_update(filename, contents)
    rs.git.add(filename)
    rs.git.commit(message=commit_message)


def test_valid():
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        _create_and_commit_file(
            rs,
            ".gitignore",
            """
            many/*
            !many/file22.txt
            ignore_me.txt
            this/**/runaway.txt
            """,
            "Add .gitignore",
        )

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.SUCCESSFUL,
            ["Great work using .gitignore!"],
        )


def test_no_change():
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        _create_and_commit_file(
            rs,
            ".gitignore",
            """
            many/*
            why_am_i_hidden.txt
            """,
            "Add .gitignore",
        )

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                STILL_IGNORING_FILE_22,
                STILL_HIDING,
                NOT_IGNORING_IGNORE_ME,
                NOT_IGNORING_RUNAWAY,
            ],
        )


def test_overriding():
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        _create_and_commit_file(
            rs,
            ".gitignore",
            """
            many/*
            !many/file22.txt
            ignore_me.txt
            this/**/runaway.txt
            !why_am_i_hidden.txt
            why_am_i_hidden.*
            """,
            "Add .gitignore",
        )

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                STILL_HIDING,
            ],
        )


def test_overriding_many():
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        _create_and_commit_file(
            rs,
            ".gitignore",
            """
            many/*
            !many/file22.txt
            !many/*
            ignore_me.txt
            this/**/runaway.txt
            """,
            "Add .gitignore",
        )

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [NOT_IGNORING_REST_OF_MANY],
        )


def test_not_pattern_matching():
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        _create_and_commit_file(
            rs,
            ".gitignore",
            """
            many/*
            !many/file22.txt
            ignore_me.txt
            this/is/very/nested/runaway.txt
            """,
            "Add .gitignore",
        )

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [NOT_PATTERN_MATCHING_RUNAWAY],
        )

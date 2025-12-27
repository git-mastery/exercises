from contextlib import contextmanager
from typing import Iterator, Tuple

from exercise_utils.test import (
    GitAutograderTest,
    GitAutograderTestLoader,
    GitMasteryHelper,
    assert_output,
)
from git_autograder import GitAutograderStatus
from repo_smith.repo_smith import RepoSmith

from .verify import EMPTY_COMMITS, NO_ADD, NO_REMOVE, WRONG_FILE, verify

REPOSITORY_NAME = "grocery-shopping"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


@contextmanager
def base_setup() -> Iterator[Tuple[GitAutograderTest, RepoSmith]]:
    with loader.start() as (test, rs):
        rs.files.create_or_update("README.md", "Hello world")
        rs.files.create_or_update(
            "shopping-list.txt",
            """
            - Milk
            - Eggs
            - Bread
            - Apples
            - Ham
            """,
        )
        rs.git.add(["README.md", "shopping-list.txt"])
        rs.git.commit(message="Initial commit")
        rs.helper(GitMasteryHelper).create_start_tag()

        yield test, rs


def test_no_changes():
    with base_setup() as (test, rs):
        rs.git.commit(message="Commit", allow_empty=True)

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [EMPTY_COMMITS])


def test_wrong_file():
    with base_setup() as (test, rs):
        rs.files.create_or_update("README.md", "Goodbye")
        rs.git.add(all=True)
        rs.git.commit(message="Update README.md")

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [WRONG_FILE])


def test_only_edit():
    with base_setup() as (test, rs):
        rs.files.create_or_update(
            "shopping-list.txt",
            """
            - Milk
            - Eggs
            - Bread
            - Apples
            - Ham1
            """,
        )
        rs.git.add(all=True)
        rs.git.commit(message="Update shopping list")

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_no_add():
    with base_setup() as (test, rs):
        rs.files.create_or_update("shopping-list.txt", "- Milk")
        rs.git.add(all=True)
        rs.git.commit(message="Update shopping list")

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [NO_ADD])


def test_no_remove():
    with base_setup() as (test, rs):
        rs.files.create_or_update(
            "shopping-list.txt",
            """
            - Milk
            - Eggs
            - Bread
            - Apples
            - Ham
            - Chicken
            """,
        )
        rs.git.add(all=True)
        rs.git.commit(message="Update shopping list")

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [NO_REMOVE])


def test_one_shot():
    with base_setup() as (test, rs):
        rs.files.create_or_update(
            "shopping-list.txt",
            """
            - Milk
            - Eggs
            - Bread
            - Apples
            - Chicken
            """,
        )
        rs.git.add(all=True)
        rs.git.commit(message="Update shopping list")

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_complex():
    with base_setup() as (test, rs):
        rs.files.create_or_update(
            "shopping-list.txt",
            """
            - Milk
            - Eggs
            - Bread
            - Apples
            """,
        )
        rs.git.add(all=True)
        rs.git.commit(message="Delete item")

        rs.files.create_or_update(
            "shopping-list.txt",
            """
            - Milk
            - Eggs
            - Bread
            - Apples
            - Chicken
            """,
        )
        rs.git.add(all=True)
        rs.git.commit(message="Add item")

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)

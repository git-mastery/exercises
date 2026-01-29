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

from .verify import (
    ADD_NOT_COMMITTED,
    NO_ADD,
    NO_REMOVE,
    REMOVE_NOT_COMMITTED,
    SHOPPING_LIST_FILE_MISSING,
    verify,
)

REPOSITORY_NAME = "grocery-shopping"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


@contextmanager
def base_setup() -> Iterator[Tuple[GitAutograderTest, RepoSmith]]:
    with loader.start() as (test, rs):
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
        rs.git.add(["shopping-list.txt"])
        rs.git.commit(message="Initial commit")
        rs.helper(GitMasteryHelper).create_start_tag()

        yield test, rs


def test_no_changes():
    with base_setup() as (test, rs):
        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [NO_ADD, NO_REMOVE])


def test_add_new_file():
    with base_setup() as (test, rs):
        rs.files.create_or_update("new-file.txt", "New file content")

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [NO_ADD, NO_REMOVE])


def test_delete_file():
    with base_setup() as (test, rs):
        rs.files.delete("shopping-list.txt")

        output = test.run()
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [SHOPPING_LIST_FILE_MISSING]
        )


def test_add_only():
    with base_setup() as (test, rs):
        rs.files.append(
            "shopping-list.txt",
            "- Chicken\n",
        )

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [NO_REMOVE])


def test_remove_only():
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

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [NO_ADD])


def test_changes_not_committed():
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

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [ADD_NOT_COMMITTED, REMOVE_NOT_COMMITTED],
        )


def test_add_committed_only():
    with base_setup() as (test, rs):
        rs.files.append(
            "shopping-list.txt",
            "- Chicken\n",
        )
        rs.git.add(all=True)
        rs.git.commit(message="Add Chicken to shopping list")

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

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [REMOVE_NOT_COMMITTED])


def test_remove_committed_only():
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
        rs.git.commit(message="Add Chicken to shopping list")

        rs.files.append(
            "shopping-list.txt",
            "- Chicken\n",
        )

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [ADD_NOT_COMMITTED])


def test_successful_change():
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

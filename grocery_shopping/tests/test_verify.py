from git_autograder import (
    GitAutograderStatus,
    GitAutograderTestLoader,
    assert_output,
)

from ..verify import EMPTY_COMMITS, NO_ADD, NO_REMOVE, WRONG_FILE, verify

REPOSITORY_NAME = "grocery-shopping"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_no_changes():
    with loader.load("specs/no_changes.yml", "start") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [EMPTY_COMMITS])


def test_wrong_file():
    with loader.load("specs/wrong_file.yml", "start") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [WRONG_FILE])


def test_only_edit():
    with loader.load("specs/only_edit.yml", "start") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [NO_ADD, NO_REMOVE])


def test_no_add():
    with loader.load("specs/no_add.yml", "start") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [NO_ADD])


def test_no_remove():
    with loader.load("specs/no_remove.yml", "start") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [NO_REMOVE])


def test_one_shot():
    with loader.load("specs/one_shot.yml", "start") as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_complex():
    with loader.load("specs/complex.yml", "start") as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL)

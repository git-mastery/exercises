from exercise_utils.test import GitAutograderTestLoader, assert_output
from git_autograder import GitAutograderStatus

from .verify import (
    MERGE_NOT_RESOLVED,
    NOT_ON_MAIN,
    RESET_MESSAGE,
    UNCOMMITTED_CHANGES,
    verify,
)

REPOSITORY_NAME = "conflict-mediator"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


def test_base():
    with loader.start() as (test, rs):
        rs.files.create_or_update("script.py", 'print("Hello Everyone and World!")')
        rs.git.add("script.py")
        rs.git.commit(message="Fix print")

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_base_single_quotes():
    with loader.start() as (test, rs):
        rs.files.create_or_update("script.py", "print('Hello Everyone and World!')")
        rs.git.add("script.py")
        rs.git.commit(message="Fix print")

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_no_fix():
    with loader.start() as (test, rs):
        rs.files.create_or_update("script.py", "print('Hello World!')")
        rs.git.add("script.py")
        rs.git.commit(message="Fix print")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [MERGE_NOT_RESOLVED, RESET_MESSAGE],
        )


def test_uncommitted():
    with loader.start() as (test, rs):
        rs.files.create_or_update("test.txt", "hi")
        rs.git.add("test.txt")
        rs.git.commit(message="Start")
        rs.files.create_or_update("test.txt", "changed")

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [UNCOMMITTED_CHANGES])


def test_not_main():
    with loader.start() as (test, rs):
        rs.git.checkout("bug-fix", branch=True)

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [NOT_ON_MAIN])
